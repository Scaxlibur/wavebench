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
    ScopeConfig,
    WaveBenchConfig,
    WaveformConfig,
)
from wavebench.drivers.dp800 import PowerStatus
from wavebench.errors import ConfigError
from wavebench.logging import CommandLogger
from wavebench.services.run_plan import load_run_plan
from wavebench.services.run_service import RunService


def make_config(tmp: str) -> WaveBenchConfig:
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
        power=PowerConfig(
            driver="dp800",
            resource="TCPIP::power::INSTR",
            default_channel=1,
            check_errors=True,
            settle_ms_after_set=2000,
            settle_ms_after_output=1000,
        ),
    )


def write_plan(tmp: str, content: str) -> Path:
    path = Path(tmp) / "plan.toml"
    path.write_text(content, encoding="utf-8")
    return path


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
            metadata = Path(tmp) / "capture" / "metadata.json"
            metadata.parent.mkdir()
            metadata.write_text("{}", encoding="utf-8")
            capture = SimpleNamespace(package_dir=metadata.parent, metadata_path=metadata)

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

    def test_rejects_source_steps_until_executor_supports_them(self):
        with TemporaryDirectory() as tmp:
            plan = load_run_plan(
                write_plan(
                    tmp,
                    """
[[steps]]
kind = "source.status"
channel = 2
""",
                )
            )
            with self.assertRaisesRegex(ConfigError, "does not support step kind"):
                RunService(config=make_config(tmp), logger=CommandLogger()).run(plan)


if __name__ == "__main__":
    unittest.main()
