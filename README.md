# WaveBench

WaveBench is a lightweight Python measurement bench for electronics contest debugging.

It provides small, explicit CLI commands for LAN-connected lab instruments. The current focus is reliable waveform capture, source-to-scope checks, and basic programmable power-supply control without hidden resets or automatic output changes.

## Current capabilities

### Oscilloscope: R&S RTM2032

- LAN VISA connection
- `scope idn`, `scope errors`
- explicit `scope auto` / `scope autoscale`
- `scope fetch` and `scope capture`
- repeated `--channel` capture for sequential multi-channel acquisition
- acquisition packages with NPY/CSV/JSON metadata and `commands.log`
- waveform metrics: Vpp/RMS/mean, frequency estimate, duty cycle, rise/fall time when applicable

### Signal generator: RIGOL DG4202

- `source idn`, `source status`
- `source set-freq`
- `source set-func`
- `source set-vpp`
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

## Safety defaults

WaveBench deliberately avoids hidden high-impact actions:

- no default `*RST`
- `scope capture` does not call autoscale unless requested separately
- `power set` does not turn output on or off
- `power output` does not change voltage or current limit
- `sweep discrete` does not restore source function/amplitude unless explicitly requested with `--restore-source-state`
- no command should silently change oscilloscope input impedance

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

Check a multi-instrument run plan without connecting to instruments:

```powershell
python -m wavebench run check --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
```

## Documentation

See [`doc/README.md`](doc/README.md) for design notes, command references, verified instrument states, and implementation constraints.
