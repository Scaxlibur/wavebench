from dataclasses import asdict

import numpy as np

from wavebench.drivers.dg4202 import SourceStatus as LegacySourceStatus
from wavebench.drivers.dm3000 import DmmReading as LegacyDmmReading
from wavebench.drivers.dp800 import PowerStatus as LegacyPowerStatus
from wavebench.drivers.rtm2032 import (
    WaveformData as LegacyWaveformData,
    WaveformHeader as LegacyWaveformHeader,
)
from wavebench.instruments.contracts import DmmDriver, PowerDriver, ScopeDriver, SourceDriver
from wavebench.instruments.models import (
    DmmReading,
    PowerStatus,
    SourceStatus,
    WaveformData,
    WaveformHeader,
)


def test_legacy_driver_model_imports_are_compatible_reexports():
    assert LegacyWaveformHeader is WaveformHeader
    assert LegacyWaveformData is WaveformData
    assert LegacySourceStatus is SourceStatus
    assert LegacyPowerStatus is PowerStatus
    assert LegacyDmmReading is DmmReading


def test_shared_models_keep_serialization_and_waveform_behavior():
    header = WaveformHeader(x_start=0.0, x_stop=2.0, points=3)
    waveform = WaveformData(channel=1, header=header, voltages_v=np.array([0.0, 1.0, 0.0]))
    reading = DmmReading(function="dcv", value=1.25, unit="V", raw="1.25")

    assert header.x_increment == 1.0
    assert waveform.times_s.tolist() == [0.0, 1.0, 2.0]
    assert waveform.sample_count == 3
    assert asdict(reading) == {"function": "dcv", "value": 1.25, "unit": "V", "raw": "1.25"}
    assert reading.as_dict() == asdict(reading)


def test_driver_contracts_are_runtime_checkable():
    assert isinstance(_Scope(), ScopeDriver)
    assert isinstance(_Source(), SourceDriver)
    assert isinstance(_Power(), PowerDriver)
    assert isinstance(_Dmm(), DmmDriver)


class _DynamicDriver:
    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class _Scope(_DynamicDriver):
    idn = close = errors = channel_coupling = autoscale = fetch_waveform = capture_waveform = screenshot_png = lambda *args, **kwargs: None


class _Source(_DynamicDriver):
    idn = close = errors = assert_no_errors = get_status = set_frequency = set_output = set_function = set_amplitude_vpp = set_square_duty_cycle = upload_dg4000_dac14_block = probe_arbitrary_queries = lambda *args, **kwargs: None


class _Power(_DynamicDriver):
    idn = close = get_status = get_measurement = get_protection_status = set_protection = set_voltage_current_limit = set_output = lambda *args, **kwargs: None


class _Dmm(_DynamicDriver):
    idn = close = function_status = set_function = read = lambda *args, **kwargs: None
