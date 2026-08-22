from __future__ import annotations

import csv
import hashlib
import json
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.evaluation import bootstrap, calibration, operating_cost
from ids_validation.evaluation.thresholds import select_all_model_operating_points
from ids_validation.explainability import shap_analysis
from ids_validation.stages.stage07 import publication


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def csv_header(relative: str) -> tuple[str, ...]:
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return tuple(next(csv.reader(handle)))


class Stage06EquivalenceTests(unittest.TestCase):
    def test_sample_topk_threshold_and_runtime_provenance(self) -> None:
        protocol = read_json("configs/stage06/protocol.json")
        metadata = read_json("metadata/dual_model_shap_metadata.json")
        method = protocol["methodology"]
        self.assertEqual((method["benign_sample_size"], method["attack_sample_size"], method["total_sample_size"]), (2500, 2500, 5000))
        self.assertEqual((method["top_feature_count"], method["feature_count"], method["random_state"]), (20, 78, 42))
        self.assertEqual((method["balanced_threshold"], method["security_threshold"]), (0.51, 0.26))
        self.assertEqual(metadata["Models"]["Balanced Threshold"], 0.51)
        self.assertEqual(metadata["Models"]["Security Threshold"], 0.26)
        self.assertTrue(all(value == "VERSION_NOT_PROVEN" for value in protocol["environment"]["unproven"].values()))
        self.assertFalse(method["scientific_recomputation_authorized"])

    def test_expected_shap_artifact_schemas_and_sizes(self) -> None:
        for name, expected in shap_analysis.SHAP_ARTIFACT_SCHEMAS.items():
            self.assertEqual(csv_header(f"results/shap/{name}"), expected)
        with (ROOT / "results/shap/shared_shap_sample_manifest.csv").open(encoding="utf-8", newline="") as handle:
            self.assertEqual(sum(1 for _ in csv.reader(handle)) - 1, 5000)
        with (ROOT / "results/shap/xgboost_shap_top20_features.csv").open(encoding="utf-8", newline="") as handle:
            self.assertEqual(sum(1 for _ in csv.reader(handle)) - 1, 20)
        with (ROOT / "results/shap/lightgbm_shap_top20_features.csv").open(encoding="utf-8", newline="") as handle:
            self.assertEqual(sum(1 for _ in csv.reader(handle)) - 1, 20)

    def test_toy_sample_and_representative_attack_logic(self) -> None:
        labels = np.array([0] * 5 + [1] * 5)
        first = shap_analysis.select_shared_sample_indices(labels, benign_sample_size=3, attack_sample_size=2, random_state=42)
        second = shap_analysis.select_shared_sample_indices(labels, benign_sample_size=3, attack_sample_size=2, random_state=42)
        np.testing.assert_array_equal(first, second)
        self.assertEqual((np.sum(labels[first] == 0), np.sum(labels[first] == 1)), (3, 2))
        position = shap_analysis.select_representative_attack(np.array([0, 1, 1]), np.array([0.8, 0.7, 0.9]), 0.75)
        self.assertEqual(position, 2)
        fallback = shap_analysis.select_representative_attack(np.array([0, 1, 1]), np.array([0.8, 0.7, 0.6]), 0.75)
        self.assertEqual(fallback, 1)

    def test_toy_global_importance_rank_and_overlap_logic(self) -> None:
        np.testing.assert_array_equal(shap_analysis.rank_min_descending([3.0, 1.0, 3.0]), np.array([1, 3, 1]))
        records = shap_analysis.build_global_importance_records(
            ["a", "b", "c"],
            np.array([[1.0, -2.0, 0.0], [3.0, 0.0, 0.0]]),
            np.array([[0.0, 1.0, 2.0], [0.0, 3.0, 0.0]]),
        )
        self.assertEqual([row["Feature"] for row in records], ["a", "b", "c"])
        self.assertAlmostEqual(sum(row["XGBoost Normalized Importance"] for row in records), 1.0)
        overlap = shap_analysis.top_feature_overlap(records, top_k=2)
        self.assertEqual(overlap["shared"], {"b"})
        self.assertAlmostEqual(overlap["jaccard"], 1 / 3)


class Stage07EquivalenceTests(unittest.TestCase):
    def test_publication_inventory_matches_frozen_metadata(self) -> None:
        metadata = read_json("metadata/publication_assets_metadata.json")
        expected = publication.expected_publication_artifacts()
        self.assertEqual(len(publication.GENERATED_FIGURES) + len(publication.COPIED_SHAP_FIGURES), metadata["Figures Generated"])
        self.assertEqual(len(publication.CSV_TABLES), metadata["CSV Tables Generated"])
        self.assertEqual(len(publication.LATEX_TABLES), metadata["LaTeX Tables Generated"])
        self.assertEqual(len(expected), 23)
        verification = publication.verify_expected_publication_artifacts(ROOT)
        self.assertTrue(all(row["exists"] for row in verification))

    def test_toy_inventory_is_sorted_and_byte_hashed(self) -> None:
        fixture_root = ROOT / "configs/stage06"
        fixture_bytes = (fixture_root / "protocol.json").read_bytes()
        rows = publication.inventory_files(fixture_root)
        self.assertEqual([row["path"] for row in rows], ["protocol.json"])
        self.assertEqual(rows[0]["size_bytes"], len(fixture_bytes))
        self.assertEqual(rows[0]["sha256"], hashlib.sha256(fixture_bytes).hexdigest())

    def test_destructive_cleanup_is_discovery_only_and_archive_is_archival(self) -> None:
        self.assertEqual(publication.zip_cleanup_candidates(ROOT / "configs/stage07"), ())
        self.assertEqual(publication.complete_archive_command("/kaggle/working", "/tmp/a.tar.gz"), ("tar", "-czf", "/tmp/a.tar.gz", "-C", "/kaggle/working", "."))
        digest = "36cf443c6cd76ca21e63518acb01b626648c1df87beda0e41ea3db87837b7e45"
        self.assertEqual(publication.archive_checksum_line("archive.tar.gz", digest), f"{digest}  archive.tar.gz\n")
        self.assertEqual((ROOT / "metadata/source_archive.sha256").read_text(encoding="utf-8").split()[0], digest)
        self.assertFalse((ROOT / "ids2018_validation_safe_complete_working.tar.gz").exists())


class Stage08EquivalenceTests(unittest.TestCase):
    def test_bootstrap_configuration_and_frozen_environment(self) -> None:
        protocol = read_json("configs/stage08/protocol.json")
        method = protocol["methodology"]
        self.assertEqual((method["bootstrap_replicates"], method["successful_bootstrap_replicates"], method["random_state"]), (2000, 2000, 42))
        self.assertEqual((method["confidence_level"], method["lower_percentile"], method["upper_percentile"]), (0.95, 2.500000000000002, 97.5))
        self.assertEqual(method["thresholds"], {"xgboost_standard": 0.5, "xgboost_balanced": 0.51, "xgboost_security": 0.27, "lightgbm_balanced": 0.5, "lightgbm_security": 0.26})
        self.assertEqual(protocol["environment"]["proven"]["scikit-learn"], "1.6.1")

    def test_frozen_replicate_schema_has_2000_successful_rows(self) -> None:
        with np.load(ROOT / "results/statistical_confidence/bootstrap_replicates.npz", allow_pickle=False) as data:
            self.assertEqual(len(data.files), 71)
            self.assertEqual(data["Replicate_Seed"].shape, (2000,))
            self.assertEqual(data["xgboost_standard__F1-score"].shape, (2000,))
            self.assertEqual(data["lightgbm_security__F2-score"].shape, (2000,))

    def test_toy_paired_stratified_sampling_preserves_counts_and_pairing(self) -> None:
        labels = np.array([0, 0, 0, 1, 1], dtype=np.int8)
        first = bootstrap.paired_stratified_resample_indices(labels, 123)
        second = bootstrap.paired_stratified_resample_indices(labels, 123)
        np.testing.assert_array_equal(first, second)
        self.assertEqual((len(first), np.sum(labels[first] == 0), np.sum(labels[first] == 1)), (5, 3, 2))
        self.assertTrue(np.all(labels[first[:3]] == 0))
        self.assertTrue(np.all(labels[first[3:]] == 1))
        expected_seeds = np.random.SeedSequence(42).generate_state(5, dtype=np.uint64)
        np.testing.assert_array_equal(bootstrap.generate_replicate_seeds(5, 42), expected_seeds)

    def test_toy_percentile_and_paired_difference_semantics(self) -> None:
        values = np.array([1.0, 2.0, 3.0, 4.0])
        summary = bootstrap.summarize_distribution(values, 2.5)
        self.assertAlmostEqual(summary["CI Lower"], np.percentile(values, 2.5))
        self.assertAlmostEqual(summary["CI Upper"], np.percentile(values, 97.5))
        self.assertAlmostEqual(summary["Bootstrap Standard Error"], np.std(values, ddof=1))
        paired = bootstrap.paired_difference_summary([3, 4, 5], [1, 2, 3], 4, 2)
        self.assertEqual(paired["Difference Convention"], "First minus second")
        self.assertEqual(paired["CI Interpretation"], "Entire CI above zero")


class Stage09EquivalenceTests(unittest.TestCase):
    def test_no_recalibration_and_bin_sensitivity_configuration(self) -> None:
        protocol = read_json("configs/stage09/protocol.json")
        method = protocol["methodology"]
        self.assertFalse(method["recalibration_performed"])
        self.assertFalse(method["model_selection_performed"])
        self.assertFalse(method["threshold_selection_performed"])
        self.assertEqual((method["primary_bin_count"], method["bin_sensitivity_counts"]), (15, [10, 15, 20]))
        self.assertEqual(method["bootstrap_replicates"], 2000)
        self.assertEqual(protocol["environment"]["proven"]["scipy"], "1.16.3")

    def test_toy_brier_and_log_loss_formulas(self) -> None:
        labels = np.array([0, 0, 1, 1], dtype=np.int8)
        probabilities = np.array([0.1, 0.4, 0.6, 0.9])
        self.assertAlmostEqual(calibration.calculate_brier_score(labels, probabilities), 0.085)
        expected_log_loss = -np.mean(labels * np.log(probabilities) + (1 - labels) * np.log(1 - probabilities))
        self.assertAlmostEqual(calibration.calculate_log_loss(labels, probabilities), expected_log_loss)

    def test_toy_ece_and_exact_bin_edge_semantics(self) -> None:
        labels = np.array([0, 0, 1, 1], dtype=np.int8)
        probabilities = np.array([0.1, 0.4, 0.6, 0.9])
        records = calibration.calibration_bin_records(labels, probabilities, 2, "uniform")
        summary = calibration.summarize_calibration_records(records)
        self.assertEqual(len(records), 2)
        self.assertAlmostEqual(summary["ECE"], 0.25)
        self.assertAlmostEqual(summary["MCE"], 0.25)
        self.assertAlmostEqual(summary["RMSCE"], 0.25)

        boundary_records = calibration.calibration_bin_records(np.array([0, 1, 0, 1]), np.array([0.0, 0.5, 0.5, 1.0]), 2, "uniform")
        self.assertEqual([row["Count"] for row in boundary_records], [3, 1])
        constant_quantile = calibration.calibration_bin_records(np.array([0, 1, 0]), np.array([0.5, 0.5, 0.5]), 10, "quantile")
        self.assertEqual(len(constant_quantile), 1)

    def test_frozen_calibration_schema_and_replicate_count(self) -> None:
        expected_header = (
            "Model", "Selected Threshold", "Brier Score", "Log Loss", "ECE Uniform 15", "MCE Uniform 15", "RMSCE Uniform 15", "Adaptive ECE Quantile 15", "MCE Quantile 15", "RMSCE Quantile 15", "Calibration Intercept", "Calibration Slope", "Calibration Regression Converged"
        )
        self.assertEqual(csv_header("results/calibration/calibration_metric_point_estimates.csv"), expected_header)
        with np.load(ROOT / "results/calibration/calibration_bootstrap_replicates.npz", allow_pickle=False) as data:
            self.assertEqual(len(data.files), 17)
            self.assertEqual(data["Replicate_Seed"].shape, (2000,))
            self.assertEqual(data["xgboost__ECE_Uniform_15"].shape, (2000,))


class Stage10EquivalenceTests(unittest.TestCase):
    def test_cost_ratio_threshold_grid_and_stage25_exclusion(self) -> None:
        protocol = read_json("configs/stage10/protocol.json")
        method = protocol["methodology"]
        self.assertEqual(method["fn_to_fp_cost_ratios"], [1, 2, 5, 10, 20, 50, 100])
        self.assertEqual(method["threshold_grid"], {"minimum": 0.05, "maximum": 0.95, "step": 0.01, "count": 91, "source": "frozen Stage 4 all-model validation sweep"})
        self.assertEqual(len(operating_cost.THRESHOLD_GRID), 91)
        self.assertFalse(method["stage25_semantics_imported"])
        self.assertTrue(all(value == "VERSION_NOT_PROVEN" for value in protocol["environment"]["unproven"].values()))

    def test_toy_cost_formula_and_exact_tie_break(self) -> None:
        self.assertEqual(operating_cost.operational_cost(fp=4, fn=3, fn_to_fp_ratio=2), 10.0)
        rows = [
            {"Threshold": 0.20, "FP": 2, "FN": 4, "F2-score": 0.99, "FPR": 0.01},
            {"Threshold": 0.40, "FP": 4, "FN": 3, "F2-score": 0.90, "FPR": 0.02},
            {"Threshold": 0.60, "FP": 4, "FN": 3, "F2-score": 0.90, "FPR": 0.03},
        ]
        selected = operating_cost.select_validation_cost_threshold(rows, 2)
        self.assertEqual(selected["Threshold"], 0.60)

    def test_stage10_cost_search_is_unconstrained_but_stage4_security_is_constrained(self) -> None:
        cost_rows = [
            {"Threshold": 0.50, "FP": 4, "FN": 4, "F2-score": 0.5, "FPR": 0.04},
            {"Threshold": 0.40, "FP": 1, "FN": 1, "F2-score": 0.9, "FPR": 0.40},
        ]
        self.assertEqual(operating_cost.select_validation_cost_threshold(cost_rows, 1)["Threshold"], 0.40)

        stage4_rows = [
            {"Threshold": 0.50, "F1-score": 0.5, "F2-score": 0.5, "Recall": 0.5, "FPR": 0.04},
            {"Threshold": 0.40, "F1-score": 0.9, "F2-score": 0.9, "Recall": 0.9, "FPR": 0.40},
        ]
        constrained = select_all_model_operating_points(stage4_rows, fpr_limit=0.05)
        self.assertEqual(constrained["Constrained Maximum F2"]["Threshold"], 0.50)

    def test_toy_break_even_and_pareto_formulas(self) -> None:
        self.assertAlmostEqual(operating_cost.break_even_cost_ratio(20, 5, 10, 10), 2.0)
        self.assertTrue(np.isnan(operating_cost.break_even_cost_ratio(20, 10, 10, 10)))
        rows = [
            {"Threshold": 0.9, "FP": 1, "FN": 9},
            {"Threshold": 0.8, "FP": 2, "FN": 7},
            {"Threshold": 0.7, "FP": 3, "FN": 8},
            {"Threshold": 0.6, "FP": 4, "FN": 5},
        ]
        frontier = operating_cost.pareto_frontier(rows)
        self.assertEqual([row["Threshold"] for row in frontier], [0.9, 0.8, 0.6])

    def test_frozen_validation_cost_table_matches_config_and_formula(self) -> None:
        protocol = read_json("configs/stage10/protocol.json")
        expected = protocol["methodology"]["validation_selected_thresholds"]
        with (ROOT / "results/operational_cost/validation_cost_ratio_threshold_selection.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 14)
        for row in rows:
            ratio_key = str(int(float(row["FN to FP Cost Ratio"])))
            self.assertEqual(float(row["Selected Threshold"]), expected[row["Model"]][ratio_key])
            calculated = operating_cost.operational_cost(int(row["Validation FP"]), int(row["Validation FN"]), float(row["FN Unit Cost"]), float(row["FP Unit Cost"]))
            self.assertEqual(calculated, float(row["Validation Operational Cost"]))


if __name__ == "__main__":
    unittest.main()
