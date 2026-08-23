from __future__ import annotations

import csv
import hashlib
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.protocol_cli import load_protocol, verify_only_report
from ids_validation.stages.stage25 import registry as stage25
from ids_validation.stages.stage26 import registry as stage26
from ids_validation.stages.stage27 import registry as stage27
from ids_validation.stages.stage28 import registry as stage28


ARCHIVE_IDENTITIES = {
    "stage25_prevalence_operational_stress_executed.ipynb": (
        "58f529ca1e1f4a94083e533b5251b8f7433cfe57909477869a71d2cfbe5b61a3",
        8,
        7,
    ),
    "stage26_deployment_profiling_executed.ipynb": (
        "f26cf14b8f5b56c7e6cb882b075b26a2c575b1c722690591ba1e779fa4fe7177",
        108,
        105,
    ),
    "stage27_loao_unseen_attack_executed.ipynb": (
        "9180523c74e91fcb5b15a2ae6563db7567faa06d0e94710d718a197de4ff15cf",
        47,
        47,
    ),
    "stage28_stability_novelty_control_executed.ipynb": (
        "3d67dacd97050683de6b2d797e76cdefc4b35ed4f6bc13bb91992ea5c43e9f95",
        47,
        46,
    ),
}


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def notebook(relative: str) -> dict:
    return read_json(relative)


def normalized_source(cell: dict) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        source = "".join(source)
    return source.replace("\r\n", "\n").strip()


class LaterArchiveEquivalenceTests(unittest.TestCase):
    def test_archive_identities_cell_counts_and_output_counts(self) -> None:
        for name, (expected_hash, expected_cells, expected_outputs) in ARCHIVE_IDENTITIES.items():
            with self.subTest(notebook=name):
                path = ROOT / "notebooks" / "archive" / name
                document = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_hash)
                self.assertEqual(len(document["cells"]), expected_cells)
                self.assertEqual(
                    sum(bool(cell.get("outputs")) for cell in document["cells"]),
                    expected_outputs,
                )

    def test_stage25_repository_export_is_exactly_supplied_cells_2_to_8(self) -> None:
        full = notebook("notebooks/archive/stage25_prevalence_operational_stress_executed.ipynb")
        exported = notebook("scripts/stage25/stage25_prevalence_operational_stress.ipynb")
        exported_code = [normalized_source(cell) for cell in exported["cells"] if cell["cell_type"] == "code"]
        self.assertEqual(exported_code, [normalized_source(cell) for cell in full["cells"][1:8]])

    def test_stage26_virtual_source_identity_and_partial_exact_cell_coverage(self) -> None:
        full = notebook("notebooks/archive/stage26_deployment_profiling_executed.ipynb")
        script = (ROOT / "scripts/stage26/stage26_deployment_profiling_kaggle.py").read_text(
            encoding="utf-8"
        ).replace("\r\n", "\n")
        self.assertEqual(
            hashlib.sha256(script.encode("utf-8")).hexdigest(),
            "e042c75c86b5f43f0da34fdb1bd63f5cb35b744f7003eaf99559324b0738229a",
        )
        code_sources = [
            normalized_source(cell) for cell in full["cells"] if cell["cell_type"] == "code"
        ]
        self.assertEqual(len(code_sources), 106)
        self.assertEqual(sum(source in script for source in code_sources), 66)

    def test_stage27_repository_export_is_exactly_supplied_cells_34_to_45(self) -> None:
        full = notebook("notebooks/archive/stage27_loao_unseen_attack_executed.ipynb")
        exported = notebook("scripts/stage27/stage27_loao_unseen_attack.ipynb")
        exported_code = [normalized_source(cell) for cell in exported["cells"] if cell["cell_type"] == "code"]
        self.assertEqual(exported_code, [normalized_source(cell) for cell in full["cells"][33:45]])

    def test_stage28_repository_archive_is_exactly_supplied_cells_33_to_47(self) -> None:
        full = notebook("notebooks/archive/stage28_stability_novelty_control_executed.ipynb")
        exported = notebook("scripts/stage28/stage28_full_kaggle_notebook.ipynb")
        exported_code = [normalized_source(cell) for cell in exported["cells"] if cell["cell_type"] == "code"]
        self.assertEqual(exported_code, [normalized_source(cell) for cell in full["cells"][32:47]])


class Stage25AnalyticEquivalenceTests(unittest.TestCase):
    def test_frozen_grid_and_terminal_table_dimensions_are_exact(self) -> None:
        protocol = load_protocol(25)["methodology"]
        counts = protocol["terminal_counts"]
        self.assertEqual(tuple(protocol["scenario"]["prevalence_grid"]), stage25.PREVALENCE_GRID)
        self.assertEqual(tuple(protocol["scenario"]["ppv_targets"]), stage25.PPV_TARGETS)
        self.assertTrue(
            stage25.frozen_grid_shape_is_exact(
                counts["operating_points"],
                counts["projection_rows"],
                counts["ppv_break_even_rows"],
                counts["required_fpr_rows"],
                counts["cost_break_even_rows"],
            )
        )

    def test_all_144_bayesian_rows_recompute_from_frozen_scalars(self) -> None:
        rows = read_csv(
            "results/stage25_prevalence_stress/stage25_1_bayesian_projection/"
            "stage25_1_bayesian_projection_grid.csv"
        )
        self.assertEqual(len(rows), 144)
        for row in rows:
            tpr = float(row["tpr"])
            fpr = float(row["fpr"])
            prevalence = float(row["projection_prevalence"])
            self.assertAlmostEqual(stage25.ppv(tpr, fpr, prevalence), float(row["ppv"]), places=14)
            self.assertAlmostEqual(stage25.npv(tpr, fpr, prevalence), float(row["npv"]), places=14)

    def test_all_projection_and_capacity_values_recompute_from_frozen_scalars(self) -> None:
        rows = read_csv(
            "results/stage25_prevalence_stress/stage25_2_traffic_soc_capacity/"
            "stage25_2_traffic_soc_projection.csv"
        )
        self.assertEqual(len(rows), 144)
        for row in rows:
            tpr = float(row["tpr"])
            fpr = float(row["fpr"])
            prevalence = float(row["projection_prevalence"])
            projected = stage25.project_confusion(tpr, fpr, prevalence)
            expected = {
                "projected_attack_flows_per_day": projected.attack,
                "projected_total_flows_per_day": projected.total,
                "tp_per_day": projected.tp,
                "fp_per_day": projected.fp,
                "tn_per_day": projected.tn,
                "fn_per_day": projected.fn,
                "total_alerts_per_day": projected.alerts,
            }
            for field, value in expected.items():
                self.assertAlmostEqual(value, float(row[field]), places=10)
            for analysts in stage25.ANALYST_TIERS:
                self.assertAlmostEqual(
                    stage25.analyst_capacity_fpr_ceiling(tpr, prevalence, analysts),
                    float(row[f"exact_total_alert_fpr_ceiling_{analysts}"]),
                    places=14,
                )

    def test_all_break_even_tables_recompute_from_frozen_scalars(self) -> None:
        ppv_rows = read_csv(
            "results/stage25_prevalence_stress/stage25_3_break_even_analysis/"
            "ppv_break_even_points.csv"
        )
        required_rows = read_csv(
            "results/stage25_prevalence_stress/stage25_3_break_even_analysis/"
            "required_fpr_by_ppv.csv"
        )
        cost_rows = read_csv(
            "results/stage25_prevalence_stress/stage25_3_break_even_analysis/"
            "cost_break_even_points.csv"
        )
        self.assertEqual((len(ppv_rows), len(required_rows), len(cost_rows)), (120, 720, 24))
        for row in ppv_rows:
            self.assertAlmostEqual(
                stage25.ppv_break_even_prevalence(
                    float(row["tpr"]), float(row["fpr"]), float(row["ppv_target"])
                ),
                float(row["required_prevalence"]),
                places=14,
            )
        for row in required_rows:
            self.assertAlmostEqual(
                stage25.required_fpr(
                    float(row["tpr"]),
                    float(row["projection_prevalence"]),
                    float(row["ppv_target"]),
                ),
                float(row["required_max_fpr"]),
                places=14,
            )
        for row in cost_rows:
            self.assertAlmostEqual(
                stage25.cost_break_even_prevalence(
                    float(row["tpr"]),
                    float(row["fpr"]),
                    float(row["C_FP"]),
                    float(row["C_FN"]),
                ),
                float(row["cost_break_even_prevalence"]),
                places=14,
            )


class Stage26StaticMethodTests(unittest.TestCase):
    def test_measurement_plan_and_schedule_are_frozen(self) -> None:
        method = load_protocol(26)["methodology"]
        self.assertTrue(
            stage26.execution_plan_is_frozen(
                method["profile_targets"],
                method["batch_sizes"],
                method["cpu"]["condition_count"],
                method["cpu"]["randomization_seed"],
            )
        )
        schedule = {int(key): value for key, value in method["warmup_timed_runs"].items()}
        self.assertTrue(stage26.warmup_schedule_is_frozen(schedule))

    def test_timing_statistics_use_toy_values_and_no_clock(self) -> None:
        summary = stage26.summarize_toy_timing_ms([1_000_000, 2_000_000, 3_000_000, 4_000_000, 5_000_000])
        self.assertEqual(summary["p50_ms"], 3.0)
        self.assertAlmostEqual(summary["p95_ms"], 4.8)
        self.assertAlmostEqual(summary["p99_ms"], 4.96)
        self.assertFalse(hasattr(stage26, "time"))

    def test_gpu_and_publication_inventory_contracts_are_static(self) -> None:
        method = load_protocol(26)["methodology"]
        gpu = method["gpu"]
        self.assertTrue(
            stage26.gpu_contract_is_frozen(
                gpu["gpu_name"], gpu["synchronization"], gpu["condition_count"], gpu["raw_timing_observations"]
            )
        )
        self.assertTrue(stage26.publication_figure_inventory_is_complete(method["publication_figure_stems"]))
        files = [path.name for path in (ROOT / "figures/stage26_deployment_profiling").iterdir()]
        self.assertEqual(
            Counter(path.rsplit(".", 1)[0] for path in files),
            Counter({stem: 2 for stem in stage26.PUBLICATION_FIGURE_STEMS}),
        )


class Stage27StaticEquivalenceTests(unittest.TestCase):
    def test_taxonomy_support_and_threshold_grid_are_frozen(self) -> None:
        method = load_protocol(27)["methodology"]
        taxonomy = method["taxonomy"]
        self.assertTrue(
            stage27.taxonomy_is_frozen(
                taxonomy["family_order"],
                taxonomy["eligible_folds"],
                taxonomy["structurally_ineligible_folds"],
                taxonomy["descriptive_only_folds"],
            )
        )
        self.assertEqual(stage27.threshold_grid(), tuple(value / 100.0 for value in range(1, 100)))
        self.assertIs(taxonomy["literal_zero_day_claim"], False)

    def test_all_five_membership_receipts_have_zero_heldout_train_and_validation(self) -> None:
        receipts = {}
        for family in stage27.ELIGIBLE_FOLDS:
            document = read_json(
                "results/stage27_loao_unseen_attack/stage27_1a_fold_membership/"
                f"fold_{family}_membership_receipt.json"
            )
            receipts[family] = document["heldout_exclusion"]
            weight = document["class_weight"]
            self.assertAlmostEqual(
                stage27.class_weight(weight["train_benign"], weight["train_attack"]),
                weight["realized_value"],
                places=14,
            )
            self.assertEqual((weight["target_rows_used"], weight["validation_rows_used"]), (0, 0))
        self.assertTrue(stage27.membership_exclusion_is_exact(receipts))

    def test_fit_opening_ledgers_and_conclusions_are_terminal(self) -> None:
        method = load_protocol(27)["methodology"]
        fit = method["fit_budget"]
        openings = method["opening_ledger"]
        self.assertTrue(
            stage27.fit_and_opening_ledgers_are_closed(
                fit["authorized"], fit["completed"], openings["budget"], openings["consumed"],
                openings["remaining"], openings["reopening_authorized"]
            )
        )
        self.assertTrue(stage27.conclusion_labels_are_frozen(method["final_synthesis"]["conclusion_labels"]))
        synthesis = read_json(
            "results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/stage27_synthesis_receipt.json"
        )
        self.assertEqual(synthesis["target_opening_ledger"], {"consumed": 5, "budget": 5, "remaining": 0, "reopening_authorized": False})
        self.assertEqual(len(read_csv("results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/stage27_final_primary_metrics.csv")), 10)


class Stage28StaticEquivalenceTests(unittest.TestCase):
    def test_component_manifest_and_seed_registry_are_exact(self) -> None:
        method = load_protocol(28)["methodology"]
        self.assertTrue(stage28.seed_spec_is_frozen(method["seeds"], method["reference_seed"], method["random_membership_seed"]))
        manifest = read_csv(
            "results/stage28_stability_novelty_control/stage28_1b_random_loao_membership_and_execution_lock/"
            "stage28_component_execution_manifest.csv"
        )
        actions = Counter(row["fit_action"] for row in manifest)
        experiments = Counter(row["experiment"] for row in manifest)
        self.assertEqual(len(manifest), 120)
        self.assertEqual(actions, Counter({"NEW_FIT_AUTHORIZED": 108, "REUSE_EXISTING": 12}))
        self.assertEqual(experiments["STAGE27_CHRONOLOGY_LOAO"], 50)
        self.assertEqual(experiments["STAGE28B_RANDOM_LOAO"], 50)
        self.assertEqual(len({row["evaluation_cell_id"] for row in manifest}), 110)
        self.assertTrue(stage28.component_manifest_is_exact(120, 108, 12, 110))

    def test_closure_ledger_and_seed_level_realizations_are_terminal(self) -> None:
        closure = read_json(
            "results/stage28_stability_novelty_control/stage28_3a_experiment_closure_audit/"
            "stage28_3a_experiment_closure_receipt.json"
        )
        budget = closure["fit_budget_closure"]
        seed_rows = read_csv(
            "results/stage28_stability_novelty_control/stage28_3_seed_uncertainty/"
            "stage28_3b_loao_seed_level_metrics.csv"
        )
        arm_counts = Counter(row["arm"] for row in seed_rows)
        self.assertEqual(arm_counts, Counter({"28A_CHRONOLOGY_LOAO": 50, "28B_RANDOM_LOAO_CONTROL": 50}))
        self.assertTrue(
            stage28.empirical_ledger_is_closed(
                budget["authorized_new_fits"], budget["consumed_new_fits"], budget["remaining_new_fits"],
                arm_counts["28A_CHRONOLOGY_LOAO"], arm_counts["28B_RANDOM_LOAO_CONTROL"], 10
            )
        )

    def test_shared_holdout_claims_are_five_of_five_and_wall_is_closed(self) -> None:
        rows = read_csv(
            "results/stage28_stability_novelty_control/stage28_4_stage22_shared_final_holdout/"
            "stage28_4_stage22_directional_stability_summary.csv"
        )
        claims = {
            "PR_RANDOM_LT_CHRONO": {
                "supporting": int(rows[0]["supporting_seeds"]),
                "total": int(rows[0]["total_frozen_seeds"]),
            },
            "ROC_RANDOM_LT_CHRONO": {
                "supporting": int(rows[1]["supporting_seeds"]),
                "total": int(rows[1]["total_frozen_seeds"]),
            },
        }
        self.assertTrue(stage28.shared_holdout_direction_is_five_of_five(claims))
        method = load_protocol(28)["methodology"]
        wall = method["final_wall"]
        self.assertTrue(
            stage28.final_wall_is_closed(
                wall["stage29_authorized"], wall["new_fits_authorized"],
                wall["target_reopenings_authorized"], wall["threshold_reselection_authorized"],
                wall["new_significance_tests_authorized"]
            )
        )
        numbers = read_json(
            "results/stage28_stability_novelty_control/stage28_final_synthesis/"
            "stage28_final_manuscript_numbers.json"
        )
        self.assertEqual(numbers["stage22_shared_holdout"]["PR_RANDOM_LT_CHRONO"]["supporting_seeds"], 5)
        self.assertEqual(numbers["stage22_shared_holdout"]["ROC_RANDOM_LT_CHRONO"]["supporting_seeds"], 5)
        self.assertEqual(len(read_csv("results/stage28_stability_novelty_control/stage28_final_synthesis/stage28_final_claim_registry.csv")), 112)


class FrozenArtifactVerificationTests(unittest.TestCase):
    EXPECTED_HASH_COUNTS = {25: 10, 26: 25, 27: 21, 28: 21}

    def test_all_declared_stage25_to_stage28_hashes_match_without_deserialization(self) -> None:
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
