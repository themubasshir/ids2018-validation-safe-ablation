"""Validation-only records for historically frozen integer seeds."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedSpec:
    """A seed plus its evidence source; this class does not set RNG state."""

    value: int
    source: str

    def __post_init__(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise TypeError("Historical seeds must be explicit integers")
