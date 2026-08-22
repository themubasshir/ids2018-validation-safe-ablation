"""Minimal logging configuration for reproducibility entrypoints."""

from __future__ import annotations

import logging


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure one concise stderr handler when the caller requests it."""

    logger = logging.getLogger("ids_validation")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
