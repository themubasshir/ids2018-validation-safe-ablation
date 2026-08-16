
from pathlib import Path

import json
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Repository paths
# =============================================================================

REPO = Path(__file__).resolve().parents[1]

RESULTS = (
    REPO
    / "results"
    / "stage21_architecture"
)

FIG_DIR = (
    REPO
    / "figures"
    / "stage21_architecture"
)

FIG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


COMPARISON_JSON = (
    RESULTS
    / "stage21_5_cnn_vit_descriptive_comparison.json"
)

BOOTSTRAP_NPY = (
    RESULTS
    / "stage21_5_paired_bootstrap_deltas.npy"
)

XAI_JSON = (
    RESULTS
    / "stage21_xai1b_integrated_gradients_result.json"
)


comparison = json.loads(
    COMPARISON_JSON.read_text(
        encoding="utf-8"
    )
)

xai = json.loads(
    XAI_JSON.read_text(
        encoding="utf-8"
    )
)

bootstrap = np.load(
    BOOTSTRAP_NPY,
    allow_pickle=False,
)


assert bootstrap.shape == (
    10000,
    2,
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


def save_figure(
    fig,
    stem,
):

    png = (
        FIG_DIR
        /
        f"{stem}.png"
    )

    pdf = (
        FIG_DIR
        /
        f"{stem}.pdf"
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

    plt.close(fig)

    return png, pdf


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


# =============================================================================
# FIGURE 21-1
# CNN vs ViT ranking performance
# =============================================================================

metrics = [
    "ROC-AUC",
    "PR-AUC",
]


# Frozen upstream Stage20 Thursday comparator.
thursday_cnn = np.asarray(
    [
        0.9295057078625447,
        0.0656836038689915,
    ],
    dtype=np.float64,
)


# Frozen Stage21-3 Thursday ViT.
thursday_vit = np.asarray(
    [
        0.973370120580421,
        0.23477059852366194,
    ],
    dtype=np.float64,
)


primary = comparison[
    "co_primary_descriptive"
]


friday_cnn = np.asarray(
    [
        primary[
            "CNN_ROC_AUC"
        ],
        primary[
            "CNN_PR_AUC"
        ],
    ],
    dtype=np.float64,
)


friday_vit = np.asarray(
    [
        primary[
            "ViT_ROC_AUC"
        ],
        primary[
            "ViT_PR_AUC"
        ],
    ],
    dtype=np.float64,
)


assert np.isclose(
    friday_vit[0]
    -
    friday_cnn[0],
    primary[
        "ViT_MINUS_CNN_ROC_AUC"
    ],
)

assert np.isclose(
    friday_vit[1]
    -
    friday_cnn[1],
    primary[
        "ViT_MINUS_CNN_PR_AUC"
    ],
)


fig, axes = plt.subplots(
    1,
    2,
    figsize=(
        7.16,
        3.05,
    ),
    sharey=True,
)


x = np.arange(
    2
)

width = 0.34


def ranking_panel(
    ax,
    cnn,
    vit,
    title,
    subtitle=None,
):

    b1 = ax.bar(
        x - width / 2,
        cnn,
        width,
        label="CNN",
        facecolor="white",
        edgecolor="black",
        linewidth=0.9,
        hatch="////",
        zorder=3,
    )

    b2 = ax.bar(
        x + width / 2,
        vit,
        width,
        label="ViT",
        facecolor="0.62",
        edgecolor="black",
        linewidth=0.9,
        hatch="....",
        zorder=3,
    )

    ax.set_xticks(
        x,
        metrics,
    )

    ax.set_ylim(
        0,
        1.08,
    )

    ax.set_yticks(
        np.arange(
            0,
            1.01,
            0.2,
        )
    )

    ax.set_title(
        title,
        fontweight="bold",
        pad=8,
    )

    if subtitle:

        ax.text(
            0.5,
            1.005,
            subtitle,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=7.1,
            fontstyle="italic",
        )

    clean_axes(
        ax
    )

    for bars in (
        b1,
        b2,
    ):

        for bar in bars:

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
                0.021,
                f"{value:.3f}",
                ha="center",
                fontsize=7.2,
            )

    return b1, b2


bars = ranking_panel(
    axes[0],
    thursday_cnn,
    thursday_vit,
    "(a) Thursday validation",
)


ranking_panel(
    axes[1],
    friday_cnn,
    friday_vit,
    "(b) Friday locked-reuse benchmark",
    "descriptive / non-confirmatory",
)


axes[0].set_ylabel(
    "Ranking metric value"
)


fig.legend(
    [
        bars[0][0],
        bars[1][0],
    ],
    [
        "CNN (Stage20 comparator)",
        "ViT (Stage21)",
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
    right=0.985,
    bottom=0.17,
    top=0.79,
    wspace=0.18,
)


save_figure(
    fig,
    "fig21_1_cnn_vit_ranking_comparison",
)


# =============================================================================
# FIGURE 21-2
# Frozen paired bootstrap distributions
# =============================================================================

targets = comparison[
    "paired_bootstrap"
][
    "targets"
]


roc_observed = targets[
    "DELTA_ROC_AUC"
][
    "observed"
]

roc_ci = targets[
    "DELTA_ROC_AUC"
][
    "percentile_95_CI"
]


pr_observed = targets[
    "DELTA_PR_AUC"
][
    "observed"
]

pr_ci = targets[
    "DELTA_PR_AUC"
][
    "percentile_95_CI"
]


fig, axes = plt.subplots(
    1,
    2,
    figsize=(
        7.16,
        3.0,
    ),
)


bootstrap_specs = [
    (
        bootstrap[
            :,
            0
        ],
        roc_observed,
        roc_ci,
        r"(a) $\Delta$ROC-AUC",
    ),
    (
        bootstrap[
            :,
            1
        ],
        pr_observed,
        pr_ci,
        r"(b) $\Delta$PR-AUC",
    ),
]


for ax, (
    values,
    observed,
    ci,
    title,
) in zip(
    axes,
    bootstrap_specs,
):

    ax.hist(
        values,
        bins=45,
        density=True,
        facecolor="0.78",
        edgecolor="black",
        linewidth=0.45,
    )

    ax.axvline(
        observed,
        linestyle="-",
        linewidth=1.35,
        color="black",
        label="Observed",
    )

    ax.axvline(
        ci[0],
        linestyle="--",
        linewidth=1.0,
        color="black",
        label="95% percentile CI",
    )

    ax.axvline(
        ci[1],
        linestyle="--",
        linewidth=1.0,
        color="black",
    )

    ax.axvline(
        0,
        linestyle=":",
        linewidth=0.9,
        color="black",
    )

    ax.set_title(
        title,
        fontweight="bold",
    )

    ax.set_xlabel(
        "ViT − CNN"
    )

    clean_axes(
        ax
    )

    ax.text(
        0.03,
        0.96,
        (
            f"Observed = {observed:.4f}\n"
            f"95% CI = [{ci[0]:.4f}, {ci[1]:.4f}]"
        ),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=7.4,
        bbox=dict(
            facecolor="white",
            edgecolor="0.55",
            linewidth=0.5,
            boxstyle="round,pad=0.25",
        ),
    )


axes[0].set_ylabel(
    "Bootstrap density"
)


handles, labels = (
    axes[0]
    .get_legend_handles_labels()
)


fig.legend(
    handles[:2],
    labels[:2],
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
    right=0.985,
    bottom=0.18,
    top=0.79,
    wspace=0.22,
)


save_figure(
    fig,
    "fig21_2_paired_bootstrap_auc_deltas",
)


# =============================================================================
# FIGURE 21-3
# Frozen Friday operating points
# =============================================================================

secondary = comparison[
    "secondary_descriptive_deltas"
]


panels = [
    {
        "title":
            "(a) Standard threshold",

        "subtitle":
            r"$\theta_{\mathrm{CNN}}=\theta_{\mathrm{ViT}}=0.50$",

        "metrics":
            [
                "F1",
                "Recall",
            ],

        "cnn":
            [
                secondary[
                    "STANDARD_0_50_F1"
                ][
                    "CNN"
                ],
                secondary[
                    "STANDARD_0_50_RECALL"
                ][
                    "CNN"
                ],
            ],

        "vit":
            [
                secondary[
                    "STANDARD_0_50_F1"
                ][
                    "ViT"
                ],
                secondary[
                    "STANDARD_0_50_RECALL"
                ][
                    "ViT"
                ],
            ],
    },

    {
        "title":
            "(b) Validation-selected balanced",

        "subtitle":
            r"CNN $\theta=0.17$; ViT $\theta=0.42$",

        "metrics":
            [
                "F1",
                "Recall",
            ],

        "cnn":
            [
                secondary[
                    "VALIDATION_SELECTED_BALANCED_F1"
                ][
                    "CNN"
                ],
                secondary[
                    "VALIDATION_SELECTED_BALANCED_RECALL"
                ][
                    "CNN"
                ],
            ],

        "vit":
            [
                secondary[
                    "VALIDATION_SELECTED_BALANCED_F1"
                ][
                    "ViT"
                ],
                secondary[
                    "VALIDATION_SELECTED_BALANCED_RECALL"
                ][
                    "ViT"
                ],
            ],
    },

    {
        "title":
            "(c) Validation-selected security",

        "subtitle":
            r"CNN $\theta=0.17$; ViT $\theta=0.24$",

        "metrics":
            [
                "F2",
                "Recall",
            ],

        "cnn":
            [
                secondary[
                    "VALIDATION_SELECTED_SECURITY_F2"
                ][
                    "CNN"
                ],
                secondary[
                    "VALIDATION_SELECTED_SECURITY_RECALL"
                ][
                    "CNN"
                ],
            ],

        "vit":
            [
                secondary[
                    "VALIDATION_SELECTED_SECURITY_F2"
                ][
                    "ViT"
                ],
                secondary[
                    "VALIDATION_SELECTED_SECURITY_RECALL"
                ][
                    "ViT"
                ],
            ],
    },
]


fig, axes = plt.subplots(
    1,
    3,
    figsize=(
        7.16,
        2.85,
    ),
    sharey=True,
)


for panel_index, (
    ax,
    panel,
) in enumerate(
    zip(
        axes,
        panels,
    )
):

    xpos = np.arange(
        2
    )

    width = 0.34


    cnn = ax.bar(
        xpos
        -
        width / 2,
        panel[
            "cnn"
        ],
        width,
        facecolor="white",
        edgecolor="black",
        linewidth=0.9,
        hatch="////",
        label="CNN",
        zorder=3,
    )

    vit = ax.bar(
        xpos
        +
        width / 2,
        panel[
            "vit"
        ],
        width,
        facecolor="0.62",
        edgecolor="black",
        linewidth=0.9,
        hatch="....",
        label="ViT",
        zorder=3,
    )


    ax.set_xticks(
        xpos,
        panel[
            "metrics"
        ],
    )

    ax.set_ylim(
        0,
        0.165,
    )


    ax.set_title(
        panel[
            "title"
        ],
        fontweight="bold",
        fontsize=8.2,
        pad=11,
    )


    ax.text(
        0.5,
        1.01,
        panel[
            "subtitle"
        ],
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=6.8,
    )


    clean_axes(
        ax
    )


    for bars in (
        cnn,
        vit,
    ):

        for bar in bars:

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
                0.004,
                f"{value:.3f}",
                ha="center",
                fontsize=6.7,
            )


axes[0].set_ylabel(
    "Friday metric value"
)


fig.legend(
    [
        axes[0].patches[0],
        axes[0].patches[2],
    ],
    [
        "CNN",
        "ViT",
    ],
    loc="upper center",
    ncol=2,
    frameon=False,
    bbox_to_anchor=(
        0.5,
        1.03,
    ),
)


fig.subplots_adjust(
    left=0.09,
    right=0.99,
    bottom=0.18,
    top=0.72,
    wspace=0.20,
)


save_figure(
    fig,
    "fig21_3_friday_frozen_operating_points",
)


# =============================================================================
# FIGURE 21-4
# Frozen Integrated Gradients numerical-completeness diagnostic
#
# Uses already-persisted descriptive summaries only.
# No new XAI calculation.
# No quality threshold is introduced.
# =============================================================================

desc = xai[
    "descriptive_by_true_class"
]


categories = [
    (
        "CNN\nBENIGN",
        desc[
            "CNN"
        ][
            "TRUE_BENIGN"
        ][
            "IG_RELATIVE_COMPLETENESS_ERROR"
        ],
    ),

    (
        "CNN\nATTACK",
        desc[
            "CNN"
        ][
            "TRUE_ATTACK"
        ][
            "IG_RELATIVE_COMPLETENESS_ERROR"
        ],
    ),

    (
        "ViT\nBENIGN",
        desc[
            "ViT"
        ][
            "TRUE_BENIGN"
        ][
            "IG_RELATIVE_COMPLETENESS_ERROR"
        ],
    ),

    (
        "ViT\nATTACK",
        desc[
            "ViT"
        ][
            "TRUE_ATTACK"
        ][
            "IG_RELATIVE_COMPLETENESS_ERROR"
        ],
    ),
]


labels = [
    item[0]
    for item in categories
]


medians = np.asarray(
    [
        item[1][
            "median"
        ]
        for item in categories
    ],
    dtype=np.float64,
)


q25 = np.asarray(
    [
        item[1][
            "q25"
        ]
        for item in categories
    ],
    dtype=np.float64,
)


q75 = np.asarray(
    [
        item[1][
            "q75"
        ]
        for item in categories
    ],
    dtype=np.float64,
)


assert np.all(
    q25
    <=
    medians
)

assert np.all(
    medians
    <=
    q75
)


lower = (
    medians
    -
    q25
)

upper = (
    q75
    -
    medians
)


fig, ax = plt.subplots(
    figsize=(
        5.25,
        3.0,
    )
)


xpos = np.arange(
    len(
        labels
    )
)


ax.errorbar(
    xpos,
    medians,
    yerr=np.vstack(
        [
            lower,
            upper,
        ]
    ),
    fmt="o",
    markersize=5,
    capsize=5,
    linewidth=1.1,
    color="black",
    ecolor="black",
)


ax.set_xticks(
    xpos,
    labels,
)


ax.set_ylabel(
    "Relative IG completeness error"
)


ax.set_title(
    "64-step midpoint Integrated Gradients numerical-completeness diagnostic",
    fontweight="bold",
)


clean_axes(
    ax
)


upper_limit = max(
    0.40,
    float(
        np.max(
            q75
        )
        *
        1.18
    ),
)


ax.set_ylim(
    0,
    upper_limit,
)


for i, median in enumerate(
    medians
):

    ax.text(
        i,
        q75[i]
        +
        upper_limit
        *
        0.035,
        f"median={median:.3f}",
        ha="center",
        va="bottom",
        fontsize=7,
    )


ax.text(
    0.99,
    0.97,
    (
        "Point = median; whisker = IQR\n"
        "Lower is better\n"
        "No post-result quality threshold introduced"
    ),
    transform=ax.transAxes,
    ha="right",
    va="top",
    fontsize=7.2,
    bbox=dict(
        facecolor="white",
        edgecolor="0.55",
        linewidth=0.5,
        boxstyle="round,pad=0.25",
    ),
)


fig.subplots_adjust(
    left=0.15,
    right=0.98,
    bottom=0.20,
    top=0.84,
)


save_figure(
    fig,
    "fig21_4_ig_completeness_quality",
)


# =============================================================================
# Completion
# =============================================================================

print("FIGURE_GENERATION_PASS")

for path in sorted(
    FIG_DIR.glob(
        "fig21_*"
    )
):

    print(path)
