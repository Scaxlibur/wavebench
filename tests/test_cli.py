import unittest

from wavebench.cli import build_parser


class CliTests(unittest.TestCase):
    def test_capture_accepts_points_and_output_flags(self):
        args = build_parser().parse_args([
            "scope", "capture", "--points", "def", "--time-range", "0.01", "--no-csv", "--label", "x"
        ])
        self.assertEqual(args.command, "capture")
        self.assertEqual(args.points, "def")
        self.assertEqual(args.time_range, 0.01)
        self.assertTrue(args.no_csv)

    def test_fetch_accepts_points(self):
        args = build_parser().parse_args(["scope", "fetch", "--points", "dmax"])
        self.assertEqual(args.command, "fetch")
        self.assertEqual(args.points, "dmax")


if __name__ == "__main__":
    unittest.main()
