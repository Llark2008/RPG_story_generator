from __future__ import annotations

"""Base class for all pipeline nodes."""

from abc import ABC, abstractmethod
from typing import Any

from ..utils import get_logger


class BaseNode(ABC):
    """Abstract pipeline node.

    A node implements ``run`` which orchestrates the typical generation steps::

        load_inputs() -> build_prompt() -> call_llm() -> parse() ->
        check_consistency() -> save()

    Subclasses should override the abstract methods. ``run`` will retry on
    failure up to ``config['retry']`` times and trigger ``pre_retry`` and
    ``post_success`` hooks accordingly.
    """

    def __init__(self, config: dict) -> None:
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.retry_limit = int(config.get("retry", 0))

    # --- life-cycle -----------------------------------------------------
    def run(self) -> Any:
        attempt = 0
        while True:
            if attempt:
                self.pre_retry(attempt)
            try:
                self.load_inputs()
                prompt = self.build_prompt()
                raw = self.call_llm(prompt)
                data = self.parse(raw)
                if not self.check_consistency(data):
                    raise ValueError("consistency check failed")
                self.save(data)
                self.post_success(data)
                return data
            except Exception as exc:  # pragma: no cover - generic catch
                self.logger.error("Attempt %s failed: %s", attempt + 1, exc)
                attempt += 1
                if attempt > self.retry_limit:
                    raise

    # --- hooks ----------------------------------------------------------
    def pre_retry(self, attempt: int) -> None:  # pragma: no cover - optional
        """Called before a retry attempt."""

    def post_success(self, result: Any) -> None:  # pragma: no cover - optional
        """Called after successful run."""

    # --- steps ----------------------------------------------------------
    @abstractmethod
    def load_inputs(self) -> None:
        """Load any required input files."""

    @abstractmethod
    def build_prompt(self) -> str:
        """Return the prompt passed to the LLM."""

    @abstractmethod
    def call_llm(self, prompt: str) -> str:
        """Call the language model and return raw output."""

    @abstractmethod
    def parse(self, raw_output: str) -> Any:
        """Parse the raw LLM output into structured data."""

    @abstractmethod
    def check_consistency(self, parsed: Any) -> bool:
        """Return ``True`` if ``parsed`` passes consistency checks."""

    @abstractmethod
    def save(self, parsed: Any) -> None:
        """Persist the generated result."""
