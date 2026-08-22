from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.protocol_cli import load_protocol, verify_only_report
from ids_validation.data import duplicate_safe_split
from ids_validation.evaluation import attack_categories, multiseed
from ids_validation.explainability import integrated_gradients, lime_analysis, local_agreement
from ids_validation.models import ft_transformer


def read_csv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(relative_path: str) -> dict[str, object]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class Stage11EquivalenceTests(unittest.TestCase):
    def test_taxonomy_support_and_low_support_are_exact(self) -> None:
        protocol = load_protocol(11)["methodology"]
        self.assertEqual(tuple(protocol["attack_categories"]), attack_categories.ATTACK_CATEGORIES)
        self.assertEqual(protocol["support_counts"], attack_categories.FROZEN_SUPPORT_COUNTS)
        self.assertEqual(sum(attack_categories.FROZEN_SUPPORT_COUNTS.values()), 24_186)
        self.assertEqual(protocol["low_support_categories"], ["SQL Injection"])
        self.assertEqual(attack_categories.support_status(13), "LOW_SUPPORT")
        self.assertEqual(attack_categories.support_status(20), "RANKING_ELIGIBLE")

    def test_frozen_support_table_matches_registry_and_schema(self) -> None:
        rows = read_csv("results/attack_category/attack_category_support_summary.csv")
        self.assertEqual(list(rows[0]), ["Attack Category", "Support", "Share of Holdout Attacks"])
        self.assertEqual(len(rows), 12)
        self.assertEqual({row["Attack Category"]: int(row["Support"]) for row in rows}, attack_categories.FROZEN_SUPPORT_COUNTS)

    def test_toy_label_reconstruction_and_grouping(self) -> None:
        labels = [" Benign ", "Bot", "Bot", "SQL   Injection"]
        targets = attack_categories.reconstruct_binary_labels(labels)
        np.testing.assert_array_equal(targets, [0, 1, 1, 1])
        rows = attack_categories.category_support(labels, targets)
        self.assertEqual(rows[0], {"Attack Category": "Bot", "Support": 2, "Support Status": "LOW_SUPPORT"})
        self.assertEqual(rows[1]["Attack Category"], "SQL Injection")

    def test_toy_wilson_bootstrap_and_fdr_formulas(self) -> None:
        low, high = attack_categories.wilson_interval(5, 10)
        self.assertAlmostEqual(low + high, 1.0)
        self.assertLess(low, 0.5)
        first = attack_categories.paired_bootstrap_detection_difference([1, 1, 0, 1], [1, 0, 0, 0], 42, replicates=50)
        second = attack_categories.paired_bootstrap_detection_difference([1, 1, 0, 1], [1, 0, 0, 0], 42, replicates=50)
        self.assertEqual(first, second)
        np.testing.assert_allclose(attack_categories.benjamini_hochberg([0.01, 0.02, 0.2]), [0.03, 0.03, 0.2])


class Stage12EquivalenceTests(unittest.TestCase):
    def test_seed_fixed_hpo_split_and_threshold_registry(self) -> None:
        methodology = load_protocol(12)["methodology"]
        self.assertEqual(tuple(methodology["seeds"]), multiseed.SEEDS)
        self.assertIs(methodology["hyperparameter_search_repeated"], False)
        self.assertIn("not full pipeline or HPO uncertainty", methodology["uncertainty_scope"])
        grid = multiseed.threshold_grid()
        self.assertEqual(len(grid), 91)
        self.assertEqual((grid[0], grid[-1]), (0.05, 0.95))

    def test_repeated_split_helper_and_frozen_sizes_are_declared(self) -> None:
        self.assertEqual(multiseed.EXPECTED_SPLIT_SIZES, {"train": 192_593, "validation": 48_149, "test": 60_186})
        source = multiseed.repeated_stratified_split_indices.__doc__
        self.assertIn("two train_test_split calls", source)
        self.assertIn("never invoked by a stage entry point", source)

    def test_toy_threshold_metrics_and_tie_chains(self) -> None:
        metrics = multiseed.calculate_threshold_metrics([0, 0, 1, 1], [0.1, 0.6, 0.4, 0.9], 0.5)
        self.assertEqual((metrics["TP"], metrics["TN"], metrics["FP"], metrics["FN"]), (1, 1, 1, 1))
        self.assertEqual(metrics["F1-score"], 0.5)
        rows = [
            {"Threshold": 0.4, "F1-score": 0.8, "F2-score": 0.7, "Recall": 0.8, "Precision": 0.8, "FPR": 0.04},
            {"Threshold": 0.6, "F1-score": 0.8, "F2-score": 0.7, "Recall": 0.8, "Precision": 0.8, "FPR": 0.04},
        ]
        self.assertEqual(multiseed.select_balanced_point(rows)["Threshold"], 0.6)
        self.assertEqual(multiseed.select_security_point(rows)["Threshold"], 0.6)

    def test_toy_aggregation_and_paired_difference_formulas(self) -> None:
        aggregate = multiseed.aggregate_values([1.0, 2.0, 3.0])
        self.assertEqual(aggregate["mean"], 2.0)
        self.assertEqual(aggregate["std"], 1.0)
        self.assertEqual(aggregate["median"], 2.0)
        np.testing.assert_array_equal(multiseed.paired_model_differences([3, 4], [1, 1]), [2, 3])

    def test_frozen_split_summary_has_all_five_exact_sizes(self) -> None:
        rows = read_csv("results/multiseed/multiseed_split_summary.csv")
        self.assertEqual([int(row["Seed"]) for row in rows], list(multiseed.SEEDS))
        for row in rows:
            self.assertEqual((int(row["Training Records"]), int(row["Validation Records"]), int(row["Test Records"])), (192_593, 48_149, 60_186))


class Stage13EquivalenceTests(unittest.TestCase):
    def test_lime_configuration_and_perturbation_seeds_are_exact(self) -> None:
        methodology = load_protocol(13)["methodology"]
        self.assertEqual(methodology["background"]["size"], lime_analysis.BACKGROUND_SIZE)
        self.assertEqual(methodology["initial_lime"]["samples"], lime_analysis.INITIAL_NUM_SAMPLES)
        self.assertEqual(methodology["initial_lime"]["features"], lime_analysis.NUM_FEATURES)
        self.assertEqual(tuple(methodology["perturbation_base_seeds"]), lime_analysis.PERTURBATION_BASE_SEEDS)
        self.assertIs(methodology["lime_execution_authorized"], False)
        self.assertIs(methodology["shap_execution_authorized"], False)

    def test_toy_fidelity_and_seed_formulas(self) -> None:
        self.assertEqual(lime_analysis.explanation_seed(130_500, 7), 130_507)
        result = lime_analysis.fidelity_metrics(0.7, 1.2, 0.5)
        self.assertEqual(result["local_prediction_clipped"], 1.0)
        self.assertAlmostEqual(result["fidelity_gap"], 0.5)
        self.assertIs(result["decision_agreement"], True)

    def test_toy_local_agreement_and_reliability_formulas(self) -> None:
        np.testing.assert_array_equal(local_agreement.deterministic_top_indices([1, -3, 3, 0], 2), [1, 2])
        self.assertAlmostEqual(local_agreement.jaccard_similarity([1, 2], [2, 3]), 1 / 3)
        self.assertAlmostEqual(local_agreement.cosine_similarity([1, 0], [1, 0]), 1.0)
        self.assertTrue(math.isnan(local_agreement.cosine_similarity([0, 0], [1, 0])))
        self.assertEqual(local_agreement.classify_stability(0.75, 0.8), "High")
        self.assertEqual(local_agreement.classify_reliability(True, 0.3, 0.1, 0.4, 0.5), "Qualified supplementary explanation")

    def test_frozen_full_panel_schema_and_provenance(self) -> None:
        rows = read_csv("results/lime/lime_full_panel_summary.csv")
        self.assertEqual(len(rows), 64)
        self.assertIn("fidelity_gap", rows[0])
        self.assertIn("top10_jaccard", rows[0])
        self.assertIn("reliability_label", rows[0])
        metadata = read_json("metadata/lime/stage13_7b_full_panel_metadata.json")
        self.assertEqual(metadata["cases"], 64)


class Stage14EquivalenceTests(unittest.TestCase):
    def test_scaler_ig_and_outcome_configuration_is_static(self) -> None:
        methodology = load_protocol(14)["methodology"]
        self.assertEqual(methodology["scaler"]["fit_records"], 192_593)
        self.assertEqual(methodology["outcome_panel"]["total_cases"], 64)
        self.assertEqual(tuple(methodology["audited_step_counts"]), integrated_gradients.AUDITED_STEP_COUNTS)
        self.assertEqual(methodology["selected_integration_steps"], 128)
        self.assertIs(methodology["neural_model_loading_authorized"], False)
        self.assertIs(methodology["ig_execution_authorized"], False)

    def test_toy_input_shape_and_probability_normalization(self) -> None:
        self.assertEqual(integrated_gradients.determine_input_mode((None, 78)), "flat_2d")
        self.assertEqual(integrated_gradients.determine_input_mode((None, 78, 1)), "sequence_3d_last_channel")
        matrix = np.zeros((2, 78))
        self.assertEqual(integrated_gradients.prepare_input_for_model(matrix, "sequence_3d_first_channel").shape, (2, 1, 78))
        np.testing.assert_array_equal(integrated_gradients.normalize_binary_attack_probability([[0.8, 0.2], [0.1, 0.9]]), [0.2, 0.9])

    def test_toy_trapezoidal_ig_and_completeness_formulas(self) -> None:
        gradients = np.ones((2, 129, 3), dtype=np.float64)
        differences = np.asarray([[1, 2, 3], [3, 4, 5]], dtype=np.float64)
        attribution, per_reference = integrated_gradients.integrate_gradient_grid(gradients, differences, 16)
        np.testing.assert_allclose(attribution, [2, 3, 4])
        np.testing.assert_allclose(per_reference, differences)
        diagnostics = integrated_gradients.completeness_diagnostics(attribution, 9.0, 0.0)
        self.assertEqual(diagnostics["absolute_error"], 0.0)
        self.assertIs(diagnostics["completeness_pass"], True)

    def test_toy_reference_and_baseline_reliability_formulas(self) -> None:
        self.assertEqual(integrated_gradients.cosine_similarity([0, 0], [0, 0]), 1.0)
        self.assertEqual(integrated_gradients.jaccard_similarity([], []), 1.0)
        self.assertEqual(integrated_gradients.classify_reference_reliability(True, 0.65, 0.0, 0.4, 0.7), "Reference-robust")
        self.assertEqual(integrated_gradients.classify_feature_reference_stability(0.75), "Reference-stable direction")
        self.assertEqual(integrated_gradients.classify_baseline_agreement(0.8, 0.5, 0.8), "Strong baseline agreement")

    def test_frozen_completeness_schema_and_neural_metadata(self) -> None:
        rows = read_csv("results/stage14_integrated_gradients/stage14_3b_ig_completeness_audit.csv")
        self.assertEqual(len(rows), 288)
        self.assertIn("normalized_completeness_error", rows[0])
        metadata = read_json("results/stage14_integrated_gradients/stage14_2_selected_preprocessing.json")
        self.assertEqual(metadata["selected_scaler_n_samples_seen"], 192_593)


class Stage15EquivalenceTests(unittest.TestCase):
    def test_feature_seed_threshold_and_cell_boundaries_are_exact(self) -> None:
        protocol = load_protocol(15)
        methodology = protocol["methodology"]
        self.assertEqual(tuple(methodology["features"]["removed_constants"]), duplicate_safe_split.CONSTANT_FEATURES)
        self.assertEqual(tuple(methodology["features"]["retained_ordered"]), duplicate_safe_split.RETAINED_FEATURES)
        self.assertEqual(len(duplicate_safe_split.RETAINED_FEATURES), 70)
        self.assertEqual(tuple(methodology["frozen_model"]["seeds"]), ft_transformer.CONFIRMATION_SEEDS)
        self.assertEqual(methodology["threshold"]["frozen"], ft_transformer.FROZEN_THRESHOLD)
        self.assertNotIn(171, protocol["source"]["physical_cells_1_based"])

    def test_toy_duplicate_safe_priority_and_conflict_policy(self) -> None:
        hashes = np.asarray([10, 20, 20, 30, 40, 10, 50, 50, 60], dtype=np.uint64)
        labels = np.asarray([0, 1, 1, 0, 1, 0, 0, 1, 1], dtype=np.int8)
        original = {"train": [0, 1, 2], "validation": [3, 4, 5], "holdout": [6, 7, 8]}
        safe = duplicate_safe_split.construct_duplicate_safe_indices(hashes, labels, original)
        np.testing.assert_array_equal(safe["train"], [0, 1])
        np.testing.assert_array_equal(safe["validation"], [3, 4])
        np.testing.assert_array_equal(safe["holdout"], [8])
        self.assertIs(duplicate_safe_split.verify_duplicate_safe_invariants(safe, hashes), True)

    def test_frozen_architecture_metadata_and_parameter_formula(self) -> None:
        frozen = read_json("results/stage15_transformer_checkpoint/stage15_4c_frozen_architecture.json")
        self.assertEqual(frozen["candidate_id"], ft_transformer.FROZEN_CANDIDATE_ID)
        self.assertEqual(frozen["five_seed_summary"]["parameter_count"], 159_169)
        self.assertEqual(ft_transformer.expected_parameter_count(), ft_transformer.EXPECTED_PARAMETER_COUNT)
        self.assertEqual(ft_transformer.FROZEN_CONFIGURATION.batch_size, 1024)
        self.assertEqual(ft_transformer.FROZEN_CONFIGURATION.maximum_epochs, 70)

    def test_checkpoint_sizes_and_hashes_match_preholdout_lock(self) -> None:
        protocol = load_protocol(15)
        for relative, expected in protocol["hash_verification_artifacts"].items():
            path = ROOT / relative
            self.assertEqual(path.stat().st_size, expected["size_bytes"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected["sha256"])

    def test_duplicate_split_and_isolated_environment_receipts(self) -> None:
        split = read_json("results/stage15_transformer_checkpoint/stage15_1_duplicate_safe_split_metadata.json")
        self.assertEqual(split["duplicate_safe_split_sizes"], {"train": 154_686, "validation": 37_835, "holdout": 46_849})
        self.assertEqual(split["cross_split_exact_overlap_after_processing"], 0)
        environment = read_json("results/stage15_transformer_checkpoint/stage15_2g_isolated_environment.json")
        verification = environment["verification"]
        self.assertEqual(verification["torch_version"], "2.7.1+cu118")
        self.assertEqual(verification["device_name"], "Tesla P100-PCIE-16GB")
        self.assertIs(verification["required_architecture_present"], True)

    def test_preholdout_and_one_time_holdout_receipts_are_immutable_provenance(self) -> None:
        lock = read_json("results/stage15_transformer_checkpoint/stage15_5b_preholdout_decision_lock.json")
        execution = read_json("results/stage15_transformer_checkpoint/stage15_6a_holdout_execution_state.json")
        completion = read_json("results/stage15_transformer_checkpoint/stage15_6b_transformer_experiment_completion.json")
        self.assertIs(lock["holdout_opened"], False)
        self.assertEqual(lock["holdout_evaluation_count"], 0)
        self.assertIs(execution["holdout_opened"], True)
        self.assertEqual(execution["holdout_evaluation_count"], 1)
        self.assertEqual(completion["holdout_status"], "EVALUATED_ONCE")
        self.assertIs(completion["scientific_boundaries"]["threshold_changed_after_holdout"], False)
        report = verify_only_report(load_protocol(15))
        self.assertTrue(all(row["status"] == "MATCH" for row in report["hashes"]))
        self.assertTrue(all(row["artifact_deserialized"] is False for row in report["hashes"]))


if __name__ == "__main__":
    unittest.main()
