from __future__ import annotations

import csv
import hashlib
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS2B = ROOT / "docs" / "manuscript" / "pass2b"
PASS2C = ROOT / "docs" / "manuscript" / "pass2c"
BASELINE = ROOT / "manuscript" / "manuscript_submission_candidate.md"
CANDIDATE = ROOT / "manuscript" / "manuscript_submission_candidate_pass2c.md"
BIBLIOGRAPHY = ROOT / "manuscript" / "references.bib"
STAGE29 = ROOT / "results" / "stage29_manuscript_synthesis"
TITLE = "A Multi-Axis Validation Framework for Machine-Learning Intrusion Detection"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def bibliography_keys(text: str) -> list[str]:
    return re.findall(r"(?m)^@[A-Za-z]+\{([^,]+),", text)


class ManuscriptPass2CReadabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = BASELINE.read_text(encoding="utf-8-sig")
        cls.candidate = CANDIDATE.read_text(encoding="utf-8-sig")
        cls.bib_text = BIBLIOGRAPHY.read_text(encoding="utf-8-sig")
        cls.claims = read_csv(PASS2C / "FINAL_CLAIM_AUDIT.csv")
        cls.numbers = read_csv(PASS2C / "FINAL_NUMBER_AUDIT.csv")
        cls.citations = read_csv(PASS2C / "FINAL_CITATION_AUDIT.csv")
        cls.checklist = read_csv(PASS2C / "VALIDATION_CHECKLIST_TRACEABILITY.csv")
        cls.limitations = read_csv(PASS2C / "LIMITATION_PRESENTATION_AUDIT.csv")
        cls.tensions = read_csv(PASS2C / "EVIDENCE_TENSION_PRESERVATION.csv")
        cls.figures = read_csv(PASS2B / "FINAL_FIGURE_REGISTRY.csv")
        cls.tables = read_csv(PASS2B / "FINAL_TABLE_REGISTRY.csv")

    def test_required_pass2c_artifacts_exist_and_are_nonempty(self) -> None:
        required = (
            PASS2C / "PASS2C_PROTOCOL.md",
            PASS2C / "PASS2C_BASELINE_RECEIPT.md",
            PASS2C / "FINAL_TITLE_REASSESSMENT.md",
            PASS2C / "CONTRIBUTION_CONSOLIDATION_AUDIT.md",
            PASS2C / "VALIDATION_CHECKLIST_TRACEABILITY.csv",
            PASS2C / "LIMITATION_PRESENTATION_AUDIT.csv",
            PASS2C / "EVIDENCE_TENSION_PRESERVATION.csv",
            PASS2C / "THESIS_ALIGNMENT_AUDIT.md",
            PASS2C / "FINAL_CLAIM_AUDIT.csv",
            PASS2C / "FINAL_NUMBER_AUDIT.csv",
            PASS2C / "FINAL_CITATION_AUDIT.csv",
            PASS2C / "PASS2C_DIFF_SUMMARY.md",
            CANDIDATE,
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

    def test_pass2b_candidate_remains_immutable(self) -> None:
        self.assertEqual(
            hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
            "c4879bbc4ca6fa6b8d638984ae1cdd0ebfb25114471c9d7c58634a5a0996ca88",
        )
        self.assertNotEqual(BASELINE, CANDIDATE)

    def test_title_is_consistent_and_scope_bounded(self) -> None:
        self.assertTrue(self.candidate.startswith(f"# {TITLE}\n"))
        decision = (PASS2C / "FINAL_TITLE_REASSESSMENT.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn(f"Use **{TITLE}**", decision)
        self.assertNotIn("Development Regime, Not Architecture", self.candidate)

    def test_abstract_order_length_thesis_and_numbers(self) -> None:
        abstract = self.candidate.split("## Abstract", 1)[1].split(
            "## 1. Introduction", 1
        )[0]
        self.assertEqual(len(abstract.split()), 201)
        self.assertGreaterEqual(len(abstract.split()), 200)
        self.assertLessEqual(len(abstract.split()), 275)
        ordered = (
            "multi-axis framework",
            "0.2599",
            "0.9285",
            "0.667483",
            "33.5 analyst-hours",
            "Stronger validation instead narrowed",
        )
        positions = [abstract.find(item) for item in ordered]
        self.assertTrue(all(position >= 0 for position in positions))
        self.assertEqual(positions, sorted(positions))
        for value in (
            "0.2599", "0.6388", "0.9285", "0.9776", "0.667483",
            "0.108176", "0.1%", "33.5",
        ):
            self.assertIn(value, abstract)
        self.assertNotIn("0.67", abstract.replace("0.667483", ""))
        self.assertNotIn("0.11", abstract)
        abstract_rows = [
            row for row in self.numbers if row["manuscript_location"].startswith("Abstract")
        ]
        self.assertTrue(abstract_rows)
        self.assertTrue(all(row["status"] == "RESOLVED" for row in abstract_rows))

    def test_introduction_contains_exactly_four_contributions(self) -> None:
        introduction = self.candidate.split("## 1. Introduction", 1)[1].split(
            "## 2. Related Work", 1
        )[0]
        contribution_block = introduction.split("This study makes four contributions:", 1)[1]
        items = re.findall(r"(?m)^(\d+)\. ", contribution_block)
        self.assertEqual(items, ["1", "2", "3", "4"])
        audit = (PASS2C / "CONTRIBUTION_CONSOLIDATION_AUDIT.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertEqual(audit.count("**NO LOSS**"), 6)

    def test_discussion_contains_exactly_eight_checklist_items(self) -> None:
        section = self.candidate.split(
            "### 6.6 An Eight-Item Validation Checklist", 1
        )[1].split("## 7. Limitations", 1)[0]
        items = re.findall(r"(?m)^(\d+)\. \*\*", section)
        self.assertEqual(items, [str(index) for index in range(1, 9)])
        self.assertEqual(len(self.checklist), 8)
        evidence_ids = {
            row["evidence_id"]
            for row in read_csv(STAGE29 / "evidence" / "master_evidence_matrix.csv")
        }
        claim_ids = {
            row["claim_id"]
            for row in read_csv(STAGE29 / "claims" / "final_claim_registry.csv")
        }
        for row in self.checklist:
            with self.subTest(item=row["checklist_item"]):
                self.assertTrue(set(row["evidence_ids"].split(";")).issubset(evidence_ids))
                self.assertTrue(set(row["claim_ids"].split(";")).issubset(claim_ids))
                self.assertTrue(row["native_metric"])
                self.assertTrue(row["required_control"])
        self.assertNotIn("industry standard", section.lower())
        self.assertNotIn("universally sufficient", section.lower())

    def test_results_question_headings_are_unchanged(self) -> None:
        pattern = r"(?m)^### 5\.[1-9] .+$"
        self.assertEqual(
            re.findall(pattern, self.candidate), re.findall(pattern, self.baseline)
        )

    def test_all_eighteen_limitations_map_into_six_groups(self) -> None:
        registry_ids = {
            row["limitation_id"]
            for row in read_csv(STAGE29 / "manuscript" / "limitations_matrix.csv")
        }
        self.assertEqual(len(self.limitations), 18)
        self.assertEqual({row["limitation_id"] for row in self.limitations}, registry_ids)
        self.assertEqual(
            set(re.findall(r"LIM29-\d{3}", self.candidate)), registry_ids
        )
        self.assertEqual(len({row["main_text_group"] for row in self.limitations}), 6)
        self.assertTrue(all(row["explicit_in_main_text"] == "YES" for row in self.limitations))
        self.assertTrue(all(row["claim_ceiling_preserved"] == "YES" for row in self.limitations))

    def test_all_seven_evidence_tensions_are_preserved(self) -> None:
        self.assertEqual(len(self.tensions), 7)
        self.assertEqual({row["status"] for row in self.tensions}, {"PRESERVED"})
        thesis = (PASS2C / "THESIS_ALIGNMENT_AUDIT.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("ALIGNED at compatible strength", thesis)
        self.assertIn(
            "Stronger validation narrows or qualifies a claim; it does not require "
            "a monotonic performance decline.",
            self.candidate,
        )

    def test_six_figures_and_six_tables_still_resolve(self) -> None:
        self.assertEqual(len({row["figure_number"] for row in self.figures}), 6)
        self.assertEqual(len(self.figures), 9)
        self.assertEqual(len(self.tables), 6)
        for row in self.figures:
            self.assertTrue((ROOT / row["source_artifact"]).is_file())
            self.assertIn(row["source_artifact"], self.candidate)
        for row in self.tables:
            self.assertTrue((ROOT / row["source_artifact"]).is_file())
        for index in range(1, 7):
            self.assertIn(f"**Figure {index}.", self.candidate)
            self.assertIn(f"**Table {index}.", self.candidate)

    def test_claim_audit_is_total_and_contains_no_removed_claims(self) -> None:
        self.assertEqual(len(self.claims), 124)
        self.assertEqual({row["occurrence_status"] for row in self.claims}, {"RESOLVED"})
        ids = {row["claim_id"] for row in self.claims}
        self.assertEqual(ids, {f"CLM29-{index:03d}" for index in range(1, 17)})
        self.assertFalse(ids.intersection({"CLM29-017", "CLM29-018", "CLM29-019", "CLM29-020"}))
        supplement_only = [row for row in self.claims if row["registry_status"] == "SUPPLEMENT_ONLY"]
        self.assertEqual(
            {(row["claim_id"], row["manuscript_location"]) for row in supplement_only},
            {("CLM29-006", "Supplement S2"), ("CLM29-007", "Supplement S2")},
        )

    def test_scientific_number_multiset_is_identical_to_pass2b(self) -> None:
        baseline_numbers = read_csv(PASS2B / "FINAL_NUMBER_AUDIT.csv")
        self.assertEqual(len(self.numbers), 137)
        self.assertEqual({row["status"] for row in self.numbers}, {"RESOLVED"})
        before = Counter((row["number_id"], row["manuscript_value"]) for row in baseline_numbers)
        after = Counter((row["number_id"], row["manuscript_value"]) for row in self.numbers)
        self.assertEqual(after, before)
        candidate_lines = self.candidate.splitlines()
        for row in self.numbers:
            line_number = int(re.search(r"line (\d+)", row["manuscript_location"]).group(1))
            self.assertIn(row["manuscript_value"], candidate_lines[line_number - 1])

    def test_references_and_citations_are_unchanged_and_resolved(self) -> None:
        keys = bibliography_keys(self.bib_text)
        cited = set(re.findall(r"@([A-Za-z0-9_:-]+)", self.candidate))
        self.assertEqual(len(keys), 27)
        self.assertEqual(cited, set(keys))
        self.assertEqual(len(self.citations), 27)
        self.assertEqual({row["citation_key"] for row in self.citations}, set(keys))
        self.assertEqual({row["status"] for row in self.citations}, {"RESOLVED"})
        self.assertTrue(all(row["scope_preserved"] == "YES" for row in self.citations))
        self.assertEqual(
            hashlib.sha256(BIBLIOGRAPHY.read_bytes()).hexdigest(),
            "b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec",
        )

    def test_internal_draft_metadata_is_absent(self) -> None:
        lower = self.candidate.lower()
        for phrase in (
            "manuscript status", "draft status", "internal audit", "pass 1",
            "pass 2", "pass2a", "pass2b", "pass 2c", "pass2c", "stage29 synthesis",
        ):
            self.assertNotIn(phrase, lower)
        self.assertNotRegex(self.candidate, r"(?m)^> \*\*Manuscript status:")

    def test_prohibited_and_high_risk_language_boundaries_hold(self) -> None:
        lower = self.candidate.lower()
        prohibited = (
            "the model generalizes",
            "the model detects zero-day attacks",
            "temporal splitting causes catastrophic performance collapse",
            "shortcut features cause cross-dataset transfer failure",
            "deep learning is universally inferior",
            "the ids literature is invalid",
            "all ids models fail",
            "stronger validation always lowers performance",
            "architecture is irrelevant",
            "industry standard",
            "universally sufficient",
        )
        for phrase in prohibited:
            self.assertNotIn(phrase, lower)
        high_risk_terms = (
            "prove", "proves", "proven", "catastrophic", "useless", "unusable",
            "real-world", "zero-day", "generalizes", "robust", "secure",
            "deployment-ready", "state-of-the-art", "superior", "causes",
            "because of", "driven by", "field-wide", "most studies", "all models",
        )
        found = [
            term
            for term in high_risk_terms
            if re.search(rf"(?i)\b{re.escape(term)}\b", self.candidate)
        ]
        self.assertEqual(found, ["proven"])
        self.assertIn("without treating a field as proven leakage", self.candidate)

    def test_stage28_wall_and_no_new_science_boundary(self) -> None:
        freeze = (
            STAGE29 / "stage29_0_synthesis_lock" / "stage29_freeze_record.json"
        ).read_text(encoding="utf-8-sig")
        self.assertIn('"stage28_final_empirical_stage": true', freeze)
        self.assertIn('"stage29_experimental": false', freeze)
        diff = (PASS2C / "PASS2C_DIFF_SUMMARY.md").read_text(encoding="utf-8-sig")
        for change_class in (
            "SCIENTIFIC_RESULT_CHANGE", "NEW_CLAIM", "NEW_EVIDENCE", "NEW_ANALYSIS",
        ):
            self.assertRegex(diff, rf"\| `{change_class}` \| 0 \|")


if __name__ == "__main__":
    unittest.main()
