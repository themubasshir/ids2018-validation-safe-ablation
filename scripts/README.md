# Stage Reproduction Interfaces

The 28 `reproduce_stageXX.py` files are the canonical public inspection
interfaces. Each delegates to the shared safety-gated protocol CLI and requires
exactly one mode:

- `--dry-run`: describe historical operations and boundaries;
- `--verify-only`: check declarations, paths and configured byte identities.

Scientific execution is prohibited for every wrapper. No wrapper has a
training, inference, target-opening, threshold, bootstrap, explanation,
timing, data-reconstruction, or default execution mode.

| Stage | Historical role | Canonical source type | Allowed modes | Reproducibility status | Scientific execution prohibited | Config |
|---:|---|---|---|---|---|---|
| 01 | Split/scaling | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage01/protocol.json` |
| 02 | Baseline models | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage02/protocol.json` |
| 03 | Tuning | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage03/protocol.json` |
| 04 | Operating points | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage04/protocol.json` |
| 05 | Locked holdout | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage05/protocol.json` |
| 06 | TreeSHAP | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage06/protocol.json` |
| 07 | Publication packaging | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage07/protocol.json` |
| 08 | Bootstrap confidence | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage08/protocol.json` |
| 09 | Calibration | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage09/protocol.json` |
| 10 | Operational cost | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage10/protocol.json` |
| 11 | Attack categories | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage11/protocol.json` |
| 12 | Multi-seed robustness | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage12/protocol.json` |
| 13 | Explanation reliability | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage13/protocol.json` |
| 14 | Integrated Gradients | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage14/protocol.json` |
| 15 | FT-Transformer | Notebook plus preserved scripts and extracted contracts | dry-run; verify-only | Partial/static | Yes | `configs/stage15/protocol.json` |
| 16 | Classical benchmark | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage16/protocol.json` |
| 17 | Attention diagnostics | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage17/protocol.json` |
| 18 | Representation feasibility | Notebook-derived branch-specific methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage18/protocol.json` |
| 19 | Temporal models | Notebook-derived extracted methodology | dry-run; verify-only | Partial/static | Yes | `configs/stage19/protocol.json` |
| 20 | Packet-image/CNN | Notebook plus ten scoped extracted namespaces | dry-run; verify-only | Partial/static | Yes | `configs/stage20/protocol.json` |
| 21 | Masked-ViT continuation | Notebook plus exact historical scripts | dry-run; verify-only | Partial/static | Yes | `configs/stage21/protocol.json` |
| 22 | Session-safe temporal validation | Notebook canonical | dry-run; verify-only | Partial/static | Yes | `configs/stage22/protocol.json` |
| 23 | Shortcut audit | Script methodology; notebook outputs | dry-run; verify-only | Partial/static | Yes | `configs/stage23/protocol.json` |
| 24 | Cross-dataset transfer | Notebook plus sanitized script | dry-run; verify-only | Partial/static | Yes | `configs/stage24/protocol.json` |
| 25 | Prevalence/SOC stress | Notebook plus exact analytic script | dry-run; verify-only | Full from frozen scalars | Yes | `configs/stage25/protocol.json` |
| 26 | Deployment profiling | Notebook canonical; virtual source archival | dry-run; verify-only | Method reproducible; timings archival | Yes | `configs/stage26/protocol.json` |
| 27 | LOAO generalization | Notebook plus late-cell scripts | dry-run; verify-only | Partial/static | Yes | `configs/stage27/protocol.json` |
| 28 | Seed/control stability | Notebook plus late-cell archive/script | dry-run; verify-only | Partial/static; final wall | Yes | `configs/stage28/protocol.json` |

Examples:

```text
python scripts/reproduce_stage01.py --dry-run
python scripts/reproduce_stage25.py --verify-only
python scripts/reproduce_stage28.py --verify-only
```

See `REPRODUCE.md` for environment setup, Stage25 deterministic analytic
verification and the meaning of equivalence Levels A–D.
