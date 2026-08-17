
# Stage23 Final Scientific Synthesis

## Frozen scope

Stage23 is a development-only validation-sensitivity and shortcut-feature audit.
It contains seven frozen primary representations, five matched-size placebo removals,
six frozen depth-1 stump controls, paired stratified bootstrap uncertainty,
component-specific TreeSHAP proxy-absorption analysis, and frozen attack-family
conditioning.

Raw Mar1 and Mar2 remain permanently forbidden. Stage23 does not create a new
untouched final holdout.

## Full-model validation-regime contrast

### RANDOM_NATURAL

- PR-AUC: 0.995590041899
- ROC-AUC: 0.998624564774
- Attack prevalence: 0.136847389454
- PR-AUC minus attack prevalence:
  0.858742652446

### CHRONOLOGICAL_NATURAL

- PR-AUC: 0.106215155134
- ROC-AUC: 0.514918426394
- Attack prevalence: 0.104846912998
- PR-AUC minus attack prevalence:
  0.001368242136

The FULL ensemble therefore shows extreme validation-regime sensitivity. Random-natural
validation is highly discriminative, whereas chronological-natural ranking is close to
the relevant no-skill references.

## Primary ablations

The frozen shortcut interaction is:

(FULL_RANDOM - ABLATED_RANDOM)
-
(FULL_CHRONOLOGICAL - ABLATED_CHRONOLOGICAL)

A positive interaction means random validation benefits disproportionately from the
tested information relative to chronological validation. A negative interaction means
chronological validation depends more strongly on the tested information.

Primary PR-AUC interactions whose frozen 95% bootstrap CIs exclude zero:

- NO_DST_PORT
- NO_PORTS
- NO_INIT_FWD_WIN_BYTS
- NO_FWD_SEG_SIZE_MIN
- NO_SUSPICIOUS_GROUP

Primary ROC-AUC interactions whose frozen 95% bootstrap CIs exclude zero:

- NO_DST_PORT
- NO_PORTS
- NO_FWD_SEG_SIZE_MIN
- NO_SUSPICIOUS_GROUP
- BEHAVIOR_ONLY

The directions are not uniform across subsets or ranking metrics. Therefore Stage23
does not support a binary leakage/not-leakage interpretation.

## Matched-size placebo context

Placebo PR-AUC interactions whose frozen CIs exclude zero:

- PLACEBO_VOLUME_DIRECTION
- PLACEBO_IAT
- PLACEBO_PACKET_SIZE

Placebo ROC-AUC interactions whose frozen CIs exclude zero:

- PLACEBO_VOLUME_DIRECTION
- PLACEBO_IAT
- PLACEBO_PACKET_SIZE

Matched-size placebo removals also produce non-zero interactions and CI exclusion.
Thus CI exclusion from zero is not unique to the pre-specified suspicious groups and
cannot by itself establish leakage.

## Single-feature stump controls

Dst Port, Init Fwd Win Byts, and Fwd Seg Size Min individually discriminate much more
strongly under RANDOM_NATURAL than under CHRONOLOGICAL_NATURAL. Their forward-temporal
degradation is consistent with split-specific or shortcut-like information that
transfers poorly. It is not proof of leakage or causality.

## SHAP proxy absorption

TreeSHAP remains component-specific for LightGBM and XGBoost. Figure 23-D uses only a
descriptive equal-weight consensus of normalized component mean-absolute SHAP shares.
It is not exact SHAP for the probability-averaged ensemble.

Ablation changes retained-feature ranks and normalized importance shares. These shifts
are consistent with proxy absorption but do not establish causal substitution.

## Behavior-restricted representation

RANDOM_NATURAL BEHAVIOR_ONLY:

- PR-AUC: 0.981588003857
- ROC-AUC: 0.996141240052
- F1@0.50: 0.946546500675

CHRONOLOGICAL_NATURAL BEHAVIOR_ONLY:

- PR-AUC: 0.095539807865
- ROC-AUC: 0.476481778469
- F1@0.50: 0.029455282147

The behavior-restricted representation does not retain strong chronological
discrimination under the frozen Stage23 protocol. This does not mean BEHAVIOR_ONLY
equals real-world deployment performance.

## Attack-family context

RANDOM_NATURAL contains 394,460 attack validation rows and
11 families meeting the frozen minimum support of 100.

CHRONOLOGICAL_NATURAL contains 62,256 attack validation rows.
All chronological attack support belongs to Infilteration under the frozen family
mapping; the other 12 development families have zero chronological attack support.

The random-versus-chronological comparison therefore combines temporal change with
a major attack-family composition change. Stage23 cannot attribute the entire split
gap to a single feature or leakage mechanism.

## Consolidated conclusion

The frozen Stage23 evidence supports the following bounded conclusions:

1. The evaluated ensemble is highly sensitive to validation regime.
2. Several individually discriminative cues transfer poorly to chronological validation.
3. Feature-removal interactions are metric- and subset-dependent.
4. Matched-size placebo interactions caution against treating statistical significance
   as leakage evidence.
5. SHAP redistribution is consistent with proxy absorption, not causal proof.
6. Chronological attack support is entirely Infilteration, materially limiting
   attack-family comparability.
7. The overall evidence supports validation sensitivity and poor temporal transfer,
   not a claim that any tested feature is proven leakage.

## Claims explicitly prohibited by the frozen interpretation matrix

- Dst Port is leakage
- Init Fwd Win Byts is leakage
- Fwd Seg Size Min is leakage
- Random splitting is universally invalid
- Chronological splitting completely eliminates leakage
- K79 provides session independence
- K79 provides endpoint/IP/5-tuple disjointness
- Removing suspicious features proves causal reliance
- SHAP importance proves causation
- Behavior-only performance equals real-world deployment performance
- Stage23 has a new untouched final holdout

## Governance

- Stage23 fit budget: 50 / 50 SEALED.
- Additional fits authorized: 0.
- Model fits in Stage23-7A-R5: 0.
- Model inference: 0.
- LightGBM execution: 0.
- XGBoost execution: 0.
- New SHAP computation: 0.
- New bootstrap sampling: 0.
- Model files read: 0.
- Probability NPZ files read: 0.
- Parquet files read: 0.
- Raw Mar1 accessed: NO.
- Raw Mar2 accessed: NO.
- Repository modified: NO.
