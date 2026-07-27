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
