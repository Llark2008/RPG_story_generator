from __future__ import annotations

"""Minimal node implementations used for CLI and tests."""

from .base_node import BaseNode


class WorldBuilder(BaseNode):
    def load_inputs(self) -> None:
        pass

    def build_prompt(self) -> str:
        return "build world"

    def call_llm(self, prompt: str) -> str:
        return "{}"  # empty JSON

    def parse(self, raw_output: str) -> dict:
        return {}

    def check_consistency(self, parsed: dict) -> bool:
        return True

    def save(self, parsed: dict) -> None:
        self.logger.info("world saved")


class CharacterBuilder(BaseNode):
    def load_inputs(self) -> None:
        pass

    def build_prompt(self) -> str:
        return "build characters"

    def call_llm(self, prompt: str) -> str:
        return "[]"  # empty list

    def parse(self, raw_output: str) -> list:
        return []

    def check_consistency(self, parsed: list) -> bool:
        return True

    def save(self, parsed: list) -> None:
        self.logger.info("characters saved")
