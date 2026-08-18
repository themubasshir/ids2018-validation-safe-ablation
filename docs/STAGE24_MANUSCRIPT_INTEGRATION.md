# Stage24 Manuscript Integration

## Cross-Dataset Generalization and Artifact-Sensitivity Audit

Scientific execution for Stage24 is closed.

Final scientific commit before this publication package:

`a4b6a3854109ba3d85954fb4a40afe6fe1ee6114`

Frozen result SHA256:

`785bbcb00140f4d7e07e9b49ad33924166b5995e66a229c986d5b1abcbcaee4b`

No section below authorizes additional model fitting, target inference,
threshold search, calibration, feature modification, or post-target model
selection.

---

# A. Results

## A.1 Bidirectional cross-dataset ranking generalization

Stage24 evaluated transfer in two separately reported directions. The
IDS2018-to-CICIDS2017 direction used the complete effective CICIDS2017
population of **2,830,743 flows**, containing
**557,646 attacks** and attack prevalence
**0.196996**. The reciprocal CICIDS2017-to-IDS2018 direction
used the frozen K79-clean IDS2018 Feb-28 population of
**593,780 flows**, including **62,256
attacks** and attack prevalence **0.104847**.

In the IDS2018-to-CICIDS2017 direction, bridge62 achieved PR-AUC
**0.667483** and ROC-AUC
**0.733946**. Including the eight
aggregate flag-count fields under the published bridge70 interpretation yielded
PR-AUC **0.663981** and ROC-AUC
**0.741891**. Under the frozen
flag-corrected interpretation, bridge70 achieved PR-AUC
**0.656252** and ROC-AUC
**0.744083**.

The reciprocal CICIDS2017-to-IDS2018 transfer was substantially weaker.
Bridge62 reached PR-AUC **0.108176** and
ROC-AUC **0.525167**, while bridge70 reached
PR-AUC **0.107419** and ROC-AUC
**0.525302**. The IDS2018 Feb-28 PR-AUC
chance anchor defined by target attack prevalence is **0.104847**.
Consequently, normalized PR-AUC is only
**0.003719** for bridge62 and
**0.002874** for bridge70, compared
with approximately
**0.585908**
for bridge62 in the opposite direction.

These results establish a pronounced directional asymmetry under the frozen
protocol: the IDS2018-trained representation retains meaningful ranking signal
on CICIDS2017, whereas models trained on CICIDS2017 Monday-Wednesday transfer
only marginally above the Feb-28 prevalence/chance ranking anchor when evaluated
on IDS2018.

## A.2 Bridge-feature sensitivity

For IDS2018-to-CICIDS2017 under published target semantics, adding the eight
aggregate flag-count features changed PR-AUC by
**-0.003502**
(95% CI
[-0.003856,
-0.003152]),
ROC-AUC by
**+0.007945**
([+0.007793,
+0.008096]),
and Brier score by
**-0.002844**
([-0.002915,
-0.002766]).

In the reciprocal direction, bridge70-minus-bridge62 produced PR-AUC difference
**-0.000757**
(95% CI [-0.001058, -0.000435]),
ROC-AUC difference
**+0.000135**
([-0.000900, +0.001263]),
and Brier difference
**-0.000106**
([-0.000124, -0.000089]).

The reciprocal ROC-AUC interval includes zero, while the very small PR-AUC and
Brier differences exclude zero. Thus, the flag-count fields do not rescue the
weak reciprocal ranking transfer.

## A.3 Extractor and serialization sensitivity

Stage24 separately audited the known aggregate-flag serialization mismatch in
CICIDS2017. Holding the target population, source model, and bridge70 feature
count fixed, replacing the published aggregate-flag interpretation with the
frozen corrected mapping changed PR-AUC by
**-0.007729**
(95% CI [-0.007921, -0.007534]),
ROC-AUC by
**+0.002192**
([+0.002139, +0.002246]),
and Brier score by
**+0.005087**
([+0.005023, +0.005152]).

All three paired intervals exclude zero. Therefore, extractor/serialization
semantics are not merely a bookkeeping concern: they measurably change the
reported cross-dataset behavior of the same nominal bridge70 representation.

## A.4 Frozen operating-point transfer

The reciprocal experiment also exposes severe operating-point transfer
failure. Source-validation thresholds selected exclusively on CICIDS2017
Thursday were transferred without target retuning.

For bridge62, target recall is
**0.000386** at the
standard threshold,
**0.000610** at the
balanced threshold, and
**0.001349** at the
security threshold.

For bridge70, corresponding recall is
**0.000386**,
**0.000610**, and
**0.000819**.

Thus, even the source-selected security thresholds detect less than 0.14% of
IDS2018 Feb-28 attacks for bridge62 and less than 0.09% for bridge70. These poor
operating points are retained as results rather than repaired through target
threshold search.

## A.5 Calibration transfer

Reciprocal cross-dataset probability calibration also deteriorates. Bridge62
has Brier score **0.105758** and 10-bin ECE
**0.105701**, while bridge70 has Brier score
**0.105652** and ECE **0.105672**.
For comparison, the target-prevalence constant predictor has Brier score
**0.093854**. Both transferred models therefore have worse
Brier score than this target-prior reference, although the target-prior value is
reported as a diagnostic anchor rather than as a trained competing model.

---

# B. Discussion

Stage24 shows that cross-dataset IDS generalization cannot be summarized by a
single portability number. The strongest observation is directional asymmetry.
An IDS2018-derived representation retains substantial threshold-independent
ranking signal when transferred to the effective CICIDS2017 population, but the
reciprocal CICIDS2017-trained models evaluated on the frozen IDS2018 Feb-28
target are only slightly above chance in both normalized PR-AUC and ROC-AUC.
Because the two directions use different source models, target populations, and
prevalence structures, they are intentionally not averaged.

This asymmetry cautions against treating successful transfer from dataset A to
dataset B as evidence that the two datasets are interchangeable. A classifier
can exploit structures that survive one transfer direction but are absent,
reweighted, or encoded differently in the reciprocal direction. Cross-dataset
evaluation should therefore be bidirectional when both source/target roles are
scientifically meaningful.

The bridge ablation provides a second result. Adding the aggregate flag-count
features changes performance, but their effect is not uniformly beneficial.
Under IDS2018-to-CICIDS2017 transfer, bridge70 increases ROC-AUC but decreases
PR-AUC relative to bridge62. Under reciprocal transfer, bridge70 does not yield
a resolved ROC-AUC improvement and slightly decreases PR-AUC. More features are
therefore not automatically more portable features.

The serialization audit strengthens this interpretation. Correcting the
CICIDS2017 aggregate-flag semantics changes all three paired metrics in the
primary bridge70 comparison. A cross-dataset experiment can consequently
attribute performance changes to domain shift when part of the difference
actually arises from feature-extractor semantics. Cross-dataset IDS studies
should document semantic feature alignment rather than relying only on
similarly named columns.

Finally, Stage24 again separates ranking transfer from operating-point transfer.
The reciprocal models are already weak in ranking terms, but their source-frozen
probability thresholds degrade even more severely, missing virtually all
attacks on IDS2018 Feb-28. Thresholds and probability calibration therefore
require separate validation from threshold-independent discrimination.

---

# C. Limitations and Threats to Validity

## C.1 Dataset scope

The study evaluates two related benchmark families, CSE-CIC-IDS2018 and
CICIDS2017. Both were produced within the CIC research ecosystem and may share
traffic-generation or feature-extraction characteristics. The measured
asymmetry should therefore not be assumed to quantify transfer to unrelated
enterprise, ISP, cloud, IoT, or operational network traffic.

## C.2 Single frozen model strategy

The primary direction uses the frozen Stage22R classical ensemble lineage,
whereas the reciprocal direction uses preregistered XGBoost-only source models.
This design answers the declared Stage24 questions but does not establish that
the same directional asymmetry magnitude would occur for every model family,
representation learner, or neural architecture.

## C.3 Different target prevalences

CICIDS2017 and IDS2018 Feb-28 have different attack prevalences. PR-AUC is
therefore interpreted together with target prevalence, normalized PR-AUC,
ROC-AUC, and calibration metrics. Raw PR-AUC values from the two directions
must not be treated as directly interchangeable without this context.

## C.4 Aggregate-flag semantic correction

The flag-corrected bridge70 result is a preregistered semantic audit, not a
post-hoc optimization. Seven physical CICIDS2017 aggregate-flag mappings differ
between published and corrected representations, while ACK is invariant.
Results should not be generalized to other CICIDS2017 exports without
confirming their extractor lineage.

## C.5 GROUNDED_S4 structural unavailability

The two preregistered GROUNDED_S4 primary cells were not evaluated. Exact
Stage20 S4 membership could not be recovered as exact physical target-table rows
from durable artifacts without introducing a new heuristic matching rule after
protocol freeze. The cells were therefore administratively cancelled before
opening. No fuzzy or inferred substitute was used, and their two opening slots
were not reallocated.

## C.6 Threshold transfer

Target thresholds were deliberately not retuned. Poor target recall therefore
represents source-to-target operating-point transfer failure under the frozen
protocol, not the best threshold achievable if IDS2018 target labels were made
available for adaptation.

## C.7 Mechanistic interpretation

The experiment establishes distributional and semantic sensitivity but does not
uniquely identify the causal mechanism. The observed differences may include
covariate shift, attack-mixture shift, label-prior effects, extractor behavior,
environmental differences, or interactions among these factors. Stage24 does
not prove any one of these mechanisms in isolation.

## C.8 Bootstrap scope

The paired 95% intervals quantify uncertainty with respect to row-level
class-stratified resampling of the frozen target populations. They do not
represent uncertainty over independently collected networks, organizations,
capture campaigns, or dataset-generation processes.

---

# D. Contributions

Stage24 adds the following publication-level contributions:

1. **Bidirectional cross-dataset evaluation.** The study evaluates both
   IDS2018-to-CICIDS2017 and CICIDS2017-to-IDS2018 transfer rather than treating
   one direction as sufficient evidence of dataset portability.

2. **Directionality as an explicit result.** The frozen experiment demonstrates
   that cross-dataset generalization can be strongly asymmetric, with substantial
   ranking transfer in one direction and near-chance reciprocal transfer.

3. **Semantic bridge ablation.** The 62-feature bridge separates a core common
   representation from eight aggregate flag-count features, allowing their
   contribution to cross-dataset portability to be measured.

4. **Extractor/serialization artifact audit.** Published and corrected
   CICIDS2017 aggregate-flag interpretations are compared on the same frozen
   target rows, showing statistically resolved changes in PR-AUC, ROC-AUC, and
   Brier score.

5. **Validation-safe target governance.** Source-validation thresholds are
   transferred without target tuning, scientific fit and target-opening budgets
   are preregistered, and unavailable GROUNDED_S4 cells are cancelled rather
   than replaced with post-result heuristics.

6. **Paired uncertainty analysis.** Feature-bridge and semantic-artifact effects
   are quantified with 2,000-replicate paired class-stratified bootstrap
   intervals using frozen target prediction vectors.

7. **Separation of ranking, calibration, and operating-point transfer.**
   Stage24 reports PR-AUC/ROC-AUC, Brier/ECE, and fixed-threshold confusion
   behavior separately, exposing failures that would be hidden by a single
   metric.

---

# E. Contribution Text for Abstract / Introduction

A validation-safe bidirectional cross-dataset audit between CSE-CIC-IDS2018 and
CICIDS2017 revealed pronounced transfer asymmetry. IDS2018-derived models
retained substantial ranking discrimination on CICIDS2017
(PR-AUC 0.667,
ROC-AUC 0.734 for the 62-feature
bridge), whereas reciprocal CICIDS2017-to-IDS2018 transfer was near the Feb-28
chance/prevalence anchor
(PR-AUC 0.108,
ROC-AUC 0.525). A semantic audit further
showed that correcting CICIDS2017 aggregate TCP-flag serialization changed
bridge70 PR-AUC by -0.0077 and ROC-AUC by
+0.0022, with paired bootstrap intervals
excluding zero. The results show that cross-dataset IDS portability depends not
only on domain shift but also on transfer direction, feature-bridge design, and
extractor semantics.

---

# F. Publication-Safe Claims

1. Stage24 completed all four preregistered scientific fits.
2. Six evaluable target openings were completed; two GROUNDED_S4 cells were
   cancelled before opening and were not reallocated.
3. IDS2018-to-CICIDS2017 transfer substantially exceeds chance ranking.
4. CICIDS2017-to-IDS2018 transfer on IDS2018 Feb-28 is only marginally above
   chance/prevalence ranking.
5. Cross-dataset generalization is strongly direction-dependent in this frozen
   experiment.
6. bridge70 does not uniformly improve cross-dataset portability over bridge62.
7. Correcting aggregate flag serialization measurably changes primary bridge70
   PR-AUC, ROC-AUC, and Brier score.
8. Source-selected probability thresholds fail to transfer operationally to the
   reciprocal IDS2018 target.
9. No target threshold tuning, calibration, feature search, or target-guided
   retraining was performed.
10. The two transfer directions must remain separately reported.

---

# G. Claims That Must Not Appear

1. CICIDS2017 and IDS2018 are universally incompatible datasets.
2. Stage24 proves a unique causal mechanism such as concept drift.
3. The transfer directions can be averaged into one cross-dataset score.
4. GROUNDED_S4 was successfully reconstructed or evaluated.
5. A fuzzy substitute was used for unavailable GROUNDED_S4 membership.
6. bridge62 is universally superior to bridge70.
7. bridge70 is universally superior to bridge62.
8. Target thresholds were optimized on IDS2018.
9. Stage24 evaluates every possible IDS model family.
10. Row-bootstrap confidence intervals represent uncertainty across independent
    real-world organizations or deployment environments.

---

# H. Recommended Main-Manuscript Figures

**Figure 24-1**
`figures/stage24_cross_dataset/fig24_1_normalized_pr_auc_directionality.png`

Normalized PR-AUC reveals the directional asymmetry while accounting for
different target prevalence.

**Figure 24-2**
`figures/stage24_cross_dataset/fig24_2_roc_auc_directionality.png`

ROC-AUC provides the prevalence-insensitive companion view.

**Figure 24-3**
`figures/stage24_cross_dataset/fig24_3_paired_effects_forest.png`

Paired bootstrap intervals quantify bridge and extractor-semantic effects.

**Supplementary Figure 24-S1**
`figures/stage24_cross_dataset/fig24_4_secondary_threshold_transfer.png`

The source-selected operating points show severe reciprocal threshold-transfer
failure.

---

# I. Recommended Manuscript Placement

- **Introduction / Contributions:** Section D or E.
- **Results:** Section A + Tables 24-1 through 24-3 + Figures 24-1 through 24-3.
- **Discussion:** Section B.
- **Limitations / Threats to Validity:** Section C.
- **Supplementary material:** Figure 24-S1 and governance table.
- **Reproducibility package:** frozen Stage24 result JSONs, prediction hashes,
  bootstrap artifacts, publication tables, and exported Stage24 notebook/script.
