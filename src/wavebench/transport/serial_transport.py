from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wavebench.config import DmmConfig
from wavebench.errors import ConnectionError, InstrumentError
from wavebench.logging import CommandLogger


_PARITY_ALIASES = {
    "N": "N",
    "NONE": "N",
    "O": "O",
    "ODD": "O",
    "E": "E",
    "EVEN": "E",
}


@dataclass
class SerialTransport:
    resource: str
    session: Any
    logger: CommandLogger

    @classmethod
    def open(cls, config: DmmConfig, logger: CommandLogger | None = None) -> "SerialTransport":
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
            )
        except Exception as exc:
            raise ConnectionError(f"failed to open serial instrument {config.resource}: {exc}") from exc
        return cls(resource=config.resource, session=session, logger=logger)

    def record_event(self, direction: str, text: str) -> None:
        self.logger.record(direction, text)

    def write(self, command: str) -> None:
        self.logger.record("write", command)
        try:
            payload = command.encode("ascii")
            if not payload.endswith(b"\n"):
                payload += b"\n"
            self.session.write(payload)
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
            response = self.session.readline().decode("ascii", errors="replace").strip()
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
