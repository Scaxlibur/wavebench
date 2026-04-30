import unittest

from wavebench.data.package import safe_label


class PackageTests(unittest.TestCase):
    def test_safe_label_keeps_simple_names(self):
        self.assertEqual(safe_label("ch1"), "ch1")

    def test_safe_label_replaces_spaces(self):
        self.assertEqual(safe_label("my capture"), "my_capture")


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import json
import tempfile
from unittest.mock import patch

import numpy as np

from wavebench.config import AutoscaleConfig, ConnectionConfig, OutputConfig, ScopeConfig, WaveBenchConfig, WaveformConfig
from wavebench.drivers.rtm2032 import WaveformData, WaveformHeader
from wavebench.logging import CommandLogger
from wavebench.services.scope_service import ScopeService


class ScreenshotScope:
    def idn(self):
        return "FAKE,SCOPE"

    def capture_waveform(self, *, channel, points, check_errors, time_range_s):
        return WaveformData(
            channel=channel,
            header=WaveformHeader(x_start=0.0, x_stop=0.001, points=3, segment=1),
            voltages_v=np.array([0.0, 1.0, 0.0], dtype=np.float64),
        )

    def screenshot_png(self, *, include_menu=False, color_scheme="COL"):
        return b"\x89PNG\r\n\x1a\nfake"

    def close(self):
        pass


class ScreenshotCaptureTests(unittest.TestCase):
    def test_capture_waveform_writes_screenshot_when_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = WaveBenchConfig(
                connection=ConnectionConfig(backend="lan", resource="TCPIP::fake::INSTR", timeout_ms=10000, opc_timeout_ms=30000),
                scope=ScopeConfig(driver="rtm2032", model_hint=None, default_channel=1, reset_before_run=False, check_errors=True),
                autoscale=AutoscaleConfig(wait_opc=True, check_errors=True),
                waveform=WaveformConfig(format="real", byte_order="lsbf", points="DEF"),
                output=OutputConfig(directory=Path(tmp), package_naming="timestamp_label", save_csv=False, save_npy=True, save_json=True, save_commands_log=True, save_screenshot=True),
                source_path=Path(tmp) / "wavebench.toml",
            )
            service = ScopeService(config=config, logger=CommandLogger())
            with patch.object(service, "_open_scope", return_value=ScreenshotScope()):
                result = service.capture_waveform(channel=1, label="with_screen")

            self.assertIsNotNone(result.screenshot_path)
            self.assertTrue(result.screenshot_path.exists())
            self.assertEqual(result.screenshot_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            metadata = json.loads((result.package_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["files"]["screenshot"], str(result.screenshot_path))
