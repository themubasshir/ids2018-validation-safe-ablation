# Operational Cost Analysis

## Purpose

This stage converts threshold-level false positives and false
negatives into deployment-oriented quantities. Thresholds for
each cost ratio were selected using validation data only and
were then evaluated descriptively on the holdout set.

## Cost function

The relative operational cost is:

`Cost = C_FP × FP + C_FN × FN`

The false-positive unit cost is fixed at one. The analyzed
false-negative to false-positive cost ratios are:

[1, 2, 5, 10, 20, 50, 100]

These are relative cost scenarios, not monetary estimates.

## Validation-selected cost-sensitive thresholds

| Model          |   FN to FP Cost Ratio |   Selected Threshold |   Validation Recall |   Validation F2 |   Validation FPR |   Validation FP |   Validation FN |
|:---------------|----------------------:|---------------------:|--------------------:|----------------:|-----------------:|----------------:|----------------:|
| XGBoost Tuned  |                     1 |                 0.51 |            0.873223 |        0.893997 |         0.007118 |             205 |            2453 |
| XGBoost Tuned  |                     2 |                 0.35 |            0.887643 |        0.90219  |         0.021319 |             614 |            2174 |
| XGBoost Tuned  |                     5 |                 0.16 |            0.943976 |        0.91367  |         0.149062 |            4293 |            1084 |
| XGBoost Tuned  |                    10 |                 0.08 |            0.983927 |        0.897722 |         0.333368 |            9601 |             311 |
| XGBoost Tuned  |                    20 |                 0.05 |            0.994005 |        0.885481 |         0.415729 |           11973 |             116 |
| XGBoost Tuned  |                    50 |                 0.05 |            0.994005 |        0.885481 |         0.415729 |           11973 |             116 |
| XGBoost Tuned  |                   100 |                 0.05 |            0.994005 |        0.885481 |         0.415729 |           11973 |             116 |
| LightGBM Tuned |                     1 |                 0.5  |            0.872603 |        0.893485 |         0.007083 |             204 |            2465 |
| LightGBM Tuned |                     2 |                 0.32 |            0.894258 |        0.904978 |         0.03125  |             900 |            2046 |
| LightGBM Tuned |                     5 |                 0.14 |            0.957104 |        0.912266 |         0.193924 |            5585 |             830 |
| LightGBM Tuned |                    10 |                 0.08 |            0.987234 |        0.895127 |         0.354236 |           10202 |             247 |
| LightGBM Tuned |                    20 |                 0.05 |            0.995607 |        0.882738 |         0.432465 |           12455 |              85 |
| LightGBM Tuned |                    50 |                 0.05 |            0.995607 |        0.882738 |         0.432465 |           12455 |              85 |
| LightGBM Tuned |                   100 |                 0.05 |            0.995607 |        0.882738 |         0.432465 |           12455 |              85 |

## Break-even analysis

The break-even ratio indicates how many false-positive
investigations are operationally equivalent to one missed
attack. A security operating point becomes less costly than its
reference point when the relative false-negative cost exceeds
the break-even ratio.

| Comparison                             |   Additional False Positives |   False Negatives Reduced |   Additional False Alerts per Additional Attack Detected |   Bootstrap CI Lower |   Bootstrap CI Upper |
|:---------------------------------------|-----------------------------:|--------------------------:|---------------------------------------------------------:|---------------------:|---------------------:|
| XGBoost Security vs XGBoost Balanced   |                         1435 |                       751 |                                                  1.91079 |              1.75571 |              2.08031 |
| LightGBM Security vs LightGBM Balanced |                         1456 |                       791 |                                                  1.84071 |              1.6987  |              1.99735 |
| LightGBM Security vs XGBoost Balanced  |                         1457 |                       784 |                                                  1.85842 |              1.7129  |              2.0265  |

## Normalized alert burden

| Operating Point   |   Threshold |   False Alerts per 10,000 Benign Flows |   Missed Attacks per 10,000 Attacks |   Detected Attacks per 10,000 Attacks |   False Alert Share of All Alerts |
|:------------------|------------:|---------------------------------------:|------------------------------------:|--------------------------------------:|----------------------------------:|
| XGBoost Standard  |        0.5  |                                64.1667 |                            1250.72  |                               8749.28 |                          0.010798 |
| XGBoost Balanced  |        0.51 |                                60.8333 |                            1256.1   |                               8743.9  |                          0.010249 |
| XGBoost Security  |        0.27 |                               459.444  |                             945.588 |                               9054.41 |                          0.070225 |
| LightGBM Balanced |        0.5  |                                61.1111 |                            1258.99  |                               8741.01 |                          0.010299 |
| LightGBM Security |        0.26 |                               465.556  |                             931.944 |                               9068.06 |                          0.070993 |

## Interpretation

The additional-false-alerts-per-additional-attack quantity
measures the investigation burden associated with the improved
attack-detection rate. It should be interpreted together with
analyst capacity and the real consequences of missed attacks.

## Limitations

- The cost ratios are hypothetical relative values.
- No monetary incident-loss assumptions are introduced.
- Alert correlation and analyst triage efficiency are not
  represented.
- Holdout data were not used to select any threshold.
