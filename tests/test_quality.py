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


if __name__ == "__main__":
    unittest.main()
