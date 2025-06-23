from __future__ import annotations

"""Unified OpenRouter LLM client using LangChain.

Environment variables are loaded from a ``.env`` file if present.
"""

from typing import Iterable, Optional
import os

from dotenv import load_dotenv

# load variables from a local .env file if present
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

__all__ = ["OpenRouterClient"]


class OpenRouterClient:
    """Simple wrapper around :class:`~langchain_openai.ChatOpenAI`.

    Parameters
    ----------
    model:
        Model name to call on OpenRouter. Defaults to ``OPENROUTER_MODEL`` or
        ``qwen/qwen3-30b-a3b:free``.
    max_retries:
        Number of attempts before giving up.
    streaming:
        Whether to enable streaming output. When enabled the response tokens
        are printed to stdout via ``StreamingStdOutCallbackHandler``.
    base_url:
        Override OpenRouter endpoint. Defaults to ``OPENROUTER_BASE_URL`` or
        ``https://openrouter.ai/api/v1``.
    api_key:
        API key used for authentication. Defaults to ``OPENROUTER_API_KEY``.
    **kwargs:
        Extra arguments forwarded to :class:`ChatOpenAI`.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        *,
        max_retries: int = 2,
        streaming: bool = False,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs: object,
    ) -> None:
        if model is None:
            model = os.environ.get("OPENROUTER_MODEL", "qwen/qwen3-30b-a3b:free")
        if base_url is None:
            base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        if api_key is None:
            api_key = os.environ.get("OPENROUTER_API_KEY")

        callbacks = kwargs.pop("callbacks", None)
        if streaming and callbacks is None:
            callbacks = [StreamingStdOutCallbackHandler()]

        self._llm: Runnable = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            streaming=streaming,
            callbacks=callbacks,
            **kwargs,
        ).with_retry(stop_after_attempt=max_retries)

        self._parser = StrOutputParser()

    def invoke(self, prompt: str) -> str:
        """Invoke the model with the given prompt and return the full text."""
        chain = self._llm | self._parser
        return chain.invoke(prompt)

    def stream(self, prompt: str) -> Iterable[str]:
        """Yield the streamed tokens for the given prompt."""
        llm = self._llm
        if not getattr(llm, "streaming", False):
            yield self.invoke(prompt)
            return
        for chunk in llm.stream(prompt):
            if hasattr(chunk, "content"):
                yield chunk.content
            else:
                yield str(chunk)

