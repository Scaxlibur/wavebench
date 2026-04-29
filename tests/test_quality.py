import unittest

import numpy as np

from wavebench.data.quality import estimate_frequency_fft, estimate_frequency_hysteresis, summarize_waveform


class QualityTests(unittest.TestCase):
    def test_estimates_sine_frequency_with_hysteresis(self):
        times = np.linspace(0.0, 0.01, 10000, endpoint=False)
        voltages = 2.5 * np.sin(2 * np.pi * 1000.0 * times)
        self.assertAlmostEqual(estimate_frequency_hysteresis(times, voltages), 1000.0, delta=2.0)

    def test_estimates_sine_frequency_with_fft(self):
        times = np.linspace(-0.001, 0.001, 10000, endpoint=False)
        voltages = 2.5 * np.sin(2 * np.pi * 1000.0 * times)
        self.assertAlmostEqual(estimate_frequency_fft(times, voltages), 1000.0, delta=5.0)

    def test_summarizes_voltage_metrics(self):
        times = np.array([0.0, 0.25, 0.5, 0.75])
        voltages = np.array([0.0, 2.0, 0.0, -2.0])
        quality = summarize_waveform(times, voltages)
        self.assertEqual(quality.voltage_vpp_v, 4.0)
        self.assertAlmostEqual(quality.voltage_rms_v, np.sqrt(2.0))

    def test_warns_when_window_has_too_few_cycles(self):
        times = np.linspace(-0.001, 0.001, 10000, endpoint=False)
        voltages = 2.5 * np.sin(2 * np.pi * 500.0 * times)
        quality = summarize_waveform(times, voltages)
        self.assertAlmostEqual(quality.estimated_cycles, 1.0, delta=0.05)
        self.assertTrue(any("frequency estimate may be unreliable" in warning for warning in quality.quality_warnings))

    def test_warns_when_expected_frequency_mismatches(self):
        times = np.linspace(0.0, 0.01, 10000, endpoint=False)
        voltages = 2.5 * np.sin(2 * np.pi * 5000.0 * times)
        quality = summarize_waveform(times, voltages, expected_frequency_hz=500.0, frequency_tolerance_ratio=0.05)
        self.assertFalse(quality.frequency_in_tolerance)
        self.assertAlmostEqual(quality.frequency_error_ratio, 9.0, delta=0.1)
        self.assertTrue(any("frequency_mismatch" in warning for warning in quality.quality_warnings))


if __name__ == "__main__":
    unittest.main()
