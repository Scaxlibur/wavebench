from __future__ import annotations

from dataclasses import dataclass

from wavebench.errors import DataError


DMM_FUNCTION_COMMANDS = {
    "dcv": ":MEASure:VOLTage:DC?",
    "acv": ":MEASure:VOLTage:AC?",
    "dci": ":MEASure:CURRent:DC?",
    "aci": ":MEASure:CURRent:AC?",
    "res": ":MEASure:RESistance?",
    "fres": ":MEASure:FRESistance?",
    "freq": ":MEASure:FREQuency?",
    "period": ":MEASure:PERiod?",
    "continuity": ":MEASure:CONTinuity?",
    "diode": ":MEASure:DIODe?",
    "cap": ":MEASure:CAPacitance?",
}

DMM_FUNCTION_UNITS = {
    "dcv": "V",
    "acv": "V",
    "dci": "A",
    "aci": "A",
    "res": "ohm",
    "fres": "ohm",
    "freq": "Hz",
    "period": "s",
    "continuity": "ohm",
    "diode": "V",
    "cap": "F",
}


@dataclass(frozen=True)
class DmmReading:
    function: str
    value: float
    unit: str
    raw: str

    def as_dict(self) -> dict[str, object]:
        return {"function": self.function, "value": self.value, "unit": self.unit, "raw": self.raw}


@dataclass
class DM3000Dmm:
    transport: object

    def idn(self) -> str:
        return self.transport.query("*IDN?")

    def read(self, function: str = "dcv") -> DmmReading:
        key = function.strip().lower()
        aliases = {"vdc": "dcv", "vac": "acv", "idc": "dci", "iac": "aci", "ohm": "res", "r": "res"}
        key = aliases.get(key, key)
        if key not in DMM_FUNCTION_COMMANDS:
            supported = ", ".join(sorted(DMM_FUNCTION_COMMANDS))
            raise DataError(f"unsupported DMM function {function!r}; supported: {supported}")
        raw = self.transport.query(DMM_FUNCTION_COMMANDS[key])
        try:
            value = float(raw)
        except ValueError as exc:
            raise DataError(f"unexpected DM3000 reading for {key}: {raw!r}") from exc
        return DmmReading(function=key, value=value, unit=DMM_FUNCTION_UNITS[key], raw=raw)

    def close(self) -> None:
        self.transport.close()
