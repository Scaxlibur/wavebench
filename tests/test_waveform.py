import unittest

from wavebench.drivers.rtm2032 import parse_waveform_header
from wavebench.errors import DataError


class WaveformHeaderTests(unittest.TestCase):
    def test_parse_waveform_header_real_format(self):
        header = parse_waveform_header("-1.0000E-03,9.9980E-04,10000,1")
        self.assertAlmostEqual(header.x_start, -1.0e-3)
        self.assertAlmostEqual(header.x_stop, 9.9980e-4)
        self.assertEqual(header.points, 10000)
        self.assertEqual(header.segment, 1)
        self.assertAlmostEqual(header.x_increment, 2.0e-7)

    def test_parse_waveform_header_rejects_invalid_response(self):
        with self.assertRaises(DataError):
            parse_waveform_header("not,a,header")


if __name__ == "__main__":
    unittest.main()
