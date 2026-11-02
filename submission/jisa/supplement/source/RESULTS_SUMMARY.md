# Results Summary

Exact values below are copied from archived CSV and JSON artifacts.

## Split Summary

| Split | Records | Benign | Attack |
| --- | ---: | ---: | ---: |
| Training | 192593 | 115200 | 77393 |
| Validation | 48149 | 28800 | 19349 |
| Holdout Test | 60186 | 36000 | 24186 |

## Baseline Leader

XGBoost ranked first in the 16-model validation ablation at threshold `0.5`, with accuracy `0.9434463851793392`, precision `0.9861972160486606`, recall `0.8714662256447362`, F1 `0.925288775482207`, and FPR `0.0081944444444444`.

## Tuned Top-Five Validation Leader

XGBoost Tuned ranked first at threshold `0.5`, with accuracy `0.9446509792519056`, precision `0.9869250525332712`, recall `0.8738436094888625`, F1 `0.9269482744442312`, and FPR `0.0077777777777777`.

## Selected Validation Operating Points

Balanced point: XGBoost Tuned, maximum validation F1 at threshold `0.51`, precision `0.9880123969358517`, recall `0.8732234223990903`, F1 `0.9270781893004115`, F2 `0.8939966348138036`, FPR `0.007118055555555555`, FN `2453`.

Constrained-security point: LightGBM Tuned, maximum validation F2 subject to FPR <= 5%, threshold `0.26`, precision `0.9267348778031066`, recall `0.9034575430254793`, F1 `0.9149481838166021`, F2 `0.9080189904320635`, FPR `0.04798611111111111`, FN `1868`.

## Holdout Results

Balanced holdout point: XGBoost Tuned at threshold `0.51`, accuracy `0.9458844249493238`, precision `0.9897505499134179`, recall `0.8743901430579675`, F1 `0.9285008671218141`, F2 `0.8952595439882822`, FPR `0.006083333333333333`, FN `3038`, ROC-AUC `0.9801912125472036`, PR-AUC `0.9776433333080397`.

Constrained-security holdout point: LightGBM Tuned at threshold `0.26`, accuracy `0.9347024224902801`, precision `0.9290071162317859`, recall `0.90680559001075`, F1 `0.9177721052851823`, F2 `0.9111605955862803`, FPR `0.04655555555555556`, FN `2254`, ROC-AUC `0.9802072525887335`, PR-AUC `0.9776909621341594`.

## SHAP Agreement

The dual-model SHAP comparison used 5,000 holdout records: 2,500 benign and 2,500 attack. Shared top-20 features: `15`. Top-20 Jaccard similarity: `0.6`. Spearman rank correlation: `0.8540662778147889`. Spearman p-value: `2.839526154790284e-23`. Common top three: `Init Fwd Win Byts`, `Fwd Seg Size Min`, and `Dst Port`.

See `results/comparison/generated_results_summary.md` for generated tables.

## Stage 8: Bootstrap Confidence

Balanced XGBoost `0.51` minus LightGBM `0.50` has confidence intervals including zero for precision, recall, F1, F2, FPR, FNR, ROC-AUC, and PR-AUC. For example, F1 difference is `0.000185061470508896` with CI `[-0.0004952955263602676, 0.0008619090916325816]`.

Security XGBoost `0.27` minus LightGBM `0.26` has recall difference `-0.0013644257008186278` with CI `[-0.002646158934921039, -8.269246671632757e-05]`, and FN difference `33.0` with CI `[2.0, 64.0]`.

## Stage 9: Calibration

XGBoost: Brier `0.04277372026730192`, log loss `0.14196578621655653`, 15-bin uniform ECE `0.0025925176372656377`.

LightGBM: Brier `0.04275382352223183`, log loss `0.14211088072820652`, 15-bin uniform ECE `0.0032418563690034628`.

All paired calibration-difference intervals include zero.

## Stage 10: Operational Cost

Break-even FN:FP ratios:

| Comparison | Additional FP | FN reduced | Break-even ratio | Bootstrap CI |
| --- | ---: | ---: | ---: | --- |
| XGBoost Security vs XGBoost Balanced | 1435 | 751 | 1.9107856191744341 | [1.7557153734902833, 2.0803045624172385] |
| LightGBM Security vs LightGBM Balanced | 1456 | 791 | 1.8407079646017699 | [1.6987043925893093, 1.9973514290693621] |
| LightGBM Security vs XGBoost Balanced | 1457 | 784 | 1.8584183673469388 | [1.7128947748789476, 2.026500762079631] |

At high FN:FP ratios, unconstrained threshold selection used threshold `0.05`, producing FPR `0.41225` for XGBoost and `0.43033333333333335` for LightGBM.

## Stage 11: Attack Categories

There are 12 attack categories. Supports include `Infilteration`: `3967`, `Brute Force -Web`: `134`, and `SQL Injection`: `13`.

Infilteration detection rates: XGBoost balanced `0.24451726745651625`, XGBoost security `0.43080413410637763`, LightGBM balanced `0.24401310814217292`, LightGBM security `0.4383665238215276`.

Brute Force -Web detection rates: XGBoost balanced `0.7388059701492538`, XGBoost security `0.7985074626865671`, LightGBM balanced `0.7238805970149254`, LightGBM security `0.8208955223880597`.

XGBoost balanced versus LightGBM security is significant after Benjamini-Hochberg correction for `Infilteration` and `Brute Force -Web`.

## Stage 12: Multi-Seed Robustness

Seeds: `42`, `52`, `62`, `72`, `82`.

Winner frequency: balanced XGBoost `3/5`, balanced LightGBM `2/5`, security LightGBM `4/5`, security XGBoost `1/5`.

Threshold stability:

| Model | Objective | Mean | SD | Range |
| --- | --- | ---: | ---: | --- |
| LightGBM Tuned | Balanced | 0.43599999999999994 | 0.0260768096208106 | 0.41-0.47 |
| LightGBM Tuned | Security | 0.266 | 0.0054772255750516665 | 0.26-0.27 |
| XGBoost Tuned | Balanced | 0.476 | 0.027018512172212596 | 0.44-0.51 |
| XGBoost Tuned | Security | 0.274 | 0.008944271909999165 | 0.26-0.28 |
