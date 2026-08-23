from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "results" / "stage29_manuscript_synthesis"


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


class Stage29SynthesisConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = read_csv(
            "results/stage29_manuscript_synthesis/evidence/master_evidence_matrix.csv"
        )
        cls.classification = read_csv(
            "results/stage29_manuscript_synthesis/evidence/evidence_classification.csv"
        )
        cls.claims = read_csv(
            "results/stage29_manuscript_synthesis/claims/final_claim_registry.csv"
        )
        cls.claim_map = read_csv(
            "results/stage29_manuscript_synthesis/claims/claim_to_artifact_map.csv"
        )
        cls.figures = read_csv(
            "results/stage29_manuscript_synthesis/figures/final_figure_registry.csv"
        )
        cls.tables = read_csv(
            "results/stage29_manuscript_synthesis/figures/final_table_registry.csv"
        )
        cls.limitations = read_csv(
            "results/stage29_manuscript_synthesis/manuscript/limitations_matrix.csv"
        )
        cls.graph = read_csv(
            "results/stage29_manuscript_synthesis/manuscript/claim_figure_table_graph.csv"
        )
        cls.numbers = read_csv(
            "results/stage29_manuscript_synthesis/evidence/final_manuscript_numbers.csv"
        )

    def test_all_stage29_csv_and_json_files_parse(self) -> None:
        parsed_csv = 0
        parsed_json = 0
        for path in SYNTHESIS.rglob("*"):
            if path.suffix == ".csv":
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertTrue(rows, path.relative_to(ROOT).as_posix())
                parsed_csv += 1
            elif path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8-sig"))
                parsed_json += 1
        self.assertGreaterEqual(parsed_csv, 14)
        self.assertGreaterEqual(parsed_json, 8)

    def test_primary_identifiers_are_unique(self) -> None:
        checks = (
            (self.evidence, "evidence_id"),
            (self.classification, "evidence_id"),
            (self.claims, "claim_id"),
            (self.claim_map, "claim_id"),
            (self.figures, "figure_candidate"),
            (self.tables, "table_candidate"),
            (self.limitations, "limitation_id"),
            (self.graph, "claim_id"),
            (self.numbers, "number_id"),
        )
        for rows, field in checks:
            with self.subTest(field=field):
                values = [row[field] for row in rows]
                self.assertEqual(len(values), len(set(values)))

    def test_evidence_classification_is_complete_and_consistent(self) -> None:
        matrix = {row["evidence_id"]: row["evidence_status"] for row in self.evidence}
        classification = {
            row["evidence_id"]: row["evidence_status"] for row in self.classification
        }
        self.assertEqual(matrix, classification)
        self.assertIn("CANCELLED", set(matrix.values()))
        self.assertIn("LOW_SUPPORT", set(matrix.values()))
        self.assertIn("HARDWARE_SPECIFIC", set(matrix.values()))
        self.assertIn("NEGATIVE_RESULT", set(matrix.values()))

    def test_every_nonremoved_final_claim_resolves_to_evidence(self) -> None:
        evidence_ids = {row["evidence_id"] for row in self.evidence}
        map_ids = {row["claim_id"] for row in self.claim_map}
        for claim in self.claims:
            with self.subTest(claim=claim["claim_id"]):
                self.assertIn(claim["claim_id"], map_ids)
                supporting = split_ids(claim["supporting_evidence_ids"])
                contradictory = split_ids(claim["contradictory_evidence_ids"])
                if claim["status"] != "REMOVE":
                    self.assertTrue(supporting)
                self.assertTrue(set(supporting + contradictory).issubset(evidence_ids))

    def test_claim_qualification_and_contradiction_rules(self) -> None:
        for claim in self.claims:
            with self.subTest(claim=claim["claim_id"]):
                if claim["status"] == "KEEP_WITH_QUALIFICATION":
                    self.assertTrue(claim["required_qualifier"].strip())
                    self.assertTrue(claim["residual_limitation"].strip())
                if split_ids(claim["contradictory_evidence_ids"]):
                    self.assertIn(
                        claim["status"],
                        {"KEEP_WITH_QUALIFICATION", "REWRITE", "REMOVE"},
                    )

    def test_cancelled_and_low_support_evidence_cannot_overreach(self) -> None:
        status = {row["evidence_id"]: row["evidence_status"] for row in self.evidence}
        for claim in self.claims:
            supporting_statuses = {
                status[evidence_id]
                for evidence_id in split_ids(claim["supporting_evidence_ids"])
            }
            combined = " ".join(
                (
                    claim["claim_text"],
                    claim["required_qualifier"],
                    claim["residual_limitation"],
                    claim["manuscript_section"],
                )
            ).lower()
            with self.subTest(claim=claim["claim_id"]):
                if "CANCELLED" in supporting_statuses:
                    self.assertIn("cancel", combined)
                    self.assertNotIn("Results:", claim["manuscript_section"])
                if "LOW_SUPPORT" in supporting_statuses:
                    self.assertTrue("descriptive" in combined or "support" in combined)

    def test_prohibited_claims_do_not_survive_registry(self) -> None:
        prohibited = (
            "the model generalizes",
            "the model detects zero-day attacks",
            "temporal splitting always causes catastrophic collapse",
            "shortcut features cause all transfer failure",
            "deep learning is universally inferior",
            "operationally useless in all real socs",
            "the ids literature is invalid",
            "supervised ids cannot detect novel attacks",
        )
        retained_text = " ".join(
            row["claim_text"].lower()
            for row in self.claims
            if row["status"] not in {"REMOVE", "REWRITE"}
        )
        for phrase in prohibited:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, retained_text)

    def test_claim_figure_table_graph_resolves(self) -> None:
        claims = {row["claim_id"] for row in self.claims}
        evidence = {row["evidence_id"] for row in self.evidence}
        figures = {row["figure_candidate"] for row in self.figures}
        tables = {row["table_candidate"] for row in self.tables}
        limitations = {row["limitation_id"] for row in self.limitations}
        for row in self.graph:
            with self.subTest(claim=row["claim_id"]):
                self.assertIn(row["claim_id"], claims)
                self.assertTrue(set(split_ids(row["evidence_ids"])).issubset(evidence))
                self.assertTrue(set(split_ids(row["figure"])).issubset(figures))
                self.assertTrue(set(split_ids(row["table"])).issubset(tables))
                self.assertTrue(set(split_ids(row["limitation_ids"])).issubset(limitations))

    def test_every_main_figure_and_table_supports_a_claim(self) -> None:
        graph_figures = {
            figure for row in self.graph for figure in split_ids(row["figure"])
        }
        graph_tables = {table for row in self.graph for table in split_ids(row["table"])}
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
        self.assertTrue(main_figures.issubset(graph_figures))
        self.assertTrue(main_tables.issubset(graph_tables))
        for row in self.figures:
            self.assertTrue((ROOT / row["source_artifact"]).is_file())
        for row in self.tables:
            self.assertTrue((ROOT / row["source_artifact"]).is_file())

    def test_every_manuscript_number_resolves_to_frozen_evidence_and_artifact(self) -> None:
        evidence = {row["evidence_id"] for row in self.evidence}
        for number in self.numbers:
            with self.subTest(number=number["number_id"]):
                self.assertIn(number["evidence_id"], evidence)
                source = ROOT / number["source_artifact"]
                self.assertTrue(source.is_file())
                self.assertNotIn(
                    "results/stage29_manuscript_synthesis",
                    source.relative_to(ROOT).as_posix(),
                )
                self.assertTrue(number["value"].strip())
                self.assertTrue(number["allowed_rounding"].strip())

    def test_no_heterogeneous_composite_or_new_empirical_boundary(self) -> None:
        retained = " ".join(
            row["claim_text"].lower()
            for row in self.claims
            if row["status"] not in {"REMOVE", "REWRITE"}
        )
        self.assertNotIn("composite robustness score", retained)
        self.assertNotIn("aggregate zero-day score", retained)
        lock = json.loads(
            (
                SYNTHESIS
                / "stage29_0_synthesis_lock"
                / "stage29_freeze_record.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(lock["stage28_final_empirical_stage"])
        self.assertFalse(lock["stage29_experimental"])


if __name__ == "__main__":
    unittest.main()
