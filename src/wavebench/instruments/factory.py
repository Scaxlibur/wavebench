from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, cast

from wavebench.config import ConnectionConfig, DmmConfig
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.plugins.api import PluginKind
from wavebench.transport.base import InstrumentTransport
from wavebench.transport.pyvisa_transport import PyVisaTransport
from wavebench.transport.rsinstrument_transport import RsInstrumentTransport
from wavebench.transport.serial_transport import SerialTransport

from .api import DriverContext, InstrumentDescriptor
from .capabilities import validate_declared_capabilities
from .contracts import InstrumentDriver
from .registry import resolve_instrument_descriptor


@dataclass(frozen=True)
class OpenedInstrument:
    descriptor: InstrumentDescriptor
    driver: InstrumentDriver


def open_instrument_driver(
    *,
    driver_reference: str,
    expected_kind: PluginKind,
    resource: str,
    configured_backend: str,
    timeout_ms: int,
    opc_timeout_ms: int,
    read_retry_attempts: int,
    read_retry_delay_ms: int,
    logger: CommandLogger,
    settings: Mapping[str, object] | None = None,
    options: Mapping[str, object] | None = None,
    serial_config: DmmConfig | None = None,
) -> OpenedInstrument:
    descriptor = resolve_instrument_descriptor(
        driver_reference,
        expected_kind=expected_kind,
    )
    backend = _select_backend(configured_backend, descriptor.backends)
    try:
        validated_options = descriptor.validate_options(options or {})
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"invalid options for instrument driver {descriptor.driver_id!r}: {exc}") from exc

    opened_transports: list[InstrumentTransport] = []

    def open_transport() -> InstrumentTransport:
        if opened_transports:
            raise ConfigError(
                f"instrument driver {descriptor.driver_id!r} requested more than one transport; "
                "instrument API v2 factories may open exactly one configured transport"
            )
        transport = _open_transport(
            backend=backend,
            resource=resource,
            timeout_ms=timeout_ms,
            opc_timeout_ms=opc_timeout_ms,
            read_retry_attempts=read_retry_attempts,
            read_retry_delay_ms=read_retry_delay_ms,
            logger=logger,
            serial_config=serial_config,
        )
        opened_transports.append(transport)
        return transport

    context = DriverContext(
        driver_id=descriptor.driver_id,
        kind=descriptor.kind,
        resource=resource,
        backend=backend,
        timeout_ms=timeout_ms,
        opc_timeout_ms=opc_timeout_ms,
        logger=logger,
        _transport_factory=open_transport,
        settings=settings or {},
        options=validated_options,
    )
    try:
        driver = descriptor.factory(context)
        validate_declared_capabilities(descriptor, driver)
    except Exception as exc:
        _close_factory_failure(driver if "driver" in locals() else None, opened_transports)
        if isinstance(exc, ConfigError):
            raise
        raise ConfigError(
            f"failed to create {expected_kind} instrument driver {descriptor.driver_id!r}: {exc}"
        ) from exc
    return OpenedInstrument(descriptor=descriptor, driver=cast(InstrumentDriver, driver))


def _select_backend(configured_backend: str, supported: tuple[str, ...]) -> str:
    aliases = {"lan": "pyvisa", "visa": "pyvisa", "pyvisa": "pyvisa"}
    normalized = aliases.get(configured_backend.strip().lower(), configured_backend.strip().lower())
    if normalized in supported:
        return normalized
    if len(supported) == 1:
        return supported[0]
    raise ConfigError(
        f"configured backend {configured_backend!r} is not supported; "
        f"driver supports: {', '.join(supported)}"
    )


def _open_transport(
    *,
    backend: str,
    resource: str,
    timeout_ms: int,
    opc_timeout_ms: int,
    read_retry_attempts: int,
    read_retry_delay_ms: int,
    logger: CommandLogger,
    serial_config: DmmConfig | None,
) -> InstrumentTransport:
    if backend == "serial":
        if serial_config is None:
            raise ConfigError("serial instrument driver requires serial configuration")
        return SerialTransport.open(serial_config, logger=logger)
    connection = ConnectionConfig(
        backend="lan",
        resource=resource,
        timeout_ms=timeout_ms,
        opc_timeout_ms=opc_timeout_ms,
        read_retry_attempts=read_retry_attempts,
        read_retry_delay_ms=read_retry_delay_ms,
    )
    if backend == "pyvisa":
        return PyVisaTransport.open(connection, logger=logger)
    if backend == "rsinstrument":
        return RsInstrumentTransport.open(connection, logger=logger)
    raise ConfigError(f"unsupported instrument transport backend: {backend}")


def _close_factory_failure(
    driver: object | None,
    opened_transports: list[InstrumentTransport],
) -> None:
    if driver is not None and callable(getattr(driver, "close", None)):
        try:
            driver.close()
            return
        except Exception:
            pass
    for transport in reversed(opened_transports):
        try:
            transport.close()
        except Exception:
            pass
