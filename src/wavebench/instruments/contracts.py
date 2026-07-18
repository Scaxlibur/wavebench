from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .models import (
    DmmReading,
    PowerMeasurement,
    PowerProtectionStatus,
    PowerStatus,
    SourceStatus,
    WaveformData,
)


@runtime_checkable
class InstrumentDriver(Protocol):
    def idn(self) -> str: ...

    def close(self) -> None: ...


@runtime_checkable
class ScopeDriver(InstrumentDriver, Protocol):
    def errors(self, limit: int = 16) -> list[str]: ...

    def channel_coupling(self, channel: int) -> str: ...

    def autoscale(self, wait_opc: bool = True, check_errors: bool = True) -> None: ...

    def fetch_waveform(
        self,
        channel: int,
        points: str = "dmax",
        check_errors: bool = True,
    ) -> WaveformData: ...

    def capture_waveform(
        self,
        channel: int,
        points: str = "dmax",
        check_errors: bool = True,
        time_range_s: float | None = None,
        vertical_scale_v_per_div: float | None = None,
    ) -> WaveformData: ...

    def screenshot_png(
        self,
        *,
        include_menu: bool = False,
        color_scheme: str = "COL",
    ) -> bytes: ...


@runtime_checkable
class SourceDriver(InstrumentDriver, Protocol):
    def errors(self, limit: int = 8) -> list[str]: ...

    def assert_no_errors(self) -> None: ...

    def get_status(self, channel: int) -> SourceStatus: ...

    def set_frequency(
        self,
        channel: int,
        value_hz: float,
        *,
        ensure_fix_mode: bool = True,
        check_errors: bool = True,
    ) -> SourceStatus: ...

    def set_output(
        self,
        channel: int,
        enabled: bool,
        *,
        check_errors: bool = True,
    ) -> SourceStatus: ...

    def set_function(
        self,
        channel: int,
        function: str,
        *,
        check_errors: bool = True,
    ) -> SourceStatus: ...

    def set_amplitude_vpp(
        self,
        channel: int,
        value_vpp: float,
        *,
        check_errors: bool = True,
    ) -> SourceStatus: ...

    def set_square_duty_cycle(
        self,
        channel: int,
        duty_percent: float,
        *,
        check_errors: bool = True,
    ) -> SourceStatus: ...

    def upload_dg4000_dac14_block(self, **kwargs: Any) -> SourceStatus: ...

    def probe_arbitrary_queries(self, channel: int) -> list[Any]: ...


@runtime_checkable
class PowerDriver(InstrumentDriver, Protocol):
    def get_status(self, channel: int) -> PowerStatus: ...

    def get_measurement(self, channel: int) -> PowerMeasurement: ...

    def get_protection_status(self, channel: int) -> PowerProtectionStatus: ...

    def set_protection(self, channel: int, **kwargs: Any) -> PowerProtectionStatus: ...

    def set_voltage_current_limit(
        self,
        channel: int,
        voltage_v: float,
        current_limit_a: float,
        **kwargs: Any,
    ) -> PowerStatus: ...

    def set_output(self, channel: int, enabled: bool, **kwargs: Any) -> PowerStatus: ...


@runtime_checkable
class DmmDriver(InstrumentDriver, Protocol):
    def function_status(self) -> str: ...

    def set_function(self, function: str) -> str: ...

    def read(self, function: str = "dcv") -> DmmReading: ...
