from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any

from wavebench.config import ConnectionConfig
from wavebench.errors import ConnectionError, InstrumentError
from wavebench.logging import CommandLogger


@dataclass
class PyVisaTransport:
    resource: str
    resource_manager: Any
    session: Any
    logger: CommandLogger
    read_retry_attempts: int = 1
    read_retry_delay_ms: int = 200

    @classmethod
    def open(cls, config: ConnectionConfig, logger: CommandLogger | None = None) -> "PyVisaTransport":
        try:
            import pyvisa
        except ImportError as exc:
            raise ConnectionError("pyvisa is not installed. Run: python -m pip install pyvisa") from exc
        logger = logger or CommandLogger()
        try:
            try:
                resource_manager = pyvisa.ResourceManager()
            except ValueError:
                resource_manager = pyvisa.ResourceManager("@py")
            session = resource_manager.open_resource(config.resource)
            session.timeout = config.timeout_ms
            try:
                session.read_termination = "\n"
            except Exception:
                pass
            try:
                session.write_termination = "\n"
            except Exception:
                pass
        except Exception as exc:
            raise ConnectionError(f"failed to open instrument {config.resource}: {exc}") from exc
        return cls(
            resource=config.resource,
            resource_manager=resource_manager,
            session=session,
            logger=logger,
            read_retry_attempts=config.read_retry_attempts,
            read_retry_delay_ms=config.read_retry_delay_ms,
        )

    def write(self, command: str) -> None:
        self.logger.record("write", command)
        try:
            self.session.write(command)
        except Exception as exc:
            raise self._instrument_io_error("write", command, exc) from exc

    def write_bytes(self, command: bytes) -> None:
        self.logger.record("write_binary", f"<bytes len={len(command)}>")
        if not hasattr(self.session, "write_raw"):
            raise ConnectionError("pyvisa session does not support raw byte writes")
        try:
            self.session.write_raw(command)
        except Exception as exc:
            raise self._instrument_io_error("write_binary", "<bytes>", exc) from exc

    def query(self, command: str) -> str:
        self.logger.record("query", command)
        try:
            response = str(self._read_with_retry("query", command, lambda: self.session.query(command))).strip()
            if response == "" and hasattr(self.session, "read"):
                for _ in range(2):
                    response = str(self.session.read()).strip()
                    if response:
                        break
        except Exception as exc:
            raise self._instrument_io_error("query", command, exc) from exc
        self.logger.record("response", response)
        return response

    def query_float_list(self, command: str) -> list[float]:
        self.logger.record("query", command)
        try:
            if hasattr(self.session, "query_binary_values"):
                try:
                    values = list(
                        self._read_with_retry(
                            "query",
                            command,
                            lambda: self.session.query_binary_values(command, datatype="f"),
                        )
                    )
                except Exception:
                    values = self._parse_ascii_float_list(
                        self._read_with_retry("query", command, lambda: self.session.query(command))
                    )
            else:
                values = self._parse_ascii_float_list(
                    self._read_with_retry("query", command, lambda: self.session.query(command))
                )
        except Exception as exc:
            raise self._instrument_io_error("query", command, exc) from exc
        self.logger.record("response", f"<float_list len={len(values)}>")
        return values

    @staticmethod
    def _parse_ascii_float_list(response: object) -> list[float]:
        return [
            float(item)
            for item in str(response).replace(";", ",").split(",")
            if item.strip()
        ]

    def query_bin_block(self, command: str) -> bytes:
        self.logger.record("query_binary", command)
        if not hasattr(self.session, "query_binary_values"):
            raise ConnectionError("pyvisa session does not support binary block queries")
        try:
            data = bytes(
                self._read_with_retry(
                    "query_binary",
                    command,
                    lambda: self.session.query_binary_values(command, datatype="B", container=bytes),
                )
            )
        except Exception as exc:
            raise self._instrument_io_error("query_binary", command, exc) from exc
        self.logger.record("response", f"<bin_block len={len(data)}>")
        return data

    def query_opc(self) -> str:
        self.logger.record("query", "*OPC?")
        try:
            response = str(self._read_with_retry("query", "*OPC?", lambda: self.session.query("*OPC?"))).strip()
        except Exception as exc:
            raise self._instrument_io_error("query", "*OPC?", exc) from exc
        self.logger.record("response", response)
        return response

    def _read_with_retry(self, operation: str, command: str, read_once: Any) -> Any:
        attempts = self.read_retry_attempts + 1
        last_exc: Exception | None = None
        for attempt in range(attempts):
            try:
                return read_once()
            except Exception as exc:
                last_exc = exc
                if attempt >= attempts - 1:
                    break
                if self.read_retry_delay_ms > 0:
                    time.sleep(self.read_retry_delay_ms / 1000.0)
                self.logger.record("retry", f"{operation} {command} attempt {attempt + 2}/{attempts}")
        assert last_exc is not None
        raise last_exc

    def _instrument_io_error(self, operation: str, command: str, exc: Exception) -> InstrumentError:
        return InstrumentError(
            f"pyvisa {operation} failed on {self.resource} command {command!r}: "
            f"{type(exc).__name__}: {exc}"
        )

    def close(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass
        try:
            self.resource_manager.close()
        except Exception:
            pass
