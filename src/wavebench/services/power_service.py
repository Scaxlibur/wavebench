from __future__ import annotations

from dataclasses import dataclass

from wavebench.config import ConnectionConfig, PowerConfig, WaveBenchConfig
from wavebench.drivers.dp800 import DP800Power, PowerStatus
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
