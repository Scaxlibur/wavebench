from __future__ import annotations

from dataclasses import dataclass

from wavebench.drivers.dg4202 import SourceStatus
from wavebench.errors import DataError


@dataclass(frozen=True)
class RestorableSourceState:
    channel: int
    output: str
    function: str
    frequency_hz: float
    amplitude_vpp: float
    amplitude_unit: str
    square_duty_cycle_percent: float | None = None

    @classmethod
    def from_status(cls, status: SourceStatus) -> "RestorableSourceState":
        if status.frequency_hz is None:
            raise DataError("cannot snapshot source state: frequency_hz is missing")
        if status.amplitude is None:
            raise DataError("cannot snapshot source state: amplitude is missing")
        if not status.amplitude_unit:
            raise DataError("cannot snapshot source state: amplitude_unit is missing")
        if status.amplitude_unit.strip().upper() != "VPP":
            raise DataError("cannot snapshot source state: only VPP amplitude is restorable for now")
        return cls(
            channel=status.channel,
            output=status.output.strip().upper(),
            function=status.function.strip().upper(),
            frequency_hz=status.frequency_hz,
            amplitude_vpp=status.amplitude,
            amplitude_unit=status.amplitude_unit.strip().upper(),
            square_duty_cycle_percent=status.square_duty_cycle_percent,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "channel": self.channel,
            "output": self.output,
            "function": self.function,
            "frequency_hz": self.frequency_hz,
            "amplitude_vpp": self.amplitude_vpp,
            "amplitude_unit": self.amplitude_unit,
            "square_duty_cycle_percent": self.square_duty_cycle_percent,
        }
