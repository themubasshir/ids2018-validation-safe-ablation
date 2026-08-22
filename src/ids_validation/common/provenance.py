"""Structured provenance records for extracted historical functions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class SourceProvenance:
    """Trace an extracted callable back to immutable historical evidence."""

    source_notebook: str
    original_cells: tuple[int, ...]
    original_stage: str
    frozen_artifacts_generated: tuple[str, ...] = ()
    notes: str = ""

    @classmethod
    def from_cells(
        cls,
        *,
        source_notebook: str,
        original_cells: Iterable[int],
        original_stage: str,
        frozen_artifacts_generated: Iterable[str] = (),
        notes: str = "",
    ) -> "SourceProvenance":
        return cls(
            source_notebook=source_notebook,
            original_cells=tuple(int(value) for value in original_cells),
            original_stage=original_stage,
            frozen_artifacts_generated=tuple(frozen_artifacts_generated),
            notes=notes,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def render(self) -> str:
        cells = ", ".join(str(cell) for cell in self.original_cells)
        artifacts = ", ".join(self.frozen_artifacts_generated) or "None recorded"
        return (
            f"Source notebook: {self.source_notebook}\n"
            f"Original physical cell(s): {cells}\n"
            f"Original stage: {self.original_stage}\n"
            f"Frozen artifacts generated: {artifacts}\n"
            f"Notes: {self.notes}"
        )


def has_required_provenance_fields(docstring: str | None) -> bool:
    """Return whether an extracted function docstring has the required fields."""

    if not docstring:
        return False
    required = (
        "Source notebook:",
        "Original physical cell(s):",
        "Original stage:",
        "Frozen artifacts generated:",
        "Notes:",
    )
    return all(field in docstring for field in required)
