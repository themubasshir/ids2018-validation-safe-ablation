"""Read-only hashing helpers for archived and frozen artifacts."""

from __future__ import annotations

import hashlib
import subprocess
from enum import Enum
from pathlib import Path


class HashMode(str, Enum):
    """Explicit byte representation used for a SHA256 comparison."""

    WORKTREE_BYTES = "worktree_bytes"
    LF_NORMALIZED = "lf_normalized"
    GIT_BLOB = "git_blob"


def sha256_bytes(payload: bytes) -> str:
    """Return the lowercase SHA256 digest for *payload*."""

    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path | str) -> str:
    """Hash exact filesystem bytes without newline normalization."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_lf_normalized(path: Path | str) -> str:
    """Hash bytes after converting CRLF to LF, preserving all other bytes."""

    return sha256_bytes(Path(path).read_bytes().replace(b"\r\n", b"\n"))


def sha256_git_blob(
    repository_root: Path | str,
    repository_relative_path: Path | str,
    revision: str = "HEAD",
) -> str:
    """Hash the canonical Git blob bytes for a tracked path.

    This is intentionally separate from worktree hashing so line-ending
    conversion can never be mistaken for frozen scientific artifact drift.
    """

    root = Path(repository_root).resolve()
    relative = Path(repository_relative_path).as_posix()
    result = subprocess.run(
        ["git", "show", f"{revision}:{relative}"],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return sha256_bytes(result.stdout)
