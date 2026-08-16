# Stage22R Final Single-Opening Holdout Report

## Governance

- Mar1-Mar2 final holdout opening consumed: **1 / 1**
- Raw holdout files after materialization: **PERMANENTLY CLOSED**
- Frozen model cells evaluated: **4 / 4**
- Frozen operating points evaluated: **12 / 12**
- Post-validation model selection: **NONE**
- Post-holdout model selection: **FORBIDDEN / NONE**

## Shared K79-Clean Final Holdout

- Rows: **1,374,133**
- Benign: **998,788**
- Attack: **375,345**
- Attack prevalence: **0.2731504156**
- Development-overlap exclusions: **0**
- Conflicting-label exclusions: **10**
- Same-label duplicate exclusions: **5,532**

## Four Frozen Cells

| Cell | PR-AUC | ROC-AUC | Standard F1 | Balanced F1 | Security F2 |
|---|---:|---:|---:|---:|---:|
| RANDOM_NATURAL | 0.2629532196 | 0.5204903285 | 0.0021595802 | 0.0028163925 | 0.0928518893 |
| RANDOM_REBALANCED | 0.2732977162 | 0.5419818376 | 0.0409609829 | 0.0093071763 | 0.0923574757 |
| CHRONOLOGICAL_NATURAL | 0.6107344876 | 0.8064180162 | 0.0000426217 | 0.0002024178 | 0.0001265405 |
| CHRONOLOGICAL_REBALANCED | 0.6926302657 | 0.8321639646 | 0.0002130765 | 0.0003886193 | 0.0002430540 |

## Interpretation Boundary

This is the protocol-defined primary Stage22R comparison because all four already-frozen model cells are evaluated on the same forward chronological Mar1-Mar2 final holdout.

K79 is an exact identity control over corrected timestamp second plus the 78 common numeric predictors. It does not establish session, 5-tuple, attacker-source-IP, or endpoint independence.

No model, threshold, calibration, feature, preprocessing, or model choice may be changed on the basis of this holdout.
