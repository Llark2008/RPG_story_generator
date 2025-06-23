import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from rpggen.runner.character_builder import CharacterBuilder
from rpggen.models import World


class FakeClient:
    def __init__(self, response: str) -> None:
        self.response = response

    def invoke(self, prompt: str) -> str:  # noqa: D401 - simple stub
        return self.response


def test_character_builder_run(tmp_path, monkeypatch):
    world_data = {
        "setting": "Test World",
        "global_theme": "Mystery",
        "technologies": [],
        "special_energy": {
            "name": "x",
            "discovery_year": 0,
            "physical_form": "field",
            "properties": [],
            "hazards": [],
            "applications": None,
            "description": "x" * 120,
        },
        "factions": [
            {
                "id": "f1",
                "name": "Faction",
                "motive": "m",
                "doctrine": "d",
                "status": "active",
                "founding_year": 1,
                "description": "x" * 100,
            }
        ],
        "historical_timeline": [],
        "notable_figures": [],
        "proper_nouns": [],
    }
    world_path = tmp_path / "world.json"
    world_path.write_text(json.dumps(world_data), encoding="utf-8")

    chars = [
        {
            "id": "c1",
            "name": "Alice",
            "aliases": None,
            "faction_id": "f1",
            "gender": "female",
            "birth": 2,
            "death": None,
            "age": None,
            "occupation": "tester",
            "personality": ["brave"],
            "values": ["justice"],
            "motives": ["m"],
            "skills": ["skill"],
            "secrets": None,
            "appearance": "x" * 60,
            "signature_items": None,
            "backstory": "x" * 120,
            "relationship_seeds": None,
        }
    ]
    response = json.dumps(chars)
    monkeypatch.setattr(
        "rpggen.runner.character_builder.OpenRouterClient",
        lambda: FakeClient(response),
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    cfg = {"output_dir": tmp_path, "world_path": world_path, "retry": 0}
    node = CharacterBuilder(cfg)
    result = node.run()
    assert result[0].name == "Alice"
    assert (tmp_path / "characters.json").exists()
