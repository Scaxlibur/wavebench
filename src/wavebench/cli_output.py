from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np

from .arbitrary import (
    load_arbitrary_waveform,
    validate_waveform_name,
    write_arbitrary_payload_json,
    write_dg4000_dac14_binary_block,
)
from .data.fft import analyze_fft, fft_harmonics
from .drivers.dg4202 import SourceStatus
from .drivers.dm3000 import DmmReading
from .drivers.dp800 import PowerProtectionStatus, PowerStatus
from .drivers.rtm2032 import WaveformData
from .errors import ConfigError
from .plugins.api import InstrumentPlugin
from .services.run_plan import RunPlan, RunStep




def _print_plugin_list(plugins: list[InstrumentPlugin]) -> None:
    if not plugins:
        print("no_plugins_found / 未发现插件")
        return
    print("driver_id	kind	origin	models	capabilities")
    for plugin in plugins:
        print(
            f"{plugin.driver_id}	{plugin.kind}	{plugin.origin}	"
            f"{plugin.model_text}	{plugin.capability_text}"
        )


def _print_plugin_info(plugin: InstrumentPlugin) -> None:
    print(f"driver_id={plugin.driver_id}")
    print(f"kind={plugin.kind}")
    print(f"display_name={plugin.display_name}")
    print(f"manufacturer={plugin.manufacturer}")
    print(f"models={plugin.model_text}")
    print(f"origin={plugin.origin}")
    print(f"package={plugin.package}")
    print(f"api_version={plugin.api_version}")
    print(f"summary={plugin.summary}")
    print("capabilities=" + plugin.capability_text)
    if plugin.idn_patterns:
        print("idn_patterns=" + ", ".join(plugin.idn_patterns))
    if plugin.config_fields:
        print("config_fields=" + ", ".join(plugin.config_fields))

def _format_step_summary(step: RunStep) -> str:
    if not step.fields:
        return f"{step.index}: {step.kind}"
    fields = " ".join(f"{key}={value}" for key, value in step.fields.items())
    return f"{step.index}: {step.kind} {fields}"


def _print_run_plan_summary(plan: RunPlan) -> None:
    print(f"plan={plan.path}")
    print(f"experiment={plan.name} label={plan.label}")
    if plan.safety.require_scope_coupling_not:
        blocked = ",".join(plan.safety.require_scope_coupling_not)
        print(f"safety: scope CH{plan.safety.scope_guard_channel} coupling not in [{blocked}]")
    else:
        print("safety: none")
    if plan.restore.source_state:
        if plan.restore.source_channels:
            channels = ",".join(str(channel) for channel in plan.restore.source_channels)
        else:
            channels = "default"
        print(f"restore: source state channels={channels}")
    else:
        print("restore: none")
    print(f"steps={len(plan.steps)}")
    for step in plan.steps:
        print(_format_step_summary(step))



def _print_run_preflight(records: list[Any]) -> None:
    print("verify=ok / 预检=通过")
    for record in records:
        print(f"instrument/仪器={record.instrument} resource/资源={record.resource} idn={record.idn}")

def _print_dmm_reading(reading: DmmReading) -> None:
    print(f"{reading.function}: {reading.value:.12g} {reading.unit} raw={reading.raw}")

def _print_dmm_function_status(function: str) -> None:
    print(f"功能 / Function: {function}")


def _print_dmm_function_set(function: str) -> None:
    print(f"功能已切换 / Function set: {function}")


def _print_power_status(status: PowerStatus) -> None:
    set_value = f"{status.set_voltage_v}V/{status.set_current_a}A"
    measured = f"{status.measured_voltage_v}V/{status.measured_current_a}A/{status.measured_power_w}W"
    print(f"CH{status.channel}: output={status.output} mode={status.mode} set={set_value} measured={measured} rating={status.rating}")


def _print_power_protection_status(status: PowerProtectionStatus) -> None:
    ovp = f"enabled={status.ovp_enabled} threshold={status.ovp_threshold_v}V tripped={status.ovp_tripped}"
    ocp = f"enabled={status.ocp_enabled} threshold={status.ocp_threshold_a}A tripped={status.ocp_tripped}"
    print(f"CH{status.channel} protection / 保护: OVP {ovp}; OCP {ocp}")


def _print_source_status(status: SourceStatus) -> None:
    duty = "" if status.square_duty_cycle_percent is None else f" duty={status.square_duty_cycle_percent}%"
    print(f"CH{status.channel}: output={status.output} func={status.function} freq={status.frequency_hz}Hz amp={status.amplitude}{status.amplitude_unit or ''}{duty} offset={status.offset_v}V phase={status.phase_deg}deg")
    print(f"mode={status.frequency_mode} sweep={status.sweep_enabled}")
    if status.apply_raw is not None:
        print(f"apply={status.apply_raw}")


def _print_capture_package_summary(package) -> None:
    print(f"package={package.path}")
    print(f"metadata={package.metadata_path}")
    command = package.operation.get("command", "")
    if command:
        print(f"operation={command}")
    resource = package.instrument.get("resource", "")
    if resource:
        print(f"resource={resource}")
    print(f"channels={','.join(str(channel.channel) for channel in package.channels)}")
    for channel in package.channels:
        summary = channel.summary
        print(f"CH{channel.channel}")
        if "samples" in summary:
            print(f"  samples={summary['samples']}")
        if "x_increment_s" in summary:
            print(f"  dt={summary['x_increment_s']:.6e} s")
        if "voltage_vpp_v" in summary:
            print(f"  vpp={summary['voltage_vpp_v']:.6g} V")
        if "voltage_rms_v" in summary:
            print(f"  rms={summary['voltage_rms_v']:.6g} V")
        if "voltage_mean_v" in summary:
            print(f"  mean={summary['voltage_mean_v']:.6g} V")
        if summary.get("frequency_estimate_hz") is not None:
            print(f"  frequency≈{summary['frequency_estimate_hz']:.6g} Hz")
        if summary.get("duty_cycle") is not None:
            print(f"  duty={summary['duty_cycle']:.6g}")
        if summary.get("rise_time_s") is not None:
            print(f"  rise_time={summary['rise_time_s']:.6e} s")
        if summary.get("fall_time_s") is not None:
            print(f"  fall_time={summary['fall_time_s']:.6e} s")
        warnings = summary.get("quality_warnings", [])
        for warning in warnings:
            print(f"  warning={warning}")
        for kind, path in sorted(channel.files.items()):
            print(f"  {kind}={path}")


def _print_capture_fft_summary(
    package,
    *,
    max_harmonic_order: int = 5,
    expected_frequency_hz: float | None = None,
    frequency_tolerance_ratio: float = 0.05,
) -> None:
    if max_harmonic_order < 1:
        raise ConfigError("--harmonics must be >= 1")
    if expected_frequency_hz is not None and expected_frequency_hz <= 0:
        raise ConfigError("--fft-expect-frequency must be > 0")
    if frequency_tolerance_ratio < 0:
        raise ConfigError("--fft-frequency-tolerance must be >= 0")
    print("FFT")
    for channel in package.channels:
        npy_text = channel.files.get("npy")
        print(f"CH{channel.channel}")
        if not npy_text:
            print("  warning=missing npy artifact")
            continue
        npy_path = _resolve_capture_file_path(package.path, npy_text)
        try:
            analysis = _analyze_fft(np.load(npy_path), max_harmonic_order=max_harmonic_order)
        except Exception as exc:  # report-style inspect should keep other channels readable
            print(f"  warning=fft unavailable: {type(exc).__name__}: {exc}")
            continue
        print(f"  window={analysis['window']}")
        print(f"  samples={analysis['samples']}")
        print(f"  sample_rate≈{analysis['sample_rate_hz']:.6g} Hz")
        print(f"  resolution≈{analysis['resolution_hz']:.6g} Hz")
        print(f"  peak_frequency≈{analysis['peak_frequency_hz']:.6g} Hz")
        if expected_frequency_hz is not None:
            error_ratio = abs(analysis["peak_frequency_hz"] - expected_frequency_hz) / expected_frequency_hz
            print(f"  peak_frequency_error≈{error_ratio:.3%}")
            print(f"  peak_frequency_ok={error_ratio <= frequency_tolerance_ratio}")
        print(f"  peak_amplitude≈{analysis['peak_amplitude_v']:.6g} V")
        print(f"  noise_floor≈{analysis['noise_floor_v']:.6g} V")
        thd = analysis.get("thd_ratio")
        if thd is not None:
            print(f"  thd≈{thd:.3%}")
        for harmonic in analysis["harmonics"]:
            print(
                f"  harmonic_{harmonic['order']:g}≈{harmonic['frequency_hz']:.6g} Hz "
                f"amplitude≈{harmonic['amplitude_v']:.6g} V"
            )
        for warning in analysis["warnings"]:
            print(f"  warning={warning}")



def _analyze_fft(waveform: Any, *, max_harmonic_order: int = 5) -> dict[str, Any]:
    return analyze_fft(waveform, max_harmonic_order=max_harmonic_order)


def _fft_harmonics(
    frequencies: Any, amplitudes: Any, fundamental_hz: float, *, max_order: int = 5
) -> list[dict[str, float]]:
    return fft_harmonics(frequencies, amplitudes, fundamental_hz, max_order=max_order)


def _resolve_capture_file_path(package_dir: Path, file_text: str) -> Path:
    path = Path(file_text.replace("\\", "/"))
    if path.is_absolute() or path.exists():
        return path
    root = _project_root_from_capture_path(package_dir)
    candidate = root / path
    if candidate.exists():
        return candidate
    return package_dir / path.name


def _project_root_from_capture_path(package_dir: Path) -> Path:
    parts = package_dir.parts
    if len(parts) >= 3 and parts[-3:-1] == ("data", "raw"):
        return Path(*parts[:-3]) if len(parts[:-3]) > 0 else Path(".")
    return package_dir.parent


def _print_discovery_results(results: list[Any]) -> None:
    if not results:
        print("no_instruments_found / 未发现仪器")
        return
    print("address	port	status	protocol	source	resource	idn	note")
    for item in results:
        port = "" if item.port is None else str(item.port)
        idn = "" if item.idn is None else item.idn
        print(
            f"{item.address}	{port}	{item.status}	{item.protocol}	"
            f"{item.source}	{item.resource}	{idn}	{item.note}"
        )


def _print_arbitrary_probe_results(results: list[Any]) -> None:
    for item in results:
        response = "" if item.response is None else item.response
        exception = "" if item.exception is None else f" exception={item.exception}"
        active_errors = [err for err in item.errors if not (err.startswith("0") or "No error" in err)]
        error_text = " | ".join(active_errors) if active_errors else "0"
        print(
            f"{item.label}: accepted={item.accepted} command={item.command} "
            f"response={response} errors={error_text}{exception}"
        )


def _print_arbitrary_waveform_summary(args: argparse.Namespace, *, dry_run: bool = True) -> None:
    name = validate_waveform_name(args.name)
    waveform = load_arbitrary_waveform(
        args.file,
        sample_rate_hz=args.sample_rate,
        max_points=args.max_points,
    )
    summary = waveform.summary()
    print(f"arb_name={name}")
    print(f"channel={args.channel}")
    print(f"file={summary['source_path']}")
    print(f"points={summary['points']}")
    print(f"input={summary['input_min']:.6g}..{summary['input_max']:.6g} mean={summary['input_mean']:.6g}")
    print(f"normalized={summary['normalized_min']:.6g}..{summary['normalized_max']:.6g}")
    print(f"dac14={summary['dac14_min']}..{summary['dac14_max']}")
    if summary["sample_rate_hz"] is not None:
        print(f"sample_rate={summary['sample_rate_hz']:.6g} Hz")
    print(f"amplitude={args.amplitude:.6g} Vpp")
    if args.frequency is not None:
        print(f"frequency={args.frequency:.6g} Hz")
    print(f"offset={args.offset:.6g} V")
    print(f"output_on={bool(args.output_on)}")
    if args.export_payload:
        output = write_arbitrary_payload_json(
            waveform,
            args.export_payload,
            name=name,
            channel=args.channel,
            amplitude_vpp=args.amplitude,
            offset_v=args.offset,
        )
        print(f"payload={output}")
    if args.export_dg4000_dac_block:
        output = write_dg4000_dac14_binary_block(
            waveform,
            args.export_dg4000_dac_block,
            byte_order=args.dg4000_byte_order,
        )
        print(f"dg4000_dac_block={output}")
        print(f"dg4000_byte_order={args.dg4000_byte_order}")
        print("dg4000_byte_order_status=dg4202_hardware_validated_2026-05-01")
    print(f"dry_run={str(dry_run).lower()}")
    if dry_run:
        print("upload=not_requested")


def _print_waveform_summary(waveform: WaveformData) -> None:
    summary = waveform.summary()
    print(f"CH{summary['channel']} waveform fetched")
    print(f"samples={summary['samples']}")
    print(f"time={summary['x_start_s']:.6e}..{summary['x_stop_s']:.6e} s")
    print(f"dt={summary['x_increment_s']:.6e} s")
    print(f"voltage={summary['voltage_min_v']:.6g}..{summary['voltage_max_v']:.6g} V")
    print(f"vpp={summary['voltage_vpp_v']:.6g} V")
    print(f"rms={summary['voltage_rms_v']:.6g} V")
    print(f"mean={summary['voltage_mean_v']:.6g} V")
    frequency = summary.get("frequency_estimate_hz")
    if frequency is not None:
        print(f"frequency≈{frequency:.6g} Hz")
    estimated_cycles = summary.get("estimated_cycles")
    if estimated_cycles is not None:
        print(f"estimated_cycles≈{estimated_cycles:.3g}")
    frequency_error = summary.get("frequency_error_ratio")
    if frequency_error is not None:
        print(f"frequency_error≈{frequency_error:.3%}")
    for warning in summary.get("quality_warnings", []):
        print(f"warning={warning}")


