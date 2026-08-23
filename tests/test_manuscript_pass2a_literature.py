from __future__ import annotations

import csv
import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS2 = ROOT / "docs" / "manuscript" / "pass2"
MANUSCRIPT = ROOT / "manuscript" / "manuscript_reconstructed.md"
BIBLIOGRAPHY = ROOT / "manuscript" / "references.bib"
STAGE29 = ROOT / "results" / "stage29_manuscript_synthesis"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def bibliography_entries(text: str) -> dict[str, str]:
    starts = list(re.finditer(r"(?m)^@[A-Za-z]+\{([^,]+),", text))
    entries: dict[str, str] = {}
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        entries[match.group(1)] = text[match.start() : end]
    return entries


class ManuscriptPass2ALiteratureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manuscript = MANUSCRIPT.read_text(encoding="utf-8-sig")
        cls.bib_text = BIBLIOGRAPHY.read_text(encoding="utf-8-sig")
        cls.bib_entries = bibliography_entries(cls.bib_text)
        cls.gaps = read_csv(PASS2 / "REFERENCE_GAP_SPECIFICATION.csv")
        cls.claims = read_csv(PASS2 / "LITERATURE_CLAIM_REGISTRY.csv")
        cls.existing = read_csv(PASS2 / "EXISTING_REFERENCE_VERIFICATION.csv")
        cls.candidates = read_csv(PASS2 / "CANDIDATE_REFERENCE_REGISTRY.csv")
        cls.related = read_csv(PASS2 / "RELATED_WORK_CLAIM_AUDIT.csv")
        cls.matrix = read_csv(PASS2 / "CITATION_CLAIM_MATRIX.csv")
        cls.changelog = read_csv(PASS2 / "BIBLIOGRAPHY_CHANGELOG.csv")

    def test_required_pass2a_artifacts_exist_and_are_nonempty(self) -> None:
        required = (
            PASS2 / "PASS2A_LITERATURE_PROTOCOL.md",
            PASS2 / "REFERENCE_GAP_SPECIFICATION.csv",
            PASS2 / "LITERATURE_CLAIM_REGISTRY.csv",
            PASS2 / "EXISTING_REFERENCE_VERIFICATION.csv",
            PASS2 / "CANDIDATE_REFERENCE_REGISTRY.csv",
            PASS2 / "RELATED_WORK_CLAIM_AUDIT.csv",
            PASS2 / "CITATION_CLAIM_MATRIX.csv",
            PASS2 / "BIBLIOGRAPHY_CHANGELOG.csv",
            PASS2 / "NOVELTY_POSITIONING_AUDIT.md",
            MANUSCRIPT,
            BIBLIOGRAPHY,
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

    def test_registry_counts_and_identifiers_are_complete(self) -> None:
        self.assertEqual(len(self.gaps), 10)
        self.assertEqual(len(self.claims), 40)
        self.assertEqual(len(self.existing), 0)
        self.assertEqual(len(self.candidates), 38)
        self.assertEqual(len(self.related), 10)
        self.assertEqual(len(self.changelog), 27)
        checks = (
            (self.gaps, "gap_id"),
            (self.claims, "literature_claim_id"),
            (self.candidates, "candidate_id"),
            (self.related, "audit_id"),
            (self.changelog, "citation_key"),
        )
        for rows, field in checks:
            with self.subTest(field=field):
                values = [row[field] for row in rows]
                self.assertEqual(len(values), len(set(values)))

    def test_selected_sources_cover_every_frozen_gap(self) -> None:
        selected = [row for row in self.candidates if row["decision"] == "SELECT"]
        rejected = [row for row in self.candidates if row["decision"] == "REJECT"]
        self.assertEqual(len(selected), 27)
        self.assertEqual(len(rejected), 11)
        self.assertEqual(
            sum(row["quality"] == "TIER_1_PRIMARY" for row in selected), 23
        )
        self.assertEqual(sum(row["peer_reviewed"] == "YES" for row in selected), 25)
        self.assertFalse(any(row["source_type"] == "PREPRINT" for row in selected))
        covered_gaps = {
            gap_id
            for row in selected
            for gap_id in split_ids(row["gap_id"])
        }
        self.assertEqual(covered_gaps, {row["gap_id"] for row in self.gaps})

    def test_every_manuscript_citation_resolves_without_duplicates(self) -> None:
        cited = set(re.findall(r"@([A-Za-z0-9_:-]+)", self.manuscript))
        bib_keys = set(self.bib_entries)
        self.assertEqual(len(self.bib_entries), 27)
        self.assertEqual(cited, bib_keys)
        self.assertNotIn("[REFERENCE GAP:", self.manuscript)
        self.assertNotIn("DOES_NOT_SUPPORT", self.manuscript)

        doi_values = [
            match.group(1)
            for match in re.finditer(
                r"(?mi)^\s*doi\s*=\s*\{([^}]+)\}", self.bib_text
            )
        ]
        self.assertEqual(len(doi_values), len(set(value.lower() for value in doi_values)))
        self.assertTrue(all(value == value.lower() for value in doi_values))

    def test_bibliography_entries_have_verified_minimum_metadata(self) -> None:
        for key, entry in self.bib_entries.items():
            with self.subTest(citation_key=key):
                for field in ("author", "title", "year"):
                    self.assertRegex(entry, rf"(?mi)^\s*{field}\s*=")
                self.assertRegex(entry, r"(?mi)^\s*(journal|booktitle|url)\s*=")
        self.assertNotRegex(self.bib_text, r"(?i)et\s+al\.\s*[},]")

    def test_bidirectional_matrix_is_total_and_has_no_orphans(self) -> None:
        forward = [row for row in self.matrix if row["mapping_direction"] == "CITATION_TO_CLAIM"]
        reverse = [row for row in self.matrix if row["mapping_direction"] == "CLAIM_TO_CITATION"]
        self.assertEqual(len(forward), 27)
        self.assertEqual(len(reverse), 40)
        self.assertEqual({row["citation_key"] for row in forward}, set(self.bib_entries))
        self.assertEqual(
            {row["literature_claim_id"] for row in reverse},
            {row["literature_claim_id"] for row in self.claims},
        )
        self.assertEqual({row["coverage_status"] for row in reverse}, {"FULL"})

        reverse_keys = {
            key
            for row in reverse
            for key in split_ids(row["citation_keys"])
        }
        self.assertEqual(reverse_keys, set(self.bib_entries))
        self.assertFalse(any(row["support_type"] == "DOES_NOT_SUPPORT" for row in forward))

    def test_claim_registry_resolves_only_to_integrated_keys(self) -> None:
        bib_keys = set(self.bib_entries)
        for claim in self.claims:
            with self.subTest(claim=claim["literature_claim_id"]):
                self.assertEqual(claim["citation_required"], "YES")
                self.assertTrue(claim["verification_status"].startswith("VERIFIED_FULL"))
                self.assertTrue(set(split_ids(claim["current_citation_keys"])).issubset(bib_keys))

    def test_related_work_and_novelty_scope_are_bounded(self) -> None:
        self.assertTrue(all(row["required_action"] == "NARROW" for row in self.related))
        novelty = (PASS2 / "NOVELTY_POSITIONING_AUDIT.md").read_text(encoding="utf-8-sig")
        self.assertEqual(novelty.count("**SUPPORTED_AS_DISTINCT**"), 5)
        self.assertEqual(novelty.count("**NEEDS_NARROWER_WORDING**"), 1)
        for phrase in ("first ever", "first comprehensive", "first framework"):
            self.assertNotIn(phrase, self.manuscript.lower())

    def test_stage29_empirical_sections_are_byte_stable_after_text_decoding(self) -> None:
        empirical = self.manuscript.split(
            "## 4. Validation Framework and Methods", 1
        )[1].split("## References", 1)[0]
        digest = hashlib.sha256(empirical.encode()).hexdigest()
        self.assertEqual(
            digest,
            "ed4d2a278b4d5db7d1dbb9f7de45926cd7f6de9e64a13b0c785522005bd52ffe",
        )

    def test_stage28_remains_the_final_empirical_wall(self) -> None:
        freeze = (
            STAGE29 / "stage29_0_synthesis_lock" / "stage29_freeze_record.json"
        ).read_text(encoding="utf-8-sig")
        self.assertIn('"stage28_final_empirical_stage": true', freeze)
        self.assertIn('"stage29_experimental": false', freeze)
        prohibited = (
            "we fit a new",
            "we trained a new",
            "we recomputed prevalence",
            "we generated bootstrap",
            "new composite score",
        )
        for phrase in prohibited:
            self.assertNotIn(phrase, self.manuscript.lower())


if __name__ == "__main__":
    unittest.main()
