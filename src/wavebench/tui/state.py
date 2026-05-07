from __future__ import annotations

from dataclasses import dataclass

from wavebench.config import WaveBenchConfig
from wavebench.drivers.dm3000 import DmmReading
from wavebench.drivers.dp800 import PowerStatus


@dataclass(frozen=True)
class PowerChannelState:
    channel: int
    output: str
    mode: str
    rating: str
    set_voltage: str
    set_current: str
    measured_voltage: str
    measured_current: str
    measured_power: str


@dataclass(frozen=True)
class PowerPanelState:
    config_status: str
    instrument_status: str
    channels: tuple[PowerChannelState, ...]
    log_lines: tuple[str, ...] = ()


@dataclass(frozen=True)
class DmmPanelState:
    config_status: str
    connection_status: str
    instrument_status: str
    function: str
    value: str
    unit: str
    raw_reading: str
    log_lines: tuple[str, ...] = ()


POWER_TABLE_COLUMNS = (
    "通道 / CH",
    "输出 / Output",
    "模式 / Mode",
    "规格 / Rating",
    "设定电压 / Set V",
    "限流 / Limit A",
    "实测电压 / Meas V",
    "实测电流 / Meas A",
    "功率 / Power W",
)


def format_optional_number(value: float | None, unit: str = "", digits: int = 6) -> str:
    if value is None:
        return "未知 / N/A"
    text = f"{value:.{digits}g}"
    return f"{text}{unit}"


def format_output_state(output: str) -> str:
    normalized = output.strip().upper()
    if normalized in {"ON", "1"}:
        return "开 / ON"
    if normalized in {"OFF", "0"}:
        return "关 / OFF"
    return f"未知 / {output}"


def channel_state_from_status(status: PowerStatus) -> PowerChannelState:
    return PowerChannelState(
        channel=status.channel,
        output=format_output_state(status.output),
        mode=status.mode or "未知 / N/A",
        rating=status.rating or "未知 / N/A",
        set_voltage=format_optional_number(status.set_voltage_v, " V"),
        set_current=format_optional_number(status.set_current_a, " A"),
        measured_voltage=format_optional_number(status.measured_voltage_v, " V"),
        measured_current=format_optional_number(status.measured_current_a, " A"),
        measured_power=format_optional_number(status.measured_power_w, " W"),
    )


def config_status(config: WaveBenchConfig) -> str:
    if config.power is None:
        return "电源配置缺失 / Power config missing"
    resource = config.power.resource or "未配置 / not configured"
    return (
        f"驱动 / Driver: {config.power.driver} | "
        f"资源 / Resource: {resource} | "
        f"默认通道 / Default CH: {config.power.default_channel}"
    )


def dmm_config_status(config: WaveBenchConfig) -> str:
    if config.dmm is None:
        return "万用表配置缺失 / DMM config missing"
    resource = config.dmm.resource or "未配置 / not configured"
    return (
        f"驱动 / Driver: {config.dmm.driver} | "
        f"后端 / Backend: {config.dmm.backend} | "
        f"资源 / Resource: {resource}"
    )


def dmm_state_from_reading(
    *,
    config: WaveBenchConfig,
    instrument_id: str,
    reading: DmmReading,
    log_lines: list[str] | tuple[str, ...] = (),
) -> DmmPanelState:
    return DmmPanelState(
        config_status=dmm_config_status(config),
        connection_status="已连接 / Connected",
        instrument_status=f"仪器 / Instrument: {instrument_id}",
        function=reading.function,
        value=format_optional_number(reading.value),
        unit=reading.unit,
        raw_reading=reading.raw,
        log_lines=tuple(log_lines),
    )
