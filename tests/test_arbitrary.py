import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from wavebench.arbitrary import load_arbitrary_waveform, normalize_peak, normalized_to_dac14
from wavebench.errors import DataError


class ArbitraryWaveformTests(unittest.TestCase):
    def test_loads_npy_vector_and_builds_normalized_payload(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "waveform.npy"
            np.save(path, np.array([-2.0, 0.0, 2.0]))

            waveform = load_arbitrary_waveform(path)

            self.assertEqual(waveform.points, 3)
            np.testing.assert_allclose(waveform.normalized, [-1.0, 0.0, 1.0])
            self.assertEqual(waveform.dac14.tolist(), [0, 8192, 16383])
            self.assertIsNone(waveform.sample_rate_hz)

    def test_loads_csv_time_value_and_infers_sample_rate(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "waveform.csv"
            path.write_text("0,0\n0.001,1\n0.002,0\n", encoding="utf-8")

            waveform = load_arbitrary_waveform(path)

            self.assertEqual(waveform.points, 3)
            self.assertAlmostEqual(waveform.sample_rate_hz, 1000.0)
            self.assertTrue(waveform.summary()["has_time_axis"])

    def test_rejects_nan_samples(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "waveform.npy"
            np.save(path, np.array([0.0, np.nan, 1.0]))

            with self.assertRaises(DataError):
                load_arbitrary_waveform(path)

    def test_rejects_too_many_points_when_limit_is_set(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "waveform.npy"
            np.save(path, np.arange(5, dtype=float))

            with self.assertRaises(DataError):
                load_arbitrary_waveform(path, max_points=4)

    def test_rejects_non_uniform_time_axis(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "waveform.csv"
            path.write_text("0,0\n0.001,1\n0.003,0\n", encoding="utf-8")

            with self.assertRaises(DataError):
                load_arbitrary_waveform(path)

    def test_normalize_peak_leaves_unit_range_unchanged(self):
        np.testing.assert_allclose(normalize_peak(np.array([-0.5, 0.25])), [-0.5, 0.25])

    def test_dac14_rejects_out_of_range_normalized_values(self):
        with self.assertRaises(DataError):
            normalized_to_dac14(np.array([-1.1, 0.0, 1.0]))


if __name__ == "__main__":
    unittest.main()
