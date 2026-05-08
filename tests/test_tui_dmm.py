from __future__ import annotations

import unittest
from pathlib import Path
import time

from wavebench.config import (
    AutoscaleConfig,
    ConnectionConfig,
    DmmConfig,
    OutputConfig,
    PowerConfig,
    ScopeConfig,
    WaveBenchConfig,
    WaveformConfig,
)
from wavebench.drivers.dm3000 import DmmReading
from wavebench.tui.dmm import FakeDmmPanelAdapter, build_dmm_panel_state
from wavebench.tui.source import FakeSourcePanelAdapter
from wavebench.tui.state import dmm_config_status, dmm_state_from_reading

from wavebench.tui import app as tui_app

if tui_app._TEXTUAL_IMPORT_ERROR is None:
    from textual.widgets import Button


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
        dmm=DmmConfig(
            driver="dm3000",
            resource="/dev/ttyUSB0",
            backend="serial",
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout_ms=1000,
            settle_ms_before_read=0,
        ),
    )


class TuiDmmTests(unittest.TestCase):
    def test_dmm_config_status_is_bilingual(self):
        status = dmm_config_status(make_config())
        self.assertIn("驱动 / Driver: dm3000", status)
        self.assertIn("后端 / Backend: serial", status)
        self.assertIn("资源 / Resource: /dev/ttyUSB0", status)

    def test_dmm_state_formats_reading_and_log(self):
        reading = DmmReading(function="dcv", value=1.234567, unit="V", raw="+1.234567E+00")
        state = dmm_state_from_reading(
            config=make_config(),
            instrument_id="RIGOL,DM3058,SN,FW",
            reading=reading,
            log_lines=["Q :MEASure:VOLTage:DC?"],
        )
        self.assertEqual(state.connection_status, "已连接 / Connected")
        self.assertEqual(state.function, "dcv")
        self.assertEqual(state.value, "1.23457")
        self.assertEqual(state.unit, "V")
        self.assertEqual(state.raw_reading, "+1.234567E+00")
        self.assertEqual(state.log_lines, ("Q :MEASure:VOLTage:DC?",))

    def test_build_dmm_panel_state_includes_instrument(self):
        state = build_dmm_panel_state(
            config=make_config(),
            instrument_id="RIGOL,DM3058,SN,FW",
            reading=DmmReading(function="res", value=1000.0, unit="ohm", raw="1000"),
        )
        self.assertIn("仪器 / Instrument: RIGOL,DM3058", state.instrument_status)
        self.assertEqual(state.value, "1000")
        self.assertEqual(state.unit, "ohm")

    def test_fake_dmm_adapter_reads_without_instrument(self):
        adapter = FakeDmmPanelAdapter()
        state = adapter.read("ohm")
        self.assertEqual(state.function, "res")
        self.assertEqual(state.value, "1000")
        self.assertEqual(state.unit, "ohm")
        self.assertTrue(any("fake DMM" in line for line in state.log_lines))
        self.assertEqual(adapter.function_status(), "res")

    def test_fake_dmm_adapter_set_function_updates_state_and_readout(self):
        adapter = FakeDmmPanelAdapter()
        state = adapter.set_function("acv")
        self.assertEqual(state.function, "acv")
        self.assertEqual(adapter.function_status(), "acv")
        self.assertTrue(any("Function set fake DMM acv" in line for line in state.log_lines))

    def test_power_resource_override_preserves_dmm_config(self):
        config = make_config().with_power_resource("TCPIP::new-power::INSTR")
        self.assertIsNotNone(config.dmm)
        self.assertEqual(config.power.resource, "TCPIP::new-power::INSTR")
        self.assertEqual(config.dmm.resource, "/dev/ttyUSB0")

    @unittest.skipIf(tui_app._TEXTUAL_IMPORT_ERROR is not None, "Textual extra is not installed")
    def test_textual_app_builds_with_fake_power_and_dmm(self):
        app = tui_app.build_app(fake=True, refresh_interval_s=10.0)
        self.assertEqual(type(app.power_adapter).__name__, "FakePowerPanelAdapter")
        self.assertEqual(type(app.dmm_adapter).__name__, "FakeDmmPanelAdapter")


@unittest.skipIf(tui_app._TEXTUAL_IMPORT_ERROR is not None, "Textual extra is not installed")
class TuiDmmBusyBehaviorTests(unittest.IsolatedAsyncioTestCase):
    async def test_read_refresh_does_not_disable_apply_button(self):
        class SlowReadAdapter(FakeDmmPanelAdapter):
            def read(self, function: str | None = None):  # type: ignore[override]
                time.sleep(0.2)
                return super().read(function=function)

        app = tui_app.WaveBenchTuiApp(
            power_adapter=tui_app.FakePowerPanelAdapter(),
            dmm_adapter=SlowReadAdapter(),
            source_adapter=FakeSourcePanelAdapter(),
            refresh_interval_s=60.0,
        )
        async with app.run_test() as pilot:
            await pilot.pause(0.25)
            app._read_dmm()
            await pilot.pause(0.02)
            self.assertTrue(app.query_one("#dmm-read", Button).disabled)
            self.assertFalse(app.query_one("#dmm-apply", Button).disabled)

    async def test_apply_reentry_is_blocked(self):
        class SlowApplyAdapter(FakeDmmPanelAdapter):
            def __init__(self):
                super().__init__()
                self.apply_calls: list[str] = []

            def set_function(self, function: str):  # type: ignore[override]
                self.apply_calls.append(function)
                time.sleep(0.2)
                return super().set_function(function)

        adapter = SlowApplyAdapter()
        app = tui_app.WaveBenchTuiApp(
            power_adapter=tui_app.FakePowerPanelAdapter(),
            dmm_adapter=adapter,
            source_adapter=FakeSourcePanelAdapter(),
            refresh_interval_s=60.0,
        )
        async with app.run_test() as pilot:
            await pilot.pause(0.25)
            app.query_one("#dmm-function").value = "acv"
            app._set_dmm_function()
            app._set_dmm_function()
            await pilot.pause(0.5)
            self.assertEqual(adapter.apply_calls, ["acv"])
            self.assertFalse(app.query_one("#dmm-apply", Button).disabled)
            self.assertEqual(app.query_one("#dmm-function").value, "acv")


if __name__ == "__main__":
    unittest.main()
