# Stage21-4 — Friday Locked Reuse Benchmark

## Status

**FRIDAY ViT REUSE BENCHMARK EVALUATED ONCE WITH NO SELECTION**

Friday remains a **locked reuse benchmark / non-confirmatory evaluation**.

No model, representation, join, or operating point is selected from this result.

## Population

- flows: **12,088**
- BENIGN: **6,486**
- ATTACK: **5,602**

## Score metrics

- ROC-AUC: **0.568693970029**
- PR-AUC: **0.606536911289**

## Frozen operating points

| Role | Threshold | TP | FN | TN | FP | Precision | Recall | F1 | F2 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Standard | 0.50 | 420 | 5182 | 6482 | 4 | 0.990566038 | 0.074973224 | 0.139395951 | 0.091976174 | 0.000616713 |
| Balanced | 0.42 | 421 | 5181 | 6481 | 5 | 0.988262911 | 0.075151732 | 0.139681486 | 0.092187089 | 0.000770891 |
| Security | 0.24 | 425 | 5177 | 6480 | 6 | 0.986078886 | 0.075865762 | 0.140891762 | 0.093042603 | 0.000925069 |

## Integrity boundary

- Friday ViT inference passes: **1**
- Friday threshold grid: **NO**
- threshold search: **NO**
- threshold reselection: **NO**
- retraining: **NO**
- optimizer steps: **0**

## Next

Stage21-5 performs the preregistered descriptive CNN-vs-ViT comparison and
paired 10,000-replicate flow-level bootstrap.

It does not alter the model or operating points.
