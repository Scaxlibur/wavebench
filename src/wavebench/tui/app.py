from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from threading import Lock

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

        #power-protection-controls {
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
            self._power_adapter_lock = Lock()
            self._power_read_in_flight = False
            self._pending_power_read_kind: str | None = None
            self._power_write_channels_in_flight: set[int] = set()
            self._power_worker_context: dict[int, tuple[str, int | None, str | None]] = {}
            self._dmm_adapter_lock = Lock()
            self._dmm_read_in_flight = False
            self._dmm_write_in_flight = False
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
            with Horizontal(id="power-protection-controls"):
                yield Button("保护刷新 / Prot Refresh", id="protection-refresh", variant="primary")
                yield Input(value="1", placeholder="保护通道 / Prot CH", id="protection-channel")
                yield Input(placeholder="OVP阈值 V / OVP V", id="ovp-threshold")
                yield Input(placeholder="OVP on/off/空 / keep", id="ovp-state")
                yield Input(placeholder="OCP阈值 A / OCP A", id="ocp-threshold")
                yield Input(placeholder="OCP on/off/空 / keep", id="ocp-state")
                yield Button("保护设定 / Set Prot", id="set-protection", variant="warning")
            with Vertical(id="dmm-panel"):
                yield Static("万用表 / DMM", id="dmm-status")
                yield Static("读数 / Reading: 未知 / N/A", id="dmm-readout")
                with Horizontal(id="dmm-controls"):
                    yield Input(value="dcv", placeholder="功能 / Function", id="dmm-function")
                    yield Button("应用功能 / Apply Func", id="dmm-apply", variant="success")
                    yield Button("读取 / Read", id="dmm-read", variant="primary")
            yield RichLog(id="log", highlight=True, markup=False)
            yield Footer()

        def on_mount(self) -> None:
            table = self.query_one("#power-table", DataTable)
            table.add_columns(*POWER_TABLE_COLUMNS)
            self.set_interval(self.refresh_interval_s, self.action_auto_refresh)
            self.action_refresh()

        def action_refresh(self) -> None:
            self._run_power_read_io("refresh", skip_if_busy=True)
            self._read_dmm(skip_if_busy=True)

        def action_auto_refresh(self) -> None:
            self._run_power_read_io("measurement-refresh", skip_if_busy=True)
            self._read_dmm(skip_if_busy=True)

        def on_button_pressed(self, event: Button.Pressed) -> None:
            button_id = event.button.id or ""
            try:
                if button_id == "refresh":
                    self.action_refresh()
                elif button_id == "protection-refresh":
                    self._refresh_protection()
                elif button_id.startswith("toggle-"):
                    channel = int(button_id.removeprefix("toggle-"))
                    self._toggle_output(channel)
                elif button_id == "set-limits":
                    self._set_limits()
                elif button_id == "set-protection":
                    self._set_protection()
                elif button_id == "dmm-apply":
                    self._set_dmm_function()
                elif button_id == "dmm-read":
                    self._read_dmm()
            except (ValueError, WaveBenchError) as exc:
                self._log(f"错误 / Error: {exc}")

        def _run_power_read_io(self, read_kind: str, *, skip_if_busy: bool = False) -> None:
            if self._power_read_in_flight:
                self._set_pending_power_read(read_kind)
                if not skip_if_busy:
                    self._log("忙碌 / Busy: read refresh in progress; queued latest refresh")
                return
            operation = self._power_read_operation(read_kind)
            self._power_read_in_flight = True
            self._set_power_read_controls_enabled(False)
            worker = self.run_worker(
                self._wrap_power_operation(operation),
                name=read_kind,
                group="power-read",
                thread=True,
                exclusive=True,
                exit_on_error=False,
            )
            self._power_worker_context[id(worker)] = ("read", None, None)

        def _run_power_write_io(
            self,
            *,
            name: str,
            channel: int,
            operation: Callable[[], PowerPanelState],
            button_id: str,
        ) -> None:
            if channel in self._power_write_channels_in_flight:
                self._log(f"忙碌 / Busy: CH{channel} write operation is still running")
                return
            self._power_write_channels_in_flight.add(channel)
            self._set_power_write_controls_enabled(channel=channel, button_id=button_id, enabled=False)
            worker = self.run_worker(
                self._wrap_power_operation(operation),
                name=name,
                group=f"power-write-ch{channel}",
                thread=True,
                exclusive=True,
                exit_on_error=False,
            )
            self._power_worker_context[id(worker)] = ("write", channel, button_id)

        def _power_read_operation(self, read_kind: str) -> Callable[[], PowerPanelState]:
            if read_kind == "refresh":
                return self.power_adapter.refresh
            if read_kind == "measurement-refresh":
                return self.power_adapter.refresh_measurements
            if read_kind == "protection-refresh":
                return self.power_adapter.refresh_protection
            raise ConfigError(f"unsupported read kind: {read_kind}")

        def _set_pending_power_read(self, read_kind: str) -> None:
            priorities = {
                "measurement-refresh": 0,
                "protection-refresh": 1,
                "refresh": 2,
            }
            current = self._pending_power_read_kind
            if current is None or priorities[read_kind] >= priorities[current]:
                self._pending_power_read_kind = read_kind

        def _run_pending_power_read_if_needed(self) -> None:
            pending = self._pending_power_read_kind
            self._pending_power_read_kind = None
            if pending is None:
                return
            self._run_power_read_io(pending, skip_if_busy=True)

        def _wrap_power_operation(
            self,
            operation: Callable[[], PowerPanelState],
        ) -> Callable[[], PowerPanelState]:
            def _locked_operation() -> PowerPanelState:
                with self._power_adapter_lock:
                    return operation()

            return _locked_operation

        def _wrap_dmm_operation(
            self,
            operation: Callable[[], DmmPanelState],
        ) -> Callable[[], DmmPanelState]:
            def _locked_operation() -> DmmPanelState:
                with self._dmm_adapter_lock:
                    return operation()

            return _locked_operation

        def _run_dmm_read_io(
            self,
            name: str,
            operation: Callable[[], DmmPanelState],
            *,
            skip_if_busy: bool = False,
        ) -> None:
            if self._dmm_write_in_flight or self._dmm_read_in_flight:
                if not skip_if_busy:
                    self._log("忙碌 / Busy: previous DMM operation is still running")
                return
            self._dmm_read_in_flight = True
            self.query_one("#dmm-read", Button).disabled = True
            self.run_worker(
                self._wrap_dmm_operation(operation),
                name=name,
                group="dmm-read",
                thread=True,
                exclusive=True,
                exit_on_error=False,
            )

        def _run_dmm_write_io(
            self,
            name: str,
            operation: Callable[[], DmmPanelState],
            *,
            skip_if_busy: bool = False,
        ) -> None:
            if self._dmm_write_in_flight:
                if not skip_if_busy:
                    self._log("忙碌 / Busy: DMM function apply is still running")
                return
            self._dmm_write_in_flight = True
            self.query_one("#dmm-apply", Button).disabled = True
            self.run_worker(
                self._wrap_dmm_operation(operation),
                name=name,
                group="dmm-write",
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
            if worker.group.startswith("power-"):
                context = self._power_worker_context.pop(id(worker), None)
                if context is None:
                    return
                kind, channel, button_id = context
                if kind == "read":
                    self._power_read_in_flight = False
                    self._set_power_read_controls_enabled(True)
                    if event.state == WorkerState.SUCCESS:
                        self._render_state(worker.result)
                    elif event.state == WorkerState.ERROR:
                        error = worker.error
                        self._log(f"错误 / Error: {error}")
                    else:
                        self._log("已取消 / Cancelled")
                    self._run_pending_power_read_if_needed()
                else:
                    if channel is None or button_id is None:
                        return
                    self._power_write_channels_in_flight.discard(channel)
                    self._set_power_write_controls_enabled(
                        channel=channel,
                        button_id=button_id,
                        enabled=True,
                    )
                    if event.state == WorkerState.SUCCESS:
                        self._render_state(worker.result)
                    elif event.state == WorkerState.ERROR:
                        error = worker.error
                        self._log(f"错误 / Error: {error}")
                    else:
                        self._log("已取消 / Cancelled")
            elif worker.group == "dmm-read":
                self._dmm_read_in_flight = False
                self.query_one("#dmm-read", Button).disabled = False
                if event.state == WorkerState.SUCCESS:
                    self._render_dmm_state(worker.result)
                elif event.state == WorkerState.ERROR:
                    error = worker.error
                    self._log(f"万用表错误 / DMM error: {error}")
                else:
                    self._log("万用表已取消 / DMM cancelled")
            elif worker.group == "dmm-write":
                self._dmm_write_in_flight = False
                self.query_one("#dmm-apply", Button).disabled = False
                if event.state == WorkerState.SUCCESS:
                    self._render_dmm_state(worker.result)
                elif event.state == WorkerState.ERROR:
                    error = worker.error
                    self._log(f"万用表功能错误 / DMM function error: {error}")
                else:
                    self._log("万用表功能已取消 / DMM function cancelled")

        def _toggle_output(self, channel: int) -> None:
            if self._last_state is None:
                raise ConfigError("state is not loaded yet / 状态尚未加载")
            current = next(item for item in self._last_state.channels if item.channel == channel)
            enabled = "ON" not in current.output
            self._run_power_write_io(
                name=f"toggle-{channel}",
                channel=channel,
                operation=lambda: self.power_adapter.set_output(channel=channel, enabled=enabled),
                button_id=f"toggle-{channel}",
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
            self._run_power_write_io(
                name="set-limits",
                channel=channel,
                operation=lambda: self.power_adapter.set_voltage_current_limit(
                    channel=channel,
                    voltage_v=voltage,
                    current_limit_a=current,
                ),
                button_id="set-limits",
            )

        def _refresh_protection(self) -> None:
            self._run_power_read_io("protection-refresh")

        def _set_protection(self) -> None:
            channel = int(self.query_one("#protection-channel", Input).value)
            if channel < 1:
                raise ConfigError("channel must be >= 1 / 通道必须 >= 1")
            ovp_threshold = self._optional_float("#ovp-threshold")
            ocp_threshold = self._optional_float("#ocp-threshold")
            ovp_enabled = self._optional_on_off("#ovp-state")
            ocp_enabled = self._optional_on_off("#ocp-state")
            self._run_power_write_io(
                name="set-protection",
                channel=channel,
                operation=lambda: self.power_adapter.set_protection(
                    channel=channel,
                    ovp_threshold_v=ovp_threshold,
                    ovp_enabled=ovp_enabled,
                    ocp_threshold_a=ocp_threshold,
                    ocp_enabled=ocp_enabled,
                ),
                button_id="set-protection",
            )

        def _optional_float(self, selector: str) -> float | None:
            value = self.query_one(selector, Input).value.strip()
            return None if value == "" else float(value)

        def _optional_on_off(self, selector: str) -> bool | None:
            value = self.query_one(selector, Input).value.strip().lower()
            if value == "":
                return None
            if value in {"on", "1", "yes", "true"}:
                return True
            if value in {"off", "0", "no", "false"}:
                return False
            raise ConfigError("state must be on/off or empty / 状态必须为 on/off 或留空")

        def _set_dmm_function(self) -> None:
            function = self.query_one("#dmm-function", Input).value.strip() or "dcv"
            self._run_dmm_write_io(
                "dmm-set-function",
                lambda: self.dmm_adapter.set_function(function=function),
            )

        def _read_dmm(self, *, skip_if_busy: bool = False) -> None:
            self._run_dmm_read_io(
                "dmm-read",
                lambda: self.dmm_adapter.read(),
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
                    channel.ovp_enabled,
                    channel.ovp_threshold,
                    channel.ovp_tripped,
                    channel.ocp_enabled,
                    channel.ocp_threshold,
                    channel.ocp_tripped,
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
            self.query_one("#dmm-function", Input).value = state.function
            self._dmm_log_lines = state.log_lines
            self._render_log()

        def _render_log(self) -> None:
            log = self.query_one("#log", RichLog)
            log.clear()
            for line in (self._power_log_lines + self._dmm_log_lines)[-80:]:
                log.write(line)

        def _set_power_read_controls_enabled(self, enabled: bool) -> None:
            for widget_id in ("refresh", "protection-refresh"):
                self.query_one(f"#{widget_id}", Button).disabled = not enabled

        def _set_power_write_controls_enabled(self, *, channel: int, button_id: str, enabled: bool) -> None:
            if channel in {1, 2, 3}:
                self.query_one(f"#toggle-{channel}", Button).disabled = not enabled
            self.query_one(f"#{button_id}", Button).disabled = not enabled

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
