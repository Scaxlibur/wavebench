from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import numpy as np

from .config import load_config
from .data.packages import load_capture_package, load_run_package
from .report.html import write_run_report_html
from .drivers.dg4202 import SourceStatus
from .drivers.dp800 import PowerStatus
from .drivers.rtm2032 import WaveformData
from .errors import ConfigError, WaveBenchError
from .logging import CommandLogger
from .services.scope_service import ScopeService
from .services.source_service import SourceService
from .services.power_service import PowerService
from .services.run_plan import RunPlan, RunStep, format_run_plan_schema, load_run_plan
from .services.run_service import RunService
from .services.sweep_service import SweepService, parse_frequency_list


def add_runtime_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default="wavebench.toml", help="Path to wavebench TOML config")
    parser.add_argument("--resource", help="Override VISA resource, e.g. TCPIP::192.168.1.100::INSTR")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wavebench")
    subparsers = parser.add_subparsers(dest="domain", required=True)

    scope_parser = subparsers.add_parser("scope", help="Oscilloscope commands")
    source_parser = subparsers.add_parser("source", help="Signal generator commands")
    power_parser = subparsers.add_parser("power", help="Power supply commands")
    sweep_parser = subparsers.add_parser("sweep", help="Source/scope sweep commands")
    run_parser = subparsers.add_parser("run", help="Multi-instrument run plan commands")
    capture_parser = subparsers.add_parser("capture", help="Offline capture package commands")

    run_sub = run_parser.add_subparsers(dest="command", required=True)
    run_check = run_sub.add_parser(
        "check", help="Parse and validate a run plan without connecting to instruments"
    )
    run_check.add_argument("--plan", required=True, help="Path to a WaveBench run plan TOML file")
    add_runtime_options(run_check)
    run_sub.add_parser("schema", help="Print supported run plan step kinds and fields")
    run_plan = run_sub.add_parser("plan", help="Execute a WaveBench run plan")
    run_plan.add_argument("--plan", required=True, help="Path to a WaveBench run plan TOML file")
    add_runtime_options(run_plan)
    run_report = run_sub.add_parser("report", help="Generate an offline HTML report for a run package")
    run_report.add_argument("path", help="Path to data/runs/<run_dir>")
    run_report.add_argument("--output", default=None, help="Output HTML path; defaults to <run_dir>/report.html")

    capture_sub = capture_parser.add_subparsers(dest="command", required=True)
    capture_inspect = capture_sub.add_parser("inspect", help="Inspect an offline capture package")
    capture_inspect.add_argument("path", help="Path to data/raw/<capture_dir>")
    capture_inspect.add_argument("--fft", action="store_true", help="Print offline FFT spectrum summary for saved NPY waveforms")

    power_sub = power_parser.add_subparsers(dest="command", required=True)
    power_idn = power_sub.add_parser("idn", help="Query power supply *IDN?")
    add_runtime_options(power_idn)
    power_status = power_sub.add_parser("status", help="Query power supply channel status")
    power_status.add_argument("--channel", type=int, default=None)
    add_runtime_options(power_status)
    power_set = power_sub.add_parser("set", help="Set power supply voltage and current limit; does not change output state")
    power_set.add_argument("--channel", type=int, default=None)
    power_set.add_argument("--voltage", type=float, required=True)
    power_set.add_argument("--current-limit", type=float, required=True)
    add_runtime_options(power_set)
    power_output = power_sub.add_parser("output", help="Turn power supply channel output on or off")
    power_output.add_argument("--channel", type=int, default=None)
    power_output.add_argument("state", choices=["on", "off"])
    add_runtime_options(power_output)

    source_sub = source_parser.add_subparsers(dest="command", required=True)

    source_idn = source_sub.add_parser("idn", help="Query source *IDN?")
    add_runtime_options(source_idn)

    source_errors = source_sub.add_parser("errors", help="Read source SYST:ERR? until empty")
    add_runtime_options(source_errors)

    source_status = source_sub.add_parser("status", help="Query source channel status")
    source_status.add_argument("--channel", type=int, default=None)
    add_runtime_options(source_status)

    source_set_freq = source_sub.add_parser("set-freq", help="Set source channel frequency in Hz")
    source_set_freq.add_argument("--channel", type=int, default=None)
    source_set_freq.add_argument("value_hz", type=float)
    add_runtime_options(source_set_freq)

    source_output = source_sub.add_parser("output", help="Set source channel output on or off")
    source_output.add_argument("--channel", type=int, default=None)
    source_output.add_argument("state", choices=["on", "off", "ON", "OFF"])
    add_runtime_options(source_output)

    source_set_func = source_sub.add_parser("set-func", help="Set source channel waveform function")
    source_set_func.add_argument("--channel", type=int, default=None)
    source_set_func.add_argument("function", help="Waveform function: sin, squ, ramp, puls, nois, or dc")
    add_runtime_options(source_set_func)

    source_set_vpp = source_sub.add_parser("set-vpp", help="Set source channel amplitude in Vpp")
    source_set_vpp.add_argument("--channel", type=int, default=None)
    source_set_vpp.add_argument("value_vpp", type=float)
    add_runtime_options(source_set_vpp)

    source_set_duty = source_sub.add_parser("set-duty", help="Set square-wave duty cycle in percent")
    source_set_duty.add_argument("--channel", type=int, default=None)
    source_set_duty.add_argument("duty_percent", type=float)
    add_runtime_options(source_set_duty)

    sweep_sub = sweep_parser.add_subparsers(dest="command", required=True)
    sweep_discrete = sweep_sub.add_parser("discrete", help="Run a discrete source-frequency sweep and capture each point")
    sweep_discrete.add_argument("--source-channel", type=int, default=None)
    sweep_discrete.add_argument("--scope-channel", type=int, default=None)
    sweep_discrete.add_argument("--source-resource", default=None, help="Override source VISA resource")
    sweep_discrete.add_argument("--frequencies", required=True, help="Comma-separated frequency list in Hz, e.g. 1000,2000,5000")
    sweep_discrete.add_argument("--target-cycles", type=float, default=10.0)
    sweep_discrete.add_argument("--frequency-tolerance", type=float, default=None)
    sweep_discrete.add_argument("--source-func", default=None, help="Optional source function to set once before sweep")
    sweep_discrete.add_argument("--source-vpp", type=float, default=None, help="Optional source amplitude in Vpp to set once before sweep")
    sweep_discrete.add_argument("--restore-source-state", action="store_true", help="Restore source output/function/frequency/amplitude after sweep")
    sweep_discrete.add_argument("--label", default="discrete_sweep")
    sweep_discrete.add_argument("--no-csv", action="store_true", help="Do not save per-point CSV waveform output")
    sweep_discrete.add_argument("--no-npy", action="store_true", help="Do not save per-point NPY waveform output")
    add_runtime_options(sweep_discrete)

    scope_sub = scope_parser.add_subparsers(dest="command", required=True)

    idn = scope_sub.add_parser("idn", help="Query *IDN?")
    add_runtime_options(idn)

    errors = scope_sub.add_parser("errors", help="Read SYST:ERR? until empty")
    add_runtime_options(errors)

    auto = scope_sub.add_parser("auto", help="Run explicit AUToscale and wait for *OPC?")
    add_runtime_options(auto)

    autoscale = scope_sub.add_parser("autoscale", help="Alias of scope auto")
    add_runtime_options(autoscale)

    fetch = scope_sub.add_parser("fetch", help="Fetch waveform data without creating full package")
    fetch.add_argument("--channel", type=int, default=None)
    fetch.add_argument("--points", default=None, help="Override waveform points: def, max, or dmax")
    add_runtime_options(fetch)

    capture = scope_sub.add_parser("capture", help="Capture waveform data into an acquisition package")
    capture.add_argument("--channel", type=int, action="append", default=None, help="Capture channel; repeat for multiple channels")
    capture.add_argument("--label", default="capture")
    capture.add_argument("--points", default=None, help="Override waveform points: def, max, or dmax")
    capture.add_argument("--time-range", type=float, default=None, help="Set total acquisition time across 10 divisions, in seconds")
    capture.add_argument("--expect-frequency", type=float, default=None, help="Expected signal frequency in Hz for metadata quality checks")
    capture.add_argument("--window-frequency", type=float, default=None, help="Frequency in Hz used only to compute target-cycle time range")
    capture.add_argument("--target-cycles", type=float, default=None, help="Set time range to target_cycles / window_frequency")
    capture.add_argument("--frequency-tolerance", type=float, default=None, help="Relative frequency tolerance, e.g. 0.05 for 5 percent")
    capture.add_argument("--no-csv", action="store_true", help="Do not save CSV waveform output")
    capture.add_argument("--no-npy", action="store_true", help="Do not save NPY waveform output")
    capture.add_argument("--screenshot", action="store_true", help="Save a PNG screenshot artifact in the capture package")
    add_runtime_options(capture)

    return parser


def _load_service(args: argparse.Namespace) -> ScopeService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_resource(args.resource)
    if (
        getattr(args, "points", None)
        or getattr(args, "time_range", None) is not None
        or getattr(args, "expect_frequency", None) is not None
        or getattr(args, "frequency_tolerance", None) is not None
        or getattr(args, "target_cycles", None) is not None
        or getattr(args, "window_frequency", None) is not None
    ):
        expected_frequency = getattr(args, "expect_frequency", None)
        window_frequency = getattr(args, "window_frequency", None) or expected_frequency
        target_cycles = getattr(args, "target_cycles", None)
        time_range = getattr(args, "time_range", None)
        if target_cycles is not None:
            if window_frequency is None or window_frequency <= 0:
                raise ConfigError("--target-cycles requires --window-frequency or --expect-frequency > 0")
            if target_cycles <= 0:
                raise ConfigError("--target-cycles must be > 0")
            if time_range is None:
                time_range = target_cycles / window_frequency
        config = config.with_waveform_overrides(
            points=getattr(args, "points", None),
            time_range_s=time_range,
            expected_frequency_hz=expected_frequency,
            frequency_tolerance_ratio=getattr(args, "frequency_tolerance", None),
            target_cycles=target_cycles,
            window_frequency_hz=window_frequency,
        )
    if getattr(args, "no_csv", False) or getattr(args, "no_npy", False) or getattr(args, "screenshot", False):
        config = config.with_output_overrides(
            save_csv=False if getattr(args, "no_csv", False) else None,
            save_npy=False if getattr(args, "no_npy", False) else None,
            save_screenshot=True if getattr(args, "screenshot", False) else None,
        )
    return ScopeService(config=config, logger=CommandLogger())


def _load_source_service(args: argparse.Namespace) -> SourceService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_source_resource(args.resource)
    return SourceService(config=config, logger=CommandLogger())


def _load_power_service(args: argparse.Namespace) -> PowerService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_power_resource(args.resource)
    return PowerService(config=config, logger=CommandLogger())


def _load_run_service(args: argparse.Namespace) -> RunService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_resource(args.resource)
    return RunService(config=config, logger=CommandLogger())


def _load_sweep_service(args: argparse.Namespace) -> SweepService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_resource(args.resource)
    if getattr(args, "source_resource", None):
        config = config.with_source_resource(args.source_resource)
    return SweepService(config=config, logger=CommandLogger())


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
        channel = "default" if plan.restore.source_channel is None else plan.restore.source_channel
        print(f"restore: source state channel={channel}")
    else:
        print("restore: none")
    print(f"steps={len(plan.steps)}")
    for step in plan.steps:
        print(_format_step_summary(step))

def _print_power_status(status: PowerStatus) -> None:
    set_value = f"{status.set_voltage_v}V/{status.set_current_a}A"
    measured = f"{status.measured_voltage_v}V/{status.measured_current_a}A/{status.measured_power_w}W"
    print(f"CH{status.channel}: output={status.output} mode={status.mode} set={set_value} measured={measured} rating={status.rating}")


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


def _print_capture_fft_summary(package) -> None:
    print("FFT")
    for channel in package.channels:
        npy_text = channel.files.get("npy")
        print(f"CH{channel.channel}")
        if not npy_text:
            print("  warning=missing npy artifact")
            continue
        npy_path = _resolve_capture_file_path(package.path, npy_text)
        try:
            analysis = _analyze_fft(np.load(npy_path))
        except Exception as exc:  # report-style inspect should keep other channels readable
            print(f"  warning=fft unavailable: {type(exc).__name__}: {exc}")
            continue
        print(f"  window={analysis['window']}")
        print(f"  samples={analysis['samples']}")
        print(f"  sample_rate≈{analysis['sample_rate_hz']:.6g} Hz")
        print(f"  resolution≈{analysis['resolution_hz']:.6g} Hz")
        print(f"  peak_frequency≈{analysis['peak_frequency_hz']:.6g} Hz")
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


def _analyze_fft(waveform: Any) -> dict[str, Any]:
    data = np.asarray(waveform, dtype=float)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError("expected an Nx2 waveform array")
    finite = np.isfinite(data[:, 0]) & np.isfinite(data[:, 1])
    data = data[finite]
    if data.shape[0] < 4:
        raise ValueError("need at least four finite waveform samples")
    time_s = data[:, 0]
    voltage_v = data[:, 1]
    dt = np.diff(time_s)
    positive_dt = dt[dt > 0]
    if positive_dt.size == 0:
        raise ValueError("waveform time axis must be increasing")
    median_dt = float(np.median(positive_dt))
    if median_dt <= 0:
        raise ValueError("waveform sample interval must be positive")
    warnings: list[str] = []
    if not np.all(dt > 0):
        warnings.append("non_monotonic_time_axis")
    if np.max(np.abs(dt - median_dt)) > median_dt * 0.01:
        warnings.append("non_uniform_sample_interval")
    samples = int(voltage_v.size)
    centered = voltage_v - float(np.mean(voltage_v))
    window = np.hanning(samples)
    coherent_gain = float(np.mean(window))
    if coherent_gain <= 0:
        raise ValueError("invalid FFT window")
    spectrum = np.fft.rfft(centered * window)
    frequencies = np.fft.rfftfreq(samples, d=median_dt)
    amplitudes = np.abs(spectrum) * 2.0 / (samples * coherent_gain)
    if amplitudes.size:
        amplitudes[0] = amplitudes[0] / 2.0
    if amplitudes.size < 2:
        raise ValueError("not enough FFT bins")
    search = amplitudes[1:]
    peak_index = int(np.argmax(search) + 1)
    peak_frequency = float(frequencies[peak_index])
    peak_amplitude = float(amplitudes[peak_index])
    noise_bins = np.delete(amplitudes[1:], max(peak_index - 1, 0))
    noise_floor = float(np.median(noise_bins)) if noise_bins.size else 0.0
    harmonics = _fft_harmonics(frequencies, amplitudes, peak_frequency)
    harmonic_power = sum(item["amplitude_v"] ** 2 for item in harmonics)
    thd = (harmonic_power ** 0.5 / peak_amplitude) if peak_amplitude > 0 and harmonics else None
    return {
        "window": "hann",
        "samples": samples,
        "sample_rate_hz": 1.0 / median_dt,
        "resolution_hz": float(frequencies[1] - frequencies[0]) if frequencies.size > 1 else 0.0,
        "peak_frequency_hz": peak_frequency,
        "peak_amplitude_v": peak_amplitude,
        "noise_floor_v": noise_floor,
        "harmonics": harmonics,
        "thd_ratio": thd,
        "warnings": warnings,
    }


def _fft_harmonics(frequencies: Any, amplitudes: Any, fundamental_hz: float) -> list[dict[str, float]]:
    if fundamental_hz <= 0:
        return []
    result: list[dict[str, float]] = []
    max_frequency = float(frequencies[-1])
    for order in range(2, 6):
        target = fundamental_hz * order
        if target > max_frequency:
            break
        index = int(np.argmin(np.abs(frequencies - target)))
        result.append(
            {
                "order": float(order),
                "frequency_hz": float(frequencies[index]),
                "amplitude_v": float(amplitudes[index]),
            }
        )
    return result


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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.domain == "capture":
            if args.command == "inspect":
                package = load_capture_package(args.path)
                _print_capture_package_summary(package)
                if args.fft:
                    _print_capture_fft_summary(package)
                return 0
        if args.domain == "run":
            if args.command == "report":
                output = write_run_report_html(load_run_package(args.path), output_path=args.output)
                print(f"report={output}")
                return 0
            if args.command == "check":
                plan = load_run_plan(args.plan)
                _print_run_plan_summary(plan)
                return 0
            if args.command == "schema":
                print(format_run_plan_schema())
                return 0
            if args.command == "plan":
                plan = load_run_plan(args.plan)
                result = _load_run_service(args).run(plan)
                print(f"run={result.run_dir}")
                print(f"run_json={result.run_json_path}")
                print(f"summary={result.summary_csv_path}")
                print(f"steps={len(result.steps)}")
                return 0
        if args.domain == "power":
            service = _load_power_service(args)
            if args.command == "idn":
                print(service.idn())
                return 0
            if args.command == "status":
                _print_power_status(service.status(channel=args.channel))
                return 0
            if args.command == "set":
                _print_power_status(
                    service.set_voltage_current_limit(
                        channel=args.channel,
                        voltage_v=args.voltage,
                        current_limit_a=args.current_limit,
                    )
                )
                return 0
            if args.command == "output":
                _print_power_status(service.set_output(channel=args.channel, enabled=args.state == "on"))
                return 0
        if args.domain == "source":
            service = _load_source_service(args)
            if args.command == "idn":
                print(service.idn())
                return 0
            if args.command == "errors":
                for item in service.errors():
                    print(item)
                return 0
            if args.command == "status":
                _print_source_status(service.status(channel=args.channel))
                return 0
            if args.command == "set-freq":
                _print_source_status(service.set_frequency(channel=args.channel, value_hz=args.value_hz))
                return 0
            if args.command == "output":
                _print_source_status(service.set_output(channel=args.channel, enabled=args.state.lower() == "on"))
                return 0
            if args.command == "set-func":
                _print_source_status(service.set_function(channel=args.channel, function=args.function))
                return 0
            if args.command == "set-vpp":
                _print_source_status(service.set_amplitude_vpp(channel=args.channel, value_vpp=args.value_vpp))
                return 0
            if args.command == "set-duty":
                _print_source_status(service.set_square_duty_cycle(channel=args.channel, duty_percent=args.duty_percent))
                return 0
        if args.domain == "sweep":
            service = _load_sweep_service(args)
            if args.command == "discrete":
                try:
                    frequencies = parse_frequency_list(args.frequencies)
                except ValueError as exc:
                    raise ConfigError(str(exc)) from exc
                result = service.run_discrete(
                    frequencies_hz=frequencies,
                    source_channel=args.source_channel,
                    scope_channel=args.scope_channel,
                    target_cycles=args.target_cycles,
                    frequency_tolerance=args.frequency_tolerance,
                    label=args.label,
                    save_csv=not args.no_csv,
                    save_npy=not args.no_npy,
                    source_function=args.source_func,
                    source_vpp=args.source_vpp,
                    restore_source_state=args.restore_source_state,
                )
                for row in result.rows:
                    measured = "n/a" if row.measured_frequency_hz is None else f"{row.measured_frequency_hz:.6g}"
                    ok = "n/a" if row.frequency_in_tolerance is None else str(row.frequency_in_tolerance)
                    print(f"{row.index}: set={row.set_frequency_hz:.6g}Hz measured≈{measured}Hz ok={ok} package={row.package}")
                print(f"summary={result.summary_path}")
                return 0
        if args.domain == "scope":
            service = _load_service(args)
            if args.command == "idn":
                print(service.idn())
                return 0
            if args.command == "errors":
                for item in service.errors():
                    print(item)
                return 0
            if args.command in {"auto", "autoscale"}:
                service.autoscale()
                print("AUToscale completed")
                return 0
            if args.command == "fetch":
                channel = args.channel or service.config.scope.default_channel
                waveform = service.fetch_waveform(channel=channel)
                _print_waveform_summary(waveform)
                return 0
            if args.command == "capture":
                channels = args.channel or [service.config.scope.default_channel]
                if len(channels) == 1:
                    result = service.capture_waveform(channel=channels[0], label=args.label)
                    _print_waveform_summary(result.waveform)
                    print(f"package={result.package_dir}")
                    if result.csv_path is not None:
                        print(f"csv={result.csv_path}")
                    if result.npy_path is not None:
                        print(f"npy={result.npy_path}")
                    if result.screenshot_path is not None:
                        print(f"screenshot={result.screenshot_path}")
                    if result.commands_log_path is not None:
                        print(f"commands_log={result.commands_log_path}")
                    return 0
                result = service.capture_waveforms(channels=channels, label=args.label)
                for channel in channels:
                    _print_waveform_summary(result.waveforms[channel])
                    files = result.files.get(str(channel), {})
                    if "csv" in files:
                        print(f"ch{channel}_csv={files['csv']}")
                    if "npy" in files:
                        print(f"ch{channel}_npy={files['npy']}")
                print(f"package={result.package_dir}")
                if result.screenshot_path is not None:
                    print(f"screenshot={result.screenshot_path}")
                if result.commands_log_path is not None:
                    print(f"commands_log={result.commands_log_path}")
                return 0
        parser.error("unknown command")
    except WaveBenchError as exc:
        print(f"wavebench: {exc}", file=sys.stderr)
        return exc.exit_code
    except KeyboardInterrupt:
        print("wavebench: interrupted", file=sys.stderr)
        return 130
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
