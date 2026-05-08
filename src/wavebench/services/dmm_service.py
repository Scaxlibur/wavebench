from __future__ import annotations

from dataclasses import dataclass
import time

from wavebench.config import ConnectionConfig, DmmConfig, WaveBenchConfig
from wavebench.drivers.dm3000 import DM3000Dmm, DmmReading
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.transport.pyvisa_transport import PyVisaTransport
from wavebench.transport.serial_transport import SerialTransport


@dataclass
class DmmService:
    config: WaveBenchConfig
    logger: CommandLogger

    def _dmm_config(self) -> DmmConfig:
        if self.config.dmm is None or not self.config.dmm.resource:
            raise ConfigError("dmm resource is not configured. Set [dmm].resource or pass --resource.")
        return self.config.dmm

    def _open_dmm(self) -> DM3000Dmm:
        dmm = self._dmm_config()
        backend = dmm.backend.strip().lower()
        if backend == "serial":
            transport = SerialTransport.open(dmm, logger=self.logger)
        elif backend in {"lan", "visa", "pyvisa"}:
            transport = PyVisaTransport.open(
                ConnectionConfig(
                    backend="lan",
                    resource=dmm.resource or "",
                    timeout_ms=dmm.timeout_ms,
                    opc_timeout_ms=dmm.timeout_ms,
                    read_retry_attempts=self.config.connection.read_retry_attempts,
                    read_retry_delay_ms=self.config.connection.read_retry_delay_ms,
                ),
                logger=self.logger,
            )
        else:
            raise ConfigError("dmm.backend must be one of: serial, lan, visa, pyvisa")
        return DM3000Dmm(transport=transport)

    def open_session(self) -> DM3000Dmm:
        return self._open_dmm()

    def idn(self) -> str:
        dmm = self._open_dmm()
        try:
            return dmm.idn()
        finally:
            dmm.close()

    def function_status(self) -> str:
        dmm = self._open_dmm()
        try:
            return dmm.function_status()
        finally:
            dmm.close()

    def set_function(self, function: str) -> str:
        dmm = self._open_dmm()
        try:
            return dmm.set_function(function=function)
        finally:
            dmm.close()

    def read(self, function: str = "dcv") -> DmmReading:
        dmm = self._open_dmm()
        try:
            settle_s = self._dmm_config().settle_ms_before_read / 1000.0
            if settle_s > 0:
                time.sleep(settle_s)
            return dmm.read(function=function)
        finally:
            dmm.close()
