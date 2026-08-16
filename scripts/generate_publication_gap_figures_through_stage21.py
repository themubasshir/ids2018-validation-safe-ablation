
from pathlib import Path

import csv
import json
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Paths
# =============================================================================

REPO = Path(__file__).resolve().parents[1]

RESULTS = (
    REPO
    / "results"
)

FIGURES = (
    REPO
    / "figures"
)


STAGE16_SOURCE = (
    RESULTS
    / "stage16_classical_benchmark_checkpoint"
    / "stage16_6c_classical_vs_transformer_holdout_comparison.csv"
)

STAGE18_SOURCE = (
    RESULTS
    / "stage18_representation_feasibility_checkpoint"
    / "stage18_3l_final_graph_holdout_lock"
    / "stage18_3m_final_graph_holdout_freeze_record.json"
)

STAGE19_POOLED = (
    RESULTS
    / "stage19_mtemporal_checkpoint"
    / "stage19_7_temporal_experiment_closure"
    / "stage19_7_manuscript_results_table.csv"
)

STAGE19_DAILY = (
    RESULTS
    / "stage19_mtemporal_checkpoint"
    / "stage19_7_temporal_experiment_closure"
    / "stage19_7_per_day_results_table.csv"
)


OUT16 = (
    FIGURES
    / "stage16_classical_transformer"
)

OUT18 = (
    FIGURES
    / "stage18_graph"
)

OUT19 = (
    FIGURES
    / "stage19_temporal"
)


for directory in (
    OUT16,
    OUT18,
    OUT19,
):

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# =============================================================================
# Helpers
# =============================================================================

def read_csv(
    path,
):

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as fh:

        return list(
            csv.DictReader(
                fh
            )
        )


def save(
    fig,
    directory,
    stem,
):

    png = (
        directory
        /
        (
            stem
            +
            ".png"
        )
    )

    pdf = (
        directory
        /
        (
            stem
            +
            ".pdf"
        )
    )

    fig.savefig(
        png,
        dpi=600,
        bbox_inches="tight",
        facecolor="white",
    )

    fig.savefig(
        pdf,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(
        fig
    )

    return (
        png,
        pdf,
    )


def clean_axes(
    ax,
):

    ax.spines[
        "top"
    ].set_visible(
        False
    )

    ax.spines[
        "right"
    ].set_visible(
        False
    )

    ax.grid(
        axis="y",
        linestyle=":",
        linewidth=0.6,
        alpha=0.65,
        zorder=0,
    )


def annotate_bars(
    ax,
    containers,
    offset,
    fmt="{:.3f}",
):

    for container in containers:

        for bar in container:

            value = (
                bar.get_height()
            )

            ax.text(
                bar.get_x()
                +
                bar.get_width()
                /
                2,
                value
                +
                offset,
                fmt.format(
                    value
                ),
                ha="center",
                va="bottom",
                fontsize=6.6,
            )


# =============================================================================
# Typography
# =============================================================================

plt.rcParams.update(
    {
        "font.family":
            "serif",

        "font.serif":
            [
                "Times New Roman",
                "Times",
                "DejaVu Serif",
            ],

        "font.size":
            8.5,

        "axes.labelsize":
            9,

        "axes.titlesize":
            9,

        "xtick.labelsize":
            8,

        "ytick.labelsize":
            8,

        "legend.fontsize":
            8,

        "axes.linewidth":
            0.8,

        "pdf.fonttype":
            42,

        "ps.fonttype":
            42,
    }
)


# =============================================================================
# FIGURE 16-1
# Classical vs Transformer — exact same duplicate-safe holdout
# =============================================================================

rows16 = {
    row["metric"]:
        row
    for row in read_csv(
        STAGE16_SOURCE
    )
}


# Exact source integrity gates.
assert float(
    rows16[
        "f1"
    ][
        "classical_value"
    ]
) == 0.8805579773321709

assert float(
    rows16[
        "f1"
    ][
        "transformer_value"
    ]
) == 0.8660798222374156

assert float(
    rows16[
        "pr_auc"
    ][
        "classical_value"
    ]
) == 0.947391385608797

assert float(
    rows16[
        "pr_auc"
    ][
        "transformer_value"
    ]
) == 0.9287861970480663


metrics = [
    "precision",
    "recall",
    "f1",
    "mcc",
    "pr_auc",
    "roc_auc",
]

labels = [
    "Precision",
    "Recall",
    "F1",
    "MCC",
    "PR-AUC",
    "ROC-AUC",
]


classical = np.asarray(
    [
        float(
            rows16[m][
                "classical_value"
            ]
        )
        for m in metrics
    ]
)

transformer = np.asarray(
    [
        float(
            rows16[m][
                "transformer_value"
            ]
        )
        for m in metrics
    ]
)


classical_fpr = float(
    rows16[
        "fpr"
    ][
        "classical_value"
    ]
)

transformer_fpr = float(
    rows16[
        "fpr"
    ][
        "transformer_value"
    ]
)


fig, axes = plt.subplots(
    1,
    2,
    figsize=(
        7.16,
        3.05,
    ),
    gridspec_kw={
        "width_ratios":
            [
                4.2,
                1.15,
            ]
    },
)


x = np.arange(
    len(
        metrics
    )
)

w = 0.36


b1 = axes[0].bar(
    x - w / 2,
    classical,
    width=w,
    facecolor="white",
    edgecolor="black",
    linewidth=0.9,
    hatch="////",
    label="Classical ensemble",
    zorder=3,
)

b2 = axes[0].bar(
    x + w / 2,
    transformer,
    width=w,
    facecolor="0.62",
    edgecolor="black",
    linewidth=0.9,
    hatch="....",
    label="Transformer",
    zorder=3,
)


axes[0].set_xticks(
    x,
    labels,
    rotation=24,
    ha="right",
)

axes[0].set_ylim(
    0,
    1.08,
)

axes[0].set_ylabel(
    "Holdout metric value"
)

axes[0].set_title(
    "(a) Detection and discrimination",
    fontweight="bold",
)

clean_axes(
    axes[0]
)

annotate_bars(
    axes[0],
    [
        b1,
        b2,
    ],
    offset=0.018,
)


fpr_x = np.arange(
    2
)

fpr_bars = axes[1].bar(
    fpr_x,
    [
        classical_fpr,
        transformer_fpr,
    ],
    width=0.58,
    facecolor=[
        "white",
        "0.62",
    ],
    edgecolor="black",
    linewidth=0.9,
    hatch=[
        "////",
        "....",
    ],
    zorder=3,
)


axes[1].set_xticks(
    fpr_x,
    [
        "Classical",
        "Transformer",
    ],
    rotation=20,
    ha="right",
)

axes[1].set_ylim(
    0,
    0.012,
)

axes[1].set_ylabel(
    "False-positive rate"
)

axes[1].set_title(
    "(b) False-positive control",
    fontweight="bold",
)

clean_axes(
    axes[1]
)


for bar in fpr_bars:

    value = (
        bar.get_height()
    )

    axes[1].text(
        bar.get_x()
        +
        bar.get_width()
        /
        2,
        value
        +
        0.00028,
        f"{value:.4f}",
        ha="center",
        fontsize=7,
    )


fig.legend(
    [
        b1[0],
        b2[0],
    ],
    [
        "ENS_LGBM_XGB_EQUAL",
        "FT_BALANCED 5-checkpoint ensemble",
    ],
    loc="upper center",
    ncol=2,
    frameon=False,
    bbox_to_anchor=(
        0.5,
        1.02,
    ),
)


fig.subplots_adjust(
    left=0.085,
    right=0.99,
    bottom=0.23,
    top=0.79,
    wspace=0.28,
)


save(
    fig,
    OUT16,
    "fig16_1_classical_vs_transformer_holdout_tradeoff",
)


# =============================================================================
# FIGURE 18-1
# Graph ranking vs frozen operating-point divergence
# =============================================================================

stage18 = json.loads(
    STAGE18_SOURCE.read_text(
        encoding="utf-8"
    )
)


graph = stage18[
    "graph_transformer_final_holdout"
]

edge = stage18[
    "edgeonly_final_holdout"
]


assert graph[
    "pr_auc"
] == 0.9735953918848133

assert graph[
    "f1"
] == 0.0

assert graph[
    "recall"
] == 0.0

assert edge[
    "pr_auc"
] == 0.42976973171668154

assert edge[
    "f1"
] == 0.6559877841940602


fig, axes = plt.subplots(
    1,
    2,
    figsize=(
        7.16,
        3.0,
    ),
)


x = np.arange(
    2
)

w = 0.36


# Ranking panel
edge_rank = [
    edge[
        "pr_auc"
    ],
    edge[
        "roc_auc"
    ],
]

graph_rank = [
    graph[
        "pr_auc"
    ],
    graph[
        "roc_auc"
    ],
]


b1 = axes[0].bar(
    x - w / 2,
    edge_rank,
    width=w,
    facecolor="white",
    edgecolor="black",
    linewidth=0.9,
    hatch="////",
    label="EdgeOnlyMLP",
    zorder=3,
)

b2 = axes[0].bar(
    x + w / 2,
    graph_rank,
    width=w,
    facecolor="0.62",
    edgecolor="black",
    linewidth=0.9,
    hatch="....",
    label="Graph Transformer",
    zorder=3,
)


axes[0].set_xticks(
    x,
    [
        "PR-AUC",
        "ROC-AUC",
    ],
)

axes[0].set_ylim(
    0,
    1.08,
)

axes[0].set_ylabel(
    "Metric value"
)

axes[0].set_title(
    "(a) Threshold-free ranking",
    fontweight="bold",
)

clean_axes(
    axes[0]
)

annotate_bars(
    axes[0],
    [
        b1,
        b2,
    ],
    offset=0.02,
)


# Frozen threshold panel
edge_op = [
    edge[
        "f1"
    ],
    edge[
        "recall"
    ],
]

graph_op = [
    graph[
        "f1"
    ],
    graph[
        "recall"
    ],
]


c1 = axes[1].bar(
    x - w / 2,
    edge_op,
    width=w,
    facecolor="white",
    edgecolor="black",
    linewidth=0.9,
    hatch="////",
    zorder=3,
)

c2 = axes[1].bar(
    x + w / 2,
    graph_op,
    width=w,
    facecolor="0.62",
    edgecolor="black",
    linewidth=0.9,
    hatch="....",
    zorder=3,
)


axes[1].set_xticks(
    x,
    [
        "F1",
        "Recall",
    ],
)

axes[1].set_ylim(
    0,
    1.08,
)

axes[1].set_ylabel(
    "Metric value"
)

axes[1].set_title(
    r"(b) Frozen threshold $\theta=0.01$",
    fontweight="bold",
)

clean_axes(
    axes[1]
)

annotate_bars(
    axes[1],
    [
        c1,
        c2,
    ],
    offset=0.02,
)


# Explicit zero labels.
for bar in c2:

    axes[1].text(
        bar.get_x()
        +
        bar.get_width()
        /
        2,
        0.025,
        "0.000",
        ha="center",
        va="bottom",
        fontsize=6.6,
    )


fig.legend(
    [
        b1[0],
        b2[0],
    ],
    [
        "EdgeOnlyMLP",
        "Graph Transformer",
    ],
    loc="upper center",
    ncol=2,
    frameon=False,
    bbox_to_anchor=(
        0.5,
        1.02,
    ),
)


fig.text(
    0.5,
    0.015,
    (
        "High Graph Transformer ranking does not translate to useful "
        "detections at the independently frozen operating threshold."
    ),
    ha="center",
    fontsize=7.2,
    fontstyle="italic",
)


fig.subplots_adjust(
    left=0.085,
    right=0.985,
    bottom=0.16,
    top=0.79,
    wspace=0.22,
)


save(
    fig,
    OUT18,
    "fig18_1_graph_ranking_vs_frozen_operating_point",
)


# =============================================================================
# FIGURE 19-1
# MTemporal pooled result + chronological heterogeneity
# =============================================================================

pooled_rows = read_csv(
    STAGE19_POOLED
)

daily_rows = read_csv(
    STAGE19_DAILY
)


pooled = {
    row[
        "model"
    ]:
        row
    for row in pooled_rows
}


single_name = (
    "SingleScaleTemporalTransformer"
)

multi_name = (
    "MTemporal-IDS"
)


assert float(
    pooled[
        single_name
    ][
        "holdout_pr_auc"
    ]
) == 0.7599570946733909

assert float(
    pooled[
        multi_name
    ][
        "holdout_pr_auc"
    ]
) == 0.8013780402555105

assert float(
    pooled[
        single_name
    ][
        "f1"
    ]
) == 0.6526175687666371

assert float(
    pooled[
        multi_name
    ][
        "f1"
    ]
) == 0.7176209461958979


single_pooled = [
    float(
        pooled[
            single_name
        ][
            "holdout_pr_auc"
        ]
    ),
    float(
        pooled[
            single_name
        ][
            "f1"
        ]
    ),
    float(
        pooled[
            single_name
        ][
            "mcc"
        ]
    ),
]

multi_pooled = [
    float(
        pooled[
            multi_name
        ][
            "holdout_pr_auc"
        ]
    ),
    float(
        pooled[
            multi_name
        ][
            "f1"
        ]
    ),
    float(
        pooled[
            multi_name
        ][
            "mcc"
        ]
    ),
]


days = [
    "03-01-2018",
    "03-02-2018",
]


daily_lookup = {
    (
        row[
            "day"
        ],
        row[
            "model"
        ],
    ):
        row
    for row in daily_rows
}


attack_rates = [
    float(
        daily_lookup[
            (
                day,
                single_name,
            )
        ][
            "attack_rate"
        ]
    )
    for day in days
]


single_pr = [
    float(
        daily_lookup[
            (
                day,
                single_name,
            )
        ][
            "pr_auc"
        ]
    )
    for day in days
]

multi_pr = [
    float(
        daily_lookup[
            (
                day,
                multi_name,
            )
        ][
            "pr_auc"
        ]
    )
    for day in days
]


single_f1 = [
    float(
        daily_lookup[
            (
                day,
                single_name,
            )
        ][
            "f1"
        ]
    )
    for day in days
]

multi_f1 = [
    float(
        daily_lookup[
            (
                day,
                multi_name,
            )
        ][
            "f1"
        ]
    )
    for day in days
]


fig, axes = plt.subplots(
    1,
    3,
    figsize=(
        7.16,
        3.05,
    ),
)


w = 0.35


# Pooled
x0 = np.arange(
    3
)

p1 = axes[0].bar(
    x0 - w / 2,
    single_pooled,
    width=w,
    facecolor="white",
    edgecolor="black",
    linewidth=0.9,
    hatch="////",
    label="Single-scale",
    zorder=3,
)

p2 = axes[0].bar(
    x0 + w / 2,
    multi_pooled,
    width=w,
    facecolor="0.62",
    edgecolor="black",
    linewidth=0.9,
    hatch="....",
    label="MTemporal-IDS",
    zorder=3,
)


axes[0].set_xticks(
    x0,
    [
        "PR-AUC",
        "F1",
        "MCC",
    ],
)

axes[0].set_ylim(
    0,
    1.03,
)

axes[0].set_ylabel(
    "Metric value"
)

axes[0].set_title(
    "(a) Pooled chronological holdout",
    fontweight="bold",
    fontsize=8.2,
)

clean_axes(
    axes[0]
)

annotate_bars(
    axes[0],
    [
        p1,
        p2,
    ],
    offset=0.018,
)


# Per-day PR
xd = np.arange(
    2
)

day_labels = [
    (
        "Mar 1\n"
        +
        f"attack={attack_rates[0]*100:.1f}%"
    ),
    (
        "Mar 2\n"
        +
        f"attack={attack_rates[1]*100:.1f}%"
    ),
]


q1 = axes[1].bar(
    xd - w / 2,
    single_pr,
    width=w,
    facecolor="white",
    edgecolor="black",
    linewidth=0.9,
    hatch="////",
    zorder=3,
)

q2 = axes[1].bar(
    xd + w / 2,
    multi_pr,
    width=w,
    facecolor="0.62",
    edgecolor="black",
    linewidth=0.9,
    hatch="....",
    zorder=3,
)


axes[1].set_xticks(
    xd,
    day_labels,
)

axes[1].set_ylim(
    0,
    1.03,
)

axes[1].set_ylabel(
    "PR-AUC"
)

axes[1].set_title(
    "(b) Day-specific ranking",
    fontweight="bold",
    fontsize=8.2,
)

clean_axes(
    axes[1]
)

annotate_bars(
    axes[1],
    [
        q1,
        q2,
    ],
    offset=0.018,
)


# Per-day F1
r1 = axes[2].bar(
    xd - w / 2,
    single_f1,
    width=w,
    facecolor="white",
    edgecolor="black",
    linewidth=0.9,
    hatch="////",
    zorder=3,
)

r2 = axes[2].bar(
    xd + w / 2,
    multi_f1,
    width=w,
    facecolor="0.62",
    edgecolor="black",
    linewidth=0.9,
    hatch="....",
    zorder=3,
)


axes[2].set_xticks(
    xd,
    day_labels,
)

axes[2].set_ylim(
    0,
    1.03,
)

axes[2].set_ylabel(
    "F1"
)

axes[2].set_title(
    "(c) Day-specific operating behavior",
    fontweight="bold",
    fontsize=8.2,
)

clean_axes(
    axes[2]
)

annotate_bars(
    axes[2],
    [
        r1,
        r2,
    ],
    offset=0.018,
)


fig.legend(
    [
        p1[0],
        p2[0],
    ],
    [
        "Single-scale temporal Transformer",
        "MTemporal-IDS",
    ],
    loc="upper center",
    ncol=2,
    frameon=False,
    bbox_to_anchor=(
        0.5,
        1.025,
    ),
)


fig.subplots_adjust(
    left=0.075,
    right=0.99,
    bottom=0.22,
    top=0.77,
    wspace=0.30,
)


save(
    fig,
    OUT19,
    "fig19_1_mtemporal_pooled_and_daily_heterogeneity",
)


# =============================================================================
# Finished
# =============================================================================

print("THROUGH_STAGE21_GAP_FIGURES_GENERATION_PASS")
