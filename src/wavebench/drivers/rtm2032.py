from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from wavebench.data.quality import summarize_waveform
from wavebench.errors import DataError, InstrumentError, OperationTimeout
from wavebench.transport.base import InstrumentTransport

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
        return np.linspace(self.header.x_start, self.header.x_stop, self.header.points, dtype=np.float64)

    @property
    def sample_count(self) -> int:
        return int(self.voltages_v.size)

    def summary(
        self, *, expected_frequency_hz: float | None = None, frequency_tolerance_ratio: float = 0.05
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

def parse_waveform_header(response: str) -> WaveformHeader:
    parts = [item.strip() for item in response.split(",")]
    if len(parts) < 3:
        raise DataError(f"invalid CHAN:DATA:HEAD? response: {response!r}")
    try:
        x_start = float(parts[0])
        x_stop = float(parts[1])
        points = int(float(parts[2]))
        segment = int(float(parts[3])) if len(parts) >= 4 else None
    except ValueError as exc:
        raise DataError(f"invalid CHAN:DATA:HEAD? response: {response!r}") from exc
    if points <= 0:
        raise DataError(f"invalid waveform point count: {points}")
    return WaveformHeader(x_start=x_start, x_stop=x_stop, points=points, segment=segment)

@dataclass
class RTM2032Scope:
    transport: InstrumentTransport
    check_errors_after_ops: bool = True

    def idn(self) -> str:
        return self.transport.query("*IDN?")

    def clear_status(self) -> None:
        self.transport.write("*CLS")

    def channel_coupling(self, channel: int) -> str:
        if channel < 1:
            raise DataError("channel must be >= 1")
        return self.transport.query(f"CHAN{channel}:COUP?").strip().upper()

    def errors(self, limit: int = 16) -> list[str]:
        errors: list[str] = []
        for _ in range(limit):
            response = self.transport.query("SYST:ERR?")
            errors.append(response)
            if response.startswith("0") or "No error" in response:
                break
        return errors

    def assert_no_errors(self) -> None:
        errors = self.errors()
        active = [item for item in errors if not (item.startswith("0") or "No error" in item)]
        if active:
            raise InstrumentError("instrument error queue is not empty: " + "; ".join(active))

    def autoscale(self, wait_opc: bool = True, check_errors: bool = True) -> None:
        self.transport.write("AUToscale")
        if wait_opc:
            self.transport.query_opc()
        if check_errors:
            self.assert_no_errors()

    def set_time_range(self, time_range_s: float) -> None:
        if time_range_s <= 0:
            raise DataError("time range must be > 0")
        self.transport.write(f"TIMebase:RANGe {time_range_s:.12g}")

    def _setup_real_waveform_transfer(self, channel: int, points: str) -> None:
        if channel < 1:
            raise DataError("channel must be >= 1")
        self.transport.write(f"CHAN{channel}:STAT ON")
        self.transport.write("FORM REAL")
        self.transport.write("FORM:BORD LSBF")
        self.transport.write(f"CHAN:DATA:POIN {points.upper()}")

    def _read_waveform(self, channel: int) -> WaveformData:
        header = parse_waveform_header(self.transport.query(f"CHAN{channel}:DATA:HEAD?"))
        voltages = np.asarray(self.transport.query_float_list(f"CHAN{channel}:DATA?"), dtype=np.float64)
        if voltages.size != header.points:
            raise DataError(f"waveform length mismatch: header says {header.points}, got {voltages.size}")
        return WaveformData(channel=channel, header=header, voltages_v=voltages)

    def fetch_waveform(self, channel: int, points: str = "dmax", check_errors: bool = True) -> WaveformData:
        self._setup_real_waveform_transfer(channel=channel, points=points)
        waveform = self._read_waveform(channel=channel)
        if check_errors:
            self.assert_no_errors()
        return waveform

    def capture_waveform(
        self, channel: int, points: str = "dmax", check_errors: bool = True, time_range_s: float | None = None
    ) -> WaveformData:
        self.transport.write("*CLS")
        if time_range_s is not None:
            self.set_time_range(time_range_s)
        self._setup_real_waveform_transfer(channel=channel, points=points)
        self.transport.write("SINGle")
        try:
            self.transport.query_opc()
        except Exception as exc:
            raise OperationTimeout(
                "single acquisition timed out while waiting for *OPC?. "
                "Check trigger source/level, or use `scope fetch` to read the current waveform."
            ) from exc
        waveform = self._read_waveform(channel=channel)
        if check_errors:
            self.assert_no_errors()
        return waveform

    def screenshot_png(self, *, include_menu: bool = False, color_scheme: str = "COL") -> bytes:
        self.transport.write("HCOP:LANG PNG")
        self.transport.write(f"HCOP:COL:SCH {color_scheme}")
        self.transport.write(f"HCOP:MENU {'ON' if include_menu else 'OFF'}")
        data = self.transport.query_bin_block("HCOP:DATA?")
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise DataError("screenshot response is not a PNG image")
        return data

    def close(self) -> None:
        self.transport.close()
