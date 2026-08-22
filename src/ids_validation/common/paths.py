"""Repository path resolution with explicit containment checks."""

from __future__ import annotations

from pathlib import Path


def repository_root(start: Path | str | None = None) -> Path:
    """Locate the repository root without changing process state."""

    candidate = (
        Path(start).resolve()
        if start is not None
        else Path(__file__).resolve().parents[3]
    )
    if candidate.is_file():
        candidate = candidate.parent
    for directory in (candidate, *candidate.parents):
        if (directory / ".git").exists() and (directory / "README.md").exists():
            return directory
    raise FileNotFoundError(f"Could not locate repository root from {candidate}")


def resolve_repository_path(
    path: Path | str,
    *,
    root: Path | str | None = None,
) -> Path:
    """Resolve a path and require it to remain inside the repository."""

    repo = repository_root(root)
    candidate = Path(path)
    resolved = (candidate if candidate.is_absolute() else repo / candidate).resolve()
    try:
        resolved.relative_to(repo)
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {resolved}") from exc
    return resolved


def repository_relative_path(
    path: Path | str,
    *,
    root: Path | str | None = None,
) -> Path:
    """Return a verified repository-relative path."""

    repo = repository_root(root)
    return resolve_repository_path(path, root=repo).relative_to(repo)
