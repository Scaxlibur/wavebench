from __future__ import annotations

from dataclasses import dataclass

from wavebench.config import WaveBenchConfig
from wavebench.drivers.rtm2032 import RTM2032Scope
from wavebench.logging import CommandLogger
from wavebench.transport.rsinstrument_transport import RsInstrumentTransport

@dataclass
class ScopeService:
    config: WaveBenchConfig
    logger: CommandLogger

    def _open_scope(self) -> RTM2032Scope:
        transport = RsInstrumentTransport.open(self.config.connection, logger=self.logger)
        return RTM2032Scope(transport=transport, check_errors_after_ops=self.config.scope.check_errors)

    def idn(self) -> str:
        scope = self._open_scope()
        try:
            return scope.idn()
        finally:
            scope.close()

    def errors(self) -> list[str]:
        scope = self._open_scope()
        try:
            return scope.errors()
        finally:
            scope.close()

    def autoscale(self) -> None:
        scope = self._open_scope()
        try:
            scope.autoscale(
                wait_opc=self.config.autoscale.wait_opc,
                check_errors=self.config.autoscale.check_errors,
            )
        finally:
            scope.close()
