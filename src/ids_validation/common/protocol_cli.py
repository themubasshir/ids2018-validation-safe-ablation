"""Dry-run and read-only verification CLI for extracted stage protocols."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .io import read_json
from .paths import repository_root


def load_protocol(stage_number: int) -> dict[str, Any]:
    """Load a repository-owned extracted-stage protocol file."""

    if stage_number not in range(1, 13):
        raise ValueError("Only Stages 1–12 are extracted in the current approved checkpoints")
    root = repository_root()
    return read_json(root / "configs" / f"stage{stage_number:02d}" / "protocol.json")


def dry_run_report(protocol: dict[str, Any]) -> dict[str, Any]:
    """Build a non-executing report of the declared historical operation."""

    return {
        "mode": "dry-run",
        "stage": protocol["stage"],
        "source_cells": protocol["source"]["physical_cells_1_based"],
        "scientific_execution_performed": False,
        "would_read": protocol["inputs"],
        "would_write": protocol["outputs"],
        "methodology": protocol["methodology"],
    }


def verify_only_report(protocol: dict[str, Any]) -> dict[str, Any]:
    """Check declarations and artifact presence without opening scientific data."""

    root = repository_root()
    artifact_rows = []
    for relative in protocol["verification_artifacts"]:
        candidate = (root / relative).resolve()
        candidate.relative_to(root)
        artifact_rows.append({"path": relative, "status": "PRESENT" if candidate.exists() else "MISSING"})
    configuration_ok = (
        protocol.get("scientific_execution_enabled") is False
        and protocol["source"]["notebook_sha256"] == "147760f81f5db581c2cbc92b3c7c24060b823dfa50ac9d9a2156eb132b51b3ce"
        and protocol["holdout_policy"]["opened_by_verify_only"] is False
    )
    return {
        "mode": "verify-only",
        "stage": protocol["stage"],
        "configuration": "PASS" if configuration_ok else "FAIL",
        "artifacts": artifact_rows,
        "scientific_files_opened": False,
        "scientific_execution_performed": False,
    }


def run_protocol_cli(stage_number: int, argv: list[str] | None = None) -> int:
    """Run one extracted-stage safety-gated command line."""

    parser = argparse.ArgumentParser(description=f"Stage {stage_number} reproducibility protocol (scientific execution disabled)")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--dry-run", action="store_true", help="describe the scientific operation without performing it")
    modes.add_argument("--verify-only", action="store_true", help="verify declarations and artifact presence without opening scientific data")
    args = parser.parse_args(argv)
    protocol = load_protocol(stage_number)
    report = dry_run_report(protocol) if args.dry_run else verify_only_report(protocol)
    print(json.dumps(report, indent=2, sort_keys=True))
    failed = report.get("configuration") == "FAIL" or any(row["status"] == "MISSING" for row in report.get("artifacts", []))
    return 1 if failed else 0
