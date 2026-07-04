import pytest

from wavebench.errors import ConfigError
from wavebench.plugins.scpi import (
    has_scpi_doctor_errors,
    load_scpi_plugin,
    scpi_plugin_doctor_records,
)


def write_scpi_plugin(path, text=None):
    path.write_text(
        text
        or """
driver_id = "example.scope"
kind = "scope"
display_name = "Example Scope"
manufacturer = "Example"
models = ["EX1"]
capabilities = ["scope.idn"]
summary = "Example declarative SCPI plugin."
idn_patterns = ["EXAMPLE,EX1"]
config_fields = ["resource"]

[scpi]
idn_query = "*IDN?"
""".strip(),
        encoding="utf-8",
    )


def test_load_scpi_plugin_returns_local_instrument_plugin(tmp_path):
    path = tmp_path / "plugin.toml"
    write_scpi_plugin(path)

    scpi_plugin = load_scpi_plugin(path)

    assert scpi_plugin.plugin.driver_id == "example.scope"
    assert scpi_plugin.plugin.kind == "scope"
    assert scpi_plugin.plugin.origin == "local"
    assert scpi_plugin.plugin.package == "local"
    assert scpi_plugin.idn_query == "*IDN?"


def test_load_scpi_plugin_rejects_missing_required_field(tmp_path):
    path = tmp_path / "plugin.toml"
    write_scpi_plugin(
        path,
        """
kind = "scope"
display_name = "Example Scope"
manufacturer = "Example"
models = ["EX1"]
capabilities = ["scope.idn"]
summary = "Example declarative SCPI plugin."
""".strip(),
    )

    with pytest.raises(ConfigError, match="field 'driver_id' must be a non-empty string"):
        load_scpi_plugin(path)


def test_scpi_plugin_doctor_accepts_valid_plugin(tmp_path):
    path = tmp_path / "plugin.toml"
    write_scpi_plugin(path)

    records = scpi_plugin_doctor_records(path)

    assert records == [("ok", "example.scope", "metadata valid")]
    assert not has_scpi_doctor_errors(records)


def test_scpi_plugin_doctor_rejects_write_command_idn_query(tmp_path):
    path = tmp_path / "plugin.toml"
    write_scpi_plugin(
        path,
        """
driver_id = "example.scope"
kind = "scope"
display_name = "Example Scope"
manufacturer = "Example"
models = ["EX1"]
capabilities = ["scope.idn"]
summary = "Example declarative SCPI plugin."

[scpi]
idn_query = "OUTP ON"
""".strip(),
    )

    records = scpi_plugin_doctor_records(path)

    assert has_scpi_doctor_errors(records)
    assert ("error", "example.scope", "scpi.idn_query must be a query ending with '?'") in records


def test_scpi_plugin_doctor_reports_invalid_toml(tmp_path):
    path = tmp_path / "plugin.toml"
    path.write_text("driver_id = [", encoding="utf-8")

    records = scpi_plugin_doctor_records(path)

    assert has_scpi_doctor_errors(records)
    assert records[0][0] == "error"
    assert str(path) in records[0][1]
