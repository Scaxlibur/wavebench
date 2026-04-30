# WaveBench

WaveBench is a lightweight Python measurement bench for contest debugging.

Current MVP scope:

- LAN VISA connection to RTM2032 oscilloscope
- explicit `scope auto` / `scope autoscale`
- `scope idn`, `scope errors`, `scope fetch`, `scope capture`
- acquisition packages with NPY/CSV/JSON metadata and `commands.log`
- repeated `--channel` capture for sequential multi-channel acquisition
- lightweight waveform quality metrics: Vpp/RMS/mean, frequency estimate, duty cycle, rise/fall time when applicable
- DG4202 source MVP: `source idn`, `source status`, `source set-freq`, `source output`
- closed-loop discrete frequency sweep: `sweep discrete`

## Quick start

```powershell
python -m pip install -e .
copy wavebench.example.toml wavebench.toml
wavebench scope idn --config wavebench.toml
```

Without editable install, from the project root:

```powershell
$env:PYTHONPATH = "src"
python -m wavebench scope idn --config wavebench.toml
```

## Example commands

Capture one point from the oscilloscope:

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

`sweep discrete` currently sets each source frequency, captures one scope package per point, and writes a summary CSV under `data/analysis/`.
