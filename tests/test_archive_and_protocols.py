from __future__ import annotations

import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.protocol_cli import dry_run_report, load_protocol, verify_only_report


class ArchiveIntegrityTests(unittest.TestCase):
    def test_authoritative_notebook_identity_and_cell_count(self) -> None:
        notebook_path = ROOT / "notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb"
        self.assertEqual(
            hashlib.sha256(notebook_path.read_bytes()).hexdigest(),
            "147760f81f5db581c2cbc92b3c7c24060b823dfa50ac9d9a2156eb132b51b3ce",
        )
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        self.assertEqual(len(notebook["cells"]), 488)
        for physical_cell in range(93, 108):
            self.assertEqual(notebook["cells"][physical_cell - 1].get("outputs", []), [])

    def test_full_cell_map_and_mapping_exceptions(self) -> None:
        with (ROOT / "docs/reproducibility/NOTEBOOK_CELL_MAP.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 488)
        self.assertEqual(rows[170]["stage"], "Stage16")
        self.assertEqual(rows[461]["stage"], "Stage21")
        self.assertEqual(rows[461]["classification"], "stage21_out_of_filename_scope")


class ProtocolSafetyTests(unittest.TestCase):
    EXPECTED_CELLS = {
        1: [93],
        2: [94, 95],
        3: [96, 97, 98, 99, 100, 101],
        4: [102, 103, 104, 106],
        5: [105, 107],
        6: [108],
        7: [109, 110, 111, 112, 113, 114, 115],
        8: [116, 117],
        9: [118],
        10: [119],
        11: [120],
        12: [121, 122, 123, 124, 125, 126, 127, 128, 129],
        13: [130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146],
        14: [147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161],
        15: [162, 163, 164, 165, 166, 167, 168, 169, 170, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189],
        16: [171, *range(190, 223)],
        17: list(range(223, 240)),
        18: list(range(240, 290)),
        19: list(range(290, 312)),
        20: list(range(312, 462)),
    }

    def test_all_protocols_are_execution_disabled_and_mapped(self) -> None:
        for stage, cells in self.EXPECTED_CELLS.items():
            with self.subTest(stage=stage):
                protocol = load_protocol(stage)
                self.assertIs(protocol["scientific_execution_enabled"], False)
                self.assertEqual(protocol["source"]["physical_cells_1_based"], cells)
                self.assertIs(protocol["holdout_policy"]["opened_by_verify_only"], False)

    def test_dry_run_never_performs_science(self) -> None:
        for stage in self.EXPECTED_CELLS:
            report = dry_run_report(load_protocol(stage))
            self.assertIs(report["scientific_execution_performed"], False)

    def test_verify_only_is_presence_only_and_all_artifacts_exist(self) -> None:
        for stage in self.EXPECTED_CELLS:
            report = verify_only_report(load_protocol(stage))
            self.assertEqual(report["configuration"], "PASS")
            self.assertIs(report["scientific_files_opened"], False)
            self.assertIs(report["scientific_execution_performed"], False)
            self.assertTrue(all(row["status"] == "PRESENT" for row in report["artifacts"]))

    def test_unknown_versions_are_explicitly_not_proven(self) -> None:
        for stage in self.EXPECTED_CELLS:
            for status in load_protocol(stage)["environment"].get("unproven", {}).values():
                self.assertEqual(status, "VERSION_NOT_PROVEN")

    def test_equivalence_matrix_uses_only_approved_levels(self) -> None:
        with (ROOT / "docs/reproducibility/EQUIVALENCE_MATRIX.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 73)
        self.assertEqual({row["status"] for row in rows}, {"PASS"})
        self.assertTrue({row["equivalence_level"] for row in rows} <= {"A", "B", "C", "D"})


if __name__ == "__main__":
    unittest.main()
