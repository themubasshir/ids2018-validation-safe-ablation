from __future__ import annotations

import ast
import csv
import inspect
import json
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.data.ids2018 import RANDOM_STATE as SPLIT_RANDOM_STATE, TEST_SIZE, VALIDATION_SHARE_OF_TRAINING_POOL, feature_signature, predictor_columns, summarize_split
from ids_validation.evaluation.metrics import calculate_baseline_metrics, calculate_final_test_metrics, calculate_threshold_metrics
from ids_validation.evaluation.thresholds import select_all_model_operating_points, select_winner_operating_points, threshold_grid
from ids_validation.models.tuning import CATBOOST_PARAMETER_SPACE, CNN_CANDIDATES, CV_FOLDS, INTERNAL_VALIDATION_SIZE, LIGHTGBM_PARAMETER_SPACE, MAX_EPOCHS, MLP_CANDIDATES, N_ITERATIONS, PATIENCE, RANDOM_STATE as TUNING_RANDOM_STATE, XGBOOST_PARAMETER_SPACE, build_randomized_search
from ids_validation.models import baselines, neural


def notebook() -> dict:
    return json.loads((ROOT / "notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb").read_text(encoding="utf-8"))


def literal_assignment(physical_cell: int, variable_name: str):
    source = "".join(notebook()["cells"][physical_cell - 1]["source"])
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == variable_name for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{variable_name} not found in cell {physical_cell}")


class Stage01EquivalenceTests(unittest.TestCase):
    def test_feature_order_and_signature_match_frozen_metadata(self) -> None:
        feature_names = json.loads((ROOT / "metadata/feature_names.json").read_text(encoding="utf-8"))
        metadata = json.loads((ROOT / "metadata/split_metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(len(feature_names), 78)
        self.assertEqual(feature_signature(feature_names), metadata["feature_signature_sha256"])
        self.assertEqual(predictor_columns(["a", "Label", "b", "binary_label"]), ["a", "b"])
        self.assertEqual(metadata["scaler_fit_split"], "Training only")
        self.assertEqual((SPLIT_RANDOM_STATE, TEST_SIZE, VALIDATION_SHARE_OF_TRAINING_POOL), (42, 0.20, 0.20))

    def test_frozen_split_memberships_are_disjoint_and_complete(self) -> None:
        with np.load(ROOT / "metadata/split_indices.npz", allow_pickle=False) as split:
            train = split["train_indices"]
            validation = split["validation_indices"]
            test = split["test_indices"]
        self.assertEqual((len(train), len(validation), len(test)), (192593, 48149, 60186))
        merged = np.concatenate([train, validation, test])
        self.assertEqual(len(np.unique(merged)), 300928)
        self.assertEqual((merged.min(), merged.max()), (0, 300927))

    def test_split_summary_formula_matches_frozen_counts(self) -> None:
        row = summarize_split("Fixture", np.array([0, 0, 0, 1, 1], dtype=np.int32))
        self.assertEqual(row["Records"], 5)
        self.assertEqual(row["Benign"], 3)
        self.assertEqual(row["Attack"], 2)
        self.assertEqual(row["Benign Ratio"], 0.6)
        self.assertEqual(row["Attack Ratio"], 0.4)


class Stage02EquivalenceTests(unittest.TestCase):
    def test_frozen_baseline_constructor_inventory(self) -> None:
        configurations = json.loads((ROOT / "metadata/baseline_model_configurations.json").read_text(encoding="utf-8"))
        self.assertEqual([row["Model"] for row in configurations], [
            "Logistic Regression", "Naive Bayes", "KNN", "Linear SVM", "Decision Tree", "Random Forest", "Extra Trees", "AdaBoost", "Gradient Boosting", "XGBoost", "LightGBM", "CatBoost"
        ])
        by_name = {row["Model"]: row for row in configurations}
        self.assertEqual(by_name["Logistic Regression"]["Parameters"]["max_iter"], 1000)
        self.assertEqual(by_name["Linear SVM"]["Parameters"]["max_iter"], 10000)
        self.assertEqual(by_name["Random Forest"]["Parameters"]["n_estimators"], 100)
        self.assertEqual(by_name["XGBoost"]["Parameters"]["max_depth"], 6)
        self.assertEqual(by_name["LightGBM"]["Parameters"]["num_leaves"], 31)
        self.assertEqual(by_name["CatBoost"]["Parameters"]["iterations"], 300)

        extracted_source = inspect.getsource(baselines.build_baseline_models)
        for exact_constructor_fragment in (
            'LogisticRegression(solver="lbfgs", max_iter=1_000',
            'KNeighborsClassifier(n_neighbors=5, weights="uniform", n_jobs=-1)',
            'LinearSVC(C=1.0, max_iter=10_000',
            'RandomForestClassifier(n_estimators=100',
            'XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.3',
            'LGBMClassifier(n_estimators=100, learning_rate=0.1, num_leaves=31',
            'CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1',
        ):
            self.assertIn(exact_constructor_fragment, extracted_source)

    def test_neural_baseline_schedule_matches_frozen_configuration(self) -> None:
        configurations = json.loads((ROOT / "metadata/neural_baseline_configurations.json").read_text(encoding="utf-8"))
        self.assertEqual([row["Model"] for row in configurations], ["MLP", "1D-CNN", "LSTM", "Transformer Encoder"])
        self.assertTrue(all(row["Batch Size"] == 1024 for row in configurations))
        self.assertTrue(all(row["Maximum Epochs"] == 30 for row in configurations))
        self.assertTrue(all(row["Early-Stopping Patience"] == 4 for row in configurations))
        protocol = json.loads((ROOT / "configs/stage02/protocol.json").read_text(encoding="utf-8"))
        self.assertEqual(protocol["methodology"]["neural_internal_early_stopping_fraction"], 0.15)

        mlp_source = inspect.getsource(neural.build_mlp_baseline)
        transformer_source = inspect.getsource(neural.build_transformer_baseline)
        self.assertIn('Dense(256, activation="relu", kernel_initializer="he_normal")', mlp_source)
        self.assertIn('Dense(128, activation="relu", kernel_initializer="he_normal")', mlp_source)
        self.assertIn('name="position_embedding"', transformer_source)
        self.assertIn('num_heads=4, key_dim=16, dropout=0.10', transformer_source)
        self.assertIn('LayerNormalization(epsilon=1e-6)', transformer_source)

    def test_binary_metric_fixture_matches_notebook_formulas(self) -> None:
        metrics = calculate_baseline_metrics(
            np.array([0, 0, 0, 1, 1, 1]),
            np.array([0, 0, 1, 0, 1, 1]),
        )
        self.assertEqual((metrics["TN"], metrics["FP"], metrics["FN"], metrics["TP"]), (2, 1, 1, 2))
        self.assertAlmostEqual(metrics["Accuracy"], 4 / 6)
        self.assertAlmostEqual(metrics["Precision"], 2 / 3)
        self.assertAlmostEqual(metrics["Recall"], 2 / 3)
        self.assertAlmostEqual(metrics["F1-score"], 2 / 3)
        self.assertAlmostEqual(metrics["FPR"], 1 / 3)
        self.assertAlmostEqual(metrics["FNR"], 1 / 3)


class Stage03EquivalenceTests(unittest.TestCase):
    def test_search_control_values_and_scheduling_are_exact(self) -> None:
        self.assertEqual((TUNING_RANDOM_STATE, CV_FOLDS, N_ITERATIONS), (42, 3, 15))
        self.assertEqual((MAX_EPOCHS, PATIENCE, INTERNAL_VALIDATION_SIZE), (50, 5, 0.15))
        source = inspect.getsource(build_randomized_search)
        for fragment in ('shuffle=True', 'scoring="f1"', 'refit=True', 'n_jobs=1', 'return_train_score=False', 'error_score="raise"', 'pre_dispatch=1'):
            self.assertIn(fragment, source)

    def test_search_spaces_are_literal_equal_to_authoritative_cells(self) -> None:
        self.assertEqual(XGBOOST_PARAMETER_SPACE, literal_assignment(96, "parameter_space"))
        self.assertEqual(LIGHTGBM_PARAMETER_SPACE, literal_assignment(97, "parameter_space"))
        self.assertEqual(CATBOOST_PARAMETER_SPACE, literal_assignment(98, "parameter_space"))

    def test_neural_candidate_grids_are_literal_equal_to_authoritative_cells(self) -> None:
        self.assertEqual(MLP_CANDIDATES, literal_assignment(99, "candidates"))
        self.assertEqual(CNN_CANDIDATES, literal_assignment(100, "candidates"))


class Stage04EquivalenceTests(unittest.TestCase):
    def test_threshold_grid_is_exact(self) -> None:
        thresholds = threshold_grid()
        self.assertEqual(len(thresholds), 91)
        np.testing.assert_array_equal(thresholds, np.round(np.arange(0.05, 0.951, 0.01), 2))

    def test_distinct_single_winner_and_all_model_f2_tie_breaks(self) -> None:
        rows = [
            {"Threshold": 0.50, "F1-score": 0.50, "F2-score": 0.50, "Recall": 0.50, "FPR": 0.01},
            {"Threshold": 0.40, "F1-score": 0.80, "F2-score": 0.90, "Recall": 0.70, "FPR": 0.01},
            {"Threshold": 0.60, "F1-score": 0.70, "F2-score": 0.90, "Recall": 0.80, "FPR": 0.01},
        ]
        winner = select_winner_operating_points(rows)
        all_model = select_all_model_operating_points(rows)
        self.assertEqual(winner["Unconstrained Maximum F2"]["Threshold"], 0.40)
        self.assertEqual(all_model["Unconstrained Maximum F2"]["Threshold"], 0.60)
        self.assertEqual(winner["Constrained Maximum F2"]["Threshold"], 0.60)

    def test_frozen_stage04_selections_match_protocol(self) -> None:
        with (ROOT / "results/threshold/final_validation_threshold_selection.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        selected = {row["Operating Point"]: row for row in rows}
        self.assertEqual(selected["Standard"]["Model"], "XGBoost Tuned")
        self.assertEqual(float(selected["Standard"]["Threshold"]), 0.50)
        self.assertEqual(float(selected["Unconstrained Maximum F2"]["Threshold"]), 0.16)
        self.assertEqual(float(selected["Constrained Security Threshold"]["Threshold"]), 0.27)

        with (ROOT / "results/threshold/cross_model_threshold_leaders.csv").open(encoding="utf-8", newline="") as handle:
            leaders = {row["Selection Objective"]: row for row in csv.DictReader(handle)}
        self.assertEqual(leaders["Best Threshold-Optimized F1"]["Model"], "XGBoost Tuned")
        self.assertEqual(float(leaders["Best Threshold-Optimized F1"]["Threshold"]), 0.51)
        self.assertEqual(leaders["Best Constrained F2"]["Model"], "LightGBM Tuned")
        self.assertEqual(float(leaders["Best Constrained F2"]["Threshold"]), 0.26)


class Stage05EquivalenceTests(unittest.TestCase):
    def test_threshold_metric_and_final_test_record_formulas_agree(self) -> None:
        labels = np.array([0, 0, 1, 1])
        probabilities = np.array([0.1, 0.8, 0.2, 0.9])
        validation = calculate_threshold_metrics("Fixture", labels, probabilities, 0.50)
        final = calculate_final_test_metrics("Fixture", labels, probabilities, 0.50, "Standard")
        for key in ("Accuracy", "Precision", "Recall", "F1-score", "F2-score", "FPR", "FNR", "TP", "TN", "FP", "FN"):
            self.assertEqual(validation[key], final[key])
        self.assertEqual(final["Evaluation Split"], "Untouched Test")

    def test_stage05_frozen_choices_are_declared_without_opening_holdout_results(self) -> None:
        protocol = json.loads((ROOT / "configs/stage05/protocol.json").read_text(encoding="utf-8"))
        self.assertEqual(protocol["methodology"]["cell_105"], {"model": "XGBoost Tuned", "standard_threshold": 0.5, "constrained_security_threshold": 0.27, "validation_fpr_constraint": 0.05})
        self.assertEqual(protocol["methodology"]["cell_107"]["balanced_threshold"], 0.51)
        self.assertEqual(protocol["methodology"]["cell_107"]["security_model"], "LightGBM Tuned")
        self.assertEqual(protocol["methodology"]["cell_107"]["security_threshold"], 0.26)
        self.assertIs(protocol["holdout_policy"]["opened_during_extraction"], False)


if __name__ == "__main__":
    unittest.main()
