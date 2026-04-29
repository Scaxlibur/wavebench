# WaveBench

WaveBench is a lightweight Python measurement bench for contest debugging.

MVP-1 scope:

- LAN VISA connection to an oscilloscope
- explicit `scope auto` / `scope autoscale`
- `scope idn`, `scope errors`
- future waveform `fetch` / `capture` package output

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

