from __future__ import annotations

from dataclasses import dataclass
import time

from wavebench.errors import DataError, InstrumentError


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


def parse_apply_response(response: str) -> tuple[str | None, float | None, float | None]:
    parts = [part.strip() for part in response.strip().split(",")]
    if len(parts) != 3:
        raise DataError(f"unexpected DP800 APPL? response: {response!r}")
    rating = None
    if ":" in parts[0]:
        _, rating = parts[0].split(":", 1)
        rating = rating.strip() or None
    return rating, float(parts[1]), float(parts[2])


def parse_measure_all_response(response: str) -> tuple[float | None, float | None, float | None]:
    parts = [part.strip() for part in response.strip().split(",")]
    if len(parts) != 3:
        raise DataError(f"unexpected DP800 MEAS:ALL? response: {response!r}")
    return float(parts[0]), float(parts[1]), float(parts[2])


@dataclass
class DP800Power:
    transport: object
    check_errors_after_ops: bool = True

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

    def get_status(self, channel: int) -> PowerStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        rating, set_voltage_v, set_current_a = parse_apply_response(self.transport.query(f":APPL? CH{channel}"))
        measured_voltage_v, measured_current_a, measured_power_w = parse_measure_all_response(
            self.transport.query(f":MEAS:ALL? CH{channel}")
        )
        return PowerStatus(
            channel=channel,
            output=self.transport.query(f":OUTP? CH{channel}").strip().upper(),
            mode=self.transport.query(f":OUTP:MODE? CH{channel}").strip().upper(),
            rating=rating,
            set_voltage_v=set_voltage_v,
            set_current_a=set_current_a,
            measured_voltage_v=measured_voltage_v,
            measured_current_a=measured_current_a,
            measured_power_w=measured_power_w,
        )

    def set_voltage_current_limit(
        self,
        channel: int,
        voltage_v: float,
        current_limit_a: float,
        *,
        check_errors: bool = True,
        settle_ms_after_set: int = 0,
    ) -> PowerStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        if voltage_v < 0:
            raise DataError("voltage must be >= 0")
        if current_limit_a <= 0:
            raise DataError("current limit must be > 0")
        self.transport.write(f":APPL CH{channel},{voltage_v:.12g},{current_limit_a:.12g}")
        if settle_ms_after_set:
            time.sleep(settle_ms_after_set / 1000.0)
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status

    def set_output(
        self,
        channel: int,
        enabled: bool,
        *,
        check_errors: bool = True,
        settle_ms_after_output: int = 0,
    ) -> PowerStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        self.transport.write(f":OUTP CH{channel},{'ON' if enabled else 'OFF'}")
        if settle_ms_after_output:
            time.sleep(settle_ms_after_output / 1000.0)
        status = self.get_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status

    def close(self) -> None:
        self.transport.close()
