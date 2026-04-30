from __future__ import annotations

import argparse
import sys

from .config import load_config
from .drivers.dg4202 import SourceStatus
from .drivers.dp800 import PowerStatus
from .drivers.rtm2032 import WaveformData
from .errors import ConfigError, WaveBenchError
from .logging import CommandLogger
from .services.scope_service import ScopeService
from .services.source_service import SourceService
from .services.power_service import PowerService
from .services.run_plan import RunPlan, RunStep, load_run_plan
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

    run_sub = run_parser.add_subparsers(dest="command", required=True)
    run_check = run_sub.add_parser(
        "check", help="Parse and validate a run plan without connecting to instruments"
    )
    run_check.add_argument("--plan", required=True, help="Path to a WaveBench run plan TOML file")
    add_runtime_options(run_check)

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
    if getattr(args, "no_csv", False) or getattr(args, "no_npy", False):
        config = config.with_output_overrides(
            save_csv=False if getattr(args, "no_csv", False) else None,
            save_npy=False if getattr(args, "no_npy", False) else None,
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
    print(f"steps={len(plan.steps)}")
    for step in plan.steps:
        print(_format_step_summary(step))

def _print_power_status(status: PowerStatus) -> None:
    set_value = f"{status.set_voltage_v}V/{status.set_current_a}A"
    measured = f"{status.measured_voltage_v}V/{status.measured_current_a}A/{status.measured_power_w}W"
    print(f"CH{status.channel}: output={status.output} mode={status.mode} set={set_value} measured={measured} rating={status.rating}")


def _print_source_status(status: SourceStatus) -> None:
    print(f"CH{status.channel}: output={status.output} func={status.function} freq={status.frequency_hz}Hz amp={status.amplitude}{status.amplitude_unit or ''} offset={status.offset_v}V phase={status.phase_deg}deg")
    print(f"mode={status.frequency_mode} sweep={status.sweep_enabled}")
    if status.apply_raw is not None:
        print(f"apply={status.apply_raw}")


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
        if args.domain == "run":
            if args.command == "check":
                plan = load_run_plan(args.plan)
                _print_run_plan_summary(plan)
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
