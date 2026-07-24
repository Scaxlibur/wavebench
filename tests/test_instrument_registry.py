from dataclasses import replace

import pytest

from wavebench.errors import ConfigError
from wavebench.instruments.api import DriverContext, InstrumentDescriptor, OptionSpec
from wavebench.instruments.factory import open_instrument_driver
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
        aliases=(),
        capabilities=("scope.idn",),
        idn_patterns=("EXAMPLE,EX1",),
        backends=("pyvisa",),
        option_specs=(OptionSpec("check_errors", bool, default=True),),
        permissions=("instrument.io",),
        factory=lambda context: object(),
    )
    return replace(descriptor, **changes)


def make_external_dg4202_descriptor(**changes):
    builtin = build_instrument_registry(include_entry_points=False).resolve(
        "rigol.dg4202",
        expected_kind="source",
    )
    changes.setdefault("distribution", "wavebench-rigol-dg4000")
    return replace(
        builtin,
        aliases=(),
        **changes,
    )


def make_external_dm3000_descriptor(**changes):
    builtin = build_instrument_registry(include_entry_points=False).resolve(
        "rigol.dm3000",
        expected_kind="dmm",
    )
    changes.setdefault("distribution", "wavebench-rigol-dm3000")
    return replace(
        builtin,
        aliases=(),
        backends=("pyvisa",),
        resource_schemes=("tcpip",),
        **changes,
    )


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
            wavebench_min_version="99.0.0",
        ),
    )
    override = FakeEntryPoint(
        "rigol.ds1104",
        make_descriptor(driver_id="rigol.ds1104"),
    )

    with pytest.raises(ConfigError, match="expected 'scope'"):
        InstrumentRegistry(external_entry_points=(wrong_kind,)).resolve(
            "example.scope", expected_kind="scope"
        )
    with pytest.raises(ConfigError, match="supports WaveBench"):
        InstrumentRegistry(external_entry_points=(incompatible,)).resolve(
            "future.scope", expected_kind="scope"
        )
    override_result = InstrumentRegistry(external_entry_points=(override,)).load_all()
    assert len(override_result.load_errors) == 1
    assert "conflicts with built-in" in override_result.load_errors[0].message


def test_migration_canonical_prefers_external_while_alias_keeps_builtin_fallback():
    entry_point = FakeEntryPoint("rigol.dg4202", make_external_dg4202_descriptor())
    registry = InstrumentRegistry(external_entry_points=(entry_point,))

    canonical = registry.resolve("rigol.dg4202", expected_kind="source")
    alias = registry.resolve("dg4202", expected_kind="source")
    loaded = registry.load_all()

    assert canonical.origin == "entry_point"
    assert alias.origin == "builtin"
    assert [item.origin for item in loaded.descriptors if item.driver_id == "rigol.dg4202"] == [
        "entry_point"
    ]
    assert loaded.load_errors == ()


def test_dm3000_migration_is_lan_only_while_aliases_keep_builtin_fallback():
    entry_point = FakeEntryPoint("rigol.dm3000", make_external_dm3000_descriptor())
    registry = InstrumentRegistry(external_entry_points=(entry_point,))

    canonical = registry.resolve("rigol.dm3000", expected_kind="dmm")
    dm3000_alias = registry.resolve("dm3000", expected_kind="dmm")
    dm3058_alias = registry.resolve("dm3058", expected_kind="dmm")
    loaded = registry.load_all()

    assert canonical.origin == "entry_point"
    assert canonical.backends == ("pyvisa",)
    assert canonical.resource_schemes == ("tcpip",)
    assert dm3000_alias.origin == "builtin"
    assert dm3058_alias.origin == "builtin"
    assert dm3000_alias.backends == ("serial", "pyvisa")
    assert dm3058_alias.backends == ("serial", "pyvisa")
    assert [item.origin for item in loaded.descriptors if item.driver_id == "rigol.dm3000"] == [
        "entry_point"
    ]
    assert loaded.load_errors == ()


def test_migration_canonical_falls_back_to_builtin_when_external_is_absent():
    descriptor = build_instrument_registry(include_entry_points=False).resolve(
        "rigol.dg4202",
        expected_kind="source",
    )

    assert descriptor.origin == "builtin"


def test_invalid_migration_plugin_does_not_remove_builtin_from_load_all():
    descriptor = make_external_dg4202_descriptor(
        capabilities=("source.unknown",),
    )
    entry_point = FakeEntryPoint("rigol.dg4202", descriptor)

    loaded = InstrumentRegistry(external_entry_points=(entry_point,)).load_all()

    matches = [item for item in loaded.descriptors if item.driver_id == "rigol.dg4202"]
    assert [item.origin for item in matches] == ["builtin"]
    assert len(loaded.load_errors) == 1


def test_duplicate_migration_entry_point_keeps_first_external_and_reports_second():
    first = FakeEntryPoint("rigol.dg4202", make_external_dg4202_descriptor())
    second = FakeEntryPoint("rigol.dg4202", make_external_dg4202_descriptor())

    loaded = InstrumentRegistry(external_entry_points=(first, second)).load_all()

    matches = [item for item in loaded.descriptors if item.driver_id == "rigol.dg4202"]
    assert [item.origin for item in matches] == ["entry_point"]
    assert len(loaded.load_errors) == 1
    assert "conflicts with loaded" in loaded.load_errors[0].message


def test_migration_slot_rejects_wrong_distribution_for_same_canonical():
    descriptor = make_external_dg4202_descriptor(distribution="not-the-allowed-package")
    entry_point = FakeEntryPoint("rigol.dg4202", descriptor)

    loaded = InstrumentRegistry(external_entry_points=(entry_point,)).load_all()

    matches = [item for item in loaded.descriptors if item.driver_id == "rigol.dg4202"]
    assert [item.origin for item in matches] == ["builtin"]
    assert len(loaded.load_errors) == 1
    assert "conflicts with built-in" in loaded.load_errors[0].message


def test_dm3000_migration_slot_rejects_wrong_distribution():
    descriptor = make_external_dm3000_descriptor(distribution="not-the-allowed-package")
    entry_point = FakeEntryPoint("rigol.dm3000", descriptor)

    loaded = InstrumentRegistry(external_entry_points=(entry_point,)).load_all()

    matches = [item for item in loaded.descriptors if item.driver_id == "rigol.dm3000"]
    assert [item.origin for item in matches] == ["builtin"]
    assert len(loaded.load_errors) == 1
    assert "conflicts with built-in" in loaded.load_errors[0].message


def test_registry_rejects_external_aliases_as_canonical_only():
    descriptor = make_descriptor(aliases=("example-scope",))
    entry_point = FakeEntryPoint("example.scope", descriptor)
    registry = InstrumentRegistry(external_entry_points=(entry_point,))

    with pytest.raises(ConfigError, match="canonical-ID-only"):
        registry.resolve("example.scope", expected_kind="scope")

    result = registry.load_all()

    assert all(item.driver_id != "example.scope" for item in result.descriptors)
    assert len(result.load_errors) == 1
    assert "canonical-ID-only" in result.load_errors[0].message


def test_descriptor_validates_restricted_options_and_exports_v1_metadata():
    descriptor = make_descriptor()

    assert descriptor.validate_options({}) == {"check_errors": True}
    assert descriptor.validate_options({"check_errors": False}) == {"check_errors": False}
    with pytest.raises(ValueError, match="unknown option"):
        descriptor.validate_options({"raw_scpi": True})
    assert descriptor.to_metadata().driver_id == descriptor.driver_id


def test_descriptor_validates_resource_scheme_tokens():
    assert make_descriptor(resource_schemes=("tcpip",)).resource_schemes == ("tcpip",)
    with pytest.raises(ValueError, match="resource schemes must be lowercase tokens"):
        make_descriptor(resource_schemes=("TCPIP",))
    with pytest.raises(ValueError, match="duplicate resource schemes"):
        make_descriptor(resource_schemes=("tcpip", "tcpip"))


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
        settings={"check_errors": True},
        options={"check_errors": True},
    )

    assert context.open_transport() is sentinel
    with pytest.raises(TypeError):
        context.settings["check_errors"] = False
    with pytest.raises(TypeError):
        context.options["check_errors"] = False


def test_core_factory_builds_context_and_validates_driver_contract(monkeypatch):
    captured = {}
    transport = object()

    def factory(context):
        captured["context"] = context
        captured["transport"] = context.open_transport()
        return _ScopeDriver()

    descriptor = make_descriptor(factory=factory, option_specs=())
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.PyVisaTransport.open",
        lambda connection, logger: transport,
    )

    opened = open_instrument_driver(
        driver_reference="example.scope",
        expected_kind="scope",
        resource="configured-resource",
        configured_backend="lan",
        timeout_ms=1000,
        opc_timeout_ms=2000,
        read_retry_attempts=1,
        read_retry_delay_ms=10,
        logger=CommandLogger(),
        settings={"check_errors": True},
    )

    assert opened.driver.__class__ is _ScopeDriver
    assert captured["transport"] is transport
    assert captured["context"].resource == "configured-resource"
    assert captured["context"].backend == "pyvisa"
    assert captured["context"].settings == {"check_errors": True}


@pytest.mark.parametrize("configured_backend", ["lan", "visa", "pyvisa"])
def test_core_factory_maps_lan_backends_to_single_rsinstrument_backend(
    monkeypatch,
    configured_backend,
):
    captured = {}
    transport = object()

    def factory(context):
        captured["backend"] = context.backend
        captured["transport"] = context.open_transport()
        return _ScopeDriver()

    descriptor = make_descriptor(
        backends=("rsinstrument",),
        factory=factory,
        option_specs=(),
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.RsInstrumentTransport.open",
        lambda connection, logger: transport,
    )

    opened = open_instrument_driver(
        driver_reference="example.scope",
        expected_kind="scope",
        resource="configured-resource",
        configured_backend=configured_backend,
        timeout_ms=1000,
        opc_timeout_ms=2000,
        read_retry_attempts=1,
        read_retry_delay_ms=10,
        logger=CommandLogger(),
    )

    assert opened.driver.__class__ is _ScopeDriver
    assert captured == {"backend": "rsinstrument", "transport": transport}


def test_core_factory_rejects_explicit_serial_for_lan_only_driver(monkeypatch):
    descriptor = make_descriptor(backends=("pyvisa",), option_specs=())
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )

    with pytest.raises(ConfigError, match="configured backend 'serial'.*supports: pyvisa"):
        open_instrument_driver(
            driver_reference="example.scope",
            expected_kind="scope",
            resource="/dev/serial/by-id/example",
            configured_backend="serial",
            timeout_ms=1000,
            opc_timeout_ms=2000,
            read_retry_attempts=1,
            read_retry_delay_ms=10,
            logger=CommandLogger(),
        )


@pytest.mark.parametrize("configured_backend", ["lan", "visa", "pyvisa"])
@pytest.mark.parametrize(
    "resource",
    [
        "ASRL/dev/ttyUSB0::INSTR",
        "ASRL1::INSTR",
        "USB0::0x1234::0x5678::INSTR",
        "GPIB0::10::INSTR",
    ],
)
def test_core_factory_rejects_non_tcpip_visa_resources_for_lan_only_driver(
    monkeypatch,
    configured_backend,
    resource,
):
    descriptor = make_descriptor(
        backends=("pyvisa",),
        resource_schemes=("tcpip",),
        option_specs=(),
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )

    with pytest.raises(ConfigError, match="resource scheme.*is not supported.*tcpip"):
        open_instrument_driver(
            driver_reference="example.scope",
            expected_kind="scope",
            resource=resource,
            configured_backend=configured_backend,
            timeout_ms=1000,
            opc_timeout_ms=2000,
            read_retry_attempts=1,
            read_retry_delay_ms=10,
            logger=CommandLogger(),
        )


@pytest.mark.parametrize("configured_backend", ["lan", "visa", "pyvisa"])
@pytest.mark.parametrize(
    "resource",
    ["TCPIP::192.0.2.40::INSTR", "TCPIP0::192.0.2.40::5025::SOCKET"],
)
def test_core_factory_accepts_tcpip_resources_for_lan_only_driver(
    monkeypatch,
    configured_backend,
    resource,
):
    transport = object()

    class MinimalIdnDriver:
        def idn(self):
            return "EXAMPLE,EX1"

        def close(self):
            pass

    descriptor = make_descriptor(
        backends=("pyvisa",),
        resource_schemes=("tcpip",),
        factory=lambda context: (context.open_transport(), MinimalIdnDriver())[1],
        option_specs=(),
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.PyVisaTransport.open",
        lambda connection, logger: transport,
    )

    opened = open_instrument_driver(
        driver_reference="example.scope",
        expected_kind="scope",
        resource=resource,
        configured_backend=configured_backend,
        timeout_ms=1000,
        opc_timeout_ms=2000,
        read_retry_attempts=1,
        read_retry_delay_ms=10,
        logger=CommandLogger(),
    )

    assert opened.driver.idn() == "EXAMPLE,EX1"


def test_core_factory_accepts_minimal_driver_for_declared_capabilities(monkeypatch):
    class MinimalIdnDriver:
        def idn(self):
            return "EXAMPLE,EX1"

        def close(self):
            pass

    descriptor = make_descriptor(factory=lambda context: MinimalIdnDriver(), option_specs=())
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )

    opened = _open_example_scope()

    assert opened.driver.idn() == "EXAMPLE,EX1"


def test_core_factory_rejects_declared_capability_without_method(monkeypatch):
    class MissingCaptureDriver:
        def idn(self):
            return "EXAMPLE,EX1"

        def close(self):
            pass

    descriptor = make_descriptor(
        capabilities=("scope.idn", "scope.capture_waveform"),
        factory=lambda context: MissingCaptureDriver(),
        option_specs=(),
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )

    with pytest.raises(ConfigError, match="scope.capture_waveform.*capture_waveform"):
        _open_example_scope()


def test_core_factory_isolates_protocol_and_close_failures(monkeypatch):
    transport = _FakeTransport()

    class BrokenDriver:
        def __init__(self, owned_transport):
            self.transport = owned_transport

        def idn(self):
            return "BROKEN"

        def close(self):
            raise RuntimeError("close failed")

    descriptor = make_descriptor(
        capabilities=("scope.idn", "scope.capture_waveform"),
        factory=lambda context: BrokenDriver(context.open_transport()),
        option_specs=(),
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory._open_transport",
        lambda **kwargs: transport,
    )

    with pytest.raises(ConfigError, match="scope.capture_waveform.*capture_waveform"):
        open_instrument_driver(
            driver_reference="example.scope",
            expected_kind="scope",
            resource="configured-resource",
            configured_backend="lan",
            timeout_ms=1000,
            opc_timeout_ms=2000,
            read_retry_attempts=1,
            read_retry_delay_ms=10,
            logger=CommandLogger(),
        )

    assert transport.close_count == 1


def test_core_factory_closes_transport_when_factory_raises(monkeypatch):
    transport = _FakeTransport()

    def factory(context):
        context.open_transport()
        raise RuntimeError("factory failed")

    descriptor = make_descriptor(factory=factory, option_specs=())
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory._open_transport",
        lambda **kwargs: transport,
    )

    with pytest.raises(ConfigError, match="factory failed"):
        _open_example_scope()

    assert transport.close_count == 1


def test_core_factory_rejects_second_transport_and_closes_first(monkeypatch):
    transport = _FakeTransport()

    def factory(context):
        context.open_transport()
        context.open_transport()
        return _ScopeDriver()

    descriptor = make_descriptor(factory=factory, option_specs=())
    monkeypatch.setattr(
        "wavebench.instruments.factory.resolve_instrument_descriptor",
        lambda reference, expected_kind: descriptor,
    )
    monkeypatch.setattr(
        "wavebench.instruments.factory._open_transport",
        lambda **kwargs: transport,
    )

    with pytest.raises(ConfigError, match="requested more than one transport"):
        _open_example_scope()

    assert transport.close_count == 1


def _open_example_scope():
    return open_instrument_driver(
        driver_reference="example.scope",
        expected_kind="scope",
        resource="configured-resource",
        configured_backend="lan",
        timeout_ms=1000,
        opc_timeout_ms=2000,
        read_retry_attempts=1,
        read_retry_delay_ms=10,
        logger=CommandLogger(),
    )


class _FakeTransport:
    def __init__(self):
        self.close_count = 0

    def close(self):
        self.close_count += 1


class _ScopeDriver:
    def idn(self):
        return "EXAMPLE,EX1"

    def close(self):
        pass

    def errors(self, limit=16):
        return []

    def channel_coupling(self, channel):
        return "DC"

    def autoscale(self, wait_opc=True, check_errors=True):
        pass

    def fetch_waveform(self, channel, points="dmax", check_errors=True):
        return None

    def capture_waveform(
        self,
        channel,
        points="dmax",
        check_errors=True,
        time_range_s=None,
        vertical_scale_v_per_div=None,
    ):
        return None

    def screenshot_png(self, *, include_menu=False, color_scheme="COL"):
        return b""
