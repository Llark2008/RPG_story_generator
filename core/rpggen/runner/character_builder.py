from __future__ import annotations

"""Implementation of Node2: character builder."""

from pathlib import Path
import os
import json
from typing import Any, List

from jinja2 import Template

from ..llm_client import OpenRouterClient
from ..models import Character, World
from ..utils import slugify
from .base_node import BaseNode


class CharacterBuilder(BaseNode):
    """Generate characters for each faction based on the world."""

    world: World
    characters: List[Character]

    def load_inputs(self) -> None:
        """Load config, world.json and optional prompt override."""
        self.output_dir = Path(self.config.get("output_dir", "output"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        world_path = Path(
            self.config.get(
                "world_path", self.output_dir / "world.json"
            )
        )
        self.world = World.model_validate_json(world_path.read_text(encoding="utf-8"))

        path = self.config.get("prompt_overrides")
        self.prompt_override = ""
        if path:
            self.prompt_override = Path(path).read_text(encoding="utf-8")

        self.render_cfg = {
            k: str(v) if isinstance(v, Path) else v
            for k, v in self.config.items()
        }

    def build_prompt(self) -> str:
        schema = Character.model_json_schema()
        base = (
            "你是一位人物设定专家。根据以下世界观(world)与配置(cfg)生成 JSON 列表。"
            "每个阵营至少生成一名角色，遵循输出格式(模型)。"
            "所有文本必须使用中文，只能返回有效 JSON。"
            "避免任何解释。"
            "cfg:\n{{ cfg | tojson(indent=2) }}\n"
            "world:\n{{ world | tojson(indent=2) }}\n"
            "模型:\n{{ schema | tojson(indent=2) }}\n"
        )
        template = Template(base + self.prompt_override)
        return template.render(cfg=self.render_cfg, world=self.world.model_dump(), schema=schema)

    def call_llm(self, prompt: str) -> str:
        """Call model or return offline stub if API key missing."""
        if not (os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")):
            chars = []
            for fac in self.world.factions:
                char = {
                    "id": slugify(fac.id) + "_stub",
                    "name": fac.name + " 角色",
                    "aliases": None,
                    "faction_id": fac.id,
                    "gender": "unknown",
                    "birth": fac.founding_year,
                    "death": None,
                    "age": None,
                    "occupation": "未知",
                    "personality": ["普通"],
                    "values": ["生存"],
                    "motives": [fac.motive],
                    "skills": ["none"],
                    "secrets": None,
                    "appearance": "x" * 60,
                    "signature_items": None,
                    "backstory": "x" * 120,
                    "relationship_seeds": None,
                }
                chars.append(char)
            return json.dumps(chars)

        client = OpenRouterClient()
        return client.invoke(prompt)

    def parse(self, raw_output: str) -> List[Character]:
        data = json.loads(raw_output)
        return [Character.model_validate(item) for item in data]

    def check_consistency(self, parsed: List[Character]) -> bool:
        faction_ids = {f.id for f in self.world.factions}
        ids = set()
        for ch in parsed:
            if ch.faction_id not in faction_ids:
                self.logger.error("invalid faction_id: %s", ch.faction_id)
                return False
            if ch.id in ids:
                self.logger.error("duplicate character id: %s", ch.id)
                return False
            ids.add(ch.id)
            if ch.death is not None and ch.death <= ch.birth:
                self.logger.error("death year before birth for %s", ch.id)
                return False
        return True

    def save(self, parsed: List[Character]) -> None:
        path = self.output_dir / "characters.json"
        text = json.dumps([c.model_dump() for c in parsed], indent=2, ensure_ascii=False)
        path.write_text(text + "\n", encoding="utf-8")
        self.characters = parsed
