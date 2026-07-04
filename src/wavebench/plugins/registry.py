from __future__ import annotations

from dataclasses import dataclass

from wavebench.errors import ConfigError

from .api import InstrumentPlugin, PluginKind
from .builtin import BUILTIN_PLUGINS


@dataclass(frozen=True)
class PluginRegistry:
    plugins: tuple[InstrumentPlugin, ...]

    def __post_init__(self) -> None:
        seen: set[str] = set()
        duplicates: list[str] = []
        for plugin in self.plugins:
            if plugin.driver_id in seen:
                duplicates.append(plugin.driver_id)
            seen.add(plugin.driver_id)
        if duplicates:
            joined = ", ".join(sorted(set(duplicates)))
            raise ConfigError(f"duplicate plugin driver_id: {joined}")

    def list_plugins(self, *, kind: PluginKind | None = None) -> list[InstrumentPlugin]:
        plugins = self.plugins
        if kind is not None:
            plugins = tuple(plugin for plugin in plugins if plugin.kind == kind)
        return sorted(plugins, key=lambda item: (item.kind, item.driver_id))

    def get(self, driver_id: str) -> InstrumentPlugin:
        normalized = driver_id.strip()
        for plugin in self.plugins:
            if plugin.driver_id == normalized:
                return plugin
        raise ConfigError(f"unknown plugin driver_id: {driver_id}")


def builtin_plugin_registry() -> PluginRegistry:
    return PluginRegistry(BUILTIN_PLUGINS)
