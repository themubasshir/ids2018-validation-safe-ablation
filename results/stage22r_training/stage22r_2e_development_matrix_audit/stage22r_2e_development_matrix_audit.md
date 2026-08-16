# Stage22R-2E — Four-Cell Development Matrix Audit

## Governance

- Development cells completed: **4 / 4**
- Mar1-Mar2 opened: **NO**
- Final opening consumed: **0 / 1**
- Post-validation model choice: **FORBIDDEN**
- Final holdout rule: **all four frozen cells, all frozen operating points, one opening**

## Development Matrix

| Cell | PR-AUC | ROC-AUC | Balanced threshold | Balanced F1 | Balanced recall |
|---|---:|---:|---:|---:|---:|
| RANDOM_NATURAL | 0.9955900419 | 0.9986245648 | 0.46 | 0.9838817869 | 0.9686406733 |
| RANDOM_REBALANCED | 0.9953050760 | 0.9985208507 | 0.70 | 0.9838961012 | 0.9692060031 |
| CHRONOLOGICAL_NATURAL | 0.1062151551 | 0.5149184264 | 0.07 | 0.0001596934 | 0.0000803135 |
| CHRONOLOGICAL_REBALANCED | 0.1037391803 | 0.4993701958 | 0.07 | 0.0004083107 | 0.0002088152 |

## Frozen Development Interpretation

Both RANDOM development cells show high discrimination, whereas both strict-forward CHRONOLOGICAL cells collapse on Feb28.

Training-only rebalancing does not rescue the chronological failure.

The gap remains after exact K79 identity/conflict control. This does not establish session, 5-tuple, source-IP, or endpoint independence.

Random-versus-chronological development metrics use different validation memberships; therefore the protocol-defined primary comparison remains the shared Mar1-Mar2 final holdout.

## Final Holdout Contract

The single authorized Mar1-Mar2 opening must evaluate all four already-frozen cells and all already-frozen STANDARD/BALANCED/SECURITY operating points in one reporting pass. No winner is selected from development.
