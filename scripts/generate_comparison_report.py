"""Generate Markdown result tables from repository CSV artifacts."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/comparison/generated_results_summary.md"


def read_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row.get(column, "") for column in columns) + " |")
    return "\n".join([header, divider, *body])


def main() -> None:
    baseline = read_csv("results/baseline/final_16_model_validation_ablation.csv")
    tuned = read_csv("results/tuning/top5_tuned_validation_results.csv")
    thresholds = read_csv("results/threshold/all_top5_selected_validation_operating_points.csv")
    holdout = read_csv("results/holdout/objective_specific_final_test_results.csv")
    shap_meta = read_csv("results/shap/xgboost_lightgbm_top20_overlap.csv")

    selected_thresholds = [
        row
        for row in thresholds
        if row["Operating Point"] in {"Maximum Validation F1", "Constrained Maximum F2"}
        and row["Model"] in {"XGBoost Tuned", "LightGBM Tuned"}
    ]
    shared_shap = [row for row in shap_meta if row.get("Shared Top 20") == "True"]

    content = [
        "# Generated Results Summary",
        "",
        "This file is generated from CSV artifacts by `scripts/generate_comparison_report.py`.",
        "",
        "## Baseline Validation Ranking",
        "",
        table(
            baseline,
            ["Rank", "Model", "Accuracy", "Precision", "Recall", "F1-score", "FPR", "FN"],
        ),
        "",
        "## Tuned Top-Five Validation Results",
        "",
        table(
            tuned,
            ["Rank", "Model", "Threshold", "Accuracy", "Precision", "Recall", "F1-score", "FPR", "FN"],
        ),
        "",
        "## Selected Validation Operating Points",
        "",
        table(
            selected_thresholds,
            ["Operating Point", "Model", "Threshold", "Precision", "Recall", "F1-score", "F2-score", "FPR", "FN"],
        ),
        "",
        "## Final Holdout Results",
        "",
        table(
            holdout,
            ["Objective", "Model", "Threshold", "Accuracy", "Precision", "Recall", "F1-score", "F2-score", "FPR", "FN", "ROC-AUC", "PR-AUC"],
        ),
        "",
        "## Shared SHAP Top-20 Features",
        "",
        table(
            shared_shap,
            ["Feature", "XGBoost Rank", "LightGBM Rank", "Absolute Rank Difference"],
        ),
        "",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(content), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
