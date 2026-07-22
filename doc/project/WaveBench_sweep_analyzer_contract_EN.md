# WaveBench Sweep Analyzer Contract

[中文版](WaveBench_扫频分析仪公共契约.md)

## Scope

WaveBench models a standalone sweep analyzer as `sweep_analyzer`. `frequency_response` is a generic data domain returned by this instrument kind, not a separate kind.

The current contract provides only hardware-independent public models, a driver Protocol, and capability-to-method mappings. It is not connected to Service, CLI, configuration, run plans, artifacts, or any concrete instrument. It does not claim that a vendor protocol, model, option, or transport has been verified.

## Public models

- `SweepPlan` represents CW or sweep operation. A sweep uses exactly one of start/stop or center/span, and can also express a linear/logarithmic axis, automatic/manual sweep time, single/continuous acquisition, internal/external triggering, averaging, point count, and source output, level, and impedance.
- `SweepAnalyzerSnapshot` keeps `requested_plan` separate from the device-read-back `effective_plan`. Restore and acceptance must use the latter; a requested value is not proof that the device applied it.
- `FrequencyResponseTrace` stores optional frequency, magnitude, and phase arrays. Its axis source is explicitly `device`, `derived`, or `unknown`; magnitude carries both a unit and `absolute`, `relative`, `linear`, or `unknown` semantics.
- `TraceIntegrity` records expected and actual point counts, completeness, and warnings. Partial data must not be padded, silently truncated, or reported as complete success.
- `MarkerReading` stores marker frequency, magnitude, phase, and delta readings; absolute and delta magnitude units are declared separately.
- `InstrumentMeasurementResult` distinguishes instrument-native results from WaveBench core recomputation through `method`.

Trace arrays are copied into read-only `float64` arrays. Empty arrays, non-finite values, unequal lengths, and non-positive frequencies are rejected. Acquisition timestamps must be timezone-aware. `raw_evidence_ref` is for a sanitized artifact reference, not a real resource, serial number, or private raw-data path.

## Driver and capabilities

`SweepAnalyzerDriver` follows the existing WaveBench atomic-capability style:

| Capability | Method |
| --- | --- |
| `sweep_analyzer.idn` | `idn()` |
| `sweep_analyzer.status` | `get_snapshot()` |
| `sweep_analyzer.trace` | `fetch_frequency_response()` |
| `sweep_analyzer.configure` | `apply_sweep_plan()` |
| `sweep_analyzer.trigger` | `trigger_single()` |
| `sweep_analyzer.output` | `set_source_output()` |
| `sweep_analyzer.marker` | `read_markers()` |
| `sweep_analyzer.analysis` | `read_measurements()` |

A plugin declares only capabilities it has actually implemented and verified. A missing method declared by a descriptor fails driver validation; kind/capability mismatches and unknown capabilities fail registry validation.

`apply_sweep_plan()` must not implicitly transition the source output from off to on. Enabling RF requires the separate `set_source_output(True)` action and explicit authorization from the upper layer. `source_output_enabled` in a plan or snapshot expresses a requested or effective read-back value; it does not replace that safety action.

## Explicitly deferred

The current core contract does not include:

- continuous trace streaming, progress, or cancellation;
- vendor commands, acknowledgements, state encodings, or parsers;
- option APIs such as external detectors, frequency discrimination, reflection, or VSWR;
- calibration, fixture, or correction models;
- Service, CLI, configuration, run-plan, or artifact serialization integration;
- model-specific frequency, level, point-count, or marker-count limits.

These capabilities require separate extensions after protocol evidence and restore semantics are known. They must not be inferred from the generic model.
