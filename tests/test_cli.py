import unittest

from wavebench.cli import build_parser


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

    def test_capture_accepts_repeated_channels(self):
        args = build_parser().parse_args(["scope", "capture", "--channel", "1", "--channel", "2"])
        self.assertEqual(args.command, "capture")
        self.assertEqual(args.channel, [1, 2])

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
        self.assertTrue(args.no_csv)


if __name__ == "__main__":
    unittest.main()
