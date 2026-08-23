from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "manuscript_reconstructed.md"
DOCS = ROOT / "docs" / "manuscript"
STAGE29 = ROOT / "results" / "stage29_manuscript_synthesis"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


class ManuscriptPass1ProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = MANUSCRIPT.read_text(encoding="utf-8-sig")
        cls.claims = read_csv(STAGE29 / "claims" / "final_claim_registry.csv")
        cls.evidence = read_csv(STAGE29 / "evidence" / "master_evidence_matrix.csv")
        cls.numbers = read_csv(
            STAGE29 / "evidence" / "final_manuscript_numbers.csv"
        )
        cls.limitations = read_csv(
            STAGE29 / "manuscript" / "limitations_matrix.csv"
        )
        cls.figures = read_csv(STAGE29 / "figures" / "final_figure_registry.csv")
        cls.tables = read_csv(STAGE29 / "figures" / "final_table_registry.csv")
        cls.claim_audit = read_csv(DOCS / "MANUSCRIPT_CLAIM_AUDIT.csv")
        cls.number_audit = read_csv(DOCS / "MANUSCRIPT_NUMBER_AUDIT.csv")
        cls.source_map = read_csv(DOCS / "MANUSCRIPT_SOURCE_MAP.csv")
        cls.figure_plan = (DOCS / "MANUSCRIPT_FIGURE_TABLE_PLAN.md").read_text(
            encoding="utf-8-sig"
        )
        cls.reference_audit = (DOCS / "MANUSCRIPT_REFERENCE_AUDIT.md").read_text(
            encoding="utf-8-sig"
        )

    def test_required_pass1_artifacts_exist_and_are_nonempty(self) -> None:
        required = (
            MANUSCRIPT,
            DOCS / "TITLE_OPTIONS.md",
            DOCS / "MANUSCRIPT_SOURCE_MAP.csv",
            DOCS / "MANUSCRIPT_NUMBER_AUDIT.csv",
            DOCS / "MANUSCRIPT_CLAIM_AUDIT.csv",
            DOCS / "MANUSCRIPT_FIGURE_TABLE_PLAN.md",
            DOCS / "MANUSCRIPT_REFERENCE_AUDIT.md",
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)
        self.assertIn("Pass 1 evidence-governed reconstruction", self.text)
        self.assertIn("This document is not final", self.text)

    def test_integrated_manuscript_has_the_approved_section_structure(self) -> None:
        required_headings = (
            "## Abstract",
            "## 1. Introduction",
            "## 2. Related Work",
            "## 3. Datasets and Provenance",
            "## 4. Validation Framework and Methods",
            "## 5. Results",
            "## 6. Discussion",
            "## 7. Limitations",
            "## 8. Conclusion",
            "## References",
            "## Supplementary Material Plan",
        )
        positions = [self.text.index(heading) for heading in required_headings]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(self.text.count("**Figure "), 6)
        self.assertEqual(self.text.count("**Table "), 6)

    def test_claim_audit_resolves_and_uses_only_main_narrative_claims(self) -> None:
        claim_by_id = {row["claim_id"]: row for row in self.claims}
        evidence_ids = {row["evidence_id"] for row in self.evidence}
        limitation_ids = {row["limitation_id"] for row in self.limitations}
        audit_ids = [row["audit_id"] for row in self.claim_audit]
        self.assertEqual(len(audit_ids), len(set(audit_ids)))

        expected_main_claims = {
            row["claim_id"]
            for row in self.claims
            if row["status"] in {"KEEP", "KEEP_WITH_QUALIFICATION"}
            and row["claim_id"] not in {"CLM29-006", "CLM29-007"}
        }
        audited_claims = {row["claim_id"] for row in self.claim_audit}
        self.assertEqual(audited_claims, expected_main_claims)

        for row in self.claim_audit:
            with self.subTest(audit=row["audit_id"]):
                self.assertIn(row["claim_id"], claim_by_id)
                self.assertNotIn(
                    claim_by_id[row["claim_id"]]["status"],
                    {"REMOVE", "REWRITE", "SUPPLEMENT_ONLY"},
                )
                self.assertTrue(set(split_ids(row["evidence_ids"])).issubset(evidence_ids))
                self.assertTrue(
                    set(split_ids(row["limitation_link"])).issubset(limitation_ids)
                )
                self.assertTrue(row["qualifier_present"].startswith("YES:"))
                self.assertEqual(row["status"], "RESOLVED")

    def test_removed_claims_and_supplement_only_results_do_not_enter_main_text(self) -> None:
        removed_exact = [
            row["claim_text"]
            for row in self.claims
            if row["status"] == "REMOVE"
        ]
        for claim_text in removed_exact:
            with self.subTest(claim=claim_text):
                self.assertNotIn(claim_text, self.text)

        supplement_only_result_phrases = (
            "source-restricted graph subset strong ranking coexisted",
            "frozen Stage21 ViT run ranked higher",
            "source-restricted graph experiment achieved strong",
        )
        for phrase in supplement_only_result_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), self.text.lower())

    def test_number_audit_resolves_to_frozen_stage29_numbers_or_metadata(self) -> None:
        number_ids = {row["number_id"] for row in self.numbers}
        evidence_ids = {row["evidence_id"] for row in self.evidence}
        audit_ids = [row["audit_id"] for row in self.number_audit]
        self.assertEqual(len(audit_ids), len(set(audit_ids)))

        allowed_resolution_types = {
            "EXACT",
            "ROUNDED",
            "FORMATTED",
            "NON_RESULT_METADATA",
        }
        for row in self.number_audit:
            with self.subTest(audit=row["audit_id"]):
                self.assertIn(row["resolution_type"], allowed_resolution_types)
                self.assertTrue(row["manuscript_value"].strip())
                self.assertTrue((ROOT / row["source_artifact"]).is_file())
                audit_evidence = set(split_ids(row["evidence_id"])) - {"NONE"}
                self.assertTrue(audit_evidence.issubset(evidence_ids))
                if row["resolution_type"] == "NON_RESULT_METADATA":
                    self.assertTrue(row["number_id"].startswith("META29-"))
                else:
                    self.assertIn(row["number_id"], number_ids)

    def test_source_map_covers_every_manuscript_section_and_subsection(self) -> None:
        mapped = {row["manuscript_subsection"] for row in self.source_map}
        map_ids = [row["map_id"] for row in self.source_map]
        self.assertEqual(len(map_ids), len(set(map_ids)))
        headings = re.findall(r"^#{2,3} (.+)$", self.text, flags=re.MULTILINE)
        self.assertEqual(set(headings), mapped)
        for row in self.source_map:
            with self.subTest(map_id=row["map_id"]):
                self.assertTrue(row["stage29_artifacts"].strip())
                self.assertTrue(row["frozen_results"].strip())
                self.assertTrue(row["reproduction_index_entries"].strip())

    def test_all_eighteen_stage29_limitation_concepts_are_present(self) -> None:
        limitation_section = self.text.split("## 7. Limitations", 1)[1].split(
            "## 8. Conclusion", 1
        )[0].lower()
        expected_markers = {
            "LIM29-001": "benchmark-family scope",
            "LIM29-002": "processed reference condition",
            "LIM29-003": "temporal/family entanglement",
            "LIM29-004": "bridge restriction",
            "LIM29-005": "cancelled membership cells",
            "LIM29-006": "loao eligibility",
            "LIM29-007": "low-support infiltration",
            "LIM29-008": "conditional resampling uncertainty",
            "LIM29-009": "finite seed scope",
            "LIM29-010": "historical environment ambiguity",
            "LIM29-011": "hardware and component boundary",
            "LIM29-012": "prior-probability shift",
            "LIM29-013": "workload and cost scenarios",
            "LIM29-014": "incomplete full-rerun reproducibility",
            "LIM29-015": "unavailable external artifacts",
            "LIM29-016": "source-restricted graph evidence",
            "LIM29-017": "descriptive architecture comparison",
            "LIM29-018": "historically reused target",
        }
        self.assertEqual(set(expected_markers), {row["limitation_id"] for row in self.limitations})
        for limitation_id, marker in expected_markers.items():
            with self.subTest(limitation=limitation_id):
                self.assertIn(marker, limitation_section)

    def test_figure_and_table_plan_uses_every_approved_main_exhibit(self) -> None:
        main_figures = {
            row["figure_candidate"]
            for row in self.figures
            if row["main_or_supplement"] == "MAIN"
        }
        main_tables = {
            row["table_candidate"]
            for row in self.tables
            if row["main_or_supplement"] == "MAIN"
        }
        for exhibit in sorted(main_figures | main_tables):
            with self.subTest(exhibit=exhibit):
                self.assertIn(f"`{exhibit}`", self.figure_plan)

        planned_paths = re.findall(
            r"`((?:results|figures|docs)/[^`]+)`", self.figure_plan
        )
        self.assertGreaterEqual(len(set(planned_paths)), 18)
        for relative in planned_paths:
            with self.subTest(source=relative):
                self.assertTrue((ROOT / relative).is_file())

        self.assertIn("does not redraw, merge, crop, recolor, relabel, or recompute", self.figure_plan)
        self.assertIn("Do not combine in Pass 1", self.figure_plan)

    def test_reference_gaps_are_complete_and_no_citations_are_invented(self) -> None:
        manuscript_gap_count = self.text.count("[REFERENCE GAP:")
        audit_gap_ids = re.findall(r"^\| (REF-GAP-\d{3}) \|", self.reference_audit, re.MULTILINE)
        self.assertEqual(manuscript_gap_count, 10)
        self.assertEqual(len(audit_gap_ids), 10)
        self.assertEqual(len(audit_gap_ids), len(set(audit_gap_ids)))
        self.assertIn("External browsing performed: **no**", self.reference_audit)
        for citation_pattern in (r"https?://", r"\[@[^\]]+\]", r"\\cite\{"):
            with self.subTest(pattern=citation_pattern):
                self.assertIsNone(re.search(citation_pattern, self.text))

    def test_manuscript_remains_a_stage29_synthesis_not_new_science(self) -> None:
        prohibited_methods = (
            "we fit a new",
            "we trained a new",
            "we optimized the threshold",
            "we recomputed prevalence",
            "we generated bootstrap",
            "new composite score",
        )
        for phrase in prohibited_methods:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.text.lower())
        self.assertIn("synthesis of frozen evidence rather than a new empirical score", self.text)


if __name__ == "__main__":
    unittest.main()
