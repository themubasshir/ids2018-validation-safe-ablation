# Stage21-5 — CNN vs ViT Descriptive Comparison

## Status

**PREREGISTERED STAGE21 ARCHITECTURE COMPARISON COMPLETE**

Friday remains a **locked reuse benchmark / non-confirmatory evaluation**.

No architecture, model, epoch, threshold, representation, or join rule was
selected from Friday or from the bootstrap analysis.

## Population

- flows: **12,088**
- BENIGN: **6,486**
- ATTACK: **5,602**
- pairing unit: **flow**
- score order: exact common Friday compact-corpus export order

## Co-primary descriptive ranking comparison

| Metric | Stage20 CNN | Stage21 ViT | ViT − CNN |
|---|---:|---:|---:|
| ROC-AUC | 0.439214008080 | 0.568693970029 | **+0.129479961949** |
| PR-AUC | 0.489452694592 | 0.606536911289 | **+0.117084216697** |

Frozen descriptive classification:

**DESCRIPTIVE_BENCHMARK_IMPROVEMENT_ON_BOTH_RANKING_METRICS**

## Paired flow-level bootstrap

- replicates: **10,000**
- seed: **21042**
- interval: **percentile 95%**
- resampling unit: **flow**
- same resampled flows used for both models
- interpretation: **descriptive, not confirmatory**

| Delta | Observed | Bootstrap median | 95% percentile CI |
|---|---:|---:|---:|
| ViT − CNN ROC-AUC | +0.129479961949 | +0.129492358166 | [+0.114504163925, +0.144567415099] |
| ViT − CNN PR-AUC | +0.117084216697 | +0.117073329647 | [+0.102921215820, +0.131503644288] |

These intervals are reported only as the preregistered descriptive uncertainty
summary. They are not used for model selection or a confirmatory superiority
claim.

## Secondary preregistered descriptive deltas

| Quantity | CNN | ViT | ViT − CNN |
|---|---:|---:|---:|
| Standard 0.50 F1 | 0.062940670679 | 0.139395950880 | +0.076455280200 |
| Standard 0.50 Recall | 0.032666904677 | 0.074973223849 | +0.042306319172 |
| Validation-selected balanced F1 | 0.062811051999 | 0.139681486397 | +0.076870434398 |
| Validation-selected balanced Recall | 0.032666904677 | 0.075151731524 | +0.042484826848 |
| Validation-selected security F2 | 0.040427694075 | 0.093042602566 | +0.052614908491 |
| Validation-selected security Recall | 0.032666904677 | 0.075865762228 | +0.043198857551 |

CNN validation-selected balanced/security threshold: **0.17**.

ViT validation-selected balanced threshold: **0.42**.

ViT validation-selected security threshold: **0.24**.

## Scientific interpretation boundary

The single frozen near-parameter-matched ViT shows better descriptive Friday
reuse-benchmark ranking than the immutable Stage20 CNN on both preregistered
ranking metrics.

This does **not** constitute independent confirmation of general ViT
superiority because the Stage20 Friday outcome was known before Stage21 was
locked.

Absolute operating-point recall remains low for both models and should not be
obscured by the positive ranking deltas.

## Integrity

- new model forward passes during Stage21-5: **0**
- threshold search: **NO**
- threshold reselection: **NO**
- model retraining: **NO**
- architecture search: **NO**
- bootstrap-based selection: **NO**
- optimizer steps: **0**

Stage21 architecture-result analysis is now frozen before any post-result
explainability work.
