# Multi-Seed Robustness

## Purpose

This stage evaluates whether the final XGBoost and LightGBM
conclusions depend on the original random seed.

## Design

- Seeds: [42, 52, 62, 72, 82]
- Models: XGBoost Tuned and LightGBM Tuned
- Split per seed: 64% training, 16% validation, 20% holdout
- Balanced criterion: maximum validation F1
- Security criterion: maximum validation F2 subject to FPR ≤ 5%
- Holdout data were excluded from model and threshold selection.

The previously selected hyperparameter configurations were held
fixed. The complete hyperparameter search was not repeated for
every seed.

## Validation-selected winners

|   Seed | Objective   | Selected Model   |   Selected Threshold |   Validation F1 |   Validation F2 |   Test F1 |   Test F2 |   Test Recall |   Test FPR |
|-------:|:------------|:-----------------|---------------------:|----------------:|----------------:|----------:|----------:|--------------:|-----------:|
|     42 | Balanced    | LightGBM Tuned   |                 0.45 |        0.927186 |        0.896568 |  0.928351 |  0.89767  |      0.878318 |   0.009333 |
|     42 | Security    | LightGBM Tuned   |                 0.26 |        0.915102 |        0.907986 |  0.918448 |  0.911452 |      0.906847 |   0.045611 |
|     52 | Balanced    | XGBoost Tuned    |                 0.44 |        0.928104 |        0.897785 |  0.928519 |  0.899622 |      0.881336 |   0.011444 |
|     52 | Security    | LightGBM Tuned   |                 0.27 |        0.916109 |        0.908037 |  0.917951 |  0.910153 |      0.905028 |   0.044889 |
|     62 | Balanced    | LightGBM Tuned   |                 0.44 |        0.929757 |        0.900152 |  0.927397 |  0.898451 |      0.880137 |   0.012056 |
|     62 | Security    | LightGBM Tuned   |                 0.27 |        0.916407 |        0.908907 |  0.916072 |  0.909163 |      0.904614 |   0.047278 |
|     72 | Balanced    | XGBoost Tuned    |                 0.48 |        0.926661 |        0.893549 |  0.927916 |  0.895925 |      0.875796 |   0.007972 |
|     72 | Security    | XGBoost Tuned    |                 0.26 |        0.913473 |        0.907156 |  0.916021 |  0.910695 |      0.907178 |   0.049389 |
|     82 | Balanced    | XGBoost Tuned    |                 0.51 |        0.927119 |        0.893719 |  0.928535 |  0.896234 |      0.87592  |   0.007222 |
|     82 | Security    | LightGBM Tuned   |                 0.27 |        0.91392  |        0.906455 |  0.91715  |  0.910439 |      0.90602  |   0.046833 |

## Winner frequency

| Objective   | Selected Model   |   Winner Count |   Winner Proportion |
|:------------|:-----------------|---------------:|--------------------:|
| Balanced    | LightGBM Tuned   |              2 |                 0.4 |
| Balanced    | XGBoost Tuned    |              3 |                 0.6 |
| Security    | LightGBM Tuned   |              4 |                 0.8 |
| Security    | XGBoost Tuned    |              1 |                 0.2 |

## Threshold stability

| Model          | Objective   |   Mean Threshold |   Threshold SD |   Minimum Threshold |   Maximum Threshold |   Median Threshold |
|:---------------|:------------|-----------------:|---------------:|--------------------:|--------------------:|-------------------:|
| LightGBM Tuned | Balanced    |            0.436 |       0.026077 |                0.41 |                0.47 |               0.44 |
| LightGBM Tuned | Security    |            0.266 |       0.005477 |                0.26 |                0.27 |               0.27 |
| XGBoost Tuned  | Balanced    |            0.476 |       0.027019 |                0.44 |                0.51 |               0.48 |
| XGBoost Tuned  | Security    |            0.274 |       0.008944 |                0.26 |                0.28 |               0.28 |

## Limitations

This experiment measures robustness to random splitting and
model training while holding tuned hyperparameters fixed. It
does not measure uncertainty from repeating the complete
hyperparameter-search procedure or external-dataset
generalization.
