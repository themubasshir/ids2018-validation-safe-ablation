"""Validate the published IDS2018 validation-safe repository."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GITHUB_LIMIT = 100 * 1024 * 1024
RAW_DATA_PATTERNS = (
    "raw_data/",
    "data/raw/",
    "merged_balanced_ids2018_safe.csv",
    "ids2018-balanced-binary-dataset",
)
ARCHIVE_PATTERNS = (".tar.gz", ".zip")
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "ids2018_clean_validation_v2", "FINAL_REVISED_LIGHTGBM", ".virtual_documents"}


REQUIRED_FILES = [
    "README.md",
    "DATASET.md",
    "REPRODUCIBILITY.md",
    "requirements.txt",
    ".gitignore",
    "metadata/feature_names.json",
    "metadata/split_metadata.json",
    "metadata/split_summary.csv",
    "metadata/split_indices.npz",
    "metadata/standard_scaler.joblib",
    "results/baseline/final_16_model_validation_ablation.csv",
    "results/baseline/validation_selected_top5_models.csv",
    "results/tuning/top5_tuned_validation_results.csv",
    "results/threshold/all_top5_selected_validation_operating_points.csv",
    "results/threshold/all_top5_threshold_summary.csv",
    "results/holdout/objective_specific_final_test_results.csv",
    "results/shap/xgboost_shap_top20_features.csv",
    "results/shap/lightgbm_shap_top20_features.csv",
    "results/shap/xgboost_lightgbm_top20_overlap.csv",
    "results/shap/xgboost_lightgbm_shap_global_comparison.csv",
    "metadata/dual_model_shap_metadata.json",
    "docs/EXPERIMENT_PROTOCOL.md",
    "docs/ORIGINAL_VS_VALIDATION_SAFE.md",
    "docs/RESULTS_SUMMARY.md",
    "docs/STATISTICAL_CONFIDENCE.md",
    "docs/CALIBRATION_ASSESSMENT.md",
    "docs/OPERATIONAL_COST_ANALYSIS.md",
    "docs/ATTACK_CATEGORY_ANALYSIS.md",
    "docs/MULTISEED_ROBUSTNESS.md",
    "docs/JOURNAL_EXTENSION_SUMMARY.md",
    "results/statistical_confidence/bootstrap_point_estimates.csv",
    "results/statistical_confidence/operating_point_bootstrap_intervals.csv",
    "results/statistical_confidence/paired_balanced_model_differences.csv",
    "results/statistical_confidence/paired_security_model_differences.csv",
    "results/statistical_confidence/paired_auc_differences.csv",
    "results/statistical_confidence/within_model_threshold_tradeoffs.csv",
    "results/statistical_confidence/bootstrap_replicates.npz",
    "metadata/statistical_confidence/bootstrap_methodology.json",
    "results/calibration/calibration_metric_point_estimates.csv",
    "results/calibration/calibration_bootstrap_intervals.csv",
    "results/calibration/paired_calibration_differences.csv",
    "results/calibration/calibration_bins_equal_width.csv",
    "results/calibration/calibration_bins_equal_frequency.csv",
    "results/calibration/calibration_bin_sensitivity.csv",
    "results/calibration/brier_score_decomposition.csv",
    "results/calibration/probability_distribution_summary.csv",
    "results/calibration/calibration_bootstrap_replicates.npz",
    "metadata/calibration/calibration_assessment_methodology.json",
    "results/operational_cost/validation_cost_ratio_threshold_selection.csv",
    "results/operational_cost/holdout_cost_ratio_evaluation.csv",
    "results/operational_cost/frozen_operating_point_costs.csv",
    "results/operational_cost/break_even_cost_analysis.csv",
    "results/operational_cost/validation_fp_fn_pareto_frontier.csv",
    "results/operational_cost/normalized_operational_burden.csv",
    "metadata/operational_cost/operational_cost_methodology.json",
    "results/attack_category/attack_category_operating_point_metrics.csv",
    "results/attack_category/attack_category_support_summary.csv",
    "results/attack_category/paired_xgboost_balanced_vs_lightgbm_security.csv",
    "results/attack_category/paired_xgboost_security_vs_lightgbm_security.csv",
    "results/attack_category/within_model_attack_category_threshold_effects.csv",
    "results/attack_category/hardest_attack_categories.csv",
    "results/attack_category/holdout_attack_category_prediction_manifest.csv",
    "metadata/attack_category/attack_category_methodology.json",
    "results/multiseed/multiseed_model_operating_points.csv",
    "results/multiseed/multiseed_selected_winners.csv",
    "results/multiseed/multiseed_metric_summary.csv",
    "results/multiseed/multiseed_winner_frequency.csv",
    "results/multiseed/multiseed_threshold_stability.csv",
    "results/multiseed/multiseed_paired_model_differences.csv",
    "results/multiseed/multiseed_split_summary.csv",
    "metadata/multiseed/fixed_model_parameters.json",
    "metadata/multiseed/multiseed_methodology.json",
    "figures/JOURNAL_FIGURE_INDEX.md",
]


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def ok(message: str) -> None:
    print(f"OK: {message}")


def tracked_files() -> list[Path]:
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
    except Exception:
        return []
    return [ROOT / line.strip() for line in proc.stdout.splitlines() if line.strip()]


def readme_linked_figures() -> list[str]:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    return [link for link in links if link.lower().endswith(".png")]


def repo_files(pattern: str) -> list[Path]:
    return [path for path in ROOT.rglob(pattern) if not any(part in SKIP_DIRS for part in path.parts)]


def validate_png(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(8) == b"\x89PNG\r\n\x1a\n"


def approx(value: float, expected: float, tolerance: float = 1e-6) -> bool:
    return abs(value - expected) <= tolerance


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if (ROOT / rel).exists():
            ok(f"required file exists: {rel}")
        else:
            fail(f"missing required file: {rel}", failures)

    for csv_path in repo_files("*.csv"):
        try:
            rows = read_csv(str(csv_path.relative_to(ROOT)))
            if rows:
                ok(f"CSV loads with {len(rows)} rows: {csv_path.relative_to(ROOT)}")
            else:
                ok(f"CSV loads and is empty/header-only: {csv_path.relative_to(ROOT)}")
        except Exception as exc:
            fail(f"CSV failed to load: {csv_path.relative_to(ROOT)} ({exc})", failures)

    baseline = read_csv("results/baseline/final_16_model_validation_ablation.csv")
    if len({row["Model"] for row in baseline}) == 16:
        ok("baseline result contains exactly 16 unique models")
    else:
        fail("baseline result does not contain exactly 16 unique models", failures)

    tuned = read_csv("results/tuning/top5_tuned_validation_results.csv")
    if len({row["Model"] for row in tuned}) == 5:
        ok("tuned comparison contains exactly 5 unique models")
    else:
        fail("tuned comparison does not contain exactly 5 unique models", failures)

    split = json.loads((ROOT / "metadata/split_metadata.json").read_text(encoding="utf-8"))
    expected_split = {
        "training_records": 192593,
        "validation_records": 48149,
        "test_records": 60186,
        "predictor_features": 78,
    }
    for key, expected in expected_split.items():
        if split.get(key) == expected:
            ok(f"{key} is {expected}")
        else:
            fail(f"{key} expected {expected}, found {split.get(key)}", failures)

    selected = read_csv("results/threshold/all_top5_selected_validation_operating_points.csv")
    by_model_point = {(row["Model"], row["Operating Point"]): row for row in selected}
    xgb = by_model_point.get(("XGBoost Tuned", "Maximum Validation F1"))
    lgb = by_model_point.get(("LightGBM Tuned", "Constrained Maximum F2"))

    if xgb and abs(float(xgb["Threshold"]) - 0.51) < 1e-12:
        ok("XGBoost balanced threshold is 0.51")
    else:
        fail("XGBoost balanced threshold is not 0.51", failures)

    if lgb and abs(float(lgb["Threshold"]) - 0.26) < 1e-12:
        ok("LightGBM constrained threshold is 0.26")
    else:
        fail("LightGBM constrained threshold is not 0.26", failures)

    if lgb and float(lgb["FPR"]) <= 0.05:
        ok("LightGBM validation FPR is <= 0.05")
    else:
        fail("LightGBM validation FPR exceeds 0.05", failures)

    shap_meta = json.loads((ROOT / "metadata/dual_model_shap_metadata.json").read_text(encoding="utf-8"))
    if shap_meta.get("Top-20 Shared Feature Count") == 15:
        ok("SHAP shared top-20 count is 15")
    else:
        fail("SHAP shared top-20 count is not 15", failures)

    bootstrap_meta = json.loads((ROOT / "metadata/statistical_confidence/bootstrap_methodology.json").read_text(encoding="utf-8"))
    if bootstrap_meta.get("Successful Bootstrap Replicates") == 2000:
        ok("Stage 8 replicate count is 2,000")
    else:
        fail("Stage 8 replicate count is not 2,000", failures)

    calibration_meta = json.loads((ROOT / "metadata/calibration/calibration_assessment_methodology.json").read_text(encoding="utf-8"))
    if calibration_meta.get("Successful Bootstrap Replicates") == 2000:
        ok("Stage 9 calibration replicate count is 2,000")
    else:
        fail("Stage 9 calibration replicate count is not 2,000", failures)

    break_even = read_csv("results/operational_cost/break_even_cost_analysis.csv")
    lgb_break_even = next((row for row in break_even if row["Comparison"] == "LightGBM Security vs LightGBM Balanced"), None)
    if lgb_break_even and approx(float(lgb_break_even["Break-even FN to FP Cost Ratio"]), 1.840708, 1e-6):
        ok("Stage 10 LightGBM break-even ratio is approximately 1.840708")
    else:
        fail("Stage 10 LightGBM break-even ratio check failed", failures)

    attack_support = read_csv("results/attack_category/attack_category_support_summary.csv")
    if len({row["Attack Category"] for row in attack_support}) == 12:
        ok("Stage 11 attack category count is 12")
    else:
        fail("Stage 11 attack category count is not 12", failures)
    infiltration = next((row for row in attack_support if row["Attack Category"] == "Infilteration"), None)
    if infiltration and int(infiltration["Support"]) == 3967:
        ok("Stage 11 Infiltration support is 3,967")
    else:
        fail("Stage 11 Infiltration support is not 3,967", failures)

    multiseed = read_csv("results/multiseed/multiseed_split_summary.csv")
    seeds = {int(row["Seed"]) for row in multiseed}
    if seeds == {42, 52, 62, 72, 82}:
        ok("Stage 12 contains exactly five expected seeds")
    else:
        fail(f"Stage 12 seed set mismatch: {sorted(seeds)}", failures)

    winner_frequency = read_csv("results/multiseed/multiseed_winner_frequency.csv")
    totals = {}
    wins = {}
    for row in winner_frequency:
        objective = row["Objective"]
        count = int(row["Winner Count"])
        totals[objective] = totals.get(objective, 0) + count
        wins[(objective, row["Selected Model"])] = count
    if totals.get("Balanced") == 5:
        ok("balanced winner frequency totals five")
    else:
        fail("balanced winner frequency does not total five", failures)
    if totals.get("Security") == 5:
        ok("security winner frequency totals five")
    else:
        fail("security winner frequency does not total five", failures)
    if wins.get(("Balanced", "XGBoost Tuned")) == 3:
        ok("XGBoost balanced wins three")
    else:
        fail("XGBoost balanced does not win three times", failures)
    if wins.get(("Security", "LightGBM Tuned")) == 4:
        ok("LightGBM security wins four")
    else:
        fail("LightGBM security does not win four times", failures)

    tracked = tracked_files()
    for path in tracked:
        rel = path.relative_to(ROOT).as_posix()
        if any(pattern in rel for pattern in RAW_DATA_PATTERNS):
            fail(f"raw dataset appears tracked: {rel}", failures)
        if rel.endswith(ARCHIVE_PATTERNS):
            fail(f"archive appears tracked: {rel}", failures)
        if path.exists() and path.stat().st_size >= GITHUB_LIMIT:
            fail(f"tracked file exceeds 100 MB: {rel}", failures)
    ok("tracked-file raw-data and 100 MB checks completed")

    for figure in readme_linked_figures():
        figure_path = ROOT / figure
        if figure_path.exists():
            ok(f"README-linked figure exists: {figure}")
        else:
            fail(f"README-linked figure missing: {figure}", failures)

    for png_path in repo_files("*.png"):
        if validate_png(png_path):
            ok(f"PNG opens by signature: {png_path.relative_to(ROOT)}")
        else:
            fail(f"PNG signature invalid: {png_path.relative_to(ROOT)}", failures)

    report = {
        "status": "passed" if not failures else "failed",
        "failure_count": len(failures),
        "failures": failures,
        "checked_files": len(repo_files("*")),
    }
    report_path = ROOT / "metadata/repository_validation_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if failures:
        print(f"\nRepository validation failed with {len(failures)} issue(s).")
        return 1
    print("\nRepository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
