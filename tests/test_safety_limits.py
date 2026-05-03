from pathlib import Path
from unittest.mock import patch
import unittest

from wavebench.config import (
    AutoscaleConfig,
    ConnectionConfig,
    OutputConfig,
    PowerConfig,
    SafetyLimitsConfig,
    SourceConfig,
    ScopeConfig,
    WaveBenchConfig,
    WaveformConfig,
)
from wavebench.drivers.dg4202 import SourceStatus
from wavebench.drivers.dp800 import PowerStatus
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.services.power_service import PowerService
from wavebench.services.source_service import SourceService


def make_config() -> WaveBenchConfig:
    return WaveBenchConfig(
        connection=ConnectionConfig("lan", "TCPIP::scope::INSTR", 1000, 1000),
        scope=ScopeConfig("rtm2032", None, 1, False, True),
        autoscale=AutoscaleConfig(True, True),
        waveform=WaveformConfig("real", "lsbf", "DMAX"),
        output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
        source_path=Path("wavebench.toml"),
        source=SourceConfig("dg4202", "TCPIP::source::INSTR", 2, True, True, 0),
        power=PowerConfig("dp800", "TCPIP::power::INSTR", 1, True, 0, 0),
        safety_limits=SafetyLimitsConfig(
            max_source_vpp=2.0,
            max_power_voltage_v=5.0,
            max_power_current_limit_a=0.2,
        ),
    )


def source_status(amplitude: float) -> SourceStatus:
    return SourceStatus(
        channel=2,
        output="OFF",
        function="SIN",
        frequency_hz=1000.0,
        amplitude=amplitude,
        amplitude_unit="VPP",
        offset_v=0.0,
        phase_deg=0.0,
        frequency_mode="FIX",
        sweep_enabled="OFF",
        apply_raw=None,
    )


def power_status(voltage: float, current_limit: float) -> PowerStatus:
    return PowerStatus(
        channel=1,
        output="OFF",
        mode="CV",
        rating=None,
        set_voltage_v=voltage,
        set_current_a=current_limit,
        measured_voltage_v=0.0,
        measured_current_a=0.0,
        measured_power_w=0.0,
    )


class FakeSource:
    def __init__(self, status: SourceStatus):
        self.status = status
        self.output_calls = []
        self.closed = False

    def get_status(self, channel: int) -> SourceStatus:
        return self.status

    def set_output(self, channel: int, enabled: bool, *, check_errors: bool = True) -> SourceStatus:
        self.output_calls.append((channel, enabled, check_errors))
        return self.status

    def close(self) -> None:
        self.closed = True


class FakePower:
    def __init__(self, status: PowerStatus):
        self.status = status
        self.output_calls = []
        self.closed = False

    def get_status(self, channel: int) -> PowerStatus:
        return self.status

    def set_output(
        self,
        channel: int,
        enabled: bool,
        *,
        check_errors: bool = True,
        settle_ms_after_output: int = 0,
    ) -> PowerStatus:
        self.output_calls.append((channel, enabled, check_errors, settle_ms_after_output))
        return self.status

    def close(self) -> None:
        self.closed = True


class SafetyLimitsOutputTests(unittest.TestCase):
    def test_source_output_on_rejects_current_amplitude_over_limit(self):
        fake = FakeSource(source_status(5.0))
        service = SourceService(config=make_config(), logger=CommandLogger())

        with patch.object(service, "_open_source", return_value=fake):
            with self.assertRaisesRegex(ConfigError, "安全上限已超出"):
                service.set_output(channel=2, enabled=True)

        self.assertEqual(fake.output_calls, [])
        self.assertTrue(fake.closed)

    def test_source_output_off_does_not_check_amplitude(self):
        fake = FakeSource(source_status(5.0))
        service = SourceService(config=make_config(), logger=CommandLogger())

        with patch.object(service, "_open_source", return_value=fake):
            service.set_output(channel=2, enabled=False)

        self.assertEqual(fake.output_calls, [(2, False, True)])

    def test_power_output_on_rejects_current_setpoints_over_limit(self):
        fake = FakePower(power_status(12.0, 0.1))
        service = PowerService(config=make_config(), logger=CommandLogger())

        with patch.object(service, "_open_power", return_value=fake):
            with self.assertRaisesRegex(ConfigError, "安全上限已超出"):
                service.set_output(channel=1, enabled=True)

        self.assertEqual(fake.output_calls, [])
        self.assertTrue(fake.closed)

    def test_power_output_off_does_not_check_setpoints(self):
        fake = FakePower(power_status(12.0, 0.5))
        service = PowerService(config=make_config(), logger=CommandLogger())

        with patch.object(service, "_open_power", return_value=fake):
            service.set_output(channel=1, enabled=False)

        self.assertEqual(fake.output_calls, [(1, False, True, 0)])


if __name__ == "__main__":
    unittest.main()
