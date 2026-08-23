# Final Stage1–28 Reproducibility Audit

## Scope

This audit records the repository-wide reproducibility layer at accepted
checkpoint `cd3c244` on branch `manuscript-reproducibility-cleanup`. It is a
software, provenance and frozen-evidence audit. It is not authorization to
rerun scientific work.

Stage28 is the final empirical wall. All 28 public stage interfaces expose only
`--dry-run` and `--verify-only`. Neither mode fits or loads a model, performs
inference, opens a target, regenerates probabilities or explanations, selects
a threshold, generates a bootstrap sample, reconstructs a dataset, profiles
hardware, or writes a frozen scientific artifact.

## Repository-wide findings

| Surface | Audited status |
|---|---|
| Stage configs | 28/28 `configs/stageXX/protocol.json` files present; Stage20 also retains five scoped subconfigs |
| Canonical entry points | 28/28 `scripts/reproduce_stageXX.py` wrappers present |
| Package namespaces | 28/28 `src/ids_validation/stages/stageXX/` namespaces present |
| Archived executed notebooks | Eight immutable archives cover Stage01–28 chronology; 13 notebooks/exports are distinguished in the inventory |
| Source registries | Stage21–24 and Stage25–28 have substage-level notebook/script/result/commit registries; Stage01–20 use the physical-cell and Stage20 substage maps |
| Equivalence evidence | 112/112 rows pass: 21 Level A, 64 Level B, 18 Level C and 9 Level D |
| Static tests at accepted checkpoint | 127/127 pass |
| Manuscript traceability | 49 manuscript-critical rows through Stage28 |
| Discrepancies and gaps | 46 discrepancies and 43 reproducibility gaps are retained rather than hidden |
| Scientific boundary | `SCIENTIFIC_EXECUTION_BOUNDARY.md` closes Stage28 and prohibits empirical Stage29 work |

The public package is intentionally heterogeneous. Historical environments,
source forms and stage protocols are not normalized when doing so would erase
scientific semantics or provenance.

## Per-stage audit

`PARTIAL_STATIC` means that source, configuration and frozen evidence are
preserved but a full scientific rerun is neither authorized nor demonstrated.
`FULL_SCALAR` is reserved for Stage25's exact deterministic reproduction from
final frozen scalar inputs. `METHOD_ARCHIVAL_TIMING` separates reproducible
Stage26 measurement methodology from hardware-specific historical values.

| Stage | Research role | Canonical source | Code coverage | Config coverage | Environment status | Strongest stage-specific equivalence | Scientific rerun status | Remaining limitation |
|---:|---|---|---|---|---|---|---|---|
| 01 | Split and scaling | NB001 cells 93; extracted module | Methodology + safe wrapper | Complete protocol | Core versions proven | B | `PARTIAL_STATIC`; disabled | Raw IDS2018 source is external |
| 02 | Sixteen-model baseline | NB001 cells 94–95; extracted constructors | Constructors + safe wrapper | Complete protocol | Mixed; neural/runtime dependencies partly unproven | C | `PARTIAL_STATIC`; disabled | Incomplete serialized model inventory |
| 03 | Validation-safe tuning | NB001 cells 96–101; extracted search spaces | Search methodology + safe wrapper | Complete protocol | Mixed; neural/runtime dependencies partly unproven | B | `PARTIAL_STATIC`; disabled | HPO was not rerun |
| 04 | Operating-point selection | NB001 cells 102–104, 106 | Exact grid/tie rules + safe wrapper | Complete protocol | Mixed; SciPy/Matplotlib unproven | B | `PARTIAL_STATIC`; disabled | Threshold sweep was not rerun |
| 05 | Locked holdout evaluation | NB001 cells 105, 107 | Metric method + safe wrapper | Complete protocol | Mixed; Joblib/SciPy unproven | C | `PARTIAL_STATIC`; disabled | Holdout remains closed |
| 06 | TreeSHAP analysis | NB001 cell 108 | Methodology/toy helpers + safe wrapper | Complete protocol | `VERSION_NOT_PROVEN` for historical runtime | B | `PARTIAL_STATIC`; disabled | Exact Joblib inputs and SHAP matrices absent |
| 07 | Publication packaging | NB001 cells 109–115 | Inventory/archive method + safe wrapper | Complete protocol | Historical runtime unproven | B | `PARTIAL_STATIC`; disabled | Destructive packaging operations intentionally unavailable |
| 08 | Bootstrap confidence | NB001 cells 116–117 | Exact method/toy helpers + safe wrapper | Complete protocol | Receipt-proven | B | `PARTIAL_STATIC`; disabled | Bootstrap was not regenerated |
| 09 | Calibration description | NB001 cell 118 | Exact method/toy helpers + safe wrapper | Complete protocol | Receipt-proven | B | `PARTIAL_STATIC`; disabled | Calibration/bootstrap not recomputed |
| 10 | Operational cost | NB001 cell 119 | Exact formula/tie helpers + safe wrapper | Complete protocol | Historical runtime unproven | B | `PARTIAL_STATIC`; disabled | Validation selection and holdout evaluation not rerun |
| 11 | Attack-category audit | NB001 cell 120 | Taxonomy/statistical helpers + safe wrapper | Complete protocol | Historical runtime unproven | B | `PARTIAL_STATIC`; disabled | Category analysis not regenerated |
| 12 | Fixed-hyperparameter multi-seed robustness | NB001 cells 121–129 | Exact split/tie helpers + safe wrapper | Complete protocol | Core learner versions proven; ancillary versions partial | B | `PARTIAL_STATIC`; disabled | Fixed-hyperparameter scope; no new fits |
| 13 | Explanation reliability | NB001 cells 130–146 | LIME/agreement helpers + safe wrapper | Complete protocol | Mixed; SHAP/SciPy/Matplotlib unproven | B | `PARTIAL_STATIC`; disabled | Explanations not regenerated |
| 14 | Integrated Gradients audit | NB001 cells 147–161 | IG mathematics/toy helpers + safe wrapper | Complete protocol | TensorFlow proven; ancillary versions partial | B | `PARTIAL_STATIC`; disabled | Model/gradient attribution not rerun |
| 15 | FT-Transformer feasibility | NB001 cells 162–170, 172–189 | Split/model specs + preserved scripts + safe wrapper | Complete protocol | Exact isolated P100 runtime proven | A | `PARTIAL_STATIC`; disabled | External processed data; checkpoints hash-only |
| 16 | Classical benchmark | NB001 cells 171, 190–222 | Static model registry + safe wrapper | Complete protocol | Historical runtime unproven | A | `PARTIAL_STATIC`; disabled | Models/scaler hash-only |
| 17 | Attention diagnostics | NB001 cells 223–239 | Toy attention helpers + safe wrapper | Complete protocol | Historical runtime unproven | B | `PARTIAL_STATIC`; disabled | Checkpoint and attention extraction unopened |
| 18 | Representation feasibility | NB001 cells 240–289 | Branch-specific helpers + safe wrapper | Complete protocol | Repaired P100 runtime partly proven | A | `PARTIAL_STATIC`; disabled | Scientific branches not rerun |
| 19 | Temporal models | NB001 cells 290–311 | Window/model specs + safe wrapper | Complete protocol | P100 runtime proven; scientific stack partial | A | `PARTIAL_STATIC`; disabled | Temporal data materialization external |
| 20 | Packet-image/CNN program | NB001 cells 312–461; scoped modules | Ten conservative namespaces + safe wrapper | Protocol + five subconfigs | Multiple separately proven/partial runtimes | A | `PARTIAL_STATIC`; disabled | Raw PCAP/components external; later Friday cells unmapped |
| 21 | Masked-ViT continuation | NB001 462–488 + NB007 2–85 + exact scripts | Notebook/script chronology + safe wrapper | Complete protocol | T4 runtime proven | A | `PARTIAL_STATIC`; disabled | Restored corpora external |
| 22 | Temporal session-safe validation | NB007 cells 86–139 | Static contracts + safe wrapper | Complete protocol | Learners proven; Python/GPU identity unproven | B | `PARTIAL_STATIC`; disabled | No standalone historical scientific script; holdout closed |
| 23 | Shortcut-feature audit | NB008 + 75-cell script | Script methodology + notebook outputs + safe wrapper | Complete protocol | Packages proven; Python/GPU identity unproven | A | `PARTIAL_STATIC`; disabled | Fit/bootstrap/SHAP evidence remains frozen |
| 24 | Cross-dataset transfer | NB009 + sanitized NB003/script | Full chronology + recovered script + safe wrapper | Complete protocol | Two-T4 runtime proven | A | `PARTIAL_STATIC`; disabled | Two exact-only GROUNDED_S4 cells cancelled |
| 25 | Prevalence/SOC stress | NB010 + exact cells 2–8 script export | Exact scalar formulas + safe wrapper | Complete protocol | Python proven; other packages unproven but nonessential | A | `FULL_SCALAR`; deterministic scalar tests only | Depends on inherited frozen operating-point scalars |
| 26 | Deployment profiling | NB011; virtual source archival only | Static protocol/toy statistics + safe wrapper | Complete protocol | CPU and T4 sessions separately recorded | A | `METHOD_ARCHIVAL_TIMING`; timing disabled | Exact milliseconds are hardware-specific |
| 27 | LOAO generalization | NB012 + late-cell scripts | Full chronology/static contracts + safe wrapper | Complete protocol | CPU runtime proven | A | `PARTIAL_STATIC`; disabled | Targets closed; five eligible folds only |
| 28 | Seed/control stability | NB013 + late-cell archive/script | Full chronology/static ledgers + safe wrapper | Complete protocol | Core CPU stack partial; learner versions unproven | A | `PARTIAL_STATIC`; disabled | Final wall; probability NPZ hash-only |

## Canonical evidence chain

The intended reviewer path is:

```text
manuscript claim
  -> frozen result, table, or figure
  -> stage config and reproduce_stageXX.py interface
  -> extracted methodology module or preserved historical script
  -> original notebook cell(s)
  -> provenance and equivalence record
```

The manuscript traceability and reproduction indexes are the claim-level
front doors. The stage config is the machine-readable safety and methodology
contract. Original notebooks remain immutable historical evidence, not the
recommended public execution surface.

## Global limitations retained

- The original IDS2018/IDS2017 source data and several processed corpora are
  external to the repository.
- Historical package identity is uneven and remains `VERSION_NOT_PROVEN` where
  no stage-specific receipt exists.
- Many serialized models and large arrays are deliberately hash-verified
  without deserialization.
- Equivalence Levels A–D describe the verified claim, not automatic
  end-to-end scientific rerun reproducibility.
- Stage26 timing values are historical measurements, not portable performance
  promises.
- Closed targets and holdouts are not reopened by reproducibility tooling.
- Stage28 is terminal. Future empirical work belongs to a separate project.

## Audit conclusion

The Stage1–28 chain has complete config, namespace and safe-entry-point
coverage. It has strong frozen-evidence and provenance coverage but only
Stage25 qualifies for deterministic full reproduction from frozen inputs.
Stage26 is method-reproducible with archival measurements. The remaining 26
stages are honestly classified as partial/static because this consolidation
does not rerun their science.
