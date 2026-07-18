from dataclasses import replace

import pytest

from wavebench.errors import ConfigError
from wavebench.instruments.api import DriverContext, InstrumentDescriptor, OptionSpec
from wavebench.instruments.registry import InstrumentRegistry, build_instrument_registry
from wavebench.logging import CommandLogger


class FakeEntryPoint:
    group = "wavebench.instruments"
    dist = None

    def __init__(self, name, loaded):
        self.name = name
        self.loaded = loaded
        self.load_count = 0

    def load(self):
        self.load_count += 1
        if isinstance(self.loaded, Exception):
            raise self.loaded
        return self.loaded


class FakeEntryPoints(list):
    def select(self, *, group):
        return [item for item in self if item.group == group]


def make_descriptor(driver_id="example.scope", **changes):
    descriptor = InstrumentDescriptor(
        driver_id=driver_id,
        kind="scope",
        display_name="Example Scope",
        manufacturer="Example",
        models=("EX1",),
        aliases=("example",),
        capabilities=("scope.idn",),
        idn_patterns=("EXAMPLE,EX1",),
        backends=("pyvisa",),
        option_specs=(OptionSpec("check_errors", bool, default=True),),
        permissions=("instrument.io",),
        factory=lambda context: object(),
    )
    return replace(descriptor, **changes)


def test_builtin_aliases_and_canonical_ids_resolve_to_same_descriptor():
    registry = build_instrument_registry(include_entry_points=False)

    assert registry.resolve("rtm2032", expected_kind="scope").driver_id == "rohde-schwarz.rtm2032"
    assert registry.resolve("ds1104", expected_kind="scope").driver_id == "rigol.ds1104"
    assert registry.resolve("ds1000z", expected_kind="scope").driver_id == "rigol.ds1104"
    assert registry.resolve("dm3058", expected_kind="dmm").driver_id == "rigol.dm3000"


def test_registry_does_not_load_unselected_entry_points(monkeypatch):
    selected = FakeEntryPoint("example.scope", make_descriptor())
    broken = FakeEntryPoint("broken.scope", RuntimeError("boom"))
    monkeypatch.setattr(
        "wavebench.instruments.registry.entry_points",
        lambda: FakeEntryPoints([selected, broken]),
    )

    registry = build_instrument_registry()
    descriptor = registry.resolve("example.scope", expected_kind="scope")

    assert descriptor.driver_id == "example.scope"
    assert selected.load_count == 1
    assert broken.load_count == 0


def test_selected_entry_point_failures_are_actionable_and_isolated():
    broken = FakeEntryPoint("broken.scope", RuntimeError("boom"))
    registry = InstrumentRegistry(external_entry_points=(broken,))

    with pytest.raises(ConfigError, match="failed to load instrument driver 'broken.scope': boom"):
        registry.resolve("broken.scope", expected_kind="scope")

    assert registry.resolve("rtm2032", expected_kind="scope").driver_id == "rohde-schwarz.rtm2032"


def test_registry_rejects_kind_version_and_builtin_override():
    wrong_kind = FakeEntryPoint("example.scope", make_descriptor(kind="source"))
    incompatible = FakeEntryPoint(
        "future.scope",
        make_descriptor(
            driver_id="future.scope",
            aliases=("future",),
            wavebench_min_version="99.0.0",
        ),
    )
    override = FakeEntryPoint(
        "external.scope",
        make_descriptor(driver_id="external.scope", aliases=("rtm2032",)),
    )

    with pytest.raises(ConfigError, match="expected 'scope'"):
        InstrumentRegistry(external_entry_points=(wrong_kind,)).resolve(
            "example.scope", expected_kind="scope"
        )
    with pytest.raises(ConfigError, match="supports WaveBench"):
        InstrumentRegistry(external_entry_points=(incompatible,)).resolve(
            "future.scope", expected_kind="scope"
        )
    with pytest.raises(ConfigError, match="conflicts with built-in"):
        InstrumentRegistry(external_entry_points=(override,)).resolve(
            "external.scope", expected_kind="scope"
        )


def test_descriptor_validates_restricted_options_and_exports_v1_metadata():
    descriptor = make_descriptor()

    assert descriptor.validate_options({}) == {"check_errors": True}
    assert descriptor.validate_options({"check_errors": False}) == {"check_errors": False}
    with pytest.raises(ValueError, match="unknown option"):
        descriptor.validate_options({"raw_scpi": True})
    assert descriptor.to_metadata().driver_id == descriptor.driver_id


def test_driver_context_exposes_only_fixed_resource_and_transport_factory():
    sentinel = object()
    context = DriverContext(
        driver_id="example.scope",
        kind="scope",
        resource="redacted-resource",
        backend="pyvisa",
        timeout_ms=1000,
        opc_timeout_ms=2000,
        logger=CommandLogger(),
        _transport_factory=lambda: sentinel,
        options={"check_errors": True},
    )

    assert context.open_transport() is sentinel
    with pytest.raises(TypeError):
        context.options["check_errors"] = False
