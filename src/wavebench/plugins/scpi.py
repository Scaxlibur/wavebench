from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import tomllib

from wavebench.errors import ConfigError

from .api import SUPPORTED_PLUGIN_API_VERSION, InstrumentPlugin
from .registry import PluginRegistry, plugin_doctor_records


@dataclass(frozen=True)
class DeclarativeScpiPlugin:
    plugin: InstrumentPlugin
    idn_query: str


def load_scpi_plugin(path: str | Path) -> DeclarativeScpiPlugin:
    plugin_path = Path(path)
    try:
        raw = tomllib.loads(plugin_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"unable to read SCPI plugin {plugin_path}: {exc}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"invalid SCPI plugin TOML {plugin_path}: {exc}") from exc
    return _parse_scpi_plugin(raw)


def scpi_plugin_doctor_records(path: str | Path):
    try:
        scpi_plugin = load_scpi_plugin(path)
    except ConfigError as exc:
        subject = str(path)
        return [("error", subject, str(exc))]
    records = plugin_doctor_records(PluginRegistry((scpi_plugin.plugin,)))
    extra_errors = _validate_scpi_query(scpi_plugin.idn_query)
    return [(record.severity, record.subject, record.message) for record in records] + [
        ("error", scpi_plugin.plugin.driver_id, message) for message in extra_errors
    ]


def has_scpi_doctor_errors(records) -> bool:
    return any(record[0] == "error" for record in records)


def _parse_scpi_plugin(raw: Any) -> DeclarativeScpiPlugin:
    if not isinstance(raw, dict):
        raise ConfigError("SCPI plugin file must contain a TOML table")
    scpi = raw.get("scpi", {})
    if not isinstance(scpi, dict):
        raise ConfigError("SCPI plugin field 'scpi' must be a table")
    idn_query = _optional_text(scpi, "idn_query", "*IDN?")
    try:
        plugin = InstrumentPlugin(
            driver_id=_required_text(raw, "driver_id"),
            kind=_required_text(raw, "kind"),
            display_name=_required_text(raw, "display_name"),
            manufacturer=_required_text(raw, "manufacturer"),
            models=_required_text_tuple(raw, "models"),
            capabilities=_required_text_tuple(raw, "capabilities"),
            summary=_required_text(raw, "summary"),
            api_version=_optional_text(raw, "api_version", SUPPORTED_PLUGIN_API_VERSION),
            package=_optional_text(raw, "package", "local"),
            origin="local",
            idn_patterns=_optional_text_tuple(raw, "idn_patterns"),
            config_fields=_optional_text_tuple(raw, "config_fields"),
        )
    except ValueError as exc:
        raise ConfigError(str(exc)) from exc
    return DeclarativeScpiPlugin(plugin=plugin, idn_query=idn_query)


def _required_text(raw: dict[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"SCPI plugin field {key!r} must be a non-empty string")
    return value.strip()


def _optional_text(raw: dict[str, Any], key: str, default: str) -> str:
    value = raw.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"SCPI plugin field {key!r} must be a non-empty string")
    return value.strip()


def _required_text_tuple(raw: dict[str, Any], key: str) -> tuple[str, ...]:
    values = raw.get(key)
    result = _text_tuple(values, key)
    if not result:
        raise ConfigError(f"SCPI plugin field {key!r} must contain at least one string")
    return result


def _optional_text_tuple(raw: dict[str, Any], key: str) -> tuple[str, ...]:
    return _text_tuple(raw.get(key, []), key)


def _text_tuple(values: Any, key: str) -> tuple[str, ...]:
    if not isinstance(values, list):
        raise ConfigError(f"SCPI plugin field {key!r} must be a list")
    result: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(f"SCPI plugin field {key!r} must contain strings")
        result.append(value.strip())
    return tuple(result)


def _validate_scpi_query(command: str) -> list[str]:
    errors: list[str] = []
    if "\n" in command or "\r" in command:
        errors.append("scpi.idn_query must be a single-line command")
    if ";" in command:
        errors.append("scpi.idn_query must not contain command separators")
    if not command.endswith("?"):
        errors.append("scpi.idn_query must be a query ending with '?'")
    return errors
