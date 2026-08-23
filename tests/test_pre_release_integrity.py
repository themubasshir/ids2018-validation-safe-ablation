from __future__ import annotations

import csv
import hashlib
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
RELEASE = ROOT / "docs" / "release"
PASS2B = ROOT / "docs" / "manuscript" / "pass2b"
PASS2C = ROOT / "docs" / "manuscript" / "pass2c"
STAGE29 = ROOT / "results" / "stage29_manuscript_synthesis"
BASELINE = MANUSCRIPT / "manuscript_submission_candidate.md"
PASS2C_CANDIDATE = MANUSCRIPT / "manuscript_submission_candidate_pass2c.md"
CANONICAL = MANUSCRIPT / "manuscript_final_content.md"
BIBLIOGRAPHY = MANUSCRIPT / "references.bib"
TITLE = "A Multi-Axis Validation Framework for Machine-Learning Intrusion Detection"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PreReleaseIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canonical = CANONICAL.read_text(encoding="utf-8-sig")
        cls.pass2c = PASS2C_CANDIDATE.read_text(encoding="utf-8-sig")
        cls.numbers = read_csv(RELEASE / "FINAL_NUMBER_AUDIT.csv")
        cls.limitations = read_csv(PASS2C / "LIMITATION_PRESENTATION_AUDIT.csv")
        cls.claims = read_csv(PASS2C / "FINAL_CLAIM_AUDIT.csv")
        cls.citations = read_csv(PASS2C / "FINAL_CITATION_AUDIT.csv")
        cls.tensions = read_csv(PASS2C / "EVIDENCE_TENSION_PRESERVATION.csv")

    def test_required_pre_release_artifacts_exist(self) -> None:
        required = (
            ROOT / "LICENSE",
            ROOT / "CITATION.cff",
            MANUSCRIPT / "README.md",
            CANONICAL,
            ROOT / "docs" / "manuscript" / "FINAL_CONTENT_FREEZE.md",
            RELEASE / "PRE_RELEASE_CORRECTION_AUDIT.md",
            RELEASE / "FINAL_NUMBER_AUDIT.csv",
            RELEASE / "LICENSE_AUDIT.md",
            RELEASE / "CITATION_METADATA_AUDIT.md",
            RELEASE / "ARTIFACT_EVALUATION_APPENDIX.md",
            RELEASE / "RELEASE_READINESS_CHECKLIST.md",
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

    def test_historical_candidates_remain_byte_immutable(self) -> None:
        self.assertEqual(
            sha256(BASELINE),
            "c4879bbc4ca6fa6b8d638984ae1cdd0ebfb25114471c9d7c58634a5a0996ca88",
        )
        self.assertEqual(
            sha256(PASS2C_CANDIDATE),
            "3d3c86876efa2e19579a68a1f7d28cb56728223771646e6c61cc409eafe07f7f",
        )

    def test_canonical_is_exactly_the_governed_pass2c_correction(self) -> None:
        expected = self.pass2c.replace(
            "The 18 governed limitations fall into six conceptual groups.",
            "The governed limitations fall into six conceptual groups.",
            1,
        )
        self.assertEqual(self.canonical, expected)
        self.assertEqual(
            sha256(CANONICAL),
            "6e2960155e7749a917fcdeb7afa3a2fd70a4b7882dacb59ce83796b392af731b",
        )

    def test_canonical_pointer_is_unambiguous(self) -> None:
        pointer = (MANUSCRIPT / "README.md").read_text(encoding="utf-8-sig")
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        self.assertIn(
            "CANONICAL SCIENTIFIC CONTENT:** `manuscript/manuscript_final_content.md`",
            pointer,
        )
        self.assertIn("must not be used for formatting or submission", pointer)
        self.assertIn("manuscript/manuscript_final_content.md", root_readme)

    def test_title_and_word_counts_are_frozen(self) -> None:
        self.assertTrue(self.canonical.startswith(f"# {TITLE}\n"))
        abstract = self.canonical.split("## Abstract", 1)[1].split(
            "## 1. Introduction", 1
        )[0]
        self.assertEqual(len(abstract.split()), 201)
        self.assertEqual(len(self.canonical.split()), 7176)

    def test_abstract_rounding_gate_and_full_precision(self) -> None:
        abstract = self.canonical.split("## Abstract", 1)[1].split(
            "## 1. Introduction", 1
        )[0]
        self.assertIn("PR-AUC 0.667483", abstract)
        self.assertIn("PR-AUC 0.108176", abstract)
        self.assertNotRegex(abstract, r"0\.67(?!\d)")
        self.assertNotRegex(abstract, r"0\.11(?!\d)")
        table3 = self.canonical.split("**Table 3.", 1)[1].split("### 5.5", 1)[0]
        self.assertIn("0.667483", table3)
        self.assertIn("0.108176", table3)
        registry = {
            row["number_id"]: row
            for row in read_csv(STAGE29 / "evidence" / "final_manuscript_numbers.csv")
        }
        for number_id, value in (("NUM29-091", "0.667483"), ("NUM29-094", "0.108176")):
            self.assertEqual(registry[number_id]["value"], value)
            self.assertEqual(registry[number_id]["allowed_rounding"], "6 decimals")
            abstract_rows = [
                row
                for row in self.numbers
                if row["number_id"] == number_id
                and row["manuscript_location"].startswith("Abstract")
            ]
            self.assertEqual(len(abstract_rows), 1)
            self.assertEqual(abstract_rows[0]["frozen_source_value"], value)
            self.assertEqual(abstract_rows[0]["displayed_manuscript_value"], value)
            self.assertIn("TWO_DECIMAL_DISPLAY_NOT_AUTHORIZED", abstract_rows[0]["rounding_authorization"])

    def test_all_limitations_and_groups_remain_governed(self) -> None:
        registry_ids = {
            row["limitation_id"]
            for row in read_csv(STAGE29 / "manuscript" / "limitations_matrix.csv")
        }
        self.assertIn("The governed limitations fall into six conceptual groups.", self.canonical)
        self.assertNotIn("18 governed limitations", self.canonical)
        self.assertEqual(len(self.limitations), 18)
        self.assertEqual({row["limitation_id"] for row in self.limitations}, registry_ids)
        self.assertEqual(set(re.findall(r"LIM29-\d{3}", self.canonical)), registry_ids)
        self.assertEqual(len({row["main_text_group"] for row in self.limitations}), 6)
        self.assertTrue(all(row["claim_ceiling_preserved"] == "YES" for row in self.limitations))

    def test_claim_and_number_resolution_remain_total(self) -> None:
        self.assertEqual(len(self.claims), 124)
        self.assertEqual({row["occurrence_status"] for row in self.claims}, {"RESOLVED"})
        self.assertEqual(len(self.numbers), 137)
        self.assertEqual({row["status"] for row in self.numbers}, {"RESOLVED"})
        pass2c_numbers = read_csv(PASS2C / "FINAL_NUMBER_AUDIT.csv")
        before = Counter((row["number_id"], row["manuscript_value"]) for row in pass2c_numbers)
        after = Counter(
            (row["number_id"], row["displayed_manuscript_value"])
            for row in self.numbers
        )
        self.assertEqual(after, before)

    def test_references_remain_complete_and_unchanged(self) -> None:
        bib_text = BIBLIOGRAPHY.read_text(encoding="utf-8-sig")
        keys = re.findall(r"(?m)^@[A-Za-z]+\{([^,]+),", bib_text)
        cited = set(re.findall(r"@([A-Za-z0-9_:-]+)", self.canonical))
        self.assertEqual(len(keys), 27)
        self.assertEqual(len(set(keys)), 27)
        self.assertEqual(cited, set(keys))
        self.assertEqual(len(self.citations), 27)
        self.assertEqual({row["status"] for row in self.citations}, {"RESOLVED"})
        self.assertEqual(
            sha256(BIBLIOGRAPHY),
            "b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec",
        )

    def test_figures_tables_and_evidence_tensions_are_preserved(self) -> None:
        figures = read_csv(PASS2B / "FINAL_FIGURE_REGISTRY.csv")
        tables = read_csv(PASS2B / "FINAL_TABLE_REGISTRY.csv")
        self.assertEqual(len({row["figure_number"] for row in figures}), 6)
        self.assertEqual(len(figures), 9)
        self.assertEqual(len(tables), 6)
        self.assertEqual(len(self.tensions), 7)
        self.assertEqual({row["status"] for row in self.tensions}, {"PRESERVED"})

    def test_internal_draft_metadata_is_absent(self) -> None:
        lower = self.canonical.lower()
        for phrase in (
            "manuscript status", "draft status", "internal audit", "pass 1",
            "pass 2", "pass2a", "pass2b", "pass 2c", "pass2c", "stage29 synthesis",
        ):
            self.assertNotIn(phrase, lower)

    def test_license_is_scoped_and_datasets_are_excluded(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8-sig")
        audit = (RELEASE / "LICENSE_AUDIT.md").read_text(encoding="utf-8-sig")
        dataset = (ROOT / "DATASET.md").read_text(encoding="utf-8-sig")
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 J. M. Mubasshir Rahman", license_text)
        self.assertIn("does not grant rights to external datasets", license_text)
        self.assertIn("730 binary or publication-artifact files", audit)
        self.assertIn("MIT License does not apply to CSE-CIC-IDS2018", dataset)

    def test_citation_cff_has_supported_metadata_only(self) -> None:
        cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8-sig")
        self.assertNotIn("\t", cff)
        for line in (
            'cff-version: "1.2.0"',
            'title: "IDS Validation Under Distribution, Operational, and Provenance Constraints"',
            "type: software",
            'family-names: "Rahman"',
            'given-names: "J. M. Mubasshir"',
            'version: "pre-release"',
            "license: MIT",
        ):
            self.assertIn(line, cff)
        for invented in ("doi:", "journal:", "volume:", "pages:", "date-released:", "preferred-citation:"):
            self.assertNotIn(invented, cff)

    def test_artifact_appendix_has_all_eighteen_sections(self) -> None:
        appendix = (RELEASE / "ARTIFACT_EVALUATION_APPENDIX.md").read_text(
            encoding="utf-8-sig"
        )
        sections = re.findall(r"(?m)^## (\d+)\. ", appendix)
        self.assertEqual(sections, [str(index) for index in range(1, 19)])
        self.assertIn("Stage 25 only", appendix)
        self.assertIn("historical timings archival", appendix)
        self.assertIn("does not claim full end-to-end reproduction", appendix)

    def test_release_checklist_has_no_dynamic_pending_items(self) -> None:
        checklist = (RELEASE / "RELEASE_READINESS_CHECKLIST.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertNotIn("| PENDING |", checklist)
        for item in (
            "Canonical manuscript is unambiguous",
            "All JSON configs parse",
            "All CSV registries parse",
            "Release tag not yet created",
            "Zenodo DOI not yet minted",
            "Abstract rounding governance",
            "Archive rights scope",
        ):
            self.assertIn(item, checklist)

    def test_all_json_configs_parse(self) -> None:
        paths = sorted((ROOT / "configs").rglob("*.json"))
        self.assertEqual(len(paths), 33)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                with path.open(encoding="utf-8-sig") as handle:
                    self.assertIsInstance(json.load(handle), dict)

    def test_all_governed_csv_registries_parse(self) -> None:
        roots = (
            ROOT / "docs",
            ROOT / "environment",
            ROOT / "manuscript",
            STAGE29,
        )
        paths = sorted({path for root in roots for path in root.rglob("*.csv")})
        self.assertEqual(len(paths), 54)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    rows = csv.reader(handle)
                    header = next(rows)
                    self.assertTrue(header)
                    for row in rows:
                        if row:
                            self.assertEqual(len(row), len(header))

    def test_stage28_wall_and_no_scientific_execution_remain_intact(self) -> None:
        boundary = (ROOT / "docs" / "reproducibility" / "SCIENTIFIC_EXECUTION_BOUNDARY.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("Stage28 is the final empirical stage", boundary)
        self.assertIn("Stage29 and all later work", boundary)
        self.assertIn("may not", boundary)
        for config in (ROOT / "configs").rglob("*.json"):
            text = config.read_text(encoding="utf-8-sig").lower()
            self.assertNotIn('"scientific_execution_allowed": true', text)
        protocol_cli = (
            ROOT / "src" / "ids_validation" / "common" / "protocol_cli.py"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("--dry-run", protocol_cli)
        self.assertIn("--verify-only", protocol_cli)
        self.assertNotIn("--execute", protocol_cli)
        for stage in range(1, 29):
            wrapper = (ROOT / "scripts" / f"reproduce_stage{stage:02d}.py").read_text(
                encoding="utf-8-sig"
            )
            self.assertIn(f"run_protocol_cli({stage})", wrapper)
            self.assertNotIn("--execute", wrapper)


if __name__ == "__main__":
    unittest.main()
