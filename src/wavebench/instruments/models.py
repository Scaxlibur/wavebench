from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from wavebench.data.quality import summarize_waveform


@dataclass(frozen=True)
class WaveformHeader:
    x_start: float
    x_stop: float
    points: int
    segment: int | None = None

    @property
    def x_increment(self) -> float:
        if self.points <= 1:
            return 0.0
        return (self.x_stop - self.x_start) / (self.points - 1)

    @property
    def duration(self) -> float:
        return self.x_stop - self.x_start


@dataclass(frozen=True)
class WaveformData:
    channel: int
    header: WaveformHeader
    voltages_v: np.ndarray

    @property
    def times_s(self) -> np.ndarray:
        if self.header.points <= 1:
            return np.array([self.header.x_start], dtype=np.float64)
        return np.linspace(
            self.header.x_start,
            self.header.x_stop,
            self.header.points,
            dtype=np.float64,
        )

    @property
    def sample_count(self) -> int:
        return int(self.voltages_v.size)

    def summary(
        self,
        *,
        expected_frequency_hz: float | None = None,
        frequency_tolerance_ratio: float = 0.05,
    ) -> dict[str, object]:
        quality = summarize_waveform(
            self.times_s,
            self.voltages_v,
            expected_frequency_hz=expected_frequency_hz,
            frequency_tolerance_ratio=frequency_tolerance_ratio,
        )
        return {
            "channel": self.channel,
            "samples": self.sample_count,
            "x_start_s": self.header.x_start,
            "x_stop_s": self.header.x_stop,
            "x_increment_s": self.header.x_increment,
            **quality.as_dict(),
        }


@dataclass(frozen=True)
class SourceStatus:
    channel: int
    output: str
    function: str
    frequency_hz: float | None
    amplitude: float | None
    amplitude_unit: str | None
    offset_v: float | None
    phase_deg: float | None
    frequency_mode: str
    sweep_enabled: str
    apply_raw: str | None
    square_duty_cycle_percent: float | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "channel": self.channel,
            "output": self.output,
            "function": self.function,
            "frequency_hz": self.frequency_hz,
            "amplitude": self.amplitude,
            "amplitude_unit": self.amplitude_unit,
            "offset_v": self.offset_v,
            "phase_deg": self.phase_deg,
            "frequency_mode": self.frequency_mode,
            "sweep_enabled": self.sweep_enabled,
            "apply_raw": self.apply_raw,
            "square_duty_cycle_percent": self.square_duty_cycle_percent,
        }


@dataclass(frozen=True)
class PowerStatus:
    channel: int
    output: str
    mode: str
    rating: str | None
    set_voltage_v: float | None
    set_current_a: float | None
    measured_voltage_v: float | None
    measured_current_a: float | None
    measured_power_w: float | None

    def as_dict(self) -> dict[str, object]:
        return {
            "channel": self.channel,
            "output": self.output,
            "mode": self.mode,
            "rating": self.rating,
            "set_voltage_v": self.set_voltage_v,
            "set_current_a": self.set_current_a,
            "measured_voltage_v": self.measured_voltage_v,
            "measured_current_a": self.measured_current_a,
            "measured_power_w": self.measured_power_w,
        }


@dataclass(frozen=True)
class PowerMeasurement:
    channel: int
    measured_voltage_v: float | None
    measured_current_a: float | None
    measured_power_w: float | None


@dataclass(frozen=True)
class PowerProtectionStatus:
    channel: int
    ovp_enabled: str
    ovp_threshold_v: float | None
    ovp_tripped: str
    ocp_enabled: str
    ocp_threshold_a: float | None
    ocp_tripped: str

    def as_dict(self) -> dict[str, object]:
        return {
            "channel": self.channel,
            "ovp_enabled": self.ovp_enabled,
            "ovp_threshold_v": self.ovp_threshold_v,
            "ovp_tripped": self.ovp_tripped,
            "ocp_enabled": self.ocp_enabled,
            "ocp_threshold_a": self.ocp_threshold_a,
            "ocp_tripped": self.ocp_tripped,
        }


@dataclass(frozen=True)
class DmmReading:
    function: str
    value: float
    unit: str
    raw: str

    def as_dict(self) -> dict[str, object]:
        return {
            "function": self.function,
            "value": self.value,
            "unit": self.unit,
            "raw": self.raw,
        }
