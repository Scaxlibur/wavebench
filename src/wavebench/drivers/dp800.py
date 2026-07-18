from __future__ import annotations

from dataclasses import dataclass
import time

from wavebench.errors import DataError, InstrumentError
from wavebench.instruments.models import PowerMeasurement, PowerProtectionStatus, PowerStatus


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


def parse_protection_value_response(response: str) -> float | None:
    return float(response.strip())


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
        measurement = self.get_measurement(channel)
        return PowerStatus(
            channel=channel,
            output=self.transport.query(f":OUTP? CH{channel}").strip().upper(),
            mode=self.transport.query(f":OUTP:MODE? CH{channel}").strip().upper(),
            rating=rating,
            set_voltage_v=set_voltage_v,
            set_current_a=set_current_a,
            measured_voltage_v=measurement.measured_voltage_v,
            measured_current_a=measurement.measured_current_a,
            measured_power_w=measurement.measured_power_w,
        )

    def get_measurement(self, channel: int) -> PowerMeasurement:
        if channel < 1:
            raise DataError("channel must be >= 1")
        measured_voltage_v, measured_current_a, measured_power_w = parse_measure_all_response(
            self.transport.query(f":MEAS:ALL? CH{channel}")
        )
        return PowerMeasurement(
            channel=channel,
            measured_voltage_v=measured_voltage_v,
            measured_current_a=measured_current_a,
            measured_power_w=measured_power_w,
        )

    def get_protection_status(self, channel: int) -> PowerProtectionStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        return PowerProtectionStatus(
            channel=channel,
            ovp_enabled=self.transport.query(f":OUTP:OVP? CH{channel}").strip().upper(),
            ovp_threshold_v=parse_protection_value_response(self.transport.query(f":OUTP:OVP:VAL? CH{channel}")),
            ovp_tripped=self.transport.query(f":OUTP:OVP:QUES? CH{channel}").strip().upper(),
            ocp_enabled=self.transport.query(f":OUTP:OCP? CH{channel}").strip().upper(),
            ocp_threshold_a=parse_protection_value_response(self.transport.query(f":OUTP:OCP:VAL? CH{channel}")),
            ocp_tripped=self.transport.query(f":OUTP:OCP:QUES? CH{channel}").strip().upper(),
        )

    def set_protection(
        self,
        channel: int,
        *,
        ovp_threshold_v: float | None = None,
        ovp_enabled: bool | None = None,
        ocp_threshold_a: float | None = None,
        ocp_enabled: bool | None = None,
        check_errors: bool = True,
    ) -> PowerProtectionStatus:
        if channel < 1:
            raise DataError("channel must be >= 1")
        if ovp_threshold_v is not None and ovp_threshold_v < 0:
            raise DataError("OVP threshold must be >= 0")
        if ocp_threshold_a is not None and ocp_threshold_a <= 0:
            raise DataError("OCP threshold must be > 0")
        if ovp_threshold_v is not None:
            self.transport.write(f":OUTP:OVP:VAL CH{channel},{ovp_threshold_v:.12g}")
        if ovp_enabled is not None:
            self.transport.write(f":OUTP:OVP CH{channel},{'ON' if ovp_enabled else 'OFF'}")
        if ocp_threshold_a is not None:
            self.transport.write(f":OUTP:OCP:VAL CH{channel},{ocp_threshold_a:.12g}")
        if ocp_enabled is not None:
            self.transport.write(f":OUTP:OCP CH{channel},{'ON' if ocp_enabled else 'OFF'}")
        status = self.get_protection_status(channel)
        if check_errors:
            self.assert_no_errors()
        return status

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
