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


if __name__ == "__main__":
    unittest.main()
