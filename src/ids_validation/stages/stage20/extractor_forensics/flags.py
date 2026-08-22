"""C8 source-derived Java ``HashMap`` flag-serialization semantics."""

from __future__ import annotations

from collections.abc import Mapping


CSV_HEADER_ORDER = ("FIN", "SYN", "RST", "PSH", "ACK", "URG", "CWE", "ECE")
JAVA8_SERIALIZED_ORDER = ("RST", "PSH", "ECE", "SYN", "ACK", "FIN", "URG", "CWR")
PHYSICAL_COLUMN_TO_SEMANTIC_FLAG = dict(zip(CSV_HEADER_ORDER, JAVA8_SERIALIZED_ORDER, strict=True))


def serialize_semantic_flags(semantic_counts: Mapping[str, int]) -> tuple[int, ...]:
    """Place caller-supplied toy semantic counts in historical physical order.

    Source notebook: physical cells 340–341 (Stage20-1C7/1C8).
    Frozen artifact: stage20_1c8_flag_serialization_correction.json.
    This is the source-derived mapping, not a searched permutation.  It does
    not modify any physical source column or label.
    """

    missing = [name for name in JAVA8_SERIALIZED_ORDER if name not in semantic_counts]
    if missing:
        raise KeyError(f"missing semantic flag counts: {', '.join(missing)}")
    return tuple(int(semantic_counts[name]) for name in JAVA8_SERIALIZED_ORDER)
