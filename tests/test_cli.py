import sys
from pathlib import Path

# Ensure core package is importable during tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from typer.testing import CliRunner
from rpggen.cli import app


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "rpg generator" in result.output.lower()


def test_cli_node1(tmp_path):
    cfg = tmp_path / "cfg.yml"
    cfg.write_text("retry: 0\n")
    runner = CliRunner()
    result = runner.invoke(app, ["node1", "--config", str(cfg)])
    assert result.exit_code == 0
