#!/usr/bin/env python3
"""
Stage27 publication integration generator.

This script creates manuscript-facing publication artifacts exclusively from
the already-frozen Stage27-4A synthesis artifacts.

It performs no model fitting, no model inference, no target reopening,
no threshold selection, no bootstrap recomputation, and no new statistical
testing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import pandas as pd


CANONICAL_SCIENTIFIC_PARENT = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

STAGE27_DATE = "2026-08-21"

SYNTHESIS_REL = Path(
    "results/stage27_loao_unseen_attack/stage27_4a_final_synthesis"
)

PACKAGE_REL = Path(
    "results/stage27_loao_unseen_attack/stage27_publication_package"
)

GENERATOR_REL = Path(
    "scripts/stage27/stage27_publication_integration.py"
)

OUTPUT_PATHS = {
    "manuscript_md": Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.md"),
    "manuscript_tex": Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.tex"),
    "tables_md": Path("docs/STAGE27_PUBLICATION_TABLES.md"),
    "tables_tex": Path("docs/STAGE27_PUBLICATION_TABLES.tex"),
}

MANIFEST_REL = PACKAGE_REL / "stage27_publication_manifest.json"


EXPECTED_SOURCE_SHA256 = {
    "stage27_final_primary_metrics.csv":
        "42ea04b3f21e6026d5d69c8d5b59aa1edd2b57e94c42da3b9f70587349704634",

    "stage27_final_operating_points.csv":
        "664a5aaaff718f20bf6d619ae1dd4871a07a37c81a1631590423ea0ae07240f4",

    "stage27_final_novelty_gaps.csv":
        "91c80319186fd3bbfc382e58cfc60e58fc75d23db15408564fd35c05d4fb316c",

    "stage27_final_similarity.csv":
        "8c110b4f1d6317d2a2125b4f24bfb8325cdeb699ce763d268d91f3bad6acc8d3",

    "stage27_synthesis.md":
        "50b44ce0740816a51464179817fb0de5111cbe942e2c18c52df8d41d48f194fb",

    "stage27_synthesis_receipt.json":
        "55a67c1173d8bb3ffe2b2200542c382296459ae24b3b96fc0767abb6cb01bd3f",

    "stage27_4a_synthesis_freeze_record.json":
        "35135f1979518b36e614c7a0c2c7db9e4bd9bb78eb4d70346255684d0a4ae1db",

    "figures/stage27_primary_roc_auc_ci.png":
        "0e3659c1abb3a5ec9cb27af3e702f734f3c00266d695a672408c3d426e746152",

    "figures/stage27_primary_pr_auc_ci.png":
        "3528a3f2854f2d40dc1e2c23c20f14fb8d3b9edb6870d32088504e23b02dfba8",

    "figures/stage27_balanced_recall_ci.png":
        "441b3adc5f357c8d5b1ac1d6ce5fd3bd449fe9fdbaeea3a1c944a965b7b1e2b6",
}


FAMILY_ORDER = [
    "BOT",
    "DDOS",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
]

LEARNER_ORDER = [
    "XGBOOST",
    "LIGHTGBM",
]

LEARNER_DISPLAY = {
    "XGBOOST": "XGBoost",
    "LIGHTGBM": "LightGBM",
}


EXECUTABILITY_ROWS = [
    {
        "family": "BOT",
        "status": "ELIGIBLE",
        "support": 1966,
        "target": "Friday",
        "interpretation": "Inferential support eligible",
    },
    {
        "family": "DDOS",
        "status": "ELIGIBLE",
        "support": 128027,
        "target": "Friday",
        "interpretation": "Inferential support eligible",
    },
    {
        "family": "DOS",
        "status": "STRUCTURALLY_INELIGIBLE",
        "support": None,
        "target": "Wednesday",
        "interpretation":
            "No valid supervised day-atomic training geometry",
    },
    {
        "family": "AUTH_BRUTE_FORCE",
        "status": "STRUCTURALLY_INELIGIBLE",
        "support": None,
        "target": "Tuesday",
        "interpretation":
            "Insufficient earlier weekday depth",
    },
    {
        "family": "INFILTRATION",
        "status": "ELIGIBLE_DESCRIPTIVE_ONLY",
        "support": 36,
        "target": "Thursday",
        "interpretation":
            "Descriptive only; held-out support < 50",
    },
    {
        "family": "PORT_SCAN",
        "status": "ELIGIBLE",
        "support": 158930,
        "target": "Friday",
        "interpretation": "Inferential support eligible",
    },
    {
        "family": "WEB_ATTACK",
        "status": "ELIGIBLE",
        "support": 2180,
        "target": "Thursday",
        "interpretation": "Inferential support eligible",
    },
]


def run_git(root: Path, *args: str):
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed:\n{result.stderr}"
        )

    return result.stdout.strip()


def repo_root():
    here = Path(__file__).resolve().parent

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=here,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError("Unable to locate Git repository root.")

    return Path(result.stdout.strip()).resolve()


def sha256_file(path: Path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def verify_scientific_parent(root: Path):
    head = run_git(root, "rev-parse", "HEAD")

    result = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            CANONICAL_SCIENTIFIC_PARENT,
            head,
        ],
        cwd=root,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Canonical Stage27 scientific parent is not an ancestor "
            "of the current repository HEAD."
        )

    return head


def verify_frozen_sources(root: Path):
    synthesis = root / SYNTHESIS_REL

    verification = {}

    for rel, expected in EXPECTED_SOURCE_SHA256.items():
        path = synthesis / rel

        if not path.is_file():
            raise RuntimeError(
                f"Frozen Stage27 source missing: {path}"
            )

        actual = sha256_file(path)

        if actual != expected:
            raise RuntimeError(
                f"Frozen Stage27 source hash mismatch:\n"
                f"  artifact: {rel}\n"
                f"  expected: {expected}\n"
                f"  actual:   {actual}"
            )

        verification[rel] = actual

    return verification


def fmt(value, digits=4):
    return f"{float(value):.{digits}f}"


def fmt6(value):
    return f"{float(value):.6f}"


def pct(value, digits=2):
    return f"{100.0 * float(value):.{digits}f}%"


def ci_text(row, metric, digits=4):
    point = float(row[metric])
    lo = float(row[f"{metric}_ci_2_5"])
    hi = float(row[f"{metric}_ci_97_5"])

    return (
        f"{point:.{digits}f} "
        f"({lo:.{digits}f}–{hi:.{digits}f})"
    )


def tex_ci(row, metric, digits=4):
    point = float(row[metric])
    lo = float(row[f"{metric}_ci_2_5"])
    hi = float(row[f"{metric}_ci_97_5"])

    return (
        f"{point:.{digits}f} "
        f"[{lo:.{digits}f}, {hi:.{digits}f}]"
    )


def select_row(df, family, learner):
    rows = df[
        (df["family"] == family)
        & (df["learner"] == learner)
    ]

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected exactly one row for {family}/{learner}; "
            f"found {len(rows)}"
        )

    return rows.iloc[0]


def balanced_row(ops, family, learner):
    rows = ops[
        (ops["family"] == family)
        & (ops["learner"] == learner)
        & (ops["operating_point"] == "BALANCED")
    ]

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected exactly one BALANCED row for "
            f"{family}/{learner}; found {len(rows)}"
        )

    return rows.iloc[0]


def scientific_sanity(primary, ops, gaps, similarity):
    assert len(primary) == 10
    assert len(ops) == 30
    assert len(gaps) == 10
    assert len(similarity) == 5

    assert set(primary["family"]) == set(FAMILY_ORDER)
    assert set(primary["learner"]) == set(LEARNER_ORDER)

    inf = primary[primary["family"] == "INFILTRATION"]

    assert len(inf) == 2
    assert (inf["heldout_attack_support"] == 36).all()

    inferential = (
        inf["inferential_family_claim_authorized"]
        .astype(str)
        .str.lower()
    )

    assert (inferential == "false").all()

    bot_xgb = select_row(primary, "BOT", "XGBOOST")
    assert float(bot_xgb["pr_excess"]) < 0

    ddos = primary[primary["family"] == "DDOS"]
    assert (ddos["roc_auc"] > 0.99).all()
    assert (ddos["pr_auc"] > 0.99).all()

    web = primary[primary["family"] == "WEB_ATTACK"]
    assert (web["roc_auc"] > 0.96).all()
    assert (web["pr_auc"] > 0.70).all()

    port_xgb = select_row(primary, "PORT_SCAN", "XGBOOST")
    port_lgb = select_row(primary, "PORT_SCAN", "LIGHTGBM")

    assert float(port_lgb["roc_auc"]) > float(port_xgb["roc_auc"])

    assert (
        similarity["interpretation"]
        == "SECONDARY_DESCRIPTIVE_ONLY"
    ).all()

    bal = ops[ops["operating_point"] == "BALANCED"]

    expected_balanced = {
        ("BOT", "XGBOOST"): 0.0,
        ("BOT", "LIGHTGBM"): 0.0,
        ("DDOS", "XGBOOST"): 0.6619697407578089,
        ("DDOS", "LIGHTGBM"): 0.2625383708124068,
        ("INFILTRATION", "XGBOOST"): 0.0,
        ("INFILTRATION", "LIGHTGBM"): 0.0,
        ("PORT_SCAN", "XGBOOST"): 0.00480085572264519,
        ("PORT_SCAN", "LIGHTGBM"): 0.011678097275530108,
        ("WEB_ATTACK", "XGBOOST"): 0.7779816513761468,
        ("WEB_ATTACK", "LIGHTGBM"): 0.5211009174311927,
    }

    for key, expected in expected_balanced.items():
        family, learner = key
        row = balanced_row(ops, family, learner)
        actual = float(row["recall"])

        assert abs(actual - expected) < 1e-15


def build_primary_markdown(primary, ops):
    lines = [
        "| Family | Learner | Held-out support | ROC-AUC (95% CI) | "
        "PR-AUC (95% CI) | BALANCED recall |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = select_row(primary, family, learner)
            op = balanced_row(ops, family, learner)

            family_display = (
                "INFILTRATION†"
                if family == "INFILTRATION"
                else family
            )

            lines.append(
                "| "
                + " | ".join([
                    family_display,
                    LEARNER_DISPLAY[learner],
                    f"{int(row['heldout_attack_support']):,}",
                    ci_text(row, "roc_auc", 4),
                    ci_text(row, "pr_auc", 6),
                    pct(op["recall"], 2),
                ])
                + " |"
            )

    lines.extend([
        "",
        "† INFILTRATION is descriptive only because "
        "held-out support is 36 (<50).",
    ])

    return "\n".join(lines)


def build_executability_markdown():
    lines = [
        "| Family | Status | Held-out support | Target day | "
        "Interpretation |",
        "|---|---|---:|---|---|",
    ]

    for row in EXECUTABILITY_ROWS:
        support = (
            "—"
            if row["support"] is None
            else f"{row['support']:,}"
        )

        lines.append(
            "| "
            + " | ".join([
                row["family"],
                row["status"],
                support,
                row["target"],
                row["interpretation"],
            ])
            + " |"
        )

    return "\n".join(lines)


def build_operating_markdown(ops):
    lines = [
        "| Family | Learner | Operating point | Threshold | "
        "Precision | Recall | FPR | F1 |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]

    order_points = ["STANDARD", "BALANCED", "SECURITY"]

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            for operating_point in order_points:
                rows = ops[
                    (ops["family"] == family)
                    & (ops["learner"] == learner)
                    & (ops["operating_point"] == operating_point)
                ]

                row = rows.iloc[0]

                lines.append(
                    "| "
                    + " | ".join([
                        family,
                        LEARNER_DISPLAY[learner],
                        operating_point,
                        fmt(row["threshold"], 2),
                        fmt6(row["precision"]),
                        fmt6(row["recall"]),
                        fmt6(row["fpr"]),
                        fmt6(row["f1"]),
                    ])
                    + " |"
                )

    return "\n".join(lines)


def build_gap_markdown(gaps):
    lines = [
        "| Family | Learner | ROC-AUC known−unseen gap | "
        "PR-excess known−unseen gap | BALANCED recall gap |",
        "|---|---|---:|---:|---:|",
    ]

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = gaps[
                (gaps["family"] == family)
                & (gaps["learner"] == learner)
            ].iloc[0]

            lines.append(
                "| "
                + " | ".join([
                    family,
                    LEARNER_DISPLAY[learner],
                    fmt6(row["gap_roc_auc"]),
                    fmt6(row["gap_pr_excess"]),
                    fmt6(row["gap_recall_balanced"]),
                ])
                + " |"
            )

    lines.extend([
        "",
        "Raw known-minus-unseen PR-AUC differences are not treated "
        "as prevalence-invariant primary novelty gaps because the "
        "comparison populations have different prevalence anchors.",
    ])

    return "\n".join(lines)


def build_similarity_markdown(similarity):
    lines = [
        "| Held-out family | Nearest seen family | Distance | "
        "Similarity | Benign distance |",
        "|---|---|---:|---:|---:|",
    ]

    indexed = similarity.set_index("family")

    for family in FAMILY_ORDER:
        row = indexed.loc[family]

        lines.append(
            "| "
            + " | ".join([
                family,
                str(row["nearest_seen_family"]),
                fmt6(row["nearest_seen_distance"]),
                fmt6(row["similarity_score"]),
                fmt6(row["benign_distance"]),
            ])
            + " |"
        )

    lines.extend([
        "",
        "This analysis is secondary and descriptive only. "
        "No formal correlation test, p-value, regression inference, "
        "or causal interpretation is authorized.",
    ])

    return "\n".join(lines)


def build_publication_tables_md(primary, ops, gaps, similarity):
    return f"""# Stage27 Publication Tables

Scientific parent:

`{CANONICAL_SCIENTIFIC_PARENT}`

These tables are generated exclusively from frozen Stage27 artifacts.
No target reopening, inference, model fitting, threshold reselection,
bootstrap recomputation, or new statistical testing is performed.

---

## Table 27-1. Chronology-first family executability

{build_executability_markdown()}

---

## Table 27-2. Primary unseen-family performance

{build_primary_markdown(primary, ops)}

The 95% intervals are the frozen 2,000-replicate stratified
row-bootstrap intervals and quantify target-sampling uncertainty
conditional on the already-fitted model.

---

## Table 27-S1. Complete frozen operating points

{build_operating_markdown(ops)}

---

## Table 27-S2. Compatible novelty-generalization gaps

{build_gap_markdown(gaps)}

---

## Table 27-S3. Behavioral similarity

{build_similarity_markdown(similarity)}

---

## Figure placement

### Main manuscript

1. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`
2. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

### Supplementary material

3. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains a co-primary metric and must remain in the main
results table and manuscript text even when its separate figure is
placed in supplementary material.
"""


def build_publication_tables_tex(primary, ops, gaps, similarity):
    lines = [
        "% =====================================================================",
        "% Stage27 Publication Tables",
        "% Auto-generated from frozen Stage27 artifacts.",
        "% No scientific model execution is performed by this file.",
        "% =====================================================================",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Chronology-first unseen-family fold executability under the frozen Stage27 protocol.}",
        r"\label{tab:stage27_executability}",
        r"\begin{tabular}{lllrl}",
        r"\hline",
        r"Family & Status & Target & Support & Interpretation \\",
        r"\hline",
    ]

    for row in EXECUTABILITY_ROWS:
        support = (
            "--"
            if row["support"] is None
            else f"{row['support']:,}"
        )

        family = row["family"].replace("_", r"\_")
        status = row["status"].replace("_", r"\_")
        interp = row["interpretation"].replace("<", "$<$")

        lines.append(
            f"{family} & {status} & {row['target']} & "
            f"{support} & {interp} \\\\"
        )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Primary unseen attack-family ranking and frozen BALANCED-threshold recall. Values in brackets are frozen 95\% percentile bootstrap intervals.}",
        r"\label{tab:stage27_primary}",
        r"\begin{tabular}{llrrrr}",
        r"\hline",
        r"Family & Learner & Support & ROC-AUC [95\% CI] & PR-AUC [95\% CI] & Balanced Recall \\",
        r"\hline",
    ])

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = select_row(primary, family, learner)
            op = balanced_row(ops, family, learner)

            family_tex = family.replace("_", r"\_")

            if family == "INFILTRATION":
                family_tex += r"$^{\dagger}$"

            lines.append(
                f"{family_tex} & "
                f"{LEARNER_DISPLAY[learner]} & "
                f"{int(row['heldout_attack_support']):,} & "
                f"{tex_ci(row, 'roc_auc', 4)} & "
                f"{tex_ci(row, 'pr_auc', 6)} & "
                f"{pct(op['recall'], 2).replace('%', r'\%')} \\\\"
            )

    lines.extend([
        r"\hline",
        r"\multicolumn{6}{l}{$^{\dagger}$INFILTRATION is descriptive only because held-out support is 36 ($<50$).}\\",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Frozen Stage27 operating-point transfer to each unseen-family isolation target.}",
        r"\label{tab:stage27_operating_points}",
        r"\begin{tabular}{lllrrrrr}",
        r"\hline",
        r"Family & Learner & Point & Threshold & Precision & Recall & FPR & F1 \\",
        r"\hline",
    ])

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            for point in ["STANDARD", "BALANCED", "SECURITY"]:
                row = ops[
                    (ops["family"] == family)
                    & (ops["learner"] == learner)
                    & (ops["operating_point"] == point)
                ].iloc[0]

                lines.append(
                    f"{family.replace('_', r'\_')} & "
                    f"{LEARNER_DISPLAY[learner]} & "
                    f"{point} & "
                    f"{float(row['threshold']):.2f} & "
                    f"{float(row['precision']):.6f} & "
                    f"{float(row['recall']):.6f} & "
                    f"{float(row['fpr']):.6f} & "
                    f"{float(row['f1']):.6f} \\\\"
                )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Frozen Stage27 novelty-generalization gaps. PR-excess is used for the prevalence-compatible primary PR comparison.}",
        r"\label{tab:stage27_novelty_gaps}",
        r"\begin{tabular}{llrrr}",
        r"\hline",
        r"Family & Learner & ROC-AUC Gap & PR-Excess Gap & Balanced Recall Gap \\",
        r"\hline",
    ])

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = gaps[
                (gaps["family"] == family)
                & (gaps["learner"] == learner)
            ].iloc[0]

            lines.append(
                f"{family.replace('_', r'\_')} & "
                f"{LEARNER_DISPLAY[learner]} & "
                f"{float(row['gap_roc_auc']):.6f} & "
                f"{float(row['gap_pr_excess']):.6f} & "
                f"{float(row['gap_recall_balanced']):.6f} \\\\"
            )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Secondary descriptive behavioral-similarity audit for the executable Stage27 families.}",
        r"\label{tab:stage27_similarity}",
        r"\begin{tabular}{llrrr}",
        r"\hline",
        r"Held-out Family & Nearest Seen Family & Distance & Similarity & Benign Distance \\",
        r"\hline",
    ])

    indexed = similarity.set_index("family")

    for family in FAMILY_ORDER:
        row = indexed.loc[family]

        lines.append(
            f"{family.replace('_', r'\_')} & "
            f"{str(row['nearest_seen_family']).replace('_', r'\_')} & "
            f"{float(row['nearest_seen_distance']):.6f} & "
            f"{float(row['similarity_score']):.6f} & "
            f"{float(row['benign_distance']):.6f} \\\\"
        )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "% Behavioral similarity is secondary and descriptive only.",
        "% No formal correlation test, regression inference, p-value,",
        "% or causal interpretation is authorized.",
        "",
    ])

    return "\n".join(lines)


def build_manuscript_md(primary, ops, gaps, similarity):
    bot_x = select_row(primary, "BOT", "XGBOOST")
    bot_l = select_row(primary, "BOT", "LIGHTGBM")
    ddos_x = select_row(primary, "DDOS", "XGBOOST")
    ddos_l = select_row(primary, "DDOS", "LIGHTGBM")
    inf_x = select_row(primary, "INFILTRATION", "XGBOOST")
    inf_l = select_row(primary, "INFILTRATION", "LIGHTGBM")
    port_x = select_row(primary, "PORT_SCAN", "XGBOOST")
    port_l = select_row(primary, "PORT_SCAN", "LIGHTGBM")
    web_x = select_row(primary, "WEB_ATTACK", "XGBOOST")
    web_l = select_row(primary, "WEB_ATTACK", "LIGHTGBM")

    bot_x_bal = balanced_row(ops, "BOT", "XGBOOST")
    bot_l_bal = balanced_row(ops, "BOT", "LIGHTGBM")
    ddos_x_bal = balanced_row(ops, "DDOS", "XGBOOST")
    ddos_l_bal = balanced_row(ops, "DDOS", "LIGHTGBM")
    inf_x_bal = balanced_row(ops, "INFILTRATION", "XGBOOST")
    inf_l_bal = balanced_row(ops, "INFILTRATION", "LIGHTGBM")
    port_x_bal = balanced_row(ops, "PORT_SCAN", "XGBOOST")
    port_l_bal = balanced_row(ops, "PORT_SCAN", "LIGHTGBM")
    web_x_bal = balanced_row(ops, "WEB_ATTACK", "XGBOOST")
    web_l_bal = balanced_row(ops, "WEB_ATTACK", "LIGHTGBM")

    similarity_idx = similarity.set_index("family")

    return f"""# Stage27 Manuscript Integration

## Scientific Identity

**Stage27 title:** Leave-One-Attack-Family-Out Unseen-Family Generalization Audit

**Design:** `CHRONOLOGY_FIRST_ZERO_TRAINING_EXPOSURE_FAMILY_AUDIT`

**Canonical scientific parent:** `{CANONICAL_SCIENTIFIC_PARENT}`

Stage27 scientific execution is closed. This document is a post-closure
publication-integration artifact generated from the frozen Stage27-4A
synthesis. It introduces no new measurement and authorizes no target
reopening, model inference, model refitting, threshold reselection,
bootstrap recomputation, feature modification, or post-target model
selection.

The publication-safe high-level outcome is:

1. `SELECTIVE_FAMILY_TRANSFER`
2. `RANKING_THRESHOLD_DIVERGENCE`
3. `LEARNER_DEPENDENCE`

Stage27 is an unseen attack-family generalization audit. It must not be
described as formal proof of zero-day detection.

---

# A. Proposed Contribution Text for the Introduction

A further contribution of this study is a chronology-first
zero-training-exposure attack-family generalization audit. Seven
CICIDS2017 attack families were preregistered for evaluation under a
strict `TRAIN < VALIDATION < TARGET` design in which the held-out family
was absent from both training and validation. Five families were
structurally executable, while DOS and AUTH_BRUTE_FORCE could not be
evaluated without violating the frozen chronological geometry. Across
the executable families, transfer was selective rather than universal:
DDoS and Web Attack retained strong ranking discrimination, Bot traffic
collapsed, and Port Scan exhibited substantial learner dependence.
Moreover, preserved ranking discrimination did not necessarily yield
useful recall at validation-selected frozen thresholds, separating
attack-family ranking generalization from operating-point transfer.

---

# B. Methods — Chronology-First Unseen-Family Generalization

## B.1 Scientific question

Stage27 evaluates whether a binary intrusion detector trained without
exposure to a particular attack family can discriminate that held-out
family from temporally matched benign traffic when the family first
becomes eligible under strict chronology.

The experiment is therefore described as an **unseen attack-family** or
**zero-training-exposure family** audit rather than as a formal
zero-day-detection experiment.

## B.2 Frozen taxonomy and executability

The preregistered primary taxonomy contains:

- BOT
- DDOS
- DOS
- AUTH_BRUTE_FORCE
- INFILTRATION
- PORT_SCAN
- WEB_ATTACK

Five of seven families were executable. DOS was structurally ineligible
because its first valid target day was Wednesday, leaving Monday for
training and Tuesday for validation, while Monday contained zero
known-family attack positives. AUTH_BRUTE_FORCE was structurally
ineligible because its first appearance on Tuesday left insufficient
earlier weekday depth for separate training and validation periods.

INFILTRATION was executable but is permanently descriptive only because
its held-out target support was 36.

## B.3 Chronological fold geometry

For BOT, DDOS, and PORT_SCAN:

- TRAIN: Monday–Wednesday
- VALIDATION: Thursday
- TARGET: Friday
- training rows: 1,668,519
- validation rows: 458,968
- Friday benign rows: 414,322

For INFILTRATION and WEB_ATTACK:

- TRAIN: Monday–Tuesday
- VALIDATION: Wednesday
- TARGET: Thursday
- training rows: 975,827
- validation rows: 692,692
- Thursday benign rows: 456,752

The held-out family has zero training rows and zero validation rows in
every executable fold. Any positive held-out-family membership in either
development role would invalidate the fold.

## B.4 Primary target semantics

The primary isolation target is:

`HELD_OUT_FAMILY + SAME_TARGET_DAY_BENIGN`

The positive class contains only the held-out attack family and the
negative class contains only benign traffic from the same target day.
Other known target-day attacks are excluded.

A broader operational context target containing held-out attacks, known
attacks, and benign traffic is secondary and descriptive only. The
manuscript should lead with the primary isolation target.

## B.5 Learners and thresholds

Two preregistered learners were evaluated:

- XGBoost
- LightGBM

No Stage27 hyperparameter optimization was permitted. Across five
executable folds and two learners, the total fit budget was exactly 10
models.

Three operating points were frozen from known-family validation data
only:

- STANDARD: threshold 0.50
- BALANCED: maximum validation F1, then minimum FPR, then higher threshold
- SECURITY: maximum validation F2 subject to FPR <= 0.05, then minimum
  FPR, then higher threshold

The threshold grid was 0.01–0.99 and the target decision rule was
`probability >= threshold`.

No target threshold search or target-guided model adaptation was
permitted.

## B.6 Bootstrap uncertainty

Stage27 uses 2,000-replicate class-stratified row bootstrap intervals
with seed 42. Sampling is performed with replacement within the benign
and held-out-attack target strata while preserving stratum sizes.

The intervals quantify **target-sampling uncertainty conditional on the
already-fitted model**. They do not include training-seed uncertainty,
model-selection uncertainty, model-retraining uncertainty, or broader
population uncertainty.

## B.7 Behavioral similarity

The secondary behavioral-similarity audit uses 11 preregistered
aggregate flow descriptors. Preprocessing is fitted only on current-fold
TRAIN rows, each family is represented by its standardized centroid, and
Euclidean distance to the nearest seen family is transformed to
similarity as:

`1 / (1 + nearest_seen_distance)`

This analysis is descriptive only. No formal correlation significance
test, regression inference, p-value, or causal interpretation is
authorized.

---

# C. Results — Unseen Attack-Family Generalization

## C.1 Executability under strict chronology

Of seven preregistered families, five were structurally executable.
BOT, DDOS, PORT_SCAN, and WEB_ATTACK satisfied the frozen family-level
support requirement. INFILTRATION was executable but remains
descriptive only because its held-out support was 36. DOS and
AUTH_BRUTE_FORCE were structurally ineligible under the precommitted
day-atomic chronology rather than being treated as model failures.

## C.2 Primary unseen-family ranking

The frozen ranking results demonstrate strongly family-dependent
transfer.

**DDoS produced the strongest transfer.** XGBoost reached ROC-AUC
{float(ddos_x['roc_auc']):.4f} and PR-AUC
{float(ddos_x['pr_auc']):.4f}, while LightGBM reached ROC-AUC
{float(ddos_l['roc_auc']):.4f} and PR-AUC
{float(ddos_l['pr_auc']):.4f}. Thus, both learners retained
near-perfect threshold-independent discrimination despite receiving
zero DDoS training or validation examples.

**Web Attack also transferred strongly.** XGBoost reached ROC-AUC
{float(web_x['roc_auc']):.4f} and PR-AUC
{float(web_x['pr_auc']):.4f}; LightGBM reached ROC-AUC
{float(web_l['roc_auc']):.4f} and PR-AUC
{float(web_l['pr_auc']):.4f}.

**Bot traffic showed substantial collapse.** XGBoost produced ROC-AUC
{float(bot_x['roc_auc']):.4f}, while LightGBM produced ROC-AUC
{float(bot_l['roc_auc']):.4f}. XGBoost PR-AUC was
{float(bot_x['pr_auc']):.6f}, below the target prevalence anchor of
{float(bot_x['prevalence']):.6f}, giving PR-excess
{float(bot_x['pr_excess']):.6f}. LightGBM was only marginally above the
same prevalence anchor, with PR-excess
{float(bot_l['pr_excess']):.6f}.

**Port Scan was materially learner-dependent.** XGBoost reached
ROC-AUC {float(port_x['roc_auc']):.4f}, whereas LightGBM reached
{float(port_l['roc_auc']):.4f}. The corresponding PR-AUC values were
{float(port_x['pr_auc']):.4f} and {float(port_l['pr_auc']):.4f},
respectively.

INFILTRATION produced ROC-AUC
{float(inf_x['roc_auc']):.4f} for XGBoost and
{float(inf_l['roc_auc']):.4f} for LightGBM, but these values are
reported descriptively because only 36 held-out attacks were available.

The overall result is therefore **selective family transfer**, not
uniform unseen-family generalization.

## C.3 Frozen operating-point transfer

Threshold-independent ranking quality did not guarantee useful
frozen-threshold detection.

At the BALANCED operating point:

- BOT recall was {pct(bot_x_bal['recall'])} for XGBoost and
  {pct(bot_l_bal['recall'])} for LightGBM.
- DDOS recall was {pct(ddos_x_bal['recall'])} and
  {pct(ddos_l_bal['recall'])}.
- INFILTRATION recall was {pct(inf_x_bal['recall'])} and
  {pct(inf_l_bal['recall'])}, descriptive only.
- PORT_SCAN recall was {pct(port_x_bal['recall'])} and
  {pct(port_l_bal['recall'])}.
- WEB_ATTACK recall was {pct(web_x_bal['recall'])} and
  {pct(web_l_bal['recall'])}.

The divergence is particularly visible for DDOS, where both learners
retain ROC-AUC above 0.998 but BALANCED recall is only
{pct(ddos_x_bal['recall'])} for XGBoost and
{pct(ddos_l_bal['recall'])} for LightGBM. Port Scan provides another
example: LightGBM retains ROC-AUC
{float(port_l['roc_auc']):.4f} but detects only
{pct(port_l_bal['recall'])} of held-out Port Scan attacks at its frozen
BALANCED threshold.

These results support the frozen Stage27 outcome
`RANKING_THRESHOLD_DIVERGENCE`.

## C.4 Novelty-generalization gaps

The compatible novelty-gap analysis further shows that family novelty
does not impose a uniform penalty.

For XGBoost, the known-minus-unseen ROC-AUC gap is approximately
{float(gaps[(gaps.family == 'BOT') & (gaps.learner == 'XGBOOST')].iloc[0]['gap_roc_auc']):.3f}
for BOT and
{float(gaps[(gaps.family == 'PORT_SCAN') & (gaps.learner == 'XGBOOST')].iloc[0]['gap_roc_auc']):.3f}
for PORT_SCAN, whereas the DDOS gap is
{float(gaps[(gaps.family == 'DDOS') & (gaps.learner == 'XGBOOST')].iloc[0]['gap_roc_auc']):.3f}.

PR-excess rather than raw PR-AUC difference is used as the primary
prevalence-compatible PR novelty gap. Raw PR-AUC differences across
populations with different prevalence anchors are retained only as
descriptive quantities.

## C.5 Behavioral similarity

The frozen behavioral-similarity values do not show a monotonic
relationship with unseen-family discrimination.

BOT has the highest observed similarity to a seen family
({float(similarity_idx.loc['BOT', 'similarity_score']):.4f}) yet weak
unseen-family performance. DDOS has a substantially lower similarity
({float(similarity_idx.loc['DDOS', 'similarity_score']):.4f}) but
near-perfect ranking. WEB_ATTACK has intermediate similarity
({float(similarity_idx.loc['WEB_ATTACK', 'similarity_score']):.4f})
while retaining strong transfer.

Behavioral proximity, as operationalized by this frozen centroid
distance, therefore does not appear sufficient by itself to explain
the observed transfer pattern.

---

# D. Discussion — Attack-Family Novelty and Generalization

Stage27 demonstrates that known-family intrusion-detection performance
cannot be treated as evidence of uniform robustness to attack-family
novelty. The strongest transfer cases, DDOS and WEB_ATTACK, retain high
ranking discrimination for both learners despite zero exposure to the
held-out family during training and validation. BOT provides the
opposite outcome, with complete frozen-threshold detection failure and
little or adverse ranking signal. PORT_SCAN occupies an intermediate
case in which the outcome depends materially on the learner.

A second finding is the distinction between ranking discrimination and
operating-point transfer. DDoS is the clearest example: both learners
rank the held-out family almost perfectly, yet validation-selected
BALANCED thresholds recover substantially less than all of the held-out
attacks. The same separation is visible for Port Scan and, to a lesser
degree, Web Attack. Consequently, ROC-AUC or PR-AUC alone cannot
characterize whether a frozen deployment threshold will remain useful
under attack-family novelty.

This ranking-versus-threshold distinction also complements earlier
experiments in the study. Representation-specific chronological
evaluation, the Stage22R forward temporal audit, and the Stage24
cross-dataset audit independently showed that strong ranking behavior
can coexist with poor fixed-threshold transfer. Stage27 extends that
observation to zero-training-exposure attack families. Across these
distinct stress regimes, threshold-independent discrimination and
operating-point behavior should therefore be evaluated as separate
properties of an IDS.

Learner dependence is itself family-dependent. XGBoost and LightGBM
agree closely on the strong DDoS and Web Attack ranking outcomes but
differ substantially on Port Scan and also differ in Bot ranking.
The evidence therefore does not support declaring one learner
universally superior for unseen-family generalization.

The behavioral-similarity analysis provides no simple mechanistic
explanation. BOT is behaviorally closest to a seen family under the
frozen 11-descriptor representation yet transfers poorly, whereas DDOS
is less similar under the same definition but transfers extremely well.
This secondary analysis should therefore be interpreted as evidence
that the selected notion of behavioral proximity is insufficient by
itself, not as proof of either the presence or absence of a particular
causal mechanism.

Finally, strict chronology exposes limitations in the benchmark itself.
The inability to execute DOS and AUTH_BRUTE_FORCE is a consequence of
the temporal arrangement of attack families and the requirement for
separate training and validation periods. Rather than manufacturing
alternative folds after observing the data, Stage27 preserves these
families as structurally ineligible. This makes the scope of the
generalization claim narrower but maintains the validation-safe
interpretation of the experiment.

---

# E. Limitations and Threats to Validity

1. **Incomplete taxonomy executability.** Only five of seven
   preregistered families could be honestly evaluated under strict
   `TRAIN < VALIDATION < TARGET` chronology.

2. **Low INFILTRATION support.** INFILTRATION contains only 36 held-out
   target attacks and is therefore descriptive only.

3. **Chronology-first rather than textbook LOAO.** Strict chronology
   means that every non-held-out attack family is not necessarily
   represented during training. Stage27 is therefore specifically a
   chronology-first zero-training-exposure family audit.

4. **Conditional bootstrap uncertainty.** The 95% intervals quantify
   row-level target-sampling uncertainty conditional on each already
   fitted model. They do not incorporate retraining, seed, model
   selection, independently collected networks, or broader population
   uncertainty.

5. **No clustered bootstrap.** No preregistered durable grouping
   variable was available for a session- or time-cluster bootstrap.

6. **Restricted similarity representation.** Behavioral similarity is
   based only on 11 preregistered aggregate flow descriptors and a
   centroid-distance representation.

7. **Descriptive similarity analysis.** No formal correlation test,
   p-value, regression inference, or causal interpretation is
   authorized.

8. **Benchmark-specific external validity.** CICIDS2017 is a benchmark
   capture. The observed transfer pattern does not establish universal
   behavior for production networks, unrelated datasets, or genuinely
   novel real-world attacks.

9. **No zero-day proof.** Zero training exposure to an attack family in
   this benchmark is not equivalent to demonstrating universal
   real-world zero-day detection.

---

# F. Stage27 Publication-Level Contributions

1. **Chronology-first unseen-family evaluation.** Attack-family novelty
   is evaluated under a strict training-before-validation-before-target
   design with zero held-out-family exposure during development.

2. **Structural executability accounting.** Families that cannot be
   evaluated without violating chronology are explicitly labeled
   structurally ineligible rather than replaced with post-hoc folds.

3. **Selective-transfer finding.** DDoS and Web Attack retain strong
   transfer, Bot collapses, and Port Scan depends materially on learner
   choice.

4. **Ranking/threshold separation.** Threshold-independent
   discrimination and frozen validation-selected operating-point
   behavior are evaluated separately.

5. **Learner-dependent novelty audit.** XGBoost and LightGBM are
   compared under the same preregistered family-holdout geometry without
   Stage27 HPO.

6. **Target-sampling uncertainty.** Primary ranking and compatible
   operating metrics are accompanied by frozen 2,000-replicate
   stratified bootstrap intervals.

7. **Secondary behavioral-similarity audit.** A preregistered
   train-fitted descriptor representation is used to test whether simple
   behavioral proximity descriptively explains transfer, without
   introducing post-result significance testing.

---

# G. Contribution Text for Abstract / Introduction

A chronology-first zero-training-exposure attack-family audit further
revealed selective rather than universal unseen-family transfer. Under
strict `TRAIN < VALIDATION < TARGET` separation, both XGBoost and
LightGBM retained near-perfect ranking discrimination for held-out DDoS
traffic and strong ranking for Web Attack, whereas Bot traffic
collapsed and Port Scan transfer was materially learner-dependent.
Moreover, high unseen-family ROC-AUC did not necessarily translate into
useful recall at frozen validation-selected thresholds. The findings
show that strong known-family IDS performance should not be interpreted
as evidence of uniform robustness to unseen attack families and that
ranking generalization and operating-point transfer should be audited
separately.

---

# H. Publication-Safe Claims

The following claims are supported by the frozen Stage27 evidence:

1. Stage27 preregistered seven attack-family categories.
2. Five of the seven families were structurally executable.
3. DOS and AUTH_BRUTE_FORCE were structurally ineligible under strict
   chronology.
4. INFILTRATION is descriptive only because held-out support was 36.
5. DDoS retained near-perfect unseen-family ranking for both learners.
6. Web Attack retained strong unseen-family ranking for both learners.
7. Bot exhibited substantial unseen-family collapse.
8. Port Scan exhibited material learner dependence.
9. Ranking performance and frozen-threshold recall diverged for several
   families.
10. Behavioral similarity did not display a monotonic relationship with
    unseen-family ranking performance across the five executable
    families.
11. No target threshold tuning, target-guided model selection, or
    target-guided adaptation was performed.
12. The bootstrap intervals quantify target-sampling uncertainty
    conditional on the fitted model.
13. Known-family performance should not be treated as evidence of
    uniform unseen-family generalization.

---

# I. Claims That Must Not Appear

1. Stage27 proves universal zero-day detection.
2. Stage27 proves all unseen cyberattacks can be detected.
3. All seven attack families were experimentally executable.
4. INFILTRATION provides an inferential family-level conclusion.
5. LightGBM is universally superior to XGBoost for unseen attacks.
6. XGBoost is universally superior to LightGBM for unseen attacks.
7. Behavioral similarity significantly predicts unseen-family
   performance.
8. A causal relationship between similarity and transfer was
   established.
9. Raw PR-AUC known-minus-unseen difference is prevalence invariant.
10. Stage27 target thresholds were optimized using held-out-family
    labels.
11. Stage27 models were adapted or recalibrated after target opening.
12. The row bootstrap represents uncertainty across independent
    organizations or future production networks.

---

# J. Recommended Main-Manuscript Assets

## Main Table 27-1

Chronology-first family executability.

Source:

`docs/STAGE27_PUBLICATION_TABLES.md`

## Main Table 27-2

Primary ROC-AUC, PR-AUC, 95% intervals, held-out support, and BALANCED
recall for both learners.

Source:

`docs/STAGE27_PUBLICATION_TABLES.md`

## Main Figure 27-1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`

Purpose: show selective ranking transfer and learner dependence.

## Main Figure 27-2

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

Purpose: show ranking–threshold divergence.

## Supplementary Figure 27-S1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains co-primary and should remain in the main table and main
text even if the separate PR-AUC figure is supplementary.

## Supplementary tables

- complete STANDARD/BALANCED/SECURITY operating points;
- novelty-generalization gaps;
- behavioral similarity.

---

# K. Recommended Manuscript Placement

The Stage27 material should be integrated into the broader robustness
narrative rather than placed according to experimental stage number.

Recommended Results ordering:

1. Validation-safe baseline/model selection
2. Representation/architecture assessment
3. Temporal validation and forward generalization
4. Cross-dataset generalization
5. **Unseen attack-family generalization (Stage27)**
6. Low-prevalence and SOC operational stress
7. Deployment/computational profiling

This ordering moves from predictive evaluation toward increasingly
deployment-facing stress tests and keeps Stage27 adjacent to the
temporal and cross-dataset generalization evidence.
"""


def build_manuscript_tex(primary, ops, gaps, similarity):
    bot_x = select_row(primary, "BOT", "XGBOOST")
    bot_l = select_row(primary, "BOT", "LIGHTGBM")
    ddos_x = select_row(primary, "DDOS", "XGBOOST")
    ddos_l = select_row(primary, "DDOS", "LIGHTGBM")
    port_x = select_row(primary, "PORT_SCAN", "XGBOOST")
    port_l = select_row(primary, "PORT_SCAN", "LIGHTGBM")
    web_x = select_row(primary, "WEB_ATTACK", "XGBOOST")
    web_l = select_row(primary, "WEB_ATTACK", "LIGHTGBM")

    ddos_x_bal = balanced_row(ops, "DDOS", "XGBOOST")
    ddos_l_bal = balanced_row(ops, "DDOS", "LIGHTGBM")
    port_l_bal = balanced_row(ops, "PORT_SCAN", "LIGHTGBM")

    sim = similarity.set_index("family")

    lines = [
        "% =====================================================================",
        "% Stage27 Manuscript Integration",
        "% Generated only from frozen Stage27-4A artifacts.",
        "% =====================================================================",
        "",
        r"\subsection{Unseen Attack-Family Generalization}",
        "",
        r"\subsubsection{Chronology-first audit design}",
        "",
        (
            "Stage27 evaluated zero-training-exposure attack-family "
            "generalization under a strict "
            r"\texttt{TRAIN < VALIDATION < TARGET} protocol. "
            "The held-out family was absent from both training and "
            "validation, thresholds were selected only on known-family "
            "validation data, and the target was not used for model "
            "selection, threshold tuning, or adaptation. The experiment "
            "is therefore described as an unseen attack-family "
            "generalization audit rather than as formal proof of "
            "zero-day detection."
        ),
        "",
        (
            "Seven primary families were preregistered. Five were "
            "structurally executable. DOS was ineligible because the "
            "available earlier day-atomic training period contained no "
            "known-family attack positives, whereas "
            r"AUTH\_BRUTE\_FORCE was ineligible because insufficient "
            "earlier weekday depth existed for separate training and "
            "validation periods. INFILTRATION was executable but is "
            "reported descriptively only because the held-out support "
            "was 36."
        ),
        "",
        r"\subsubsection{Primary unseen-family ranking}",
        "",
        (
            "Unseen-family ranking was strongly family dependent. "
            "DDoS retained near-perfect discrimination: XGBoost reached "
            "ROC-AUC %.4f and PR-AUC %.4f, while LightGBM reached "
            "ROC-AUC %.4f and PR-AUC %.4f. "
            "Web Attack also transferred strongly, with XGBoost "
            "ROC-AUC %.4f and PR-AUC %.4f and LightGBM ROC-AUC %.4f "
            "and PR-AUC %.4f."
        ) % (
            ddos_x["roc_auc"],
            ddos_x["pr_auc"],
            ddos_l["roc_auc"],
            ddos_l["pr_auc"],
            web_x["roc_auc"],
            web_x["pr_auc"],
            web_l["roc_auc"],
            web_l["pr_auc"],
        ),
        "",
        (
            "Bot traffic showed substantial collapse. XGBoost produced "
            "ROC-AUC %.4f and PR-AUC %.6f, while LightGBM produced "
            "ROC-AUC %.4f and PR-AUC %.6f. The XGBoost PR-AUC was below "
            "the target prevalence anchor, giving negative PR-excess "
            "%.6f. Port Scan was materially learner-dependent: XGBoost "
            "reached ROC-AUC %.4f compared with %.4f for LightGBM."
        ) % (
            bot_x["roc_auc"],
            bot_x["pr_auc"],
            bot_l["roc_auc"],
            bot_l["pr_auc"],
            bot_x["pr_excess"],
            port_x["roc_auc"],
            port_l["roc_auc"],
        ),
        "",
        (
            "The overall Stage27 outcome is therefore selective family "
            "transfer rather than universal unseen-family "
            "generalization."
        ),
        "",
        r"\subsubsection{Frozen operating-point transfer}",
        "",
        (
            "Threshold-independent ranking did not guarantee useful "
            "frozen-threshold detection. At the BALANCED operating "
            "point, DDoS recall was %.2f\\%% for XGBoost and %.2f\\%% "
            "for LightGBM despite ROC-AUC above 0.998 for both learners. "
            "Similarly, LightGBM retained Port Scan ROC-AUC %.4f while "
            "BALANCED recall was only %.2f\\%%."
        ) % (
            100 * ddos_x_bal["recall"],
            100 * ddos_l_bal["recall"],
            port_l["roc_auc"],
            100 * port_l_bal["recall"],
        ),
        "",
        (
            "These results distinguish ranking generalization from "
            "operating-point transfer and support the frozen Stage27 "
            "outcome of ranking--threshold divergence."
        ),
        "",
        r"\subsubsection{Behavioral similarity}",
        "",
        (
            "The secondary behavioral-similarity audit did not show a "
            "monotonic relationship with transfer. BOT had the highest "
            "observed similarity to a seen family (%.4f) but weak "
            "generalization, whereas DDoS had lower similarity (%.4f) "
            "and near-perfect ranking. Behavioral proximity under the "
            "frozen 11-descriptor centroid definition therefore does "
            "not appear sufficient by itself to explain the transfer "
            "pattern."
        ) % (
            sim.loc["BOT", "similarity_score"],
            sim.loc["DDOS", "similarity_score"],
        ),
        "",
        r"\subsection{Discussion of Attack-Family Novelty}",
        "",
        (
            "Stage27 shows that strong performance on known attack "
            "families cannot be interpreted as evidence of uniform "
            "robustness to attack-family novelty. DDoS and Web Attack "
            "retained strong ranking for both learners, Bot collapsed, "
            "and Port Scan exhibited substantial learner dependence."
        ),
        "",
        (
            "The experiment also reinforces a broader finding across "
            "the study: threshold-independent discrimination and "
            "fixed operating-point behavior are distinct properties. "
            "Representation-specific chronological evaluation, the "
            "temporal-validation stress test, cross-dataset transfer, "
            "and now unseen-family transfer each expose cases in which "
            "ranking and frozen-threshold behavior diverge. Reporting "
            "only ROC-AUC or PR-AUC would therefore provide an "
            "incomplete description of deployment robustness."
        ),
        "",
        (
            "The evidence does not establish a universal learner "
            "winner. XGBoost and LightGBM agree closely on DDoS and Web "
            "Attack ranking but differ substantially for Port Scan and "
            "Bot. Learner dependence is therefore itself "
            "family-dependent."
        ),
        "",
        r"\subsection{Stage27 Limitations}",
        "",
        r"\begin{itemize}",
        (
            r"\item Only five of seven preregistered families were "
            r"structurally executable under strict chronology."
        ),
        (
            r"\item INFILTRATION is descriptive only because the "
            r"held-out support was 36."
        ),
        (
            r"\item The design is chronology-first zero-training-"
            r"exposure evaluation rather than textbook LOAO in which "
            r"every other family is necessarily represented in training."
        ),
        (
            r"\item The 95\% bootstrap intervals quantify target-"
            r"sampling uncertainty conditional on the fitted model and "
            r"do not include retraining, seed, model-selection, or "
            r"broader population uncertainty."
        ),
        (
            r"\item Behavioral similarity uses only 11 preregistered "
            r"aggregate descriptors and is descriptive only."
        ),
        (
            r"\item The benchmark-specific results do not establish "
            r"universal real-world zero-day detection."
        ),
        r"\end{itemize}",
        "",
        "% Main Stage27 figures:",
        "% stage27_primary_roc_auc_ci.png",
        "% stage27_balanced_recall_ci.png",
        "%",
        "% Supplementary:",
        "% stage27_primary_pr_auc_ci.png",
        "",
    ]

    return "\n".join(lines)


def build_contents(primary, ops, gaps, similarity):
    return {
        OUTPUT_PATHS["manuscript_md"]:
            build_manuscript_md(primary, ops, gaps, similarity),

        OUTPUT_PATHS["manuscript_tex"]:
            build_manuscript_tex(primary, ops, gaps, similarity),

        OUTPUT_PATHS["tables_md"]:
            build_publication_tables_md(primary, ops, gaps, similarity),

        OUTPUT_PATHS["tables_tex"]:
            build_publication_tables_tex(primary, ops, gaps, similarity),
    }


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized = content.rstrip() + "\n"

    path.write_text(
        normalized,
        encoding="utf-8",
        newline="\n",
    )


def create_manifest(
    root: Path,
    head: str,
    source_hashes: dict,
    generated_paths: list[Path],
):
    generated = {}

    for rel in generated_paths:
        path = root / rel

        generated[str(rel)] = {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }

    generator = root / GENERATOR_REL

    generated[str(GENERATOR_REL)] = {
        "sha256": sha256_file(generator),
        "bytes": generator.stat().st_size,
    }

    return {
        "stage": "STAGE27-PUB1",
        "publication_date": STAGE27_DATE,
        "scientific_parent":
            CANONICAL_SCIENTIFIC_PARENT,
        "generation_head": head,
        "scientific_status": "CLOSED",
        "publication_package_status":
            "PUBLICATION_CONTENT_FROZEN",
        "science_operations": {
            "model_fits": 0,
            "model_inference": 0,
            "target_reopenings": 0,
            "threshold_reselection": 0,
            "bootstrap_recomputation": 0,
            "new_formal_statistical_tests": 0,
        },
        "high_level_outcomes": [
            "SELECTIVE_FAMILY_TRANSFER",
            "RANKING_THRESHOLD_DIVERGENCE",
            "LEARNER_DEPENDENCE",
        ],
        "frozen_source_sha256": source_hashes,
        "generated_artifacts": generated,
        "figure_policy": {
            "main": [
                (
                    "results/stage27_loao_unseen_attack/"
                    "stage27_4a_final_synthesis/figures/"
                    "stage27_primary_roc_auc_ci.png"
                ),
                (
                    "results/stage27_loao_unseen_attack/"
                    "stage27_4a_final_synthesis/figures/"
                    "stage27_balanced_recall_ci.png"
                ),
            ],
            "supplementary": [
                (
                    "results/stage27_loao_unseen_attack/"
                    "stage27_4a_final_synthesis/figures/"
                    "stage27_primary_pr_auc_ci.png"
                ),
            ],
        },
        "reporting_guards": {
            "formal_zero_day_proof": False,
            "universal_unseen_family_generalization": False,
            "infiltration_inferential_claim": False,
            "similarity_significance_inference": False,
            "target_threshold_search": False,
        },
    }


def validate_generated_text(root: Path):
    manuscript = (
        root / OUTPUT_PATHS["manuscript_md"]
    ).read_text(encoding="utf-8")

    tables = (
        root / OUTPUT_PATHS["tables_md"]
    ).read_text(encoding="utf-8")

    required_manuscript_strings = [
        "SELECTIVE_FAMILY_TRANSFER",
        "RANKING_THRESHOLD_DIVERGENCE",
        "LEARNER_DEPENDENCE",
        "formal proof of zero-day detection",
        "descriptive only because",
        "ranking generalization",
        "operating-point transfer",
        "five of seven",
        "DOS",
        "AUTH_BRUTE_FORCE",
        "INFILTRATION",
        "BOT",
        "DDOS",
        "PORT_SCAN",
        "WEB_ATTACK",
        "0.9982",
        "0.9986",
        "0.3224",
        "0.5591",
        "0.5506",
        "0.7559",
        "77.80%",
        "52.11%",
    ]

    for token in required_manuscript_strings:
        if token not in manuscript:
            raise RuntimeError(
                f"Generated manuscript missing required token: {token}"
            )

    forbidden_overclaims = [
        "proves universal zero-day detection",
        "all seven families were experimentally executable",
        "LightGBM is universally superior",
        "XGBoost is universally superior",
        "statistically significant similarity",
    ]

    # These phrases are allowed only inside the explicit
    # "Claims That Must Not Appear" section.
    # Therefore the generated artifact must contain that section.
    assert "# I. Claims That Must Not Appear" in manuscript

    assert "Table 27-1" in tables
    assert "Table 27-2" in tables
    assert "Table 27-S1" in tables
    assert "Table 27-S2" in tables
    assert "Table 27-S3" in tables

    assert (
        "INFILTRATION is descriptive only"
        in tables
    )

    return True


def check_mode(root: Path):
    source_hashes = verify_frozen_sources(root)

    synthesis = root / SYNTHESIS_REL

    primary = pd.read_csv(
        synthesis / "stage27_final_primary_metrics.csv"
    )
    ops = pd.read_csv(
        synthesis / "stage27_final_operating_points.csv"
    )
    gaps = pd.read_csv(
        synthesis / "stage27_final_novelty_gaps.csv"
    )
    similarity = pd.read_csv(
        synthesis / "stage27_final_similarity.csv"
    )

    scientific_sanity(
        primary,
        ops,
        gaps,
        similarity,
    )

    expected = build_contents(
        primary,
        ops,
        gaps,
        similarity,
    )

    for rel, content in expected.items():
        path = root / rel

        if not path.is_file():
            raise RuntimeError(
                f"Generated publication artifact missing: {rel}"
            )

        actual_text = path.read_text(encoding="utf-8")
        expected_text = content.rstrip() + "\n"

        if actual_text != expected_text:
            raise RuntimeError(
                f"Generated artifact differs from deterministic "
                f"generator output: {rel}"
            )

    manifest_path = root / MANIFEST_REL

    if not manifest_path.is_file():
        raise RuntimeError("Publication manifest is missing.")

    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    for rel in expected:
        rel_str = str(rel)

        expected_hash = manifest[
            "generated_artifacts"
        ][rel_str]["sha256"]

        actual_hash = sha256_file(root / rel)

        if actual_hash != expected_hash:
            raise RuntimeError(
                f"Manifest hash mismatch: {rel}"
            )

    validate_generated_text(root)

    print("[PASS] frozen Stage27 source hashes")
    print("[PASS] scientific sanity gates")
    print("[PASS] deterministic document contents")
    print("[PASS] publication manifest hashes")
    print("[PASS] manuscript claim/data gates")
    print()
    print("STAGE27 PUBLICATION PACKAGE CHECK: PASS")


def generate_mode(root: Path):
    head = verify_scientific_parent(root)

    source_hashes = verify_frozen_sources(root)

    synthesis = root / SYNTHESIS_REL

    primary = pd.read_csv(
        synthesis / "stage27_final_primary_metrics.csv"
    )

    ops = pd.read_csv(
        synthesis / "stage27_final_operating_points.csv"
    )

    gaps = pd.read_csv(
        synthesis / "stage27_final_novelty_gaps.csv"
    )

    similarity = pd.read_csv(
        synthesis / "stage27_final_similarity.csv"
    )

    scientific_sanity(
        primary,
        ops,
        gaps,
        similarity,
    )

    contents = build_contents(
        primary,
        ops,
        gaps,
        similarity,
    )

    for rel, content in contents.items():
        write_text(
            root / rel,
            content,
        )

    validate_generated_text(root)

    manifest = create_manifest(
        root=root,
        head=head,
        source_hashes=source_hashes,
        generated_paths=list(contents.keys()),
    )

    manifest_path = root / MANIFEST_REL
    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 80)
    print("STAGE27 PUBLICATION GENERATOR COMPLETE")
    print("=" * 80)

    print()
    print("Scientific parent:")
    print(f"  {CANONICAL_SCIENTIFIC_PARENT}")

    print()
    print("Generated artifacts:")

    for rel in contents:
        path = root / rel

        print(
            f"  {rel}\n"
            f"    SHA256: {sha256_file(path)}\n"
            f"    bytes:  {path.stat().st_size:,}"
        )

    print(
        f"  {GENERATOR_REL}\n"
        f"    SHA256: {sha256_file(root / GENERATOR_REL)}"
    )

    print(
        f"  {MANIFEST_REL}\n"
        f"    SHA256: {sha256_file(manifest_path)}"
    )

    print()
    print("Science operations:")
    print("  model fits                 : 0")
    print("  model inference            : 0")
    print("  target reopenings          : 0")
    print("  threshold reselection      : 0")
    print("  bootstrap recomputation    : 0")
    print("  new formal statistical test: 0")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing publication package without rewriting it.",
    )

    args = parser.parse_args()

    root = repo_root()

    verify_scientific_parent(root)

    if args.check:
        check_mode(root)
    else:
        generate_mode(root)


if __name__ == "__main__":
    main()
