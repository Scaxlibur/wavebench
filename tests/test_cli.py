import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from wavebench.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_capture_accepts_points_and_output_flags(self):
        args = build_parser().parse_args([
            "scope", "capture", "--points", "def", "--time-range", "0.01", "--window-frequency", "500", "--target-cycles", "10", "--expect-frequency", "500", "--frequency-tolerance", "0.1", "--no-csv", "--label", "x"
        ])
        self.assertEqual(args.command, "capture")
        self.assertEqual(args.points, "def")
        self.assertEqual(args.time_range, 0.01)
        self.assertEqual(args.window_frequency, 500.0)
        self.assertEqual(args.expect_frequency, 500.0)
        self.assertEqual(args.target_cycles, 10.0)
        self.assertEqual(args.frequency_tolerance, 0.1)
        self.assertTrue(args.no_csv)

    def test_capture_accepts_screenshot_flag(self):
        args = build_parser().parse_args(["scope", "capture", "--screenshot"])
        self.assertEqual(args.command, "capture")
        self.assertTrue(args.screenshot)

    def test_capture_accepts_repeated_channels(self):
        args = build_parser().parse_args(["scope", "capture", "--channel", "1", "--channel", "2"])
        self.assertEqual(args.command, "capture")
        self.assertEqual(args.channel, [1, 2])

    def test_power_status_accepts_channel(self):
        args = build_parser().parse_args(["power", "status", "--channel", "1"])
        self.assertEqual(args.domain, "power")
        self.assertEqual(args.command, "status")
        self.assertEqual(args.channel, 1)

    def test_power_set_accepts_voltage_and_current_limit(self):
        args = build_parser().parse_args([
            "power", "set", "--channel", "1", "--voltage", "3.3", "--current-limit", "0.2"
        ])
        self.assertEqual(args.domain, "power")
        self.assertEqual(args.command, "set")
        self.assertEqual(args.channel, 1)
        self.assertEqual(args.voltage, 3.3)
        self.assertEqual(args.current_limit, 0.2)

    def test_power_output_accepts_on_off(self):
        args = build_parser().parse_args(["power", "output", "--channel", "1", "off"])
        self.assertEqual(args.domain, "power")
        self.assertEqual(args.command, "output")
        self.assertEqual(args.channel, 1)
        self.assertEqual(args.state, "off")

    def test_source_status_accepts_channel(self):
        args = build_parser().parse_args(["source", "status", "--channel", "2"])
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "status")
        self.assertEqual(args.channel, 2)

    def test_source_set_freq_accepts_value(self):
        args = build_parser().parse_args(["source", "set-freq", "--channel", "2", "1000"])
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "set-freq")
        self.assertEqual(args.channel, 2)
        self.assertEqual(args.value_hz, 1000.0)

    def test_fetch_accepts_points(self):
        args = build_parser().parse_args(["scope", "fetch", "--points", "dmax"])
        self.assertEqual(args.command, "fetch")
        self.assertEqual(args.points, "dmax")
    def test_source_set_func_accepts_function(self):
        args = build_parser().parse_args(["source", "set-func", "--channel", "2", "squ"])
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "set-func")
        self.assertEqual(args.channel, 2)
        self.assertEqual(args.function, "squ")

    def test_source_set_vpp_accepts_value(self):
        args = build_parser().parse_args(["source", "set-vpp", "--channel", "2", "3.3"])
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "set-vpp")
        self.assertEqual(args.channel, 2)
        self.assertEqual(args.value_vpp, 3.3)


    def test_source_set_duty_accepts_percent(self):
        args = build_parser().parse_args(["source", "set-duty", "--channel", "2", "25"] )
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "set-duty")
        self.assertEqual(args.channel, 2)
        self.assertEqual(args.duty_percent, 25.0)




    def test_source_arb_probe_accepts_channel(self):
        args = build_parser().parse_args(["source", "arb-probe", "--channel", "2", "--probe-timeout-ms", "700"])
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "arb-probe")
        self.assertEqual(args.channel, 2)
        self.assertEqual(args.probe_timeout_ms, 700)

    def test_source_arb_load_accepts_dry_run_options(self):
        args = build_parser().parse_args([
            "source", "arb-load",
            "--channel", "2",
            "--file", "waveform.npy",
            "--name", "REI_ARB",
            "--amplitude", "1.0",
            "--offset", "0.0",
            "--sample-rate", "1000",
            "--max-points", "16384",
            "--output-on",
            "--export-payload", "payload.json",
            "--dry-run",
        ])
        self.assertEqual(args.domain, "source")
        self.assertEqual(args.command, "arb-load")
        self.assertEqual(args.channel, 2)
        self.assertEqual(args.file, "waveform.npy")
        self.assertEqual(args.name, "REI_ARB")
        self.assertEqual(args.amplitude, 1.0)
        self.assertEqual(args.offset, 0.0)
        self.assertEqual(args.sample_rate, 1000.0)
        self.assertEqual(args.max_points, 16384)
        self.assertTrue(args.output_on)
        self.assertEqual(args.export_payload, "payload.json")
        self.assertTrue(args.dry_run)

    def test_source_arb_load_dry_run_prints_payload_summary(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "waveform.npy"
            payload = root / "payload.json"
            np.save(path, np.array([-1.0, 0.0, 1.0]))
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                status = main([
                    "source", "arb-load",
                    "--channel", "2",
                    "--file", str(path),
                    "--name", "REI_ARB",
                    "--amplitude", "1.0",
                    "--offset", "0.0",
                    "--export-payload", str(payload),
                    "--dry-run",
                ])

            output = stdout.getvalue()
            self.assertEqual(status, 0)
            self.assertIn("arb_name=REI_ARB", output)
            self.assertIn("channel=2", output)
            self.assertIn("points=3", output)
            self.assertIn("dac14=0..16383", output)
            self.assertIn(f"payload={payload}", output)
            self.assertIn("dry_run=true", output)
            self.assertIn("upload=blocked_until_dg4202_scpi_is_confirmed", output)
            self.assertIn('"format": "wavebench.arbitrary.v1"', payload.read_text(encoding="utf-8"))

    def test_sweep_discrete_accepts_frequencies_and_channels(self):
        args = build_parser().parse_args([
            "sweep", "discrete",
            "--source-channel", "2",
            "--scope-channel", "1",
            "--source-resource", "TCPIP::192.168.123.3::INSTR",
            "--frequencies", "1000,2000,5000",
            "--target-cycles", "8",
            "--frequency-tolerance", "0.02",
            "--source-func", "sin",
            "--source-vpp", "3.3",
            "--restore-source-state",
            "--no-csv",
        ])
        self.assertEqual(args.domain, "sweep")
        self.assertEqual(args.command, "discrete")
        self.assertEqual(args.source_channel, 2)
        self.assertEqual(args.scope_channel, 1)
        self.assertEqual(args.source_resource, "TCPIP::192.168.123.3::INSTR")
        self.assertEqual(args.frequencies, "1000,2000,5000")
        self.assertEqual(args.target_cycles, 8.0)
        self.assertEqual(args.frequency_tolerance, 0.02)
        self.assertEqual(args.source_func, "sin")
        self.assertEqual(args.source_vpp, 3.3)
        self.assertTrue(args.restore_source_state)
        self.assertTrue(args.no_csv)

    def test_run_check_accepts_plan_and_config(self):
        args = build_parser().parse_args([
            "run", "check", "--config", "wavebench.toml", "--plan", "plans/example.toml"
        ])
        self.assertEqual(args.domain, "run")
        self.assertEqual(args.command, "check")
        self.assertEqual(args.config, "wavebench.toml")
        self.assertEqual(args.plan, "plans/example.toml")


    def test_run_schema_accepts_no_plan(self):
        args = build_parser().parse_args(["run", "schema"])
        self.assertEqual(args.domain, "run")
        self.assertEqual(args.command, "schema")

    def test_run_plan_accepts_plan_and_config(self):
        args = build_parser().parse_args([
            "run", "plan", "--config", "wavebench.toml", "--plan", "plans/example.toml"
        ])
        self.assertEqual(args.domain, "run")
        self.assertEqual(args.command, "plan")
        self.assertEqual(args.config, "wavebench.toml")
        self.assertEqual(args.plan, "plans/example.toml")


    def test_capture_inspect_accepts_path(self):
        args = build_parser().parse_args(["capture", "inspect", "data/raw/example"])
        self.assertEqual(args.domain, "capture")
        self.assertEqual(args.command, "inspect")
        self.assertEqual(args.path, "data/raw/example")

    def test_capture_inspect_accepts_fft(self):
        args = build_parser().parse_args(["capture", "inspect", "data/raw/example", "--fft"])
        self.assertEqual(args.domain, "capture")
        self.assertEqual(args.command, "inspect")
        self.assertTrue(args.fft)

    def test_capture_inspect_fft_prints_spectrum_summary(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "data" / "raw" / "fft_cap"
            capture.mkdir(parents=True)
            sample_rate = 1000.0
            samples = 1000
            time_s = np.arange(samples) / sample_rate
            voltage_v = np.sin(2 * np.pi * 50.0 * time_s)
            np.save(capture / "ch1.npy", np.column_stack((time_s, voltage_v)))
            (capture / "metadata.json").write_text(
                json.dumps(
                    {
                        "operation": {"command": "scope capture", "channel": 1},
                        "waveform": {
                            "summary": {
                                "channel": 1,
                                "samples": samples,
                                "x_increment_s": 1.0 / sample_rate,
                            }
                        },
                        "files": {"npy": "data/raw/fft_cap/ch1.npy"},
                    }
                ),
                encoding="utf-8",
            )
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                status = main(["capture", "inspect", str(capture), "--fft"])

            output = stdout.getvalue()
            self.assertEqual(status, 0)
            self.assertIn("FFT", output)
            self.assertIn("CH1", output)
            self.assertIn("window=hann", output)
            self.assertIn("sample_rate≈1000 Hz", output)
            self.assertIn("resolution≈1 Hz", output)
            self.assertIn("peak_frequency≈50 Hz", output)
            self.assertIn("noise_floor≈", output)

    def test_run_report_accepts_path_and_output(self):
        args = build_parser().parse_args(["run", "report", "data/runs/example", "--output", "report.html"])
        self.assertEqual(args.domain, "run")
        self.assertEqual(args.command, "report")
        self.assertEqual(args.path, "data/runs/example")
        self.assertEqual(args.output, "report.html")


if __name__ == "__main__":
    unittest.main()
