import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from wavebench.data.packages import load_run_package
from wavebench.report.html import render_run_report_html, write_run_report_html


class RunReportTests(unittest.TestCase):
    def test_run_report_embeds_capture_screenshot_relative_to_report(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "cap1"
            capture.mkdir(parents=True)
            (capture / "screenshot.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            np.save(capture / "ch1.npy", np.array([[0.0, 0.0], [0.5e-3, 1.0], [1.0e-3, 0.0]]))
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
            self.assertIn("<h2>Summary</h2>", html)
            self.assertIn('<div class="label">Status</div><div class="value ok">ok</div>', html)
            self.assertIn('<div class="label">Captures</div><div class="value">1</div>', html)
            self.assertIn('<div class="label">Screenshots</div><div class="value">1</div>', html)
            self.assertIn('<div class="label">Primary frequency</div><div class="value">10000 Hz</div>', html)
            self.assertIn('<div class="label">Primary Vpp</div><div class="value">0.8 V</div>', html)
            self.assertIn("<h2>Screenshots</h2>", html)
            self.assertIn('src="../../raw/cap1/screenshot.png"', html)
            self.assertIn('href="../../raw/cap1/screenshot.png"', html)
            self.assertIn('class="screenshot-thumb"', html)
            self.assertIn("<h2>Signal analysis</h2>", html)
            self.assertIn("10000 Hz", html)
            self.assertIn("0.8 V", html)
            self.assertIn("50%", html)
            self.assertIn("<h2>Waveform previews</h2>", html)
            self.assertIn("Step 3 ch1", html)
            self.assertIn("<polyline", html)
            manifest = json.loads((run_dir / "report-assets" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "wavebench.report_manifest.v1")
            self.assertEqual(manifest["report"], "report.html")
            self.assertEqual(manifest["run_json"], "run.json")
            self.assertEqual(manifest["capture_packages"][0]["package"], "data\\raw\\cap1")
            self.assertEqual(manifest["screenshots"][0]["path"], "../../raw/cap1/screenshot.png")
            self.assertEqual(manifest["waveform_previews"][0]["source_npy"], "../../raw/cap1/ch1.npy")
            self.assertEqual(manifest["warnings"], [])

    def test_run_report_without_screenshot_omits_screenshots_section(self):
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "data" / "runs" / "run1"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({"status": "ok", "steps": [{"index": 0, "kind": "sleep"}]}),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn("<h2>Summary</h2>", html)
            self.assertIn('<div class="label">Steps</div><div class="value">1</div>', html)
            self.assertIn('<div class="label">Captures</div><div class="value">0</div>', html)
            self.assertNotIn("<h2>Screenshots</h2>", html)
            self.assertNotIn("<h2>Signal analysis</h2>", html)
            self.assertIn("<th>Screenshot</th>", html)

    def test_run_report_summary_counts_failed_expectations_and_warnings(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "cap1"
            capture.mkdir(parents=True)
            (capture / "metadata.json").write_text(
                json.dumps(
                    {
                        "waveform": {
                            "summary": {
                                "channel": 1,
                                "samples": 20,
                                "frequency_estimate_hz": 1000.0,
                                "voltage_vpp_v": 0.01,
                                "quality_warnings": ["low_signal_amplitude"],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            run_dir = root / "data" / "runs" / "run_failed"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "status": "failed",
                        "experiment": {"label": "bad_run"},
                        "restore": {"status": "ok"},
                        "steps": [
                            {
                                "index": 0,
                                "kind": "scope.capture",
                                "status": "failed",
                                "artifact": {
                                    "package": "data/raw/cap1",
                                    "metadata": "data/raw/cap1/metadata.json",
                                    "quality": {"warnings": ["low_signal_amplitude"]},
                                    "expect": {
                                        "status": "failed",
                                        "checks": {
                                            "voltage_vpp_v": {
                                                "status": "failed",
                                                "value": 0.01,
                                                "limits": {"min": 0.05},
                                            }
                                        },
                                        "failures": ["voltage_vpp_v: 0.01 below min 0.05"],
                                    },
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn('<div class="label">Status</div><div class="value failed">failed</div>', html)
            self.assertIn('<div class="label">Failed steps</div><div class="value failed">1</div>', html)
            self.assertIn('<div class="label">Warnings</div><div class="value warning">1</div>', html)
            self.assertIn('<div class="label">Expect failed</div><div class="value failed">1</div>', html)
            self.assertIn('<div class="label">Restore</div><div class="value">ok</div>', html)

    def test_run_report_lists_multi_channel_signal_analysis(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "dual"
            capture.mkdir(parents=True)
            np.save(capture / "ch1.npy", np.array([[0.0, 0.0], [1e-3, 1.0], [2e-3, 0.0]]))
            np.save(capture / "ch2.npy", np.array([[0.0, 1.65], [1e-3, 3.3], [2e-3, 1.65]]))
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
            self.assertIn("Step 0 ch1", html)
            self.assertIn("Step 0 ch2", html)

    def test_run_report_keeps_running_when_waveform_preview_fails(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "bad_waveform"
            capture.mkdir(parents=True)
            (capture / "metadata.json").write_text(
                json.dumps(
                    {
                        "waveform": {"summary": {"channel": 1, "frequency_estimate_hz": 1000.0}},
                        "files": {"npy": "data/raw/bad_waveform/missing.npy"},
                    }
                ),
                encoding="utf-8",
            )
            run_dir = root / "data" / "runs" / "run_bad_waveform"
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
                                    "package": "data/raw/bad_waveform",
                                    "metadata": "data/raw/bad_waveform/metadata.json",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            output = write_run_report_html(load_run_package(run_dir))
            html = output.read_text(encoding="utf-8")

            self.assertIn("<h2>Waveform previews</h2>", html)
            self.assertIn("waveform preview unavailable", html)
            self.assertIn("FileNotFoundError", html)
            manifest = json.loads((run_dir / "report-assets" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["waveform_previews"][0]["exists"], False)
            self.assertIn("waveform npy missing", manifest["warnings"][0])

    def test_run_report_renders_expected_vs_measured_table(self):
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "data" / "runs" / "run_expect"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "status": "failed",
                        "steps": [
                            {
                                "index": 7,
                                "kind": "scope.capture",
                                "status": "failed",
                                "artifact": {
                                    "expect": {
                                        "status": "failed",
                                        "checks": {
                                            "frequency_estimate_hz": {
                                                "status": "ok",
                                                "value": 10000.0,
                                                "limits": {"min": 9500.0, "max": 10500.0},
                                            },
                                            "voltage_vpp_v": {
                                                "status": "failed",
                                                "value": 0.01,
                                                "limits": {"min": 0.05},
                                                "reasons": ["below min 0.05"],
                                            },
                                            "duty_cycle": {
                                                "status": "failed",
                                                "reason": "unavailable",
                                                "limits": {"min": 0.49, "max": 0.51},
                                            },
                                            "frequency_error_ratio": {
                                                "status": "failed",
                                                "value": "nan-ish",
                                                "reason": "not_numeric",
                                                "limits": {"max": 0.02},
                                            },
                                        },
                                        "failures": [
                                            "voltage_vpp_v: 0.01 below min 0.05",
                                            "duty_cycle: unavailable",
                                            "frequency_error_ratio: not numeric",
                                        ],
                                    }
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn("<h2>Expected vs measured</h2>", html)
            self.assertIn("<td>frequency_estimate_hz</td>", html)
            self.assertIn("<td>9500..10500</td>", html)
            self.assertIn("<td>10000</td>", html)
            self.assertIn("<td>&gt;= 0.05</td>", html)
            self.assertIn("<td>below min 0.05</td>", html)
            self.assertIn("<td>unavailable</td>", html)
            self.assertIn("<td>not_numeric</td>", html)
            self.assertIn('<tr class="failed"><td>7</td><td>scope.capture</td><td>voltage_vpp_v</td>', html)

    def test_run_report_omits_expected_vs_measured_without_expect_checks(self):
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "data" / "runs" / "run_no_expect"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({"status": "ok", "steps": [{"index": 0, "kind": "sleep", "status": "ok"}]}),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertNotIn("<h2>Expected vs measured</h2>", html)


if __name__ == "__main__":
    unittest.main()
