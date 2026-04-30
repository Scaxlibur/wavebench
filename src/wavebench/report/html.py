from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from wavebench.data.packages import RunPackage


def write_run_report_html(run: RunPackage, output_path: str | Path | None = None) -> Path:
    path = Path(output_path) if output_path is not None else run.path / "report.html"
    path.write_text(render_run_report_html(run), encoding="utf-8")
    return path


def render_run_report_html(run: RunPackage) -> str:
    experiment = run.run.get("experiment", {}) if isinstance(run.run.get("experiment"), dict) else {}
    restore = run.run.get("restore", {}) if isinstance(run.run.get("restore"), dict) else {}
    error = run.run.get("error", {}) if isinstance(run.run.get("error"), dict) else {}
    rows = "\n".join(_step_row(step) for step in run.steps)
    if not rows:
        rows = '<tr><td colspan="8">No steps recorded.</td></tr>'
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
<thead><tr><th>#</th><th>Kind</th><th>Status</th><th>Package</th><th>Quality</th><th>Expect</th><th>Warnings</th><th>Failures</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>
"""


def _step_row(step: dict[str, Any]) -> str:
    artifact = step.get("artifact", {}) if isinstance(step.get("artifact"), dict) else {}
    quality = artifact.get("quality", {}) if isinstance(artifact.get("quality"), dict) else {}
    expect = artifact.get("expect", {}) if isinstance(artifact.get("expect"), dict) else {}
    package = artifact.get("package", "")
    package_link = ""
    if package:
        package_link = f'<code>{escape(str(package))}</code>'
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
        f"<td>{escape(str(quality.get('status', '')))}</td>"
        f"<td>{escape(str(expect.get('status', '')))}</td>"
        f"<td>{escape(warnings_text)}</td>"
        f"<td>{escape(failures_text)}</td>"
        "</tr>"
    )
