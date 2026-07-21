from __future__ import annotations

from base64 import urlsafe_b64encode
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import sys
import sysconfig
import venv
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from wavebench.errors import ConfigError
from wavebench.plugins.lifecycle import PluginLifecycle


def _run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=check)


def _target_venv(root: Path) -> Path:
    target = root / "venv"
    venv.EnvBuilder(with_pip=True).create(target)
    python = target / "bin" / "python"
    purelib = _run(
        [str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"]
    ).stdout.strip()
    Path(purelib, "wavebench-test-runtime.pth").write_text(
        str(Path(__file__).resolve().parents[1] / "src")
        + "\n"
        + sysconfig.get_paths()["purelib"]
        + "\n",
        encoding="utf-8",
    )
    return python


def _plugin_wheel(
    root: Path,
    *,
    version: str,
    driver_id: str = "example.scope",
    distribution: str = "wavebench-example-scope",
    broken_descriptor: bool = False,
    include_entry_point: bool = True,
) -> Path:
    filename_name = distribution.replace("-", "_")
    dist_info = f"{filename_name}-{version}.dist-info"
    package_name = "wavebench_example_scope"
    path = root / f"{filename_name}-{version}-py3-none-any.whl"
    metadata = (
        "Metadata-Version: 2.1\n"
        f"Name: {distribution}\n"
        f"Version: {version}\n"
        "Requires-Python: >=3.11\n"
        "Requires-Dist: wavebench>=0.7,<1\n\n"
    ).encode()
    if broken_descriptor:
        package = b"def descriptor():\n    raise RuntimeError('broken descriptor')\n"
    else:
        package = f'''from wavebench.instruments.api import InstrumentDescriptor


class Driver:
    def idn(self):
        return "EXAMPLE,SCOPE"

    def close(self):
        pass


def descriptor():
    return InstrumentDescriptor(
        driver_id={driver_id!r},
        kind="scope",
        display_name="Example Scope",
        manufacturer="Example",
        models=("EX1",),
        aliases=(),
        capabilities=("scope.idn",),
        idn_patterns=("EXAMPLE,SCOPE",),
        backends=("pyvisa",),
        option_specs=(),
        permissions=("instrument.io",),
        factory=lambda context: Driver(),
    )
'''.encode()
    members = {
        f"{dist_info}/METADATA": metadata,
        f"{dist_info}/WHEEL": (
            b"Wheel-Version: 1.0\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
        ),
        f"{package_name}/__init__.py": package,
    }
    if include_entry_point:
        members[f"{dist_info}/entry_points.txt"] = (
            f"[wavebench.instruments]\n{driver_id} = {package_name}:descriptor\n"
        ).encode()
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    for member, payload in members.items():
        digest = urlsafe_b64encode(sha256(payload).digest()).rstrip(b"=").decode()
        writer.writerow((member, f"sha256={digest}", len(payload)))
    writer.writerow((f"{dist_info}/RECORD", "", ""))
    members[f"{dist_info}/RECORD"] = output.getvalue().encode()
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        for member, payload in members.items():
            archive.writestr(member, payload)
    return path


def _raw_pip_install(python: Path, wheel: Path) -> None:
    _run(
        [
            str(python),
            "-I",
            "-m",
            "pip",
            "install",
            "--isolated",
            "--no-index",
            "--no-deps",
            "--disable-pip-version-check",
            str(wheel),
        ]
    )


def _plugin_source(root: Path) -> Path:
    source = root / "source-plugin"
    package = source / "src" / "wavebench_source_scope"
    package.mkdir(parents=True)
    (source / "pyproject.toml").write_text(
        """
[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[project]
name = "wavebench-source-scope"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["wavebench>=0.7,<1"]

[project.entry-points."wavebench.instruments"]
"example.source-scope" = "wavebench_source_scope:descriptor"

[tool.hatch.build.targets.wheel]
packages = ["src/wavebench_source_scope"]
""",
        encoding="utf-8",
    )
    (package / "__init__.py").write_text(
        '''from wavebench.instruments.api import InstrumentDescriptor


class Driver:
    def idn(self):
        return "EXAMPLE,SOURCE-SCOPE"

    def close(self):
        pass


def descriptor():
    return InstrumentDescriptor(
        driver_id="example.source-scope",
        kind="scope",
        display_name="Example Source Scope",
        manufacturer="Example",
        models=("EX1",),
        aliases=(),
        capabilities=("scope.idn",),
        idn_patterns=("EXAMPLE,SOURCE-SCOPE",),
        backends=("pyvisa",),
        option_specs=(),
        permissions=("instrument.io",),
        factory=lambda context: Driver(),
    )
''',
        encoding="utf-8",
    )
    return source


def test_lifecycle_rejects_system_python():
    lifecycle = PluginLifecycle(python_executable=Path(sys.base_prefix) / "bin" / "python3")

    with pytest.raises(ConfigError, match="virtual environment"):
        lifecycle.installed()


def test_lifecycle_preserves_venv_launcher_path(tmp_path):
    python = _target_venv(tmp_path)
    launcher = python.parent / "wavebench-python-link"
    launcher.symlink_to("python")
    lifecycle = PluginLifecycle(python_executable=launcher)

    environment = lifecycle.environment()

    assert environment.prefix == str(python.parents[1])
    assert Path(environment.python) == launcher


def test_dry_run_does_not_modify_target_venv(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)

    result = lifecycle.install(wheel, dry_run=True)

    assert result.status == "would-install"
    assert not (python.parents[1] / ".wavebench").exists()
    assert lifecycle.installed() == ()


def test_dry_run_refuses_unmanaged_distribution_without_writing_state(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    _raw_pip_install(python, wheel)
    lifecycle = PluginLifecycle(python_executable=python)

    with pytest.raises(ConfigError, match="unmanaged"):
        lifecycle.install(wheel, dry_run=True)

    assert not lifecycle.state_dir.exists()


def test_install_status_and_remove_round_trip(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)

    installed = lifecycle.install(wheel)
    statuses = lifecycle.installed()

    assert installed.status == "installed"
    assert [(item.driver_id, item.version, item.status) for item in statuses] == [
        ("example.scope", "0.1.0", "healthy")
    ]
    assert lifecycle.info("example.scope").wheel_sha256 == sha256(wheel.read_bytes()).hexdigest()
    assert lifecycle.remove("example.scope").status == "removed"
    assert lifecycle.installed() == ()


def test_source_directory_install_keeps_built_wheel_alive_until_cached(tmp_path):
    python = _target_venv(tmp_path)
    source = _plugin_source(tmp_path)
    lifecycle = PluginLifecycle(python_executable=python)

    installed = lifecycle.install(source)

    assert installed.driver_id == "example.source-scope"
    assert lifecycle.info("example.source-scope").status == "healthy"
    assert lifecycle.remove("example.source-scope").status == "removed"


def test_install_refuses_to_take_over_unmanaged_distribution(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    _raw_pip_install(python, wheel)
    lifecycle = PluginLifecycle(python_executable=python)

    assert lifecycle.installed()[0].status == "unmanaged"
    with pytest.raises(ConfigError, match="unmanaged"):
        lifecycle.install(wheel)


def test_install_refuses_file_owned_by_another_distribution(tmp_path):
    python = _target_venv(tmp_path)
    foreign = _plugin_wheel(
        tmp_path,
        version="0.1.0",
        distribution="foreign-scope-plugin",
        include_entry_point=False,
    )
    target = _plugin_wheel(tmp_path, version="0.1.0")
    _raw_pip_install(python, foreign)
    lifecycle = PluginLifecycle(python_executable=python)

    with pytest.raises(ConfigError, match="overlaps files"):
        lifecycle.install(target, dry_run=True)

    assert not lifecycle.state_dir.exists()


def test_install_refuses_unreadable_distribution_ownership(tmp_path):
    python = _target_venv(tmp_path)
    foreign = _plugin_wheel(
        tmp_path,
        version="0.1.0",
        distribution="foreign-scope-plugin",
        include_entry_point=False,
    )
    target = _plugin_wheel(tmp_path, version="0.1.0")
    _raw_pip_install(python, foreign)
    purelib = Path(
        _run(
            [str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"]
        ).stdout.strip()
    )
    record = next(purelib.glob("foreign_scope_plugin-*.dist-info/RECORD"))
    record.write_bytes(record.read_bytes() + b"\n")
    lifecycle = PluginLifecycle(python_executable=python)

    with pytest.raises(ConfigError, match="ownership cannot be proven"):
        lifecycle.install(target, dry_run=True)

    assert not lifecycle.state_dir.exists()


def test_install_refuses_distribution_without_record(tmp_path):
    python = _target_venv(tmp_path)
    foreign = _plugin_wheel(
        tmp_path,
        version="0.1.0",
        distribution="foreign-scope-plugin",
        include_entry_point=False,
    )
    target = _plugin_wheel(tmp_path, version="0.1.0")
    _raw_pip_install(python, foreign)
    purelib = Path(
        _run(
            [str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"]
        ).stdout.strip()
    )
    next(purelib.glob("foreign_scope_plugin-*.dist-info/RECORD")).unlink()
    lifecycle = PluginLifecycle(python_executable=python)

    with pytest.raises(ConfigError, match="ownership cannot be proven"):
        lifecycle.install(target, dry_run=True)

    assert not lifecycle.state_dir.exists()


def test_remove_refuses_files_shared_with_out_of_band_distribution(tmp_path):
    python = _target_venv(tmp_path)
    managed = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    lifecycle.install(managed)
    foreign = _plugin_wheel(
        tmp_path,
        version="0.1.0",
        distribution="foreign-scope-plugin",
        include_entry_point=False,
    )
    _raw_pip_install(python, foreign)

    installed = lifecycle.info("example.scope")
    assert installed.status == "broken"
    assert "shared ownership" in installed.detail
    with pytest.raises(ConfigError, match="healthy"):
        lifecycle.remove("example.scope", dry_run=True)

    assert lifecycle.info("example.scope").status == "broken"


def test_upgrade_downgrade_and_failed_upgrade_roll_back(tmp_path):
    python = _target_venv(tmp_path)
    v1 = _plugin_wheel(tmp_path, version="0.1.0")
    v2 = _plugin_wheel(tmp_path, version="0.2.0")
    broken = _plugin_wheel(tmp_path, version="0.3.0", broken_descriptor=True)
    lifecycle = PluginLifecycle(python_executable=python)
    lifecycle.install(v1)

    assert lifecycle.upgrade(v2).status == "upgraded"
    assert lifecycle.info("example.scope").version == "0.2.0"
    assert lifecycle.downgrade(v1).status == "downgraded"
    assert lifecycle.info("example.scope").version == "0.1.0"

    with pytest.raises(ConfigError, match="postflight"):
        lifecycle.upgrade(broken)

    restored = lifecycle.info("example.scope")
    assert restored.version == "0.1.0"
    assert restored.status == "healthy"
    assert not lifecycle.journal_path.exists()


def test_out_of_band_change_is_reported_as_missing_or_drifted(tmp_path):
    python = _target_venv(tmp_path)
    v1 = _plugin_wheel(tmp_path, version="0.1.0")
    v2 = _plugin_wheel(tmp_path, version="0.2.0")
    lifecycle = PluginLifecycle(python_executable=python)
    lifecycle.install(v1)

    _raw_pip_install(python, v2)
    assert lifecycle.info("example.scope").status == "drifted"
    with pytest.raises(ConfigError, match="healthy"):
        lifecycle.remove("example.scope")

    _run([str(python), "-I", "-m", "pip", "uninstall", "--yes", "wavebench-example-scope"])
    assert lifecycle.info("example.scope").status == "missing"


def test_same_version_file_tampering_is_reported_as_drifted(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    lifecycle.install(wheel)
    purelib = Path(lifecycle.environment().purelib)
    (purelib / "wavebench_example_scope/__init__.py").write_text(
        "# out-of-band change\n",
        encoding="utf-8",
    )

    assert lifecycle.info("example.scope").status == "drifted"
    with pytest.raises(ConfigError, match="healthy"):
        lifecycle.remove("example.scope")


def test_record_tampering_is_reported_as_drifted(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    lifecycle.install(wheel)
    purelib = Path(lifecycle.environment().purelib)
    record = next(purelib.glob("wavebench_example_scope-*.dist-info/RECORD"))
    record.write_bytes(record.read_bytes() + b"\n")

    assert lifecycle.info("example.scope").status == "drifted"


def test_missing_entry_point_is_reported_as_drifted_not_missing(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    lifecycle.install(wheel)
    purelib = Path(lifecycle.environment().purelib)
    entry_points = next(purelib.glob("wavebench_example_scope-*.dist-info/entry_points.txt"))
    entry_points.unlink()

    installed = lifecycle.info("example.scope")

    assert installed.status == "drifted"


def test_prepared_journal_blocks_mutation_and_can_be_recovered(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    environment = lifecycle.environment()
    lifecycle.state_dir.mkdir(mode=0o700)
    with lifecycle._inspected_input(wheel) as package:
        cached = lifecycle._cache_wheel(package)
        record = lifecycle._package_record(package, cached)
    lifecycle.journal_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "environment": environment.to_json(),
                "operation": "install",
                "stage": "prepared",
                "before_ledger": lifecycle.empty_ledger(environment),
                "package": record,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="recovery required"):
        lifecycle.install(wheel)

    assert lifecycle.recover().status == "recovered-before-mutation"
    assert not lifecycle.journal_path.exists()


def test_recover_commits_exact_desired_state_after_pip_finished(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    environment = lifecycle.environment()
    before = lifecycle.empty_ledger(environment)
    with lifecycle._inspected_input(wheel) as package:
        cached = lifecycle._cache_wheel(package)
        record = lifecycle._package_record(package, cached)
    journal = lifecycle._journal(
        environment=environment,
        operation="install",
        stage="pip_finished",
        before_ledger=before,
        package=record,
    )
    lifecycle.state_dir.mkdir(mode=0o700, exist_ok=True)
    lifecycle._write_json(lifecycle.journal_path, journal)
    lifecycle._pip_install(cached)

    result = lifecycle.recover()

    assert result.status == "recovered-to-desired"
    assert lifecycle.info("example.scope").status == "healthy"
    assert not lifecycle.journal_path.exists()


def test_recover_refuses_unknown_partial_state(tmp_path):
    python = _target_venv(tmp_path)
    wheel = _plugin_wheel(tmp_path, version="0.1.0")
    lifecycle = PluginLifecycle(python_executable=python)
    environment = lifecycle.environment()
    before = lifecycle.empty_ledger(environment)
    with lifecycle._inspected_input(wheel) as package:
        cached = lifecycle._cache_wheel(package)
        record = lifecycle._package_record(package, cached)
    lifecycle._pip_install(cached)
    purelib = Path(environment.purelib)
    (purelib / "wavebench_example_scope/__init__.py").write_text(
        "# partial state\n",
        encoding="utf-8",
    )
    journal = lifecycle._journal(
        environment=environment,
        operation="install",
        stage="pip_started",
        before_ledger=before,
        package=record,
    )
    lifecycle.state_dir.mkdir(mode=0o700, exist_ok=True)
    lifecycle._write_json(lifecycle.journal_path, journal)

    with pytest.raises(ConfigError, match="manual inspection"):
        lifecycle.recover()

    assert lifecycle.journal_path.exists()
