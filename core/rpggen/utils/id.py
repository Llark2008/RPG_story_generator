from __future__ import annotations

"""ID generation helpers."""

import hashlib
from uuid import uuid5, NAMESPACE_DNS

__all__ = ["hash_id", "uuid_id"]


def hash_id(text: str, length: int = 10) -> str:
    """Return a deterministic short hash derived from ``text``.

    Parameters
    ----------
    text:
        Input text used to compute the hash.
    length:
        Length of the resulting hexadecimal string.
    """
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
    return digest[:length]


def uuid_id(name: str, length: int = 8) -> str:
    """Generate a UUID5 based identifier."""
    return uuid5(NAMESPACE_DNS, name).hex[:length]
