from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import difflib
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
        "quality_gate",
        "auto_recover",
        "expect",
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


_STEP_NOTES = {
    "scope.auto": "Explicit RTM2032 AUToscale. It changes front-panel settings and is never inserted implicitly.",
    "scope.capture": "Trigger one acquisition, write a capture package, and optionally evaluate quality/expect checks.",
    "source.status": "Read signal-generator channel state without changing output.",
    "source.set_freq": "Set fixed source frequency in Hz; config may force FIX mode first.",
    "source.set_func": "Set source waveform function, for example SIN or SQU.",
    "source.set_vpp": "Set source amplitude in Vpp.",
    "source.set_duty": "Set square-wave duty cycle in percent; valid range is 0 < duty_percent < 100.",
    "source.output": "Turn source channel output on or off.",
    "power.status": "Read power-supply channel state without changing output.",
    "power.set": "Set DP800 voltage/current limit; does not change output state.",
    "power.output": "Turn power-supply channel output on or off; does not change voltage/current limit.",
    "sleep": "Wait between hardware actions.",
}


@dataclass(frozen=True)
class StepSchema:
    kind: str
    required: tuple[str, ...]
    optional: frozenset[str]
    notes: str = ""


STEP_SCHEMAS = {
    kind: StepSchema(
        kind=kind,
        required=_REQUIRED_FIELDS.get(kind, ()),
        optional=frozenset(_OPTIONAL_FIELDS.get(kind, set())),
        notes=_STEP_NOTES.get(kind, ""),
    )
    for kind in sorted(ALLOWED_STEP_KINDS)
}


def run_plan_schema_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for schema in STEP_SCHEMAS.values():
        required = ", ".join(schema.required) or "-"
        optional = ", ".join(sorted(schema.optional)) or "-"
        rows.append({
            "kind": schema.kind,
            "required": required,
            "optional": optional,
            "notes": schema.notes,
        })
    return rows


def format_run_plan_schema() -> str:
    lines = [
        "WaveBench run plan schema",
        "",
        "Top-level tables:",
        "  [experiment] optional: name, label",
        "  [safety] optional: scope_guard_channel, require_scope_coupling_not",
        "  [restore] optional: source_state, source_channel",
        "  [[steps]] required: kind",
        "",
        "Supported step kinds:",
    ]
    for row in run_plan_schema_rows():
        lines.append(f"  - {row['kind']}")
        lines.append(f"      required: {row['required']}")
        lines.append(f"      optional : {row['optional']}")
        if row["notes"]:
            lines.append(f"      note     : {row['notes']}")
    lines.extend([
        "",
        "scope.capture [steps.expect] metrics:",
        "  Any numeric key from the capture quality summary may be checked with { min = ..., max = ... }.",
        "  Common metrics: frequency_estimate_hz, frequency_error_ratio, voltage_vpp_v, voltage_mean_v, duty_cycle.",
    ])
    return "\n".join(lines)


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
    if not kind:
        raise ConfigError(
            f"steps[{index}].kind is required. Run `python -m wavebench run schema` "
            "to list supported step kinds."
        )
    if kind not in ALLOWED_STEP_KINDS:
        allowed = ", ".join(sorted(ALLOWED_STEP_KINDS))
        closest = difflib.get_close_matches(kind, sorted(ALLOWED_STEP_KINDS), n=1)
        suggestion = f" Did you mean '{closest[0]}'?" if closest else ""
        raise ConfigError(
            f"steps[{index}].kind '{kind}' is not supported.{suggestion} "
            f"Supported kinds: {allowed}. Run `python -m wavebench run schema` for field details."
        )

    schema = STEP_SCHEMAS[kind]
    allowed_fields = {"kind", *schema.required, *schema.optional}
    _reject_unknown_keys(table, allowed_fields, f"steps[{index}]")
    for field in schema.required:
        if field not in table:
            required = ", ".join(schema.required) or "-"
            optional = ", ".join(sorted(schema.optional)) or "-"
            raise ConfigError(
                f"steps[{index}] {kind} missing required field '{field}'. "
                f"Required fields: {required}. Optional fields: {optional}. "
                "Run `python -m wavebench run schema` for examples."
            )

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
        for field in ("save_csv", "save_npy", "quality_gate", "auto_recover"):
            if field in fields and not isinstance(fields[field], bool):
                raise ConfigError(f"{prefix}.{field} must be true or false")
        if "expect" in fields:
            fields["expect"] = _parse_expect(fields["expect"], f"{prefix}.expect")
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


def _parse_expect(raw: Any, name: str) -> dict[str, dict[str, float]]:
    table = _table(raw, name)
    if not table:
        raise ConfigError(f"{name} must not be empty")
    result: dict[str, dict[str, float]] = {}
    for metric, limits_raw in table.items():
        metric_name = _non_empty_str(metric, f"{name} metric")
        limits = _table(limits_raw, f"{name}.{metric_name}")
        _reject_unknown_keys(limits, {"min", "max"}, f"{name}.{metric_name}")
        if "min" not in limits and "max" not in limits:
            raise ConfigError(f"{name}.{metric_name} requires min or max")
        parsed: dict[str, float] = {}
        for key in ("min", "max"):
            if key in limits:
                parsed[key] = _finite_float(limits[key], f"{name}.{metric_name}.{key}")
        if "min" in parsed and "max" in parsed and parsed["min"] > parsed["max"]:
            raise ConfigError(f"{name}.{metric_name}.min must be <= max")
        result[metric_name] = parsed
    return result


def _finite_float(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ConfigError(f"{name} must be a number")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{name} must be a number") from exc
    if result != result or result in (float("inf"), float("-inf")):
        raise ConfigError(f"{name} must be finite")
    return result


def _table(raw: Any, name: str) -> dict[str, Any]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ConfigError(f"{name} must be a TOML table")
    return raw


def _reject_unknown_keys(table: dict[str, Any], allowed: set[str], name: str) -> None:
    unknown = sorted(set(table) - allowed)
    if unknown:
        allowed_text = ", ".join(sorted(allowed)) or "-"
        suggestions = _unknown_key_suggestions(unknown, allowed)
        suggestion_text = f" {suggestions}" if suggestions else ""
        hint = " Run `python -m wavebench run schema` for field details." if name.startswith("steps[") else ""
        raise ConfigError(
            f"{name} has unknown key(s): {', '.join(unknown)}.{suggestion_text} "
            f"Allowed keys: {allowed_text}.{hint}"
        )


def _unknown_key_suggestions(unknown: list[str], allowed: set[str]) -> str:
    parts = []
    choices = sorted(allowed)
    for key in unknown:
        closest = difflib.get_close_matches(key, choices, n=1)
        if closest:
            parts.append(f"'{key}' -> '{closest[0]}'")
    if not parts:
        return ""
    return "Did you mean " + ", ".join(parts) + "?"


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
