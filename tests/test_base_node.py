import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))

from rpggen.runner.base_node import BaseNode


class Dummy(BaseNode):
    def __init__(self):
        super().__init__({"retry": 1})
        self.calls = []
        self.first = True

    def load_inputs(self) -> None:
        self.calls.append("load")

    def build_prompt(self) -> str:
        self.calls.append("prompt")
        return "p"

    def call_llm(self, prompt: str) -> str:
        self.calls.append("call")
        return "raw"

    def parse(self, raw_output: str):
        self.calls.append("parse")
        if self.first:
            self.first = False
            raise ValueError("fail")
        return {"ok": True}

    def check_consistency(self, parsed) -> bool:
        self.calls.append("check")
        return True

    def save(self, parsed) -> None:
        self.calls.append("save")

    def pre_retry(self, attempt: int) -> None:
        self.calls.append(f"pre{attempt}")

    def post_success(self, result) -> None:
        self.calls.append("post")


def test_base_node_run_retry():
    node = Dummy()
    result = node.run()
    assert result == {"ok": True}
    assert node.calls == [
        "load",
        "prompt",
        "call",
        "parse",
        "pre1",
        "load",
        "prompt",
        "call",
        "parse",
        "check",
        "save",
        "post",
    ]
