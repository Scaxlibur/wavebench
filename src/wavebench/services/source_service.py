from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
import time

from wavebench.arbitrary import build_dg4000_dac14_binary_block, load_arbitrary_waveform
from wavebench.config import ConnectionConfig, SourceConfig, WaveBenchConfig
from wavebench.drivers.dg4202 import ArbitraryQueryProbeResult, DG4202Source, SourceStatus
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.services.source_state import RestorableSourceState
from wavebench.transport.pyvisa_transport import PyVisaTransport


@dataclass
class SourceService:
    config: WaveBenchConfig
    logger: CommandLogger
    session: DG4202Source | None = None

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
            read_retry_attempts=self.config.connection.read_retry_attempts,
            read_retry_delay_ms=self.config.connection.read_retry_delay_ms,
        )
        transport = PyVisaTransport.open(connection, logger=self.logger)
        return DG4202Source(transport=transport, check_errors_after_ops=source.check_errors)

    def open_session(self) -> DG4202Source:
        return self._open_source()

    @contextmanager
    def _source_session(self) -> Iterator[DG4202Source]:
        if self.session is not None:
            yield self.session
            return
        source = self._open_source()
        try:
            yield source
        finally:
            source.close()

    def idn(self) -> str:
        with self._source_session() as source:
            return source.idn()

    def errors(self) -> list[str]:
        with self._source_session() as source:
            return source.errors()

    def status(self, channel: int | None = None) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
            return source.get_status(channel)

    def snapshot_restorable_state(self, channel: int | None = None) -> RestorableSourceState:
        return RestorableSourceState.from_status(self.status(channel=channel))

    def restore_restorable_state(self, state: RestorableSourceState) -> SourceStatus:
        self.set_function(channel=state.channel, function=state.function)
        self.set_amplitude_vpp(channel=state.channel, value_vpp=state.amplitude_vpp)
        self.set_frequency(channel=state.channel, value_hz=state.frequency_hz)
        if state.square_duty_cycle_percent is not None:
            self.set_square_duty_cycle(
                channel=state.channel,
                duty_percent=state.square_duty_cycle_percent,
            )
        return self.set_output(channel=state.channel, enabled=state.output == "ON")

    def set_frequency(self, channel: int | None, value_hz: float) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
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

    def set_output(self, channel: int | None, enabled: bool) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
            if enabled:
                status = source.get_status(channel)
                self._check_source_vpp(status.amplitude, field="source output amplitude / 信号源输出幅度")
            return source.set_output(channel, enabled, check_errors=source_cfg.check_errors)

    def set_function(self, channel: int | None, function: str) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
            return source.set_function(channel, function, check_errors=source_cfg.check_errors)

    def set_square_duty_cycle(self, channel: int | None, duty_percent: float) -> SourceStatus:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
            return source.set_square_duty_cycle(channel, duty_percent, check_errors=source_cfg.check_errors)

    def set_amplitude_vpp(self, channel: int | None, value_vpp: float) -> SourceStatus:
        source_cfg = self._source_config()
        self._check_source_vpp(value_vpp, field="source amplitude / 信号源幅度")
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
            return source.set_amplitude_vpp(channel, value_vpp, check_errors=source_cfg.check_errors)


    def upload_arbitrary_waveform(
        self,
        *,
        channel: int | None,
        file_path: str,
        playback_frequency_hz: float,
        amplitude_vpp: float,
        offset_v: float = 0.0,
        sample_rate_hz: float | None = None,
        max_points: int = 16384,
        byte_order: str = "little",
        output_on: bool = False,
    ) -> SourceStatus:
        source_cfg = self._source_config()
        self._check_source_vpp(amplitude_vpp, field="arbitrary waveform amplitude / 任意波幅度")
        channel = source_cfg.default_channel if channel is None else channel
        waveform = load_arbitrary_waveform(
            file_path,
            sample_rate_hz=sample_rate_hz,
            max_points=max_points,
        )
        block = build_dg4000_dac14_binary_block(waveform, byte_order=byte_order)
        with self._source_session() as source:
            return source.upload_dg4000_dac14_block(
                channel=channel,
                block=block,
                playback_frequency_hz=playback_frequency_hz,
                amplitude_vpp=amplitude_vpp,
                offset_v=offset_v,
                output_on=output_on,
                check_errors=source_cfg.check_errors,
            )

    def _check_source_vpp(self, value_vpp: float, *, field: str) -> None:
        limit = self.config.safety_limits.max_source_vpp
        if limit is not None and value_vpp > limit:
            raise ConfigError(
                f"safety limit exceeded / 安全上限已超出: {field} {value_vpp:.12g} Vpp "
                f"> max_source_vpp {limit:.12g} Vpp"
            )

    def probe_arbitrary_queries(self, channel: int | None = None) -> list[ArbitraryQueryProbeResult]:
        source_cfg = self._source_config()
        channel = source_cfg.default_channel if channel is None else channel
        with self._source_session() as source:
            return source.probe_arbitrary_queries(channel)
