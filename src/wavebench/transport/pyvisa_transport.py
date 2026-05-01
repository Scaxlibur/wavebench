from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wavebench.config import ConnectionConfig
from wavebench.errors import ConnectionError
from wavebench.logging import CommandLogger


@dataclass
class PyVisaTransport:
    resource: str
    resource_manager: Any
    session: Any
    logger: CommandLogger

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
        return cls(resource=config.resource, resource_manager=resource_manager, session=session, logger=logger)

    def write(self, command: str) -> None:
        self.logger.record("write", command)
        self.session.write(command)

    def write_bytes(self, command: bytes) -> None:
        self.logger.record("write_binary", f"<bytes len={len(command)}>")
        if hasattr(self.session, "write_raw"):
            self.session.write_raw(command)
        else:
            raise ConnectionError("pyvisa session does not support raw byte writes")

    def query(self, command: str) -> str:
        self.logger.record("query", command)
        response = str(self.session.query(command)).strip()
        self.logger.record("response", response)
        return response

    def close(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass
        try:
            self.resource_manager.close()
        except Exception:
            pass
