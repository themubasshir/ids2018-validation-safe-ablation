"""Generate Markdown result tables from repository CSV artifacts."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/comparison/generated_results_summary.md"
JOURNAL_TABLE_DIR = ROOT / "tables/journal_extension"


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


def write_csv(path: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def latex_escape(value: str) -> str:
    return (
        str(value)
        .replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def write_latex(path: Path, rows: list[dict[str, str]], columns: list[str], caption: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    spec = "l" * len(columns)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{latex_escape(caption)}}}",
        rf"\begin{{tabular}}{{{spec}}}",
        r"\hline",
        " & ".join(latex_escape(column) for column in columns) + r" \\",
        r"\hline",
    ]
    for row in rows:
        lines.append(" & ".join(latex_escape(row.get(column, "")) for column in columns) + r" \\")
    lines.extend([r"\hline", r"\end{tabular}", r"\end{table}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_table_pair(name: str, rows: list[dict[str, str]], columns: list[str], caption: str) -> None:
    write_csv(JOURNAL_TABLE_DIR / f"{name}.csv", rows, columns)
    write_latex(JOURNAL_TABLE_DIR / f"{name}.tex", rows, columns, caption)


def main() -> None:
    baseline = read_csv("results/baseline/final_16_model_validation_ablation.csv")
    tuned = read_csv("results/tuning/top5_tuned_validation_results.csv")
    thresholds = read_csv("results/threshold/all_top5_selected_validation_operating_points.csv")
    holdout = read_csv("results/holdout/objective_specific_final_test_results.csv")
    shap_meta = read_csv("results/shap/xgboost_lightgbm_top20_overlap.csv")
    bootstrap_balanced = read_csv("results/statistical_confidence/paired_balanced_model_differences.csv")
    bootstrap_security = read_csv("results/statistical_confidence/paired_security_model_differences.csv")
    bootstrap_auc = read_csv("results/statistical_confidence/paired_auc_differences.csv")
    calibration = read_csv("results/calibration/calibration_metric_point_estimates.csv")
    break_even = read_csv("results/operational_cost/break_even_cost_analysis.csv")
    attack_metrics = read_csv("results/attack_category/attack_category_operating_point_metrics.csv")
    multiseed_winners = read_csv("results/multiseed/multiseed_winner_frequency.csv")
    multiseed_thresholds = read_csv("results/multiseed/multiseed_threshold_stability.csv")

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

    key_bootstrap = [
        row
        for row in [*bootstrap_balanced, *bootstrap_security, *bootstrap_auc]
        if row["Metric"] in {"Precision", "Recall", "F1-score", "F2-score", "FPR", "FNR", "FN", "ROC-AUC", "PR-AUC"}
    ]
    write_table_pair(
        "table01_bootstrap_key_differences",
        key_bootstrap,
        ["Comparison", "Metric", "Point Estimate", "CI Lower", "CI Upper", "CI Interpretation"],
        "Paired bootstrap key differences",
    )

    write_table_pair(
        "table02_calibration_metrics",
        calibration,
        ["Model", "Selected Threshold", "Brier Score", "Log Loss", "ECE Uniform 15", "Adaptive ECE Quantile 15", "Calibration Intercept", "Calibration Slope"],
        "Calibration metrics for selected operating points",
    )

    write_table_pair(
        "table03_break_even_cost_analysis",
        break_even,
        ["Comparison", "Additional False Positives", "False Negatives Reduced", "Break-even FN to FP Cost Ratio", "Bootstrap CI Lower", "Bootstrap CI Upper"],
        "Break-even operational cost analysis",
    )

    key_categories = {"Infilteration", "Brute Force -Web", "SQL Injection"}
    key_attack_rows = [row for row in attack_metrics if row["Attack Category"] in key_categories]
    write_table_pair(
        "table04_key_attack_category_results",
        key_attack_rows,
        ["Attack Category", "Support", "Operating Point", "Threshold", "Detected", "Missed", "Detection Rate", "Detection Rate CI Lower", "Detection Rate CI Upper"],
        "Key attack-category detection results",
    )

    write_table_pair(
        "table05_multiseed_winner_frequency",
        multiseed_winners,
        ["Objective", "Selected Model", "Winner Count", "Winner Proportion"],
        "Multi-seed winner frequency",
    )

    write_table_pair(
        "table06_multiseed_threshold_stability",
        multiseed_thresholds,
        ["Model", "Objective", "Mean Threshold", "Threshold SD", "Minimum Threshold", "Maximum Threshold", "Median Threshold"],
        "Multi-seed threshold stability",
    )

    contribution_rows = [
        {
            "Analysis": "Bootstrap confidence",
            "Finding": next(row for row in bootstrap_balanced if row["Metric"] == "F1-score")["CI Interpretation"],
            "Source Artifact": "paired_balanced_model_differences.csv",
        },
        {
            "Analysis": "Calibration",
            "Finding": next(row for row in calibration if row["Model"] == "XGBoost Tuned")["Brier Score"],
            "Source Artifact": "calibration_metric_point_estimates.csv",
        },
        {
            "Analysis": "Operational cost",
            "Finding": next(row for row in break_even if row["Comparison"] == "LightGBM Security vs LightGBM Balanced")["Break-even FN to FP Cost Ratio"],
            "Source Artifact": "break_even_cost_analysis.csv",
        },
        {
            "Analysis": "Attack categories",
            "Finding": next(row for row in attack_metrics if row["Attack Category"] == "Infilteration" and row["Operating Point"] == "LightGBM Security")["Detection Rate"],
            "Source Artifact": "attack_category_operating_point_metrics.csv",
        },
        {
            "Analysis": "Multi-seed robustness",
            "Finding": next(row for row in multiseed_winners if row["Objective"] == "Security" and row["Selected Model"] == "LightGBM Tuned")["Winner Count"],
            "Source Artifact": "multiseed_winner_frequency.csv",
        },
    ]
    write_table_pair(
        "table07_final_contribution_summary",
        contribution_rows,
        ["Analysis", "Finding", "Source Artifact"],
        "Journal-extension contribution summary",
    )

    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Wrote journal-extension tables under {JOURNAL_TABLE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
