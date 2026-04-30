import unittest
import tempfile
from pathlib import Path

from wavebench.config import AutoscaleConfig, ConnectionConfig, OutputConfig, PowerConfig, ScopeConfig, WaveBenchConfig, WaveformConfig, load_config


class ConfigOverrideTests(unittest.TestCase):
    def test_output_overrides_disable_csv_only(self):
        config = WaveBenchConfig(
            connection=ConnectionConfig("lan", "TCPIP::127.0.0.1::INSTR", 100, 100),
            scope=ScopeConfig("rtm2032", None, 1, False, True),
            autoscale=AutoscaleConfig(True, True),
            waveform=WaveformConfig("real", "lsbf", "dmax"),
            output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
            source_path=Path("test.toml"),
        )
        updated = config.with_output_overrides(save_csv=False)
        self.assertFalse(updated.output.save_csv)
        self.assertTrue(updated.output.save_npy)

    def test_waveform_overrides_points_only(self):
        config = WaveBenchConfig(
            connection=ConnectionConfig("lan", "TCPIP::127.0.0.1::INSTR", 100, 100),
            scope=ScopeConfig("rtm2032", None, 1, False, True),
            autoscale=AutoscaleConfig(True, True),
            waveform=WaveformConfig("real", "lsbf", "dmax"),
            output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
            source_path=Path("test.toml"),
        )
        updated = config.with_waveform_overrides(points="def")
        self.assertEqual(updated.waveform.points, "DEF")
        self.assertEqual(updated.waveform.format, "real")

    def test_waveform_overrides_reject_invalid_points(self):
        config = WaveBenchConfig(
            connection=ConnectionConfig("lan", "TCPIP::127.0.0.1::INSTR", 100, 100),
            scope=ScopeConfig("rtm2032", None, 1, False, True),
            autoscale=AutoscaleConfig(True, True),
            waveform=WaveformConfig("real", "lsbf", "dmax"),
            output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
            source_path=Path("test.toml"),
        )
        with self.assertRaises(Exception):
            config.with_waveform_overrides(points="10000")

    def test_waveform_overrides_time_range(self):
        config = WaveBenchConfig(
            connection=ConnectionConfig("lan", "TCPIP::127.0.0.1::INSTR", 100, 100),
            scope=ScopeConfig("rtm2032", None, 1, False, True),
            autoscale=AutoscaleConfig(True, True),
            waveform=WaveformConfig("real", "lsbf", "dmax"),
            output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
            source_path=Path("test.toml"),
        )
        updated = config.with_waveform_overrides(time_range_s=0.01)
        self.assertEqual(updated.waveform.points, "dmax")
        self.assertEqual(updated.waveform.time_range_s, 0.01)

    def test_waveform_overrides_expected_frequency(self):
        config = WaveBenchConfig(
            connection=ConnectionConfig("lan", "TCPIP::127.0.0.1::INSTR", 100, 100),
            scope=ScopeConfig("rtm2032", None, 1, False, True),
            autoscale=AutoscaleConfig(True, True),
            waveform=WaveformConfig("real", "lsbf", "dmax"),
            output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
            source_path=Path("test.toml"),
        )
        updated = config.with_waveform_overrides(expected_frequency_hz=500.0, frequency_tolerance_ratio=0.1)
        self.assertEqual(updated.waveform.expected_frequency_hz, 500.0)
        self.assertEqual(updated.waveform.frequency_tolerance_ratio, 0.1)

    def test_waveform_overrides_target_cycles(self):
        config = WaveBenchConfig(
            connection=ConnectionConfig("lan", "TCPIP::127.0.0.1::INSTR", 100, 100),
            scope=ScopeConfig("rtm2032", None, 1, False, True),
            autoscale=AutoscaleConfig(True, True),
            waveform=WaveformConfig("real", "lsbf", "dmax"),
            output=OutputConfig(Path("data/raw"), "timestamp_label", True, True, True, True, False),
            source_path=Path("test.toml"),
        )
        updated = config.with_waveform_overrides(window_frequency_hz=1000.0, target_cycles=10.0)
        self.assertEqual(updated.waveform.window_frequency_hz, 1000.0)
        self.assertEqual(updated.waveform.target_cycles, 10.0)


if __name__ == "__main__":
    unittest.main()


class SourceConfigTests(unittest.TestCase):
    def test_loads_source_settle_delay(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "wavebench.toml"
            path.write_text("""
[connection]
backend = "lan"
resource = "TCPIP::127.0.0.1::INSTR"
timeout_ms = 1000
opc_timeout_ms = 1000

[scope]
driver = "rtm2032"
default_channel = 1
reset_before_run = false
check_errors = true

[autoscale]
wait_opc = true
check_errors = true

[waveform]
format = "real"
byte_order = "lsbf"
points = "def"

[output]
directory = "data/raw"
package_naming = "timestamp_label"
save_csv = true
save_npy = true
save_json = true
save_commands_log = true
save_screenshot = false

[source]
driver = "dg4202"
resource = "TCPIP::192.168.123.3::INSTR"
default_channel = 2
settle_ms_after_set_frequency = 500
""", encoding="utf-8")
            config = load_config(path)
            self.assertIsNotNone(config.source)
            self.assertEqual(config.source.default_channel, 2)
            self.assertEqual(config.source.settle_ms_after_set_frequency, 500)


class PowerConfigTests(unittest.TestCase):
    def test_loads_power_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "wavebench.toml"
            path.write_text("""
[connection]
backend = "lan"
resource = "TCPIP::127.0.0.1::INSTR"
timeout_ms = 1000
opc_timeout_ms = 1000

[scope]
driver = "rtm2032"
default_channel = 1
reset_before_run = false
check_errors = true

[autoscale]
wait_opc = true
check_errors = true

[waveform]
format = "real"
byte_order = "lsbf"
points = "def"

[output]
directory = "data/raw"
package_naming = "timestamp_label"
save_csv = true
save_npy = true
save_json = true
save_commands_log = true
save_screenshot = false

[power]
driver = "dp800"
resource = "TCPIP::192.168.123.4::INSTR"
default_channel = 1
check_errors = true
""", encoding="utf-8")
            config = load_config(path)
            self.assertIsNotNone(config.power)
            self.assertEqual(config.power.resource, "TCPIP::192.168.123.4::INSTR")
            self.assertEqual(config.power.default_channel, 1)
            updated = config.with_power_resource("TCPIP::192.168.1.50::INSTR")
            self.assertEqual(updated.power.resource, "TCPIP::192.168.1.50::INSTR")
