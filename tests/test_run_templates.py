from pathlib import Path

import pytest

from wavebench.errors import ConfigError
from wavebench.services.run_plan import load_run_plan
from wavebench.services.run_templates import list_run_templates, render_run_template, write_run_template


def test_list_run_templates_includes_public_names():
    names = [item.name for item in list_run_templates()]

    assert names == ["dmm-acv-source", "power-dmm-dcv", "source-scope-sine"]


@pytest.mark.parametrize("name", ["source-scope-sine", "dmm-acv-source", "power-dmm-dcv"])
def test_run_templates_render_valid_plans(tmp_path: Path, name: str):
    output = write_run_template(name, tmp_path / f"{name}.toml")

    plan = load_run_plan(output)

    assert plan.name
    assert plan.steps
    assert render_run_template(name).endswith("\n")


def test_write_run_template_refuses_overwrite_without_force(tmp_path: Path):
    output = write_run_template("source-scope-sine", tmp_path / "plan.toml")

    with pytest.raises(ConfigError, match="--force"):
        write_run_template("source-scope-sine", output)


def test_write_run_template_overwrites_with_force(tmp_path: Path):
    output = tmp_path / "plan.toml"
    output.write_text("old", encoding="utf-8")

    write_run_template("power-dmm-dcv", output, force=True)

    assert "power_dmm_dcv_smoke" in output.read_text(encoding="utf-8")


def test_unknown_run_template_reports_choices():
    with pytest.raises(ConfigError, match="unknown run template"):
        render_run_template("missing")
