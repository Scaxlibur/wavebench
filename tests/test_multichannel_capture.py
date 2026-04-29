import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from wavebench.config import AutoscaleConfig, ConnectionConfig, OutputConfig, ScopeConfig, WaveBenchConfig, WaveformConfig
from wavebench.drivers.rtm2032 import WaveformData, WaveformHeader
from wavebench.logging import CommandLogger
from wavebench.services.scope_service import ScopeService


class FakeScope:
    def __init__(self):
        self.closed = False

    def idn(self):
        return "FAKE,SCOPE"

    def capture_waveform(self, *, channel, points, check_errors, time_range_s):
        return WaveformData(
            channel=channel,
            header=WaveformHeader(x_start=0.0, x_stop=0.001, points=3, segment=1),
            voltages_v=np.array([0.0, float(channel), 0.0], dtype=np.float64),
        )

    def close(self):
        self.closed = True


class MultiChannelCaptureTests(unittest.TestCase):
    def test_capture_waveforms_writes_per_channel_files_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = WaveBenchConfig(
                connection=ConnectionConfig(backend="lan", resource="TCPIP::fake::INSTR", timeout_ms=10000, opc_timeout_ms=30000),
                scope=ScopeConfig(driver="rtm2032", model_hint=None, default_channel=1, reset_before_run=False, check_errors=True),
                autoscale=AutoscaleConfig(wait_opc=True, check_errors=True),
                waveform=WaveformConfig(format="real", byte_order="lsbf", points="DEF", time_range_s=0.01),
                output=OutputConfig(directory=Path(tmp), package_naming="timestamp_label", save_csv=False, save_npy=True, save_json=True, save_commands_log=True, save_screenshot=False),
                source_path=Path(tmp) / "wavebench.toml",
            )
            service = ScopeService(config=config, logger=CommandLogger())
            with patch.object(service, "_open_scope", return_value=FakeScope()):
                result = service.capture_waveforms(channels=[1, 2], label="dual")

            self.assertTrue((result.package_dir / "ch1.npy").exists())
            self.assertTrue((result.package_dir / "ch2.npy").exists())
            metadata = json.loads((result.package_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["operation"]["channels"], [1, 2])
            self.assertEqual(metadata["operation"]["trigger_mode"], "sequential_per_channel")
            self.assertIn("1", metadata["channels"])
            self.assertIn("2", metadata["channels"])
            self.assertEqual(metadata["channels"]["1"]["summary"]["channel"], 1)
            self.assertEqual(metadata["channels"]["2"]["summary"]["channel"], 2)
            self.assertIn("npy", metadata["files"]["1"])
            self.assertIn("npy", metadata["files"]["2"])


if __name__ == "__main__":
    unittest.main()
