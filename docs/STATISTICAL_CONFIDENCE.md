# Statistical Confidence Analysis

## Purpose

This stage quantifies sampling uncertainty around the frozen
validation-selected operating points using a paired,
class-stratified percentile bootstrap.

## Method

- Bootstrap replicates: 2,000
- Confidence level: 95%
- Random seed: 42
- Holdout records: 60,186
- Benign records: 36,000
- Attack records: 24,186
- Pairing: identical sampled records were used for both models
  in every replicate.
- Stratification: benign and attack records were sampled
  separately while preserving the original class counts.

## Frozen operating points

- XGBoost standard: 0.50
- XGBoost balanced: 0.51
- XGBoost security: 0.27
- LightGBM balanced: 0.50
- LightGBM security: 0.26

## Operating-point confidence intervals

| Operating Point Key   | Metric    |   Point Estimate |   CI Lower |   CI Upper |
|:----------------------|:----------|-----------------:|-----------:|-----------:|
| xgboost_standard      | Precision |         0.989202 |   0.98787  |   0.990541 |
| xgboost_standard      | Recall    |         0.874928 |   0.870875 |   0.879187 |
| xgboost_standard      | F1-score  |         0.928562 |   0.926215 |   0.93105  |
| xgboost_standard      | F2-score  |         0.89562  |   0.892199 |   0.899196 |
| xgboost_standard      | FPR       |         0.006417 |   0.005611 |   0.007222 |
| xgboost_standard      | FNR       |         0.125072 |   0.120813 |   0.129125 |
| xgboost_standard      | ROC-AUC   |         0.980191 |   0.979264 |   0.981094 |
| xgboost_standard      | PR-AUC    |         0.977643 |   0.976657 |   0.978621 |
| xgboost_balanced      | Precision |         0.989751 |   0.988453 |   0.991069 |
| xgboost_balanced      | Recall    |         0.87439  |   0.870338 |   0.878649 |
| xgboost_balanced      | F1-score  |         0.928501 |   0.926147 |   0.930989 |
| xgboost_balanced      | F2-score  |         0.89526  |   0.891908 |   0.898834 |
| xgboost_balanced      | FPR       |         0.006083 |   0.005306 |   0.006861 |
| xgboost_balanced      | FNR       |         0.12561  |   0.121351 |   0.129662 |
| xgboost_balanced      | ROC-AUC   |         0.980191 |   0.979264 |   0.981094 |
| xgboost_balanced      | PR-AUC    |         0.977643 |   0.976657 |   0.978621 |
| xgboost_security      | Precision |         0.929775 |   0.926718 |   0.932726 |
| xgboost_security      | Recall    |         0.905441 |   0.901927 |   0.90908  |
| xgboost_security      | F1-score  |         0.917447 |   0.914951 |   0.919891 |
| xgboost_security      | F2-score  |         0.910206 |   0.90725  |   0.913234 |
| xgboost_security      | FPR       |         0.045944 |   0.043833 |   0.048056 |
| xgboost_security      | FNR       |         0.094559 |   0.09092  |   0.098073 |
| xgboost_security      | ROC-AUC   |         0.980191 |   0.979264 |   0.981094 |
| xgboost_security      | PR-AUC    |         0.977643 |   0.976657 |   0.978621 |
| lightgbm_balanced     | Precision |         0.989701 |   0.988356 |   0.991021 |
| lightgbm_balanced     | Recall    |         0.874101 |   0.870007 |   0.878277 |
| lightgbm_balanced     | F1-score  |         0.928316 |   0.925939 |   0.93075  |
| lightgbm_balanced     | F2-score  |         0.895009 |   0.891619 |   0.898522 |
| lightgbm_balanced     | FPR       |         0.006111 |   0.005333 |   0.006917 |
| lightgbm_balanced     | FNR       |         0.125899 |   0.121723 |   0.129993 |
| lightgbm_balanced     | ROC-AUC   |         0.980207 |   0.979263 |   0.981137 |
| lightgbm_balanced     | PR-AUC    |         0.977691 |   0.976713 |   0.978677 |
| lightgbm_security     | Precision |         0.929007 |   0.925926 |   0.931992 |
| lightgbm_security     | Recall    |         0.906806 |   0.90325  |   0.910444 |
| lightgbm_security     | F1-score  |         0.917772 |   0.915248 |   0.920175 |
| lightgbm_security     | F2-score  |         0.911161 |   0.908176 |   0.914209 |
| lightgbm_security     | FPR       |         0.046556 |   0.044472 |   0.04875  |
| lightgbm_security     | FNR       |         0.093194 |   0.089556 |   0.09675  |
| lightgbm_security     | ROC-AUC   |         0.980207 |   0.979263 |   0.981137 |
| lightgbm_security     | PR-AUC    |         0.977691 |   0.976713 |   0.978677 |

## Balanced paired comparison

Difference convention: XGBoost 0.51 minus LightGBM 0.50.

| Metric    |   Point Estimate |   CI Lower |   CI Upper | CI Interpretation   |
|:----------|-----------------:|-----------:|-----------:|:--------------------|
| Precision |         5e-05    |  -0.000911 |   0.000987 | CI includes zero    |
| Recall    |         0.000289 |  -0.00062  |   0.001241 | CI includes zero    |
| F1-score  |         0.000185 |  -0.000495 |   0.000862 | CI includes zero    |
| F2-score  |         0.000251 |  -0.000525 |   0.001077 | CI includes zero    |
| FPR       |        -2.8e-05  |  -0.000584 |   0.000556 | CI includes zero    |
| FNR       |        -0.000289 |  -0.001241 |   0.00062  | CI includes zero    |
| ROC-AUC   |        -1.6e-05  |  -0.000248 |   0.00021  | CI includes zero    |
| PR-AUC    |        -4.8e-05  |  -0.000281 |   0.000175 | CI includes zero    |

## Security paired comparison

Difference convention: XGBoost 0.27 minus LightGBM 0.26.

| Metric    |   Point Estimate |   CI Lower |   CI Upper | CI Interpretation    |
|:----------|-----------------:|-----------:|-----------:|:---------------------|
| Precision |         0.000768 |  -0.001283 |   0.002844 | CI includes zero     |
| Recall    |        -0.001364 |  -0.002646 |  -8.3e-05  | Entire CI below zero |
| F1-score  |        -0.000325 |  -0.001559 |   0.000915 | CI includes zero     |
| F2-score  |        -0.000955 |  -0.002081 |   0.000194 | CI includes zero     |
| FPR       |        -0.000611 |  -0.002056 |   0.000806 | CI includes zero     |
| FNR       |         0.001364 |   8.3e-05  |   0.002646 | Entire CI above zero |

## Within-model threshold trade-offs

| Comparison               | Metric    |   Point Estimate |    CI Lower |    CI Upper | CI Interpretation    |
|:-------------------------|:----------|-----------------:|------------:|------------:|:---------------------|
| XGBoost 0.51 minus 0.50  | Precision |         0.000549 |    0.000269 |    0.000876 | Entire CI above zero |
| XGBoost 0.51 minus 0.50  | Recall    |        -0.000538 |   -0.000868 |   -0.000248 | Entire CI below zero |
| XGBoost 0.51 minus 0.50  | F1-score  |        -6.1e-05  |   -0.000283 |    0.000155 | CI includes zero     |
| XGBoost 0.51 minus 0.50  | F2-score  |        -0.000361 |   -0.000628 |   -0.00012  | Entire CI below zero |
| XGBoost 0.51 minus 0.50  | FPR       |        -0.000333 |   -0.000528 |   -0.000167 | Entire CI below zero |
| XGBoost 0.51 minus 0.50  | FNR       |         0.000538 |    0.000248 |    0.000868 | Entire CI above zero |
| XGBoost 0.51 minus 0.50  | FP        |       -12        |  -19        |   -6        | Entire CI below zero |
| XGBoost 0.51 minus 0.50  | FN        |        13        |    6        |   21        | Entire CI above zero |
| LightGBM 0.26 minus 0.50 | Precision |        -0.060694 |   -0.063606 |   -0.057868 | Entire CI below zero |
| LightGBM 0.26 minus 0.50 | Recall    |         0.032705 |    0.030596 |    0.034897 | Entire CI above zero |
| LightGBM 0.26 minus 0.50 | F1-score  |        -0.010544 |   -0.012432 |   -0.008754 | Entire CI below zero |
| LightGBM 0.26 minus 0.50 | F2-score  |         0.016152 |    0.014297 |    0.018045 | Entire CI above zero |
| LightGBM 0.26 minus 0.50 | FPR       |         0.040444 |    0.038472 |    0.042528 | Entire CI above zero |
| LightGBM 0.26 minus 0.50 | FNR       |        -0.032705 |   -0.034897 |   -0.030596 | Entire CI below zero |
| LightGBM 0.26 minus 0.50 | FP        |      1456        | 1384.97     | 1531        | Entire CI above zero |
| LightGBM 0.26 minus 0.50 | FN        |      -791        | -844.025    | -740        | Entire CI below zero |

## Interpretation rule

An interval entirely above zero supports a positive difference
for the first operating point. An interval entirely below zero
supports a negative difference. An interval containing zero
means the holdout bootstrap does not clearly resolve the
difference; it does not prove equivalence.

## Limitation

These intervals quantify holdout-sample uncertainty conditional
on the models, hyperparameters, and thresholds selected from the
validation workflow. They do not incorporate uncertainty from
repeating the complete model-selection procedure across
different random splits.
