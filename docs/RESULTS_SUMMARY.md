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
