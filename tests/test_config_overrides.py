import unittest
from pathlib import Path

from wavebench.config import AutoscaleConfig, ConnectionConfig, OutputConfig, ScopeConfig, WaveBenchConfig, WaveformConfig


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


if __name__ == "__main__":
    unittest.main()
