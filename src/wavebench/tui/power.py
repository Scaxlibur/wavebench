from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from wavebench.config import WaveBenchConfig, load_config
from wavebench.drivers.dp800 import PowerStatus
from wavebench.logging import CommandLogger
from wavebench.services.power_service import PowerService
from wavebench.tui.state import PowerPanelState, channel_state_from_status, config_status


class PowerPanelAdapter(Protocol):
    def refresh(self) -> PowerPanelState:
        ...

    def set_output(self, channel: int, enabled: bool) -> PowerPanelState:
        ...

    def set_voltage_current_limit(
        self, channel: int, voltage_v: float, current_limit_a: float
    ) -> PowerPanelState:
        ...


@dataclass
class PowerServicePanelAdapter:
    service: PowerService
    channels: tuple[int, ...] = (1, 2, 3)
    _instrument_id: str | None = None

    @classmethod
    def from_config(
        cls, config_path: str | Path = "wavebench.toml", resource: str | None = None
    ) -> "PowerServicePanelAdapter":
        config = load_config(config_path)
        if resource:
            config = config.with_power_resource(resource)
        return cls(service=PowerService(config=config, logger=CommandLogger()))

    def refresh(self) -> PowerPanelState:
        if self._instrument_id is None:
            self._instrument_id = self.service.idn()
        statuses = [self.service.status(channel=channel) for channel in self.channels]
        return build_power_panel_state(
            config=self.service.config,
            instrument_id=self._instrument_id,
            statuses=statuses,
            log_lines=_logger_lines(self.service.logger),
        )

    def set_output(self, channel: int, enabled: bool) -> PowerPanelState:
        self.service.set_output(channel=channel, enabled=enabled)
        return self.refresh()

    def set_voltage_current_limit(
        self, channel: int, voltage_v: float, current_limit_a: float
    ) -> PowerPanelState:
        self.service.set_voltage_current_limit(
            channel=channel,
            voltage_v=voltage_v,
            current_limit_a=current_limit_a,
        )
        return self.refresh()


@dataclass
class FakePowerPanelAdapter:
    statuses: dict[int, PowerStatus] = field(default_factory=dict)
    log_lines: list[str] = field(default_factory=list)
    instrument_id: str = "RIGOL TECHNOLOGIES,DP832A,FAKE,0.0"

    def __post_init__(self) -> None:
        if not self.statuses:
            self.statuses = {
                channel: PowerStatus(
                    channel=channel,
                    output="OFF",
                    mode="CV",
                    rating="30V/3A" if channel < 3 else "5V/3A",
                    set_voltage_v=0.0,
                    set_current_a=0.1,
                    measured_voltage_v=0.0,
                    measured_current_a=0.0,
                    measured_power_w=0.0,
                )
                for channel in (1, 2, 3)
            }

    def refresh(self) -> PowerPanelState:
        self.log_lines.append("刷新 / Refresh fake DP832A snapshot")
        return PowerPanelState(
            config_status="演示模式 / Fake mode: DP832A snapshot",
            instrument_status=f"仪器 / Instrument: {self.instrument_id}",
            channels=tuple(channel_state_from_status(self.statuses[channel]) for channel in (1, 2, 3)),
            log_lines=tuple(self.log_lines[-80:]),
        )

    def set_output(self, channel: int, enabled: bool) -> PowerPanelState:
        old = self.statuses[channel]
        self.statuses[channel] = PowerStatus(
            channel=old.channel,
            output="ON" if enabled else "OFF",
            mode=old.mode,
            rating=old.rating,
            set_voltage_v=old.set_voltage_v,
            set_current_a=old.set_current_a,
            measured_voltage_v=old.set_voltage_v if enabled else 0.0,
            measured_current_a=old.measured_current_a,
            measured_power_w=(old.set_voltage_v or 0.0) * (old.measured_current_a or 0.0),
        )
        self.log_lines.append(f"CH{channel} 输出 / Output -> {'ON' if enabled else 'OFF'}")
        return self.refresh()

    def set_voltage_current_limit(
        self, channel: int, voltage_v: float, current_limit_a: float
    ) -> PowerPanelState:
        old = self.statuses[channel]
        self.statuses[channel] = PowerStatus(
            channel=old.channel,
            output=old.output,
            mode=old.mode,
            rating=old.rating,
            set_voltage_v=voltage_v,
            set_current_a=current_limit_a,
            measured_voltage_v=voltage_v if old.output == "ON" else 0.0,
            measured_current_a=old.measured_current_a,
            measured_power_w=(voltage_v if old.output == "ON" else 0.0) * (old.measured_current_a or 0.0),
        )
        self.log_lines.append(f"CH{channel} 设定 / Set {voltage_v:g} V, {current_limit_a:g} A")
        return self.refresh()


def build_power_panel_state(
    *,
    config: WaveBenchConfig,
    instrument_id: str,
    statuses: list[PowerStatus],
    log_lines: list[str] | tuple[str, ...] = (),
) -> PowerPanelState:
    return PowerPanelState(
        config_status=config_status(config),
        instrument_status=f"仪器 / Instrument: {instrument_id}",
        channels=tuple(channel_state_from_status(status) for status in statuses),
        log_lines=tuple(log_lines),
    )


def _logger_lines(logger: CommandLogger) -> list[str]:
    return [f"{entry.timestamp} {entry.direction} {entry.text}" for entry in logger.entries[-80:]]
