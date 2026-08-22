"""Generate the physical-cell provenance map for the archived research notebook.

This is an audit utility only.  It reads notebook JSON and writes a CSV index; it
does not import or execute notebook source.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


EXPECTED_NOTEBOOK_SHA256 = (
    "147760f81f5db581c2cbc92b3c7c24060b823dfa50ac9d9a2156eb132b51b3ce"
)

STAGE_RANGES: tuple[tuple[int, tuple[tuple[int, int], ...]], ...] = (
    (1, ((93, 93),)),
    (2, ((94, 95),)),
    (3, ((96, 101),)),
    (4, ((102, 104), (106, 106))),
    (5, ((105, 105), (107, 107))),
    (6, ((108, 108),)),
    (7, ((109, 115),)),
    (8, ((116, 117),)),
    (9, ((118, 118),)),
    (10, ((119, 119),)),
    (11, ((120, 120),)),
    (12, ((121, 129),)),
    (13, ((130, 146),)),
    (14, ((147, 161),)),
    (15, ((162, 170), (172, 189))),
    (16, ((171, 171), (190, 222))),
    (17, ((223, 239),)),
    (18, ((240, 289),)),
    (19, ((290, 311),)),
    (20, ((312, 461),)),
    (21, ((462, 488),)),
)

ALLOWED_CLASSIFICATIONS = {
    "precursor",
    "canonical",
    "repair",
    "recovery",
    "superseded",
    "packaging",
    "stage21_out_of_filename_scope",
}

PATH_LITERAL_RE = re.compile(
    r"(?P<quote>['\"])(?P<value>[^'\"\r\n]{1,500})(?P=quote)"
)
REPOSITORY_ARTIFACT_RE = re.compile(
    r"(?i)(?:results|metadata|models|docs|figures|tables)/[^'\"\s,)\]}]+"
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def stage_for_cell(physical_cell: int) -> str:
    if physical_cell <= 92:
        return "PRECURSOR"
    for stage, ranges in STAGE_RANGES:
        if any(start <= physical_cell <= end for start, end in ranges):
            return f"Stage{stage:02d}"
    return "UNMAPPED"


def meaningful_comments(source: str) -> list[str]:
    comments: list[str] = []
    for raw_line in source.splitlines()[:100]:
        stripped = raw_line.strip()
        if stripped.startswith("#!"):
            continue
        if not stripped.startswith("#"):
            if comments:
                break
            continue
        text = stripped.lstrip("#").strip()
        if not text or set(text) <= {"=", "-", "_"}:
            continue
        if text.upper() in {"PURPOSE", "IMPORTANT", "STATUS", "SCOPE"}:
            continue
        comments.append(re.sub(r"\s+", " ", text))
        if len(comments) >= 4:
            break
    return comments


def scientific_role(source: str) -> str:
    comments = meaningful_comments(source)
    if comments:
        return " | ".join(comments)[:500]
    compact = re.sub(r"\s+", " ", source).strip()
    return compact[:500] if compact else "Empty historical code cell"


def classification_for_cell(physical_cell: int, role: str, source: str) -> str:
    if 462 <= physical_cell <= 488:
        return "stage21_out_of_filename_scope"
    if 1 <= physical_cell <= 6 or 68 <= physical_cell <= 72 or physical_cell == 92:
        return "precursor"
    if 7 <= physical_cell <= 67 or 73 <= physical_cell <= 91:
        return "superseded"

    header = (role + "\n" + "\n".join(source.splitlines()[:35])).upper()
    if "ABANDONED" in header or "SUPERSEDED" in header:
        classification = "superseded"
    elif any(
        marker in header
        for marker in (
            " REPAIR",
            "-REPAIR",
            " PATCH",
            "-FIX",
            " ERRATUM",
            " CORRECTION",
            "CORRECTED VERSION",
        )
    ):
        classification = "repair"
    elif any(
        marker in header
        for marker in (
            " RECOVERY",
            " RESTORE",
            " RESUME",
            "POST-RESTART",
            "FRESH-SESSION",
            "POST-RECONNECT",
            "KAGGLE SESSION RECOVERY",
        )
    ):
        classification = "recovery"
    elif any(
        marker in header
        for marker in (
            "GIT ANCHOR",
            "PACKAGE AND PUSH",
            "PACKAGE, COMMIT",
            "REPOSITORY PACKAGING",
            "COMMIT AND PUSH",
            "PUSH EXISTING",
            "PUSH-ONLY",
            "PUBLICATION ASSETS",
            "ARCHIVE",
            "PERSIST CURRENT",
            "DURABILITY RECOVERY",
        )
    ):
        classification = "packaging"
    else:
        classification = "canonical"

    if classification not in ALLOWED_CLASSIFICATIONS:
        raise AssertionError(f"Unexpected classification: {classification}")
    return classification


def path_literals(source: str) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    for line in source.splitlines():
        for match in PATH_LITERAL_RE.finditer(line):
            value = match.group("value").strip()
            if not (
                "/" in value
                or "\\" in value
                or re.search(
                    r"(?i)\.(?:csv|json|npy|npz|joblib|pkl|keras|pt|txt|md|png|pdf|zip|gz|parquet|sha256)$",
                    value,
                )
            ):
                continue
            context = line.lower()
            if any(
                token in context
                for token in (
                    "to_csv",
                    "save",
                    "dump",
                    "write",
                    "output",
                    "results_dir",
                    "figures_dir",
                    "archive",
                    "destination",
                )
            ):
                kind = "output"
            elif any(
                token in context
                for token in (
                    "read_",
                    "load",
                    "input",
                    "source",
                    "dataset",
                    "required",
                    "model_path",
                )
            ):
                kind = "input"
            else:
                kind = "reference"
            records.append((kind, value))
    return records


def limited_join(values: list[str], limit: int = 12) -> str:
    unique: list[str] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    if len(unique) > limit:
        return "; ".join(unique[:limit]) + f"; ... (+{len(unique) - limit} more)"
    return "; ".join(unique)


def generate(notebook_path: Path, output_path: Path) -> None:
    raw = notebook_path.read_bytes()
    observed_sha = sha256_bytes(raw)
    if observed_sha != EXPECTED_NOTEBOOK_SHA256:
        raise RuntimeError(
            "Authoritative notebook SHA256 mismatch: "
            f"expected {EXPECTED_NOTEBOOK_SHA256}, observed {observed_sha}"
        )

    notebook = json.loads(raw.decode("utf-8"))
    cells = notebook.get("cells", [])
    if len(cells) != 488:
        raise RuntimeError(f"Expected 488 physical cells, observed {len(cells)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "physical_cell",
        "execution_count",
        "cell_type",
        "stage",
        "classification",
        "scientific_role",
        "inputs",
        "outputs",
        "frozen_artifacts",
        "output_blocks",
        "source_lines",
        "source_sha256",
        "notes",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for physical_cell, cell in enumerate(cells, start=1):
            source = "".join(cell.get("source", []))
            role = scientific_role(source)
            classification = classification_for_cell(
                physical_cell=physical_cell,
                role=role,
                source=source,
            )
            paths = path_literals(source)
            inputs = [value for kind, value in paths if kind == "input"]
            outputs = [value for kind, value in paths if kind == "output"]
            frozen_artifacts = REPOSITORY_ARTIFACT_RE.findall(source)
            notes = [
                "Physical 1-based order is canonical; execution_count is historical evidence only."
            ]
            if physical_cell == 171:
                notes.append("Approved override: Stage16 cell inside the Stage15 physical sequence.")
            if 462 <= physical_cell <= 488:
                notes.append(
                    "Approved override: Stage21 work retained inside the notebook named Stage01-to-Stage20."
                )
            if physical_cell <= 92:
                notes.append(
                    "Pre-canonical notebook history; retained to preserve methodological evolution."
                )
            writer.writerow(
                {
                    "physical_cell": physical_cell,
                    "execution_count": (
                        "" if cell.get("execution_count") is None else cell["execution_count"]
                    ),
                    "cell_type": cell.get("cell_type", ""),
                    "stage": stage_for_cell(physical_cell),
                    "classification": classification,
                    "scientific_role": role,
                    "inputs": limited_join(inputs),
                    "outputs": limited_join(outputs),
                    "frozen_artifacts": limited_join(frozen_artifacts),
                    "output_blocks": len(cell.get("outputs", [])),
                    "source_lines": len(source.splitlines()),
                    "source_sha256": sha256_bytes(source.encode("utf-8")),
                    "notes": " ".join(notes),
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--notebook",
        type=Path,
        default=Path("notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/reproducibility/NOTEBOOK_CELL_MAP.csv"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate(args.notebook, args.output)


if __name__ == "__main__":
    main()
