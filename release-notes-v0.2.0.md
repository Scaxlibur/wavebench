# WaveBench v0.2.0 - readable evidence reports

## Highlights

- Added offline capture/run package readers for `data/raw/...` and `data/runs/...`.
- Added `wavebench capture inspect <capture_dir>` for human-readable capture summaries.
- Added `wavebench run report <run_dir>` for static offline HTML reports.
- Added `scope capture --screenshot` for RTM2032 PNG screenshot artifacts.
- Added run-plan `scope.capture screenshot = true` so full experiments can capture screenshots.
- Reports now embed screenshot thumbnails and a Screenshots section when captures include `screenshot.png`.
- Reports now include a Signal analysis section with frequency, Vpp, RMS, mean, duty, rise/fall, and quality warnings.
- Added `plans/demo_dg4202_10k_screenshot_report.toml` as a minimal v0.2 hardware demo plan.
- Added WSL-friendly VISA fallback through `pyvisa-py` when native RS VISA is unavailable.

## Safety model

- `run report` and `capture inspect` are offline-only and never connect to instruments.
- Screenshots are capture artifacts, not report side effects.
- Run plans remain explicit: no hidden autoscale, no hidden power output changes, no implicit reset.
- Source restore remains opt-in through `[restore] source_state = true`.

## Validation

- Unit test suite: 118 tests passing.
- Real WSL hardware demo passed: DG4202 CH2 -> RTM2032 CH1, 10 kHz capture, screenshot artifact, report generation.
- Demo report includes Signal analysis and Screenshots sections.
- Public docs avoid real local instrument IPs and private config paths.

## Known limits

- No GUI.
- No YAML workflow layer.
- No conditionals, loops, matrix experiments, or expression language in run plans.
- Signal analysis in reports summarizes existing capture metadata; it does not reprocess NPY waveforms.
- Instrument support remains intentionally narrow and verified for the documented RTM2032 / DG4202 / DP800 paths.
