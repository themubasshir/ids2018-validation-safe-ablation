# Stage 19 — MTemporal-IDS Scientific Closure

## Final decision

**SUPPORTED_WITH_CONSTRAINTS**

Stage 19 evaluated an authentic multiscale causal temporal
representation for intrusion detection. The experiment compared
a frozen single-scale 60-second temporal Transformer control with
MTemporal-IDS, which combined 1-second, 15-second, and 60-second
temporal resolutions covering a maximum causal context of
20 minutes.

No future context, cross-day context, arbitrary spatial reshaping,
post-hoc architecture search, seed selection, calibration fitting,
or holdout-driven threshold adjustment was permitted.

## Development protocol

The chronological training partition comprised February 14,
15, 16, 20, 21, 22, and 23. February 28 was used exclusively
for development validation. March 1 and March 2 formed the
chronological holdout.

The single-scale control and MTemporal-IDS were each trained with
seeds 7, 29, and 101. Their unweighted probability ensembles were
frozen before operating-point selection.

Both validation-selected thresholds were 0.01, the lower boundary
of the predeclared threshold grid from 0.01 through 0.99. The grid
was not extended after observing this boundary result.

## Validation behavior

The single-scale ensemble achieved validation PR-AUC
0.310812877, whereas MTemporal-IDS achieved
0.285609745.

Thus, multiscale temporal fusion did not improve validation PR-AUC.
MTemporal-IDS nevertheless showed higher validation ROC-AUC, which
indicated that ranking behavior and precision-recall behavior did
not move uniformly.

The learned fusion gate was also initialization-sensitive:
seed 7: fine (0.5540); seed 29: coarse (0.8366); seed 101: medium (0.8722). Each of the three frozen seeds therefore favored
a different temporal resolution.

## Frozen chronological holdout

The holdout contained 84,000 eligible one-second prediction
intervals, including 27,502 attack-positive and 56,498 benign
seconds. The raw holdout was opened exactly once, converted into
the frozen Stage-19 representation, and permanently closed before
model evaluation.

The single-scale ensemble achieved PR-AUC
0.759957095, ROC-AUC
0.845298213, F1
0.652617569, precision
0.663758743, recall
0.641844230, MCC
0.487854562, and FPR
0.158271089 at its frozen threshold.

MTemporal-IDS achieved PR-AUC
0.801378040, ROC-AUC
0.850201653, F1
0.717620946, precision
0.825250520, recall
0.634826558, MCC
0.615545684, and FPR
0.065435945 at the same independently
frozen threshold value of 0.01.

Relative to the single-scale control, the multiscale ensemble
improved pooled holdout PR-AUC by
+0.041420946, ROC-AUC by
+0.004903439, and F1 by
+0.065003377. Precision increased by
+0.161491777, while recall changed by
-0.007017671. MCC improved by
+0.127691121, and FPR changed by
-0.092835145.

However, probability calibration did not improve. Relative to the
single-scale control, MTemporal-IDS changed Brier score by
+0.012918823 and log loss by +0.167486721.

## Temporal heterogeneity

The pooled result was not consistent across the two holdout days.

On March 1, the single-scale control achieved PR-AUC
0.290639853 and F1
0.222222222, whereas MTemporal-IDS achieved
PR-AUC 0.241329513 and F1
0.058285260.

On March 2, the single-scale control achieved PR-AUC
0.909117583, ROC-AUC
0.917345457, and F1
0.794474758. MTemporal-IDS achieved
PR-AUC 0.957848235, ROC-AUC
0.966206262, and F1
0.889337892.

The attack prevalence also differed strongly across the two days.
Consequently, pooled precision-recall metrics must be interpreted
together with the day-specific results rather than as evidence of
uniform temporal generalization.

## Scale fusion

The frozen MTemporal ensemble's mean holdout gate was:

- Fine: 0.238799
- Medium: 0.320501
- Coarse: 0.440700

These values describe learned model behavior only. They are not
causal feature or temporal-scale explanations.

## Scientific interpretation

MTemporal-IDS is classified as **SUPPORTED_WITH_CONSTRAINTS**.

The experiment supports the claim that authentic multiscale causal
temporal context can provide meaningful intrusion-detection benefit
under some chronological regimes. In the pooled frozen holdout,
multiscale temporal modeling substantially improved precision, F1,
MCC, and false-positive control while maintaining similar recall.

The evidence does not support universal superiority. Multiscale
performance deteriorated on March 1, improved strongly on March 2,
the learned scale gate varied markedly across random seeds, and
probability calibration remained weak. The appropriate conclusion
is therefore conditional multiscale benefit under chronological
distribution shift.

## Claim boundaries

The results must not be used to claim causal superiority,
universally optimal temporal scales, globally optimal threshold
0.01, reliable probability calibration, or guaranteed
generalization to unseen future attack regimes.

## Protocol closure

Stage-19 raw holdout access is permanently closed at **1 / 1**.

No further retraining, threshold adjustment, calibration,
representation modification, seed selection, or holdout reread is
permitted.

The next experimental stage is Stage 20: assessment and
construction of an authentic traffic-image representation before
any Vision Transformer experiment.
