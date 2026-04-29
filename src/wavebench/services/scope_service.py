from __future__ import annotations

import csv
import json
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from wavebench.config import WaveBenchConfig
from wavebench.data.package import new_package_dir
from wavebench.drivers.rtm2032 import RTM2032Scope, WaveformData
from wavebench.errors import ConfigError, WaveBenchError
from wavebench.logging import CommandLogger
from wavebench.transport.rsinstrument_transport import RsInstrumentTransport

@dataclass(frozen=True)
class CaptureResult:
    package_dir: Path
    waveform: WaveformData
    metadata_path: Path
    csv_path: Path | None
    npy_path: Path | None
    commands_log_path: Path | None

@dataclass
class ScopeService:
    config: WaveBenchConfig
    logger: CommandLogger

    def _open_scope(self) -> RTM2032Scope:
        transport = RsInstrumentTransport.open(self.config.connection, logger=self.logger)
        return RTM2032Scope(transport=transport, check_errors_after_ops=self.config.scope.check_errors)

    def idn(self) -> str:
        scope = self._open_scope()
        try:
            return scope.idn()
        finally:
            scope.close()

    def errors(self) -> list[str]:
        scope = self._open_scope()
        try:
            return scope.errors()
        finally:
            scope.close()

    def autoscale(self) -> None:
        scope = self._open_scope()
        try:
            scope.autoscale(
                wait_opc=self.config.autoscale.wait_opc,
                check_errors=self.config.autoscale.check_errors,
            )
        finally:
            scope.close()

    def fetch_waveform(self, channel: int) -> WaveformData:
        if self.config.waveform.format.lower() != "real":
            raise ConfigError("MVP-1 only supports waveform.format = 'real'")
        if self.config.waveform.byte_order.lower() != "lsbf":
            raise ConfigError("MVP-1 only supports waveform.byte_order = 'lsbf'")
        scope = self._open_scope()
        try:
            return scope.fetch_waveform(
                channel=channel,
                points=self.config.waveform.points,
                check_errors=self.config.scope.check_errors,
            )
        finally:
            scope.close()

    def capture_waveform(self, channel: int, label: str) -> CaptureResult:
        package_dir = new_package_dir(self.config.output.directory, label)
        package_dir.mkdir(parents=True, exist_ok=False)
        commands_log_path = package_dir / "commands.log" if self.config.output.save_commands_log else None
        if commands_log_path is not None:
            self.logger.path = commands_log_path
        try:
            scope = self._open_scope()
            try:
                instrument_idn = scope.idn()
                waveform = scope.capture_waveform(
                    channel=channel,
                    points=self.config.waveform.points,
                    check_errors=self.config.scope.check_errors,
                    time_range_s=self.config.waveform.time_range_s,
                )
            finally:
                scope.close()
        except Exception as exc:
            failed_dir = package_dir.with_name(package_dir.name + "_failed")
            package_dir.rename(failed_dir)
            (failed_dir / "error.txt").write_text(
                f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}",
                encoding="utf-8",
            )
            partial = {
                "instrument": {"resource": self.config.connection.resource},
                "operation": {
                    "command": "scope capture",
                    "channel": channel,
                    "label": label,
                    "time_range_s": self.config.waveform.time_range_s,
                    "expected_frequency_hz": self.config.waveform.expected_frequency_hz,
                    "frequency_tolerance_ratio": self.config.waveform.frequency_tolerance_ratio,
                    "failed": True,
                },
                "error": {"type": type(exc).__name__, "message": str(exc)},
                "files": {"commands": str(failed_dir / "commands.log")} if commands_log_path is not None else {},
            }
            (failed_dir / "metadata.partial.json").write_text(
                json.dumps(partial, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            if isinstance(exc, WaveBenchError):
                raise
            raise
        times = waveform.times_s
        files: dict[str, str] = {}
        csv_path: Path | None = None
        npy_path: Path | None = None

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

        metadata: dict[str, Any] = {
            "instrument": {"idn": instrument_idn, "resource": self.config.connection.resource},
            "operation": {
                "command": "scope capture",
                "channel": channel,
                "label": label,
                "triggered_single": True,
                "time_range_s": self.config.waveform.time_range_s,
                "expected_frequency_hz": self.config.waveform.expected_frequency_hz,
                "frequency_tolerance_ratio": self.config.waveform.frequency_tolerance_ratio,
            },
            "waveform": {
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
            },
            "files": files,
        }
        metadata_path = package_dir / "metadata.json"
        if self.config.output.save_json:
            metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
        return CaptureResult(
            package_dir=package_dir,
            waveform=waveform,
            metadata_path=metadata_path,
            csv_path=csv_path,
            npy_path=npy_path,
            commands_log_path=commands_log_path,
        )
