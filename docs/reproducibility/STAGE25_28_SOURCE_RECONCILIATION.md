# Stage 25-28 notebook, script and result reconciliation

## Scope and evidence rule

This inventory was completed before Stage 25-28 methodology consolidation.
It is a provenance reconciliation, not permission to execute historical
scientific code. Historical execution evidence wins over source cleanliness.
Canonical decisions use only the approved status vocabulary and are enumerated
in `STAGE25_28_SOURCE_REGISTRY.csv`.

No notebook or historical script was executed during reconciliation. The
inventory read notebook JSON, text source, small receipts and Git metadata, and
streamed bytes for SHA256 calculation. It did not load a model, checkpoint,
probability array, raw timing sample into an analysis, source corpus, target or
holdout. It generated no prediction, prevalence projection, bootstrap,
statistic or figure.

## Archived notebook identities

The four supplied notebooks are preserved byte-for-byte under
`notebooks/archive/`. Physical one-based cell order is canonical; execution
counts and outputs are historical evidence only.

| Repository archive | SHA256 | Bytes | Cells | Code | Code with outputs | Scope |
|---|---|---:|---:|---:|---:|---|
| `stage25_prevalence_operational_stress_executed.ipynb` | `58f529ca1e1f4a94083e533b5251b8f7433cfe57909477869a71d2cfbe5b61a3` | 739,572 | 8 | 8 | 7 | Generic Kaggle cell 1; Stage25 cells 2-8. |
| `stage26_deployment_profiling_executed.ipynb` | `f26cf14b8f5b56c7e6cb882b075b26a2c575b1c722690591ba1e779fa4fe7177` | 7,101,455 | 108 | 106 | 105 | Generic cell 1; Stage26 cells 2-108; two markdown cells. |
| `stage27_loao_unseen_attack_executed.ipynb` | `9180523c74e91fcb5b15a2ae6563db7567faa06d0e94710d718a197de4ff15cf` | 5,058,625 | 47 | 47 | 47 | Generic cell 1; Stage27 cells 2-47. |
| `stage28_stability_novelty_control_executed.ipynb` | `3d67dacd97050683de6b2d797e76cdefc4b35ed4f6bc13bb91992ea5c43e9f95` | 2,973,910 | 47 | 47 | 46 | Generic cell 1; all remaining cells are Stage28. |

The supplied Stage28 filename mentioned Stage29, but static heading inspection
found no Stage29 cell or Stage29 scientific section. Cells 2-47 are all
identified as Stage28, ending with the Stage28 archival cell. The complete file
is therefore Stage28 evidence. No Stage29 scientific content was inventoried or
authorized.

## Repository source and result inventory

### Stage25

The supplied executed notebook contains the generic Kaggle bootstrap followed
by seven Stage25 cells. Repository notebook
`scripts/stage25/stage25_prevalence_operational_stress.ipynb` and Python export
`stage25_prevalence_operational_stress.py` preserve supplied cells 2-8 exactly
after newline normalization and intentionally omit cell 1. The repository
notebook removes outputs and records recovery from kernel input history.

The result root contains 67 files and 1,126,273 bytes: 22 protocol-lock files,
the Bayesian projection, SOC-capacity, exact break-even and operational
translation packages, the final seal and the publication package. The stage is
zero-fit and zero-inference. Its formulas are reusable from frozen scalar
operating points, but the executed notebook and frozen results remain the
historical evidence.

Canonical classification: `NOTEBOOK_PLUS_SCRIPT`. The script is canonical for
the seven-cell analytic methodology; the full notebook is canonical for
execution outputs and the omitted generic bootstrap context.

### Stage26

The full executed notebook preserves 108 physical cells spanning protocol,
CPU cold/warm inference, memory and package profiling, extraction,
representation timing, timing uncertainty, Pareto/capacity analyses, CPU
publication closure, single-T4 profiling, CPU/GPU comparison and notebook
export.

`scripts/stage26/stage26_deployment_profiling_kaggle.py` is not a conventional
notebook conversion. Its receipt identifies it as a byte-for-byte export of
Kaggle's misleadingly named `.virtual_documents/__notebook_source__.ipynb`,
which was UTF-8 Python source and did not compile as one module. The checked-out
file uses CRLF; converting checkout line endings to LF yields exactly 3,807,767
bytes and SHA256
`e042c75c86b5f43f0da34fdb1bd63f5cb35b744f7003eaf99559324b0738229a`,
matching the frozen export receipt. Sixty-six of 106 executed code-cell bodies
occur verbatim in the virtual-source export; the remaining cells reflect the
virtual-history/export boundary and cannot honestly be claimed as a clean
one-cell-to-one-block conversion. Standalone executability is not guaranteed.

The result root contains 945 files and 21,887,684 bytes. It separates CPU
protocol/preflight, cold and warm observations, memory/package observations,
extraction/representation measurements, corrected timing uncertainty,
capacity and Pareto summaries, CPU publication assets, single-T4 results and
final CPU/GPU closure. The figure root contains 20 frozen PNG/PDF assets.
Historical measurements are environment-specific and authoritative; no new
machine is expected to reproduce identical milliseconds.

Canonical classification: `NOTEBOOK_CANONICAL` for execution chronology and
outputs. The virtual-source Python file is `ARCHIVAL_ONLY`, while frozen
receipts and raw observations are `STATIC_ARTIFACT_ONLY` evidence for the
historical measurements.

### Stage27

The supplied executed notebook is the only complete 47-cell chronology. The
repository notebook and cell-marked script contain 12 cells, mapping exactly
to supplied cells 34-45 after newline normalization. They preserve the
post-Stage27-3B0 recovery, similarity, final synthesis and publication
integration segment. Supplied cells 2-33 uniquely retain protocol,
family-by-day feasibility, memberships, prefit materialization, ten fits,
Thursday/Friday openings and bootstrap uncertainty. Cells 46-47 retain the
post-scientific source-export recovery and are also absent from the repository
notebook.

`scripts/stage27/stage27_publication_integration.py` is a separate frozen-result
publication generator. It is not a substitute for the missing early notebook
cells and does not authorize LOAO execution.

The result root contains 119 files and 73,931,638 bytes across protocol and
feasibility, memberships, prefit inputs, preopening models, Thursday and Friday
openings, 2,000-replicate frozen bootstrap evidence, behavioral similarity,
final synthesis and publication integration.

Canonical classification: `NOTEBOOK_PLUS_SCRIPT`. The full notebook is
canonical for the scientific execution history; the 12-cell export and the
publication integration script are canonical only for their represented
late-stage and publication scopes.

### Stage28

The supplied notebook is the complete 47-cell Stage28 history. Repository
notebook `scripts/stage28/stage28_full_kaggle_notebook.ipynb` contains 15 code
cells reconstructed from IPython raw execution history; all 15 map exactly to
supplied cells 33-47 after newline normalization. The paired Python file is a
cell-ordered archival linearization with framing markers. Repository archival
metadata explicitly says markdown and outputs were unavailable and that the
archive is not new science. Supplied cells 2-32 uniquely preserve the earlier
protocol, membership/input recovery and initial Stage22/chronology seed runs.

The result root contains 937 files and 862,831,604 bytes. It preserves the
protocol/amendment, inherited and random memberships, input identity locks,
Stage22 seed stability, chronology LOAO stability, random LOAO control, the
108-fit closure audit, seed uncertainty, shared-final-holdout evaluation and
final claim/manuscript-number synthesis. The Stage28 archive manifest's LF
identities remain exact after accounting for checkout line-ending conversion.

Canonical classification: `NOTEBOOK_PLUS_SCRIPT`. The supplied notebook is
canonical for complete execution chronology and outputs. The 15-cell repository
archive is canonical only for cells 33-47 and is otherwise archival. Frozen
ledgers and final synthesis are `STATIC_ARTIFACT_ONLY` terminal evidence.

## Canonical-source decision summary

| Stage | Classification | Reproducibility interpretation |
|---:|---|---|
| 25 | `NOTEBOOK_PLUS_SCRIPT` | Complete analytic method is preserved in a seven-cell script; outputs and execution history are preserved in the full notebook and frozen tables. |
| 26 | `NOTEBOOK_CANONICAL` | Measurement methodology and outputs are preserved; the virtual-source export is archival and historical timings are hardware-specific. |
| 27 | `NOTEBOOK_PLUS_SCRIPT` | Full notebook provides complete execution history; scripts cover only cells 34-45 and frozen-result publication integration. |
| 28 | `NOTEBOOK_PLUS_SCRIPT` | Full notebook provides cells 1-47; repository archive provides the exact late cells 33-47; frozen closure artifacts are terminal evidence. |

## Reconciliation discrepancies retained as evidence

- Stage25 repository exports intentionally omit the generic Kaggle cell and all
  outputs.
- Stage26's preserved virtual-source file is non-compiling and is not a clean
  cell export; this is documented historical behavior, not a repair target.
- Stage27's repository notebook/script omit physical cells 1-33 and 46-47.
- Stage28's pre-existing repository archive contains only physical cells 33-47
  of the supplied complete notebook, and its original manifest could not
  preserve outputs or markdown.
- Stage28's supplied filename suggests Stage29 even though its cell content is
  wholly Stage28. The archive name records content rather than the misleading
  external filename.

None of these gaps justifies rerunning science or replacing frozen artifacts.
