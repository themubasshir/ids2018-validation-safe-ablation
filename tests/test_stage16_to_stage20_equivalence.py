from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.protocol_cli import load_protocol, verify_only_report
from ids_validation.evaluation import attention
from ids_validation.models import classical


def read_csv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(relative_path: str) -> dict[str, object]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


class Stage16EquivalenceTests(unittest.TestCase):
    def test_candidate_seed_and_threshold_registries_are_exact(self) -> None:
        methodology = load_protocol(16)["methodology"]
        self.assertEqual(tuple(methodology["baseline"]["candidate_ids"]), classical.BASELINE_CANDIDATES)
        self.assertEqual(tuple(methodology["confirmation"]["seeds"]), classical.CONFIRMATION_SEEDS)
        self.assertEqual(len(classical.threshold_grid()), 181)
        self.assertEqual((classical.threshold_grid()[0], classical.threshold_grid()[-1]), (0.05, 0.95))
        self.assertEqual(methodology["final_strategy"]["threshold"], 0.46)
        self.assertIs(methodology["model_fitting_authorized"], False)

    def test_toy_ensemble_and_confirmation_formulas(self) -> None:
        np.testing.assert_allclose(classical.equal_weight_lightgbm_xgboost([0.2, 0.4], [0.6, 0.8]), [0.4, 0.6])
        rows = [
            {"f1": 0.8, "f2": 0.7, "recall": 0.7, "fpr": 0.03, "threshold": 0.4},
            {"f1": 0.8, "f2": 0.8, "recall": 0.7, "fpr": 0.03, "threshold": 0.6},
        ]
        self.assertEqual(classical.select_validation_threshold(rows)["threshold"], 0.6)


class Stage17EquivalenceTests(unittest.TestCase):
    def test_frozen_panel_architecture_and_safety_boundary_are_exact(self) -> None:
        protocol = load_protocol(17)
        methodology = protocol["methodology"]
        self.assertEqual(tuple(methodology["frozen_transformer"]["checkpoint_seeds"]), attention.CHECKPOINT_SEEDS)
        self.assertEqual(tuple(methodology["case_panel"]["confusion_states"]), attention.CONFUSION_STATES)
        self.assertEqual(tuple(methodology["diagnostics"]["top_k"]), attention.TOP_K_VALUES)
        self.assertEqual(methodology["case_panel"]["total_cases"], 64)
        self.assertIs(methodology["private_attention_hook"]["framework_sensitive"], True)
        self.assertIs(methodology["model_loading_authorized"], False)
        self.assertIs(methodology["attention_extraction_authorized"], False)

    def test_toy_panel_ranks_cls_attention_entropy_and_rollout(self) -> None:
        np.testing.assert_array_equal(attention.evenly_spaced_positions(32, 16), [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 31])
        matrix = np.eye(3)
        matrix[0] = [0.5, 0.25, 0.25]
        np.testing.assert_allclose(attention.direct_cls_feature_attention(matrix), [0.5, 0.5])
        self.assertAlmostEqual(attention.normalized_entropy([0.5, 0.5]), 1.0)
        layers = np.asarray([[matrix], [matrix]])
        rollout = attention.attention_rollout(layers)
        self.assertEqual(rollout.shape, (2,))
        self.assertAlmostEqual(float(rollout.sum()), 1.0)

    def test_toy_ranking_and_agreement_formulas(self) -> None:
        np.testing.assert_array_equal(attention.deterministic_top_indices([0.2, 0.5, 0.5], 2), [1, 2])
        self.assertAlmostEqual(attention.cosine_similarity([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(attention.jaccard_similarity([1, 2], [2, 3]), 1 / 3)

    def test_frozen_attention_and_cross_method_results_match_protocol(self) -> None:
        methodology = load_protocol(17)["methodology"]
        result = read_json(
            "results/stage17_attention_explainability_checkpoint/stage17_2_attention_analysis_package/"
            "stage17_2_attention_analysis_result.json"
        )
        self.assertEqual(result["global_rollout"]["top20_features"][0]["feature"], methodology["frozen_headlines"]["global_top3_rollout_features"][0])
        self.assertAlmostEqual(result["global_rollout"]["cross_seed_stability"]["mean_cosine"], methodology["frozen_headlines"]["mean_cross_seed_cosine"])
        rows = read_csv(
            "results/stage17_attention_explainability_checkpoint/stage17_3b_cross_method_agreement_package/"
            "stage17_3b_cross_method_agreement.csv"
        )
        self.assertEqual(len(rows), 4)
        self.assertAlmostEqual(float(rows[0]["cosine_similarity"]), methodology["cross_method_agreement"]["frozen_results"]["XGBoost TreeSHAP"]["cosine"])

    def test_checkpoint_verification_hashes_bytes_without_deserialization(self) -> None:
        report = verify_only_report(load_protocol(17))
        self.assertTrue(all(row["status"] == "MATCH" for row in report["hashes"]))
        self.assertTrue(all(row["artifact_deserialized"] is False for row in report["hashes"]))


if __name__ == "__main__":
    unittest.main()
