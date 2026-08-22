"""Deterministic JSON/text utilities for newly generated provenance files."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def read_json(path: Path | str) -> Any:
    """Read UTF-8 JSON without modifying it."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def deterministic_json_text(value: Any) -> str:
    """Serialize new provenance JSON with stable ordering and LF line endings."""

    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def atomic_write_text(path: Path | str, text: str) -> None:
    """Atomically write a newly generated text artifact.

    Callers remain responsible for ensuring the destination is not a frozen
    scientific result path.
    """

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
