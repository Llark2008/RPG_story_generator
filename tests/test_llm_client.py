import sys
from pathlib import Path

# Make core package importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

import rpggen
from rpggen.llm_client import OpenRouterClient


def test_openrouterclient_invoke(monkeypatch):
    from langchain_community.llms import FakeListLLM

    captured = {}

    def fake_chat_openai(*args, **kwargs):
        captured.update(kwargs)
        return FakeListLLM(responses=["ok"])

    monkeypatch.setattr("rpggen.llm_client.ChatOpenAI", fake_chat_openai)
    monkeypatch.setenv("OPENROUTER_MODEL", "env-model")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://example.com")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")

    client = OpenRouterClient()
    assert client.invoke("test") == "ok"
    assert captured["model"] == "env-model"
    assert captured["base_url"] == "https://example.com"
    assert captured["api_key"] == "sk-test"

