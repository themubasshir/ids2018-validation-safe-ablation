# Journal Extension Summary

The Stage 8-12 experiments strengthen the validation-safe repository with uncertainty, calibration, deployment, attack-level, and multi-seed robustness analyses. They do not claim a guaranteed journal tier; they provide additional evidence for a stronger and more transparent manuscript.

## Uncertainty

The paired bootstrap analysis used 2,000 class-stratified holdout replicates. For the balanced comparison, XGBoost at threshold `0.51` minus LightGBM at threshold `0.50` had confidence intervals including zero for precision, recall, F1, F2, FPR, FNR, ROC-AUC, and PR-AUC. The balanced model comparison is therefore statistically unresolved on the holdout sample.

For the constrained-security comparison, XGBoost at threshold `0.27` minus LightGBM at threshold `0.26` had recall difference `-0.0013644257008186278` with CI `[-0.002646158934921039, -8.269246671632757e-05]`, and FN difference `33.0` with CI `[2.0, 64.0]`. LightGBM security therefore missed fewer attacks and achieved higher recall.

## Calibration

Both final models were reasonably calibrated without recalibration. XGBoost had Brier score `0.04277372026730192`, log loss `0.14196578621655653`, and 15-bin equal-width ECE `0.0025925176372656377`. LightGBM had Brier score `0.04275382352223183`, log loss `0.14211088072820652`, and 15-bin equal-width ECE `0.0032418563690034628`. All paired calibration-difference intervals included zero, so no statistically resolved calibration winner was found.

## Operational Deployment

The operational cost analysis expresses deployment preference as a relative missed-attack to false-alert cost ratio. LightGBM security becomes preferable to LightGBM balanced when one missed attack costs more than `1.8407079646017699` false-positive investigations, with bootstrap CI `[1.6987043925893093, 1.9973514290693621]`. High FN:FP ratios selected thresholds near `0.05` and produced FPR above 40%, supporting the explicit FPR <= 5% security constraint.

## Attack-Level Performance

The holdout set contains 12 attack categories. Most DoS/DDoS categories and FTP brute force achieved 100% detection across operating points. Residual difficulty is concentrated in `Infilteration`, where LightGBM security detected `1739` of `3967` examples, and `Brute Force -Web`, where it detected `110` of `134` examples. `SQL Injection` has only `13` holdout examples, so category-specific claims there are fragile.

## Robustness Across Seeds

The fixed-hyperparameter multi-seed study repeated splitting, fitting, validation threshold selection, and holdout evaluation for seeds `42`, `52`, `62`, `72`, and `82`. The full hyperparameter search was not repeated for each seed. XGBoost won the balanced objective in `3` of `5` seeds, while LightGBM won the security objective in `4` of `5` seeds.

## Remaining Limitation

All analyses remain single-dataset evaluations on the processed CSE-CIC-IDS2018 binary dataset. The extension improves uncertainty accounting and deployment interpretation, but cross-dataset generalization remains future work.

<!-- BEGIN STAGE22R JOURNAL EXTENSION SUMMARY -->

## Stage22R — Source-Faithful Temporal Validation Stress Test

Stage22R adds a precommitted four-cell ablation over development split
(`RANDOM` versus `CHRONOLOGICAL`) and training prevalence (`NATURAL` versus
training-only `REBALANCED`) while evaluating every frozen cell on one common
forward Mar1--Mar2 holdout.

After exact K79 cleaning, the final evaluation set contains **1,374,133** rows
with attack prevalence **0.273150**. Exact
development-to-final K79 overlap is **zero**.

The random cells are nearly perfect on their development validation membership
but fall to final ROC-AUC **0.5205** and
**0.5420**. The chronological cells are near chance on
Feb28 validation yet reach final ROC-AUC **0.8064** and
**0.8322**. The largest observed final PR-AUC is
**0.6926** for Chronological/Rebalanced, but no
post-holdout model selection is permitted.

Frozen operating thresholds transfer poorly. Chronological thresholds almost
never fire despite substantially better final ranking, whereas the random
security operating points reach final FPR **0.2870** and
**0.2685**, violating the development-era 5% FPR constraint.

The result supports strong temporal/distribution heterogeneity and a need to
separate ranking generalization from operating-point transfer. It does not
prove session independence or a specific mechanism such as concept drift.

See `docs/STAGE22R_MANUSCRIPT_INTEGRATION.md` and
`docs/STAGE22R_PUBLICATION_FIGURES_AND_CLOSEOUT.md`.

<!-- END STAGE22R JOURNAL EXTENSION SUMMARY -->

<!-- BEGIN STAGE24 JOURNAL EXTENSION SUMMARY -->

## Stage24 — Bidirectional Cross-Dataset Generalization

Stage24 closes the earlier cross-dataset future-work gap through a frozen
bidirectional audit between CSE-CIC-IDS2018 and CICIDS2017.

IDS2018-to-CICIDS2017 transfer retained substantial ranking signal. The
62-feature bridge achieved PR-AUC
**0.667483**
and ROC-AUC
**0.733946**
on **2,830,743** effective CICIDS2017 rows.

The reciprocal CICIDS2017-to-IDS2018 transfer was much weaker. On the frozen
IDS2018 Feb-28 target, attack prevalence was
**0.104847**, while bridge62 reached PR-AUC
**0.108176**
and ROC-AUC
**0.525167**.

A preregistered serialization audit further showed that correcting the
CICIDS2017 aggregate flag mapping changed primary bridge70 PR-AUC by
**-0.007729**, ROC-AUC by
**+0.002192**, and Brier score by
**+0.005087**. The corresponding paired
95% bootstrap intervals excluded zero.

The two transfer directions are reported separately and are not averaged.
No target-guided fitting, target threshold tuning, calibration, or feature
search was performed.

Two GROUNDED_S4 target cells were administratively cancelled before opening
because exact durable physical-row membership could not be reconstructed
without introducing a new post-freeze heuristic. No fuzzy substitute was used
and the cancelled slots were not reallocated.

Stage24 therefore supersedes the earlier statement that cross-dataset
generalization remained untested.

Publication package:

- `docs/STAGE24_MANUSCRIPT_INTEGRATION.md`
- `docs/STAGE24_PUBLICATION_TABLES.md`
- `docs/STAGE24_PUBLICATION_CLOSEOUT.md`
- `figures/stage24_cross_dataset/`
- `scripts/stage24/`

<!-- END STAGE24 JOURNAL EXTENSION SUMMARY -->

<!-- STAGE25_JOURNAL_EXTENSION_CLOSEOUT -->
## Stage25 — Deployment Prevalence and SOC Operational Stress

Stage25 is now scientifically closed. The stage uses the frozen Stage22
random/chronological and Stage24 bidirectional cross-dataset operating
points and performs no new model fitting or target access.

The extension contributes a prior-shift deployment analysis across
10%, 3%, 1%, 0.3%, 0.1%, and 0.01% attack prevalence. It reports PPV,
NPV, likelihood-ratio evidence translation, exact PPV thresholds,
required FPR for target PPV, projected false/true alert volume,
analyst-processing workload, SOC capacity exceedance, and a frozen
relative cost model.

At 0.1% prevalence the Stage22 random STANDARD operating point retains
PPV 0.965572 but still requires
33.5
analyst-hours/day because true positives themselves consume capacity.
The chronological STANDARD operating point instead projects PPV
0.000551068 with only
0.0322 true alerts/day, showing why
capacity fit cannot be equated with operational usefulness.

The primary IDS2018→CICIDS2017 STANDARD transfer projects PPV
0.039233–0.060313 at 0.1%,
whereas the reverse CICIDS2017→IDS2018 STANDARD direction projects only
0.000257610–0.000287993.
Under the frozen 1:100 relative-cost scenario, 15/24 operating points
favor the model at 0.1% prevalence but only 3/24 do so at 0.01%.

All seven preregistered sanity checks pass and all five preregistered
figures are retained.

Stage25-4 frozen result SHA:
`8fcc28f0ce2a616a166f22f4a33d0c76001f8ef9a337739bd32c14778932c205`
