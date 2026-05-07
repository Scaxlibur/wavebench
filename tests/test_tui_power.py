from __future__ import annotations

import importlib
import unittest
from pathlib import Path

from wavebench.cli import build_parser
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
from wavebench.tui.power import FakePowerPanelAdapter, build_power_panel_state
from wavebench.tui.state import channel_state_from_status, format_output_state

from wavebench.tui import app as tui_app


def make_config() -> WaveBenchConfig:
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
        waveform=WaveformConfig(format="real", byte_order="lsbf", points="DEF"),
        output=OutputConfig(
            directory=Path("data/raw"),
            package_naming="timestamp_label",
            save_csv=True,
            save_npy=True,
            save_json=True,
            save_commands_log=True,
            save_screenshot=False,
        ),
        source_path=Path("wavebench.toml"),
        power=PowerConfig(
            driver="dp800",
            resource="TCPIP::power::INSTR",
            default_channel=1,
            check_errors=True,
            settle_ms_after_set=0,
            settle_ms_after_output=0,
        ),
    )


class TuiPowerTests(unittest.TestCase):
    def test_tui_package_import_does_not_require_textual(self):
        module = importlib.import_module("wavebench.tui")
        self.assertEqual(module.__all__, ["run"])

    def test_cli_default_refresh_interval_is_conservative(self):
        args = build_parser().parse_args(["tui", "--fake"])
        self.assertEqual(args.refresh_interval, 5.0)

    def test_cli_accepts_tui_fake_without_launching(self):
        args = build_parser().parse_args(["tui", "--fake", "--refresh-interval", "0.5"])
        self.assertEqual(args.domain, "tui")
        self.assertTrue(args.fake)
        self.assertEqual(args.refresh_interval, 0.5)

    def test_channel_state_formats_bilingual_output(self):
        status = PowerStatus(
            channel=1,
            output="ON",
            mode="CV",
            rating="30V/3A",
            set_voltage_v=5.0,
            set_current_a=0.2,
            measured_voltage_v=5.01,
            measured_current_a=0.01,
            measured_power_w=0.0501,
        )
        state = channel_state_from_status(status)
        self.assertEqual(format_output_state("0"), "关 / OFF")
        self.assertEqual(state.output, "开 / ON")
        self.assertEqual(state.set_voltage, "5 V")
        self.assertEqual(state.measured_power, "0.0501 W")

    def test_build_power_panel_state_includes_config_and_log(self):
        status = PowerStatus(
            channel=1,
            output="OFF",
            mode="CV",
            rating="30V/3A",
            set_voltage_v=3.3,
            set_current_a=0.1,
            measured_voltage_v=0.0,
            measured_current_a=0.0,
            measured_power_w=0.0,
        )
        state = build_power_panel_state(
            config=make_config(),
            instrument_id="RIGOL,DP832A,SN,FW",
            statuses=[status],
            log_lines=["Q :APPL? CH1"],
        )
        self.assertIn("驱动 / Driver: dp800", state.config_status)
        self.assertIn("仪器 / Instrument: RIGOL,DP832A", state.instrument_status)
        self.assertEqual(state.channels[0].output, "关 / OFF")
        self.assertEqual(state.log_lines, ("Q :APPL? CH1",))

    def test_fake_adapter_updates_snapshot_without_instruments(self):
        adapter = FakePowerPanelAdapter()
        state = adapter.set_voltage_current_limit(channel=1, voltage_v=3.3, current_limit_a=0.2)
        self.assertEqual(state.channels[0].set_voltage, "3.3 V")
        state = adapter.set_output(channel=1, enabled=True)
        self.assertEqual(state.channels[0].output, "开 / ON")
        self.assertTrue(any("Output -> ON" in line for line in state.log_lines))

    @unittest.skipIf(tui_app._TEXTUAL_IMPORT_ERROR is not None, "Textual extra is not installed")
    def test_textual_app_builds_against_fake_adapter(self):
        app = tui_app.build_app(fake=True, refresh_interval_s=10.0)
        self.assertEqual(type(app).__name__, "WaveBenchTuiApp")


if __name__ == "__main__":
    unittest.main()
