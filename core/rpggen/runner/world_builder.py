from __future__ import annotations

"""Implementation of Node1: world building."""

from pathlib import Path
import os
import json
from typing import Any

from jinja2 import Template

from ..llm_client import OpenRouterClient
from ..models import World
from .base_node import BaseNode


class WorldBuilder(BaseNode):
    """Generate the initial world description."""

    def load_inputs(self) -> None:
        """Prepare output directory and optional prompt overrides."""
        self.output_dir = Path(self.config.get("output_dir", "output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        path = self.config.get("prompt_overrides")
        self.prompt_override = ""
        if path:
            self.prompt_override = Path(path).read_text(encoding="utf-8")

        # convert config values for Jinja2 rendering
        self.render_cfg = {
            k: str(v) if isinstance(v, Path) else v for k, v in self.config.items()
        }

    def build_prompt(self) -> str:
        base = (
            "你是一位世界观设计师。基于以下控制参数生成 JSON:\n"
            "{{ cfg | tojson(indent=2) }}\n"
        )
        template = Template(base + self.prompt_override)
        return template.render(cfg=self.render_cfg)

    def call_llm(self, prompt: str) -> str:
        """Call the language model or fall back to a stub world."""
        if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")):
            # Offline fallback used during tests when no API key is configured
            stub = {
                "setting": "stub", "global_theme": "stub", "technologies": [],
                "special_energy": {
                    "name": "stub", "discovery_year": 0,
                    "physical_form": "field", "properties": [],
                    "hazards": [], "applications": None, "description": ""
                },
                "factions": [], "historical_timeline": [],
                "notable_figures": []
            }
            return json.dumps(stub)

        client = OpenRouterClient()
        return client.invoke(prompt)

    def parse(self, raw_output: str) -> World:
        data = json.loads(raw_output)
        return World.model_validate(data)

    def check_consistency(self, parsed: World) -> bool:
        # ensure timeline sorted by year
        years = [e.year for e in parsed.historical_timeline]
        if years != sorted(years):
            self.logger.error("timeline not sorted")
            return False
        # ids unique for factions
        ids = [f.id for f in parsed.factions]
        if len(ids) != len(set(ids)):
            self.logger.error("duplicate faction id")
            return False
        return True

    def save(self, parsed: World) -> None:
        path = self.output_dir / "world.json"
        path.write_text(parsed.model_dump_json(indent=2) + "\n", encoding="utf-8")

