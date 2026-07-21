from __future__ import annotations

from types import MappingProxyType
from typing import Final, Mapping


BUILTIN_MIGRATION_DISTRIBUTIONS: Final[Mapping[str, str]] = MappingProxyType(
    {
        "rigol.dg4202": "wavebench-rigol-dg4000",
    }
)
