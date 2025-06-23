from __future__ import annotations

"""Command line interface for running pipeline nodes."""

from pathlib import Path
from typing import List, Type

import typer
import yaml

from .runner.base_node import BaseNode
from .runner.dummy_nodes import CharacterBuilder, WorldBuilder

app = typer.Typer(help="RPG generator CLI")

NODE_CLASSES: dict[str, Type[BaseNode]] = {
    "node1": WorldBuilder,
    "node2": CharacterBuilder,
}


def _load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _apply_overrides(cfg: dict, overrides: List[str]) -> None:
    for item in overrides:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        cfg[key] = yaml.safe_load(value)


def _run_node(name: str, config: Path, overrides: List[str], retries: int) -> None:
    cls = NODE_CLASSES[name]
    cfg = _load_config(config)
    _apply_overrides(cfg, overrides)
    cfg.setdefault("retry", retries)
    cls(cfg).run()


@app.command()
def node1(
    *,
    config: Path = typer.Option(..., exists=True, help="YAML config file"),
    override: List[str] = typer.Option(None, help="key=value overrides"),
    retry: int = 0,
) -> None:
    """Run WorldBuilder node."""
    _run_node("node1", config, override or [], retry)


@app.command()
def node2(
    *,
    config: Path = typer.Option(..., exists=True, help="YAML config file"),
    override: List[str] = typer.Option(None, help="key=value overrides"),
    retry: int = 0,
) -> None:
    """Run CharacterBuilder node."""
    _run_node("node2", config, override or [], retry)


@app.command()
def all(
    *,
    config: Path = typer.Option(..., exists=True, help="YAML config file"),
    override: List[str] = typer.Option(None, help="key=value overrides"),
    retry: int = 0,
) -> None:
    """Run all nodes sequentially."""
    for name in ["node1", "node2"]:
        _run_node(name, config, override or [], retry)


def main(args: List[str] | None = None) -> None:
    app(args=args)


if __name__ == "__main__":  # pragma: no cover
    main()
