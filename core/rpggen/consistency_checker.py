from __future__ import annotations

"""Generic retrieval-augmented consistency checker.

This module provides a small helper that scores how well a question can be
answered using a set of reference texts. It builds a FAISS index from the
supplied documents and then queries an LLM with the top matching chunks. The
LLM is expected to return a floating point score between 0 and 1 where higher
means more consistent.
"""

from typing import Iterable, Sequence
import re

from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
try:  # pragma: no cover - optional dependency
    from langchain_community.vectorstores import FAISS
except Exception:  # pragma: no cover - fallback if faiss unavailable
    FAISS = None

__all__ = ["ConsistencyChecker"]


class ConsistencyChecker:
    """Simple retrieval based consistency scorer."""

    def __init__(
        self,
        *,
        llm: BaseLanguageModel,
        embeddings: Embeddings,
        score_threshold: float = 0.5,
        top_k: int = 4,
    ) -> None:
        self.llm = llm
        self.embeddings = embeddings
        self.score_threshold = score_threshold
        self.top_k = top_k
        self._index: object | None = None

    def build_index(self, texts: Sequence[str]) -> None:
        """Build an in-memory index from ``texts``."""
        if FAISS is not None:
            try:
                self._index = FAISS.from_texts(list(texts), self.embeddings)
                return
            except Exception:  # pragma: no cover - faiss failed
                pass
        self._index = list(texts)

    def score(self, question: str) -> float:
        """Return the LLM predicted consistency score for ``question``."""
        if self._index is None:
            raise ValueError("index not built")

        if FAISS is not None and not isinstance(self._index, list):
            retriever = self._index.as_retriever(search_kwargs={"k": self.top_k})
            docs: Iterable[Document] = retriever.invoke(question)
            context = "\n".join(d.page_content for d in docs)
        else:
            context = "\n".join(self._index)

        prompt = (
            "You are a consistency checking assistant.\n"
            "Use the context to answer the question and output a single floating "
            "point score between 0 and 1 where higher means more consistent.\n"
            f"Context:\n{context}\nQuestion: {question}\nScore:"
        )
        response = self.llm.invoke(prompt)
        try:
            return float(response.strip())
        except ValueError:
            match = re.search(r"([0-9]+(?:\.[0-9]+)?)", response)
            if not match:
                raise ValueError(f"cannot parse score from LLM output: {response}")
            return float(match.group(1))

    def check(self, question: str) -> bool:
        """Return ``True`` if the score meets ``score_threshold``."""
        return self.score(question) >= self.score_threshold

