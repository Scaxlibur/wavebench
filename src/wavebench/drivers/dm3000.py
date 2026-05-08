from __future__ import annotations

from dataclasses import dataclass

from wavebench.errors import DataError


DMM_FUNCTION_ALIASES = {
    "vdc": "dcv",
    "vac": "acv",
    "idc": "dci",
    "iac": "aci",
    "ohm": "res",
    "r": "res",
    "2wr": "res",
    "4wr": "fres",
    "cont": "continuity",
}

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

DMM_FUNCTION_SET_COMMANDS = {
    "dcv": ":FUNCtion:VOLTage:DC",
    "acv": ":FUNCtion:VOLTage:AC",
    "dci": ":FUNCtion:CURRent:DC",
    "aci": ":FUNCtion:CURRent:AC",
    "res": ":FUNCtion:RESistance",
    "fres": ":FUNCtion:FRESistance",
    "freq": ":FUNCtion:FREQuency",
    "period": ":FUNCtion:PERiod",
    "continuity": ":FUNCtion:CONTinuity",
    "diode": ":FUNCtion:DIODe",
    "cap": ":FUNCtion:CAPacitance",
}

DMM_FUNCTION_QUERY_MAP = {
    "DCV": "dcv",
    "ACV": "acv",
    "DCI": "dci",
    "ACI": "aci",
    "RESISTANCE": "res",
    "2WR": "res",
    "FRESISTANCE": "fres",
    "4WR": "fres",
    "FREQUENCY": "freq",
    "FREQ": "freq",
    "PERIOD": "period",
    "CONTINUITY": "continuity",
    "CONT": "continuity",
    "DIODE": "diode",
    "CAPACITANCE": "cap",
    "CAP": "cap",
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

    def function_status(self) -> str:
        raw = self.transport.query(":FUNCtion?").strip().strip('"')
        normalized = DMM_FUNCTION_QUERY_MAP.get(raw.upper())
        if normalized is None:
            supported = ", ".join(sorted(DMM_FUNCTION_QUERY_MAP))
            raise DataError(
                f"unexpected DMM function status {raw!r}; expected one of: {supported}"
            )
        return normalized

    def set_function(self, function: str) -> str:
        key = normalize_dmm_function(function)
        if key not in DMM_FUNCTION_SET_COMMANDS:
            supported = ", ".join(sorted(DMM_FUNCTION_SET_COMMANDS))
            raise DataError(f"unsupported DMM function {function!r}; supported: {supported}")
        self.transport.write(DMM_FUNCTION_SET_COMMANDS[key])
        return self.function_status()

    def read(self, function: str = "dcv") -> DmmReading:
        key = normalize_dmm_function(function)
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


def normalize_dmm_function(function: str) -> str:
    key = function.strip().lower()
    return DMM_FUNCTION_ALIASES.get(key, key)
