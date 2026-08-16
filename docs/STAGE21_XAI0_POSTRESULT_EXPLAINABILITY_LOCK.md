# Stage21-XAI0 — Post-result Explainability Lock

## Status

**EXPLAINABILITY PROTOCOL FROZEN BEFORE ATTRIBUTION EXECUTION**

The Stage21 architecture comparison was already durably frozen before this
protocol was created.

Explainability is descriptive only and may not modify the Stage21 architecture
result.

## Locked cohort

A deterministic class-balanced Friday cohort is selected using **true binary
label only**.

- random seed: **21100**
- BENIGN: **256**
- ATTACK: **256**
- total: **512**
- sampling: without replacement within class
- score-conditioned sampling: **NO**
- prediction-conditioned sampling: **NO**
- model-disagreement sampling: **NO**
- cohort SHA256: `ba29cf4611db82fa3c72b84f99ee537425c61c087c96ba96f02091f1156f83d8`

## Attribution method

Exactly one method is permitted:

**Integrated Gradients**

- target: attack pre-sigmoid logit
- baseline: all-zero normalized packet image
- original validity mask held fixed along the integration path
- integration: straight line
- numerical rule: Riemann midpoint
- steps: **64**

No method/baseline/step search is permitted after attribution inspection.

Explicitly excluded:

- attention rollout
- Grad-CAM
- SmoothGrad
- SHAP
- alternative IG baselines
- second attribution method

## Common CNN/ViT comparison grid

Absolute IG attribution is aggregated to the same spatial patch geometry for
both models:

- patch: **8 packet rows × 16 byte columns**
- grid: **8 × 16**
- patches: **128**

This is the frozen ViT patch geometry and is applied identically to CNN
attribution for direct descriptive comparison.

## Descriptive scope

The analysis will report:

- IG completeness residual/error
- padded-pixel attribution leakage
- normalized valid-patch attribution entropy
- top-1 and top-5 patch concentration
- early/middle/late packet-row attribution mass
- per-flow row and byte-position attribution distributions
- true-BENIGN and true-ATTACK mean normalized heatmaps
- paired CNN-vs-ViT summaries on the exact same 512 flows

## Claim boundary

The explanations may describe spatial attribution differences between the
frozen CNN and ViT.

They may **not**:

- select a model
- change a threshold
- change an architecture
- establish causality
- establish independent confirmation
- establish general ViT superiority
- infer protocol-field semantics solely from image location

If the locked explanation method behaves poorly, that limitation is reported.
The method is not replaced post hoc.
