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
            self.assertIn("<h2>摘要 / Summary</h2>", html)
            self.assertIn('<div class="label">状态 / Status</div><div class="value ok">ok</div>', html)
            self.assertIn('<div class="label">采集 / Captures</div><div class="value">1</div>', html)
            self.assertIn('<div class="label">截图 / Screenshots</div><div class="value">1</div>', html)
            self.assertIn('<div class="label">主频率 / Primary frequency</div><div class="value">10000 Hz</div>', html)
            self.assertIn('<div class="label">主峰峰值 / Primary Vpp</div><div class="value">0.8 V</div>', html)
            self.assertIn("<h2>截图 / Screenshots</h2>", html)
            self.assertIn('src="../../raw/cap1/screenshot.png"', html)
            self.assertIn('href="../../raw/cap1/screenshot.png"', html)
            self.assertIn('class="screenshot-thumb"', html)
            self.assertIn("<h2>信号分析 / Signal analysis</h2>", html)
            self.assertIn("10000 Hz", html)
            self.assertIn("0.8 V", html)
            self.assertIn("50%", html)
            self.assertIn("<h2>波形预览 / Waveform previews</h2>", html)
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

            self.assertIn("<h2>摘要 / Summary</h2>", html)
            self.assertIn('<div class="label">步骤 / Steps</div><div class="value">1</div>', html)
            self.assertIn('<div class="label">采集 / Captures</div><div class="value">0</div>', html)
            self.assertNotIn("<h2>截图 / Screenshots</h2>", html)
            self.assertNotIn("<h2>信号分析 / Signal analysis</h2>", html)
            self.assertIn("<th>截图 / Screenshot</th>", html)

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

            self.assertIn('<div class="label">状态 / Status</div><div class="value failed">failed</div>', html)
            self.assertIn('<div class="label">失败步骤 / Failed steps</div><div class="value failed">1</div>', html)
            self.assertIn('<div class="label">警告 / Warnings</div><div class="value warning">1</div>', html)
            self.assertIn('<div class="label">预期失败 / Expect failed</div><div class="value failed">1</div>', html)
            self.assertIn('<div class="label">恢复 / Restore</div><div class="value">ok</div>', html)

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

            self.assertIn("<h2>信号分析 / Signal analysis</h2>", html)
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

            self.assertIn("<h2>波形预览 / Waveform previews</h2>", html)
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
                                    },
                                    "expect_fft": {
                                        "status": "ok",
                                        "checks": {
                                            "peak_frequency_hz": {
                                                "status": "ok",
                                                "value": 1000.0,
                                                "limits": {"min": 990.0, "max": 1010.0},
                                            },
                                            "harmonic_2_amplitude_v": {
                                                "status": "ok",
                                                "value": 0.1,
                                                "limits": {"max": 0.2},
                                            },
                                        },
                                        "failures": [],
                                    },
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn("<h2>验收摘要 / Acceptance summary</h2>", html)
            self.assertIn("频率 / Frequency", html)
            self.assertIn("峰峰值 / Vpp", html)
            self.assertIn("占空比 / Duty", html)
            self.assertIn("频率误差 / Frequency error", html)
            self.assertIn("<h2>预期 vs 实测 / Expected vs measured</h2>", html)
            self.assertIn("<td>frequency_estimate_hz</td>", html)
            self.assertIn("<td>9500..10500</td>", html)
            self.assertIn("<td>10000</td>", html)
            self.assertIn("<td>&gt;= 0.05</td>", html)
            self.assertIn("<td>below min 0.05</td>", html)
            self.assertIn("<td>unavailable</td>", html)
            self.assertIn("<td>not_numeric</td>", html)
            self.assertIn('<tr class="failed"><td>7</td><td>scope.capture</td><td>voltage_vpp_v</td>', html)
            self.assertIn("FFT 主频 / FFT peak", html)
            self.assertIn("FFT H2 幅度 / FFT H2 amplitude", html)
            self.assertIn("<td>fft.peak_frequency_hz</td>", html)
            self.assertIn("<td>fft.harmonic_2_amplitude_v</td>", html)

    def test_run_report_renders_dmm_reading_cards(self):
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "data" / "runs" / "run_dmm"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "status": "ok",
                        "steps": [
                            {
                                "index": 6,
                                "kind": "dmm.read",
                                "status": "ok",
                                "fields": {"function": "acv"},
                                "artifact": {
                                    "dmm_reading": {
                                        "function": "acv",
                                        "value": 0.3535,
                                        "unit": "V",
                                        "raw": "3.535000E-01",
                                    },
                                    "expect": {
                                        "status": "ok",
                                        "checks": {
                                            "value": {
                                                "status": "ok",
                                                "value": 0.3535,
                                                "limits": {"min": 0.34, "max": 0.37},
                                            }
                                        },
                                        "failures": [],
                                    },
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn("<h2>DMM 读数 / DMM readings</h2>", html)
            self.assertIn('<article class="card dmm-card">', html)
            self.assertIn("<header><h3>dmm.read</h3><span class=\"badge ok\">ok</span></header>", html)
            self.assertIn('<p class="reading">0.3535<span class="unit">V</span></p>', html)
            self.assertIn("<div><dt>功能 / Function</dt><dd>acv</dd></div>", html)
            self.assertIn("<div><dt>步骤 / Step</dt><dd>6 · dmm.read</dd></div>", html)
            self.assertIn("<div><dt>预期 / Expected</dt><dd>0.34..0.37 V</dd></div>", html)
            self.assertIn('<tr class="ok"><td>6</td><td>dmm.read</td><td>value</td>', html)

    def test_run_report_renders_evidence_summary(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "evidence"
            capture.mkdir(parents=True)
            np.save(capture / "ch1.npy", np.array([[0.0, 0.0], [1e-3, 1.0], [2e-3, 0.0]]))
            (capture / "screenshot.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (capture / "metadata.json").write_text(
                json.dumps(
                    {
                        "operation": {"command": "scope capture", "channel": 1},
                        "waveform": {
                            "summary": {
                                "channel": 1,
                                "samples": 3,
                                "frequency_estimate_hz": 1000.0,
                                "voltage_vpp_v": 1.0,
                                "quality_warnings": [],
                            }
                        },
                        "files": {
                            "npy": "data/raw/evidence/ch1.npy",
                            "screenshot": "data/raw/evidence/screenshot.png",
                        },
                    }
                ),
                encoding="utf-8",
            )
            run_dir = root / "data" / "runs" / "run_evidence"
            run_dir.mkdir(parents=True)
            (run_dir / "summary.csv").write_text(
                "index,kind,status\n0,source.set_freq,ok\n1,scope.capture,failed\n2,dmm.read,ok\n3,sleep,ok\n",
                encoding="utf-8",
            )
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "status": "failed",
                        "steps": [
                            {
                                "index": 0,
                                "kind": "source.set_freq",
                                "status": "ok",
                                "fields": {"channel": 1, "frequency_hz": 1000.0},
                                "artifact": {"source_status": {"channel": 1, "frequency_hz": 1000.0}},
                            },
                            {
                                "index": 1,
                                "kind": "scope.capture",
                                "status": "failed",
                                "artifact": {
                                    "package": "data/raw/evidence",
                                    "metadata": "data/raw/evidence/metadata.json",
                                    "expect": {
                                        "status": "failed",
                                        "checks": {
                                            "voltage_vpp_v": {
                                                "status": "failed",
                                                "value": 1.0,
                                                "limits": {"min": 2.0},
                                            }
                                        },
                                        "failures": ["voltage_vpp_v below min"],
                                    },
                                },
                            },
                            {
                                "index": 2,
                                "kind": "dmm.read",
                                "status": "ok",
                                "artifact": {
                                    "dmm_reading": {"function": "dcv", "value": 3.3, "unit": "V"},
                                    "expect": {
                                        "status": "ok",
                                        "checks": {
                                            "value": {
                                                "status": "ok",
                                                "value": 3.3,
                                                "limits": {"min": 3.2, "max": 3.4},
                                            }
                                        },
                                    },
                                },
                            },
                            {
                                "index": 3,
                                "kind": "sleep",
                                "status": "ok",
                                "fields": {"duration_s": 0.25},
                                "artifact": {"duration_s": 0.25},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertIn("<h2>实验证据摘要 / Run evidence summary</h2>", html)
            self.assertIn("<td>信号源设置步骤 / Source setting steps</td><td>1</td>", html)
            self.assertIn("<td>示波器采集步骤 / Scope capture steps</td><td>1</td>", html)
            self.assertIn("<td>DMM 读数 / DMM readings</td><td>1</td>", html)
            self.assertIn('<td>失败预期项 / Failed expectations</td><td class="failed">1</td>', html)
            self.assertIn('<td>run.json</td><td class="ok">存在 / present</td>', html)
            self.assertIn('<td>summary.csv</td><td class="ok">存在 / present</td>', html)
            self.assertIn("<td>采集包 / Capture packages</td><td>1</td>", html)
            self.assertIn("<td>截图 / Screenshots</td><td>1</td>", html)
            self.assertIn("<td>波形预览 / Waveform previews</td><td>1</td>", html)
            self.assertIn("<h2>证据时间线 / Evidence timeline</h2>", html)
            self.assertIn("<th>证据 / Evidence</th>", html)
            self.assertIn("<td>0</td><td>source.set_freq</td><td><span class=\"badge ok\">ok</span></td>", html)
            self.assertIn("信号源 / Source; 通道 / Channel: 1; 频率 / Frequency: 1000 Hz", html)
            self.assertIn("<td>1</td><td>scope.capture</td><td><span class=\"badge failed\">failed</span></td>", html)
            self.assertIn(
                "示波器 / Scope; 采集包 / Package: data/raw/evidence; 截图 / Screenshot: 存在 / present",
                html,
            )
            self.assertIn("预期 / Expect: failed", html)
            self.assertIn("<td>2</td><td>dmm.read</td><td><span class=\"badge ok\">ok</span></td>", html)
            self.assertIn("DMM; 功能 / Function: dcv; 读数 / Reading: 3.3 V; 预期 / Expect: ok", html)
            self.assertIn("<td>3</td><td>sleep</td><td><span class=\"badge ok\">ok</span></td>", html)
            self.assertIn("等待 / Sleep; 时长 / Duration: 0.25 s", html)
            self.assertIn("<h2>产物链接 / Artifact links</h2>", html)
            self.assertIn('<td>运行记录 / Run JSON</td><td>run.json</td><td><a href="run.json">run.json</a></td>', html)
            self.assertIn(
                '<td>摘要 CSV / Summary CSV</td><td>summary.csv</td><td><a href="summary.csv">summary.csv</a></td>',
                html,
            )
            self.assertIn(
                '<td>采集包 / Capture package</td><td>data/raw/evidence</td>'
                '<td><a href="../../raw/evidence">../../raw/evidence</a></td>',
                html,
            )
            self.assertIn(
                '<td>截图 / Screenshot</td><td>screenshot.png</td>'
                '<td><a href="../../raw/evidence/screenshot.png">../../raw/evidence/screenshot.png</a></td>',
                html,
            )
            self.assertIn(
                '<td>波形原始数据 / Waveform raw artifact</td><td>ch1 ch1.npy</td>'
                '<td><a href="../../raw/evidence/ch1.npy">../../raw/evidence/ch1.npy</a></td>',
                html,
            )

    def test_run_report_omits_expected_vs_measured_without_expect_checks(self):
        with TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "data" / "runs" / "run_no_expect"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({"status": "ok", "steps": [{"index": 0, "kind": "sleep", "status": "ok"}]}),
                encoding="utf-8",
            )

            html = render_run_report_html(load_run_package(run_dir), output_dir=run_dir)

            self.assertNotIn("<h2>验收摘要 / Acceptance summary</h2>", html)
            self.assertNotIn("<h2>预期 vs 实测 / Expected vs measured</h2>", html)


if __name__ == "__main__":
    unittest.main()
