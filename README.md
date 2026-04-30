# WaveBench

WaveBench is a lightweight Python measurement bench for electronics contest debugging.

It provides small, explicit CLI commands for LAN-connected lab instruments. The current focus is reliable waveform capture, source-to-scope checks, basic programmable power-supply control, and explicit multi-instrument run plans without hidden resets or automatic output changes.

## Current capabilities

### Oscilloscope: R&S RTM2032

- LAN VISA connection
- `scope idn`, `scope errors`
- explicit `scope auto` / `scope autoscale`
- `scope fetch` and `scope capture`
- repeated `--channel` capture for sequential multi-channel acquisition
- acquisition packages with NPY/CSV/JSON metadata and `commands.log`
- waveform metrics: Vpp/RMS/mean, frequency estimate, duty cycle, rise/fall time when applicable
- waveform quality warnings for low cycle count, low samples/cycle, low amplitude, and frequency mismatch

### Signal generator: RIGOL DG4202

- `source idn`, `source status`
- `source set-freq`
- `source set-func`
- `source set-vpp`
- `source set-duty`
- `source output`
- `sweep discrete` source-to-scope frequency sweeps
- optional `--restore-source-state` for discrete sweep

### Power supply: RIGOL DP800 series

- `power idn`, `power status`
- `power set --voltage --current-limit`
- `power output on|off`
- configurable readback settle delays:
  - `power.settle_ms_after_set`
  - `power.settle_ms_after_output`

### Multi-instrument run plans

- `run check --plan <plan.toml>` parses and summarizes a plan without connecting to instruments
- `run plan --plan <plan.toml>` executes explicit source, power, scope, and sleep steps
- `run report <run_dir>` generates a static offline HTML report from `run.json` / `summary.csv` and embeds capture screenshots when present
- `capture inspect <capture_dir>` prints a human-readable offline capture summary
- optional scope coupling guard can query the configured oscilloscope channel and refuse unsafe power-supply probe plans
- optional `[restore] source_state = true` snapshots and restores the selected source channel in a `finally` path
- flow-level output is written under `data/runs/<timestamp>_<label>/` with `run.json`, `summary.csv`, step records, quality status, and references to normal capture packages
- `scope.capture` steps can opt into `quality_gate = true`; with `auto_recover = true`, warning captures trigger up to `[quality].auto_recover_attempts` autoscale + recapture attempts
- repeated warning captures can be accepted as `ok_by_consistency` when their measured metrics are stable within `[quality]` tolerances
- `scope.capture` steps can include `[steps.expect]` metric limits; failed expectations mark the run as `failed` while preserving captured artifacts

## Safety defaults

WaveBench deliberately avoids hidden high-impact actions:

- no default `*RST`
- `scope capture` does not call autoscale unless requested separately
- `power set` does not turn output on or off
- `power output` does not change voltage or current limit
- `sweep discrete` does not restore source function/amplitude unless explicitly requested with `--restore-source-state`
- no command should silently change oscilloscope input impedance
- run-plan safety guards may query instrument state and refuse execution, but must not auto-correct hardware settings

When measuring a power supply with an oscilloscope, keep the oscilloscope input in a safe high-impedance mode. Do not switch the input to 50 Ω termination unless the voltage and instrument limits are known to be safe.

## Quick start

```powershell
python -m pip install -e .
copy wavebench.example.toml wavebench.toml
python -m wavebench scope idn --config wavebench.toml
```

Without editable install, from the project root:

```powershell
$env:PYTHONPATH = "src"
python -m wavebench scope idn --config wavebench.toml
```

## Example commands

Capture from the oscilloscope:

```powershell
python -m wavebench scope capture --config wavebench.toml --channel 1 --label smoke --points def --window-frequency 1000 --target-cycles 10 --expect-frequency 1000 --frequency-tolerance 0.05 --no-csv
python -m wavebench scope capture --config wavebench.toml --channel 1 --label smoke_with_screen --points def --no-csv --screenshot
```

Set DG4202 source frequency:

```powershell
python -m wavebench source set-freq --config wavebench.toml --channel 2 1000
```

Run a discrete source-to-scope frequency sweep:

```powershell
python -m wavebench sweep discrete --config wavebench.toml --source-channel 2 --scope-channel 1 --frequencies 1000,2000,5000,10000 --target-cycles 10 --frequency-tolerance 0.05 --label dg4202_discrete_sweep --no-csv
```

Run a sweep with explicit source state restoration:

```powershell
python -m wavebench sweep discrete --config wavebench.toml --source-channel 2 --scope-channel 1 --frequencies 1000,5000 --source-func SQU --source-vpp 3.3 --restore-source-state --no-csv
```

Read DP800 power status:

```powershell
python -m wavebench power status --config wavebench.toml --channel 1
```

Set DP800 voltage and current limit without changing output state:

```powershell
python -m wavebench power set --config wavebench.toml --channel 1 --voltage 5.0 --current-limit 0.1
```

Turn DP800 output on or off explicitly:

```powershell
python -m wavebench power output --config wavebench.toml --channel 1 off
python -m wavebench power output --config wavebench.toml --channel 1 on
```

Set DG4202 square-wave duty cycle in percent:

```powershell
python -m wavebench source set-duty --config wavebench.toml --channel 2 25
```

Run the verified duty-cycle analysis plan while also checking DP800 CH1 through scope CH2:

```powershell
python -m wavebench run plan --config wavebench.toml --plan plans/dg4202_duty_10k_power_ch2_check.toml
```

Run a minimal v0.2 screenshot-report demo. This plan drives DG4202 CH2, captures RTM2032 CH1 with a screenshot, restores the source state, checks frequency plus visible signal amplitude, then generates a static report from the saved run package:

```powershell
python -m wavebench run check --config wavebench.toml --plan plans/demo_dg4202_10k_screenshot_report.toml
python -m wavebench run plan --config wavebench.toml --plan plans/demo_dg4202_10k_screenshot_report.toml
python -m wavebench run report data/runs/<run_dir>
```

Check the run-plan schema and validate plans without connecting to instruments:

```powershell
python -m wavebench run schema
python -m wavebench run check --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
python -m wavebench run check --config wavebench.toml --plan plans/example_scope_expect_quality.toml
```

A public example plan with `quality_gate`, `auto_recover`, source restoration, and `[steps.expect]` lives at `plans/example_scope_expect_quality.toml`.

Execute the verified DP800-to-scope probe voltage-step plan:

```powershell
python -m wavebench run plan --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
```

That plan performs a read-only scope coupling guard first, then records the 5 V -> 3.3 V -> 5 V DP800 step sequence into `data/runs/...`.

Run plans can opt into source restoration:

```toml
[restore]
source_state = true
source_channel = 2
```

When enabled, WaveBench snapshots output/function/frequency/amplitude and square duty cycle before executing steps, then restores them on success or failure.

## Documentation

See [`doc/README.md`](doc/README.md) for design notes, command references, verified instrument states, and implementation constraints. For writing TOML run plans, start with [`doc/WaveBench_run_plan_使用指南.md`](doc/WaveBench_run_plan_使用指南.md). For release readiness, see [`doc/WaveBench_v0.1_收口清单.md`](doc/WaveBench_v0.1_收口清单.md).


### Run plan `scope.auto`

`scope.auto` is available as an explicit run-plan step. It maps to RTM2032 `AUToscale` and waits for `*OPC?` through the existing scope service. It is never inserted implicitly before `scope.capture`, because autoscale changes horizontal, vertical, and trigger settings.

```toml
[[steps]]
kind = "scope.auto"

[[steps]]
kind = "scope.capture"
channel = 1
label = "after_auto"
```

A capture step can also request a screenshot, a quality check, and one auto-recovery retry:

```toml
[[steps]]
kind = "scope.capture"
channel = 1
label = "after_auto_if_needed"
expect_frequency_hz = 100000
window_frequency_hz = 100000
target_cycles = 10
screenshot = true
quality_gate = true
auto_recover = true
```

If the first capture reports quality warnings such as low samples per cycle, low amplitude, or frequency mismatch, WaveBench runs `scope.auto` and captures again with numbered `_auto_retryN` labels. The maximum retry count and consistency tolerances live in `[quality]` in `wavebench.toml`. If repeated warning captures produce similar frequency/Vpp/mean/duty metrics, the final capture is marked `ok_by_consistency`; all attempt package paths and warnings are kept in `run.json`.

A capture step can also assert summary metrics with `[steps.expect]`:

```toml
[[steps]]
kind = "scope.capture"
channel = 1
label = "duty_50"
expect_frequency_hz = 10000
frequency_tolerance = 0.05
quality_gate = true

[steps.expect]
duty_cycle = { min = 0.45, max = 0.55 }
frequency_estimate_hz = { min = 9500, max = 10500 }
voltage_vpp_v = { min = 2.8, max = 3.8 }
```

Failed expectations mark the step and run as `failed`, while keeping the capture package, step record, `run.json`, and `summary.csv` for debugging.
