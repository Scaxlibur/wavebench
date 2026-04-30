import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from wavebench.data.packages import load_run_package
from wavebench.report.html import render_run_report_html, write_run_report_html


class RunReportTests(unittest.TestCase):
    def test_run_report_embeds_capture_screenshot_relative_to_report(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "cap1"
            capture.mkdir(parents=True)
            (capture / "screenshot.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (capture / "metadata.json").write_text(
                json.dumps(
                    {
                        "operation": {"command": "scope capture", "channel": 1},
                        "waveform": {
                            "summary": {
                                "channel": 1,
                                "samples": 10,
                                "frequency_estimate_hz": 10000.0,
                                "voltage_vpp_v": 0.8,
                                "voltage_rms_v": 0.28,
                                "voltage_mean_v": -0.01,
                                "duty_cycle": 0.5,
                                "rise_time_s": 3.2e-8,
                                "fall_time_s": 3.4e-8,
                                "quality_warnings": [],
                            }
                        },
                        "files": {
                            "npy": "data\\raw\\cap1\\ch1.npy",
                            "screenshot": "data\\raw\\cap1\\screenshot.png",
                        },
                    }
                ),
                encoding="utf-8",
            )
            run_dir = root / "data" / "runs" / "run1"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "status": "ok",
                        "steps": [
                            {
                                "index": 3,
                                "kind": "scope.capture",
                                "status": "ok",
                                "artifact": {
                                    "package": "data\\raw\\cap1",
                                    "metadata": "data\\raw\\cap1\\metadata.json",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            output = write_run_report_html(load_run_package(run_dir))

            html = output.read_text(encoding="utf-8")
            self.assertIn("<h2>Screenshots</h2>", html)
            self.assertIn('src="../../raw/cap1/screenshot.png"', html)
            self.assertIn('href="../../raw/cap1/screenshot.png"', html)
            self.assertIn('class="screenshot-thumb"', html)
            self.assertIn("<h2>Signal analysis</h2>", html)
            self.assertIn("10000 Hz", html)
            self.assertIn("0.8 V", html)
            self.assertIn("50%", html)

    def test_run_report_without_screenshot_omits_screenshots_section(self):
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "data" / "runs" / "run1"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({"status": "ok", "steps": [{"index": 0, "kind": "sleep"}]}),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertNotIn("<h2>Screenshots</h2>", html)
            self.assertNotIn("<h2>Signal analysis</h2>", html)
            self.assertIn("<th>Screenshot</th>", html)

    def test_run_report_lists_multi_channel_signal_analysis(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "dual"
            capture.mkdir(parents=True)
            (capture / "metadata.json").write_text(
                json.dumps(
                    {
                        "channels": {
                            "1": {
                                "summary": {
                                    "channel": 1,
                                    "samples": 100,
                                    "frequency_estimate_hz": 1000.0,
                                    "voltage_vpp_v": 1.2,
                                    "voltage_rms_v": 0.4,
                                    "voltage_mean_v": 0.0,
                                    "quality_warnings": ["low_cycles"],
                                }
                            },
                            "2": {
                                "summary": {
                                    "channel": 2,
                                    "samples": 100,
                                    "frequency_estimate_hz": 2000.0,
                                    "voltage_vpp_v": 3.3,
                                    "voltage_rms_v": 1.1,
                                    "voltage_mean_v": 1.65,
                                    "duty_cycle": 0.25,
                                    "quality_warnings": [],
                                }
                            },
                        },
                        "files": {"1": {"npy": "ch1.npy"}, "2": {"npy": "ch2.npy"}},
                    }
                ),
                encoding="utf-8",
            )
            run_dir = root / "data" / "runs" / "run1"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "status": "ok",
                        "steps": [
                            {
                                "index": 0,
                                "kind": "scope.capture",
                                "status": "ok",
                                "artifact": {
                                    "package": "data/raw/dual",
                                    "metadata": "data/raw/dual/metadata.json",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn("<h2>Signal analysis</h2>", html)
            self.assertIn("1000 Hz", html)
            self.assertIn("2000 Hz", html)
            self.assertIn("25%", html)
            self.assertIn("low_cycles", html)


if __name__ == "__main__":
    unittest.main()
