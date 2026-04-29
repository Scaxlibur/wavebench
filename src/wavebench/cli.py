from __future__ import annotations

import argparse
import sys

from .config import load_config
from .drivers.dg4202 import SourceStatus
from .drivers.rtm2032 import WaveformData
from .errors import ConfigError, WaveBenchError
from .logging import CommandLogger
from .services.scope_service import ScopeService
from .services.source_service import SourceService


def add_runtime_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default="wavebench.toml", help="Path to wavebench TOML config")
    parser.add_argument("--resource", help="Override VISA resource, e.g. TCPIP::192.168.1.100::INSTR")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wavebench")
    subparsers = parser.add_subparsers(dest="domain", required=True)

    scope_parser = subparsers.add_parser("scope", help="Oscilloscope commands")
    source_parser = subparsers.add_parser("source", help="Signal generator commands")
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
