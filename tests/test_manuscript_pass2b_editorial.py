from __future__ import annotations

import csv
import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS2B = ROOT / "docs" / "manuscript" / "pass2b"
CANDIDATE = ROOT / "manuscript" / "manuscript_submission_candidate.md"
BASELINE = ROOT / "manuscript" / "manuscript_reconstructed.md"
BIBLIOGRAPHY = ROOT / "manuscript" / "references.bib"
STAGE29 = ROOT / "results" / "stage29_manuscript_synthesis"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def bibliography_keys(text: str) -> list[str]:
    return re.findall(r"(?m)^@[A-Za-z]+\{([^,]+),", text)


class ManuscriptPass2BEditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate = CANDIDATE.read_text(encoding="utf-8-sig")
        cls.baseline = BASELINE.read_text(encoding="utf-8-sig")
        cls.bib_text = BIBLIOGRAPHY.read_text(encoding="utf-8-sig")
        cls.claims = read_csv(PASS2B / "FINAL_CLAIM_AUDIT.csv")
        cls.numbers = read_csv(PASS2B / "FINAL_NUMBER_AUDIT.csv")
        cls.citations = read_csv(PASS2B / "FINAL_CITATION_AUDIT.csv")
        cls.figures = read_csv(PASS2B / "FINAL_FIGURE_REGISTRY.csv")
        cls.tables = read_csv(PASS2B / "FINAL_TABLE_REGISTRY.csv")
        cls.language = read_csv(PASS2B / "HIGH_RISK_LANGUAGE_AUDIT.csv")
        cls.stage29_claims = read_csv(
            STAGE29 / "claims" / "final_claim_registry.csv"
        )
        cls.stage29_numbers = read_csv(
            STAGE29 / "evidence" / "final_manuscript_numbers.csv"
        )
        cls.stage29_limitations = read_csv(
            STAGE29 / "manuscript" / "limitations_matrix.csv"
        )

    def test_required_pass2b_artifacts_exist_and_are_nonempty(self) -> None:
        required = (
            PASS2B / "PASS2B_EDITORIAL_PROTOCOL.md",
            PASS2B / "FINAL_TITLE_DECISION.md",
            PASS2B / "EVIDENCE_TENSION_AUDIT.md",
            PASS2B / "FINAL_FIGURE_REGISTRY.csv",
            PASS2B / "FINAL_TABLE_REGISTRY.csv",
            PASS2B / "FINAL_SUPPLEMENT_PLAN.md",
            PASS2B / "HIGH_RISK_LANGUAGE_AUDIT.csv",
            PASS2B / "FINAL_CLAIM_AUDIT.csv",
            PASS2B / "FINAL_NUMBER_AUDIT.csv",
            PASS2B / "FINAL_CITATION_AUDIT.csv",
            PASS2B / "LATEX_MIGRATION_PLAN.md",
            PASS2B / "PASS2B_CHANGELOG.md",
            CANDIDATE,
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

    def test_title_abstract_word_count_and_structure(self) -> None:
        self.assertTrue(
            self.candidate.startswith(
                "# Beyond Benchmark Scores: A Multi-Axis Validation Framework "
                "for Intrusion Detection"
            )
        )
        abstract = self.candidate.split("## Abstract", 1)[1].split(
            "## 1. Introduction", 1
        )[0]
        self.assertGreaterEqual(len(abstract.split()), 200)
        self.assertLessEqual(len(abstract.split()), 275)
        self.assertEqual(len(self.candidate.split()), 7523)
        self.assertGreaterEqual(len(self.candidate.split()), 7500)
        self.assertLessEqual(len(self.candidate.split()), 8500)
        h2 = re.findall(r"(?m)^## (.+)$", self.candidate)
        self.assertEqual(len(h2), 11)
        self.assertEqual(
            h2[:9],
            [
                "Abstract",
                "1. Introduction",
                "2. Related Work",
                "3. Datasets and Provenance",
                "4. Validation Framework and Methods",
                "5. Results",
                "6. Discussion",
                "7. Limitations",
                "8. Conclusion",
            ],
        )
        self.assertNotRegex(self.candidate, r"(?m)^#{2,3}\s+Stage\s*\d+")

    def test_reconstructed_manuscript_and_bibliography_remain_frozen(self) -> None:
        self.assertEqual(
            hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
            "b0495f7aa48b1b30876cd5ef2b428a876f4020bb7641043a4a6a09bc33bcc8f8",
        )
        self.assertEqual(
            hashlib.sha256(BIBLIOGRAPHY.read_bytes()).hexdigest(),
            "b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec",
        )
        empirical = self.baseline.split(
            "## 4. Validation Framework and Methods", 1
        )[1].split("## References", 1)[0]
        self.assertEqual(
            hashlib.sha256(empirical.encode()).hexdigest(),
            "ed4d2a278b4d5db7d1dbb9f7de45926cd7f6de9e64a13b0c785522005bd52ffe",
        )

    def test_claim_occurrences_resolve_and_status_boundaries_hold(self) -> None:
        self.assertEqual(len(self.claims), 115)
        self.assertEqual({row["occurrence_status"] for row in self.claims}, {"RESOLVED"})
        registry = {row["claim_id"]: row for row in self.stage29_claims}
        for row in self.claims:
            with self.subTest(audit_id=row["audit_id"]):
                self.assertIn(row["claim_id"], registry)
                self.assertTrue(row["evidence_ids"])
                self.assertTrue(row["qualifier_present"].startswith("YES:"))
                self.assertTrue(row["limitation_link"])
                self.assertEqual(row["registry_status"], registry[row["claim_id"]]["status"])
        audited_ids = {row["claim_id"] for row in self.claims}
        self.assertNotIn("CLM29-017", audited_ids)
        self.assertNotIn("CLM29-018", audited_ids)
        self.assertFalse(
            audited_ids.intersection({"CLM29-019", "CLM29-020"})
        )
        supplement_only = [
            row for row in self.claims if row["registry_status"] == "SUPPLEMENT_ONLY"
        ]
        self.assertEqual(
            {(row["claim_id"], row["manuscript_location"]) for row in supplement_only},
            {("CLM29-006", "Supplement S2"), ("CLM29-007", "Supplement S2")},
        )

    def test_removed_rewrite_and_prohibited_claims_are_absent(self) -> None:
        lower = self.candidate.lower()
        prohibited = (
            "the model generalizes",
            "the model detects zero-day attacks",
            "temporal splitting causes catastrophic performance collapse",
            "shortcut features cause cross-dataset transfer failure",
            "deep learning is universally inferior",
            "the model is operationally useless",
            "the ids literature is invalid",
            "supervised ids cannot detect novel attacks",
            "graph context causally improves intrusion detection",
            "hardware-independent deployment constants",
            "aggregate zero-day score",
        )
        for phrase in prohibited:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, lower)
        main = self.candidate.split("## Supplementary Material Plan", 1)[0]
        self.assertNotIn("strong ranking coexisted with zero detection", main.lower())
        self.assertNotIn("vit run ranked higher", main.lower())

    def test_scientific_number_occurrences_resolve_without_drift(self) -> None:
        self.assertEqual(len(self.numbers), 137)
        self.assertEqual({row["status"] for row in self.numbers}, {"RESOLVED"})
        registry_ids = {row["number_id"] for row in self.stage29_numbers}
        baseline_rows = read_csv(ROOT / "docs" / "manuscript" / "MANUSCRIPT_NUMBER_AUDIT.csv")
        baseline_pairs = {
            (row["number_id"], row["manuscript_value"])
            for row in baseline_rows
            if row["resolution_type"] != "NON_RESULT_METADATA"
        }
        candidate_lines = self.candidate.splitlines()
        for row in self.numbers:
            with self.subTest(audit_id=row["audit_id"]):
                ids = split_ids(row["number_id"])
                self.assertTrue(set(ids).issubset(registry_ids))
                self.assertTrue(
                    all((number_id, row["manuscript_value"]) in baseline_pairs for number_id in ids)
                )
                line_match = re.search(r"line (\d+)", row["manuscript_location"])
                self.assertIsNotNone(line_match)
                line = candidate_lines[int(line_match.group(1)) - 1]
                self.assertIn(row["manuscript_value"], line)
                self.assertTrue(row["source_artifact"])
                self.assertTrue(row["evidence_id"])
                self.assertTrue(row["allowed_rounding"])

    def test_citations_and_bibliography_are_total_and_unchanged(self) -> None:
        cited = set(re.findall(r"@([A-Za-z0-9_:-]+)", self.candidate))
        keys = bibliography_keys(self.bib_text)
        self.assertEqual(len(keys), 27)
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(cited, set(keys))
        self.assertEqual(len(self.citations), 27)
        self.assertEqual({row["citation_key"] for row in self.citations}, set(keys))
        self.assertEqual({row["status"] for row in self.citations}, {"RESOLVED"})
        self.assertEqual(
            {row["orphan_status"] for row in self.citations}, {"USED_AND_MAPPED"}
        )
        self.assertTrue(all(row["scope_preserved"] == "YES" for row in self.citations))
        self.assertNotIn("[REFERENCE GAP:", self.candidate)

    def test_main_figure_registry_resolves_to_unchanged_sources(self) -> None:
        self.assertEqual(len(self.figures), 9)
        self.assertEqual(
            {row["figure_number"] for row in self.figures},
            {f"Figure {index}" for index in range(1, 7)},
        )
        stage29_main = {
            row["figure_candidate"]
            for row in read_csv(STAGE29 / "figures" / "final_figure_registry.csv")
            if row["main_or_supplement"] == "MAIN"
        }
        self.assertEqual({row["stage29_candidate"] for row in self.figures}, stage29_main)
        for row in self.figures:
            with self.subTest(candidate=row["stage29_candidate"]):
                self.assertTrue((ROOT / row["source_artifact"]).is_file())
                self.assertEqual(row["status"], "RESOLVED")
                self.assertIn(row["source_artifact"], self.candidate)
                self.assertTrue(row["final_caption"])

    def test_main_table_registry_is_complete_and_nonredundant(self) -> None:
        self.assertEqual(len(self.tables), 6)
        self.assertEqual(
            {row["table_number"] for row in self.tables},
            {f"Table {index}" for index in range(1, 7)},
        )
        stage29_main = {
            row["table_candidate"]
            for row in read_csv(STAGE29 / "figures" / "final_table_registry.csv")
            if row["main_or_supplement"] == "MAIN"
        }
        self.assertEqual({row["stage29_candidate"] for row in self.tables}, stage29_main)
        self.assertTrue(all(row["disposition"] == "MAIN" for row in self.tables))
        self.assertTrue(all(row["status"] == "RESOLVED" for row in self.tables))
        self.assertTrue(all((ROOT / row["source_artifact"]).is_file() for row in self.tables))
        for index in range(1, 7):
            self.assertIn(f"**Table {index}.", self.candidate)

    def test_all_limitations_and_evidence_tensions_are_preserved(self) -> None:
        limitation_ids = {row["limitation_id"] for row in self.stage29_limitations}
        self.assertEqual(
            set(re.findall(r"LIM29-\d{3}", self.candidate)), limitation_ids
        )
        tension_text = (PASS2B / "EVIDENCE_TENSION_AUDIT.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertEqual(len(re.findall(r"\| \*\*PRESERVED\*\* \|", tension_text)), 7)
        self.assertNotIn("**WEAKENED**", tension_text)
        self.assertNotIn("**LOST**", tension_text)

    def test_high_risk_language_occurrences_are_exhaustively_reviewed(self) -> None:
        terms = (
            "prove", "proves", "proven", "catastrophic", "useless", "unusable",
            "real-world", "zero-day", "generalizes", "robust", "secure",
            "deployment-ready", "state-of-the-art", "superior", "causes",
            "because of", "driven by", "field-wide", "most studies", "all models",
        )
        occurrences: list[tuple[str, int]] = []
        for term in terms:
            pattern = rf"(?i)\b{re.escape(term)}\b"
            occurrences.extend((term, match.start()) for match in re.finditer(pattern, self.candidate))
        self.assertEqual([term for term, _ in occurrences], ["proven"])
        self.assertEqual(len(self.language), 1)
        self.assertEqual(self.language[0]["term"], "proven")
        self.assertEqual(self.language[0]["supported"], "YES_NEGATED_AND_BOUNDARY_PRESERVING")
        self.assertEqual(self.language[0]["action"], "KEEP_REVIEWED")

    def test_supplement_and_latex_plans_preserve_stop_condition(self) -> None:
        supplement = (PASS2B / "FINAL_SUPPLEMENT_PLAN.md").read_text(
            encoding="utf-8-sig"
        )
        latex = (PASS2B / "LATEX_MIGRATION_PLAN.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertEqual(len(re.findall(r"(?m)^## S\d+\.", supplement)), 7)
        self.assertIn("venue template not selected", latex.lower())
        self.assertIn("must not begin under the present authorization", latex.lower())

    def test_stage28_wall_and_no_new_computation_boundary(self) -> None:
        freeze = (
            STAGE29 / "stage29_0_synthesis_lock" / "stage29_freeze_record.json"
        ).read_text(encoding="utf-8-sig")
        self.assertIn('"stage28_final_empirical_stage": true', freeze)
        self.assertIn('"stage29_experimental": false', freeze)
        lower = self.candidate.lower()
        for phrase in (
            "we fit a new",
            "we trained a new",
            "we recomputed prevalence",
            "we generated bootstrap",
            "new composite score",
        ):
            self.assertNotIn(phrase, lower)


if __name__ == "__main__":
    unittest.main()
