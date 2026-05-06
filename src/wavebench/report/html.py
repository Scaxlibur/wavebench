from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
import os
from pathlib import Path
from typing import Any

import numpy as np

from wavebench.data.packages import RunPackage


def write_run_report_html(run: RunPackage, output_path: str | Path | None = None) -> Path:
    path = Path(output_path) if output_path is not None else run.path / "report.html"
    path.write_text(render_run_report_html(run, output_dir=path.parent), encoding="utf-8")
    write_run_report_manifest(run, output_dir=path.parent, report_path=path)
    return path


def write_run_report_manifest(
    run: RunPackage, output_dir: str | Path | None = None, report_path: str | Path | None = None
) -> Path:
    report_output_dir = Path(output_dir) if output_dir is not None else run.path
    manifest_path = report_output_dir / "report-assets" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = _build_report_manifest(
        run,
        output_dir=report_output_dir,
        report_path=Path(report_path) if report_path is not None else report_output_dir / "report.html",
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest_path


@dataclass(frozen=True)
class ReportScreenshot:
    step_index: str
    package: str
    path: Path
    src: str


@dataclass(frozen=True)
class ReportSignalSummary:
    step_index: str
    package: str
    channel: str
    samples: str
    frequency_hz: str
    vpp_v: str
    rms_v: str
    mean_v: str
    duty_cycle: str
    rise_time_s: str
    fall_time_s: str
    warnings: str


@dataclass(frozen=True)
class ReportSummary:
    status: str
    experiment_label: str
    total_steps: int
    failed_steps: int
    capture_count: int
    warning_count: int
    failed_expect_count: int
    screenshot_count: int
    restore_status: str
    primary_frequency: str
    primary_vpp: str


@dataclass(frozen=True)
class ReportExpectationRow:
    step_index: str
    step_kind: str
    metric: str
    expected: str
    measured: str
    status: str
    details: str


@dataclass(frozen=True)
class ReportDmmReading:
    step_index: str
    step_name: str
    function: str
    value: str
    unit: str
    expected: str
    status: str
    details: str


@dataclass(frozen=True)
class ReportWaveformPreview:
    step_index: str
    package: str
    channel: str
    title: str
    svg: str
    warning: str


@dataclass(frozen=True)
class ReportArtifactLink:
    step_index: str
    kind: str
    label: str
    href: str
    status: str


@dataclass(frozen=True)
class ReportEvidenceSummary:
    source_step_count: int
    scope_capture_count: int
    dmm_reading_count: int
    failed_expectation_count: int
    run_json_available: bool
    summary_csv_available: bool
    capture_package_count: int
    screenshot_count: int
    waveform_preview_count: int


def render_run_report_html(run: RunPackage, output_dir: str | Path | None = None) -> str:
    experiment = run.run.get("experiment", {}) if isinstance(run.run.get("experiment"), dict) else {}
    restore = run.run.get("restore", {}) if isinstance(run.run.get("restore"), dict) else {}
    error = run.run.get("error", {}) if isinstance(run.run.get("error"), dict) else {}
    report_output_dir = Path(output_dir) if output_dir is not None else run.path
    screenshots = _collect_screenshots(run, report_output_dir)
    signals = _collect_signal_summaries(run)
    expectations = _collect_expectation_rows(run)
    dmm_readings = _collect_dmm_readings(run)
    waveform_previews = _collect_waveform_previews(run)
    evidence = _build_evidence_summary(run, expectations, dmm_readings, screenshots, waveform_previews)
    artifact_links = _collect_artifact_links(run, report_output_dir, screenshots)
    summary = _build_report_summary(run, screenshots, signals)
    screenshots_by_step = {item.step_index: item for item in screenshots}
    evidence_timeline_block = _evidence_timeline_block(run, screenshots_by_step)
    rows = "\n".join(_step_row(step, screenshots_by_step.get(str(step.get("index", "")))) for step in run.steps)
    if not rows:
        rows = '<tr><td colspan="9">没有记录步骤 / No steps recorded.</td></tr>'
    screenshots_block = _screenshots_block(screenshots)
    acceptance_block = _acceptance_block(expectations)
    expectations_block = _expectations_block(expectations)
    dmm_block = _dmm_readings_block(dmm_readings)
    artifact_links_block = _artifact_links_block(artifact_links)
    signals_block = _signals_block(signals)
    waveform_previews_block = _waveform_previews_block(waveform_previews)
    summary_note = "present" if run.summary_csv_path is not None else "missing"
    error_block = ""
    if error:
        error_block = f"<h2>运行错误 / Run error</h2><pre>{escape(str(error))}</pre>"
    restore_block = ""
    if restore:
        restore_block = f"<p><b>恢复 / Restore:</b> {escape(str(restore.get('status', 'unknown')))}</p>"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>WaveBench 运行报告 / Run report - {escape(str(experiment.get('label', run.path.name)))}</title>
<style>
body {{ --bg: #f6f7f9; --surface: #ffffff; --text: #1f2933; --muted: #667085; --line: #d9e2ec; --brand: #2563eb; --ok-bg: #e3f9e5; --ok: #0b6b3a; --failed-bg: #ffe3e3; --failed: #a61b1b; --warning-bg: #fff3c4; --warning: #915930; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans CJK SC", "Microsoft YaHei", sans-serif; line-height: 1.5; margin: 0; color: var(--text); background: var(--bg); }}
main {{ max-width: 1180px; margin: 0 auto; padding: 2rem 1rem 3rem; }}
h1, h2 {{ color: #102a43; letter-spacing: -0.02em; }}
h1 {{ margin-bottom: 0.25rem; font-size: clamp(1.75rem, 4vw, 2.7rem); }}
h2 {{ margin-top: 1.75rem; }}
section, article.card, figure.card {{ border: 1px solid var(--line); border-radius: 14px; background: var(--surface); box-shadow: 0 1px 2px rgba(16, 42, 67, 0.04); }}
table {{ border-collapse: collapse; width: 100%; background: var(--surface); }}
th, td {{ border-bottom: 1px solid var(--line); padding: 0.5rem 0.65rem; text-align: left; vertical-align: top; }}
th {{ background: #f0f4f8; color: #334e68; font-weight: 650; }}
tr:last-child td {{ border-bottom: 0; }}
code {{ background: #f0f4f8; padding: 0.1rem 0.3rem; border-radius: 5px; }}
.table {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); margin: 0.5rem 0 1.25rem; }}
.compact-table table {{ font-size: 0.92rem; }}
.compact-table th, .compact-table td {{ padding: 0.42rem 0.55rem; }}
.compact-table code, .artifact-link {{ font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace; font-size: 0.86rem; overflow-wrap: anywhere; }}
.artifact-table td:nth-child(3), .artifact-table td:nth-child(4) {{ color: var(--muted); }}
.meta-card {{ padding: 0.85rem 1rem; margin: 1rem 0 1.25rem; }}
.meta-card p {{ margin: 0.35rem 0; }}
.screenshot-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); gap: 1rem; }}
.screenshot-card {{ padding: 0.85rem; }}
.screenshot-card img {{ display: block; max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 8px; }}
.screenshot-thumb {{ max-width: 12rem; height: auto; border: 1px solid var(--line); border-radius: 6px; }}
.waveform-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(22rem, 1fr)); gap: 1rem; }}
.waveform-card {{ padding: 0.85rem; }}
.waveform-card svg {{ display: block; max-width: 100%; height: auto; margin-top: 0.5rem; border-radius: 8px; }}
.summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 0.75rem; margin: 1rem 0 1.25rem; padding: 0.85rem; }}
.summary-card {{ padding: 0.85rem; min-width: 0; }}
.summary-card .label {{ color: var(--muted); font-size: 0.85rem; }}
.summary-card .value {{ display: inline-block; font-size: 1.25rem; font-weight: 750; margin-top: 0.15rem; overflow-wrap: anywhere; }}
.badge, .summary-card .value.ok, .summary-card .value.failed, .summary-card .value.warning {{ border-radius: 999px; padding: 0.08rem 0.5rem; font-size: 0.95rem; }}
.summary-card .value.ok, .badge.ok {{ background: var(--ok-bg); color: var(--ok); }}
.summary-card .value.failed, .badge.failed {{ background: var(--failed-bg); color: var(--failed); }}
.summary-card .value.warning, .badge.warning {{ background: var(--warning-bg); color: var(--warning); }}
.evidence-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(12rem, 1fr)); gap: 0.6rem; margin: 0.5rem 0 1.25rem; }}
.evidence-card {{ padding: 0.7rem 0.8rem; min-width: 0; }}
.evidence-card .label {{ color: var(--muted); font-size: 0.82rem; line-height: 1.35; }}
.evidence-card .value {{ display: inline-block; margin-top: 0.2rem; font-weight: 750; overflow-wrap: anywhere; }}
.evidence-card .value.ok, .evidence-card .value.failed, .evidence-card .value.warning {{ border-radius: 999px; padding: 0.08rem 0.5rem; }}
.evidence-cell {{ min-width: 18rem; max-width: 40rem; }}
.evidence-token {{ display: inline-block; margin: 0 0.35rem 0.25rem 0; padding: 0.1rem 0.4rem; border: 1px solid #e5e7eb; border-radius: 999px; background: #f8fafc; line-height: 1.35; }}
.muted {{ color: var(--muted); font-weight: 500; }}
.ok {{ color: var(--ok); }}
.failed {{ color: var(--failed); }}
.warning {{ color: var(--warning); }}
.expectations-table tr.failed td {{ background: #fff8f8; }}
.expectations-table tr.ok td {{ background: #f7fff9; }}
.acceptance-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 0.75rem; margin: 0.5rem 0 1.25rem; }}
.acceptance-card {{ padding: 0.85rem; }}
.acceptance-card header {{ display: flex; justify-content: space-between; gap: 0.5rem; align-items: start; margin-bottom: 0.45rem; }}
.acceptance-card h3 {{ margin: 0; font-size: 1rem; }}
.acceptance-card dl {{ margin: 0; display: grid; gap: 0.25rem; }}
.acceptance-card div {{ display: grid; grid-template-columns: 5.5rem 1fr; gap: 0.5rem; }}
.acceptance-card dt {{ color: var(--muted); }}
.acceptance-card dd {{ margin: 0; font-weight: 650; overflow-wrap: anywhere; }}
.dmm-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); gap: 0.75rem; margin: 0.5rem 0 1.25rem; }}
.dmm-card {{ padding: 0.9rem; }}
.dmm-card header {{ display: flex; justify-content: space-between; gap: 0.5rem; align-items: start; margin-bottom: 0.55rem; }}
.dmm-card h3 {{ margin: 0; font-size: 1rem; }}
.dmm-card .reading {{ font-size: 1.9rem; line-height: 1.15; font-weight: 800; margin: 0.1rem 0 0.65rem; overflow-wrap: anywhere; }}
.dmm-card .reading .unit {{ color: var(--muted); font-size: 1rem; font-weight: 650; margin-left: 0.25rem; }}
.dmm-card dl {{ margin: 0; display: grid; gap: 0.25rem; }}
.dmm-card div {{ display: grid; grid-template-columns: 5.5rem 1fr; gap: 0.5rem; }}
.dmm-card dt {{ color: var(--muted); }}
.dmm-card dd {{ margin: 0; font-weight: 650; overflow-wrap: anywhere; }}
@media print {{ body {{ background: #fff; }} main {{ max-width: none; padding: 0; }} section, article.card, figure.card, .table {{ box-shadow: none; }} }}
</style>
</head>
<body>
<main>
<h1>WaveBench 运行报告 <span class="muted">Run report</span></h1>
<p class="muted">A static, self-contained hardware validation report.</p>
{_summary_block(summary)}
{_evidence_summary_block(evidence)}
{evidence_timeline_block}
{artifact_links_block}
<article class="card meta-card">
<p><b>运行目录 / Run directory:</b> <code>{escape(str(run.path))}</code></p>
<p><b>状态 / Status:</b> <span class="badge {escape(run.status)}">{escape(run.status)}</span></p>
<p><b>实验 / Experiment:</b> {escape(str(experiment.get('name', '')))} / {escape(str(experiment.get('label', '')))}</p>
<p><b>summary.csv:</b> {summary_note}</p>
{restore_block}
</article>
{error_block}
<h2>步骤 / Steps</h2>
<div class="table">
<table>
<thead><tr><th>#</th><th>类型 / Kind</th><th>状态 / Status</th><th>采集包 / Package</th><th>截图 / Screenshot</th><th>质量 / Quality</th><th>预期 / Expect</th><th>警告 / Warnings</th><th>失败项 / Failures</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
{dmm_block}
{acceptance_block}
{expectations_block}
{signals_block}
{waveform_previews_block}
{screenshots_block}
</main>
</body>
</html>
"""


def _build_report_manifest(run: RunPackage, *, output_dir: Path, report_path: Path) -> dict[str, Any]:
    screenshots = _collect_screenshots(run, output_dir)
    capture_packages: list[dict[str, Any]] = []
    waveform_previews: list[dict[str, Any]] = []
    warnings: list[str] = []
    for step in run.steps:
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        package_text = artifact.get("package")
        if not package_text:
            continue
        package = str(package_text)
        package_dir = _resolve_artifact_path(run.path, package)
        step_index = str(step.get("index", ""))
        package_record = {
            "step_index": step_index,
            "package": package,
            "path": _relative_url(package_dir, output_dir),
            "exists": package_dir.exists(),
        }
        capture_packages.append(package_record)
        if not package_dir.exists():
            warnings.append(f"step {step_index}: capture package missing: {package}")
        metadata = _read_capture_metadata(package_dir, artifact.get("metadata"))
        for channel, npy_text, _summary in _metadata_waveform_npy_files(metadata):
            if npy_text:
                npy_path = _resolve_capture_file_path(run.path, package_dir, str(npy_text))
                npy_exists = npy_path.exists()
                source_npy = _relative_url(npy_path, output_dir)
                if not npy_exists:
                    warnings.append(f"step {step_index} ch{channel}: waveform npy missing: {npy_text}")
            else:
                npy_exists = False
                source_npy = ""
                warnings.append(f"step {step_index} ch{channel}: waveform npy missing")
            waveform_previews.append(
                {
                    "step_index": step_index,
                    "package": package,
                    "channel": channel,
                    "source_npy": source_npy,
                    "exists": npy_exists,
                    "generated": "inline-svg",
                }
            )
    return {
        "schema": "wavebench.report_manifest.v1",
        "report": _relative_url(report_path, output_dir),
        "run_json": _relative_url(run.run_json_path, output_dir),
        "summary_csv": _relative_url(run.summary_csv_path, output_dir) if run.summary_csv_path is not None else None,
        "capture_packages": capture_packages,
        "screenshots": [
            {
                "step_index": item.step_index,
                "package": item.package,
                "path": _relative_url(item.path, output_dir),
            }
            for item in screenshots
        ],
        "waveform_previews": waveform_previews,
        "warnings": warnings,
    }


def _summary_block(summary: ReportSummary) -> str:
    return f"""<h2>摘要 / Summary</h2>
<section class="summary-grid">
{_summary_card("状态 / Status", summary.status, css_class=summary.status)}
{_summary_card("实验 / Experiment", summary.experiment_label)}
{_summary_card("步骤 / Steps", str(summary.total_steps))}
{_summary_card("失败步骤 / Failed steps", str(summary.failed_steps), css_class="failed" if summary.failed_steps else "ok")}
{_summary_card("采集 / Captures", str(summary.capture_count))}
{_summary_card("警告 / Warnings", str(summary.warning_count), css_class="warning" if summary.warning_count else "ok")}
{_summary_card("预期失败 / Expect failed", str(summary.failed_expect_count), css_class="failed" if summary.failed_expect_count else "ok")}
{_summary_card("截图 / Screenshots", str(summary.screenshot_count))}
{_summary_card("恢复 / Restore", summary.restore_status)}
{_summary_card("主频率 / Primary frequency", summary.primary_frequency)}
{_summary_card("主峰峰值 / Primary Vpp", summary.primary_vpp)}
</section>
"""


def _summary_card(label: str, value: str, *, css_class: str = "") -> str:
    safe_class = f" {escape(css_class)}" if css_class else ""
    return (
        '<article class="card summary-card">'
        f'<div class="label">{escape(label)}</div>'
        f'<div class="value{safe_class}">{escape(value) if value else "-"}</div>'
        '</article>'
    )


def _evidence_summary_block(evidence: ReportEvidenceSummary) -> str:
    cards = [
        ("信号源设置步骤 / Source setting steps", str(evidence.source_step_count), ""),
        ("示波器采集步骤 / Scope capture steps", str(evidence.scope_capture_count), ""),
        ("DMM 读数 / DMM readings", str(evidence.dmm_reading_count), ""),
        (
            "失败预期项 / Failed expectations",
            str(evidence.failed_expectation_count),
            "failed" if evidence.failed_expectation_count else "ok",
        ),
        ("run.json", _availability_text(evidence.run_json_available), "ok" if evidence.run_json_available else "failed"),
        (
            "summary.csv",
            _availability_text(evidence.summary_csv_available),
            "ok" if evidence.summary_csv_available else "warning",
        ),
        ("采集包 / Capture packages", str(evidence.capture_package_count), ""),
        ("截图 / Screenshots", str(evidence.screenshot_count), ""),
        ("波形预览 / Waveform previews", str(evidence.waveform_preview_count), ""),
    ]
    body = "\n".join(_evidence_summary_card(label, value, css_class) for label, value, css_class in cards)
    return f"""<h2>实验证据摘要 / Run evidence summary</h2>
<section class="evidence-grid">
{body}
</section>
"""


def _evidence_summary_card(label: str, value: str, css_class: str) -> str:
    safe_class = f" {escape(css_class)}" if css_class else ""
    return (
        '<article class="card evidence-card">'
        f'<div class="label">{escape(label)}</div>'
        f'<div class="value{safe_class}">{escape(value)}</div>'
        "</article>"
    )


def _availability_text(available: bool) -> str:
    return "存在 / present" if available else "缺失 / missing"


def _evidence_timeline_block(run: RunPackage, screenshots_by_step: dict[str, ReportScreenshot]) -> str:
    rows = "\n".join(_evidence_timeline_row(step, screenshots_by_step) for step in run.steps)
    if not rows:
        rows = '<tr><td colspan="4">没有记录步骤 / No steps recorded.</td></tr>'
    return f"""<h2>证据时间线 / Evidence timeline</h2>
<div class="table"><table>
<thead><tr><th>步骤 / Step</th><th>类型 / Kind</th><th>状态 / Status</th><th>证据 / Evidence</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
"""


def _evidence_timeline_row(step: dict[str, Any], screenshots_by_step: dict[str, ReportScreenshot]) -> str:
    status = str(step.get("status", ""))
    evidence = _evidence_text_html(_step_evidence_summary(step, screenshots_by_step))
    return (
        "<tr>"
        f"<td>{escape(str(step.get('index', '')))}</td>"
        f"<td>{escape(str(step.get('kind', '')))}</td>"
        f'<td><span class="badge {escape(status)}">{escape(status)}</span></td>'
        f'<td class="evidence-cell">{evidence}</td>'
        "</tr>"
    )


def _evidence_text_html(text: str) -> str:
    parts = [part.strip() for part in text.split(";") if part.strip()]
    if not parts:
        return ""
    return "".join(f'<span class="evidence-token">{escape(part)}</span>' for part in parts)


def _step_evidence_summary(step: dict[str, Any], screenshots_by_step: dict[str, ReportScreenshot]) -> str:
    kind = str(step.get("kind", ""))
    artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
    if kind.startswith("source."):
        return _source_step_evidence(step, artifact)
    if kind == "scope.capture":
        return _scope_step_evidence(step, artifact, screenshots_by_step)
    if kind == "dmm.read":
        return _dmm_step_evidence(step, artifact)
    if kind == "sleep":
        duration = artifact.get("duration_s", _step_field(step, "duration_s"))
        return _join_evidence_parts(["等待 / Sleep", _labeled_value("时长 / Duration", _format_metric(duration, "s"))])
    if kind == "scope.auto":
        return _join_evidence_parts(["示波器 / Scope", _labeled_value("自动设置 / Autoscale", artifact.get("autoscale"))])
    return _join_evidence_parts([_labeled_value("产物 / Artifact", ", ".join(sorted(artifact.keys())))])


def _source_step_evidence(step: dict[str, Any], artifact: dict[str, Any]) -> str:
    status = artifact.get("source_status", {}) if isinstance(artifact.get("source_status"), dict) else {}
    parts = ["信号源 / Source"]
    for label, key, unit in (
        ("通道 / Channel", "channel", ""),
        ("功能 / Function", "function", ""),
        ("频率 / Frequency", "frequency_hz", "Hz"),
        ("输出 / Output", "output", ""),
    ):
        value = status.get(key, _step_field(step, key))
        parts.append(_labeled_value(label, _format_metric(value, unit) if unit else _format_plain(value)))
    amplitude = status.get("amplitude", _step_field(step, "value_vpp"))
    amplitude_unit = str(status.get("amplitude_unit") or "Vpp")
    parts.append(_labeled_value("幅度 / Amplitude", _format_metric(amplitude, amplitude_unit)))
    return _join_evidence_parts(parts)


def _scope_step_evidence(
    step: dict[str, Any], artifact: dict[str, Any], screenshots_by_step: dict[str, ReportScreenshot]
) -> str:
    quality = artifact.get("quality", {}) if isinstance(artifact.get("quality"), dict) else {}
    expect = artifact.get("expect", {}) if isinstance(artifact.get("expect"), dict) else {}
    expect_fft = artifact.get("expect_fft", {}) if isinstance(artifact.get("expect_fft"), dict) else {}
    warnings = quality.get("warnings", [])
    warnings_text = " | ".join(str(item) for item in warnings) if isinstance(warnings, list) else str(warnings)
    step_index = str(step.get("index", ""))
    screenshot_text = "存在 / present" if step_index in screenshots_by_step else "缺失 / missing"
    parts = [
        "示波器 / Scope",
        _labeled_value("采集包 / Package", artifact.get("package")),
        _labeled_value("截图 / Screenshot", screenshot_text),
        _labeled_value("质量 / Quality", quality.get("status")),
        _labeled_value("预期 / Expect", expect.get("status")),
        _labeled_value("FFT 预期 / FFT expect", expect_fft.get("status")),
        _labeled_value("警告 / Warnings", warnings_text),
    ]
    return _join_evidence_parts(parts)


def _dmm_step_evidence(step: dict[str, Any], artifact: dict[str, Any]) -> str:
    reading = artifact.get("dmm_reading", {}) if isinstance(artifact.get("dmm_reading"), dict) else {}
    expect = artifact.get("expect", {}) if isinstance(artifact.get("expect"), dict) else {}
    value = _format_plain(reading.get("value"))
    unit = str(reading.get("unit", ""))
    if value and unit:
        value = f"{value} {unit}"
    return _join_evidence_parts(
        [
            "DMM",
            _labeled_value("功能 / Function", reading.get("function") or _step_field(step, "function")),
            _labeled_value("读数 / Reading", value),
            _labeled_value("预期 / Expect", expect.get("status")),
        ]
    )


def _labeled_value(label: str, value: Any) -> str:
    text = _format_plain(value)
    return f"{label}: {text}" if text else ""


def _join_evidence_parts(parts: list[str]) -> str:
    return "; ".join(part for part in parts if part)


def _artifact_links_block(links: list[ReportArtifactLink]) -> str:
    if not links:
        return ""
    rows = "\n".join(_artifact_link_row(link) for link in links)
    return f"""<h2>产物链接 / Artifact links</h2>
<div class="table compact-table artifact-table"><table>
<thead><tr><th>步骤 / Step</th><th>类型 / Type</th><th>产物 / Artifact</th><th>链接 / Link</th><th>状态 / Status</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
"""


def _artifact_link_row(link: ReportArtifactLink) -> str:
    href = escape(link.href, quote=True)
    return (
        "<tr>"
        f"<td>{escape(link.step_index)}</td>"
        f"<td>{escape(link.kind)}</td>"
        f"<td><code>{escape(link.label)}</code></td>"
        f'<td><a class="artifact-link" href="{href}">{escape(link.href)}</a></td>'
        f"<td>{escape(link.status)}</td>"
        "</tr>"
    )


def _acceptance_block(expectations: list[ReportExpectationRow]) -> str:
    selected = _acceptance_rows(expectations)
    if not selected:
        return ""
    cards = "\n".join(_acceptance_card(row) for row in selected)
    return f"""<h2>验收摘要 / Acceptance summary</h2>
<section class="acceptance-grid">
{cards}
</section>
"""


def _acceptance_rows(expectations: list[ReportExpectationRow]) -> list[ReportExpectationRow]:
    preferred = ("frequency", "voltage_vpp", "vpp", "duty", "harmonic", "thd")
    rows = [row for row in expectations if any(token in row.metric.lower() for token in preferred)]
    if rows:
        return rows
    return expectations[:6]


def _acceptance_card(row: ReportExpectationRow) -> str:
    status = escape(row.status or "unknown")
    return f"""<article class="card acceptance-card">
<header><h3>{escape(_metric_label(row.metric))}</h3><span class="badge {status}">{status}</span></header>
<dl>
<div><dt>实测 / Measured</dt><dd>{escape(row.measured or "-")}</dd></div>
<div><dt>预期 / Expected</dt><dd>{escape(row.expected or "-")}</dd></div>
<div><dt>步骤 / Step</dt><dd>{escape(row.step_index)} · {escape(row.step_kind)}</dd></div>
</dl>
</article>
"""


def _dmm_readings_block(readings: list[ReportDmmReading]) -> str:
    if not readings:
        return ""
    cards = "\n".join(_dmm_reading_card(reading) for reading in readings)
    return f"""<h2>DMM 读数 / DMM readings</h2>
<section class="dmm-grid">
{cards}
</section>
"""


def _dmm_reading_card(reading: ReportDmmReading) -> str:
    status = escape(reading.status or "unknown")
    unit = f'<span class="unit">{escape(reading.unit)}</span>' if reading.unit else ""
    details = ""
    if reading.details:
        details = f"<div><dt>细节 / Details</dt><dd>{escape(reading.details)}</dd></div>"
    return f"""<article class="card dmm-card">
<header><h3>{escape(reading.step_name)}</h3><span class="badge {status}">{status}</span></header>
<p class="reading">{escape(reading.value or "-")}{unit}</p>
<dl>
<div><dt>功能 / Function</dt><dd>{escape(reading.function or "-")}</dd></div>
<div><dt>步骤 / Step</dt><dd>{escape(reading.step_index)} · {escape(reading.step_name)}</dd></div>
<div><dt>预期 / Expected</dt><dd>{escape(reading.expected or "-")}</dd></div>
{details}
</dl>
</article>
"""


def _metric_label(metric: str) -> str:
    labels = {
        "frequency_estimate_hz": "频率 / Frequency",
        "frequency_error_ratio": "频率误差 / Frequency error",
        "voltage_vpp_v": "峰峰值 / Vpp",
        "duty_cycle": "占空比 / Duty",
        "thd_ratio": "总谐波失真 / THD",
        "fft.peak_frequency_hz": "FFT 主频 / FFT peak",
        "fft.peak_amplitude_v": "FFT 主幅度 / FFT peak amp",
        "fft.thd_ratio": "FFT 总谐波失真 / FFT THD",
    }
    if metric.startswith("fft.harmonic_") and metric.endswith("_amplitude_v"):
        order = metric.split("_")[1]
        return f"FFT H{order} 幅度 / FFT H{order} amplitude"
    return labels.get(metric, metric.replace("_", " "))


def _expectations_block(expectations: list[ReportExpectationRow]) -> str:
    if not expectations:
        return ""
    rows = "\n".join(_expectation_row(row) for row in expectations)
    return f"""<h2>预期 vs 实测 / Expected vs measured</h2>
<div class="table"><table class="expectations-table">
<thead><tr><th>步骤 / Step</th><th>类型 / Kind</th><th>指标 / Metric</th><th>预期 / Expected</th><th>实测 / Measured</th><th>状态 / Status</th><th>细节 / Details</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
"""


def _expectation_row(row: ReportExpectationRow) -> str:
    status = escape(row.status)
    return (
        f'<tr class="{status}">'
        f"<td>{escape(row.step_index)}</td>"
        f"<td>{escape(row.step_kind)}</td>"
        f"<td>{escape(row.metric)}</td>"
        f"<td>{escape(row.expected)}</td>"
        f"<td>{escape(row.measured)}</td>"
        f'<td class="{status}">{escape(row.status)}</td>'
        f"<td>{escape(row.details)}</td>"
        "</tr>"
    )


def _step_row(step: dict[str, Any], screenshot: ReportScreenshot | None = None) -> str:
    artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
    quality = artifact.get("quality", {}) if isinstance(artifact.get("quality"), dict) else {}
    expect = artifact.get("expect", {}) if isinstance(artifact.get("expect"), dict) else {}
    package = artifact.get("package", "")
    package_link = ""
    if package:
        package_link = f'<code>{escape(str(package))}</code>'
    screenshot_cell = ""
    if screenshot is not None:
        screenshot_cell = (
            f'<a href="{escape(screenshot.src, quote=True)}">'
            f'<img class="screenshot-thumb" src="{escape(screenshot.src, quote=True)}" '
            f'alt="Step {escape(screenshot.step_index, quote=True)} screenshot"></a>'
        )
    warnings = quality.get("warnings", [])
    if isinstance(warnings, list):
        warnings_text = " | ".join(str(item) for item in warnings)
    else:
        warnings_text = str(warnings)
    failures = expect.get("failures", [])
    if isinstance(failures, list):
        failures_text = " | ".join(str(item) for item in failures)
    else:
        failures_text = str(failures)
    status = str(step.get("status", ""))
    return (
        "<tr>"
        f"<td>{escape(str(step.get('index', '')))}</td>"
        f"<td>{escape(str(step.get('kind', '')))}</td>"
        f"<td class=\"{escape(status)}\">{escape(status)}</td>"
        f"<td>{package_link}</td>"
        f"<td>{screenshot_cell}</td>"
        f"<td>{escape(str(quality.get('status', '')))}</td>"
        f"<td>{escape(str(expect.get('status', '')))}</td>"
        f"<td>{escape(warnings_text)}</td>"
        f"<td>{escape(failures_text)}</td>"
        "</tr>"
    )


def _collect_expectation_rows(run: RunPackage) -> list[ReportExpectationRow]:
    rows: list[ReportExpectationRow] = []
    for step in run.steps:
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        for expect_key, prefix in (("expect", ""), ("expect_fft", "fft.")):
            expect = artifact.get(expect_key, {}) if isinstance(artifact.get(expect_key), dict) else {}
            checks = expect.get("checks", {})
            if not isinstance(checks, dict):
                continue
            for metric, raw_check in checks.items():
                check = raw_check if isinstance(raw_check, dict) else {}
                status = str(check.get("status", "")) or str(expect.get("status", ""))
                rows.append(
                    ReportExpectationRow(
                        step_index=str(step.get("index", "")),
                        step_kind=str(step.get("kind", "")),
                        metric=f"{prefix}{metric}",
                        expected=_format_limits(check.get("limits", {})),
                        measured=_format_expect_measured(check),
                        status=status,
                        details=_format_expect_details(check),
                    )
                )
    return rows


def _collect_dmm_readings(run: RunPackage) -> list[ReportDmmReading]:
    readings: list[ReportDmmReading] = []
    for step in run.steps:
        if step.get("kind") != "dmm.read":
            continue
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        reading = artifact.get("dmm_reading", {}) if isinstance(artifact.get("dmm_reading"), dict) else {}
        expect = artifact.get("expect", {}) if isinstance(artifact.get("expect"), dict) else {}
        value_check = _dmm_value_check(expect)
        unit = str(reading.get("unit", ""))
        expected = _format_limits(value_check.get("limits", {})) if value_check else ""
        if expected and unit:
            expected = f"{expected} {unit}"
        status = str(value_check.get("status", "")) if value_check else str(expect.get("status", "") or step.get("status", ""))
        details = _format_expect_details(value_check) if value_check else _format_dmm_failures(expect)
        step_name = _step_display_name(step)
        readings.append(
            ReportDmmReading(
                step_index=str(step.get("index", "")),
                step_name=step_name,
                function=str(reading.get("function") or _step_field(step, "function") or ""),
                value=_format_plain(reading.get("value")),
                unit=unit,
                expected=expected,
                status=status,
                details=details,
            )
        )
    return readings


def _dmm_value_check(expect: dict[str, Any]) -> dict[str, Any]:
    checks = expect.get("checks", {})
    if not isinstance(checks, dict):
        return {}
    value_check = checks.get("value", {})
    return value_check if isinstance(value_check, dict) else {}


def _format_dmm_failures(expect: dict[str, Any]) -> str:
    failures = expect.get("failures", [])
    if isinstance(failures, list):
        return " | ".join(str(item) for item in failures)
    return str(failures) if failures else ""


def _step_display_name(step: dict[str, Any]) -> str:
    for key in ("name", "label", "kind"):
        value = step.get(key)
        if value:
            return str(value)
    return "step"


def _step_field(step: dict[str, Any], key: str) -> Any:
    fields = step.get("fields", {})
    if isinstance(fields, dict):
        return fields.get(key)
    return None


def _format_limits(limits: Any) -> str:
    if not isinstance(limits, dict):
        return ""
    minimum = limits.get("min")
    maximum = limits.get("max")
    if minimum is not None and maximum is not None:
        return f"{_format_plain(minimum)}..{_format_plain(maximum)}"
    if minimum is not None:
        return f">= {_format_plain(minimum)}"
    if maximum is not None:
        return f"<= {_format_plain(maximum)}"
    return ""


def _format_expect_measured(check: dict[str, Any]) -> str:
    if "value" in check:
        return _format_plain(check.get("value"))
    reason = check.get("reason")
    if reason:
        return str(reason)
    return ""


def _format_expect_details(check: dict[str, Any]) -> str:
    reasons = check.get("reasons")
    if isinstance(reasons, list):
        return " | ".join(str(item) for item in reasons)
    reason = check.get("reason")
    if reason:
        return str(reason)
    return ""


def _build_report_summary(
    run: RunPackage, screenshots: list[ReportScreenshot], signals: list[ReportSignalSummary]
) -> ReportSummary:
    experiment = run.run.get("experiment", {}) if isinstance(run.run.get("experiment"), dict) else {}
    restore = run.run.get("restore", {}) if isinstance(run.run.get("restore"), dict) else {}
    failed_steps = 0
    packages: set[str] = set()
    warning_messages: set[str] = set()
    failed_expect_count = 0
    for step in run.steps:
        if step.get("status") == "failed":
            failed_steps += 1
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        package = artifact.get("package")
        if package:
            packages.add(str(package))
        quality = artifact.get("quality", {}) if isinstance(artifact.get("quality"), dict) else {}
        warnings = quality.get("warnings", [])
        if isinstance(warnings, list):
            warning_messages.update(str(item) for item in warnings if item)
        elif warnings:
            warning_messages.add(str(warnings))
        expect = artifact.get("expect", {}) if isinstance(artifact.get("expect"), dict) else {}
        expect_fft = artifact.get("expect_fft", {}) if isinstance(artifact.get("expect_fft"), dict) else {}
        if expect.get("status") == "failed":
            failed_expect_count += 1
        if expect_fft.get("status") == "failed":
            failed_expect_count += 1
    for signal in signals:
        if signal.warnings:
            warning_messages.update(item for item in signal.warnings.split(" | ") if item)
    primary = signals[0] if signals else None
    return ReportSummary(
        status=run.status,
        experiment_label=str(experiment.get("label") or experiment.get("name") or run.path.name),
        total_steps=len(run.steps),
        failed_steps=failed_steps,
        capture_count=len(packages),
        warning_count=len(warning_messages),
        failed_expect_count=failed_expect_count,
        screenshot_count=len(screenshots),
        restore_status=str(restore.get("status", "not configured")) if restore else "not configured",
        primary_frequency=primary.frequency_hz if primary is not None else "",
        primary_vpp=primary.vpp_v if primary is not None else "",
    )


def _build_evidence_summary(
    run: RunPackage,
    expectations: list[ReportExpectationRow],
    dmm_readings: list[ReportDmmReading],
    screenshots: list[ReportScreenshot],
    waveform_previews: list[ReportWaveformPreview],
) -> ReportEvidenceSummary:
    packages = {
        str(artifact.get("package"))
        for step in run.steps
        for artifact in [step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}]
        if artifact.get("package")
    }
    return ReportEvidenceSummary(
        source_step_count=sum(1 for step in run.steps if str(step.get("kind", "")).startswith("source.")),
        scope_capture_count=sum(1 for step in run.steps if step.get("kind") == "scope.capture"),
        dmm_reading_count=len(dmm_readings),
        failed_expectation_count=sum(1 for row in expectations if row.status == "failed"),
        run_json_available=run.run_json_path.exists(),
        summary_csv_available=run.summary_csv_path is not None and run.summary_csv_path.exists(),
        capture_package_count=len(packages),
        screenshot_count=len(screenshots),
        waveform_preview_count=len(waveform_previews),
    )


def _collect_artifact_links(
    run: RunPackage, output_dir: Path, screenshots: list[ReportScreenshot]
) -> list[ReportArtifactLink]:
    links = [
        ReportArtifactLink(
            step_index="-",
            kind="运行记录 / Run JSON",
            label="run.json",
            href=_relative_url(run.run_json_path, output_dir),
            status=_availability_text(run.run_json_path.exists()),
        )
    ]
    if run.summary_csv_path is not None:
        links.append(
            ReportArtifactLink(
                step_index="-",
                kind="摘要 CSV / Summary CSV",
                label="summary.csv",
                href=_relative_url(run.summary_csv_path, output_dir),
                status=_availability_text(run.summary_csv_path.exists()),
            )
        )
    screenshots_by_step = {item.step_index: item for item in screenshots}
    for step in run.steps:
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        package_text = artifact.get("package")
        if not package_text:
            continue
        step_index = str(step.get("index", ""))
        package = str(package_text)
        package_dir = _resolve_artifact_path(run.path, package)
        links.append(
            ReportArtifactLink(
                step_index=step_index,
                kind="采集包 / Capture package",
                label=package,
                href=_relative_url(package_dir, output_dir),
                status=_availability_text(package_dir.exists()),
            )
        )
        screenshot = screenshots_by_step.get(step_index)
        if screenshot is not None:
            links.append(
                ReportArtifactLink(
                    step_index=step_index,
                    kind="截图 / Screenshot",
                    label=Path(screenshot.src).name,
                    href=screenshot.src,
                    status=_availability_text(screenshot.path.exists()),
                )
            )
        metadata = _read_capture_metadata(package_dir, artifact.get("metadata"))
        for channel, npy_text, _summary in _metadata_waveform_npy_files(metadata):
            if not npy_text:
                continue
            npy_path = _resolve_capture_file_path(run.path, package_dir, str(npy_text))
            if not npy_path.exists():
                continue
            npy_name = Path(str(npy_text).replace("\\", "/")).name
            links.append(
                ReportArtifactLink(
                    step_index=step_index,
                    kind="波形原始数据 / Waveform raw artifact",
                    label=f"ch{channel} {npy_name}",
                    href=_relative_url(npy_path, output_dir),
                    status=_availability_text(True),
                )
            )
    return links


def _screenshots_block(screenshots: list[ReportScreenshot]) -> str:
    if not screenshots:
        return ""
    cards = "\n".join(_screenshot_card(item) for item in screenshots)
    return f"""<h2>截图 / Screenshots</h2>
<div class="screenshot-grid">
{cards}
</div>
"""


def _waveform_previews_block(previews: list[ReportWaveformPreview]) -> str:
    if not previews:
        return ""
    cards = "\n".join(_waveform_preview_card(item) for item in previews)
    return f"""<h2>波形预览 / Waveform previews</h2>
<div class="waveform-grid">
{cards}
</div>
"""


def _waveform_preview_card(preview: ReportWaveformPreview) -> str:
    warning = f'<p class="warning">{escape(preview.warning)}</p>' if preview.warning else ""
    return (
        '<figure class="card waveform-card">'
        f"<figcaption>{escape(preview.title)}<br><code>{escape(preview.package)}</code></figcaption>"
        f"{preview.svg}"
        f"{warning}"
        "</figure>"
    )


def _signals_block(signals: list[ReportSignalSummary]) -> str:
    if not signals:
        return ""
    rows = "\n".join(_signal_row(item) for item in signals)
    return f"""<h2>信号分析 / Signal analysis</h2>
<div class="table"><table>
<thead><tr><th>步骤 / Step</th><th>通道 / Channel</th><th>采样点 / Samples</th><th>频率 / Frequency</th><th>Vpp</th><th>RMS</th><th>Mean</th><th>Duty</th><th>Rise</th><th>Fall</th><th>警告 / Warnings</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>
"""


def _signal_row(signal: ReportSignalSummary) -> str:
    return (
        "<tr>"
        f"<td>{escape(signal.step_index)}</td>"
        f"<td>{escape(signal.channel)}</td>"
        f"<td>{escape(signal.samples)}</td>"
        f"<td>{escape(signal.frequency_hz)}</td>"
        f"<td>{escape(signal.vpp_v)}</td>"
        f"<td>{escape(signal.rms_v)}</td>"
        f"<td>{escape(signal.mean_v)}</td>"
        f"<td>{escape(signal.duty_cycle)}</td>"
        f"<td>{escape(signal.rise_time_s)}</td>"
        f"<td>{escape(signal.fall_time_s)}</td>"
        f"<td>{escape(signal.warnings)}</td>"
        "</tr>"
    )


def _screenshot_card(screenshot: ReportScreenshot) -> str:
    step = escape(screenshot.step_index)
    src = escape(screenshot.src, quote=True)
    package = escape(screenshot.package)
    return (
        '<figure class="card screenshot-card">'
        f'<a href="{src}"><img src="{src}" alt="Step {step} screenshot"></a>'
        f'<figcaption>Step {step}: <code>{package}</code></figcaption>'
        '</figure>'
    )


def _collect_waveform_previews(run: RunPackage) -> list[ReportWaveformPreview]:
    previews: list[ReportWaveformPreview] = []
    for step in run.steps:
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        package_text = artifact.get("package")
        if not package_text:
            continue
        package_dir = _resolve_artifact_path(run.path, str(package_text))
        metadata = _read_capture_metadata(package_dir, artifact.get("metadata"))
        for channel, npy_text, summary in _metadata_waveform_npy_files(metadata):
            title = _waveform_preview_title(step.get("index", ""), channel, summary)
            if not npy_text:
                previews.append(
                    ReportWaveformPreview(
                        step_index=str(step.get("index", "")),
                        package=str(package_text),
                        channel=channel,
                        title=title,
                        svg="",
                        warning="waveform preview unavailable: missing npy artifact",
                    )
                )
                continue
            npy_path = _resolve_capture_file_path(run.path, package_dir, str(npy_text))
            svg = ""
            warning = ""
            try:
                waveform = np.load(npy_path)
                svg = _waveform_svg(waveform)
            except Exception as exc:  # noqa: BLE001 - report generation should survive bad artifacts
                warning = f"waveform preview unavailable: {type(exc).__name__}: {exc}"
            previews.append(
                ReportWaveformPreview(
                    step_index=str(step.get("index", "")),
                    package=str(package_text),
                    channel=channel,
                    title=title,
                    svg=svg,
                    warning=warning,
                )
            )
    return previews


def _metadata_waveform_npy_files(metadata: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    channels = metadata.get("channels")
    files = metadata.get("files")
    if isinstance(channels, dict):
        file_map = files if isinstance(files, dict) else {}
        result: list[tuple[str, str, dict[str, Any]]] = []
        for raw_channel, payload in sorted(channels.items(), key=lambda item: int(item[0])):
            channel_payload = payload if isinstance(payload, dict) else {}
            summary = channel_payload.get("summary") if isinstance(channel_payload.get("summary"), dict) else {}
            channel_files = file_map.get(str(raw_channel), {}) if isinstance(file_map, dict) else {}
            npy_text = channel_files.get("npy", "") if isinstance(channel_files, dict) else ""
            result.append((str(raw_channel), str(npy_text) if npy_text else "", summary))
        return result
    waveform = metadata.get("waveform")
    if isinstance(waveform, dict):
        summary = waveform.get("summary") if isinstance(waveform.get("summary"), dict) else {}
        operation = metadata.get("operation") if isinstance(metadata.get("operation"), dict) else {}
        channel = summary.get("channel", operation.get("channel", ""))
        file_map = files if isinstance(files, dict) else {}
        npy_text = file_map.get("npy", "") if isinstance(file_map, dict) else ""
        return [(str(channel), str(npy_text) if npy_text else "", summary)]
    return []


def _waveform_preview_title(step_index: Any, channel: str, summary: dict[str, Any]) -> str:
    parts = [f"Step {step_index} ch{channel}"]
    frequency = _format_metric(summary.get("frequency_estimate_hz"), "Hz")
    vpp = _format_metric(summary.get("voltage_vpp_v"), "Vpp")
    if frequency:
        parts.append(frequency)
    if vpp:
        parts.append(vpp)
    return " — ".join(parts)


def _waveform_svg(waveform: Any, *, max_points: int = 600) -> str:
    data = np.asarray(waveform, dtype=float)
    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError("expected an Nx2 waveform array")
    finite = np.isfinite(data[:, 0]) & np.isfinite(data[:, 1])
    data = data[finite]
    if data.shape[0] < 2:
        raise ValueError("need at least two finite waveform samples")
    if data.shape[0] > max_points:
        indices = np.linspace(0, data.shape[0] - 1, max_points).astype(int)
        data = data[indices]
    x = data[:, 0]
    y = data[:, 1]
    if float(np.max(x)) == float(np.min(x)):
        x = np.arange(data.shape[0], dtype=float)
    width = 640
    height = 180
    pad = 24
    x_min = float(np.min(x))
    x_max = float(np.max(x))
    y_min = float(np.min(y))
    y_max = float(np.max(y))
    if y_max == y_min:
        y_min -= 0.5
        y_max += 0.5
    x_scale = (width - 2 * pad) / (x_max - x_min)
    y_scale = (height - 2 * pad) / (y_max - y_min)
    points = []
    for x_value, y_value in zip(x, y):
        px = pad + (float(x_value) - x_min) * x_scale
        py = height - pad - (float(y_value) - y_min) * y_scale
        points.append(f"{px:.2f},{py:.2f}")
    zero_line = ""
    if y_min <= 0 <= y_max:
        zero_y = height - pad - (0 - y_min) * y_scale
        zero_line = f'<line x1="{pad}" y1="{zero_y:.2f}" x2="{width - pad}" y2="{zero_y:.2f}" stroke="#bcccdc" stroke-width="1"/>'
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="waveform preview">'
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#f8fafc"/>'
        f'{zero_line}'
        f'<polyline points="{" ".join(points)}" fill="none" stroke="#2563eb" stroke-width="1.5"/>'
        f'<text x="{pad}" y="16" font-size="12" fill="#627d98">'
        f't={_format_axis_value(x_min)}..{_format_axis_value(x_max)} s, '
        f'v={_format_axis_value(y_min)}..{_format_axis_value(y_max)} V'
        f'</text>'
        f'</svg>'
    )


def _format_axis_value(value: float) -> str:
    return f"{value:.4g}"


def _resolve_capture_file_path(run_path: Path, package_dir: Path, file_text: str) -> Path:
    candidate = _resolve_artifact_path(run_path, file_text)
    if candidate.exists() or Path(file_text).is_absolute():
        return candidate
    return package_dir / file_text.replace("\\", "/")


def _collect_signal_summaries(run: RunPackage) -> list[ReportSignalSummary]:
    summaries: list[ReportSignalSummary] = []
    for step in run.steps:
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        package_text = artifact.get("package")
        if not package_text:
            continue
        package_dir = _resolve_artifact_path(run.path, str(package_text))
        metadata = _read_capture_metadata(package_dir, artifact.get("metadata"))
        for summary in _metadata_signal_summaries(metadata):
            warnings = summary.get("quality_warnings", [])
            if isinstance(warnings, list):
                warnings_text = " | ".join(str(item) for item in warnings)
            else:
                warnings_text = str(warnings) if warnings else ""
            summaries.append(
                ReportSignalSummary(
                    step_index=str(step.get("index", "")),
                    package=str(package_text),
                    channel=_format_plain(summary.get("channel")),
                    samples=_format_plain(summary.get("samples")),
                    frequency_hz=_format_metric(summary.get("frequency_estimate_hz"), "Hz"),
                    vpp_v=_format_metric(summary.get("voltage_vpp_v"), "V"),
                    rms_v=_format_metric(summary.get("voltage_rms_v"), "V"),
                    mean_v=_format_metric(summary.get("voltage_mean_v"), "V"),
                    duty_cycle=_format_percent(summary.get("duty_cycle")),
                    rise_time_s=_format_metric(summary.get("rise_time_s"), "s"),
                    fall_time_s=_format_metric(summary.get("fall_time_s"), "s"),
                    warnings=warnings_text,
                )
            )
    return summaries


def _metadata_signal_summaries(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    channels = metadata.get("channels")
    if isinstance(channels, dict):
        result: list[dict[str, Any]] = []
        for _raw_channel, payload in sorted(channels.items(), key=lambda item: int(item[0])):
            channel_payload = payload if isinstance(payload, dict) else {}
            summary = channel_payload.get("summary")
            if isinstance(summary, dict):
                result.append(summary)
        return result
    waveform = metadata.get("waveform")
    if isinstance(waveform, dict) and isinstance(waveform.get("summary"), dict):
        return [waveform["summary"]]
    return []


def _collect_screenshots(run: RunPackage, output_dir: Path) -> list[ReportScreenshot]:
    screenshots: list[ReportScreenshot] = []
    for step in run.steps:
        artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
        package_text = artifact.get("package")
        if not package_text:
            continue
        package_dir = _resolve_artifact_path(run.path, str(package_text))
        metadata = _read_capture_metadata(package_dir, artifact.get("metadata"))
        screenshot_text = _metadata_screenshot_path(metadata)
        if not screenshot_text:
            continue
        screenshot_path = _resolve_artifact_path(run.path, screenshot_text)
        if not screenshot_path.exists():
            screenshot_path = package_dir / "screenshot.png"
        if not screenshot_path.exists():
            continue
        screenshots.append(
            ReportScreenshot(
                step_index=str(step.get("index", "")),
                package=str(package_text),
                path=screenshot_path,
                src=_relative_url(screenshot_path, output_dir),
            )
        )
    return screenshots


def _read_capture_metadata(package_dir: Path, metadata_text: Any) -> dict[str, Any]:
    metadata_path = _resolve_artifact_path(package_dir, str(metadata_text)) if metadata_text else package_dir / "metadata.json"
    if not metadata_path.exists():
        metadata_path = package_dir / "metadata.json"
    try:
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _metadata_screenshot_path(metadata: dict[str, Any]) -> str | None:
    files = metadata.get("files", {})
    if isinstance(files, dict):
        screenshot = files.get("screenshot")
        if screenshot:
            return str(screenshot)
    return None


def _format_plain(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def _format_metric(value: Any, unit: str) -> str:
    if value is None:
        return ""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{numeric:.6g} {unit}"


def _format_percent(value: Any) -> str:
    if value is None:
        return ""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{numeric * 100:.3g}%"


def _resolve_artifact_path(run_path: Path, artifact_path: str) -> Path:
    normalized = artifact_path.replace("\\", "/")
    path = Path(normalized)
    if path.is_absolute():
        return path
    root = _project_root_from_run_path(run_path)
    return root / path


def _project_root_from_run_path(run_path: Path) -> Path:
    parts = run_path.parts
    if len(parts) >= 3 and parts[-3:-1] == ("data", "runs"):
        return Path(*parts[:-3]) if len(parts[:-3]) > 0 else Path(".")
    return run_path.parent


def _relative_url(path: Path, output_dir: Path) -> str:
    try:
        relative = os.path.relpath(path, start=output_dir)
    except ValueError:
        relative = str(path)
    return relative.replace(os.sep, "/")
