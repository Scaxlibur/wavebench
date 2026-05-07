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
from wavebench.drivers.dp800 import PowerMeasurement, PowerStatus
from wavebench.errors import WaveBenchError
from wavebench.logging import CommandLogger
from wavebench.tui.power import FakePowerPanelAdapter, PowerServicePanelAdapter, build_power_panel_state
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


def make_status(
    *,
    channel: int = 1,
    output: str = "OFF",
    voltage: float = 3.3,
    current: float = 0.2,
    measured_voltage: float = 0.0,
    measured_current: float = 0.0,
    measured_power: float = 0.0,
) -> PowerStatus:
    return PowerStatus(
        channel=channel,
        output=output,
        mode="CV",
        rating="30V/3A",
        set_voltage_v=voltage,
        set_current_a=current,
        measured_voltage_v=measured_voltage,
        measured_current_a=measured_current,
        measured_power_w=measured_power,
    )


class FakePowerService:
    def __init__(self) -> None:
        self.config = make_config()
        self.logger = CommandLogger()
        self.statuses = {1: make_status(channel=1, voltage=3.3, current=0.2)}
        self.measurements = {
            1: PowerMeasurement(
                channel=1,
                measured_voltage_v=3.31,
                measured_current_a=0.01,
                measured_power_w=0.0331,
            )
        }
        self.status_calls: list[int] = []
        self.measurement_calls: list[int] = []
        self.fail_measurement = False

    def idn(self) -> str:
        return "RIGOL,DP832A,SN,FW"

    def status(self, channel: int | None = None) -> PowerStatus:
        channel = 1 if channel is None else channel
        self.status_calls.append(channel)
        return self.statuses[channel]

    def measurement(self, channel: int | None = None) -> PowerMeasurement:
        channel = 1 if channel is None else channel
        self.measurement_calls.append(channel)
        if self.fail_measurement:
            raise RuntimeError("LAN timeout")
        return self.measurements[channel]

    def set_output(self, channel: int, enabled: bool) -> PowerStatus:
        self.statuses[channel] = make_status(
            channel=channel,
            output="ON" if enabled else "OFF",
            voltage=self.statuses[channel].set_voltage_v or 0.0,
            current=self.statuses[channel].set_current_a or 0.0,
        )
        return self.statuses[channel]

    def set_voltage_current_limit(self, channel: int, voltage_v: float, current_limit_a: float) -> PowerStatus:
        self.statuses[channel] = make_status(
            channel=channel,
            output=self.statuses[channel].output,
            voltage=voltage_v,
            current=current_limit_a,
        )
        return self.statuses[channel]


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

    def test_measurement_refresh_preserves_cached_static_fields(self):
        service = FakePowerService()
        adapter = PowerServicePanelAdapter(service=service, channels=(1,))
        adapter.refresh()
        state = adapter.refresh_measurements()
        self.assertEqual(service.status_calls, [1])
        self.assertEqual(service.measurement_calls, [1])
        self.assertEqual(state.channels[0].output, "关 / OFF")
        self.assertEqual(state.channels[0].set_voltage, "3.3 V")
        self.assertEqual(state.channels[0].measured_voltage, "3.31 V")

    def test_measurement_refresh_failure_forces_next_full_refresh(self):
        service = FakePowerService()
        adapter = PowerServicePanelAdapter(service=service, channels=(1,))
        adapter.refresh()
        service.fail_measurement = True
        with self.assertRaisesRegex(WaveBenchError, "测量刷新失败.*Measurement refresh failed"):
            adapter.refresh_measurements()
        service.fail_measurement = False
        adapter.refresh_measurements()
        self.assertEqual(service.status_calls, [1, 1])

    def test_set_updates_cache_then_refreshes_measurements(self):
        service = FakePowerService()
        adapter = PowerServicePanelAdapter(service=service, channels=(1,))
        adapter.refresh()
        state = adapter.set_voltage_current_limit(channel=1, voltage_v=4.2, current_limit_a=0.3)
        self.assertEqual(service.status_calls, [1])
        self.assertEqual(service.measurement_calls, [1])
        self.assertEqual(state.channels[0].set_voltage, "4.2 V")
        self.assertEqual(state.channels[0].set_current, "0.3 A")
        self.assertEqual(state.channels[0].measured_power, "0.0331 W")

    @unittest.skipIf(tui_app._TEXTUAL_IMPORT_ERROR is not None, "Textual extra is not installed")
    def test_textual_app_builds_against_fake_adapter(self):
        app = tui_app.build_app(fake=True, refresh_interval_s=10.0)
        self.assertEqual(type(app).__name__, "WaveBenchTuiApp")
        self.assertTrue(hasattr(app, "action_auto_refresh"))


if __name__ == "__main__":
    unittest.main()
