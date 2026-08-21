# Stage27 Manuscript Integration

## Scientific Identity

**Stage27 title:** Leave-One-Attack-Family-Out Unseen-Family Generalization Audit

**Design:** `CHRONOLOGY_FIRST_ZERO_TRAINING_EXPOSURE_FAMILY_AUDIT`

**Canonical scientific parent:** `0e1439565aedc7da9b7ca1207262e9061422bc22`

Stage27 scientific execution is closed. This document is a post-closure
publication-integration artifact generated from the frozen Stage27-4A
synthesis. It introduces no new measurement and authorizes no target
reopening, model inference, model refitting, threshold reselection,
bootstrap recomputation, feature modification, or post-target model
selection.

The publication-safe high-level outcome is:

1. `SELECTIVE_FAMILY_TRANSFER`
2. `RANKING_THRESHOLD_DIVERGENCE`
3. `LEARNER_DEPENDENCE`

Stage27 is an unseen attack-family generalization audit. It must not be
described as formal proof of zero-day detection.

---

# A. Proposed Contribution Text for the Introduction

A further contribution of this study is a chronology-first
zero-training-exposure attack-family generalization audit. Seven
CICIDS2017 attack families were preregistered for evaluation under a
strict `TRAIN < VALIDATION < TARGET` design in which the held-out family
was absent from both training and validation. Five families were
structurally executable, while DOS and AUTH_BRUTE_FORCE could not be
evaluated without violating the frozen chronological geometry. Across
the executable families, transfer was selective rather than universal:
DDoS and Web Attack retained strong ranking discrimination, Bot traffic
collapsed, and Port Scan exhibited substantial learner dependence.
Moreover, preserved ranking discrimination did not necessarily yield
useful recall at validation-selected frozen thresholds, separating
attack-family ranking generalization from operating-point transfer.

---

# B. Methods — Chronology-First Unseen-Family Generalization

## B.1 Scientific question

Stage27 evaluates whether a binary intrusion detector trained without
exposure to a particular attack family can discriminate that held-out
family from temporally matched benign traffic when the family first
becomes eligible under strict chronology.

The experiment is therefore described as an **unseen attack-family** or
**zero-training-exposure family** audit rather than as a formal
zero-day-detection experiment.

## B.2 Frozen taxonomy and executability

The preregistered primary taxonomy contains:

- BOT
- DDOS
- DOS
- AUTH_BRUTE_FORCE
- INFILTRATION
- PORT_SCAN
- WEB_ATTACK

Five of seven families were executable. DOS was structurally ineligible
because its first valid target day was Wednesday, leaving Monday for
training and Tuesday for validation, while Monday contained zero
known-family attack positives. AUTH_BRUTE_FORCE was structurally
ineligible because its first appearance on Tuesday left insufficient
earlier weekday depth for separate training and validation periods.

INFILTRATION was executable but is permanently descriptive only because
its held-out target support was 36.

## B.3 Chronological fold geometry

For BOT, DDOS, and PORT_SCAN:

- TRAIN: Monday–Wednesday
- VALIDATION: Thursday
- TARGET: Friday
- training rows: 1,668,519
- validation rows: 458,968
- Friday benign rows: 414,322

For INFILTRATION and WEB_ATTACK:

- TRAIN: Monday–Tuesday
- VALIDATION: Wednesday
- TARGET: Thursday
- training rows: 975,827
- validation rows: 692,692
- Thursday benign rows: 456,752

The held-out family has zero training rows and zero validation rows in
every executable fold. Any positive held-out-family membership in either
development role would invalidate the fold.

## B.4 Primary target semantics

The primary isolation target is:

`HELD_OUT_FAMILY + SAME_TARGET_DAY_BENIGN`

The positive class contains only the held-out attack family and the
negative class contains only benign traffic from the same target day.
Other known target-day attacks are excluded.

A broader operational context target containing held-out attacks, known
attacks, and benign traffic is secondary and descriptive only. The
manuscript should lead with the primary isolation target.

## B.5 Learners and thresholds

Two preregistered learners were evaluated:

- XGBoost
- LightGBM

No Stage27 hyperparameter optimization was permitted. Across five
executable folds and two learners, the total fit budget was exactly 10
models.

Three operating points were frozen from known-family validation data
only:

- STANDARD: threshold 0.50
- BALANCED: maximum validation F1, then minimum FPR, then higher threshold
- SECURITY: maximum validation F2 subject to FPR <= 0.05, then minimum
  FPR, then higher threshold

The threshold grid was 0.01–0.99 and the target decision rule was
`probability >= threshold`.

No target threshold search or target-guided model adaptation was
permitted.

## B.6 Bootstrap uncertainty

Stage27 uses 2,000-replicate class-stratified row bootstrap intervals
with seed 42. Sampling is performed with replacement within the benign
and held-out-attack target strata while preserving stratum sizes.

The intervals quantify **target-sampling uncertainty conditional on the
already-fitted model**. They do not include training-seed uncertainty,
model-selection uncertainty, model-retraining uncertainty, or broader
population uncertainty.

## B.7 Behavioral similarity

The secondary behavioral-similarity audit uses 11 preregistered
aggregate flow descriptors. Preprocessing is fitted only on current-fold
TRAIN rows, each family is represented by its standardized centroid, and
Euclidean distance to the nearest seen family is transformed to
similarity as:

`1 / (1 + nearest_seen_distance)`

This analysis is descriptive only. No formal correlation significance
test, regression inference, p-value, or causal interpretation is
authorized.

---

# C. Results — Unseen Attack-Family Generalization

## C.1 Executability under strict chronology

Of seven preregistered families, five were structurally executable.
BOT, DDOS, PORT_SCAN, and WEB_ATTACK satisfied the frozen family-level
support requirement. INFILTRATION was executable but remains
descriptive only because its held-out support was 36. DOS and
AUTH_BRUTE_FORCE were structurally ineligible under the precommitted
day-atomic chronology rather than being treated as model failures.

## C.2 Primary unseen-family ranking

The frozen ranking results demonstrate strongly family-dependent
transfer.

**DDoS produced the strongest transfer.** XGBoost reached ROC-AUC
0.9982 and PR-AUC
0.9925, while LightGBM reached ROC-AUC
0.9986 and PR-AUC
0.9940. Thus, both learners retained
near-perfect threshold-independent discrimination despite receiving
zero DDoS training or validation examples.

**Web Attack also transferred strongly.** XGBoost reached ROC-AUC
0.9693 and PR-AUC
0.7206; LightGBM reached ROC-AUC
0.9901 and PR-AUC
0.7605.

**Bot traffic showed substantial collapse.** XGBoost produced ROC-AUC
0.3224, while LightGBM produced ROC-AUC
0.5591. XGBoost PR-AUC was
0.003256, below the target prevalence anchor of
0.004723, giving PR-excess
-0.001467. LightGBM was only marginally above the
same prevalence anchor, with PR-excess
0.000156.

**Port Scan was materially learner-dependent.** XGBoost reached
ROC-AUC 0.5506, whereas LightGBM reached
0.7559. The corresponding PR-AUC values were
0.3622 and 0.4191,
respectively.

INFILTRATION produced ROC-AUC
0.7816 for XGBoost and
0.7537 for LightGBM, but these values are
reported descriptively because only 36 held-out attacks were available.

The overall result is therefore **selective family transfer**, not
uniform unseen-family generalization.

## C.3 Frozen operating-point transfer

Threshold-independent ranking quality did not guarantee useful
frozen-threshold detection.

At the BALANCED operating point:

- BOT recall was 0.00% for XGBoost and
  0.00% for LightGBM.
- DDOS recall was 66.20% and
  26.25%.
- INFILTRATION recall was 0.00% and
  0.00%, descriptive only.
- PORT_SCAN recall was 0.48% and
  1.17%.
- WEB_ATTACK recall was 77.80% and
  52.11%.

The divergence is particularly visible for DDOS, where both learners
retain ROC-AUC above 0.998 but BALANCED recall is only
66.20% for XGBoost and
26.25% for LightGBM. Port Scan provides another
example: LightGBM retains ROC-AUC
0.7559 but detects only
1.17% of held-out Port Scan attacks at its frozen
BALANCED threshold.

These results support the frozen Stage27 outcome
`RANKING_THRESHOLD_DIVERGENCE`.

## C.4 Novelty-generalization gaps

The compatible novelty-gap analysis further shows that family novelty
does not impose a uniform penalty.

For XGBoost, the known-minus-unseen ROC-AUC gap is approximately
0.671
for BOT and
0.442
for PORT_SCAN, whereas the DDOS gap is
-0.005.

PR-excess rather than raw PR-AUC difference is used as the primary
prevalence-compatible PR novelty gap. Raw PR-AUC differences across
populations with different prevalence anchors are retained only as
descriptive quantities.

## C.5 Behavioral similarity

The frozen behavioral-similarity values do not show a monotonic
relationship with unseen-family discrimination.

BOT has the highest observed similarity to a seen family
(0.6994) yet weak
unseen-family performance. DDOS has a substantially lower similarity
(0.3834) but
near-perfect ranking. WEB_ATTACK has intermediate similarity
(0.4600)
while retaining strong transfer.

Behavioral proximity, as operationalized by this frozen centroid
distance, therefore does not appear sufficient by itself to explain
the observed transfer pattern.

---

# D. Discussion — Attack-Family Novelty and Generalization

Stage27 demonstrates that known-family intrusion-detection performance
cannot be treated as evidence of uniform robustness to attack-family
novelty. The strongest transfer cases, DDOS and WEB_ATTACK, retain high
ranking discrimination for both learners despite zero exposure to the
held-out family during training and validation. BOT provides the
opposite outcome, with complete frozen-threshold detection failure and
little or adverse ranking signal. PORT_SCAN occupies an intermediate
case in which the outcome depends materially on the learner.

A second finding is the distinction between ranking discrimination and
operating-point transfer. DDoS is the clearest example: both learners
rank the held-out family almost perfectly, yet validation-selected
BALANCED thresholds recover substantially less than all of the held-out
attacks. The same separation is visible for Port Scan and, to a lesser
degree, Web Attack. Consequently, ROC-AUC or PR-AUC alone cannot
characterize whether a frozen deployment threshold will remain useful
under attack-family novelty.

This ranking-versus-threshold distinction also complements earlier
experiments in the study. Representation-specific chronological
evaluation, the Stage22R forward temporal audit, and the Stage24
cross-dataset audit independently showed that strong ranking behavior
can coexist with poor fixed-threshold transfer. Stage27 extends that
observation to zero-training-exposure attack families. Across these
distinct stress regimes, threshold-independent discrimination and
operating-point behavior should therefore be evaluated as separate
properties of an IDS.

Learner dependence is itself family-dependent. XGBoost and LightGBM
agree closely on the strong DDoS and Web Attack ranking outcomes but
differ substantially on Port Scan and also differ in Bot ranking.
The evidence therefore does not support declaring one learner
universally superior for unseen-family generalization.

The behavioral-similarity analysis provides no simple mechanistic
explanation. BOT is behaviorally closest to a seen family under the
frozen 11-descriptor representation yet transfers poorly, whereas DDOS
is less similar under the same definition but transfers extremely well.
This secondary analysis should therefore be interpreted as evidence
that the selected notion of behavioral proximity is insufficient by
itself, not as proof of either the presence or absence of a particular
causal mechanism.

Finally, strict chronology exposes limitations in the benchmark itself.
The inability to execute DOS and AUTH_BRUTE_FORCE is a consequence of
the temporal arrangement of attack families and the requirement for
separate training and validation periods. Rather than manufacturing
alternative folds after observing the data, Stage27 preserves these
families as structurally ineligible. This makes the scope of the
generalization claim narrower but maintains the validation-safe
interpretation of the experiment.

---

# E. Limitations and Threats to Validity

1. **Incomplete taxonomy executability.** Only five of seven
   preregistered families could be honestly evaluated under strict
   `TRAIN < VALIDATION < TARGET` chronology.

2. **Low INFILTRATION support.** INFILTRATION contains only 36 held-out
   target attacks and is therefore descriptive only.

3. **Chronology-first rather than textbook LOAO.** Strict chronology
   means that every non-held-out attack family is not necessarily
   represented during training. Stage27 is therefore specifically a
   chronology-first zero-training-exposure family audit.

4. **Conditional bootstrap uncertainty.** The 95% intervals quantify
   row-level target-sampling uncertainty conditional on each already
   fitted model. They do not incorporate retraining, seed, model
   selection, independently collected networks, or broader population
   uncertainty.

5. **No clustered bootstrap.** No preregistered durable grouping
   variable was available for a session- or time-cluster bootstrap.

6. **Restricted similarity representation.** Behavioral similarity is
   based only on 11 preregistered aggregate flow descriptors and a
   centroid-distance representation.

7. **Descriptive similarity analysis.** No formal correlation test,
   p-value, regression inference, or causal interpretation is
   authorized.

8. **Benchmark-specific external validity.** CICIDS2017 is a benchmark
   capture. The observed transfer pattern does not establish universal
   behavior for production networks, unrelated datasets, or genuinely
   novel real-world attacks.

9. **No zero-day proof.** Zero training exposure to an attack family in
   this benchmark is not equivalent to demonstrating universal
   real-world zero-day detection.

---

# F. Stage27 Publication-Level Contributions

1. **Chronology-first unseen-family evaluation.** Attack-family novelty
   is evaluated under a strict training-before-validation-before-target
   design with zero held-out-family exposure during development.

2. **Structural executability accounting.** Families that cannot be
   evaluated without violating chronology are explicitly labeled
   structurally ineligible rather than replaced with post-hoc folds.

3. **Selective-transfer finding.** DDoS and Web Attack retain strong
   transfer, Bot collapses, and Port Scan depends materially on learner
   choice.

4. **Ranking/threshold separation.** Threshold-independent
   discrimination and frozen validation-selected operating-point
   behavior are evaluated separately.

5. **Learner-dependent novelty audit.** XGBoost and LightGBM are
   compared under the same preregistered family-holdout geometry without
   Stage27 HPO.

6. **Target-sampling uncertainty.** Primary ranking and compatible
   operating metrics are accompanied by frozen 2,000-replicate
   stratified bootstrap intervals.

7. **Secondary behavioral-similarity audit.** A preregistered
   train-fitted descriptor representation is used to test whether simple
   behavioral proximity descriptively explains transfer, without
   introducing post-result significance testing.

---

# G. Contribution Text for Abstract / Introduction

A chronology-first zero-training-exposure attack-family audit further
revealed selective rather than universal unseen-family transfer. Under
strict `TRAIN < VALIDATION < TARGET` separation, both XGBoost and
LightGBM retained near-perfect ranking discrimination for held-out DDoS
traffic and strong ranking for Web Attack, whereas Bot traffic
collapsed and Port Scan transfer was materially learner-dependent.
Moreover, high unseen-family ROC-AUC did not necessarily translate into
useful recall at frozen validation-selected thresholds. The findings
show that strong known-family IDS performance should not be interpreted
as evidence of uniform robustness to unseen attack families and that
ranking generalization and operating-point transfer should be audited
separately.

---

# H. Publication-Safe Claims

The following claims are supported by the frozen Stage27 evidence:

1. Stage27 preregistered seven attack-family categories.
2. Five of the seven families were structurally executable.
3. DOS and AUTH_BRUTE_FORCE were structurally ineligible under strict
   chronology.
4. INFILTRATION is descriptive only because held-out support was 36.
5. DDoS retained near-perfect unseen-family ranking for both learners.
6. Web Attack retained strong unseen-family ranking for both learners.
7. Bot exhibited substantial unseen-family collapse.
8. Port Scan exhibited material learner dependence.
9. Ranking performance and frozen-threshold recall diverged for several
   families.
10. Behavioral similarity did not display a monotonic relationship with
    unseen-family ranking performance across the five executable
    families.
11. No target threshold tuning, target-guided model selection, or
    target-guided adaptation was performed.
12. The bootstrap intervals quantify target-sampling uncertainty
    conditional on the fitted model.
13. Known-family performance should not be treated as evidence of
    uniform unseen-family generalization.

---

# I. Claims That Must Not Appear

1. Stage27 proves universal zero-day detection.
2. Stage27 proves all unseen cyberattacks can be detected.
3. All seven attack families were experimentally executable.
4. INFILTRATION provides an inferential family-level conclusion.
5. LightGBM is universally superior to XGBoost for unseen attacks.
6. XGBoost is universally superior to LightGBM for unseen attacks.
7. Behavioral similarity significantly predicts unseen-family
   performance.
8. A causal relationship between similarity and transfer was
   established.
9. Raw PR-AUC known-minus-unseen difference is prevalence invariant.
10. Stage27 target thresholds were optimized using held-out-family
    labels.
11. Stage27 models were adapted or recalibrated after target opening.
12. The row bootstrap represents uncertainty across independent
    organizations or future production networks.

---

# J. Recommended Main-Manuscript Assets

## Main Table 27-1

Chronology-first family executability.

Source:

`docs/STAGE27_PUBLICATION_TABLES.md`

## Main Table 27-2

Primary ROC-AUC, PR-AUC, 95% intervals, held-out support, and BALANCED
recall for both learners.

Source:

`docs/STAGE27_PUBLICATION_TABLES.md`

## Main Figure 27-1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`

Purpose: show selective ranking transfer and learner dependence.

## Main Figure 27-2

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

Purpose: show ranking–threshold divergence.

## Supplementary Figure 27-S1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains co-primary and should remain in the main table and main
text even if the separate PR-AUC figure is supplementary.

## Supplementary tables

- complete STANDARD/BALANCED/SECURITY operating points;
- novelty-generalization gaps;
- behavioral similarity.

---

# K. Recommended Manuscript Placement

The Stage27 material should be integrated into the broader robustness
narrative rather than placed according to experimental stage number.

Recommended Results ordering:

1. Validation-safe baseline/model selection
2. Representation/architecture assessment
3. Temporal validation and forward generalization
4. Cross-dataset generalization
5. **Unseen attack-family generalization (Stage27)**
6. Low-prevalence and SOC operational stress
7. Deployment/computational profiling

This ordering moves from predictive evaluation toward increasingly
deployment-facing stress tests and keeps Stage27 adjacent to the
temporal and cross-dataset generalization evidence.
