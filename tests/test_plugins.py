import pytest

from wavebench.errors import ConfigError
from wavebench.plugins.api import InstrumentPlugin
from wavebench.plugins.registry import PluginRegistry, builtin_plugin_registry


def test_builtin_registry_lists_expected_drivers():
    registry = builtin_plugin_registry()
    driver_ids = [plugin.driver_id for plugin in registry.list_plugins()]

    assert driver_ids == [
        "rigol.dm3000",
        "rigol.dp800",
        "rohde-schwarz.rtm2032",
        "rigol.dg4202",
    ]


def test_builtin_registry_filters_by_kind():
    registry = builtin_plugin_registry()

    assert [plugin.driver_id for plugin in registry.list_plugins(kind="source")] == ["rigol.dg4202"]
    assert [plugin.driver_id for plugin in registry.list_plugins(kind="scope")] == [
        "rohde-schwarz.rtm2032"
    ]


def test_builtin_registry_get_returns_metadata():
    plugin = builtin_plugin_registry().get("rigol.dg4202")

    assert plugin.kind == "source"
    assert "source.set_frequency" in plugin.capabilities
    assert "DG4202" in plugin.models


def test_registry_rejects_duplicate_driver_ids():
    plugin = InstrumentPlugin(
        driver_id="example.driver",
        kind="scope",
        display_name="Example Scope",
        manufacturer="Example",
        models=("EX1",),
        capabilities=("scope.idn",),
        summary="Example plugin.",
    )

    with pytest.raises(ConfigError, match="duplicate plugin driver_id"):
        PluginRegistry((plugin, plugin))


def test_registry_unknown_driver_raises_config_error():
    with pytest.raises(ConfigError, match="unknown plugin driver_id"):
        builtin_plugin_registry().get("missing.driver")
