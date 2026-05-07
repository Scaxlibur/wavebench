from __future__ import annotations

from dataclasses import dataclass

from wavebench.config import ConnectionConfig, PowerConfig, WaveBenchConfig
from wavebench.drivers.dp800 import DP800Power, PowerMeasurement, PowerStatus
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.transport.pyvisa_transport import PyVisaTransport


@dataclass
class PowerService:
    config: WaveBenchConfig
    logger: CommandLogger

    def _power_config(self) -> PowerConfig:
        if self.config.power is None or not self.config.power.resource:
            raise ConfigError("power resource is not configured. Set [power].resource or pass --resource.")
        return self.config.power

    def _open_power(self) -> DP800Power:
        power = self._power_config()
        connection = ConnectionConfig(
            backend=self.config.connection.backend,
            resource=power.resource,
            timeout_ms=self.config.connection.timeout_ms,
            opc_timeout_ms=self.config.connection.opc_timeout_ms,
        )
        transport = PyVisaTransport.open(connection, logger=self.logger)
        return DP800Power(transport=transport, check_errors_after_ops=power.check_errors)

    def idn(self) -> str:
        power = self._open_power()
        try:
            return power.idn()
        finally:
            power.close()

    def status(self, channel: int | None = None) -> PowerStatus:
        power_cfg = self._power_config()
        channel = power_cfg.default_channel if channel is None else channel
        power = self._open_power()
        try:
            return power.get_status(channel)
        finally:
            power.close()

    def measurement(self, channel: int | None = None) -> PowerMeasurement:
        power_cfg = self._power_config()
        channel = power_cfg.default_channel if channel is None else channel
        power = self._open_power()
        try:
            return power.get_measurement(channel)
        finally:
            power.close()

    def set_voltage_current_limit(
        self, channel: int | None, voltage_v: float, current_limit_a: float
    ) -> PowerStatus:
        power_cfg = self._power_config()
        self._check_power_limits(voltage_v=voltage_v, current_limit_a=current_limit_a)
        channel = power_cfg.default_channel if channel is None else channel
        power = self._open_power()
        try:
            return power.set_voltage_current_limit(
                channel,
                voltage_v,
                current_limit_a,
                check_errors=power_cfg.check_errors,
                settle_ms_after_set=power_cfg.settle_ms_after_set,
            )
        finally:
            power.close()

    def _check_power_limits(self, *, voltage_v: float | None, current_limit_a: float | None) -> None:
        max_voltage = self.config.safety_limits.max_power_voltage_v
        if max_voltage is not None and voltage_v is not None and voltage_v > max_voltage:
            raise ConfigError(
                f"safety limit exceeded / 安全上限已超出: power voltage {voltage_v:.12g} V "
                f"> max_power_voltage_v {max_voltage:.12g} V"
            )
        max_current = self.config.safety_limits.max_power_current_limit_a
        if max_current is not None and current_limit_a is not None and current_limit_a > max_current:
            raise ConfigError(
                f"safety limit exceeded / 安全上限已超出: power current limit {current_limit_a:.12g} A "
                f"> max_power_current_limit_a {max_current:.12g} A"
            )

    def set_output(self, channel: int | None, enabled: bool) -> PowerStatus:
        power_cfg = self._power_config()
        channel = power_cfg.default_channel if channel is None else channel
        power = self._open_power()
        try:
            if enabled:
                status = power.get_status(channel)
                self._check_power_limits(
                    voltage_v=status.set_voltage_v,
                    current_limit_a=status.set_current_a,
                )
            return power.set_output(
                channel,
                enabled,
                check_errors=power_cfg.check_errors,
                settle_ms_after_output=power_cfg.settle_ms_after_output,
            )
        finally:
            power.close()
