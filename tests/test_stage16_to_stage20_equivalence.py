from __future__ import annotations

import csv
import json
import sys
import unittest
from datetime import datetime
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.protocol_cli import load_protocol, verify_only_report
from ids_validation.data import graph_snapshots, temporal_bins
from ids_validation.evaluation import attention
from ids_validation.models import classical, graph_models, masked_cnn, temporal_models
from ids_validation.stages.stage20.cnn import registry as cnn_registry
from ids_validation.stages.stage20.compact_corpus import manifest as corpus_manifest
from ids_validation.stages.stage20.directed_s4 import signature
from ids_validation.stages.stage20.evaluation import operating_points
from ids_validation.stages.stage20.extractor_forensics import flags
from ids_validation.stages.stage20.governance import holdout
from ids_validation.stages.stage20.packet_representation import encoder, geometry
from ids_validation.stages.stage20.provenance import registry as stage20_provenance
from ids_validation.stages.stage20.reconstruction import transitions


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


class Stage18EquivalenceTests(unittest.TestCase):
    def test_three_historical_branch_decisions_and_chronology_are_frozen(self) -> None:
        methodology = load_protocol(18)["methodology"]
        self.assertEqual(methodology["overall_decisions"]["temporal_mtemporal"], "SUPPORTED_WITH_CONSTRAINTS")
        self.assertEqual(methodology["overall_decisions"]["vision_transformer"], "NOT_SUPPORTED_BY_CURRENT_ARTIFACTS")
        self.assertEqual(methodology["overall_decisions"]["graph_transformer"], "SUPPORTED_WITH_CONSTRAINTS")
        self.assertIn("must not retroactively change", methodology["chronology_of_knowledge"])
        self.assertIs(methodology["vit_feasibility"]["vit_models_fit"], 0)

    def test_toy_graph_partition_snapshot_and_shape_helpers(self) -> None:
        self.assertEqual(graph_snapshots.chronological_partition(datetime.fromisoformat("2018-02-20 08:59:59")), "train")
        self.assertEqual(graph_snapshots.chronological_partition(datetime.fromisoformat("2018-02-20 09:00:00")), "validation")
        self.assertEqual(graph_snapshots.chronological_partition(datetime.fromisoformat("2018-02-20 11:00:00")), "holdout")
        np.testing.assert_array_equal(graph_snapshots.wall_clock_snapshot_indices([0, 59, 60, 119]), [0, 0, 1, 1])
        shape = graph_snapshots.validate_directed_multigraph_shapes([0, 0, 1], [1, 1, 0], np.zeros((3, 70)))
        self.assertEqual(shape, {"nodes": 2, "edges": 3, "edge_feature_dim": 70})

    def test_graph_seed_architecture_threshold_and_negative_finding_are_exact(self) -> None:
        graph = load_protocol(18)["methodology"]["graph_branch"]
        self.assertEqual(tuple(graph["replication"]["seeds"]), graph_models.SEEDS)
        self.assertEqual(graph["chronology"]["snapshot_seconds"], graph_snapshots.SNAPSHOT_SECONDS)
        self.assertEqual(graph_models.EDGE_ONLY_SPEC.parameter_count, 17_409)
        self.assertEqual(graph_models.GRAPH_TRANSFORMER_SPEC.parameter_count, 113_993)
        self.assertEqual(len(graph_models.threshold_grid()), 99)
        self.assertEqual((graph_models.threshold_grid()[0], graph_models.threshold_grid()[-1]), (0.01, 0.99))
        self.assertEqual(graph["frozen_findings"]["graph_holdout_true_positives"], 0)
        self.assertEqual(graph["frozen_findings"]["graph_holdout_false_negatives"], 151_773)

    def test_toy_graph_threshold_tie_rule(self) -> None:
        rows = [
            {"f1": 0.8, "recall": 0.7, "threshold": 0.01},
            {"f1": 0.8, "recall": 0.8, "threshold": 0.02},
        ]
        self.assertEqual(graph_models.select_validation_threshold(rows)["threshold"], 0.02)

    def test_all_six_graph_checkpoint_hashes_match_without_deserialization(self) -> None:
        report = verify_only_report(load_protocol(18))
        self.assertEqual(len(report["hashes"]), 6)
        self.assertTrue(all(row["status"] == "MATCH" for row in report["hashes"]))
        self.assertTrue(all(row["artifact_deserialized"] is False for row in report["hashes"]))


class Stage19EquivalenceTests(unittest.TestCase):
    def test_dates_one_second_representation_and_train_only_preprocessing_are_exact(self) -> None:
        methodology = load_protocol(19)["methodology"]
        self.assertEqual(methodology["partition"]["train_range"], "2018-02-14 through 2018-02-23")
        self.assertEqual(methodology["partition"]["validation_files"], ["02-28-2018.csv"])
        self.assertEqual(methodology["partition"]["holdout_files"], ["03-01-2018.csv", "03-02-2018.csv"])
        self.assertEqual(methodology["one_second_materialization"]["base_resolution_seconds"], 1)
        self.assertIs(methodology["train_only_preprocessing"]["validation_or_holdout_statistics_used"], False)

    def test_toy_train_transform_and_multiscale_shapes(self) -> None:
        raw = np.full((1201, temporal_bins.BASE_FEATURE_COUNT), np.nan)
        means = np.arange(temporal_bins.BASE_FEATURE_COUNT, dtype=np.float64)
        scales = np.ones(temporal_bins.BASE_FEATURE_COUNT)
        standardized = temporal_bins.standardize_base(raw, means, scales)
        np.testing.assert_array_equal(standardized, np.zeros_like(standardized))
        fine, medium, coarse = temporal_bins.construct_multiscale(standardized, np.arange(1201) % 3, 1200)
        self.assertEqual(fine.shape, (60, 80))
        self.assertEqual(medium.shape, (20, 80))
        self.assertEqual(coarse.shape, (20, 80))
        np.testing.assert_array_equal(temporal_bins.construct_fine_only(standardized, np.arange(1201) % 3, 1200), fine)

    def test_temporal_architecture_seed_threshold_and_governance_are_exact(self) -> None:
        methodology = load_protocol(19)["methodology"]
        self.assertEqual(tuple(methodology["training"]["seeds"]), temporal_models.SEEDS)
        self.assertEqual(temporal_models.SINGLE_SCALE_SPEC.input_dimension, 80)
        self.assertEqual(temporal_models.MTEMPORAL_SPEC.layers_per_branch, 2)
        self.assertEqual(len(temporal_models.threshold_grid()), 99)
        self.assertEqual((temporal_models.threshold_grid()[0], temporal_models.threshold_grid()[-1]), (0.01, 0.99))
        self.assertEqual(methodology["threshold"]["single_scale_frozen"], 0.01)
        self.assertEqual(methodology["threshold"]["mtemporal_frozen"], 0.01)
        self.assertEqual(methodology["holdout_governance"]["status"], "PERMANENTLY_CLOSED")

    def test_toy_temporal_threshold_tie_rule_and_frozen_reversal(self) -> None:
        rows = [
            {"f1": 0.7, "recall": 0.8, "threshold": 0.01},
            {"f1": 0.7, "recall": 0.8, "threshold": 0.02},
        ]
        self.assertEqual(temporal_models.select_validation_threshold(rows)["threshold"], 0.01)
        findings = load_protocol(19)["methodology"]["frozen_findings"]
        self.assertLess(findings["validation"]["mtemporal_pr_auc"], findings["validation"]["single_scale_pr_auc"])
        self.assertLess(findings["march_1"]["mtemporal_f1"], findings["march_1"]["single_scale_f1"])
        self.assertGreater(findings["march_2"]["mtemporal_f1"], findings["march_2"]["single_scale_f1"])

    def test_scaler_and_six_model_hashes_match_without_deserialization(self) -> None:
        report = verify_only_report(load_protocol(19))
        self.assertEqual(len(report["hashes"]), 7)
        self.assertTrue(all(row["status"] == "MATCH" for row in report["hashes"]))
        self.assertTrue(all(row["artifact_deserialized"] is False for row in report["hashes"]))


class Stage20EquivalenceTests(unittest.TestCase):
    def test_source_boundary_and_substage_map_are_exact(self) -> None:
        protocol = load_protocol(20)
        self.assertEqual(protocol["source"]["physical_cells_1_based"], list(range(312, 462)))
        self.assertEqual(protocol["source"]["stage21_excluded_cells"], "462–488")
        rows = read_csv("docs/reproducibility/STAGE20_CELL_MAP.csv")
        self.assertEqual(len(rows), 150)
        self.assertEqual([int(row["physical_cell"]) for row in rows], list(range(312, 462)))

    def test_source_hash_and_label_hygiene_registries_are_frozen(self) -> None:
        self.assertEqual(len(stage20_provenance.DEVELOPMENT_PCAPS), 4)
        self.assertEqual(stage20_provenance.DEVELOPMENT_PCAPS[0].sha256, "f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972")
        self.assertEqual(stage20_provenance.HOLDOUT_PCAP.status, "LATER_FROZEN_EVIDENCE_NOTEBOOK_CELL_NOT_MAPPED")
        self.assertEqual(len(stage20_provenance.CANONICAL_LABEL_TABLES), 5)
        provenance = read_json("configs/stage20/provenance.json")
        self.assertEqual(provenance["label_hygiene"]["thursday_morning_structural_all_column_null_suffix_rows"], 288_602)

    def test_exact_s4_order_signed_duration_and_flag_serialization(self) -> None:
        self.assertEqual(len(signature.SIGNATURE_FIELDS), 21)
        record = {field: index for index, field in enumerate(signature.SIGNATURE_FIELDS)}
        record["Flow Duration"] = -7
        built = signature.build_signature(record)
        self.assertEqual(built[6], -7)
        self.assertEqual(built[0], record["Source IP"])
        semantic = {"FIN": 1, "SYN": 2, "RST": 3, "PSH": 4, "ACK": 5, "URG": 6, "CWR": 7, "ECE": 8}
        self.assertEqual(flags.serialize_semantic_flags(semantic), (3, 4, 8, 2, 5, 1, 6, 7))

    def test_d5_v1_transition_accounting_and_negative_rule_status(self) -> None:
        self.assertEqual(sum(transitions.TRANSITION_COUNTS.values()), 675)
        self.assertEqual(transitions.D5_COUNTS["membership_exact"], 635)
        self.assertEqual(transitions.V1_COUNTS["membership_exact"], 318)
        self.assertEqual(transitions.classify_transition(True, False), "exact_to_absent")
        self.assertEqual(transitions.classify_transition(False, True), "absent_to_exact")
        reconstruction = read_json("configs/stage20/reconstruction.json")
        self.assertEqual(reconstruction["v1_global_payload_validation"]["status"], "PRE_FROZEN_HYPOTHESIS_REJECTED_AS_GLOBAL_RECONSTRUCTION_RULE")
        self.assertIs(reconstruction["c16_mechanism_closure"]["published_label_reconstruction_rule_adopted"], False)

    def test_toy_geometry_masking_padding_and_truncation(self) -> None:
        self.assertEqual(geometry.select_geometry({38: 95, 39: 5}, {64: 94, 2960: 6}), (64, 256, 1))
        packet = bytearray(value % 256 for value in range(300))
        packet[0], packet[6], packet[7], packet[9] = 0x45, 0, 0, 6
        image, mask = encoder.encode_packet_rows([bytes(packet)] * 70)
        self.assertEqual((image.shape, mask.shape), ((64, 256), (64, 256)))
        self.assertEqual((image.dtype, mask.dtype), (np.dtype("uint8"), np.dtype("bool")))
        self.assertTrue(mask[0, 4])
        self.assertEqual(image[0, 4], 0)
        self.assertEqual(image[0, 20], 20)
        self.assertEqual(image[0, 24], 0)
        self.assertEqual(image[0, 255], 255)
        short_image, short_mask = encoder.encode_packet_rows([b"\x45"])
        self.assertTrue(short_mask[0, 0])
        self.assertFalse(short_mask[0, 1])
        self.assertFalse(short_mask[1].any())
        self.assertAlmostEqual(float(encoder.scale_for_model(short_image)[0, 0]), 69 / 255)

    def test_compact_corpus_receipts_preserve_daily_counts_and_hashes(self) -> None:
        self.assertEqual([(row.day, row.split, row.flow_count) for row in corpus_manifest.CORPUS_RECEIPTS], [
            ("Monday", "TRAIN", 528_509),
            ("Tuesday", "TRAIN", 4_170),
            ("Wednesday", "TRAIN", 12_951),
            ("Thursday", "VALIDATION", 8_197),
        ])
        self.assertEqual(corpus_manifest.CORPUS_RECEIPTS[0].files[0].sha256, "27e6f730c9951075f500bedc96b91d215b74a995ee23e1f09e269eaa7a2bd82c")
        self.assertIs(corpus_manifest.DENSE_PADDING_PERSISTED, False)
        self.assertIs(corpus_manifest.PADDING_MASK_RECONSTRUCTED_FROM_LENGTHS, True)

    def test_cnn_architecture_training_and_runtime_metadata_are_exact(self) -> None:
        self.assertEqual(masked_cnn.MASKED_CNN_SPEC.input_shape, (1, 64, 256))
        self.assertEqual([block.output_channels for block in masked_cnn.MASKED_CNN_SPEC.blocks], [32, 64, 128])
        self.assertEqual(masked_cnn.MASKED_CNN_SPEC.trainable_parameters, 93_025)
        self.assertEqual((cnn_registry.TRAINING_SPEC.seed, cnn_registry.TRAINING_SPEC.epochs, cnn_registry.TRAINING_SPEC.batch_size), (42, 10, 256))
        config = read_json("configs/stage20/cnn_governance.json")
        self.assertEqual(config["isolated_training_runtime"]["pytorch"], "2.10.0+cu126")
        self.assertEqual(config["isolated_training_runtime"]["gpu"], "Tesla P100-PCIE-16GB")

    def test_toy_threshold_rules_and_frozen_thursday_points(self) -> None:
        self.assertEqual((len(operating_points.threshold_grid()), operating_points.threshold_grid()[0], operating_points.threshold_grid()[-1]), (91, 0.05, 0.95))
        tied = [
            {"TP": 8, "TN": 90, "FP": 10, "FN": 2, "threshold_integer_percent": 60},
            {"TP": 8, "TN": 90, "FP": 10, "FN": 2, "threshold_integer_percent": 40},
        ]
        self.assertEqual(operating_points.select_balanced(tied)["threshold_integer_percent"], 40)
        security_rows = [
            {"TP": 9, "TN": 94, "FP": 6, "FN": 1, "threshold_integer_percent": 10},
            {"TP": 8, "TN": 96, "FP": 4, "FN": 2, "threshold_integer_percent": 17},
        ]
        self.assertEqual(operating_points.select_security(security_rows)["threshold_integer_percent"], 17)
        self.assertEqual((operating_points.STANDARD_THRESHOLD, operating_points.BALANCED_THRESHOLD, operating_points.SECURITY_THRESHOLD), (0.50, 0.17, 0.17))

    def test_friday_direct_lineage_and_later_unmapped_evidence_are_separate(self) -> None:
        self.assertEqual(holdout.DIRECT_NOTEBOOK_RECORD.source_cells, tuple(range(455, 462)))
        self.assertEqual(holdout.DIRECT_NOTEBOOK_RECORD.inference_passes, 0)
        self.assertEqual(len(holdout.UNMAPPED_LATER_ARTIFACTS), 7)
        self.assertTrue(all((ROOT / path).is_file() for path in holdout.UNMAPPED_LATER_ARTIFACTS))
        protocol = load_protocol(20)
        self.assertEqual(protocol["unmapped_frozen_evidence"]["mapping_status"], "NOTEBOOK_CELL_NOT_MAPPED")
        self.assertIs(protocol["holdout_policy"]["opened_during_extraction"], False)

    def test_all_stage20_declared_hashes_match_without_deserialization(self) -> None:
        report = verify_only_report(load_protocol(20))
        self.assertEqual(len(report["hashes"]), 22)
        self.assertTrue(all(row["status"] == "MATCH" for row in report["hashes"]))
        self.assertTrue(all(row["artifact_deserialized"] is False for row in report["hashes"]))
        self.assertIs(report["scientific_files_opened"], False)


if __name__ == "__main__":
    unittest.main()
