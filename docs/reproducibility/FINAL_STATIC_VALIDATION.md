# Final Static Reproducibility Validation

## Validated checkpoint

- Branch: `manuscript-reproducibility-cleanup`
- Consolidated source tree before this receipt: `985656a`
- Accepted scientific baseline: `cd3c244`
- Validation date: 2026-08-23
- Scientific boundary: Stage28 final empirical wall

## Results

| Check | Result |
|---|---|
| Approved unittest suite | 127/127 PASS |
| Equivalence matrix | 112/112 PASS |
| Equivalence levels | A=21; B=64; C=18; D=9 |
| Stage protocol JSON | 28/28 parsed; execution disabled |
| All config JSON including Stage20 subconfigs | 33/33 parsed |
| Reproducibility/environment CSV registries | 15/15 parsed |
| Stage package imports | 28/28 PASS |
| Wrapper `--dry-run` | 28/28 PASS |
| Wrapper `--verify-only` | 28/28 PASS |
| Public CLI flags | Exactly `--dry-run`; `--verify-only` |
| Frozen result/figure/table/model/metadata paths | Unchanged from `cd3c244` |
| Archived `.ipynb` bytes | Unchanged from `cd3c244` |

## Commands

```text
python -m unittest discover -s tests -v
python -m compileall -q src
python scripts/reproduce_stageXX.py --dry-run
python scripts/reproduce_stageXX.py --verify-only
```

The wrapper commands were applied to every Stage01–28 interface. JSON, CSV,
import and CLI-surface checks were performed with read-only Python standard
library inspection.

## Scientific safety statement

No fit, model load, inference, target/holdout opening, threshold selection,
bootstrap generation, SHAP/LIME/IG generation, clock/profiler execution,
dataset reconstruction, feature analysis, model selection, new statistic,
new architecture, hypothesis test, or frozen-artifact write occurred.

Approved tests exercised only static parsing/identity checks, permitted exact
Stage25 scalar equations and toy mathematical fixtures. Configured large model,
checkpoint and probability artifacts were streamed for bytes only where
declared; they were not deserialized.

## Conclusion

The repository-wide consolidation preserves the accepted scientific history
and provides a complete public Stage1–28 reproducibility inspection surface.
Stage29 synthesis and manuscript rewriting remain outside this completed
boundary and were not begun.
