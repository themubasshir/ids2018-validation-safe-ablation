# Stage 13 — Local Explanation Reliability Analysis

## Experimental scope

Local explanations were evaluated for the validation-selected XGBoost and
LightGBM intrusion-detection models. The analysis used the original
training-only background distribution and preserved the untouched
seed-42 holdout partition. A deterministic panel contained eight true
positives, true negatives, false positives, and false negatives for each
model, yielding 64 model-specific cases.

## LIME configuration selection

Six perturbation configurations were evaluated on 12 cross-model
disagreement cases. The strongest tested configuration used continuous
features, instance-centred sampling, 10,000 perturbations, and a kernel
width of 8.8318. Its overall local
decision agreement was
0.875, with median
local R2 of 0.280 and median
absolute fidelity gap of
0.142. The corresponding
90th-percentile fidelity gap remained
0.357, demonstrating that the
selected configuration improved but did not resolve surrogate mismatch.

## Perturbation-seed stability

Across five independent perturbation seeds, the feature rankings and
weights were comparatively stable. XGBoost achieved mean top-10 Jaccard
stability of
0.753,
whereas LightGBM achieved
0.745.
The corresponding attribution-vector cosine similarities were
0.962
and
0.990.
Consequently, the principal limitation was not random seed instability;
the explanations were repeatable but often represented an inaccurate
local linear approximation.

## Agreement with TreeSHAP

TreeSHAP satisfied additive reconstruction, with maximum raw-score errors
of 5.868e-06 for XGBoost and
1.776e-14 for LightGBM. In contrast, the mean local
SHAP–LIME top-10 Jaccard similarities on the disagreement panel were
0.304
for XGBoost and
0.360
for LightGBM. Signed attribution agreement was substantially weaker than
absolute-magnitude agreement, indicating that the two methods frequently
differed not only in feature ranking but also in the inferred direction
of local influence.

## Full outcome-stratified panel

Only 2 of the 64 explanations
(3.1%) satisfied every study-specific fidelity and
cross-method criterion. The qualified cases were LIGHTGBM_FP_01, LIGHTGBM_TP_01.
A total of 31 explanations
(48.4%) failed to reproduce the model's local
classification decision, 30 were classified as
fidelity-limited, and 1 was classified as
cross-method divergent.

The outcome-specific failure patterns were asymmetric. LightGBM LIME
surrogates failed to preserve the local decision for all selected false
negatives, while XGBoost surrogates failed for all selected false
positives and all selected true positives. Even when the surrogate
decision agreed, local R2 and probability fidelity often remained
insufficient.

## Interpretation

These findings do not demonstrate that LIME explanations are random.
Instead, they show that a stable local surrogate may still be an
inaccurate representation of the underlying nonlinear tree ensemble.
Stability alone must therefore not be interpreted as explanation
validity.

TreeSHAP should serve as the primary local explanation method because its
attributions preserve the additive model decomposition. LIME may be
retained as a supplementary diagnostic and robustness analysis, provided
that each displayed explanation is accompanied by its local R2,
model-surrogate probability gap, seed-stability result, and agreement
with TreeSHAP.

## Recommended manuscript claim

“LIME explanations were reproducible across perturbation seeds but
frequently exhibited limited local fidelity and weak directional
agreement with exact TreeSHAP attributions. We therefore use TreeSHAP as
the primary local explanation method and retain LIME as a supplementary
surrogate-reliability analysis rather than an equivalent attribution
ground truth.”