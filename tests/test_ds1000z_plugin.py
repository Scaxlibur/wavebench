from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import sysconfig

import numpy as np
import pytest

from wavebench.errors import DataError, OperationTimeout
from wavebench.instruments.api import DriverContext
from wavebench.logging import CommandLogger

PLUGIN_ROOT = (
    Path(__file__).resolve().parents[1]
    / "packages"
    / "plugins"
    / "wavebench-rigol-ds1000z"
)
sys.path.insert(0, str(PLUGIN_ROOT / "src"))

from wavebench_rigol_ds1000z import descriptor as plugin_descriptor  # noqa: E402
from wavebench_rigol_ds1000z.driver import DS1000ZScope  # noqa: E402


class FakeTransport:
    def __init__(self, *, responses=None, binary_reader=None):
        self.responses = responses or {}
        self.binary_reader = binary_reader
        self.writes = []
        self.queries = []
        self.events = []
        self.closed = False

    def write(self, command):
        self.writes.append(command)

    def query(self, command):
        self.queries.append(command)
        return self.responses[command]

    def query_bin_block(self, command):
        self.queries.append(command)
        if self.binary_reader is not None:
            return self.binary_reader(self, command)
        return self.responses[command]

    def query_opc(self):
        self.queries.append("*OPC?")
        return "1"

    def record_event(self, direction, text):
        self.events.append((direction, text))

    def close(self):
        self.closed = True


def test_plugin_descriptor_is_executable_v2_metadata_without_io():
    descriptor = plugin_descriptor()

    assert descriptor.driver_id == "rigol.ds1000z"
    assert descriptor.api_version == "wavebench.instrument.v2"
    assert descriptor.aliases == ()
    assert descriptor.backends == ("pyvisa",)
    assert descriptor.scope_coupling_policy == "fixed-high-impedance"
    assert descriptor.validate_options({}) == {"max_chunk_points": 250_000}
    with pytest.raises(ValueError, match=r"must be <= 250000"):
        descriptor.validate_options({"max_chunk_points": 250_001})


def test_plugin_factory_uses_core_context_transport_only():
    transport = FakeTransport()
    descriptor = plugin_descriptor()
    context = DriverContext(
        driver_id=descriptor.driver_id,
        kind="scope",
        resource="configured-resource",
        backend="pyvisa",
        timeout_ms=1000,
        opc_timeout_ms=2000,
        logger=CommandLogger(),
        _transport_factory=lambda: transport,
        settings={"check_errors": True},
        options=descriptor.validate_options({"max_chunk_points": 123}),
    )

    driver = descriptor.factory(context)

    assert driver.transport is transport
    assert driver.max_byte_points_per_read == 123


def test_plugin_norm_raw_dmax_conversion_and_chunk_boundaries():
    normal_transport = FakeTransport(
        responses={
            ":WAVeform:PREamble?": "0,0,3,1,0.5,-1,1,0.25,100,10",
            ":WAVeform:DATA?": bytes([109, 110, 111]),
        }
    )
    normal_scope = DS1000ZScope(transport=normal_transport, max_byte_points_per_read=3)

    normal = normal_scope.fetch_waveform(channel=2, points="DEF", check_errors=False)

    np.testing.assert_allclose(normal.voltages_v, [-0.25, 0.0, 0.25])
    np.testing.assert_allclose(normal.times_s, [-1.5, -1.0, -0.5])
    assert ":WAVeform:MODE NORMal" in normal_transport.writes

    def binary_reader(transport, command):
        start = int(transport.writes[-2].split()[-1])
        stop = int(transport.writes[-1].split()[-1])
        return bytes([127]) * (stop - start + 1)

    for points_alias in ("MAX", "DMAX"):
        raw_transport = FakeTransport(
            responses={":WAVeform:PREamble?": "0,0,8,1,1e-9,0,0,0.01,0,127"},
            binary_reader=binary_reader,
        )
        raw_scope = DS1000ZScope(transport=raw_transport, max_byte_points_per_read=3)

        waveform = raw_scope.fetch_waveform(
            channel=1,
            points=points_alias,
            check_errors=False,
        )

        assert waveform.sample_count == 8
        assert raw_transport.writes[0] == ":STOP"
        assert raw_transport.queries.count(":WAVeform:DATA?") == 3
        assert ":WAVeform:STARt 7" in raw_transport.writes
        assert ":WAVeform:STOP 8" in raw_transport.writes
        assert any(
            direction == "telemetry"
            and "stage=waveform_chunk" in text
            and "range=1-3" in text
            for direction, text in raw_transport.events
        )
        assert any(
            direction == "telemetry"
            and "stage=waveform_transfer" in text
            and "chunks=3" in text
            for direction, text in raw_transport.events
        )


def test_plugin_failed_raw_chunk_records_range_before_raising():
    def binary_reader(transport, command):
        start = int(transport.writes[-2].split()[-1])
        if start == 4:
            raise TimeoutError("interrupted")
        return bytes([127]) * 3

    transport = FakeTransport(
        responses={":WAVeform:PREamble?": "0,0,6,1,1e-9,0,0,0.01,0,127"},
        binary_reader=binary_reader,
    )

    with pytest.raises(TimeoutError, match="interrupted"):
        DS1000ZScope(
            transport=transport,
            max_byte_points_per_read=3,
        ).fetch_waveform(channel=1, points="DMAX", check_errors=False)

    assert any(
        direction == "telemetry"
        and "stage=waveform_chunk" in text
        and "status=failed" in text
        and "range=4-6" in text
        for direction, text in transport.events
    )


def test_plugin_single_autoscale_screenshot_errors_and_close():
    png = b"\x89PNG\r\n\x1a\nplugin"
    transport = FakeTransport(
        responses={
            ":WAVeform:PREamble?": "0,0,2,1,1e-3,0,0,0.1,0,127",
            ":WAVeform:DATA?": bytes([127, 128]),
            ":SYSTem:ERRor?": '0,"No error"',
            ":DISPlay:DATA? ON,OFF,PNG": png,
        }
    )
    scope = DS1000ZScope(transport=transport)

    scope.capture_waveform(channel=1, points="DEF", check_errors=True)
    scope.autoscale(wait_opc=True, check_errors=True)

    assert ":SINGle" in transport.writes
    assert ":AUToscale" in transport.writes
    assert transport.queries.count("*OPC?") == 2
    assert scope.screenshot_png() == png
    assert scope.errors() == ['0,"No error"']
    scope.close()
    assert transport.closed


def test_plugin_multichannel_capture_uses_one_single_and_one_opc():
    transport = FakeTransport(
        responses={
            ":WAVeform:PREamble?": "0,0,2,1,1e-3,0,0,0.1,0,127",
            ":WAVeform:DATA?": bytes([127, 128]),
        }
    )

    waveforms = DS1000ZScope(transport=transport).capture_waveforms(
        channels=[1, 2],
        points="DEF",
        check_errors=False,
    )

    assert list(waveforms) == [1, 2]
    assert transport.writes.count(":SINGle") == 1
    assert transport.queries.count("*OPC?") == 1


def test_plugin_rejects_bad_preamble_short_blocks_screenshot_and_opc_timeout():
    bad_preamble = FakeTransport(responses={":WAVeform:PREamble?": "bad"})
    with pytest.raises(DataError, match="PREamble"):
        DS1000ZScope(bad_preamble).fetch_waveform(
            channel=1,
            points="DEF",
            check_errors=False,
        )

    short_block = FakeTransport(
        responses={
            ":WAVeform:PREamble?": "0,0,3,1,1e-3,0,0,0.1,0,127",
            ":WAVeform:DATA?": bytes([127]),
        }
    )
    with pytest.raises(DataError, match="length mismatch"):
        DS1000ZScope(short_block).fetch_waveform(
            channel=1,
            points="DEF",
            check_errors=False,
        )

    with pytest.raises(DataError, match="not a PNG"):
        DS1000ZScope(
            FakeTransport(responses={":DISPlay:DATA? ON,OFF,PNG": b"not-png"})
        ).screenshot_png()

    timeout_transport = FakeTransport(
        responses={
            ":WAVeform:PREamble?": "0,0,2,1,1e-3,0,0,0.1,0,127",
            ":WAVeform:DATA?": bytes([127, 128]),
        }
    )
    timeout_transport.query_opc = lambda: (_ for _ in ()).throw(TimeoutError("timeout"))
    with pytest.raises(OperationTimeout, match="single acquisition timed out"):
        DS1000ZScope(timeout_transport).capture_waveform(
            channel=1,
            points="DEF",
            check_errors=False,
        )


def test_plugin_wheel_install_discovery_reinstall_and_uninstall(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    _run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-build-isolation",
            "--no-deps",
            "--wheel-dir",
            str(wheelhouse),
            str(project_root),
            str(PLUGIN_ROOT),
        ],
        cwd=tmp_path,
    )
    core_wheel = next(wheelhouse.glob("wavebench-0.7.0-*.whl"))
    plugin_wheel = next(wheelhouse.glob("wavebench_rigol_ds1000z-0.1.0-*.whl"))
    venv_dir = tmp_path / "venv"
    _run([sys.executable, "-m", "venv", str(venv_dir)], cwd=tmp_path)
    python = venv_dir / "bin" / "python"
    purelib = _run(
        [str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"],
        cwd=tmp_path,
    ).stdout.strip()
    parent_site_packages = sysconfig.get_paths()["purelib"]
    Path(purelib, "wavebench-test-dependencies.pth").write_text(
        parent_site_packages + "\n",
        encoding="utf-8",
    )
    _run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-deps",
            str(core_wheel),
            str(plugin_wheel),
        ],
        cwd=tmp_path,
    )
    discovery_script = """
from importlib.metadata import entry_points
from wavebench.instruments.registry import build_instrument_registry
from wavebench.transport.pyvisa_transport import PyVisaTransport

def forbidden(*args, **kwargs):
    raise AssertionError("plugin import attempted instrument I/O")

PyVisaTransport.open = forbidden
points = list(entry_points().select(group="wavebench.instruments"))
assert [point.name for point in points] == ["rigol.ds1000z"]
loaded = points[0].load()
descriptor = loaded()
assert descriptor.driver_id == "rigol.ds1000z"
resolved = build_instrument_registry().resolve("rigol.ds1000z", expected_kind="scope")
assert resolved.distribution == "wavebench-rigol-ds1000z"
"""
    _run([str(python), "-c", discovery_script], cwd=tmp_path)
    _run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--force-reinstall",
            str(plugin_wheel),
        ],
        cwd=tmp_path,
    )
    _run(
        [str(python), "-m", "pip", "uninstall", "-y", "wavebench-rigol-ds1000z"],
        cwd=tmp_path,
    )
    uninstall_script = """
from importlib.metadata import entry_points
from wavebench.instruments.registry import build_instrument_registry

assert not entry_points().select(group="wavebench.instruments")
descriptor = build_instrument_registry().resolve("ds1000z", expected_kind="scope")
assert descriptor.driver_id == "rigol.ds1104"
"""
    _run([str(python), "-c", uninstall_script], cwd=tmp_path)


def _run(command, *, cwd):
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )
