from pathlib import Path
import tempfile
import unittest

from wavebench.errors import ConfigError
from wavebench.services.run_plan import load_run_plan


VALID_PLAN = """
[experiment]
name = "dp800_voltage_capture"
label = "dp800_voltage_capture"

[safety]
require_scope_coupling_not = ["DC"]
scope_guard_channel = 2

[restore]
source_state = true
source_channel = 2

[[steps]]
kind = "power.status"
channel = 1

[[steps]]
kind = "scope.capture"
channel = 2
label = "before"
points = "def"
time_range_s = 0.01
save_csv = false

[[steps]]
kind = "power.set"
channel = 1
voltage_v = 3.3
current_limit_a = 0.1
"""


class RunPlanTests(unittest.TestCase):
    def _write_plan(self, content: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "plan.toml"
        path.write_text(content, encoding="utf-8")
        return path

    def test_loads_power_scope_plan_and_safety_guard(self):
        plan = load_run_plan(self._write_plan(VALID_PLAN))
        self.assertEqual(plan.name, "dp800_voltage_capture")
        self.assertEqual(plan.label, "dp800_voltage_capture")
        self.assertEqual(plan.safety.scope_guard_channel, 2)
        self.assertEqual(plan.safety.require_scope_coupling_not, ("DC",))
        self.assertTrue(plan.restore.source_state)
        self.assertEqual(plan.restore.source_channel, 2)
        self.assertEqual(
            [step.kind for step in plan.steps], ["power.status", "scope.capture", "power.set"]
        )
        self.assertEqual(plan.steps[1].fields["points"], "DEF")
        self.assertFalse(plan.steps[1].fields["save_csv"])
        self.assertEqual(plan.steps[2].fields["voltage_v"], 3.3)

    def test_unknown_step_kind_is_rejected(self):
        path = self._write_plan("""
[[steps]]
kind = "power.magic"
""")
        with self.assertRaises(ConfigError):
            load_run_plan(path)

    def test_missing_required_step_field_is_rejected(self):
        path = self._write_plan("""
[[steps]]
kind = "power.set"
voltage_v = 3.3
""")
        with self.assertRaises(ConfigError):
            load_run_plan(path)

    def test_restore_source_channel_requires_source_state(self):
        path = self._write_plan("""
[restore]
source_channel = 2

[[steps]]
kind = "source.status"
""")
        with self.assertRaises(ConfigError):
            load_run_plan(path)

    def test_safety_coupling_guard_requires_channel(self):
        path = self._write_plan("""
[safety]
require_scope_coupling_not = ["DC"]

[[steps]]
kind = "power.status"
""")
        with self.assertRaises(ConfigError):
            load_run_plan(path)

    def test_source_and_sleep_steps_validate_fields(self):
        path = self._write_plan("""
[[steps]]
kind = "source.set_freq"
channel = 2
frequency_hz = 1000

[[steps]]
kind = "source.output"
channel = 2
state = "ON"

[[steps]]
kind = "source.set_duty"
channel = 2
duty_percent = 25

[[steps]]
kind = "sleep"
duration_s = 0.5
""")
        plan = load_run_plan(path)
        self.assertEqual(plan.steps[0].fields["frequency_hz"], 1000.0)
        self.assertEqual(plan.steps[1].fields["state"], "on")
        self.assertEqual(plan.steps[2].fields["duty_percent"], 25.0)
        self.assertEqual(plan.steps[3].fields["duration_s"], 0.5)

    def test_scope_auto_step_is_explicit_and_has_no_fields(self):
        path = self._write_plan("""
[[steps]]
kind = "scope.auto"
""")
        plan = load_run_plan(path)
        self.assertEqual(plan.steps[0].kind, "scope.auto")
        self.assertEqual(plan.steps[0].fields, {})

    def test_scope_auto_rejects_unknown_fields(self):
        path = self._write_plan("""
[[steps]]
kind = "scope.auto"
channel = 1
""")
        with self.assertRaisesRegex(ConfigError, "unknown key"):
            load_run_plan(path)

    def test_scope_target_cycles_derives_time_range(self):
        path = self._write_plan("""
[[steps]]
kind = "scope.capture"
window_frequency_hz = 100000
target_cycles = 10
""")
        plan = load_run_plan(path)
        self.assertAlmostEqual(plan.steps[0].fields["time_range_s"], 0.0001)

    def test_scope_target_cycles_requires_frequency(self):
        path = self._write_plan("""
[[steps]]
kind = "scope.capture"
target_cycles = 10
""")
        with self.assertRaisesRegex(ConfigError, "target_cycles requires"):
            load_run_plan(path)

    def test_scope_capture_accepts_quality_gate_and_auto_recover(self):
        path = self._write_plan("""
[[steps]]
kind = "scope.capture"
quality_gate = true
auto_recover = true
""")
        plan = load_run_plan(path)
        self.assertTrue(plan.steps[0].fields["quality_gate"])
        self.assertTrue(plan.steps[0].fields["auto_recover"])

    def test_scope_capture_rejects_non_bool_quality_gate(self):
        path = self._write_plan("""
[[steps]]
kind = "scope.capture"
quality_gate = "yes"
""")
        with self.assertRaisesRegex(ConfigError, "quality_gate must be true or false"):
            load_run_plan(path)


if __name__ == "__main__":
    unittest.main()
