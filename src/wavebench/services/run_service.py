from __future__ import annotations

import csv
import json
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wavebench.config import WaveBenchConfig
from wavebench.data.package import new_package_dir
from wavebench.errors import ConfigError, WaveBenchError
from wavebench.logging import CommandLogger
from wavebench.services.power_service import PowerService
from wavebench.services.run_plan import RunPlan, RunStep
from wavebench.services.scope_service import ScopeService


_EXECUTABLE_STEP_KINDS = {"power.status", "power.set", "scope.capture", "sleep"}


@dataclass(frozen=True)
class RunStepRecord:
    index: int
    kind: str
    status: str
    fields: dict[str, Any]
    artifact: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "kind": self.kind,
            "status": self.status,
            "fields": self.fields,
            "artifact": self.artifact,
        }


@dataclass(frozen=True)
class RunResult:
    run_dir: Path
    run_json_path: Path
    summary_csv_path: Path
    steps: list[RunStepRecord]


def run_output_base(config: WaveBenchConfig) -> Path:
    return config.output.directory.parent / "runs"


@dataclass
class RunService:
    config: WaveBenchConfig
    logger: CommandLogger

    def run(self, plan: RunPlan) -> RunResult:
        if plan.safety.require_scope_coupling_not:
            raise ConfigError(
                "run plan safety guard execution is not implemented yet; "
                "use run check, or remove the guard for non-special topologies"
            )
        self._reject_unsupported_steps(plan)
        run_dir = new_package_dir(run_output_base(self.config), plan.label)
        steps_dir = run_dir / "steps"
        steps_dir.mkdir(parents=True, exist_ok=False)
        if plan.path.exists():
            shutil.copyfile(plan.path, run_dir / "plan.toml")

        records: list[RunStepRecord] = []
        run_json_path = run_dir / "run.json"
        summary_csv_path = run_dir / "summary.csv"
        try:
            for step in plan.steps:
                record = self._run_step(plan, step)
                records.append(record)
                self._write_step_record(steps_dir, record)
        except Exception as exc:
            self._write_run_files(
                plan=plan,
                run_json_path=run_json_path,
                summary_csv_path=summary_csv_path,
                status="failed",
                records=records,
                error={"type": type(exc).__name__, "message": str(exc)},
            )
            if isinstance(exc, WaveBenchError):
                raise
            raise

        self._write_run_files(
            plan=plan,
            run_json_path=run_json_path,
            summary_csv_path=summary_csv_path,
            status="ok",
            records=records,
            error=None,
        )
        return RunResult(
            run_dir=run_dir,
            run_json_path=run_json_path,
            summary_csv_path=summary_csv_path,
            steps=records,
        )

    def _reject_unsupported_steps(self, plan: RunPlan) -> None:
        unsupported = [step.kind for step in plan.steps if step.kind not in _EXECUTABLE_STEP_KINDS]
        if unsupported:
            raise ConfigError(
                "run plan execution does not support step kind(s) yet: " + ", ".join(unsupported)
            )

    def _run_step(self, plan: RunPlan, step: RunStep) -> RunStepRecord:
        if step.kind == "power.status":
            status = self._power_service().status(channel=step.fields.get("channel"))
            artifact = {"power_status": _status_payload(status)}
        elif step.kind == "power.set":
            status = self._power_service().set_voltage_current_limit(
                channel=step.fields.get("channel"),
                voltage_v=step.fields["voltage_v"],
                current_limit_a=step.fields["current_limit_a"],
            )
            artifact = {"power_status": _status_payload(status)}
        elif step.kind == "scope.capture":
            capture = self._scope_service_for_capture(plan, step).capture_waveform(
                channel=step.fields.get("channel", self.config.scope.default_channel),
                label=step.fields.get("label", f"{plan.label}_{step.index:02d}_capture"),
            )
            artifact = {
                "package": str(capture.package_dir),
                "metadata": str(capture.metadata_path),
            }
        elif step.kind == "sleep":
            time.sleep(step.fields["duration_s"])
            artifact = {"duration_s": step.fields["duration_s"]}
        else:  # pragma: no cover - guarded before execution
            raise ConfigError(f"unsupported run step kind: {step.kind}")
        return RunStepRecord(
            index=step.index,
            kind=step.kind,
            status="ok",
            fields=step.fields,
            artifact=artifact,
        )

    def _power_service(self) -> PowerService:
        return PowerService(config=self.config, logger=CommandLogger())

    def _scope_service_for_capture(self, plan: RunPlan, step: RunStep) -> ScopeService:
        config = self.config
        if _has_waveform_overrides(step):
            config = config.with_waveform_overrides(
                points=step.fields.get("points"),
                time_range_s=step.fields.get("time_range_s"),
                expected_frequency_hz=step.fields.get("expect_frequency_hz"),
                frequency_tolerance_ratio=step.fields.get("frequency_tolerance"),
                target_cycles=step.fields.get("target_cycles"),
                window_frequency_hz=step.fields.get("window_frequency_hz"),
            )
        if "save_csv" in step.fields or "save_npy" in step.fields:
            config = config.with_output_overrides(
                save_csv=step.fields.get("save_csv"),
                save_npy=step.fields.get("save_npy"),
            )
        return ScopeService(config=config, logger=CommandLogger())

    def _write_step_record(self, steps_dir: Path, record: RunStepRecord) -> None:
        safe_kind = record.kind.replace(".", "_")
        path = steps_dir / f"{record.index:02d}_{safe_kind}.json"
        path.write_text(
            json.dumps(record.as_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _write_run_files(
        self,
        *,
        plan: RunPlan,
        run_json_path: Path,
        summary_csv_path: Path,
        status: str,
        records: list[RunStepRecord],
        error: dict[str, str] | None,
    ) -> None:
        run_data: dict[str, Any] = {
            "status": status,
            "experiment": {"name": plan.name, "label": plan.label},
            "plan": str(plan.path),
            "steps": [record.as_dict() for record in records],
        }
        if error is not None:
            run_data["error"] = error
        run_json_path.write_text(
            json.dumps(run_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        with summary_csv_path.open("w", newline="", encoding="utf-8") as file:
            fieldnames = ["index", "kind", "status", "package", "metadata"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow(
                    {
                        "index": record.index,
                        "kind": record.kind,
                        "status": record.status,
                        "package": record.artifact.get("package", ""),
                        "metadata": record.artifact.get("metadata", ""),
                    }
                )


def _has_waveform_overrides(step: RunStep) -> bool:
    return any(
        key in step.fields
        for key in (
            "points",
            "time_range_s",
            "expect_frequency_hz",
            "frequency_tolerance",
            "target_cycles",
            "window_frequency_hz",
        )
    )


def _status_payload(status: Any) -> dict[str, Any]:
    if hasattr(status, "as_dict"):
        return status.as_dict()
    if hasattr(status, "__dict__"):
        return dict(status.__dict__)
    return {"repr": repr(status)}
