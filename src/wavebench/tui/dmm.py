from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from wavebench.config import WaveBenchConfig, load_config
from wavebench.drivers.dm3000 import DmmReading, normalize_dmm_function
from wavebench.logging import CommandLogger
from wavebench.services.dmm_service import DmmService
from wavebench.tui.state import DmmPanelState, dmm_state_from_reading


class DmmPanelAdapter(Protocol):
    def read(self, function: str | None = None) -> DmmPanelState:
        ...

    def function_status(self) -> str:
        ...

    def set_function(self, function: str) -> DmmPanelState:
        ...


@dataclass
class DmmServicePanelAdapter:
    service: DmmService
    _instrument_id: str | None = None
    _active_function: str = "dcv"

    @classmethod
    def from_config(
        cls, config_path: str | Path = "wavebench.toml", resource: str | None = None
    ) -> "DmmServicePanelAdapter":
        config = load_config(config_path)
        if resource:
            config = config.with_dmm_resource(resource)
        return cls(service=DmmService(config=config, logger=CommandLogger()))

    def function_status(self) -> str:
        self._active_function = self.service.function_status()
        return self._active_function

    def read(self, function: str | None = None) -> DmmPanelState:
        if self._instrument_id is None:
            self._instrument_id = self.service.idn()
        normalized_function = self._active_function if function is None else normalize_dmm_function(function)
        normalized_function = normalized_function or "dcv"
        self._active_function = normalized_function
        reading = self.service.read(function=normalized_function)
        return build_dmm_panel_state(
            config=self.service.config,
            instrument_id=self._instrument_id,
            reading=reading,
            log_lines=_logger_lines(self.service.logger),
        )

    def set_function(self, function: str) -> DmmPanelState:
        if self._instrument_id is None:
            self._instrument_id = self.service.idn()
        applied_function = self.service.set_function(function=function)
        self._active_function = applied_function
        reading = self.service.read(function=applied_function)
        return build_dmm_panel_state(
            config=self.service.config,
            instrument_id=self._instrument_id,
            reading=reading,
            log_lines=_logger_lines(self.service.logger),
        )


@dataclass
class FakeDmmPanelAdapter:
    readings: dict[str, DmmReading] = field(default_factory=dict)
    log_lines: list[str] = field(default_factory=list)
    instrument_id: str = "RIGOL TECHNOLOGIES,DM3058,FAKE,0.0"
    current_function: str = "dcv"

    def __post_init__(self) -> None:
        if not self.readings:
            self.readings = {
                "dcv": DmmReading(function="dcv", value=1.2345, unit="V", raw="1.2345"),
                "acv": DmmReading(function="acv", value=0.0123, unit="V", raw="0.0123"),
                "res": DmmReading(function="res", value=1000.0, unit="ohm", raw="1000"),
            }

    def function_status(self) -> str:
        return self.current_function

    def set_function(self, function: str) -> DmmPanelState:
        key = function.strip().lower() or "dcv"
        aliases = {"vdc": "dcv", "vac": "acv", "ohm": "res", "r": "res", "cont": "continuity"}
        key = aliases.get(key, key)
        if key not in self.readings:
            self.readings[key] = DmmReading(function=key, value=0.0, unit="", raw="0")
        self.current_function = key
        self.log_lines.append(f"功能切换 / Function set fake DMM {self.current_function}")
        return self.read(function=self.current_function)

    def read(self, function: str | None = None) -> DmmPanelState:
        key = self.current_function if function is None else function.strip().lower()
        key = key or self.current_function or "dcv"
        aliases = {"vdc": "dcv", "vac": "acv", "ohm": "res", "r": "res", "cont": "continuity"}
        key = aliases.get(key, key)
        self.current_function = key
        reading = self.readings.get(
            key,
            DmmReading(function=key, value=0.0, unit="", raw="0"),
        )
        self.log_lines.append(f"读取 / Read fake DMM {reading.function}")
        return DmmPanelState(
            config_status="演示模式 / Fake mode: DM3000 snapshot",
            connection_status="已连接 / Connected",
            instrument_status=f"仪器 / Instrument: {self.instrument_id}",
            function=reading.function,
            value=f"{reading.value:.6g}",
            unit=reading.unit,
            raw_reading=reading.raw,
            log_lines=tuple(self.log_lines[-80:]),
        )


def build_dmm_panel_state(
    *,
    config: WaveBenchConfig,
    instrument_id: str,
    reading: DmmReading,
    log_lines: list[str] | tuple[str, ...] = (),
) -> DmmPanelState:
    return dmm_state_from_reading(
        config=config,
        instrument_id=instrument_id,
        reading=reading,
        log_lines=log_lines,
    )


def _logger_lines(logger: CommandLogger) -> list[str]:
    return [f"{entry.timestamp} {entry.direction} {entry.text}" for entry in logger.entries[-80:]]
