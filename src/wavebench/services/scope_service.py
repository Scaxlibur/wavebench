from __future__ import annotations

import csv
import json
import traceback
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import numpy as np

from wavebench.config import WaveBenchConfig
from wavebench.data.package import new_package_dir
from wavebench.drivers.ds1104 import DS1104Scope
from wavebench.drivers.rtm2032 import RTM2032Scope, WaveformData
from wavebench.errors import ConfigError, WaveBenchError
from wavebench.logging import CommandLogger
from wavebench.transport.pyvisa_transport import PyVisaTransport
from wavebench.transport.rsinstrument_transport import RsInstrumentTransport

HIGH_IMPEDANCE_COUPLINGS = {"DCL", "DCLIMIT", "ACL", "ACLIMIT"}
LOW_IMPEDANCE_COUPLINGS = {"DC", "AC"}
RIGOL_DS1000Z_DRIVERS = {"ds1104", "ds1000z"}


class ScopeDriver(Protocol):
    def idn(self) -> str: ...
    def errors(self, limit: int = 16) -> list[str]: ...
    def channel_coupling(self, channel: int) -> str: ...
    def autoscale(self, wait_opc: bool = True, check_errors: bool = True) -> None: ...
    def fetch_waveform(self, channel: int, points: str = "dmax", check_errors: bool = True) -> WaveformData: ...
    def capture_waveform(self, channel: int, points: str = "dmax", check_errors: bool = True, time_range_s: float | None = None, vertical_scale_v_per_div: float | None = None) -> WaveformData: ...
    def screenshot_png(self, *, include_menu: bool = False, color_scheme: str = "COL") -> bytes: ...
    def close(self) -> None: ...


def normalize_coupling(value: str) -> str:
    return value.strip().upper()


def is_high_impedance_coupling(value: str) -> bool:
    return normalize_coupling(value) in HIGH_IMPEDANCE_COUPLINGS


def assert_scope_high_impedance(
    coupling: str,
    *,
    channel: int,
    allow_50ohm: bool = False,
    driver: str = "rtm2032",
) -> str:
    normalized = normalize_coupling(coupling)
    if driver.strip().lower() in RIGOL_DS1000Z_DRIVERS:
        if normalized in {"AC", "DC", "GND"}:
            return normalized
        raise ConfigError(
            f"scope CH{channel} coupling {normalized!r} is not recognized for RIGOL DS1000Z; "
            "expected AC, DC, or GND. / "
            f"示波器 CH{channel} 耦合值 {normalized!r} 不是已知的 RIGOL DS1000Z 耦合方式。"
        )
    if normalized in HIGH_IMPEDANCE_COUPLINGS:
        return normalized
    if allow_50ohm and normalized in LOW_IMPEDANCE_COUPLINGS:
        return normalized
    if normalized in LOW_IMPEDANCE_COUPLINGS:
        raise ConfigError(
            f"scope CH{channel} coupling is {normalized}, which may use 50 ohm termination; "
            "default capture requires high impedance. Pass --allow-50ohm or set "
            "safety.allow_50ohm = true only when the test setup explicitly accepts this. "
            f"/ 示波器 CH{channel} 当前耦合为 {normalized}，可能是 50Ω 输入；默认要求高阻测量。"
            "只有明确允许 50Ω 时才使用 --allow-50ohm 或 safety.allow_50ohm = true。"
        )
    raise ConfigError(
        f"scope CH{channel} coupling {normalized!r} is not recognized; refusing capture by default. "
        "Known high-impedance values: ACL, ACLimit, DCL, DCLimit. "
        f"/ 示波器 CH{channel} 耦合值 {normalized!r} 无法确认是否高阻，默认拒绝采集。"
    )


@dataclass(frozen=True)
class CaptureResult:
    package_dir: Path
    waveform: WaveformData
    metadata_path: Path
    csv_path: Path | None
    npy_path: Path | None
    screenshot_path: Path | None
    commands_log_path: Path | None

@dataclass(frozen=True)
class MultiCaptureResult:
    package_dir: Path
    waveforms: dict[int, WaveformData]
    metadata_path: Path
    files: dict[str, dict[str, str]]
    screenshot_path: Path | None
    commands_log_path: Path | None

@dataclass
class ScopeService:
    config: WaveBenchConfig
    logger: CommandLogger
    session: ScopeDriver | None = None

    def _open_scope(self) -> ScopeDriver:
        if self.config.scope.driver.strip().lower() in RIGOL_DS1000Z_DRIVERS:
            transport = PyVisaTransport.open(self.config.connection, logger=self.logger)
            return DS1104Scope(
                transport=transport,
                check_errors_after_ops=self.config.scope.check_errors,
            )
        transport = RsInstrumentTransport.open(self.config.connection, logger=self.logger)
        return RTM2032Scope(transport=transport, check_errors_after_ops=self.config.scope.check_errors)

    def open_session(self) -> ScopeDriver:
        return self._open_scope()

    @contextmanager
    def _scope_session(self) -> Iterator[ScopeDriver]:
        if self.session is not None:
            yield self.session
            return
        scope = self._open_scope()
        try:
            yield scope
        finally:
            scope.close()

    def idn(self) -> str:
        with self._scope_session() as scope:
            return scope.idn()

    def errors(self) -> list[str]:
        with self._scope_session() as scope:
            return scope.errors()

    def channel_coupling(self, channel: int) -> str:
        with self._scope_session() as scope:
            return scope.channel_coupling(channel)

    def require_high_impedance(self, channel: int, *, allow_50ohm: bool = False) -> str:
        coupling = self.channel_coupling(channel)
        return assert_scope_high_impedance(
            coupling,
            channel=channel,
            allow_50ohm=allow_50ohm,
            driver=self.config.scope.driver,
        )

    def autoscale(self) -> None:
        with self._scope_session() as scope:
            scope.autoscale(
                wait_opc=self.config.autoscale.wait_opc,
                check_errors=self.config.autoscale.check_errors,
            )

    def fetch_waveform(self, channel: int) -> WaveformData:
        if self.config.waveform.format.lower() != "real":
            raise ConfigError("MVP-1 only supports waveform.format = 'real'")
        if self.config.waveform.byte_order.lower() != "lsbf":
            raise ConfigError("MVP-1 only supports waveform.byte_order = 'lsbf'")
        with self._scope_session() as scope:
            return scope.fetch_waveform(
                channel=channel,
                points=self.config.waveform.points,
                check_errors=self.config.scope.check_errors,
            )

    def _write_waveform_files(self, package_dir: Path, channel: int, waveform: WaveformData) -> dict[str, str]:
        times = waveform.times_s
        files: dict[str, str] = {}
        if self.config.output.save_csv:
            csv_path = package_dir / f"ch{channel}.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["index", "time_s", "voltage_v"])
                for index, (time_s, voltage_v) in enumerate(zip(times, waveform.voltages_v)):
                    writer.writerow([index, f"{time_s:.12e}", f"{float(voltage_v):.12e}"])
            files["csv"] = str(csv_path)
        if self.config.output.save_npy:
            npy_path = package_dir / f"ch{channel}.npy"
            np.save(npy_path, np.column_stack((times, waveform.voltages_v)))
            files["npy"] = str(npy_path)
        return files


    def _write_screenshot_file(self, package_dir: Path, scope: ScopeDriver) -> tuple[Path | None, dict[str, str] | None]:
        if not self.config.output.save_screenshot:
            return None, None
        screenshot_path = package_dir / "screenshot.png"
        try:
            screenshot_path.write_bytes(scope.screenshot_png(include_menu=False, color_scheme="COL"))
        except Exception as exc:
            return None, {"type": type(exc).__name__, "message": str(exc)}
        return screenshot_path, None

    def _waveform_metadata(self, waveform: WaveformData) -> dict[str, Any]:
        return {
            "header": {
                "x_start_s": waveform.header.x_start,
                "x_stop_s": waveform.header.x_stop,
                "x_increment_s": waveform.header.x_increment,
                "points": waveform.header.points,
                "segment": waveform.header.segment,
            },
            "summary": waveform.summary(
                expected_frequency_hz=self.config.waveform.expected_frequency_hz,
                frequency_tolerance_ratio=self.config.waveform.frequency_tolerance_ratio,
            ),
        }

    def _failed_capture_package(
        self, *, package_dir: Path, operation: dict[str, Any], exc: Exception, commands_log_path: Path | None
    ) -> None:
        failed_dir = package_dir.with_name(package_dir.name + "_failed")
        package_dir.rename(failed_dir)
        (failed_dir / "error.txt").write_text(
            f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}",
            encoding="utf-8",
        )
        partial = {
            "instrument": {"resource": self.config.connection.resource},
            "operation": {**operation, "failed": True},
            "error": {"type": type(exc).__name__, "message": str(exc)},
            "files": {"commands": str(failed_dir / "commands.log")} if commands_log_path is not None else {},
        }
        (failed_dir / "metadata.partial.json").write_text(
            json.dumps(partial, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def capture_waveform(self, channel: int, label: str) -> CaptureResult:
        package_dir = new_package_dir(self.config.output.directory, label)
        package_dir.mkdir(parents=True, exist_ok=False)
        commands_log_path = package_dir / "commands.log" if self.config.output.save_commands_log else None
        if commands_log_path is not None:
            self.logger.path = commands_log_path
        operation = {
            "command": "scope capture",
            "channel": channel,
            "label": label,
            "time_range_s": self.config.waveform.time_range_s,
            "expected_frequency_hz": self.config.waveform.expected_frequency_hz,
            "target_cycles": self.config.waveform.target_cycles,
            "window_frequency_hz": self.config.waveform.window_frequency_hz,
            "frequency_tolerance_ratio": self.config.waveform.frequency_tolerance_ratio,
            "vertical_scale_v_per_div": self.config.waveform.vertical_scale_v_per_div,
            "target_vpp": self.config.waveform.target_vpp,
        }
        screenshot_path: Path | None = None
        screenshot_error: dict[str, str] | None = None
        try:
            with self._scope_session() as scope:
                instrument_idn = scope.idn()
                capture_kwargs = {
                    "channel": channel,
                    "points": self.config.waveform.points,
                    "check_errors": self.config.scope.check_errors,
                    "time_range_s": self.config.waveform.time_range_s,
                }
                if self.config.waveform.vertical_scale_v_per_div is not None:
                    capture_kwargs["vertical_scale_v_per_div"] = self.config.waveform.vertical_scale_v_per_div
                waveform = scope.capture_waveform(**capture_kwargs)
                screenshot_path, screenshot_error = self._write_screenshot_file(package_dir, scope)
        except Exception as exc:
            self._failed_capture_package(
                package_dir=package_dir,
                operation=operation,
                exc=exc,
                commands_log_path=commands_log_path,
            )
            if isinstance(exc, WaveBenchError):
                raise
            raise

        files = self._write_waveform_files(package_dir, channel, waveform)
        if self.config.output.save_screenshot:
            files["screenshot"] = str(screenshot_path) if screenshot_path is not None else None
        metadata: dict[str, Any] = {
            "instrument": {"idn": instrument_idn, "resource": self.config.connection.resource},
            "operation": {**operation, "triggered_single": True},
            "waveform": self._waveform_metadata(waveform),
            "files": files,
        }
        if screenshot_error is not None:
            metadata["screenshot_error"] = screenshot_error
        metadata_path = package_dir / "metadata.json"
        if self.config.output.save_json:
            metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        return CaptureResult(
            package_dir=package_dir,
            waveform=waveform,
            metadata_path=metadata_path,
            csv_path=Path(files["csv"]) if "csv" in files else None,
            npy_path=Path(files["npy"]) if "npy" in files else None,
            screenshot_path=screenshot_path,
            commands_log_path=commands_log_path,
        )

    def capture_waveforms(self, channels: list[int], label: str) -> MultiCaptureResult:
        if not channels:
            raise ConfigError("at least one channel is required")
        if len(set(channels)) != len(channels):
            raise ConfigError("duplicate channels are not allowed")
        package_dir = new_package_dir(self.config.output.directory, label)
        package_dir.mkdir(parents=True, exist_ok=False)
        commands_log_path = package_dir / "commands.log" if self.config.output.save_commands_log else None
        if commands_log_path is not None:
            self.logger.path = commands_log_path
        operation = {
            "command": "scope capture",
            "channels": channels,
            "label": label,
            "time_range_s": self.config.waveform.time_range_s,
            "expected_frequency_hz": self.config.waveform.expected_frequency_hz,
            "target_cycles": self.config.waveform.target_cycles,
            "window_frequency_hz": self.config.waveform.window_frequency_hz,
            "frequency_tolerance_ratio": self.config.waveform.frequency_tolerance_ratio,
            "vertical_scale_v_per_div": self.config.waveform.vertical_scale_v_per_div,
            "target_vpp": self.config.waveform.target_vpp,
        }
        waveforms: dict[int, WaveformData] = {}
        screenshot_path: Path | None = None
        screenshot_error: dict[str, str] | None = None
        try:
            with self._scope_session() as scope:
                instrument_idn = scope.idn()
                for channel in channels:
                    capture_kwargs = {
                        "channel": channel,
                        "points": self.config.waveform.points,
                        "check_errors": self.config.scope.check_errors,
                        "time_range_s": self.config.waveform.time_range_s,
                    }
                    if self.config.waveform.vertical_scale_v_per_div is not None:
                        capture_kwargs["vertical_scale_v_per_div"] = self.config.waveform.vertical_scale_v_per_div
                    waveforms[channel] = scope.capture_waveform(**capture_kwargs)
                screenshot_path, screenshot_error = self._write_screenshot_file(package_dir, scope)
        except Exception as exc:
            self._failed_capture_package(
                package_dir=package_dir,
                operation=operation,
                exc=exc,
                commands_log_path=commands_log_path,
            )
            if isinstance(exc, WaveBenchError):
                raise
            raise

        files: dict[str, dict[str, str]] = {}
        channel_metadata: dict[str, Any] = {}
        for channel in channels:
            waveform = waveforms[channel]
            key = str(channel)
            files[key] = self._write_waveform_files(package_dir, channel, waveform)
            channel_metadata[key] = self._waveform_metadata(waveform)

        metadata_files: dict[str, Any] = dict(files)
        if self.config.output.save_screenshot:
            metadata_files["screenshot"] = str(screenshot_path) if screenshot_path is not None else None
        metadata: dict[str, Any] = {
            "instrument": {"idn": instrument_idn, "resource": self.config.connection.resource},
            "operation": {**operation, "triggered_single": True, "trigger_mode": "sequential_per_channel"},
            "channels": channel_metadata,
            "files": metadata_files,
        }
        if screenshot_error is not None:
            metadata["screenshot_error"] = screenshot_error
        metadata_path = package_dir / "metadata.json"
        if self.config.output.save_json:
            metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        return MultiCaptureResult(
            package_dir=package_dir,
            waveforms=waveforms,
            metadata_path=metadata_path,
            files=files,
            screenshot_path=screenshot_path,
            commands_log_path=commands_log_path,
        )
