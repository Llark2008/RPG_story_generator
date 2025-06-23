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
        schema = World.model_json_schema()
        base = (
            "你是一位经验丰富的世界观设计师。请仔细阅读下方的用戶需求(cfg)，"
            "根据提供的输出格式(模型)生成 JSON 数据。"
            "所有文本必须使用中文，并且只能返回有效的 JSON，"
            "不要添加任何解释或多余内容。"
            "生成的描述不需要顾虑长度限制，务必非常详细，"
            "所有描述字段需达到最小字数要求，并尽可能超出这些要求，"
            "并额外生成 'proper_nouns' 专有名词表。"
            "各字段最小字数如下：Technology.description ≥40，"
            "SpecialEnergy.description ≥120，Faction.description ≥100，"
            "NotableFigure.biography ≥40，ProperNoun.description 40-100。"
            "世界至少包含三大势力，并给出完整的设定说明。"
            "历史时间轴应充分展开，不能过于简短。"
            "'setting' 字段必须填写世界名称。\n"
            "用戶需求(cfg):\n"
            "{{ cfg | tojson(indent=2) }}\n"
            "输出格式(模型):\n"
            "{{ schema | tojson(indent=2) }}\n"
        )
        template = Template(base + self.prompt_override)
        return template.render(cfg=self.render_cfg, schema=schema)

    def call_llm(self, prompt: str) -> str:
        """Call the language model or fall back to a stub world."""
        if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")):
            # Offline fallback used during tests when no API key is configured
            stub = {
                "setting": "stub",
                "global_theme": "stub",
                "technologies": [],
                "special_energy": {
                    "name": "stub",
                    "discovery_year": 0,
                    "physical_form": "field",
                    "properties": [],
                    "hazards": [],
                    "applications": None,
                    "description": "x" * 120,
                },
                "factions": [],
                "historical_timeline": [],
                "notable_figures": [],
                "proper_nouns": []
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
        # proper noun names must be unique
        names = [n.name for n in parsed.proper_nouns]
        if len(names) != len(set(names)):
            self.logger.error("duplicate proper noun")
            return False
        return True

    def save(self, parsed: World) -> None:
        path = self.output_dir / "world.json"
        path.write_text(parsed.model_dump_json(indent=2) + "\n", encoding="utf-8")

