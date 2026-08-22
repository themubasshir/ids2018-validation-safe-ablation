"""Separately scoped Stage 20 forensic runtime records."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeRecord:
    """Proven and explicitly unproven properties of one historical runtime."""

    scope: str
    proven: tuple[str, ...]
    unproven: tuple[str, ...]
    evidence: str


HISTORICAL_EXTRACTOR = RuntimeRecord(
    scope="historical Java/jNetPcap/CICFlowMeter source inspection",
    proven=(
        "ahlashkari/CICFlowMeter commit eaa853dd82f08ba5288bb7f295b471de7313f883 inspected",
        "Java 8 HashMap positional order derived from source",
        "snapshot not claimed byte-identical to the July 2017 build",
    ),
    unproven=("Java version VERSION_NOT_PROVEN", "jNetPcap version VERSION_NOT_PROVEN"),
    evidence="Notebook cells 330–341 and stage20_1c8_flag_serialization_correction.json",
)

RECONSTRUCTION_RUNTIME = RuntimeRecord(
    scope="Python reconstruction and forensic utilities",
    proven=("runtime recovery occurred in multiple notebook sessions",),
    unproven=(
        "Python version VERSION_NOT_PROVEN",
        "Scapy version VERSION_NOT_PROVEN",
        "NumPy version VERSION_NOT_PROVEN",
        "PyArrow version VERSION_NOT_PROVEN",
    ),
    evidence="Notebook cells 315 and 348–411; versions are not promoted from package-install intent",
)
