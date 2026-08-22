"""Frozen 21-field packet-reproducible directed-flow signature."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


SIGNATURE_NAME = "S4_PACKET_REPRODUCIBLE_DIRECTED_FLOW_SIGNATURE"
SIGNATURE_FIELDS = (
    "Source IP",
    "Source Port",
    "Destination IP",
    "Destination Port",
    "Protocol",
    "Timestamp",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Min",
    "Fwd Packet Length Max",
    "Bwd Packet Length Min",
    "Bwd Packet Length Max",
    "FIN Flag Count",
    "SYN Flag Count",
    "RST Flag Count",
    "PSH Flag Count",
    "ACK Flag Count",
    "URG Flag Count",
)


def build_signature(record: Mapping[str, Any]) -> tuple[Any, ...]:
    """Format an already-canonical toy record in exact S4 field order.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 320, 321, 322, 323, 324, 325
    Original stage: Stage20-1B4 through 1B4E
    Frozen artifacts generated: stage20_1b4e_packet_label_reconstruction_spec.json
    Notes: Values are neither coerced nor canonicalized; no tolerance, nearest
    match, label guidance, or bidirectional endpoint swap is implemented.
    """

    missing = [field for field in SIGNATURE_FIELDS if field not in record]
    if missing:
        raise KeyError(f"missing S4 fields: {', '.join(missing)}")
    return tuple(record[field] for field in SIGNATURE_FIELDS)
