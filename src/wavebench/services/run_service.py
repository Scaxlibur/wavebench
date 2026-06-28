from __future__ import annotations

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
from wavebench.services.dmm_service import DmmService
from wavebench.services.run_artifacts import RunStepRecord, write_run_files, write_step_record
from wavebench.services.run_analysis import (
    capture_consistency,
    capture_fft_summary,
    evaluate_expect,
    step_status,
)
from wavebench.services.run_plan import RunPlan, RunStep
from wavebench.services.scope_service import ScopeService
from wavebench.services.source_service import SourceService
from wavebench.services.source_state import RestorableSourceState


_EXECUTABLE_STEP_KINDS = {
    "power.status",
    "power.set",
    "power.output",
    "scope.auto",
    "scope.capture",
    "source.status",
    "source.set_freq",
    "source.arb_load",
    "source.set_func",
    "source.set_vpp",
    "source.set_duty",
    "source.output",
    "dmm.read",
    "sleep",
}


@dataclass(frozen=True)
class RunResult:
    run_dir: Path
    run_json_path: Path
    summary_csv_path: Path
    steps: list[RunStepRecord]


@dataclass(frozen=True)
class RunPreflightRecord:
    instrument: str
    resource: str
    idn: str


def run_output_base(config: WaveBenchConfig) -> Path:
    return config.output.directory.parent / "runs"


@dataclass
class RunService:
    config: WaveBenchConfig
    logger: CommandLogger

    def verify(self, plan: RunPlan) -> list[RunPreflightRecord]:
        self.check(plan)
        self._run_safety_guards(plan)
        instruments = self._plan_instruments(plan)
        records: list[RunPreflightRecord] = []
        if "scope" in instruments:
            records.append(
                RunPreflightRecord(
                    instrument="scope",
                    resource=self.config.connection.resource,
                    idn=self._scope_service().idn(),
                )
            )
        if "source" in instruments:
            source = self.config.source
            if source is None or not source.resource:
                raise ConfigError("source resource is required by this run plan")
            records.append(
                RunPreflightRecord(
                    instrument="source",
                    resource=source.resource,
                    idn=self._source_service().idn(),
                )
            )
        if "power" in instruments:
            power = self.config.power
            if power is None or not power.resource:
                raise ConfigError("power resource is required by this run plan")
            records.append(
                RunPreflightRecord(
                    instrument="power",
                    resource=power.resource,
                    idn=self._power_service().idn(),
                )
            )
        if "dmm" in instruments:
            dmm = self.config.dmm
            if dmm is None or not dmm.resource:
                raise ConfigError("dmm resource is required by this run plan")
            records.append(
                RunPreflightRecord(
                    instrument="dmm",
                    resource=dmm.resource,
                    idn=self._dmm_service().idn(),
                )
            )
        return records

    def check(self, plan: RunPlan) -> None:
        self._check_run_plan_safety_limits(plan)
        self._reject_unsupported_steps(plan)

    def _plan_instruments(self, plan: RunPlan) -> set[str]:
        instruments = {step.kind.split(".", 1)[0] for step in plan.steps if "." in step.kind}
        instruments.discard("sleep")
        if plan.restore.source_state:
            instruments.add("source")
        if plan.safety.require_scope_coupling_not:
            instruments.add("scope")
        if self._scope_guard_channels(plan):
            instruments.add("scope")
        return instruments

    def run(self, plan: RunPlan) -> RunResult:
        self._check_run_plan_safety_limits(plan)
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
        restore_state: list[RestorableSourceState] | None = None
        restore_error: dict[str, str] | None = None
        try:
            restore_state = self._snapshot_source_state(plan)
            for step in plan.steps:
                record = self._run_step(plan, step)
                records.append(record)
                write_step_record(steps_dir, record)
        except Exception as exc:
            restore_error = self._restore_source_state(restore_state)
            write_run_files(
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
            write_run_files(
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

        run_status = "failed" if any(record.status == "failed" for record in records) else "ok"
        write_run_files(
            plan=plan,
            run_json_path=run_json_path,
            summary_csv_path=summary_csv_path,
            status=run_status,
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

    def _check_run_plan_safety_limits(self, plan: RunPlan) -> None:
        limits = self.config.safety_limits
        for step in plan.steps:
            if step.kind == "source.set_vpp":
                _check_limit(
                    step.fields["value_vpp"],
                    limits.max_source_vpp,
                    field=f"run step {step.index} source amplitude / 运行步骤 {step.index} 信号源幅度",
                    config_key="max_source_vpp",
                    unit="Vpp",
                )
            elif step.kind == "source.arb_load":
                _check_limit(
                    step.fields["amplitude_vpp"],
                    limits.max_source_vpp,
                    field=f"run step {step.index} arbitrary waveform amplitude / 运行步骤 {step.index} 任意波幅度",
                    config_key="max_source_vpp",
                    unit="Vpp",
                )
            elif step.kind == "power.set":
                _check_limit(
                    step.fields["voltage_v"],
                    limits.max_power_voltage_v,
                    field=f"run step {step.index} power voltage / 运行步骤 {step.index} 电源电压",
                    config_key="max_power_voltage_v",
                    unit="V",
                )
                _check_limit(
                    step.fields["current_limit_a"],
                    limits.max_power_current_limit_a,
                    field=f"run step {step.index} power current limit / 运行步骤 {step.index} 电源限流",
                    config_key="max_power_current_limit_a",
                    unit="A",
                )

    def _scope_guard_channels(self, plan: RunPlan) -> list[int]:
        channels: list[int] = []
        for step in plan.steps:
            if step.kind == "scope.capture":
                channel = step.fields.get("channel") or self.config.scope.default_channel
                if channel not in channels:
                    channels.append(channel)
        return channels

    def _run_safety_guards(self, plan: RunPlan) -> None:
        service = ScopeService(config=self.config, logger=CommandLogger())
        if plan.safety.require_scope_coupling_not:
            if plan.safety.scope_guard_channel is None:  # pragma: no cover - parser enforces this
                raise ConfigError("safety.scope_guard_channel is required")
            channel = plan.safety.scope_guard_channel
            coupling = service.channel_coupling(channel)
            blocked = set(plan.safety.require_scope_coupling_not)
            if coupling.strip().upper() in blocked:
                blocked_text = ", ".join(sorted(blocked))
                raise ConfigError(
                    f"safety guard failed: scope CH{channel} coupling is {coupling}; "
                    f"blocked coupling value(s): {blocked_text}"
                )
        for channel in self._scope_guard_channels(plan):
            service.require_high_impedance(channel, allow_50ohm=plan.safety.allow_50ohm)

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
        elif step.kind == "power.output":
            status = self._power_service().set_output(
                channel=step.fields.get("channel"),
                enabled=step.fields["state"] == "on",
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
        elif step.kind == "source.arb_load":
            status = self._source_service().upload_arbitrary_waveform(
                channel=step.fields.get("channel"),
                file_path=step.fields["file"],
                playback_frequency_hz=step.fields["frequency_hz"],
                amplitude_vpp=step.fields["amplitude_vpp"],
                offset_v=step.fields.get("offset_v", 0.0),
                sample_rate_hz=step.fields.get("sample_rate_hz"),
                max_points=step.fields.get("max_points", 16384),
                byte_order=step.fields.get("byte_order", "little"),
                output_on=step.fields.get("output_on", False),
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
        elif step.kind == "scope.auto":
            self._scope_service().autoscale()
            artifact = {"autoscale": "completed"}
        elif step.kind == "scope.capture":
            artifact = self._run_scope_capture_step(plan, step)
        elif step.kind == "dmm.read":
            reading = self._dmm_service().read(function=step.fields.get("function", "dcv"))
            reading_payload = _status_payload(reading)
            artifact = {"dmm_reading": reading_payload}
            if "expect" in step.fields:
                artifact["expect"] = evaluate_expect(reading_payload, step.fields["expect"])
        elif step.kind == "sleep":
            time.sleep(step.fields["duration_s"])
            artifact = {"duration_s": step.fields["duration_s"]}
        else:  # pragma: no cover - guarded before execution
            raise ConfigError(f"unsupported run step kind: {step.kind}")
        return RunStepRecord(
            index=step.index,
            kind=step.kind,
            status=step_status(artifact),
            fields=step.fields,
            artifact=artifact,
        )

    def _run_scope_capture_step(self, plan: RunPlan, step: RunStep) -> dict[str, Any]:
        service = self._scope_service_for_capture(plan, step)
        channel = step.fields.get("channel", self.config.scope.default_channel)
        label = step.fields.get("label", f"{plan.label}_{step.index:02d}_capture")
        capture = service.capture_waveform(channel=channel, label=label)
        artifact = self._capture_artifact(capture, service)

        quality_gate = step.fields.get("quality_gate", False)
        auto_recover = step.fields.get("auto_recover", False)
        warnings = list(artifact["quality"]["warnings"])
        if (quality_gate or auto_recover) and warnings and auto_recover:
            artifacts = [artifact]
            attempts: list[dict[str, Any]] = [self._recovery_attempt_record(0, "initial", artifact)]
            consistency = capture_consistency(artifacts, self.config.quality)
            for attempt in range(1, self.config.quality.auto_recover_attempts + 1):
                service.autoscale()
                retry = service.capture_waveform(
                    channel=channel, label=f"{label}_auto_retry{attempt}"
                )
                artifact = self._capture_artifact(retry, service)
                artifacts.append(artifact)
                attempts.append(self._recovery_attempt_record(attempt, "auto_retry", artifact))
                if not artifact["quality"]["warnings"]:
                    consistency = capture_consistency(artifacts, self.config.quality)
                    break
                consistency = capture_consistency(artifacts, self.config.quality)
                if consistency["status"] == "consistent":
                    artifact["quality"] = {
                        **artifact["quality"],
                        "status": "ok_by_consistency",
                        "trusted_by_consistency": True,
                    }
                    break
            artifact["quality_recovery"] = {
                "trigger": "quality_warnings",
                "max_auto_recover_attempts": self.config.quality.auto_recover_attempts,
                "attempts": attempts,
                "consistency": consistency,
            }
        elif quality_gate:
            artifact["quality_gate"] = {
                "status": "warning" if warnings else "ok",
                "warnings": warnings,
            }
        if "expect" in step.fields:
            artifact["expect"] = evaluate_expect(artifact.get("quality", {}), step.fields["expect"])
        if "expect_fft" in step.fields:
            fft_summary = capture_fft_summary(capture)
            artifact["fft"] = fft_summary
            artifact["expect_fft"] = evaluate_expect(fft_summary, step.fields["expect_fft"])
        return artifact

    def _recovery_attempt_record(
        self, index: int, kind: str, artifact: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "index": index,
            "kind": kind,
            "package": artifact["package"],
            "metadata": artifact["metadata"],
            "quality": artifact["quality"],
        }

    def _capture_artifact(self, capture: Any, service: ScopeService) -> dict[str, Any]:
        summary = capture.waveform.summary(
            expected_frequency_hz=service.config.waveform.expected_frequency_hz,
            frequency_tolerance_ratio=service.config.waveform.frequency_tolerance_ratio,
        )
        return {
            "package": str(capture.package_dir),
            "metadata": str(capture.metadata_path),
            "quality": {
                "status": "warning" if summary.get("quality_warnings") else "ok",
                "warnings": list(summary.get("quality_warnings", [])),
                "frequency_estimate_hz": summary.get("frequency_estimate_hz"),
                "estimated_cycles": summary.get("estimated_cycles"),
                "points_per_cycle": summary.get("points_per_cycle"),
                "voltage_vpp_v": summary.get("voltage_vpp_v"),
                "voltage_mean_v": summary.get("voltage_mean_v"),
                "duty_cycle": summary.get("duty_cycle"),
                "frequency_error_ratio": summary.get("frequency_error_ratio"),
            },
        }

    def _power_service(self) -> PowerService:
        return PowerService(config=self.config, logger=CommandLogger())

    def _source_service(self) -> SourceService:
        return SourceService(config=self.config, logger=CommandLogger())

    def _dmm_service(self) -> DmmService:
        return DmmService(config=self.config, logger=CommandLogger())

    def _scope_service(self) -> ScopeService:
        return ScopeService(config=self.config, logger=CommandLogger())

    def _snapshot_source_state(self, plan: RunPlan) -> list[RestorableSourceState] | None:
        if not plan.restore.source_state:
            return None
        service = self._source_service()
        channels = plan.restore.source_channels or (None,)
        return [service.snapshot_restorable_state(channel=channel) for channel in channels]

    def _restore_source_state(
        self, states: list[RestorableSourceState] | None
    ) -> dict[str, Any] | None:
        if not states:
            return None
        errors: list[dict[str, str | int | None]] = []
        service = self._source_service()
        for state in states:
            try:
                service.restore_restorable_state(state)
            except Exception as exc:  # pragma: no cover - defensive, covered through mocks
                errors.append(
                    {"channel": state.channel, "type": type(exc).__name__, "message": str(exc)}
                )
        if errors:
            return {
                "type": "RestoreError",
                "message": "source state restore failed",
                "errors": errors,
            }
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
                vertical_scale_v_per_div=step.fields.get("vertical_scale_v_per_div"),
                target_vpp=step.fields.get("target_vpp"),
            )
        if "save_csv" in step.fields or "save_npy" in step.fields or "screenshot" in step.fields:
            config = config.with_output_overrides(
                save_csv=step.fields.get("save_csv"),
                save_npy=step.fields.get("save_npy"),
                save_screenshot=step.fields.get("screenshot"),
            )
        return ScopeService(config=config, logger=CommandLogger())


def _check_limit(
    value: float | None, limit: float | None, *, field: str, config_key: str, unit: str
) -> None:
    if value is None or limit is None:
        return
    if value > limit:
        raise ConfigError(
            f"safety limit exceeded / 安全上限已超出: {field} {value:.12g} {unit} "
            f"> {config_key} {limit:.12g} {unit}"
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
            "vertical_scale_v_per_div",
            "target_vpp",
        )
    )


def _status_payload(status: Any) -> dict[str, Any]:
    if hasattr(status, "as_dict"):
        return status.as_dict()
    if hasattr(status, "__dict__"):
        return dict(status.__dict__)
    return {"repr": repr(status)}
