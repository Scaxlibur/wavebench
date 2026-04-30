from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from wavebench.config import ConnectionConfig
from wavebench.errors import ConnectionError
from wavebench.logging import CommandLogger

@dataclass
class RsInstrumentTransport:
    resource: str
    session: Any
    logger: CommandLogger

    @classmethod
    def open(cls, config: ConnectionConfig, logger: CommandLogger | None = None) -> "RsInstrumentTransport":
        try:
            from RsInstrument import RsInstrument
        except ImportError as exc:
            raise ConnectionError("RsInstrument is not installed. Run: python -m pip install -e .") from exc
        logger = logger or CommandLogger()
        try:
            session = RsInstrument(config.resource, True, False)
            session.visa_timeout = config.timeout_ms
            session.opc_timeout = config.opc_timeout_ms
            session.instrument_status_checking = False
        except Exception as exc:
            raise ConnectionError(f"failed to open instrument {config.resource}: {exc}") from exc
        return cls(resource=config.resource, session=session, logger=logger)

    def write(self, command: str) -> None:
        self.logger.record("write", command)
        self.session.write_str(command)

    def query(self, command: str) -> str:
        self.logger.record("query", command)
        response = self.session.query_str(command).strip()
        self.logger.record("response", response)
        return response

    def query_float_list(self, command: str) -> list[float]:
        self.logger.record("query", command)
        values = list(self.session.query_bin_or_ascii_float_list(command))
        self.logger.record("response", f"<float_list len={len(values)}>")
        return values

    def query_bin_block(self, command: str) -> bytes:
        self.logger.record("query_binary", command)
        data = bytes(self.session.query_bin_block(command))
        self.logger.record("response", f"<bin_block len={len(data)}>")
        return data

    def query_opc(self) -> str:
        self.logger.record("query", "*OPC?")
        response = str(self.session.query_opc()).strip()
        self.logger.record("response", response)
        return response

    def close(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass
