from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wavebench.config import DmmConfig
from wavebench.errors import ConfigError, ConnectionError, InstrumentError
from wavebench.logging import CommandLogger


_PARITY_ALIASES = {
    "N": "N",
    "NONE": "N",
    "O": "O",
    "ODD": "O",
    "E": "E",
    "EVEN": "E",
}

_TERMINATIONS = {
    "LF": b"\n",
    "CRLF": b"\r\n",
}


@dataclass
class SerialTransport:
    resource: str
    session: Any
    logger: CommandLogger
    write_termination: bytes = b"\n"
    read_termination: bytes = b"\n"

    @classmethod
    def open(cls, config: DmmConfig, logger: CommandLogger | None = None) -> "SerialTransport":
        try:
            write_termination = _TERMINATIONS[config.write_termination.strip().upper()]
            read_termination = _TERMINATIONS[config.read_termination.strip().upper()]
        except (AttributeError, KeyError) as exc:
            raise ConfigError("serial terminations must be lf or crlf") from exc
        try:
            import serial
        except ImportError as exc:
            raise ConnectionError("pyserial is not installed. Run: python -m pip install pyserial") from exc
        if not config.resource:
            raise ConnectionError("serial resource is not configured")
        logger = logger or CommandLogger()
        try:
            session = serial.Serial(
                port=config.resource,
                baudrate=config.baudrate,
                bytesize=config.bytesize,
                parity=_PARITY_ALIASES[config.parity.upper()],
                stopbits=config.stopbits,
                timeout=config.timeout_ms / 1000.0,
                write_timeout=config.timeout_ms / 1000.0,
                xonxoff=config.xonxoff,
                rtscts=config.rtscts,
                dsrdtr=config.dsrdtr,
            )
        except Exception as exc:
            raise ConnectionError(f"failed to open serial instrument {config.resource}: {exc}") from exc
        return cls(
            resource=config.resource,
            session=session,
            logger=logger,
            write_termination=write_termination,
            read_termination=read_termination,
        )

    def record_event(self, direction: str, text: str) -> None:
        self.logger.record(direction, text)

    def write(self, command: str) -> None:
        self.logger.record("write", command)
        try:
            payload = command.rstrip("\r\n").encode("ascii") + self.write_termination
            written = self.session.write(payload)
            if written is not None and written != len(payload):
                raise OSError(f"short serial write: wrote {written} of {len(payload)} bytes")
            if hasattr(self.session, "flush"):
                self.session.flush()
        except Exception as exc:
            raise self._instrument_io_error("write", command, exc) from exc

    def write_bytes(self, command: bytes) -> None:
        self.logger.record("write_binary", f"<bytes len={len(command)}>")
        try:
            self.session.write(command)
            if hasattr(self.session, "flush"):
                self.session.flush()
        except Exception as exc:
            raise self._instrument_io_error("write_binary", "<bytes>", exc) from exc

    def query(self, command: str) -> str:
        self.logger.record("query", command)
        try:
            self.write(command)
            if hasattr(self.session, "read_until"):
                raw = self.session.read_until(self.read_termination)
            else:
                raw = self.session.readline()
            if not raw:
                raise TimeoutError(f"timed out waiting for {self.read_termination!r}")
            if not raw.endswith(self.read_termination):
                raise TimeoutError(
                    f"serial response ended before {self.read_termination!r}; received {len(raw)} bytes"
                )
            response_bytes = raw[: -len(self.read_termination)]
            if self.read_termination == b"\n" and response_bytes.endswith(b"\r"):
                response_bytes = response_bytes[:-1]
            response = response_bytes.decode("ascii")
        except Exception as exc:
            raise self._instrument_io_error("query", command, exc) from exc
        self.logger.record("response", response)
        return response

    def query_float_list(self, command: str) -> list[float]:
        response = self.query(command)
        return [float(item) for item in response.replace(";", ",").split(",") if item.strip()]

    def query_bin_block(self, command: str) -> bytes:
        raise ConnectionError("serial transport does not support binary block queries yet")

    def query_opc(self) -> str:
        return self.query("*OPC?")

    def _instrument_io_error(self, operation: str, command: str, exc: Exception) -> InstrumentError:
        return InstrumentError(
            f"serial {operation} failed on {self.resource} command {command!r}: "
            f"{type(exc).__name__}: {exc}"
        )

    def close(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass
