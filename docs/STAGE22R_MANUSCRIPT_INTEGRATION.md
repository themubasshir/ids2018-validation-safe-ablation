# Stage22R Manuscript Integration

This document contains manuscript-ready text derived exclusively from the
already-frozen Stage22R development and single-opening final-holdout artifacts.

Scientific result commit: `b5e44615269198426cc8a9aa3b3e701c2ca9e48e`  
Scientific tag: `stage22r-final-single-holdout-v1`  
Mar1--Mar2 final-holdout opening: **1 / 1**  
Final-holdout status: **PERMANENTLY CLOSED**

No text in this document authorizes retraining, threshold reselection,
calibration, feature changes, preprocessing changes, or post-holdout model
choice.

---

# A. Proposed Contribution Text for the Introduction

A further contribution of this study is a source-faithful temporal-validation
stress test of the frozen classical IDS strategy. The experiment contrasts
random versus chronological development validation and natural versus
training-only rebalanced class prevalence in a precommitted $2\times2$ design,
while all four resulting model cells are evaluated on one common forward
Mar1--Mar2 holdout. Exact K79 identity control is applied using corrected
timestamp second plus the 78 numeric predictors uniformly retained by the
historical Kaggle source. This design separates development-split effects,
training-prevalence effects, threshold-independent ranking transfer, and
frozen operating-point transfer without allowing the final holdout to become
an additional development set.

---

# B. Methods — Stage22R Kaggle-Faithful Temporal Validation

## Source and exact-identity control

Stage22R uses the historical Kaggle IDS2018 daily CSV lineage. Because endpoint
fields are not uniformly retained across all daily files, the corrective
protocol does **not** claim S4 equivalence, five-tuple disjointness, endpoint
disjointness, attacker-source-IP disjointness, or session independence.

Instead, the uniformly available exact identity K79 consists of corrected
integer-second timestamp plus all 78 common numeric predictors, with the label
excluded. Predictor tokens are parsed as IEEE-754 float64 values; NaN is
canonicalized, positive and negative infinity remain distinct for identity,
and negative zero is normalized to positive zero. BLAKE2b-128 is used only as
an accelerator, with exact canonical-record verification for candidate
collisions.

Development exact conflicts and duplicates were removed before split
construction. At the single final opening, development retained signatures had
priority over holdout signatures, followed by within-holdout mixed-label
conflict exclusion and deterministic same-label duplicate collapse.

## Factorial development design

The four frozen cells are:

1. RANDOM × NATURAL,
2. RANDOM × REBALANCED,
3. CHRONOLOGICAL × NATURAL, and
4. CHRONOLOGICAL × REBALANCED.

The chronological development split trains on 14--23 February source days and
validates on 28 February. The random split uses a stratified 80/20 split of the
same K79-clean development universe. Rebalancing is training-only deterministic
benign undersampling; validation and final holdout are never resampled.

All cells use the frozen Stage16 equal-weight LightGBM/XGBoost ensemble and the
same 70 retained model predictors. Standard, balanced, and security thresholds
are fixed from development validation before the final holdout is opened. No
model selection, training, calibration, threshold search, or feature search is
performed on Mar1--Mar2.

---

# C. Results — Development Validation and Single Forward Holdout

## Exact-K79 final-holdout audit

The two final source days contain **1,379,675** effective traffic rows before
K79 cleaning. No holdout K79 record exactly matches a retained development K79
record. Within the final holdout, **5** mixed-label exact signatures account for
**10** excluded rows, and same-label duplicate collapse removes **5,532** rows.
The resulting common final evaluation set contains **1,374,133** rows:
**998,788 benign** and **375,345 attack**, for attack prevalence
**0.273150**.

The absence of exact K79 development overlap shows that exact
timestamp-plus-predictor duplicate reuse does not explain the observed
development-to-forward performance changes. It does not establish session,
endpoint, five-tuple, or source-IP independence.

## Ranking transfer

| Cell | Development PR-AUC | Final PR-AUC | Development ROC-AUC | Final ROC-AUC |
|---|---:|---:|---:|---:|
| Random / Natural | 0.995590 | 0.262953 | 0.998625 | 0.520490 |
| Random / Rebalanced | 0.995305 | 0.273298 | 0.998521 | 0.541982 |
| Chronological / Natural | 0.106215 | 0.610734 | 0.514918 | 0.806418 |
| Chronological / Rebalanced | 0.103739 | 0.692630 | 0.499370 | 0.832164 |

The random-validation cells are nearly perfect on their development validation
membership (PR-AUC approximately **0.995**, ROC-AUC approximately **0.999**) but
drop to PR-AUC **0.263--0.273**
and ROC-AUC **0.520--0.542**
on the common forward holdout.

The chronological cells show the opposite development pattern: 28 February
validation is near chance in ranking terms, yet on the subsequent Mar1--Mar2
holdout the chronological natural cell reaches PR-AUC
**0.610734** and ROC-AUC **0.806418**,
while the chronological rebalanced cell reaches PR-AUC
**0.692630** and ROC-AUC **0.832164**.
These are the largest observed final ranking values among the four
precommitted cells; they are **not** used to select a post-holdout winner.

PR-AUC comparisons across development partitions require caution because the
random and chronological validation cohorts have different prevalences, and
the final holdout prevalence is also different. ROC-AUC provides the
prevalence-insensitive companion view.

## Frozen operating-point transfer

Ranking quality does not imply successful transfer of an absolute probability
threshold. At the frozen balanced operating point, final recall is
**0.001412** for Random/Natural,
**0.004708** for Random/Rebalanced,
**0.000101** for Chronological/Natural, and
**0.000194** for
Chronological/Rebalanced.

The chronological cells therefore retain substantial threshold-free ranking
information on Mar1--Mar2 while their validation-selected threshold of 0.07
almost never fires. Conversely, the random security operating points recover
approximately nine percent attack recall, but their final false-positive rates
rise to **0.287015** and **0.268529**, far above the
development security constraint of 5%. A threshold satisfying a validation
FPR constraint therefore cannot be assumed to preserve that constraint under
the forward distribution.

## Training-prevalence contrast

Training-only rebalancing gives modest final ranking gains under the random
split (PR-AUC **+0.010344**, ROC-AUC
**+0.021492**) and a larger PR-AUC gain
under chronological development (PR-AUC
**+0.081896**, ROC-AUC
**+0.025746**). These are descriptive
factorial contrasts on the common final holdout; no post-holdout model choice
is made.

---

# D. Discussion — Validation Regime, Ranking, and Threshold Transfer

Stage22R demonstrates that validation protocol can change the apparent
generalization story even when model family, feature set, and final evaluation
set are held fixed. The random development cells look exceptionally strong on
their own validation membership but provide weak ranking discrimination on the
later common holdout. The chronological cells look poor on 28 February yet
rank Mar1--Mar2 substantially better. The result argues against treating one
development partition as a universally representative estimate of future
traffic behavior.

The second major finding is the separation between ranking discrimination and
operational threshold transfer. The chronological ensembles can rank later
traffic reasonably well while producing almost no positive classifications at
their frozen threshold. The random security thresholds show the complementary
problem: some recall is recovered, but the final FPR is far above the
validation-era security constraint. These outcomes should be retained rather
than repaired by post-hoc threshold search or calibration on the final
holdout.

The data support a conclusion of strong temporal/distribution heterogeneity
and forward operating-point transfer failure. They do **not** by themselves
establish a particular mechanism such as concept drift, covariate shift,
label-prior shift, campaign composition change, or score calibration drift.
Mechanistic diagnosis would require a separately declared post-result analysis
that cannot modify the closed Stage22R result.

---

# E. Limitations

First, Stage22R's exact K79 control is weaker than endpoint-rich session or
five-tuple grouping because endpoint fields are not uniformly preserved in the
historical Kaggle source. Zero exact K79 overlap therefore must not be described
as proof of session independence.

Second, the experiment evaluates one IDS2018 source lineage and one frozen
classical strategy. The observed validation-transfer pattern should not be
assumed to generalize to other datasets, time periods, feature extractors, or
model families.

Third, the final holdout contains a different attack prevalence from either
development validation regime. PR-AUC is therefore interpreted together with
ROC-AUC and fixed-threshold confusion metrics rather than in isolation.

Fourth, Stage22R intentionally forbids post-holdout threshold repair,
calibration, hyperparameter tuning, or model selection. Consequently, very
poor frozen-threshold performance remains part of the result.

---

# F. Contribution Statement for Abstract or Introduction

A source-faithful $2\times2$ temporal-validation ablation further showed that
development protocol and training prevalence can dramatically alter estimates
of future IDS behavior. After exact K79 duplicate control, random validation
produced near-perfect development discrimination but weak forward ranking,
whereas chronological models showed poor 28 February validation ranking yet
substantially stronger Mar1--Mar2 ROC-AUC and PR-AUC. At the same time,
validation-selected operating thresholds transferred poorly: chronological
thresholds almost never fired, while random security thresholds exceeded the
5% FPR constraint on the final period. The experiment therefore separates
ranking generalization from operating-point transfer and demonstrates why
future-facing IDS evaluation should report both.

---

# G. Publication-Safe Claims

1. The final shared K79-clean holdout contains 1,374,133 rows.
2. No final-holdout K79 signature exactly overlaps a retained development K79 signature.
3. Random development validation substantially overstates its cells' forward ranking performance.
4. Chronological development cells rank Mar1--Mar2 substantially better than they rank Feb28.
5. Chronological/Rebalanced has the largest observed final PR-AUC and ROC-AUC among the four frozen cells.
6. This observed ordering does not authorize post-holdout winner selection.
7. Frozen threshold behavior can diverge sharply from threshold-independent ranking behavior.
8. Random security thresholds do not preserve the 5% FPR constraint on the final holdout.
9. Training-only rebalancing improves final ranking within both split families, most strongly in chronological PR-AUC.
10. Stage22R supports temporal/distribution heterogeneity as a concern for IDS validation.

---

# H. Claims That Must Not Appear

1. Stage22R provides exact S4 duplicate control.
2. Stage22R proves session, endpoint, five-tuple, or source-IP independence.
3. Chronological/Rebalanced was selected as a new final winner.
4. The final holdout was used to select or repair a threshold.
5. The final holdout was used for calibration or retraining.
6. Stage22R proves concept drift as the mechanism.
7. PR-AUC values from cohorts with different prevalence are directly interchangeable without qualification.
8. The training-only rebalance operator reproduces an unknown historical flagship balancing procedure.
9. The random validation result is an unbiased estimate of future chronological performance.
10. The chronological validation result alone establishes that the model is unusable.

---

# I. Recommended Manuscript Figures

- **Figure 22R-1:** `figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.png`
- **Figure 22R-2:** `figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.png`
- **Figure 22R-3:** `figures/stage22r_temporal_validation/fig22r_3_final_frozen_operating_points.png`
- **Supplementary Figure 22R-S1:** `figures/stage22r_temporal_validation/fig22r_4_k79_final_holdout_cleaning.png`

The first three figures are recommended for the main manuscript. The K79
cleaning figure is primarily a reproducibility/supplementary asset.

---

# J. Recommended Placement

- **Introduction / Contributions:** Sections A or F.
- **Methods:** Section B.
- **Results:** Section C plus Figures 22R-1 through 22R-3.
- **Discussion:** Section D.
- **Limitations:** Section E.
- **Supplementary / reproducibility:** K79 cleaning figure and Sections G--H as claim-control notes.

Stage22R should be described as the **Kaggle-faithful temporal-vs-random
experiment under exact K79 identity control**, not as the original endpoint-rich
S4/session-safe experiment.
