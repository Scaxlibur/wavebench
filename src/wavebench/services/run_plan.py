from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import tomllib

from wavebench.config import normalize_waveform_points
from wavebench.errors import ConfigError


ALLOWED_STEP_KINDS = {
    "scope.auto",
    "scope.capture",
    "source.status",
    "source.set_freq",
    "source.set_func",
    "source.set_vpp",
    "source.set_duty",
    "source.output",
    "power.status",
    "power.set",
    "power.output",
    "sleep",
}

_REQUIRED_FIELDS = {
    "power.set": ("voltage_v", "current_limit_a"),
    "power.output": ("state",),
    "source.set_freq": ("frequency_hz",),
    "source.set_func": ("function",),
    "source.set_vpp": ("value_vpp",),
    "source.set_duty": ("duty_percent",),
    "source.output": ("state",),
    "sleep": ("duration_s",),
}

_OPTIONAL_FIELDS = {
    "scope.auto": set(),
    "scope.capture": {
        "channel",
        "label",
        "points",
        "time_range_s",
        "expect_frequency_hz",
        "window_frequency_hz",
        "target_cycles",
        "frequency_tolerance",
        "save_csv",
        "save_npy",
    },
    "source.status": {"channel"},
    "source.set_freq": {"channel"},
    "source.set_func": {"channel"},
    "source.set_vpp": {"channel"},
    "source.set_duty": {"channel"},
    "source.output": {"channel"},
    "power.status": {"channel"},
    "power.set": {"channel"},
    "power.output": {"channel"},
    "sleep": set(),
}


@dataclass(frozen=True)
class SafetyGuard:
    scope_guard_channel: int | None
    require_scope_coupling_not: tuple[str, ...]


@dataclass(frozen=True)
class SourceRestorePolicy:
    source_state: bool
    source_channel: int | None


@dataclass(frozen=True)
class RunStep:
    index: int
    kind: str
    fields: dict[str, Any]


@dataclass(frozen=True)
class RunPlan:
    path: Path
    name: str
    label: str
    safety: SafetyGuard
    restore: SourceRestorePolicy
    steps: list[RunStep]


def load_run_plan(path: str | Path) -> RunPlan:
    plan_path = Path(path)
    if not plan_path.exists():
        raise ConfigError(f"run plan not found: {plan_path}")
    try:
        raw = tomllib.loads(plan_path.read_bytes().decode("utf-8-sig"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"invalid TOML in {plan_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError("run plan must be a TOML table")

    experiment = _table(raw.get("experiment", {}), "experiment")
    name = str(experiment.get("name", plan_path.stem)).strip()
    label = str(experiment.get("label", name)).strip()
    if not name:
        raise ConfigError("experiment.name must not be empty")
    if not label:
        raise ConfigError("experiment.label must not be empty")

    safety = _parse_safety(raw.get("safety", {}))
    restore = _parse_restore(raw.get("restore", {}))
    steps_raw = raw.get("steps")
    if not isinstance(steps_raw, list) or not steps_raw:
        raise ConfigError("run plan requires at least one [[steps]] entry")
    steps = [_parse_step(index, item) for index, item in enumerate(steps_raw)]
    return RunPlan(path=plan_path, name=name, label=label, safety=safety, restore=restore, steps=steps)


def _parse_restore(raw: Any) -> SourceRestorePolicy:
    table = _table(raw, "restore")
    allowed = {"source_state", "source_channel"}
    _reject_unknown_keys(table, allowed, "restore")

    source_state = table.get("source_state", False)
    if not isinstance(source_state, bool):
        raise ConfigError("restore.source_state must be true or false")
    source_channel = table.get("source_channel")
    if source_channel is not None:
        source_channel = _positive_int(source_channel, "restore.source_channel")
    if source_channel is not None and not source_state:
        raise ConfigError("restore.source_channel requires restore.source_state = true")
    return SourceRestorePolicy(source_state=source_state, source_channel=source_channel)


def _parse_safety(raw: Any) -> SafetyGuard:
    table = _table(raw, "safety")
    allowed = {"scope_guard_channel", "require_scope_coupling_not"}
    _reject_unknown_keys(table, allowed, "safety")

    channel = table.get("scope_guard_channel")
    if channel is not None:
        channel = _positive_int(channel, "safety.scope_guard_channel")

    blocked_raw = table.get("require_scope_coupling_not", [])
    if isinstance(blocked_raw, str):
        blocked = (blocked_raw.strip().upper(),)
    elif isinstance(blocked_raw, list):
        blocked = tuple(str(item).strip().upper() for item in blocked_raw)
    else:
        raise ConfigError("safety.require_scope_coupling_not must be a string or list of strings")
    if any(not item for item in blocked):
        raise ConfigError("safety.require_scope_coupling_not entries must not be empty")
    if blocked and channel is None:
        raise ConfigError(
            "safety.scope_guard_channel is required when require_scope_coupling_not is set"
        )
    return SafetyGuard(scope_guard_channel=channel, require_scope_coupling_not=blocked)


def _parse_step(index: int, raw: Any) -> RunStep:
    table = _table(raw, f"steps[{index}]")
    kind = str(table.get("kind", "")).strip()
    if kind not in ALLOWED_STEP_KINDS:
        allowed = ", ".join(sorted(ALLOWED_STEP_KINDS))
        raise ConfigError(f"steps[{index}].kind must be one of: {allowed}")

    allowed_fields = {"kind", *_REQUIRED_FIELDS.get(kind, ()), *_OPTIONAL_FIELDS.get(kind, set())}
    _reject_unknown_keys(table, allowed_fields, f"steps[{index}]")
    for field in _REQUIRED_FIELDS.get(kind, ()):
        if field not in table:
            raise ConfigError(f"steps[{index}] {kind} requires {field}")

    fields = {key: value for key, value in table.items() if key != "kind"}
    _normalize_step_fields(index, kind, fields)
    return RunStep(index=index, kind=kind, fields=fields)


def _normalize_step_fields(index: int, kind: str, fields: dict[str, Any]) -> None:
    prefix = f"steps[{index}]"
    if "channel" in fields:
        fields["channel"] = _positive_int(fields["channel"], f"{prefix}.channel")
    if kind == "scope.capture":
        if "label" in fields:
            fields["label"] = _non_empty_str(fields["label"], f"{prefix}.label")
        if "points" in fields:
            fields["points"] = normalize_waveform_points(
                _non_empty_str(fields["points"], f"{prefix}.points")
            )
        for field in (
            "time_range_s",
            "expect_frequency_hz",
            "window_frequency_hz",
            "target_cycles",
            "frequency_tolerance",
        ):
            if field in fields:
                fields[field] = _positive_float(fields[field], f"{prefix}.{field}")
        if "target_cycles" in fields:
            window_frequency = fields.get("window_frequency_hz") or fields.get("expect_frequency_hz")
            if window_frequency is None:
                raise ConfigError(
                    f"{prefix}.target_cycles requires window_frequency_hz or expect_frequency_hz"
                )
            if "time_range_s" not in fields:
                fields["time_range_s"] = fields["target_cycles"] / window_frequency
        for field in ("save_csv", "save_npy"):
            if field in fields and not isinstance(fields[field], bool):
                raise ConfigError(f"{prefix}.{field} must be true or false")
    elif kind == "power.set":
        fields["voltage_v"] = _positive_float(fields["voltage_v"], f"{prefix}.voltage_v")
        fields["current_limit_a"] = _positive_float(
            fields["current_limit_a"], f"{prefix}.current_limit_a"
        )
    elif kind in {"power.output", "source.output"}:
        state = _non_empty_str(fields["state"], f"{prefix}.state").lower()
        if state not in {"on", "off"}:
            raise ConfigError(f"{prefix}.state must be 'on' or 'off'")
        fields["state"] = state
    elif kind == "source.set_freq":
        fields["frequency_hz"] = _positive_float(fields["frequency_hz"], f"{prefix}.frequency_hz")
    elif kind == "source.set_func":
        fields["function"] = _non_empty_str(fields["function"], f"{prefix}.function")
    elif kind == "source.set_vpp":
        fields["value_vpp"] = _positive_float(fields["value_vpp"], f"{prefix}.value_vpp")
    elif kind == "source.set_duty":
        fields["duty_percent"] = _duty_percent(fields["duty_percent"], f"{prefix}.duty_percent")
    elif kind == "sleep":
        fields["duration_s"] = _positive_float(fields["duration_s"], f"{prefix}.duration_s")


def _table(raw: Any, name: str) -> dict[str, Any]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ConfigError(f"{name} must be a TOML table")
    return raw


def _reject_unknown_keys(table: dict[str, Any], allowed: set[str], name: str) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        raise ConfigError(f"{name} has unknown key(s): {', '.join(unknown)}")


def _positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ConfigError(f"{name} must be a positive integer")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{name} must be a positive integer") from exc
    if result < 1:
        raise ConfigError(f"{name} must be >= 1")
    return result


def _positive_float(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ConfigError(f"{name} must be a positive number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{name} must be a positive number") from exc
    if result <= 0:
        raise ConfigError(f"{name} must be > 0")
    return result


def _non_empty_str(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ConfigError(f"{name} must not be empty")
    return result


def _duty_percent(value: Any, name: str) -> float:
    result = _positive_float(value, name)
    if result >= 100:
        raise ConfigError(f"{name} must be < 100")
    return result
