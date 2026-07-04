"""Plugin registry support for WaveBench."""

from .api import InstrumentPlugin
from .registry import PluginRegistry, builtin_plugin_registry

__all__ = ["InstrumentPlugin", "PluginRegistry", "builtin_plugin_registry"]
