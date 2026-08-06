# Stage 14 — Integrated Gradients Analysis

## Scope

This directory contains the complete Stage 14 Integrated Gradients
analysis for the archived validation-selected MLP and one-dimensional
CNN checkpoints.

The models were not retrained. The original repository StandardScaler,
seed-42 data split, model checkpoints, and validation-selected operating
threshold of 0.50 were preserved.

Base repository commit before packaging:

`b689d21e96d0097f7eccfc37815f4e7cad337d52`

## Holdout performance

| Model | Accuracy | Precision | Recall | F1 | FPR | FNR | ROC-AUC |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MLP | 0.9395 | 0.9952 | 0.8536 | 0.9189 | 0.0028 | 0.1464 | 0.9668 |
| CNN | 0.9370 | 0.9899 | 0.8520 | 0.9158 | 0.0058 | 0.1480 | 0.9630 |

## Integrated Gradients configuration

- Attribution target: pre-sigmoid attack logit
- Integration method: trapezoidal rule over a straight-line path
- Integration steps: 128
- Primary baseline: mean attribution over 32 deterministic benign
  training references
- Case panel: 64 model-specific cases
- Cases per architecture and outcome: 8 TP, 8 TN, 8 FP, and 8 FN
- Numerical completeness passes: 64/64

The 128-step setting was selected through an explicit convergence audit
covering 16, 32, 64, and 128 integration steps.

## Reference-reliability results

| Reliability classification | Cases | Rate |
| --- | --- | --- |
| Reference-robust | 10 | 15.6% |
| Moderately reference-stable | 29 | 45.3% |
| Reference-sensitive | 25 | 39.1% |

Twenty-two of the 64 explanations had at least one benign reference that
produced a negatively oriented attribution vector relative to the mean
multi-reference explanation.

No false-negative case from either neural architecture satisfied every
study-specific reference-robustness criterion.

## Cross-model feature agreement

- Shared top-10 features: 6
- Top-10 Jaccard similarity: 0.4286
- Absolute-importance cosine:
  0.9107
- Signed-attribution cosine:
  0.7906

Shared top-10 features:

Bwd Pkt Len Std, ECE Flag Cnt, Fwd Pkt Len Max, Fwd Pkt Len Std, Fwd Seg Size Min, Init Fwd Win Byts

The high absolute-importance cosine indicates broad agreement in feature
magnitude, while the lower signed cosine and moderate top-10 overlap show
meaningful architectural differences in feature ranking and direction.

## Reporting decision

Aggregate recurring feature patterns are the primary neural explanation
result.

Individual cases should be handled as follows:

- Reference-robust cases may be shown directly.
- Moderately stable cases require an explicit sensitivity caveat.
- Reference-sensitive cases should remain supplementary diagnostics.

Numerical completeness must not be presented as evidence of baseline or
reference invariance.

## CNN interpretation boundary

The CNN operates over a fixed ordered vector of 78 tabular features.
Integrated Gradients measures sensitivity to those feature positions but
does not establish meaningful spatial locality between adjacent features.

## Directory structure

- `publication_assets/figures/`: manuscript-ready figures
- `publication_assets/tables/`: CSV and LaTeX tables
- `publication_assets/text/`: formal findings and manuscript paragraphs
- Root-level CSV/JSON/NPZ files: full numerical results, diagnostics,
  attribution archives, case panels, and metadata
- `checksums.sha256`: SHA-256 checksums for packaged files
- `stage14_repository_package_manifest.json`: package-level provenance
  and integrity metadata
