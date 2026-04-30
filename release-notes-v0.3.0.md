# WaveBench v0.3.0 - visual evidence reports

v0.3.0 turns WaveBench reports from plain readable logs into small visual evidence packets. It keeps the offline-first boundary: reports and inspect commands read existing artifacts only and do not connect to instruments.

## Highlights

- Added a run-report Summary card for status, experiment label, steps, failed steps, captures, warnings, failed expectations, screenshots, restore status, and primary signal metrics.
- Added an `Expected vs measured` table for `[steps.expect]` checks.
- Added inline SVG waveform previews generated from saved `ch*.npy` data.
- Added `report-assets/manifest.json` for report artifact references and missing-artifact warnings.
- Added optional offline FFT text summaries:

```bash
python -m wavebench capture inspect data/raw/<capture_dir> --fft
```

## Report improvements

`python -m wavebench run report data/runs/<run_dir>` now writes:

```text
report.html
report-assets/manifest.json
```

The HTML report includes:

- Summary card
- Steps table with screenshot thumbnails
- Expected vs measured checks
- Signal analysis table
- Waveform previews
- Screenshot gallery

## FFT inspect

`capture inspect --fft` prints a lightweight frequency-domain summary for saved NPY waveforms:

- Hann window
- sample rate
- frequency resolution
- peak frequency and amplitude
- noise floor estimate
- 2nd to 5th harmonic bins
- rough THD estimate
- warnings for non-uniform or problematic time axes

This is intentionally a text inspect tool, not a default report section.

## Boundaries kept

v0.3.0 does not add:

- GUI / SPA
- interactive charts
- new workflow language
- conditional or matrix run plans
- default spectrum reports
- zip export
- new instrument models

## Validation

```text
124 passed
```

## Notes

The report can generate derived preview and manifest files, but it does not modify original capture data, metadata, or run records.
