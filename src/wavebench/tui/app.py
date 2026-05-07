from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from wavebench.errors import ConfigError, WaveBenchError
from wavebench.tui.dmm import DmmPanelAdapter, DmmServicePanelAdapter, FakeDmmPanelAdapter
from wavebench.tui.power import FakePowerPanelAdapter, PowerPanelAdapter, PowerServicePanelAdapter
from wavebench.tui.state import POWER_TABLE_COLUMNS, DmmPanelState, PowerPanelState

try:
    from textual.app import App, ComposeResult
    from textual.containers import Horizontal, Vertical
    from textual.worker import Worker, WorkerState
    from textual.widgets import Button, DataTable, Footer, Header, Input, RichLog, Static
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by CLI smoke without extra
    _TEXTUAL_IMPORT_ERROR = exc
else:  # pragma: no cover - import branch depends on optional extra
    _TEXTUAL_IMPORT_ERROR = None


if _TEXTUAL_IMPORT_ERROR is None:

    class WaveBenchTuiApp(App):
        CSS = """
        Screen {
            layout: vertical;
        }

        #status {
            height: 3;
            padding: 0 1;
        }

        #power-table {
            height: 8;
        }

        #power-controls {
            height: 3;
            padding: 0 1;
        }

        #dmm-panel {
            height: 8;
            padding: 0 1;
            border: solid $primary;
        }

        #dmm-controls {
            height: 3;
        }

        #dmm-readout {
            height: 2;
        }

        #log {
            height: 1fr;
            border: solid $primary;
        }
        """

        BINDINGS = [
            ("r", "refresh", "刷新 / Refresh"),
            ("q", "quit", "退出 / Quit"),
        ]

        def __init__(
            self,
            power_adapter: PowerPanelAdapter,
            dmm_adapter: DmmPanelAdapter,
            refresh_interval_s: float = 5.0,
        ):
            super().__init__()
            self.power_adapter = power_adapter
            self.dmm_adapter = dmm_adapter
            self.refresh_interval_s = refresh_interval_s
            self._power_io_in_flight = False
            self._dmm_io_in_flight = False
            self._last_state: PowerPanelState | None = None
            self._last_dmm_state: DmmPanelState | None = None
            self._power_log_lines: tuple[str, ...] = ()
            self._dmm_log_lines: tuple[str, ...] = ()

        def compose(self) -> ComposeResult:
            yield Header(show_clock=True)
            yield Static("WaveBench TUI - 实验台控制面板 / Bench Control Panel", id="status")
            table = DataTable(id="power-table")
            table.cursor_type = "row"
            yield table
            with Horizontal(id="power-controls"):
                yield Button("刷新 / Refresh", id="refresh", variant="primary")
                yield Button("CH1 开关 / Toggle", id="toggle-1")
                yield Button("CH2 开关 / Toggle", id="toggle-2")
                yield Button("CH3 开关 / Toggle", id="toggle-3")
                yield Input(value="1", placeholder="通道 / CH", id="set-channel")
                yield Input(placeholder="电压 V / Voltage", id="set-voltage")
                yield Input(placeholder="限流 A / Current", id="set-current")
                yield Button("设定 / Set", id="set-limits", variant="success")
            with Vertical(id="dmm-panel"):
                yield Static("万用表 / DMM", id="dmm-status")
                yield Static("读数 / Reading: 未知 / N/A", id="dmm-readout")
                with Horizontal(id="dmm-controls"):
                    yield Input(value="dcv", placeholder="功能 / Function", id="dmm-function")
                    yield Button("读取 / Read", id="dmm-read", variant="primary")
            yield RichLog(id="log", highlight=True, markup=False)
            yield Footer()

        def on_mount(self) -> None:
            table = self.query_one("#power-table", DataTable)
            table.add_columns(*POWER_TABLE_COLUMNS)
            self.set_interval(self.refresh_interval_s, self.action_refresh)
            self.action_refresh()

        def action_refresh(self) -> None:
            self._run_power_io("refresh", self.power_adapter.refresh, skip_if_busy=True)
            self._read_dmm(skip_if_busy=True)

        def on_button_pressed(self, event: Button.Pressed) -> None:
            button_id = event.button.id or ""
            try:
                if button_id == "refresh":
                    self.action_refresh()
                elif button_id.startswith("toggle-"):
                    channel = int(button_id.removeprefix("toggle-"))
                    self._toggle_output(channel)
                elif button_id == "set-limits":
                    self._set_limits()
                elif button_id == "dmm-read":
                    self._read_dmm()
            except (ValueError, WaveBenchError) as exc:
                self._log(f"错误 / Error: {exc}")

        def _run_power_io(
            self,
            name: str,
            operation: Callable[[], PowerPanelState],
            *,
            skip_if_busy: bool = False,
        ) -> None:
            if self._power_io_in_flight:
                if not skip_if_busy:
                    self._log("忙碌 / Busy: previous instrument operation is still running")
                return
            self._power_io_in_flight = True
            self._set_controls_enabled(False)
            self.run_worker(
                operation,
                name=name,
                group="power-io",
                thread=True,
                exclusive=True,
                exit_on_error=False,
            )

        def _run_dmm_io(
            self,
            name: str,
            operation: Callable[[], DmmPanelState],
            *,
            skip_if_busy: bool = False,
        ) -> None:
            if self._dmm_io_in_flight:
                if not skip_if_busy:
                    self._log("忙碌 / Busy: previous DMM operation is still running")
                return
            self._dmm_io_in_flight = True
            self.query_one("#dmm-read", Button).disabled = True
            self.run_worker(
                operation,
                name=name,
                group="dmm-io",
                thread=True,
                exclusive=True,
                exit_on_error=False,
            )

        def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
            worker = event.worker
            if event.state not in {
                WorkerState.CANCELLED,
                WorkerState.ERROR,
                WorkerState.SUCCESS,
            }:
                return
            if worker.group == "power-io":
                self._power_io_in_flight = False
                self._set_controls_enabled(True)
                if event.state == WorkerState.SUCCESS:
                    self._render_state(worker.result)
                elif event.state == WorkerState.ERROR:
                    error = worker.error
                    self._log(f"错误 / Error: {error}")
                else:
                    self._log("已取消 / Cancelled")
            elif worker.group == "dmm-io":
                self._dmm_io_in_flight = False
                self.query_one("#dmm-read", Button).disabled = False
                if event.state == WorkerState.SUCCESS:
                    self._render_dmm_state(worker.result)
                elif event.state == WorkerState.ERROR:
                    error = worker.error
                    self._log(f"万用表错误 / DMM error: {error}")
                else:
                    self._log("万用表已取消 / DMM cancelled")

        def _toggle_output(self, channel: int) -> None:
            if self._last_state is None:
                raise ConfigError("state is not loaded yet / 状态尚未加载")
            current = next(item for item in self._last_state.channels if item.channel == channel)
            enabled = "ON" not in current.output
            self._run_power_io(
                f"toggle-{channel}",
                lambda: self.power_adapter.set_output(channel=channel, enabled=enabled),
            )

        def _set_limits(self) -> None:
            channel = int(self.query_one("#set-channel", Input).value)
            voltage = float(self.query_one("#set-voltage", Input).value)
            current = float(self.query_one("#set-current", Input).value)
            if channel < 1:
                raise ConfigError("channel must be >= 1 / 通道必须 >= 1")
            if voltage < 0:
                raise ConfigError("voltage must be >= 0 / 电压必须 >= 0")
            if current <= 0:
                raise ConfigError("current limit must be > 0 / 限流必须 > 0")
            self._run_power_io(
                "set-limits",
                lambda: self.power_adapter.set_voltage_current_limit(
                    channel=channel,
                    voltage_v=voltage,
                    current_limit_a=current,
                ),
            )

        def _read_dmm(self, *, skip_if_busy: bool = False) -> None:
            function = self.query_one("#dmm-function", Input).value.strip() or "dcv"
            self._run_dmm_io(
                "dmm-read",
                lambda: self.dmm_adapter.read(function=function),
                skip_if_busy=skip_if_busy,
            )

        def _render_state(self, state: PowerPanelState) -> None:
            self._last_state = state
            status = self.query_one("#status", Static)
            status.update(f"{state.config_status}\n{state.instrument_status}")
            table = self.query_one("#power-table", DataTable)
            table.clear()
            for channel in state.channels:
                table.add_row(
                    f"CH{channel.channel}",
                    channel.output,
                    channel.mode,
                    channel.rating,
                    channel.set_voltage,
                    channel.set_current,
                    channel.measured_voltage,
                    channel.measured_current,
                    channel.measured_power,
                    key=str(channel.channel),
                )
            self._power_log_lines = state.log_lines
            self._render_log()

        def _render_dmm_state(self, state: DmmPanelState) -> None:
            self._last_dmm_state = state
            status = self.query_one("#dmm-status", Static)
            status.update(
                f"万用表 / DMM\n"
                f"{state.config_status}\n"
                f"{state.connection_status}\n"
                f"{state.instrument_status}"
            )
            readout = self.query_one("#dmm-readout", Static)
            readout.update(
                f"功能 / Function: {state.function} | "
                f"读数 / Reading: {state.value} {state.unit} | "
                f"原始 / Raw: {state.raw_reading}"
            )
            self._dmm_log_lines = state.log_lines
            self._render_log()

        def _render_log(self) -> None:
            log = self.query_one("#log", RichLog)
            log.clear()
            for line in (self._power_log_lines + self._dmm_log_lines)[-80:]:
                log.write(line)

        def _set_controls_enabled(self, enabled: bool) -> None:
            for widget_id in ("refresh", "toggle-1", "toggle-2", "toggle-3", "set-limits"):
                self.query_one(f"#{widget_id}", Button).disabled = not enabled

        def _log(self, line: str) -> None:
            self.query_one("#log", RichLog).write(line)


def build_app(
    *,
    config_path: str | Path = "wavebench.toml",
    resource: str | None = None,
    fake: bool = False,
    refresh_interval_s: float = 5.0,
) -> object:
    if _TEXTUAL_IMPORT_ERROR is not None:
        raise ConfigError(
            "Textual is not installed / Textual 未安装. "
            "Install with `pip install wavebench[tui]` or `pip install textual`."
        ) from _TEXTUAL_IMPORT_ERROR
    power_adapter: PowerPanelAdapter
    dmm_adapter: DmmPanelAdapter
    if fake:
        power_adapter = FakePowerPanelAdapter()
        dmm_adapter = FakeDmmPanelAdapter()
    else:
        power_adapter = PowerServicePanelAdapter.from_config(config_path=config_path, resource=resource)
        dmm_adapter = DmmServicePanelAdapter.from_config(config_path=config_path)
    return WaveBenchTuiApp(
        power_adapter=power_adapter,
        dmm_adapter=dmm_adapter,
        refresh_interval_s=refresh_interval_s,
    )


def run(
    *,
    config_path: str | Path = "wavebench.toml",
    resource: str | None = None,
    fake: bool = False,
    refresh_interval_s: float = 5.0,
) -> int:
    app = build_app(
        config_path=config_path,
        resource=resource,
        fake=fake,
        refresh_interval_s=refresh_interval_s,
    )
    app.run()
    return 0
