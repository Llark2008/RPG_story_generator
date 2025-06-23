import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from rpggen.runner.world_builder import WorldBuilder


class FakeClient:
    def __init__(self, response: str) -> None:
        self.response = response

    def invoke(self, prompt: str) -> str:  # noqa: D401 - simple stub
        return self.response


def test_world_builder_run(tmp_path, monkeypatch):
    data = {
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
            "description": ""
        },
        "factions": [],
        "historical_timeline": [],
        "notable_figures": []
    }
    response = json.dumps(data)
    monkeypatch.setattr(
        "rpggen.runner.world_builder.OpenRouterClient",
        lambda: FakeClient(response),
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy")
    cfg = {"output_dir": tmp_path, "retry": 0}
    node = WorldBuilder(cfg)
    result = node.run()
    assert result.setting == "Test World"
    assert (tmp_path / "world.json").exists()
