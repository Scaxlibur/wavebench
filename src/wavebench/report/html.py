from __future__ import annotations

from dataclasses import dataclass
from html import escape
import json
import os
from pathlib import Path
from typing import Any

from wavebench.data.packages import RunPackage


def write_run_report_html(run: RunPackage, output_path: str | Path | None = None) -> Path:
    path = Path(output_path) if output_path is not None else run.path / "report.html"
    path.write_text(render_run_report_html(run, output_dir=path.parent), encoding="utf-8")
    return path


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


def render_run_report_html(run: RunPackage, output_dir: str | Path | None = None) -> str:
    experiment = run.run.get("experiment", {}) if isinstance(run.run.get("experiment"), dict) else {}
    restore = run.run.get("restore", {}) if isinstance(run.run.get("restore"), dict) else {}
    error = run.run.get("error", {}) if isinstance(run.run.get("error"), dict) else {}
    report_output_dir = Path(output_dir) if output_dir is not None else run.path
    screenshots = _collect_screenshots(run, report_output_dir)
    signals = _collect_signal_summaries(run)
    screenshots_by_step = {item.step_index: item for item in screenshots}
    rows = "\n".join(_step_row(step, screenshots_by_step.get(str(step.get("index", "")))) for step in run.steps)
    if not rows:
        rows = '<tr><td colspan="9">No steps recorded.</td></tr>'
    screenshots_block = _screenshots_block(screenshots)
    signals_block = _signals_block(signals)
    summary_note = "present" if run.summary_csv_path is not None else "missing"
    error_block = ""
    if error:
        error_block = f"<h2>Run error</h2><pre>{escape(str(error))}</pre>"
    restore_block = ""
    if restore:
        restore_block = f"<p><b>Restore:</b> {escape(str(restore.get('status', 'unknown')))}</p>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>WaveBench run report - {escape(str(experiment.get('label', run.path.name)))}</title>
<style>
body {{ font-family: system-ui, sans-serif; line-height: 1.45; margin: 2rem; color: #1f2933; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #d9e2ec; padding: 0.35rem 0.5rem; text-align: left; vertical-align: top; }}
th {{ background: #f0f4f8; }}
code {{ background: #f0f4f8; padding: 0.1rem 0.25rem; border-radius: 3px; }}
.screenshot-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr)); gap: 1rem; }}
.screenshot-card {{ border: 1px solid #d9e2ec; border-radius: 6px; padding: 0.75rem; background: #fff; }}
.screenshot-card img {{ display: block; max-width: 100%; height: auto; border: 1px solid #d9e2ec; }}
.screenshot-thumb {{ max-width: 12rem; height: auto; border: 1px solid #d9e2ec; }}
.ok {{ color: #0b6b3a; }}
.failed {{ color: #a61b1b; }}
.warning {{ color: #915930; }}
</style>
</head>
<body>
<h1>WaveBench run report</h1>
<p><b>Run directory:</b> <code>{escape(str(run.path))}</code></p>
<p><b>Status:</b> <span class="{escape(run.status)}">{escape(run.status)}</span></p>
<p><b>Experiment:</b> {escape(str(experiment.get('name', '')))} / {escape(str(experiment.get('label', '')))}</p>
<p><b>summary.csv:</b> {summary_note}</p>
{restore_block}
{error_block}
<h2>Steps</h2>
<table>
<thead><tr><th>#</th><th>Kind</th><th>Status</th><th>Package</th><th>Screenshot</th><th>Quality</th><th>Expect</th><th>Warnings</th><th>Failures</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
{signals_block}
{screenshots_block}
</body>
</html>
"""


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


def _screenshots_block(screenshots: list[ReportScreenshot]) -> str:
    if not screenshots:
        return ""
    cards = "\n".join(_screenshot_card(item) for item in screenshots)
    return f"""<h2>Screenshots</h2>
<div class="screenshot-grid">
{cards}
</div>
"""


def _signals_block(signals: list[ReportSignalSummary]) -> str:
    if not signals:
        return ""
    rows = "\n".join(_signal_row(item) for item in signals)
    return f"""<h2>Signal analysis</h2>
<table>
<thead><tr><th>Step</th><th>Channel</th><th>Samples</th><th>Frequency</th><th>Vpp</th><th>RMS</th><th>Mean</th><th>Duty</th><th>Rise</th><th>Fall</th><th>Warnings</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
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
        '<figure class="screenshot-card">'
        f'<a href="{src}"><img src="{src}" alt="Step {step} screenshot"></a>'
        f'<figcaption>Step {step}: <code>{package}</code></figcaption>'
        '</figure>'
    )


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
