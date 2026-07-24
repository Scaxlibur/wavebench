import tomllib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_lint_toolchain_is_reproducible() -> None:
    metadata = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert "ruff==0.15.20" in metadata["project"]["optional-dependencies"]["dev"]
    assert metadata["tool"]["ruff"]["lint"]["select"] == ["E4", "E7", "E9", "F"]
