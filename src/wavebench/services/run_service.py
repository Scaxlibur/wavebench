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
from wavebench.services.source_service import SourceService
from wavebench.services.source_state import RestorableSourceState


_EXECUTABLE_STEP_KINDS = {
    "power.status",
    "power.set",
    "scope.capture",
    "source.status",
    "source.set_freq",
    "source.set_func",
    "source.set_vpp",
    "source.set_duty",
    "source.output",
    "sleep",
}


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
        self._run_safety_guards(plan)
        self._reject_unsupported_steps(plan)
        run_dir = new_package_dir(run_output_base(self.config), plan.label)
        steps_dir = run_dir / "steps"
        steps_dir.mkdir(parents=True, exist_ok=False)
        if plan.path.exists():
            shutil.copyfile(plan.path, run_dir / "plan.toml")

        records: list[RunStepRecord] = []
        run_json_path = run_dir / "run.json"
        summary_csv_path = run_dir / "summary.csv"
        restore_state: RestorableSourceState | None = None
        restore_error: dict[str, str] | None = None
        try:
            restore_state = self._snapshot_source_state(plan)
            for step in plan.steps:
                record = self._run_step(plan, step)
                records.append(record)
                self._write_step_record(steps_dir, record)
        except Exception as exc:
            restore_error = self._restore_source_state(restore_state)
            self._write_run_files(
                plan=plan,
                run_json_path=run_json_path,
                summary_csv_path=summary_csv_path,
                status="failed",
                records=records,
                error={"type": type(exc).__name__, "message": str(exc)},
                restore_state=restore_state,
                restore_error=restore_error,
            )
            if isinstance(exc, WaveBenchError):
                raise
            raise

        restore_error = self._restore_source_state(restore_state)
        if restore_error is not None:
            self._write_run_files(
                plan=plan,
                run_json_path=run_json_path,
                summary_csv_path=summary_csv_path,
                status="failed",
                records=records,
                error={"type": "ConfigError", "message": "source state restore failed"},
                restore_state=restore_state,
                restore_error=restore_error,
            )
            raise ConfigError("run plan source state restore failed: " + restore_error["message"])

        self._write_run_files(
            plan=plan,
            run_json_path=run_json_path,
            summary_csv_path=summary_csv_path,
            status="ok",
            records=records,
            error=None,
            restore_state=restore_state,
            restore_error=None,
        )
        return RunResult(
            run_dir=run_dir,
            run_json_path=run_json_path,
            summary_csv_path=summary_csv_path,
            steps=records,
        )

    def _run_safety_guards(self, plan: RunPlan) -> None:
        if not plan.safety.require_scope_coupling_not:
            return
        if plan.safety.scope_guard_channel is None:  # pragma: no cover - parser enforces this
            raise ConfigError("safety.scope_guard_channel is required")
        channel = plan.safety.scope_guard_channel
        coupling = ScopeService(config=self.config, logger=CommandLogger()).channel_coupling(channel)
        blocked = set(plan.safety.require_scope_coupling_not)
        if coupling.strip().upper() in blocked:
            blocked_text = ", ".join(sorted(blocked))
            raise ConfigError(
                f"safety guard failed: scope CH{channel} coupling is {coupling}; "
                f"blocked coupling value(s): {blocked_text}"
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
        elif step.kind == "source.status":
            status = self._source_service().status(channel=step.fields.get("channel"))
            artifact = {"source_status": _status_payload(status)}
        elif step.kind == "source.set_freq":
            status = self._source_service().set_frequency(
                channel=step.fields.get("channel"),
                value_hz=step.fields["frequency_hz"],
            )
            artifact = {"source_status": _status_payload(status)}
        elif step.kind == "source.set_func":
            status = self._source_service().set_function(
                channel=step.fields.get("channel"),
                function=step.fields["function"],
            )
            artifact = {"source_status": _status_payload(status)}
        elif step.kind == "source.set_vpp":
            status = self._source_service().set_amplitude_vpp(
                channel=step.fields.get("channel"),
                value_vpp=step.fields["value_vpp"],
            )
            artifact = {"source_status": _status_payload(status)}
        elif step.kind == "source.set_duty":
            status = self._source_service().set_square_duty_cycle(
                channel=step.fields.get("channel"),
                duty_percent=step.fields["duty_percent"],
            )
            artifact = {"source_status": _status_payload(status)}
        elif step.kind == "source.output":
            status = self._source_service().set_output(
                channel=step.fields.get("channel"),
                enabled=step.fields["state"] == "on",
            )
            artifact = {"source_status": _status_payload(status)}
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

    def _source_service(self) -> SourceService:
        return SourceService(config=self.config, logger=CommandLogger())

    def _snapshot_source_state(self, plan: RunPlan) -> RestorableSourceState | None:
        if not plan.restore.source_state:
            return None
        return self._source_service().snapshot_restorable_state(channel=plan.restore.source_channel)

    def _restore_source_state(self, state: RestorableSourceState | None) -> dict[str, str] | None:
        if state is None:
            return None
        try:
            self._source_service().restore_restorable_state(state)
        except Exception as exc:  # pragma: no cover - defensive, covered through mocks
            return {"type": type(exc).__name__, "message": str(exc)}
        return None

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
        restore_state: RestorableSourceState | None = None,
        restore_error: dict[str, str] | None = None,
    ) -> None:
        run_data: dict[str, Any] = {
            "status": status,
            "experiment": {"name": plan.name, "label": plan.label},
            "plan": str(plan.path),
            "steps": [record.as_dict() for record in records],
        }
        if restore_state is not None:
            run_data["restore"] = {
                "source_state": True,
                "source_channel": restore_state.channel,
                "snapshot": restore_state.as_dict(),
                "status": "failed" if restore_error is not None else "ok",
            }
            if restore_error is not None:
                run_data["restore"]["error"] = restore_error
        elif plan.restore.source_state:
            run_data["restore"] = {
                "source_state": True,
                "source_channel": plan.restore.source_channel,
                "status": "not_started",
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
