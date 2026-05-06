from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from wavebench.data.packages import load_run_package
from wavebench.errors import ConfigError


@dataclass(frozen=True)
class ReportIndexResult:
    output_dir: Path
    manifest_json_path: Path
    manifest_csv_path: Path
    count: int


def write_report_index(run_dirs: list[str | Path], output_dir: str | Path) -> ReportIndexResult:
    if not run_dirs:
        raise ConfigError('report-index requires at least one run directory')
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    entries = [build_manifest_entry(Path(run_dir)) for run_dir in run_dirs]
    manifest = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_runs': [str(Path(run_dir)) for run_dir in run_dirs],
        'count': len(entries),
        'runs': entries,
    }

    manifest_json_path = output / 'manifest.json'
    manifest_csv_path = output / 'manifest.csv'
    manifest_json_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    _write_manifest_csv(entries, manifest_csv_path)
    return ReportIndexResult(
        output_dir=output,
        manifest_json_path=manifest_json_path,
        manifest_csv_path=manifest_csv_path,
        count=len(entries),
    )


def build_manifest_entry(run_dir: str | Path) -> dict[str, Any]:
    package = load_run_package(run_dir)
    run = package.run
    steps = run.get('steps', []) if isinstance(run.get('steps'), list) else []
    restore = run.get('restore', {}) if isinstance(run.get('restore'), dict) else {}

    scope_step = next((step for step in steps if step.get('kind') == 'scope.capture'), None)
    dmm_step = next((step for step in steps if step.get('kind') == 'dmm.read'), None)

    scope_summary = _scope_summary(scope_step)
    dmm_summary = _dmm_summary(dmm_step)
    expect_failures = sum(1 for step in steps if _expect_failed(step.get('artifact', {})))
    expect_fft_failures = sum(1 for step in steps if _expect_fft_failed(step.get('artifact', {})))
    failed_steps = sum(1 for step in steps if step.get('status') == 'failed')

    report_path = package.path / 'report.html'
    restore_channels = restore.get('source_channels') if isinstance(restore.get('source_channels'), list) else None
    if restore_channels is None:
        channel = restore.get('source_channel')
        restore_channels = [channel] if channel is not None else []

    entry: dict[str, Any] = {
        'run_dir': str(package.path),
        'report_path': str(report_path) if report_path.exists() else None,
        'plan_path': str(run.get('plan')) if run.get('plan') is not None else None,
        'experiment_name': _nested(run, 'experiment', 'name'),
        'experiment_label': _nested(run, 'experiment', 'label'),
        'status': run.get('status'),
        'step_count': len(steps),
        'failed_steps': failed_steps,
        'has_dmm': dmm_step is not None,
        'has_scope_capture': scope_step is not None,
        'expect_failures': expect_failures,
        'expect_fft_failures': expect_fft_failures,
        'restore_status': restore.get('status'),
        'restore_source_channels': restore_channels,
        'primary_scope_frequency_hz': scope_summary.get('frequency_estimate_hz'),
        'primary_scope_vpp_v': scope_summary.get('voltage_vpp_v'),
        'primary_dmm_value': dmm_summary.get('value'),
        'primary_dmm_unit': dmm_summary.get('unit'),
        'primary_dmm_function': dmm_summary.get('function'),
        'artifact_paths': {
            'run_json': str(package.run_json_path),
            'summary_csv': str(package.summary_csv_path) if package.summary_csv_path is not None else None,
            'report_html': str(report_path) if report_path.exists() else None,
        },
    }
    return entry


CSV_FIELDS = [
    'run_dir',
    'status',
    'experiment_label',
    'step_count',
    'failed_steps',
    'expect_failures',
    'expect_fft_failures',
    'restore_status',
    'restore_source_channels',
    'primary_scope_frequency_hz',
    'primary_scope_vpp_v',
    'primary_dmm_value',
    'primary_dmm_unit',
    'primary_dmm_function',
    'report_path',
]


def _write_manifest_csv(entries: list[dict[str, Any]], path: Path) -> None:
    with path.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for entry in entries:
            row = {key: entry.get(key) for key in CSV_FIELDS}
            channels = row.get('restore_source_channels')
            if isinstance(channels, list):
                row['restore_source_channels'] = '|'.join(str(channel) for channel in channels)
            writer.writerow(row)


def _nested(obj: dict[str, Any], *keys: str) -> Any:
    cur: Any = obj
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _scope_summary(step: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(step, dict):
        return {}
    artifact = step.get('artifact', {})
    capture = artifact.get('capture') if isinstance(artifact, dict) else None
    if isinstance(capture, dict):
        quality = capture.get('quality', {})
        if isinstance(quality, dict):
            summary = quality.get('summary', {})
            if isinstance(summary, dict):
                return summary
    quality = artifact.get('quality', {}) if isinstance(artifact, dict) else {}
    if isinstance(quality, dict):
        summary = quality.get('summary', {})
        if isinstance(summary, dict):
            return summary
    return {}


def _dmm_summary(step: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(step, dict):
        return {}
    artifact = step.get('artifact', {})
    if isinstance(artifact, dict):
        reading = artifact.get('dmm_reading', {})
        if isinstance(reading, dict):
            return reading
    return {}


def _expect_failed(artifact: dict[str, Any]) -> bool:
    expect = artifact.get('expect') if isinstance(artifact, dict) else None
    return isinstance(expect, dict) and expect.get('status') == 'failed'


def _expect_fft_failed(artifact: dict[str, Any]) -> bool:
    expect_fft = artifact.get('expect_fft') if isinstance(artifact, dict) else None
    return isinstance(expect_fft, dict) and expect_fft.get('status') == 'failed'
