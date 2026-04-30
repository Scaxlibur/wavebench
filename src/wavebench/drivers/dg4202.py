from __future__ import annotations

from dataclasses import dataclass

from wavebench.errors import DataError, InstrumentError


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


@dataclass
class DG4202Source:
    transport: object
    check_errors_after_ops: bool = True

    def _query_float(self, command: str) -> float | None:
        try:
            return float(self.transport.query(command))
        except Exception:
            return None

    def idn(self) -> str:
        return self.transport.query("*IDN?")

    def errors(self, limit: int = 8) -> list[str]:
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

    def get_status(self, channel: int) -> SourceStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        return SourceStatus(
            channel=channel,
            output=self.transport.query(f":OUTP{channel}?"),
            function=self.transport.query(f":SOUR{channel}:FUNC?"),
            frequency_hz=self._query_float(f":SOUR{channel}:FREQ?"),
            amplitude=self._query_float(f":SOUR{channel}:VOLT?"),
            amplitude_unit=self.transport.query(f":SOUR{channel}:VOLT:UNIT?"),
            offset_v=self._query_float(f":SOUR{channel}:VOLT:OFFS?"),
            phase_deg=self._query_float(f":SOUR{channel}:PHAS?"),
            frequency_mode=self.transport.query(f":SOUR{channel}:FREQ:MODE?"),
            sweep_enabled=self.transport.query(f":SOUR{channel}:SWE:STAT?"),
            apply_raw=self.transport.query(f":SOUR{channel}:APPL?"),
            square_duty_cycle_percent=self._query_float(f":SOUR{channel}:FUNC:SQU:DCYC?"),
        )

    def set_frequency(
        self, channel: int, value_hz: float, *, ensure_fix_mode: bool = True, check_errors: bool = True
    ) -> SourceStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        if value_hz <= 0:
            raise DataError("frequency must be > 0")
        if ensure_fix_mode:
            mode = self.transport.query(f":SOUR{channel}:FREQ:MODE?").strip().upper()
            if mode != "FIX":
                self.transport.write(f":SOUR{channel}:FREQ:MODE FIX")
        self.transport.write(f":SOUR{channel}:FREQ {value_hz:.12g}")
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status

    def set_output(self, channel: int, enabled: bool, *, check_errors: bool = True) -> SourceStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        self.transport.write(f":OUTP{channel} {'ON' if enabled else 'OFF'}")
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status


    def set_function(self, channel: int, function: str, *, check_errors: bool = True) -> SourceStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        normalized = function.strip().upper()
        aliases = {
            "SINE": "SIN",
            "SIN": "SIN",
            "SQUARE": "SQU",
            "SQU": "SQU",
            "RAMP": "RAMP",
            "PULSE": "PULS",
            "PULS": "PULS",
            "NOISE": "NOIS",
            "NOIS": "NOIS",
            "DC": "DC",
        }
        if normalized not in aliases:
            raise DataError("function must be one of: sin, squ, ramp, puls, nois, dc")
        self.transport.write(f":SOUR{channel}:FUNC {aliases[normalized]}")
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status

    def set_amplitude_vpp(self, channel: int, value_vpp: float, *, check_errors: bool = True) -> SourceStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        if value_vpp <= 0:
            raise DataError("amplitude must be > 0")
        self.transport.write(f":SOUR{channel}:VOLT:UNIT VPP")
        self.transport.write(f":SOUR{channel}:VOLT {value_vpp:.12g}")
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status


    def set_square_duty_cycle(self, channel: int, duty_percent: float, *, check_errors: bool = True) -> SourceStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        if duty_percent <= 0 or duty_percent >= 100:
            raise DataError("duty cycle percent must be > 0 and < 100")
        self.transport.write(f":SOUR{channel}:FUNC:SQU:DCYC {duty_percent:.12g}")
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status

    def close(self) -> None:
        self.transport.close()
