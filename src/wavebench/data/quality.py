from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class WaveformQuality:
    voltage_min_v: float
    voltage_max_v: float
    voltage_mean_v: float
    voltage_rms_v: float
    voltage_vpp_v: float
    frequency_estimate_hz: float | None
    frequency_method: str
    estimated_cycles: float | None
    expected_frequency_hz: float | None
    frequency_error_ratio: float | None
    frequency_in_tolerance: bool | None
    quality_warnings: list[str]

    def as_dict(self) -> dict[str, object]:
        return {
            "voltage_min_v": self.voltage_min_v,
            "voltage_max_v": self.voltage_max_v,
            "voltage_mean_v": self.voltage_mean_v,
            "voltage_rms_v": self.voltage_rms_v,
            "voltage_vpp_v": self.voltage_vpp_v,
            "frequency_estimate_hz": self.frequency_estimate_hz,
            "frequency_method": self.frequency_method,
            "estimated_cycles": self.estimated_cycles,
            "expected_frequency_hz": self.expected_frequency_hz,
            "frequency_error_ratio": self.frequency_error_ratio,
            "frequency_in_tolerance": self.frequency_in_tolerance,
            "quality_warnings": self.quality_warnings,
        }


def estimate_frequency_hysteresis(times_s: np.ndarray, voltages_v: np.ndarray) -> float | None:
    if times_s.size != voltages_v.size or times_s.size < 3:
        return None
    v_min = float(np.min(voltages_v))
    v_max = float(np.max(voltages_v))
    span = v_max - v_min
    if span <= 0:
        return None

    center = (v_max + v_min) / 2.0
    hysteresis = span * 0.10
    low = center - hysteresis
    high = center + hysteresis

    armed = bool(voltages_v[0] < low)
    crossings: list[float] = []
    prev_v = float(voltages_v[0])
    prev_t = float(times_s[0])

    for time_s, voltage_v in zip(times_s[1:], voltages_v[1:]):
        v = float(voltage_v)
        t = float(time_s)
        if not armed:
            if v < low:
                armed = True
        elif prev_v < center <= v:
            fraction = (center - prev_v) / (v - prev_v) if v != prev_v else 0.0
            crossings.append(prev_t + fraction * (t - prev_t))
            armed = False
        prev_v = v
        prev_t = t

    if len(crossings) < 2:
        return None
    periods = np.diff(np.asarray(crossings, dtype=np.float64))
    periods = periods[periods > 0]
    if periods.size == 0:
        return None
    return float(1.0 / np.median(periods))


def estimate_frequency_fft(times_s: np.ndarray, voltages_v: np.ndarray, max_points: int = 262_144) -> float | None:
    if times_s.size != voltages_v.size or times_s.size < 4:
        return None
    step = max(1, int(np.ceil(times_s.size / max_points)))
    sampled_times = times_s[::step]
    sampled_voltages = voltages_v[::step]
    if sampled_times.size < 4:
        return None
    dt = float(np.median(np.diff(sampled_times)))
    if dt <= 0:
        return None
    centered = sampled_voltages - np.mean(sampled_voltages)
    spectrum = np.fft.rfft(centered)
    magnitudes = np.abs(spectrum)
    if magnitudes.size <= 1:
        return None
    peak_index = int(np.argmax(magnitudes[1:]) + 1)
    frequencies = np.fft.rfftfreq(sampled_times.size, dt)
    frequency = float(frequencies[peak_index])
    return frequency if frequency > 0 else None


def estimate_cycles_in_window(times_s: np.ndarray, frequency_hz: float | None) -> float | None:
    if frequency_hz is None or times_s.size < 2:
        return None
    dt = float(np.median(np.diff(times_s)))
    if dt <= 0:
        return None
    duration = float(times_s[-1] - times_s[0] + dt)
    if duration <= 0:
        return None
    return float(frequency_hz * duration)


def frequency_error_ratio(frequency_hz: float | None, expected_frequency_hz: float | None) -> float | None:
    if frequency_hz is None or expected_frequency_hz is None or expected_frequency_hz <= 0:
        return None
    return float(abs(frequency_hz - expected_frequency_hz) / expected_frequency_hz)


def quality_warnings(estimated_cycles: float | None, frequency_error: float | None, tolerance_ratio: float) -> list[str]:
    warnings: list[str] = []
    if estimated_cycles is not None and estimated_cycles < 2.0:
        warnings.append("low_cycle_count: waveform window contains fewer than 2 estimated cycles; frequency estimate may be unreliable")
    if frequency_error is not None and frequency_error > tolerance_ratio:
        warnings.append("frequency_mismatch: estimated frequency differs from expected frequency")
    return warnings


def summarize_waveform(
    times_s: np.ndarray,
    voltages_v: np.ndarray,
    *,
    expected_frequency_hz: float | None = None,
    frequency_tolerance_ratio: float = 0.05,
) -> WaveformQuality:
    frequency = estimate_frequency_hysteresis(times_s, voltages_v)
    method = "hysteresis_rising_crossing"
    if frequency is None:
        frequency = estimate_frequency_fft(times_s, voltages_v)
        method = "fft_peak"
    estimated_cycles = estimate_cycles_in_window(times_s, frequency)
    freq_error = frequency_error_ratio(frequency, expected_frequency_hz)
    return WaveformQuality(
        voltage_min_v=float(np.min(voltages_v)),
        voltage_max_v=float(np.max(voltages_v)),
        voltage_mean_v=float(np.mean(voltages_v)),
        voltage_rms_v=float(np.sqrt(np.mean(np.square(voltages_v)))),
        voltage_vpp_v=float(np.max(voltages_v) - np.min(voltages_v)),
        frequency_estimate_hz=frequency,
        frequency_method=method,
        estimated_cycles=estimated_cycles,
        expected_frequency_hz=expected_frequency_hz,
        frequency_error_ratio=freq_error,
        frequency_in_tolerance=None if freq_error is None else freq_error <= frequency_tolerance_ratio,
        quality_warnings=quality_warnings(estimated_cycles, freq_error, frequency_tolerance_ratio),
    )
