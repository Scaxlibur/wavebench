from __future__ import annotations

from dataclasses import dataclass

from wavebench.errors import InstrumentError
from wavebench.transport.base import InstrumentTransport

@dataclass
class RTM2032Scope:
    transport: InstrumentTransport
    check_errors_after_ops: bool = True

    def idn(self) -> str:
        return self.transport.query("*IDN?")

    def clear_status(self) -> None:
        self.transport.write("*CLS")

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

    def close(self) -> None:
        self.transport.close()
