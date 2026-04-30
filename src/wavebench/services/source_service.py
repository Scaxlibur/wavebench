from __future__ import annotations

from dataclasses import dataclass
import time

from wavebench.config import ConnectionConfig, SourceConfig, WaveBenchConfig
from wavebench.drivers.dg4202 import DG4202Source, SourceStatus
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.services.source_state import RestorableSourceState
from wavebench.transport.pyvisa_transport import PyVisaTransport


@dataclass
class SourceService:
    config: WaveBenchConfig
    logger: CommandLogger

    def _source_config(self) -> SourceConfig:
        if self.config.source is None or not self.config.source.resource:
            raise ConfigError("source resource is not configured. Set [source].resource or pass --resource.")
        return self.config.source

    def _open_source(self) -> DG4202Source:
        source = self._source_config()
        connection = ConnectionConfig(
            backend=self.config.connection.backend,
            resource=source.resource,
            timeout_ms=self.config.connection.timeout_ms,
            opc_timeout_ms=self.config.connection.opc_timeout_ms,
        )
        transport = PyVisaTransport.open(connection, logger=self.logger)
        return DG4202Source(transport=transport, check_errors_after_ops=source.check_errors)

    def idn(self) -> str:
        source = self._open_source()
        try:
            return source.idn()
        finally:
            source.close()

    def errors(self) -> list[str]:
        source = self._open_source()
        try:
            return source.errors()
        finally:
            source.close()

    def status(self, channel: int | None = None) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        source = self._open_source()
        try:
            return source.get_status(channel)
        finally:
            source.close()

    def snapshot_restorable_state(self, channel: int | None = None) -> RestorableSourceState:
        return RestorableSourceState.from_status(self.status(channel=channel))

    def restore_restorable_state(self, state: RestorableSourceState) -> SourceStatus:
        self.set_function(channel=state.channel, function=state.function)
        self.set_amplitude_vpp(channel=state.channel, value_vpp=state.amplitude_vpp)
        self.set_frequency(channel=state.channel, value_hz=state.frequency_hz)
        return self.set_output(channel=state.channel, enabled=state.output == "ON")

    def set_frequency(self, channel: int | None, value_hz: float) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        source = self._open_source()
        try:
            status = source.set_frequency(
                channel,
                value_hz,
                ensure_fix_mode=source_cfg.ensure_fix_mode_on_set_frequency,
                check_errors=False,
            )
            if source_cfg.settle_ms_after_set_frequency:
                time.sleep(source_cfg.settle_ms_after_set_frequency / 1000.0)
                status = source.get_status(channel)
            if source_cfg.check_errors:
                source.assert_no_errors()
            return status
        finally:
            source.close()

    def set_output(self, channel: int | None, enabled: bool) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        source = self._open_source()
        try:
            return source.set_output(channel, enabled, check_errors=source_cfg.check_errors)
        finally:
            source.close()

    def set_function(self, channel: int | None, function: str) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        source = self._open_source()
        try:
            return source.set_function(channel, function, check_errors=source_cfg.check_errors)
        finally:
            source.close()

    def set_amplitude_vpp(self, channel: int | None, value_vpp: float) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        source = self._open_source()
        try:
            return source.set_amplitude_vpp(channel, value_vpp, check_errors=source_cfg.check_errors)
        finally:
            source.close()
