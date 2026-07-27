# Attack-Category Analysis

## Purpose

This stage evaluates the frozen balanced and security-oriented
operating points separately for each original attack category.
The original multiclass label was used only for post-selection
holdout analysis and was excluded from the predictor matrix.

## Data alignment

- Processed dataset: `/kaggle/input/datasets/jmmubasshirrahman/ids2018-balanced-binary-dataset/merged_balanced_ids2018_safe.csv`
- Original label column: `Label`
- Holdout records: 60,186
- Holdout attack records: 24,186
- Attack categories: 12
- Test-index key: `test_indices`

The reconstructed binary labels matched the saved holdout labels
exactly.

## Operating points

- XGBoost balanced: 0.51
- XGBoost security: 0.27
- LightGBM balanced: 0.50
- LightGBM security: 0.26

## Per-category detection rates

| Attack Category          |   Support |   lightgbm_balanced |   lightgbm_security |   xgboost_balanced |   xgboost_security |
|:-------------------------|----------:|--------------------:|--------------------:|-------------------:|-------------------:|
| Bot                      |      3998 |            0.998749 |            0.99975  |           0.9995   |           0.99975  |
| DDOS attack-HOIC         |      3970 |            1        |            1        |           1        |           1        |
| Infilteration            |      3967 |            0.244013 |            0.438367 |           0.244517 |           0.430804 |
| FTP-BruteForce           |      3950 |            1        |            1        |           1        |           1        |
| DoS attacks-SlowHTTPTest |      3721 |            1        |            1        |           1        |           1        |
| DoS attacks-GoldenEye    |      3141 |            1        |            1        |           1        |           1        |
| DoS attacks-Slowloris    |       820 |            1        |            1        |           1        |           1        |
| DoS attacks-Hulk         |       347 |            1        |            1        |           1        |           1        |
| Brute Force -Web         |       134 |            0.723881 |            0.820896 |           0.738806 |           0.798507 |
| DDOS attack-LOIC-UDP     |        75 |            1        |            1        |           1        |           1        |
| Brute Force -XSS         |        50 |            0.94     |            0.98     |           0.94     |           0.98     |
| SQL Injection            |        13 |            0.923077 |            1        |           0.923077 |           1        |

## XGBoost balanced versus LightGBM security

The detection-rate difference is defined as XGBoost balanced
minus LightGBM security. Negative values therefore favor the
LightGBM security operating point.

| Attack Category          |   Support |   First Detection Rate |   Second Detection Rate |   Detection Rate Difference |   Difference CI Lower |   Difference CI Upper |   First Only Detected |   Second Only Detected |   Benjamini-Hochberg Adjusted P-value | Significant After BH 0.05   |
|:-------------------------|----------:|-----------------------:|------------------------:|----------------------------:|----------------------:|----------------------:|----------------------:|-----------------------:|--------------------------------------:|:----------------------------|
| Bot                      |      3998 |               0.9995   |                0.99975  |                   -0.00025  |             -0.001001 |              0        |                     0 |                      1 |                              1        | False                       |
| Brute Force -Web         |       134 |               0.738806 |                0.820896 |                   -0.08209  |             -0.134328 |             -0.037313 |                     0 |                     11 |                              0.005859 | True                        |
| Brute Force -XSS         |        50 |               0.94     |                0.98     |                   -0.04     |             -0.1      |              0        |                     0 |                      2 |                              1        | False                       |
| DDOS attack-HOIC         |      3970 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| DDOS attack-LOIC-UDP     |        75 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| DoS attacks-GoldenEye    |      3141 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| DoS attacks-Hulk         |       347 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| DoS attacks-SlowHTTPTest |      3721 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| DoS attacks-Slowloris    |       820 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| FTP-BruteForce           |      3950 |               1        |                1        |                    0        |              0        |              0        |                     0 |                      0 |                              1        | False                       |
| Infilteration            |      3967 |               0.244517 |                0.438367 |                   -0.193849 |             -0.205955 |             -0.181749 |                     1 |                    770 |                              0        | True                        |
| SQL Injection            |        13 |               0.923077 |                1        |                   -0.076923 |             -0.230769 |              0        |                     0 |                      1 |                              1        | False                       |

## Hardest supported attack categories

Only categories with at least
20 holdout records were included in
this ranking.

| Attack Category          |   Support |   lightgbm_balanced |   lightgbm_security |   xgboost_balanced |   xgboost_security |   Mean Detection Rate Across Operating Points |
|:-------------------------|----------:|--------------------:|--------------------:|-------------------:|-------------------:|----------------------------------------------:|
| Infilteration            |      3967 |            0.244013 |            0.438367 |           0.244517 |           0.430804 |                                      0.339425 |
| Brute Force -Web         |       134 |            0.723881 |            0.820896 |           0.738806 |           0.798507 |                                      0.770522 |
| Brute Force -XSS         |        50 |            0.94     |            0.98     |           0.94     |           0.98     |                                      0.96     |
| Bot                      |      3998 |            0.998749 |            0.99975  |           0.9995   |           0.99975  |                                      0.999437 |
| DDOS attack-HOIC         |      3970 |            1        |            1        |           1        |           1        |                                      1        |
| FTP-BruteForce           |      3950 |            1        |            1        |           1        |           1        |                                      1        |
| DoS attacks-SlowHTTPTest |      3721 |            1        |            1        |           1        |           1        |                                      1        |
| DoS attacks-GoldenEye    |      3141 |            1        |            1        |           1        |           1        |                                      1        |
| DoS attacks-Slowloris    |       820 |            1        |            1        |           1        |           1        |                                      1        |
| DoS attacks-Hulk         |       347 |            1        |            1        |           1        |           1        |                                      1        |

## Statistical method

- Individual detection-rate intervals use Wilson score
  confidence intervals.
- Paired detection-rate differences use
  1,000 paired bootstrap replicates.
- Exact McNemar tests compare discordant predictions.
- Benjamini-Hochberg adjustment controls the false discovery
  rate across attack categories.

## Limitations

Attack categories with small support have wide uncertainty.
Results reflect the category composition of this processed,
rebalanced dataset and do not establish external
generalization.
