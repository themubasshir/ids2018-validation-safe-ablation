# Calibration Assessment

## Purpose

This stage evaluates the reliability of the saved XGBoost and
LightGBM attack probabilities. It is a descriptive holdout
assessment and does not retrain, recalibrate, or alter either
model or threshold.

## Models and operating points

- Balanced model: XGBoost Tuned, threshold
  0.51
- Security-oriented model: LightGBM Tuned, threshold
  0.26

Calibration itself is threshold-independent, but the selected
thresholds are shown in the probability-distribution figures.

## Calibration metrics

| Model          |   Selected Threshold |   Brier Score |   Log Loss |   ECE Uniform 15 |   Adaptive ECE Quantile 15 |   Calibration Intercept |   Calibration Slope |
|:---------------|---------------------:|--------------:|-----------:|-----------------:|---------------------------:|------------------------:|--------------------:|
| XGBoost Tuned  |                 0.51 |      0.042774 |   0.141966 |         0.002593 |                   0.002697 |                0.099824 |             1.03941 |
| LightGBM Tuned |                 0.26 |      0.042754 |   0.142111 |         0.003242 |                   0.003836 |                0.177251 |             1.10048 |

Ideal calibration has:

- low Brier score and log loss;
- low ECE, MCE, and RMSCE;
- calibration intercept near zero;
- calibration slope near one.

## Paired bootstrap comparison

Difference convention: XGBoost minus LightGBM. All listed
calibration-error metrics are better when lower.

| Metric                   |   Point Estimate |   CI Lower |   CI Upper | Interpretation   |
|:-------------------------|-----------------:|-----------:|-----------:|:-----------------|
| Brier Score              |         2e-05    |  -0.000156 |   0.000197 | CI includes zero |
| Log Loss                 |        -0.000145 |  -0.000701 |   0.00041  | CI includes zero |
| ECE Uniform 15           |        -0.000649 |  -0.001627 |   0.000966 | CI includes zero |
| MCE Uniform 15           |        -0.043705 |  -0.110081 |   0.024694 | CI includes zero |
| RMSCE Uniform 15         |        -0.002236 |  -0.00501  |   0.002133 | CI includes zero |
| Adaptive ECE Quantile 15 |        -0.001139 |  -0.00209  |   0.000968 | CI includes zero |
| MCE Quantile 15          |         0.004698 |  -0.010084 |   0.011508 | CI includes zero |
| RMSCE Quantile 15        |        -0.000704 |  -0.003015 |   0.002306 | CI includes zero |

## Method

- Holdout records: 60,186
- Benign records: 36,000
- Attack records: 24,186
- Primary bin count: 15
- Bin-sensitivity counts: [10, 15, 20]
- Bootstrap replicates: 2,000
- Confidence level: 95%
- Random seed: 42

The same stratified bootstrap sample was used for both models in
each replicate.

## Important limitation

Calibration error estimates depend partly on bin count and
binning strategy. This stage therefore reports both equal-width
and equal-frequency estimates and includes sensitivity analysis
with 10, 15, and 20 bins.

No recalibration was fitted using holdout data. Any future Platt
scaling, isotonic regression, or other probability recalibration
must be fitted using training or validation data and evaluated
separately on holdout data.
