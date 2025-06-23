from __future__ import annotations

"""Small text utilities."""

import re
import unicodedata

__all__ = ["slugify", "chinese_length"]


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Return a slug suitable for URLs or identifiers.

    Parameters
    ----------
    value:
        Arbitrary text to slugify.
    allow_unicode:
        Keep unicode characters instead of ASCII folding.

    """
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value


def chinese_length(text: str) -> int:
    """Approximate length of Chinese text in characters."""
    return len(text.encode("gb18030")) // 2
