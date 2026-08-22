"""Artifact declarations and read-only verification records."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .hashing import (
    HashMode,
    sha256_file,
    sha256_git_blob,
    sha256_lf_normalized,
)
from .paths import repository_relative_path, resolve_repository_path


@dataclass(frozen=True)
class ArtifactSpec:
    """Expected identity of one historical artifact."""

    path: str
    expected_sha256: str | None = None
    hash_mode: HashMode = HashMode.WORKTREE_BYTES
    description: str = ""
    required: bool = True


@dataclass(frozen=True)
class ArtifactVerification:
    """Serializable result of an artifact identity check."""

    path: str
    exists: bool
    expected_sha256: str | None
    observed_sha256: str | None
    hash_mode: str
    status: str
    description: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def verify_artifact(
    spec: ArtifactSpec,
    *,
    root: Path | str | None = None,
    revision: str = "HEAD",
) -> ArtifactVerification:
    """Verify one artifact without reading scientific data through a model."""

    resolved = resolve_repository_path(spec.path, root=root)
    if not resolved.exists():
        status = "MISSING" if spec.required else "OPTIONAL_MISSING"
        return ArtifactVerification(
            path=spec.path,
            exists=False,
            expected_sha256=spec.expected_sha256,
            observed_sha256=None,
            hash_mode=spec.hash_mode.value,
            status=status,
            description=spec.description,
        )

    if spec.hash_mode is HashMode.WORKTREE_BYTES:
        observed = sha256_file(resolved)
    elif spec.hash_mode is HashMode.LF_NORMALIZED:
        observed = sha256_lf_normalized(resolved)
    elif spec.hash_mode is HashMode.GIT_BLOB:
        relative = repository_relative_path(resolved, root=root)
        observed = sha256_git_blob(
            repository_root=resolved.parents[len(relative.parts) - 1],
            repository_relative_path=relative,
            revision=revision,
        )
    else:  # pragma: no cover - Enum prevents this in normal use.
        raise ValueError(f"Unsupported hash mode: {spec.hash_mode}")

    status = (
        "PRESENT_UNHASHED"
        if spec.expected_sha256 is None
        else "PASS"
        if observed == spec.expected_sha256.lower()
        else "FAIL"
    )
    return ArtifactVerification(
        path=spec.path,
        exists=True,
        expected_sha256=spec.expected_sha256,
        observed_sha256=observed,
        hash_mode=spec.hash_mode.value,
        status=status,
        description=spec.description,
    )
