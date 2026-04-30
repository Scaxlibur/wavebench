from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
import json
import unittest

from wavebench.config import (
    AutoscaleConfig,
    ConnectionConfig,
    OutputConfig,
    PowerConfig,
    QualityConfig,
    SourceConfig,
    ScopeConfig,
    WaveBenchConfig,
    WaveformConfig,
)
from wavebench.drivers.dp800 import PowerStatus
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.services.run_plan import load_run_plan
from wavebench.services.run_service import RunService


def make_config(tmp: str, quality: QualityConfig | None = None) -> WaveBenchConfig:
    return WaveBenchConfig(
        connection=ConnectionConfig(
            backend="lan",
            resource="TCPIP::scope::INSTR",
            timeout_ms=1000,
            opc_timeout_ms=1000,
        ),
        scope=ScopeConfig(
            driver="rtm2032",
            model_hint=None,
            default_channel=1,
            reset_before_run=False,
            check_errors=True,
        ),
        autoscale=AutoscaleConfig(wait_opc=True, check_errors=True),
        waveform=WaveformConfig(format="real", byte_order="lsbf", points="DMAX"),
        output=OutputConfig(
            directory=Path(tmp) / "data" / "raw",
            package_naming="timestamp_label",
            save_csv=True,
            save_npy=True,
            save_json=True,
            save_commands_log=True,
            save_screenshot=False,
        ),
        source_path=Path(tmp) / "wavebench.toml",
        source=SourceConfig(
            driver="dg4202",
            resource="TCPIP::source::INSTR",
            default_channel=2,
            check_errors=True,
            ensure_fix_mode_on_set_frequency=True,
            settle_ms_after_set_frequency=0,
        ),
        power=PowerConfig(
            driver="dp800",
            resource="TCPIP::power::INSTR",
            default_channel=1,
            check_errors=True,
            settle_ms_after_set=2000,
            settle_ms_after_output=1000,
        ),
        quality=quality or QualityConfig(),
    )


def write_plan(tmp: str, content: str) -> Path:
    path = Path(tmp) / "plan.toml"
    path.write_text(content, encoding="utf-8")
    return path




def fake_capture(
    tmp: str,
    name: str,
    warnings: list[str] | None = None,
    *,
    frequency_hz: float | None = 1000.0,
    voltage_vpp_v: float = 5.0,
    voltage_mean_v: float = 0.0,
    duty_cycle: float | None = None,
    frequency_error_ratio: float | None = 0.0,
):
    package = Path(tmp) / name
    package.mkdir()
    metadata = package / "metadata.json"
    metadata.write_text("{}", encoding="utf-8")
    summary = {
        "quality_warnings": warnings or [],
        "frequency_estimate_hz": frequency_hz,
        "estimated_cycles": 10.0,
        "points_per_cycle": 1000.0,
        "voltage_vpp_v": voltage_vpp_v,
        "voltage_mean_v": voltage_mean_v,
        "duty_cycle": duty_cycle,
        "frequency_error_ratio": frequency_error_ratio,
    }
    waveform = SimpleNamespace(summary=lambda **kwargs: summary)
    return SimpleNamespace(package_dir=package, metadata_path=metadata, waveform=waveform)

def ok_power_status() -> PowerStatus:
    return PowerStatus(
        channel=1,
        output="ON",
        mode="CV",
        rating="P6V",
        set_voltage_v=5.0,
        set_current_a=0.1,
        measured_voltage_v=5.0,
        measured_current_a=0.01,
        measured_power_w=0.05,
    )


class RunServiceTests(unittest.TestCase):
    def test_runs_minimal_power_scope_plan_and_writes_run_files(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[experiment]
name = "plain_voltage_capture"
label = "plain_voltage_capture"

[[steps]]
kind = "power.status"
channel = 1

[[steps]]
kind = "power.set"
channel = 1
voltage_v = 3.3
current_limit_a = 0.1

[[steps]]
kind = "scope.capture"
channel = 2
label = "v3v3"
points = "def"
time_range_s = 0.01
save_csv = false

[[steps]]
kind = "sleep"
duration_s = 0.01
""",
                )
            )
            capture = fake_capture(tmp, "capture")

            with patch("wavebench.services.run_service.PowerService") as power_cls, patch(
                "wavebench.services.run_service.ScopeService"
            ) as scope_cls, patch("wavebench.services.run_service.time.sleep") as sleep:
                power = power_cls.return_value
                power.status.return_value = ok_power_status()
                power.set_voltage_current_limit.return_value = ok_power_status()
                scope_cls.return_value.capture_waveform.return_value = capture

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                power.status.assert_called_once_with(channel=1)
                power.set_voltage_current_limit.assert_called_once_with(
                    channel=1,
                    voltage_v=3.3,
                    current_limit_a=0.1,
                )
                scope_cls.return_value.capture_waveform.assert_called_once_with(
                    channel=2,
                    label="v3v3",
                )
                sleep.assert_called_once_with(0.01)

            self.assertTrue(result.run_json_path.exists())
            self.assertTrue(result.summary_csv_path.exists())
            self.assertTrue((result.run_dir / "plan.toml").exists())
            run_data = json.loads(result.run_json_path.read_text(encoding="utf-8"))
            self.assertEqual(run_data["status"], "ok")
            self.assertEqual(len(run_data["steps"]), 4)
            self.assertIn("data", str(result.run_dir))
            self.assertIn("runs", str(result.run_dir))


    def test_runs_power_output_step(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "power.output"
channel = 1
state = "off"
""",
                )
            )
            with patch("wavebench.services.run_service.PowerService") as power_cls:
                power = power_cls.return_value
                power.set_output.return_value = ok_power_status()

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                power.set_output.assert_called_once_with(channel=1, enabled=False)
                self.assertEqual(result.steps[0].artifact["power_status"]["output"], "ON")



    def test_scope_capture_quality_gate_records_warnings_without_recovery(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.capture"
label = "weak"
quality_gate = true
""",
                )
            )
            capture = fake_capture(tmp, "weak", ["low_signal_amplitude: waveform Vpp is below 20 mV"])
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                scope = scope_cls.return_value
                scope.capture_waveform.return_value = capture

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                scope.capture_waveform.assert_called_once_with(channel=1, label="weak")
                scope.autoscale.assert_not_called()
                self.assertEqual(result.steps[0].artifact["quality_gate"]["status"], "warning")
                self.assertIn("low_signal_amplitude", result.steps[0].artifact["quality_gate"]["warnings"][0])

    def test_scope_capture_auto_recovers_until_warning_is_clear(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.capture"
label = "weak"
quality_gate = true
auto_recover = true
""",
                )
            )
            first = fake_capture(tmp, "weak", ["low_points_per_cycle: too sparse"])
            second = fake_capture(tmp, "weak_retry", [])
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                scope = scope_cls.return_value
                scope.capture_waveform.side_effect = [first, second]

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                self.assertEqual(scope.capture_waveform.call_count, 2)
                scope.capture_waveform.assert_any_call(channel=1, label="weak")
                scope.capture_waveform.assert_any_call(channel=1, label="weak_auto_retry1")
                scope.autoscale.assert_called_once_with()
                artifact = result.steps[0].artifact
                self.assertEqual(artifact["quality"]["status"], "ok")
                self.assertEqual(artifact["quality_recovery"]["max_auto_recover_attempts"], 2)
                self.assertIn("low_points_per_cycle", artifact["quality_recovery"]["attempts"][0]["quality"]["warnings"][0])

    def test_scope_capture_uses_configured_recovery_attempts_and_accepts_consistency(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.capture"
label = "sparse"
quality_gate = true
auto_recover = true
""",
                )
            )
            warning = ["low_points_per_cycle: too sparse"]
            first = fake_capture(tmp, "sparse", warning, frequency_hz=1000.0, voltage_vpp_v=5.00, voltage_mean_v=0.01, duty_cycle=0.50)
            second = fake_capture(tmp, "sparse_retry1", warning, frequency_hz=1001.0, voltage_vpp_v=5.02, voltage_mean_v=0.02, duty_cycle=0.51)
            third = fake_capture(tmp, "sparse_retry2", warning, frequency_hz=1000.5, voltage_vpp_v=5.01, voltage_mean_v=0.015, duty_cycle=0.505)
            quality = QualityConfig(auto_recover_attempts=3, consistency_required_captures=3)
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                scope = scope_cls.return_value
                scope.capture_waveform.side_effect = [first, second, third]

                result = RunService(config=make_config(tmp, quality), logger=CommandLogger()).run(plan)

                self.assertEqual(scope.capture_waveform.call_count, 3)
                scope.capture_waveform.assert_any_call(channel=1, label="sparse_auto_retry1")
                scope.capture_waveform.assert_any_call(channel=1, label="sparse_auto_retry2")
                self.assertEqual(scope.autoscale.call_count, 2)
                artifact = result.steps[0].artifact
                self.assertEqual(artifact["quality"]["status"], "ok_by_consistency")
                self.assertTrue(artifact["quality"]["trusted_by_consistency"])
                self.assertEqual(artifact["quality_recovery"]["consistency"]["status"], "consistent")


    def test_scope_capture_expect_passes_and_is_written_to_summary(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.capture"
label = "pwm"

[steps.expect]
duty_cycle = { min = 0.49, max = 0.51 }
frequency_error_ratio = { max = 0.02 }
voltage_vpp_v = { min = 3.0, max = 3.6 }
""",
                )
            )
            capture = fake_capture(
                tmp,
                "pwm",
                [],
                voltage_vpp_v=3.3,
                duty_cycle=0.5,
                frequency_error_ratio=0.01,
            )
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                scope_cls.return_value.capture_waveform.return_value = capture

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                self.assertEqual(result.steps[0].status, "ok")
                self.assertEqual(result.steps[0].artifact["expect"]["status"], "ok")
                run_data = json.loads(result.run_json_path.read_text(encoding="utf-8"))
                self.assertEqual(run_data["status"], "ok")
                summary = result.summary_csv_path.read_text(encoding="utf-8")
                self.assertIn("expect_status", summary)
                self.assertIn(",ok,", summary)

    def test_scope_capture_expect_failure_marks_run_failed_without_exception(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.capture"
label = "pwm"

[steps.expect]
duty_cycle = { min = 0.73, max = 0.77 }
frequency_error_ratio = { max = 0.02 }
""",
                )
            )
            capture = fake_capture(tmp, "pwm", [], duty_cycle=0.5, frequency_error_ratio=0.03)
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                scope_cls.return_value.capture_waveform.return_value = capture

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                self.assertEqual(result.steps[0].status, "failed")
                expect = result.steps[0].artifact["expect"]
                self.assertEqual(expect["status"], "failed")
                self.assertIn("duty_cycle", expect["failures"][0])
                run_data = json.loads(result.run_json_path.read_text(encoding="utf-8"))
                self.assertEqual(run_data["status"], "failed")

    def test_scope_capture_expect_fails_when_metric_is_unavailable(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.capture"
label = "dc"

[steps.expect]
duty_cycle = { min = 0.49, max = 0.51 }
""",
                )
            )
            capture = fake_capture(tmp, "dc", [], duty_cycle=None)
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                scope_cls.return_value.capture_waveform.return_value = capture

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                self.assertEqual(result.steps[0].status, "failed")
                self.assertEqual(result.steps[0].artifact["expect"]["checks"]["duty_cycle"]["reason"], "unavailable")

    def test_runs_scope_auto_step(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "scope.auto"
""",
                )
            )
            with patch("wavebench.services.run_service.ScopeService") as scope_cls:
                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                scope_cls.return_value.autoscale.assert_called_once_with()
                self.assertEqual(len(result.steps), 1)
                self.assertEqual(result.steps[0].artifact, {"autoscale": "completed"})

    def test_allows_safety_guard_on_configured_ch1_when_coupling_is_safe(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[safety]
require_scope_coupling_not = ["DC"]
scope_guard_channel = 1

[[steps]]
kind = "power.status"
channel = 1
""",
                )
            )
            with patch("wavebench.services.run_service.ScopeService") as scope_cls, patch(
                "wavebench.services.run_service.PowerService"
            ) as power_cls:
                scope_cls.return_value.channel_coupling.return_value = "DCL"
                power_cls.return_value.status.return_value = ok_power_status()

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                scope_cls.return_value.channel_coupling.assert_called_once_with(1)
                power_cls.return_value.status.assert_called_once_with(channel=1)
                self.assertEqual(len(result.steps), 1)

    def test_rejects_safety_guard_on_configured_ch2_when_coupling_is_blocked(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[safety]
require_scope_coupling_not = ["DC"]
scope_guard_channel = 2

[[steps]]
kind = "power.status"
channel = 1
""",
                )
            )
            with patch("wavebench.services.run_service.ScopeService") as scope_cls, patch(
                "wavebench.services.run_service.PowerService"
            ) as power_cls:
                scope_cls.return_value.channel_coupling.return_value = "DC"

                with self.assertRaisesRegex(ConfigError, "scope CH2 coupling is DC"):
                    RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                scope_cls.return_value.channel_coupling.assert_called_once_with(2)
                power_cls.assert_not_called()

    def test_runs_source_steps(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "source.status"
channel = 2

[[steps]]
kind = "source.set_func"
channel = 2
function = "SQU"

[[steps]]
kind = "source.set_freq"
channel = 2
frequency_hz = 1000

[[steps]]
kind = "source.set_vpp"
channel = 2
value_vpp = 3.3

[[steps]]
kind = "source.set_duty"
channel = 2
duty_percent = 25

[[steps]]
kind = "source.output"
channel = 2
state = "on"
""",
                )
            )
            fake_status = SimpleNamespace(as_dict=lambda: {"channel": 2})
            with patch("wavebench.services.run_service.SourceService") as source_cls:
                source = source_cls.return_value
                source.status.return_value = fake_status
                source.set_function.return_value = fake_status
                source.set_frequency.return_value = fake_status
                source.set_amplitude_vpp.return_value = fake_status
                source.set_square_duty_cycle.return_value = fake_status
                source.set_output.return_value = fake_status

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                source.status.assert_called_once_with(channel=2)
                source.set_function.assert_called_once_with(channel=2, function="SQU")
                source.set_frequency.assert_called_once_with(channel=2, value_hz=1000.0)
                source.set_amplitude_vpp.assert_called_once_with(channel=2, value_vpp=3.3)
                source.set_square_duty_cycle.assert_called_once_with(channel=2, duty_percent=25.0)
                source.set_output.assert_called_once_with(channel=2, enabled=True)
                self.assertEqual(len(result.steps), 6)

    def test_restores_source_state_after_success_when_enabled(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[restore]
source_state = true
source_channel = 2

[[steps]]
kind = "source.set_func"
channel = 2
function = "SQU"
""",
                )
            )
            fake_state = SimpleNamespace(channel=2, as_dict=lambda: {"channel": 2, "function": "SIN", "square_duty_cycle_percent": 50.0})
            fake_status = SimpleNamespace(as_dict=lambda: {"channel": 2})
            with patch("wavebench.services.run_service.SourceService") as source_cls:
                source = source_cls.return_value
                source.snapshot_restorable_state.return_value = fake_state
                source.set_function.return_value = fake_status

                result = RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                source.snapshot_restorable_state.assert_called_once_with(channel=2)
                source.set_function.assert_called_once_with(channel=2, function="SQU")
                source.restore_restorable_state.assert_called_once_with(fake_state)
                run_data = json.loads(result.run_json_path.read_text(encoding="utf-8"))
                self.assertEqual(run_data["restore"]["status"], "ok")
                self.assertEqual(run_data["restore"]["snapshot"]["square_duty_cycle_percent"], 50.0)

    def test_restores_source_state_after_step_failure_when_enabled(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[restore]
source_state = true
source_channel = 2

[[steps]]
kind = "source.set_func"
channel = 2
function = "SQU"
""",
                )
            )
            fake_state = SimpleNamespace(channel=2, as_dict=lambda: {"channel": 2, "function": "SIN", "square_duty_cycle_percent": 50.0})
            with patch("wavebench.services.run_service.SourceService") as source_cls:
                source = source_cls.return_value
                source.snapshot_restorable_state.return_value = fake_state
                source.set_function.side_effect = ConfigError("boom")

                with self.assertRaisesRegex(ConfigError, "boom"):
                    RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)

                source.restore_restorable_state.assert_called_once_with(fake_state)



if __name__ == "__main__":
    unittest.main()
