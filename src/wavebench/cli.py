from __future__ import annotations

import argparse
import sys


from .config import load_config, vertical_scale_from_vpp
from .data.packages import load_capture_package, load_run_package
from .discovery import DEFAULT_DISCOVERY_PORTS, discover_instruments
from .report.html import write_run_report_html
from .report.index import write_report_index
from .errors import ConfigError, WaveBenchError
from .cli_output import (
    _print_arbitrary_probe_results,
    _print_arbitrary_waveform_summary,
    _print_capture_fft_summary,
    _print_capture_package_summary,
    _print_discovery_results,
    _print_dmm_function_set,
    _print_dmm_function_status,
    _print_dmm_reading,
    _print_power_protection_status,
    _print_power_status,
    _print_run_plan_summary,
    _print_run_preflight,
    _print_source_status,
    _print_waveform_summary,
)
from .logging import CommandLogger
from .mcp_http import (
    DEFAULT_MCP_HOST,
    DEFAULT_MCP_PORT,
    DEFAULT_MCP_TOKEN_ENV,
    resolve_mcp_token,
    serve_mcp_http,
)
from .services.scope_service import ScopeService
from .services.source_service import SourceService
from .services.power_service import PowerService
from .services.dmm_service import DmmService
from .services.run_plan import format_run_plan_schema, load_run_plan
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
    dmm_parser = subparsers.add_parser("dmm", help="Digital multimeter commands")
    sweep_parser = subparsers.add_parser("sweep", help="Source/scope sweep commands")
    run_parser = subparsers.add_parser("run", help="Multi-instrument run plan commands")
    capture_parser = subparsers.add_parser("capture", help="Offline capture package commands")
    mcp_parser = subparsers.add_parser("mcp", help="HTTP MCP server / HTTP MCP 服务")
    tui_parser = subparsers.add_parser("tui", help="Launch terminal UI / 启动终端界面")
    net_parser = subparsers.add_parser("net", help="Network discovery helpers / 网络发现工具")
    tui_parser.add_argument("--config", default="wavebench.toml", help="Path to wavebench TOML config")
    tui_parser.add_argument("--resource", help="Override power VISA resource / 覆盖电源 VISA 资源")
    tui_parser.add_argument(
        "--fake",
        action="store_true",
        help="Use fake power, DMM, and source snapshots / 使用模拟电源、万用表和信号源快照",
    )
    tui_parser.add_argument(
        "--refresh-interval",
        type=float,
        default=5.0,
        help="Refresh interval in seconds / 刷新间隔（秒）",
    )
    tui_parser.add_argument(
        "--log-file",
        default="data/tui/wavebench-tui.log",
        help="Persist TUI debug log to this file / TUI 调试日志文件",
    )

    net_sub = net_parser.add_subparsers(dest="command", required=True)
    net_discover = net_sub.add_parser(
        "discover",
        help="Read-only scan for LAN SCPI/VISA instruments / 只读扫描局域网 SCPI/VISA 仪器",
    )
    net_discover.add_argument("--subnet", required=True, help="Subnet to scan, e.g. 192.168.1.0/24")
    net_discover.add_argument(
        "--ports",
        default=",".join(str(port) for port in DEFAULT_DISCOVERY_PORTS),
        help="Comma-separated TCP ports to probe / 要探测的 TCP 端口",
    )
    net_discover.add_argument(
        "--timeout-ms",
        type=int,
        default=300,
        help="Per-connection timeout in milliseconds / 每次连接超时毫秒数",
    )
    net_discover.add_argument("--workers", type=int, default=64, help="Concurrent probe workers / 并发探测数")
    net_discover.add_argument(
        "--max-hosts",
        type=int,
        default=256,
        help="Maximum hosts allowed in one scan / 单次扫描允许的最大主机数",
    )
    net_discover.add_argument(
        "--no-idn",
        action="store_true",
        help="Only test open ports; do not send read-only *IDN? / 只测端口，不发送只读 *IDN?",
    )
    net_discover.add_argument(
        "--idn-only",
        action="store_true",
        help="Only show devices that answered *IDN? / 只显示响应 *IDN? 的设备",
    )
    net_discover.add_argument(
        "--no-visa",
        action="store_true",
        help="Skip PyVISA resource-manager discovery / 跳过 PyVISA 资源枚举",
    )

    run_sub = run_parser.add_subparsers(dest="command", required=True)
    run_check = run_sub.add_parser(
        "check", help="Parse and validate a run plan without connecting to instruments"
    )
    run_check.add_argument("--plan", required=True, help="Path to a WaveBench run plan TOML file")
    add_runtime_options(run_check)
    run_verify = run_sub.add_parser(
        "verify",
        help="Verify / 预检 instruments referenced by a run plan with read-only *IDN? queries",
    )
    run_verify.add_argument("--plan", required=True, help="Path to a WaveBench run plan TOML file")
    add_runtime_options(run_verify)
    run_sub.add_parser("schema", help="Print supported run plan step kinds and fields")
    run_plan = run_sub.add_parser("plan", help="Execute a WaveBench run plan")
    run_plan.add_argument("--plan", required=True, help="Path to a WaveBench run plan TOML file")
    add_runtime_options(run_plan)
    run_report = run_sub.add_parser("report", help="Generate an offline HTML report for a run package")
    run_report.add_argument("path", help="Path to data/runs/<run_dir>")
    run_report.add_argument("--output", default=None, help="Output HTML path; defaults to <run_dir>/report.html")
    run_report_index = run_sub.add_parser("report-index", help="Generate manifest JSON/CSV for multiple run directories")
    run_report_index.add_argument("paths", nargs="+", help="Paths to data/runs/<run_dir>")
    run_report_index.add_argument("--output", required=True, help="Output directory for manifest.json and manifest.csv")

    capture_sub = capture_parser.add_subparsers(dest="command", required=True)
    capture_inspect = capture_sub.add_parser("inspect", help="Inspect an offline capture package")
    capture_inspect.add_argument("path", help="Path to data/raw/<capture_dir>")
    capture_inspect.add_argument("--fft", action="store_true", help="Print offline FFT spectrum summary for saved NPY waveforms")
    capture_inspect.add_argument("--harmonics", type=int, default=5, help="Highest harmonic order to report with --fft")
    capture_inspect.add_argument("--fft-expect-frequency", type=float, default=None, help="Expected FFT peak frequency in Hz")
    capture_inspect.add_argument("--fft-frequency-tolerance", type=float, default=0.05, help="Relative tolerance for --fft-expect-frequency")

    mcp_sub = mcp_parser.add_subparsers(dest="command", required=True)
    mcp_serve = mcp_sub.add_parser(
        "serve",
        help="Serve read-only HTTP MCP tools / 启动只读 HTTP MCP 工具服务",
    )
    mcp_serve.add_argument(
        "--host",
        default=DEFAULT_MCP_HOST,
        help="Bind host, defaults to 127.0.0.1 / 监听地址，默认 127.0.0.1",
    )
    mcp_serve.add_argument(
        "--port",
        type=int,
        default=DEFAULT_MCP_PORT,
        help="Bind port / 监听端口",
    )
    mcp_serve.add_argument(
        "--token",
        default=None,
        help="Bearer token for HTTP MCP auth / HTTP MCP Bearer 认证 token",
    )
    mcp_serve.add_argument(
        "--token-env",
        default=DEFAULT_MCP_TOKEN_ENV,
        help="Environment variable containing the bearer token / 保存 Bearer token 的环境变量",
    )
    mcp_serve.add_argument(
        "--config",
        default="wavebench.toml",
        help="Path to wavebench TOML config for read-only checks / 只读检查使用的 wavebench TOML 配置",
    )

    dmm_sub = dmm_parser.add_subparsers(dest="command", required=True)
    dmm_idn = dmm_sub.add_parser("idn", help="Query DMM *IDN? over configured backend")
    add_runtime_options(dmm_idn)
    dmm_read = dmm_sub.add_parser("read", help="Read one DMM measurement")
    dmm_read.add_argument("function", nargs="?", default="dcv", help="dcv/acv/dci/aci/res/fres/freq/period/continuity/diode/cap")
    add_runtime_options(dmm_read)
    dmm_function = dmm_sub.add_parser(
        "function", help="Query or set DMM function / 查询或设置万用表功能"
    )
    dmm_function_sub = dmm_function.add_subparsers(
        dest="dmm_function_command", required=True
    )
    dmm_function_status = dmm_function_sub.add_parser(
        "status", help="Query current DMM function / 查询当前万用表功能"
    )
    add_runtime_options(dmm_function_status)
    dmm_function_set = dmm_function_sub.add_parser(
        "set", help="Set DMM function / 设置万用表功能"
    )
    dmm_function_set.add_argument(
        "function",
        help="dcv/acv/dci/aci/res/fres/freq/period/continuity/diode/cap",
    )
    add_runtime_options(dmm_function_set)

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
    power_protection = power_sub.add_parser("protection", help="Query or set power supply OVP/OCP protection")
    protection_sub = power_protection.add_subparsers(dest="protection_command", required=True)
    protection_status = protection_sub.add_parser("status", help="Query OVP/OCP protection status")
    protection_status.add_argument("--channel", type=int, default=None)
    add_runtime_options(protection_status)
    protection_set = protection_sub.add_parser("set", help="Set OVP/OCP thresholds or enable state")
    protection_set.add_argument("--channel", type=int, default=None)
    protection_set.add_argument("--ovp-threshold", type=float, default=None)
    protection_set.add_argument("--ovp", choices=["on", "off"], default=None)
    protection_set.add_argument("--ocp-threshold", type=float, default=None)
    protection_set.add_argument("--ocp", choices=["on", "off"], default=None)
    add_runtime_options(protection_set)

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
    source_set_func.add_argument("function", help="Waveform function: sin, squ, ramp/triangle, puls, nois, or dc")
    add_runtime_options(source_set_func)

    source_set_vpp = source_sub.add_parser("set-vpp", help="Set source channel amplitude in Vpp")
    source_set_vpp.add_argument("--channel", type=int, default=None)
    source_set_vpp.add_argument("value_vpp", type=float)
    add_runtime_options(source_set_vpp)

    source_set_duty = source_sub.add_parser("set-duty", help="Set square-wave duty cycle in percent")
    source_set_duty.add_argument("--channel", type=int, default=None)
    source_set_duty.add_argument("duty_percent", type=float)
    add_runtime_options(source_set_duty)

    source_arb_probe = source_sub.add_parser("arb-probe", help="Run query-only DG4202 arbitrary-waveform SCPI probes; does not upload or enable output")
    source_arb_probe.add_argument("--channel", type=int, default=None)
    source_arb_probe.add_argument("--probe-timeout-ms", type=int, default=1000, help="Per-query timeout for unsupported SCPI candidates")
    add_runtime_options(source_arb_probe)

    source_arb_load = source_sub.add_parser("arb-load", help="Load a DG4202 arbitrary waveform from .csv/.npy; dry-run can export offline payloads")
    source_arb_load.add_argument("--channel", type=int, required=True)
    source_arb_load.add_argument("--file", required=True, help="Input waveform file: .csv or .npy")
    source_arb_load.add_argument("--name", required=True, help="Instrument waveform name, e.g. REI_ARB")
    source_arb_load.add_argument("--amplitude", type=float, required=True, help="Target output amplitude in Vpp")
    source_arb_load.add_argument("--frequency", type=float, default=None, help="Arbitrary waveform playback frequency in Hz; required when uploading")
    source_arb_load.add_argument("--offset", type=float, default=0.0, help="Target output offset in V")
    source_arb_load.add_argument("--sample-rate", type=float, default=None, help="Sample rate in Hz when the file has no time axis")
    source_arb_load.add_argument("--max-points", type=int, default=16384, help="Point-count guard; DG4000 specs list 16K arbitrary length")
    source_arb_load.add_argument("--output-on", action="store_true", help="Allow output state change after upload; ignored by dry-run")
    source_arb_load.add_argument("--export-payload", default=None, help="Write a WaveBench JSON payload artifact for manual review or future upload")
    source_arb_load.add_argument("--export-dg4000-dac-block", default=None, help="Write a DG4000 DATA:DAC VOLATILE binary SCPI command; offline artifact only")
    source_arb_load.add_argument("--dg4000-byte-order", choices=("big", "little"), default="little", help="Byte order for DG4000 uint16 DAC block; DG4202 hardware validation confirmed little-endian")
    source_arb_load.add_argument("--dry-run", action="store_true", help="Only validate/build payload summary; do not connect to the instrument")
    add_runtime_options(source_arb_load)

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
    sweep_discrete.add_argument("--allow-50ohm", action="store_true", help="Explicitly allow scope input coupling that may be 50 ohm; default requires high impedance")
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
    fetch.add_argument("--allow-50ohm", action="store_true", help="Explicitly allow scope input coupling that may be 50 ohm; default requires high impedance")
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
    capture.add_argument("--vertical-scale", type=float, default=None, help="Set channel vertical scale in V/div before capture")
    capture.add_argument("--target-vpp", type=float, default=None, help="Set vertical scale from expected Vpp; defaults to about 5 vertical divisions")
    capture.add_argument("--no-csv", action="store_true", help="Do not save CSV waveform output")
    capture.add_argument("--no-npy", action="store_true", help="Do not save NPY waveform output")
    capture.add_argument("--screenshot", action="store_true", help="Save a PNG screenshot artifact in the capture package")
    capture.add_argument("--allow-50ohm", action="store_true", help="Explicitly allow scope input coupling that may be 50 ohm; default requires high impedance")
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
        or getattr(args, "vertical_scale", None) is not None
        or getattr(args, "target_vpp", None) is not None
    ):
        expected_frequency = getattr(args, "expect_frequency", None)
        window_frequency = getattr(args, "window_frequency", None) or expected_frequency
        target_cycles = getattr(args, "target_cycles", None)
        time_range = getattr(args, "time_range", None)
        vertical_scale = getattr(args, "vertical_scale", None)
        target_vpp = getattr(args, "target_vpp", None)
        if target_vpp is not None:
            if target_vpp <= 0:
                raise ConfigError("--target-vpp must be > 0")
            if vertical_scale is None:
                vertical_scale = vertical_scale_from_vpp(target_vpp)
        if vertical_scale is not None and vertical_scale <= 0:
            raise ConfigError("--vertical-scale must be > 0")
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
            vertical_scale_v_per_div=vertical_scale,
            target_vpp=target_vpp,
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
    probe_timeout_ms = getattr(args, "probe_timeout_ms", None)
    if probe_timeout_ms is not None:
        config = config.with_connection_timeout_ms(probe_timeout_ms)
    return SourceService(config=config, logger=CommandLogger())


def _load_power_service(args: argparse.Namespace) -> PowerService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_power_resource(args.resource)
    return PowerService(config=config, logger=CommandLogger())


def _load_dmm_service(args: argparse.Namespace) -> DmmService:
    config = load_config(args.config)
    if args.resource:
        config = config.with_dmm_resource(args.resource)
    return DmmService(config=config, logger=CommandLogger())


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



def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.domain == "net":
            if args.command == "discover":
                results = discover_instruments(
                    subnet=args.subnet,
                    ports=args.ports,
                    timeout_ms=args.timeout_ms,
                    workers=args.workers,
                    max_hosts=args.max_hosts,
                    query_idn=not args.no_idn,
                    idn_only=args.idn_only,
                    include_visa=not args.no_visa,
                )
                _print_discovery_results(results)
                return 0
        if args.domain == "tui":
            if args.refresh_interval <= 0:
                raise ConfigError("--refresh-interval must be > 0 / 刷新间隔必须 > 0")
            from .tui import run as run_tui

            return run_tui(
                config_path=args.config,
                resource=args.resource,
                fake=args.fake,
                refresh_interval_s=args.refresh_interval,
                log_path=args.log_file,
            )
        if args.domain == "capture":
            if args.command == "inspect":
                package = load_capture_package(args.path)
                _print_capture_package_summary(package)
                if args.fft:
                    _print_capture_fft_summary(
                        package,
                        max_harmonic_order=args.harmonics,
                        expected_frequency_hz=args.fft_expect_frequency,
                        frequency_tolerance_ratio=args.fft_frequency_tolerance,
                )
                return 0
        if args.domain == "mcp":
            if args.command == "serve":
                token = resolve_mcp_token(args.token, args.token_env)
                serve_mcp_http(
                    host=args.host,
                    port=args.port,
                    token=token,
                    config_path=args.config,
                )
                return 0
        if args.domain == "run":
            if args.command == "report":
                output = write_run_report_html(load_run_package(args.path), output_path=args.output)
                print(f"report={output}")
                return 0
            if args.command == "report-index":
                result = write_report_index(args.paths, args.output)
                print(f"manifest_json={result.manifest_json_path}")
                print(f"manifest_csv={result.manifest_csv_path}")
                print(f"runs={result.count}")
                print(f"index_html={result.index_html_path}")
                return 0
            if args.command == "check":
                plan = load_run_plan(args.plan)
                _load_run_service(args).check(plan)
                _print_run_plan_summary(plan)
                print("safety_limits=ok / 安全上限=通过")
                return 0
            if args.command == "verify":
                plan = load_run_plan(args.plan)
                records = _load_run_service(args).verify(plan)
                _print_run_preflight(records)
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
        if args.domain == "dmm":
            service = _load_dmm_service(args)
            if args.command == "idn":
                print(service.idn())
                return 0
            if args.command == "read":
                _print_dmm_reading(service.read(function=args.function))
                return 0
            if args.command == "function":
                if args.dmm_function_command == "status":
                    _print_dmm_function_status(service.function_status())
                    return 0
                if args.dmm_function_command == "set":
                    _print_dmm_function_set(service.set_function(function=args.function))
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
            if args.command == "protection":
                if args.protection_command == "status":
                    _print_power_protection_status(service.protection_status(channel=args.channel))
                    return 0
                if args.protection_command == "set":
                    _print_power_protection_status(
                        service.set_protection(
                            channel=args.channel,
                            ovp_threshold_v=args.ovp_threshold,
                            ovp_enabled=None if args.ovp is None else args.ovp == "on",
                            ocp_threshold_a=args.ocp_threshold,
                            ocp_enabled=None if args.ocp is None else args.ocp == "on",
                        )
                    )
                    return 0
        if args.domain == "source":
            if args.command == "arb-load":
                if args.amplitude <= 0:
                    raise ConfigError("--amplitude must be > 0")
                if args.dry_run:
                    _print_arbitrary_waveform_summary(args, dry_run=True)
                    return 0
                if args.frequency is None or args.frequency <= 0:
                    raise ConfigError("--frequency must be > 0 when uploading")
                service = _load_source_service(args)
                _print_arbitrary_waveform_summary(args, dry_run=False)
                status = service.upload_arbitrary_waveform(
                    channel=args.channel,
                    file_path=args.file,
                    playback_frequency_hz=args.frequency,
                    amplitude_vpp=args.amplitude,
                    offset_v=args.offset,
                    sample_rate_hz=args.sample_rate,
                    max_points=args.max_points,
                    byte_order=args.dg4000_byte_order,
                    output_on=args.output_on,
                )
                print("upload=ok")
                _print_source_status(status)
                return 0
            service = _load_source_service(args)
            if args.command == "idn":
                print(service.idn())
                return 0
            if args.command == "errors":
                for item in service.errors():
                    print(item)
                return 0
            if args.command == "arb-probe":
                _print_arbitrary_probe_results(service.probe_arbitrary_queries(channel=args.channel))
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
                scope_channel = args.scope_channel or service.config.scope.default_channel
                ScopeService(config=service.config, logger=CommandLogger()).require_high_impedance(scope_channel, allow_50ohm=args.allow_50ohm)
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
                service.require_high_impedance(channel, allow_50ohm=args.allow_50ohm)
                waveform = service.fetch_waveform(channel=channel)
                _print_waveform_summary(waveform)
                return 0
            if args.command == "capture":
                channels = args.channel or [service.config.scope.default_channel]
                for channel in channels:
                    service.require_high_impedance(channel, allow_50ohm=args.allow_50ohm)
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
