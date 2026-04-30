import unittest

from wavebench.drivers.dg4202 import SourceStatus
from wavebench.errors import DataError
from wavebench.logging import CommandLogger
from wavebench.services.source_service import SourceService
from wavebench.services.source_state import RestorableSourceState


def make_status(**overrides):
    values = {
        "channel": 2,
        "output": "ON",
        "function": "SIN",
        "frequency_hz": 5000.0,
        "amplitude": 5.0,
        "amplitude_unit": "VPP",
        "offset_v": 0.0,
        "phase_deg": 0.0,
        "frequency_mode": "FIX",
        "sweep_enabled": "OFF",
        "apply_raw": None,
    }
    values.update(overrides)
    return SourceStatus(**values)


class RestorableSourceStateTests(unittest.TestCase):
    def test_from_status_keeps_only_restorable_fields(self):
        state = RestorableSourceState.from_status(make_status())
        self.assertEqual(state.channel, 2)
        self.assertEqual(state.output, "ON")
        self.assertEqual(state.function, "SIN")
        self.assertEqual(state.frequency_hz, 5000.0)
        self.assertEqual(state.amplitude_vpp, 5.0)
        self.assertEqual(state.amplitude_unit, "VPP")
        self.assertNotIn("frequency_mode", state.as_dict())
        self.assertNotIn("sweep_enabled", state.as_dict())

    def test_from_status_rejects_missing_frequency(self):
        with self.assertRaisesRegex(DataError, "frequency_hz is missing"):
            RestorableSourceState.from_status(make_status(frequency_hz=None))

    def test_from_status_rejects_missing_amplitude(self):
        with self.assertRaisesRegex(DataError, "amplitude is missing"):
            RestorableSourceState.from_status(make_status(amplitude=None))

    def test_from_status_rejects_non_vpp_unit(self):
        with self.assertRaisesRegex(DataError, "only VPP amplitude"):
            RestorableSourceState.from_status(make_status(amplitude_unit="VRMS"))


class SourceServiceSnapshotTests(unittest.TestCase):
    def test_snapshot_restorable_state_uses_status(self):
        service = SourceService(config=None, logger=CommandLogger())
        service.status = lambda channel=None: make_status(channel=channel or 2)

        state = service.snapshot_restorable_state(channel=2)

        self.assertEqual(state.as_dict(), {
            "channel": 2,
            "output": "ON",
            "function": "SIN",
            "frequency_hz": 5000.0,
            "amplitude_vpp": 5.0,
            "amplitude_unit": "VPP",
        })


if __name__ == "__main__":
    unittest.main()
