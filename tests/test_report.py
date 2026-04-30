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
                        "waveform": {"summary": {"channel": 1, "samples": 10}},
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
            self.assertIn("<th>Screenshot</th>", html)


if __name__ == "__main__":
    unittest.main()
