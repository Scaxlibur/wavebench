# WaveBench v0.4.0 - arbitrary waveform closure

WaveBench v0.4.0 closes the first real arbitrary-waveform loop for the RIGOL DG4202 and R&S RTM2032 lab pair.

The scope of this release is deliberately small: take a CSV/NPY waveform, validate and map it into DG4000/DG4202 14-bit DAC data, upload it through `DATA:DAC VOLATILE`, capture the result with RTM2032, and preserve enough evidence to decide whether the loop actually worked.

## Highlights

- Added DG4202 arbitrary waveform upload through `DATA:DAC VOLATILE`.
- Added raw byte transport support with `InstrumentTransport.write_bytes()` and PyVISA `write_raw`.
- Added DG4000/DG4202 14-bit DAC binary block generation from validated CSV / NPY waveforms.
- Promoted `source arb-load` from dry-run-only payload validation to a minimal upload command.
- Added `source.arb_load` run-plan step so upload, output enablement, capture, and `[steps.expect]` checks can live in one explicit plan.
- Recorded the first real closure evidence: DG4202 triangle arbitrary waveform -> RTM2032 capture -> FFT peak at 1 kHz -> static report.

## CLI example

Dry-run validation remains available:

```bash
python -m wavebench source arb-load \
  --channel 1 \
  --file waveform.npy \
  --name REI_ARB \
  --amplitude 1.0 \
  --offset 0.0 \
  --export-payload data/arb/REI_ARB.json \
  --dry-run
```

Upload requires an explicit playback frequency:

```bash
python -m wavebench source arb-load \
  --config wavebench.toml \
  --channel 1 \
  --file waveform.npy \
  --name REI_TRI \
  --amplitude 1.0 \
  --frequency 1000 \
  --offset 0.0 \
  --output-on
```

## Run-plan example

```toml
[[steps]]
kind = "source.arb_load"
channel = 1
file = "data/arb/triangle_1024.npy"
frequency_hz = 1000
amplitude_vpp = 1.0
offset_v = 0.0
output_on = true

[[steps]]
kind = "scope.capture"
channel = 1
label = "arb_triangle_1k"
window_frequency_hz = 1000
target_cycles = 10
target_vpp = 1.0
screenshot = true

[steps.expect]
voltage_vpp_v = { min = 0.8, max = 1.2 }
frequency_estimate_hz = { min = 950, max = 1050 }
```

## Validation

- `python -m pytest -q` -> `150 passed`
- `git diff --check` -> OK
- Lab closure record: `doc/project/WaveBench_v0.4_闭环验证记录.md`

## Not included

v0.4.0 is not an arbitrary-waveform editor. It does not add GUI editing, cross-vendor waveform abstraction, non-volatile waveform library management, RAF / Ultra Station workflows, or automatic waveform synthesis.

Those can come later. This release is about proving the first small loop.
