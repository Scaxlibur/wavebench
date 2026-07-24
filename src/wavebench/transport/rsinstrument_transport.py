from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import time
from typing import Any

from wavebench.config import ConnectionConfig
from wavebench.errors import ConnectionError, InstrumentError
from wavebench.logging import CommandLogger


def _open_rsinstrument_session(
    rs_instrument_cls: Any,
    resource: str,
    *,
    select_visa: str | None = None,
) -> Any:
    if select_visa is not None:
        options = f"SelectVisa={select_visa}"
        if select_visa == "socketio":
            options += ",AddTermCharToWriteBinBlock=True,DataChunkSize=512"
        return rs_instrument_cls(
            resource,
            True,
            False,
            options,
        )
    try:
        return rs_instrument_cls(resource, True, False)
    except Exception as exc:
        message = str(exc).lower()
        if "rsvisa" not in message and "visa implementation" not in message:
            raise
        return rs_instrument_cls(resource, True, False, "SelectVisa=pyvisa-py")


@dataclass
class RsInstrumentTransport:
    resource: str
    session: Any
    logger: CommandLogger
    select_visa: str | None = None

    @classmethod
    def open(
        cls,
        config: ConnectionConfig,
        logger: CommandLogger | None = None,
        *,
        select_visa: str | None = None,
    ) -> "RsInstrumentTransport":
        try:
            from RsInstrument import RsInstrument
        except ImportError as exc:
            raise ConnectionError("RsInstrument is not installed. Run: python -m pip install -e .") from exc
        logger = logger or CommandLogger()
        try:
            session = _open_rsinstrument_session(
                RsInstrument,
                config.resource,
                select_visa=select_visa,
            )
            session.visa_timeout = config.timeout_ms
            session.opc_timeout = config.opc_timeout_ms
            session.instrument_status_checking = False
        except Exception as exc:
            raise ConnectionError(f"failed to open instrument {config.resource}: {exc}") from exc
        return cls(
            resource=config.resource,
            session=session,
            logger=logger,
            select_visa=select_visa,
        )

    def record_event(self, direction: str, text: str) -> None:
        self.logger.record(direction, text)

    def write(self, command: str) -> None:
        self.logger.record("write", command)
        self.session.write_str(command)

    def query(self, command: str) -> str:
        self.logger.record("query", command)
        response = self.session.query_str(command).strip()
        self.logger.record("response", response)
        return response

    def query_float_list(
        self,
        command: str,
        *,
        timeout_ms: int | None = None,
    ) -> list[float]:
        self.logger.record("query", command)
        started = time.perf_counter()
        try:
            with self._temporary_timeout(timeout_ms), self._read_progress(
                "query_float_list"
            ) as progress:
                values = list(self.session.query_bin_or_ascii_float_list(command))
        except Exception as exc:
            self._record_query_telemetry(
                operation="query_float_list",
                started=started,
                status="failed",
                progress=progress if "progress" in locals() else None,
            )
            raise self._nonreplayable_query_error(
                "query_float_list",
                command,
                exc,
            ) from exc
        self.logger.record("response", f"<float_list len={len(values)}>")
        self._record_query_telemetry(
            operation="query_float_list",
            started=started,
            status="ok",
            progress=progress,
            items=len(values),
        )
        return values

    def query_bin_block(self, command: str) -> bytes:
        self.logger.record("query_binary", command)
        started = time.perf_counter()
        try:
            with self._read_progress("query_binary") as progress:
                data = bytes(self.session.query_bin_block(command))
        except Exception as exc:
            self._record_query_telemetry(
                operation="query_binary",
                started=started,
                status="failed",
                progress=progress if "progress" in locals() else None,
            )
            raise self._nonreplayable_query_error(
                "query_binary",
                command,
                exc,
            ) from exc
        self.logger.record("response", f"<bin_block len={len(data)}>")
        self._record_query_telemetry(
            operation="query_binary",
            started=started,
            status="ok",
            progress=progress,
            bytes_count=len(data),
        )
        return data

    @contextmanager
    def _temporary_timeout(self, timeout_ms: int | None):
        if timeout_ms is None:
            yield
            return
        if timeout_ms < 1:
            raise ValueError("timeout_ms must be >= 1")
        original_timeout = self.session.visa_timeout
        self.session.visa_timeout = timeout_ms
        try:
            yield
        finally:
            self.session.visa_timeout = original_timeout

    @contextmanager
    def _read_progress(self, operation: str):
        progress = {"transferred": 0, "total": None, "chunks": 0}
        events = getattr(self.session, "events", None)
        if events is None or not hasattr(events, "on_read_handler"):
            yield progress
            return
        previous_handler = events.on_read_handler
        previous_include_data = events.io_events_include_data

        def on_read(args: Any) -> None:
            transferred = int(getattr(args, "transferred_size", 0) or 0)
            total = getattr(args, "total_size", None)
            chunk_ix = int(getattr(args, "chunk_ix", 0) or 0)
            progress["transferred"] = max(progress["transferred"], transferred)
            progress["total"] = int(total) if total is not None else progress["total"]
            progress["chunks"] = max(progress["chunks"], chunk_ix + 1)
            fields = [
                f"operation={operation}_progress",
                f"chunk={chunk_ix + 1}",
                f"transferred_bytes={transferred}",
            ]
            if total is not None:
                fields.append(f"total_bytes={int(total)}")
            if bool(getattr(args, "end_of_transfer", False)):
                fields.append("end=true")
            self.logger.record("telemetry", " ".join(fields))
            if previous_handler is not None:
                previous_handler(args)

        events.io_events_include_data = False
        events.on_read_handler = on_read
        try:
            yield progress
        finally:
            events.on_read_handler = previous_handler
            events.io_events_include_data = previous_include_data

    def _record_query_telemetry(
        self,
        *,
        operation: str,
        started: float,
        status: str,
        progress: dict[str, int | None] | None,
        bytes_count: int | None = None,
        items: int | None = None,
    ) -> None:
        elapsed_s = max(time.perf_counter() - started, 0.0)
        transferred = int(progress["transferred"] or 0) if progress else 0
        measured_bytes = bytes_count if bytes_count is not None else transferred or None
        fields = [
            f"operation={operation}",
            f"status={status}",
            f"elapsed_ms={elapsed_s * 1000.0:.3f}",
            "replay=disabled",
        ]
        if measured_bytes is not None:
            fields.append(f"bytes={measured_bytes}")
            throughput = (
                measured_bytes / elapsed_s / (1024.0 * 1024.0)
                if elapsed_s > 0
                else 0.0
            )
            fields.append(f"throughput_mib_s={throughput:.3f}")
        if items is not None:
            fields.append(f"items={items}")
        if progress and progress["chunks"]:
            fields.append(f"chunks={progress['chunks']}")
        self.logger.record("telemetry", " ".join(fields))

    def _nonreplayable_query_error(
        self,
        operation: str,
        command: str,
        exc: Exception,
    ) -> InstrumentError:
        return InstrumentError(
            f"RsInstrument {operation} failed for command {command!r}: "
            f"{type(exc).__name__}: {exc}. The response state may be partial; reopen the "
            "instrument session and restart the complete acquisition before retrying."
        )

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
