from __future__ import annotations

"""Lightweight logger setup."""

import logging
from pathlib import Path
from typing import Optional, Union

__all__ = ["get_logger"]


PathLike = Union[str, Path]


def get_logger(name: str, log_file: Optional[PathLike] = None, level: int = logging.INFO) -> logging.Logger:
    """Create and configure a logger.

    If ``log_file`` is given a file handler is added in addition to the
    standard output handler.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
