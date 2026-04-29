from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

from .errors import ConfigError

WAVEFORM_POINTS_ALIASES = {
    "def": "DEF",
    "default": "DEF",
    "max": "MAX",
    "maximum": "MAX",
    "dmax": "DMAX",
    "dmaximum": "DMAX",
}


def normalize_waveform_points(points: str) -> str:
    normalized = points.strip().lower()
    try:
        return WAVEFORM_POINTS_ALIASES[normalized]
    except KeyError as exc:
        raise ConfigError("waveform points must be one of: def, max, dmax") from exc

@dataclass(frozen=True)
class ConnectionConfig:
    backend: str
    resource: str
    timeout_ms: int
    opc_timeout_ms: int

@dataclass(frozen=True)
class ScopeConfig:
    driver: str
    model_hint: str | None
    default_channel: int
    reset_before_run: bool
    check_errors: bool

@dataclass(frozen=True)
class AutoscaleConfig:
    wait_opc: bool
    check_errors: bool

@dataclass(frozen=True)
class WaveformConfig:
    format: str
    byte_order: str
    points: str
    time_range_s: float | None = None

@dataclass(frozen=True)
class OutputConfig:
    directory: Path
    package_naming: str
    save_csv: bool
    save_npy: bool
    save_json: bool
    save_commands_log: bool
    save_screenshot: bool

@dataclass(frozen=True)
class WaveBenchConfig:
    connection: ConnectionConfig
    scope: ScopeConfig
    autoscale: AutoscaleConfig
    waveform: WaveformConfig
    output: OutputConfig
    source_path: Path

    def with_resource(self, resource: str) -> "WaveBenchConfig":
        return WaveBenchConfig(
            connection=ConnectionConfig(
                backend=self.connection.backend,
                resource=resource,
                timeout_ms=self.connection.timeout_ms,
                opc_timeout_ms=self.connection.opc_timeout_ms,
            ),
            scope=self.scope,
            autoscale=self.autoscale,
            waveform=self.waveform,
            output=self.output,
            source_path=self.source_path,
        )

    def with_output_overrides(self, *, save_csv: bool | None = None, save_npy: bool | None = None) -> "WaveBenchConfig":
        return WaveBenchConfig(
            connection=self.connection,
            scope=self.scope,
            autoscale=self.autoscale,
            waveform=self.waveform,
            output=OutputConfig(
                directory=self.output.directory,
                package_naming=self.output.package_naming,
                save_csv=self.output.save_csv if save_csv is None else save_csv,
                save_npy=self.output.save_npy if save_npy is None else save_npy,
                save_json=self.output.save_json,
                save_commands_log=self.output.save_commands_log,
                save_screenshot=self.output.save_screenshot,
            ),
            source_path=self.source_path,
        )

    def with_waveform_overrides(
        self, *, points: str | None = None, time_range_s: float | None = None
    ) -> "WaveBenchConfig":
        return WaveBenchConfig(
            connection=self.connection,
            scope=self.scope,
            autoscale=self.autoscale,
            waveform=WaveformConfig(
                format=self.waveform.format,
                byte_order=self.waveform.byte_order,
                points=self.waveform.points if points is None else normalize_waveform_points(points),
                time_range_s=self.waveform.time_range_s if time_range_s is None else time_range_s,
            ),
            output=self.output,
            source_path=self.source_path,
        )

def load_config(path: str | Path = "wavebench.toml") -> WaveBenchConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(
            f"config file not found: {config_path}. Copy wavebench.example.toml to wavebench.toml first."
        )
    try:
        raw = tomllib.loads(config_path.read_bytes().decode("utf-8-sig"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"invalid TOML in {config_path}: {exc}") from exc

    try:
        c = raw["connection"]
        s = raw["scope"]
        a = raw.get("autoscale", {})
        w = raw.get("waveform", {})
        o = raw.get("output", {})
        config = WaveBenchConfig(
            connection=ConnectionConfig(
                backend=str(c.get("backend", "lan")),
                resource=str(c["resource"]),
                timeout_ms=int(c.get("timeout_ms", 10000)),
                opc_timeout_ms=int(c.get("opc_timeout_ms", 30000)),
            ),
            scope=ScopeConfig(
                driver=str(s.get("driver", "rtm2032")),
                model_hint=s.get("model_hint"),
                default_channel=int(s.get("default_channel", 1)),
                reset_before_run=bool(s.get("reset_before_run", False)),
                check_errors=bool(s.get("check_errors", True)),
            ),
            autoscale=AutoscaleConfig(
                wait_opc=bool(a.get("wait_opc", True)),
                check_errors=bool(a.get("check_errors", True)),
            ),
            waveform=WaveformConfig(
                format=str(w.get("format", "real")),
                byte_order=str(w.get("byte_order", "lsbf")),
                points=normalize_waveform_points(str(w.get("points", "dmax"))),
                time_range_s=float(w["time_range_s"]) if "time_range_s" in w else None,
            ),
            output=OutputConfig(
                directory=Path(str(o.get("directory", "data/raw"))),
                package_naming=str(o.get("package_naming", "timestamp_label")),
                save_csv=bool(o.get("save_csv", True)),
                save_npy=bool(o.get("save_npy", True)),
                save_json=bool(o.get("save_json", True)),
                save_commands_log=bool(o.get("save_commands_log", True)),
                save_screenshot=bool(o.get("save_screenshot", False)),
            ),
            source_path=config_path,
        )
    except KeyError as exc:
        raise ConfigError(f"missing required config key: {exc}") from exc
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"invalid config value in {config_path}: {exc}") from exc

    if config.connection.backend.lower() != "lan":
        raise ConfigError("MVP-1 only supports LAN VISA resources")
    if config.scope.driver.lower() != "rtm2032":
        raise ConfigError("MVP-1 only supports driver = 'rtm2032'")
    if config.scope.default_channel < 1:
        raise ConfigError("scope.default_channel must be >= 1")
    if config.waveform.time_range_s is not None and config.waveform.time_range_s <= 0:
        raise ConfigError("waveform.time_range_s must be > 0")
    return config
