from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.protocol_cli import load_protocol, verify_only_report
from ids_validation.stages.stage22 import registry as stage22
from ids_validation.stages.stage23 import registry as stage23
from ids_validation.stages.stage24 import registry as stage24


ARCHIVE_IDENTITIES = {
    "stage21_stage22_research_continues.ipynb": (
        "dab6efa73600d36b1a6324ffa4036d6b02453b3b6c4ea84f995875d74a35a5db",
        139,
        138,
    ),
    "stage23_research_executed.ipynb": (
        "a33b83e09261aed6f7b772049bcfb7f4691e63e0cf2e13202c4cd00afeae007e",
        78,
        77,
    ),
    "stage24_cross_dataset_executed.ipynb": (
        "395465a0b72d718c997583ac3838fe12731d990799cadb134c20a548e669b8ac",
        62,
        45,
    ),
}


def notebook(name: str) -> dict:
    path = ROOT / "notebooks" / "archive" / name
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_source(cell: dict) -> str:
    return "".join(cell.get("source", [])).replace("\r\n", "\n").strip()


class LaterArchiveEquivalenceTests(unittest.TestCase):
    def test_three_archive_identities_cell_counts_and_output_counts(self) -> None:
        for name, (expected_hash, expected_cells, expected_outputs) in ARCHIVE_IDENTITIES.items():
            with self.subTest(notebook=name):
                path = ROOT / "notebooks" / "archive" / name
                document = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_hash)
                self.assertEqual(len(document["cells"]), expected_cells)
                self.assertEqual(sum(bool(cell.get("outputs")) for cell in document["cells"]), expected_outputs)
                self.assertTrue(all(cell.get("cell_type") == "code" for cell in document["cells"]))

    def test_stage21_workers_are_exactly_embedded_in_historical_cells(self) -> None:
        document = notebook("stage21_stage22_research_continues.ipynb")
        pairs = {
            49: "results/stage21_architecture/stage21_2_train_fast_executed.py",
            51: "results/stage21_architecture/stage21_3_thursday_eval_executed.py",
            66: "results/stage21_architecture/stage21_4_friday_eval_executed.py",
            82: "scripts/stage21_generate_publication_figures.py",
        }
        for physical_cell, relative_path in pairs.items():
            worker = (ROOT / relative_path).read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            self.assertIn(worker, normalized_source(document["cells"][physical_cell - 1]))

    def test_stage23_script_preserves_75_cells_with_documented_hoisting_only(self) -> None:
        document = notebook("stage23_research_executed.ipynb")
        script = (ROOT / "scripts/stage23_shortcut_feature_audit_kaggle.py").read_text(encoding="utf-8")
        matches = list(
            re.finditer(r"^# %% \[notebook cell (\d+);[^\n]*\]\n", script, re.MULTILINE)
        )
        exported = {
            int(match.group(1)): script[
                match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(script)
            ].strip()
            for index, match in enumerate(matches)
        }
        self.assertEqual(tuple(exported), tuple(range(1, 76)))
        nonexact = []
        for physical_cell in range(1, 76):
            if exported[physical_cell] != normalized_source(document["cells"][physical_cell - 1]):
                nonexact.append(physical_cell)
        self.assertEqual(nonexact, [68, 71, 73])
        for physical_cell in nonexact:
            notebook_lines = normalized_source(document["cells"][physical_cell - 1]).splitlines()
            script_lines = exported[physical_cell].splitlines()
            differing = [pair for pair in zip(notebook_lines, script_lines) if pair[0] != pair[1]]
            self.assertEqual(len(differing), 1)
            self.assertEqual(differing[0][0], "from __future__ import annotations")
            self.assertIn("hoisted to file header", differing[0][1])

    def test_stage24_sanitized_code_maps_exactly_to_full_cells_18_to_60(self) -> None:
        full = notebook("stage24_cross_dataset_executed.ipynb")
        sanitized = json.loads(
            (ROOT / "scripts/stage24/stage24_cross_dataset_generalization.ipynb").read_text(
                encoding="utf-8"
            )
        )
        full_by_source: dict[str, list[int]] = defaultdict(list)
        for physical_cell, cell in enumerate(full["cells"], start=1):
            full_by_source[normalized_source(cell)].append(physical_cell)
        mappings = []
        for repository_cell, cell in enumerate(sanitized["cells"], start=1):
            if cell.get("cell_type") == "code":
                mappings.append((repository_cell, tuple(full_by_source[normalized_source(cell)])))
        self.assertEqual(len(mappings), 44)
        self.assertTrue(all(source_cells for _, source_cells in mappings))
        self.assertEqual(mappings[0], (2, (18,)))
        self.assertEqual(mappings[-1], (45, (60,)))
        source_counts = Counter(source_cells for _, source_cells in mappings)
        self.assertEqual([item for item, count in source_counts.items() if count == 2], [(40,)])
        self.assertEqual({item[0] for item in source_counts}, set(range(18, 61)))


class Stage21EquivalenceTests(unittest.TestCase):
    def test_masked_vit_geometry_training_and_locked_reuse_contract(self) -> None:
        method = load_protocol(21)["methodology"]
        self.assertEqual(method["representation"]["shape"], [64, 256, 1])
        self.assertEqual(method["model"]["trainable_parameters"], 91_969)
        self.assertEqual(method["model"]["patch_tokens"], 128)
        self.assertEqual(method["training"]["epochs"], 10)
        self.assertEqual(method["training"]["seed"], 42)
        self.assertEqual(method["validation"]["flows"], 8_197)
        self.assertEqual(method["validation"]["balanced_threshold"], 0.42)
        self.assertEqual(method["validation"]["security_threshold"], 0.24)
        self.assertEqual(method["friday"]["flows"], 12_088)
        self.assertIs(method["friday"]["threshold_reselection"], False)

    def test_comparison_and_scientific_authorization_are_frozen(self) -> None:
        method = load_protocol(21)["methodology"]
        self.assertEqual(method["comparison"]["paired_bootstrap_replicates"], 10_000)
        self.assertEqual(method["comparison"]["seed"], 21_042)
        self.assertIs(method["comparison"]["confirmatory"], False)
        for key in (
            "scientific_execution_authorized",
            "training_authorized",
            "inference_authorized",
            "threshold_selection_authorized",
            "bootstrap_generation_authorized",
            "integrated_gradients_authorized",
        ):
            self.assertIs(method[key], False)


class Stage22EquivalenceTests(unittest.TestCase):
    def test_membership_and_threshold_contracts_match_frozen_values(self) -> None:
        method = load_protocol(22)["methodology"]
        cells = {
            name: {
                role: {"rows": values[0], "attack": values[1], "benign": values[2]}
                for role, values in roles.items()
            }
            for name, roles in method["memberships"].items()
        }
        self.assertTrue(stage22.membership_counts_are_frozen(cells))
        self.assertEqual(stage22.development_threshold_grid_integer_percent(), tuple(range(5, 96)))
        self.assertEqual(
            {name: {key: row[key] for key in ("standard", "balanced", "security")}
             for name, row in method["validation"]["thresholds"].items()},
            stage22.VALIDATION_THRESHOLDS,
        )

    def test_single_final_opening_and_four_results_are_frozen(self) -> None:
        final = load_protocol(22)["methodology"]["forward_final_holdout"]
        self.assertEqual((final["rows"], final["attack"], final["benign"]), (1_374_133, 375_345, 998_788))
        self.assertAlmostEqual(stage22.chance_pr_auc(final["attack"], final["rows"]), final["attack_prevalence"])
        self.assertTrue(
            stage22.final_opening_is_permanently_closed(
                {
                    "maximum_authorized": 1,
                    "consumed": 1,
                    "permanently_closed": True,
                    "post_holdout_model_change": False,
                    "post_holdout_threshold_change": False,
                    "post_holdout_calibration": False,
                }
            )
        )
        self.assertAlmostEqual(final["results"]["CHRONOLOGICAL_REBALANCED"]["pr_auc"], 0.6926302657182113)
        self.assertAlmostEqual(final["results"]["CHRONOLOGICAL_REBALANCED"]["roc_auc"], 0.8321639645817649)


class Stage23EquivalenceTests(unittest.TestCase):
    def test_primary_subsets_and_no_ports_boundary_are_exact(self) -> None:
        subsets = load_protocol(23)["methodology"]["primary_subsets"]
        self.assertTrue(stage23.primary_subset_contract_is_frozen(subsets))
        self.assertTrue(
            stage23.no_ports_claim_is_accurate(
                ["Dst Port", "Protocol", "Flow Duration"], subsets["NO_PORTS"]["removed"]
            )
        )
        self.assertIs(subsets["NO_PORTS"]["src_port_removed"], False)

    def test_fit_budget_shap_and_uncertainty_are_closed(self) -> None:
        method = load_protocol(23)["methodology"]
        budget = method["fit_budget"]
        self.assertTrue(stage23.fit_budget_is_closed(budget))
        self.assertEqual(budget["consumed"], 50)
        self.assertEqual(budget["additional_fits_authorized"], 0)
        self.assertTrue(stage23.shap_reporting_label_is_safe(True, "DESCRIPTIVE_ONLY"))
        self.assertIs(method["shap"]["exact_shap_for_probability_averaged_ensemble"], False)
        self.assertEqual(method["uncertainty"]["cohort_rows_per_split"], 50_000)
        self.assertEqual(method["uncertainty"]["replicates"], 1_000)
        self.assertIs(method["uncertainty"]["regeneration_authorized"], False)

    def test_final_synthesis_counts_and_closure_are_frozen(self) -> None:
        method = load_protocol(23)["methodology"]
        synthesis = method["final_synthesis"]
        self.assertEqual((synthesis["primary_figure_pairs"], synthesis["supplementary_figure_pairs"]), (4, 2))
        self.assertEqual(synthesis["publication_and_supplementary_tables"], 10)
        self.assertEqual(synthesis["status"], "FINAL_PROTOCOL_CLOSURE_SEALED")
        self.assertIs(method["model_fitting_authorized"], False)
        self.assertIs(method["bootstrap_generation_authorized"], False)
        self.assertIs(method["shap_generation_authorized"], False)


class Stage24EquivalenceTests(unittest.TestCase):
    def test_semantic_bridge_contract_is_static_and_unmodified(self) -> None:
        bridges = load_protocol(24)["methodology"]["semantic_bridges"]
        self.assertTrue(stage24.bridge62_exclusion_is_frozen(bridges["bridge62"]["excluded_aggregate_flag_features"]))
        self.assertTrue(
            stage24.feature_bridge_counts_are_frozen(
                {
                    "bridge62": bridges["bridge62"]["feature_count"],
                    "bridge70": bridges["bridge70"]["feature_count"],
                    "mapping_search_performed": bridges["mapping_search_performed"],
                    "fuzzy_mapping": bridges["fuzzy_mapping"],
                }
            )
        )
        self.assertIs(bridges["modification_authorized"], False)
        self.assertIs(bridges["target_labels_used_to_build_mapping"], False)

    def test_fit_and_opening_ledgers_are_terminal(self) -> None:
        method = load_protocol(24)["methodology"]
        fit = method["fit_budget"]
        self.assertEqual((fit["total"], fit["consumed"], fit["additional_fits_authorized"]), (4, 4, 0))
        ledger = method["opening_ledger"]
        self.assertTrue(
            stage24.opening_ledger_is_closed(
                {
                    "evaluable_budget": ledger["evaluable_budget"],
                    "evaluable_consumed": ledger["evaluable_consumed"],
                    "administratively_cancelled": ledger["grounded_s4_administratively_cancelled_before_opening"],
                    "cancelled_slots_reallocated": ledger["cancelled_slots_reallocated"],
                    "remaining": ledger["remaining_evaluable_openings"],
                }
            )
        )
        self.assertEqual(method["grounded_s4"]["status"], "NOT_EVALUABLE")
        self.assertIs(method["grounded_s4"]["fuzzy_substitute_used"], False)

    def test_bidirectional_metrics_and_separate_reporting_are_exact(self) -> None:
        method = load_protocol(24)["methodology"]
        primary = method["primary_direction"]
        secondary = method["secondary_direction"]
        self.assertEqual((primary["target"]["rows"], primary["target"]["attack"]), (2_830_743, 557_646))
        self.assertAlmostEqual(primary["results"]["bridge70_flag_corrected"]["pr_auc"], 0.6562523506197266)
        self.assertAlmostEqual(primary["results"]["bridge70_flag_corrected"]["roc_auc"], 0.7440833611037603)
        self.assertEqual((secondary["target"]["rows"], secondary["target"]["attack"]), (593_780, 62_256))
        self.assertAlmostEqual(secondary["results"]["bridge62"]["pr_auc"], 0.10817592573968819)
        self.assertAlmostEqual(secondary["results"]["bridge70"]["roc_auc"], 0.5253021473786115)
        self.assertTrue(
            stage24.transfer_directions_remain_separate(
                [primary["direction"], secondary["direction"]], method["reporting"]["directions_averaged"]
            )
        )


class FrozenArtifactVerificationTests(unittest.TestCase):
    EXPECTED_HASH_COUNTS = {21: 7, 22: 13, 23: 11, 24: 13}

    def test_all_declared_stage21_to_stage24_hashes_match_without_deserialization(self) -> None:
        for stage, expected_count in self.EXPECTED_HASH_COUNTS.items():
            with self.subTest(stage=stage):
                report = verify_only_report(load_protocol(stage))
                self.assertEqual(len(report["hashes"]), expected_count)
                self.assertTrue(all(row["status"] == "MATCH" for row in report["hashes"]))
                self.assertTrue(all(row["artifact_deserialized"] is False for row in report["hashes"]))
                self.assertIs(report["scientific_execution_performed"], False)
                self.assertIs(report["scientific_files_opened"], False)
                self.assertIs(report["would_touch_frozen_target"], False)


if __name__ == "__main__":
    unittest.main()
