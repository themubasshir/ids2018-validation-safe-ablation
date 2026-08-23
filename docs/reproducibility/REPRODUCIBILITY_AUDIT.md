# Reproducibility Audit

## Scope and safety boundary

This audit was materialized on branch `manuscript-reproducibility-cleanup`
from starting HEAD `ca538faa4d39ef7f8921d98399c261944c905f28`.

The approved Stage21-Stage24 reconciliation extends the accepted Stage20
checkpoint `f5e4e5b` on the same branch. It inventories later user-supplied
executed notebooks before consolidation and applies the evidence order below
without modifying accepted Stage01-Stage20 commits.

The scientific program is closed through Stage28. This work is source
preservation, provenance mapping and reproducibility engineering only. It does
not authorize model fitting, inference, threshold selection, holdout access,
feature changes, taxonomy changes or alteration of frozen result artifacts.

The evidence priority is:

1. frozen results, manifests, receipts and protocol artifacts;
2. original notebooks;
3. existing scripts;
4. documentation;
5. interpretation.

Conflicts are recorded in `DISCREPANCY_REGISTER.csv`; they are not silently
resolved.

## Initial repository state

| Item | Audited value |
|---|---|
| Branch | `manuscript-reproducibility-cleanup` |
| Starting HEAD | `ca538faa4d39ef7f8921d98399c261944c905f28` |
| Working tree before changes | Clean |
| Files | 4,165 |
| Approximate repository payload | 2,322,014,833 bytes |
| Repository notebooks before archive | 5 |
| Python files before extraction | 42 |
| Result files | 3,846 |
| Result payload | 2,250,869,509 bytes |
| Top-level `src/` before extraction | Absent |
| Top-level `configs/` before extraction | Absent |
| Top-level `tests/` before extraction | Absent |
| Top-level `environment/` before extraction | Absent |

Serialized binary model artifacts include 52 `.pt`, 25 `.joblib`, two
`.keras` and one `.cbm` file. Additional native XGBoost/LightGBM models and
model identities are stored as JSON/TXT files and manifests. The result tree
also contains many JSON ledgers that describe models but are not themselves
serialized estimators; these categories must remain distinct.

## Stage28 closure gate

Stage28 final scientific closure exists at:

`results/stage28_stability_novelty_control/stage28_final_synthesis/`

The final receipt records:

- 108 authorized new fits;
- 108 consumed new fits;
- zero remaining fits;
- 12 historical reuses;
- zero scientific operations during final synthesis;
- no authorized Stage29.

The Stage28-3A receipt separately confirms contiguous `FIT_001` through
`FIT_108`, exact 108/108 new-fit coverage and 12/12 reuse coverage.

### LF/CRLF checksum audit

The ten paths in the Stage28 final-synthesis `checksums.sha256` file produce:

- raw Windows worktree byte matches: 0/10;
- worktree bytes normalized from CRLF to LF: 10/10;
- canonical `HEAD` Git blob matches: 10/10.

`core.autocrlf=true` and no applicable `eol` attribute explain the checkout
behavior. This is a reproducibility-engineering discrepancy only. Frozen
Stage28 artifacts must not be edited to make worktree hashes match.

## Authoritative notebook

The user-supplied notebook is archived byte-for-byte at:

`notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb`

| Property | Value |
|---|---|
| SHA256 | `147760f81f5db581c2cbc92b3c7c24060b823dfa50ac9d9a2156eb132b51b3ce` |
| Bytes | 14,127,660 |
| Physical cells | 488 |
| Code cells | 488 |
| Markdown cells | 0 |
| Cells with integer execution counts | 324 |
| Cells without integer execution counts | 164 |

Physical 1-based cell order is the canonical locator. Execution counters are
retained as historical evidence but cannot define order because they are
non-monotonic and reused.

Approved mapping exceptions:

- physical cell 171 is Stage16 despite appearing inside the Stage15 sequence;
- physical cells 462-488 contain Stage21 work despite the archive filename.

The earlier repository file
`notebooks/original_kaggle_working_notebook.ipynb` is a partial Stage01-Stage07
source. It contains 109 exact source-cell matches with the authoritative
notebook but is not a replacement for the complete archive.

## Notebook status vocabulary

`NOTEBOOK_CELL_MAP.csv` uses these classifications:

- `precursor`: early state needed to understand methodological evolution;
- `canonical`: scientific or protocol logic retained as the applicable stage
  source;
- `repair`: an explicit correction, patch or erratum;
- `recovery`: runtime/session/source restoration or resume logic;
- `superseded`: abandoned or replaced historical logic retained for audit;
- `packaging`: archive, Git-anchor, publication or persistence operations;
- `stage21_out_of_filename_scope`: Stage21 cells physically preserved in the
  Stage01-to-Stage20-named notebook.

Classification is provenance metadata, not permission to delete or rewrite a
cell. Every archived cell remains immutable.

## Code and artifact coverage

Detailed inventories are in `NOTEBOOK_INVENTORY.csv` and
`STAGE_CODE_INVENTORY.csv`.

Key findings after the approved Stage01-Stage20 extraction checkpoint:

- Stages01-15 now have provenance-bearing methodology modules, explicit JSON
  protocols and dry-run/verify-only entry points. Scientific execution is not
  exposed by those entry points.
- Stages11-14 preserve exact configuration and frozen-output structure, but
  their scientific category, multi-seed, LIME/SHAP and IG operations were not
  rerun during extraction.
- Stage15 preserves its historical Python sources and extensive checkpoints;
  the extraction adds thin duplicate-policy and FT-Transformer architecture
  wrappers. Verify-only byte-hashes the five locked checkpoints without
  deserializing them.
- Stage16 now has a static duplicate-safe classical registry and protocol;
  its frozen scaler/model artifacts are verified by bytes without loading.
- Stage17 exposes only toy attention mathematics and frozen result metadata;
  checkpoint loading, attention extraction and holdout access remain disabled.
- Stage18 keeps the temporal, historical ViT and graph conclusions separate.
  The later Stage20 packet recovery does not retroactively alter the Stage18
  ViT conclusion. Six graph checkpoints are byte-verified only.
- Stage19 preserves one-second materialization/window contracts and static
  model registries. Its scaler and six checkpoints are byte-verified only.
- Stage20 is split into provenance, extractor forensics, directed-S4,
  reconstruction, runtime recovery, packet representation, compact corpus,
  CNN, evaluation and governance namespaces. No raw forensic or learning path
  is exposed. Its authoritative per-cell detail is in
  `STAGE20_SUBSTAGE_MAP.md` and `STAGE20_CELL_MAP.csv`.
- Stage21 is `NOTEBOOK_PLUS_SCRIPT`: initial restoration is in NB001 cells
  462-488, continuation is in NB007 cells 2-85, and exact executed workers plus
  model/XAI/publication scripts are preserved. The Stage18 feasibility finding
  remains historically distinct from the later Stage20/21 recovery.
- Stage22 is `NOTEBOOK_CANONICAL`: NB007 cells 86-139 and complete frozen
  Stage22R artifacts preserve four development cells and the permanently
  closed shared forward holdout. No standalone historical scientific Python
  script exists, so the new interface exposes static contracts only.
- Stage23 is `SCRIPT_CANONICAL` for methodology and notebook-canonical for
  execution/output evidence. The 50-of-50 fit budget, fixed subsets, placebo
  and stump controls, bootstrap/SHAP evidence and final closure are preserved
  without importing the monolithic worker.
- Stage24 is `NOTEBOOK_PLUS_SCRIPT`: the full executed NB009 supplies chronology
  absent from the sanitized NB003/script. Four fits and six evaluable openings
  are closed; two GROUNDED_S4 cells remain administratively cancelled before
  opening and their slots were not reallocated.
- Stages25-28 remain outside this approved extraction block and were not
  changed by the Stage21-Stage24 work.

Stages01-13 use functional result roots such as `results/baseline`,
`results/tuning`, `results/threshold` and `results/holdout`, whereas later
stages generally use stage-numbered trees. Directory naming is therefore not
itself sufficient evidence of stage ownership.

## Environment evidence

Historical environments are stage-specific. Stage08 and Stage09 receipts prove
their analysis runtimes directly; Stage06, Stage07 and Stage10 do not preserve
complete stage-specific runtime receipts.

Examples proven by receipts include:

- Stage08 bootstrap: Python 3.12.13, NumPy 2.4.6, pandas 2.3.3,
  scikit-learn 1.6.1, Matplotlib 3.10.0 and Joblib 1.5.3;
- Stage09 calibration: the Stage08 versions plus SciPy 1.16.3, with no
  scikit-learn dependency recorded by that receipt;
- Stage12 multi-seed: Python 3.12.13, NumPy 2.4.6, pandas 2.3.3,
  scikit-learn 1.6.1, XGBoost 3.2.0 and LightGBM 4.6.0;
- Stage13 LIME receipt: Python 3.12.13, NumPy 2.4.6, pandas 2.3.3,
  scikit-learn 1.6.1, XGBoost 3.2.0, LightGBM 4.6.0 and LIME 0.2.0.1;
- Stage14 IG receipt: Python 3.12.13, TensorFlow 2.19.0, NumPy 2.4.6 and
  pandas 2.3.3;
- Stage15 isolated runtime: PyTorch 2.7.1+cu118 and CUDA 11.8 on a Tesla
  P100-PCIE-16GB with required `sm_60` kernels;
- Stage18 graph repair and Stage19 temporal runtime: PyTorch 2.10.0+cu126 on
  a Tesla P100 with `sm_60` support;
- Stage20 isolated CNN training/Thursday runtime: Python 3.12.13, NumPy 2.4.6,
  PyTorch 2.10.0+cu126, CUDA 12.6 and cuDNN 9.1.0.2 on a Tesla P100;
- Stage20 later final-holdout amendment: PyTorch 2.10.0+cu126 on a Tesla T4,
  recorded as `NOTEBOOK_CELL_NOT_MAPPED` rather than assigned to cells 455-461;
- Stage21 training/evaluation: Python 3.12.13, NumPy 2.4.6, PyTorch
  2.10.0+cu126, CUDA 12.6 and cuDNN 9.1.0.2 on a Tesla T4;
- Stage22R: NumPy 2.0.2, pandas 2.3.3, scikit-learn 1.6.1, LightGBM 4.6.0 and
  XGBoost 3.2.0, with LightGBM on CPU and XGBoost on CUDA; Python version and
  GPU model are `VERSION_NOT_PROVEN`;
- Stage23: NumPy 2.0.2, pandas 2.3.3, scikit-learn 1.6.1, LightGBM 4.6.0,
  XGBoost 3.2.0 and SHAP 0.51.0, with Python version and GPU model
  `VERSION_NOT_PROVEN`;
- Stage24: its own bootstrap receipt proves Python 3.12.13, NumPy 2.0.2,
  pandas 2.3.3, PyArrow 24.0.0, scikit-learn 1.6.1, LightGBM 4.6.0,
  XGBoost 3.2.0 and CatBoost 1.2.10 on two Tesla T4 GPUs;
- Stage26 GPU receipt: PyTorch 2.10.0+cu128 on a Tesla T4.

The historical TensorFlow version is unproven for the early neural stages but
proven as 2.19.0 for Stage14 only. Standalone Keras remains unproven for
Stage14. SHAP is `VERSION_NOT_PROVEN` for Stages06 and 13. SciPy, Matplotlib
and Joblib are likewise unproven except where a stage-specific receipt such as
Stage08/09 identifies them. No convenient modern version may be substituted
as historical fact.

The Stage15 environment history also contains a superseded system PyTorch
2.10.0+cu128 receipt that lacked P100 `sm_60` kernels. It must not be confused
with the isolated 2.7.1+cu118 environment that passed matrix, forward,
backward and optimizer checks. See `STAGE15_ENVIRONMENT_PROVENANCE.md`.

## Stage01-Stage24 equivalence checkpoint

The non-scientific suite contains 108 tests and passes in full. The 93 rows in
`EQUIVALENCE_MATRIX.csv` are distributed across the approved evidence levels
as follows: 11 Level A byte-identity checks, 55 Level B exact static/numerical
checks, 18 Level C fixture/tolerance checks and nine Level D
structural/provenance checks.

The lower equivalence levels are intentional. The external processed dataset
is not in the repository, several exact historical dependency versions are
unproven, and the exact Stage06 Joblib inputs and SHAP arrays are absent. No
model was constructed or fitted, no inference or target reconstruction
occurred, no threshold sweep or cost selection was rerun, no calibration or
2,000-replicate bootstrap computation was performed, and no holdout
target/probability input was opened. Stage08/09 NPZ artifacts were opened only
for key/schema/shape validation, and frozen Stage10 validation selections were
checked statically.

For Stages11-15, frozen CSV/JSON schemas and values were checked statically and
mathematical helpers were exercised only on synthetic inputs. No category
analysis, multi-seed fit, LIME, SHAP, IG or FT-Transformer training/inference
was executed. Stage15 verify-only streamed checkpoint bytes for SHA256 and size
checks only; no checkpoint was deserialized. The historical receipts record
one Stage15 holdout opening after architecture, threshold and checkpoint locks.
Extraction did not reconstruct, open or reevaluate that holdout.

Reproducibility classification at this checkpoint is **partially
reproducible** for each of Stages11-15. Exact source, configuration and frozen
evidence are preserved, but a full scientific rerun is neither authorized nor
demonstrated. Stage11 additionally lacks a proven runtime; Stage13 retains
unproven SHAP/SciPy/Matplotlib versions; Stage14 retains unproven standalone
Keras/scikit-learn/Joblib/Matplotlib versions; and Stage15 depends on an
external processed dataset despite complete locked checkpoint provenance.

Stages16-20 are also classified **partially reproducible**. Their authoritative
cells, extracted configurations, static methodology and frozen receipts are
preserved, but full scientific reruns were neither authorized nor attempted.
Stage16 and Stage17 runtime versions remain unproven. Stage18 and Stage19 have
stage-specific P100 runtime evidence but were not rerun. Stage20 has unusually
strong source hashes, exact artifact-byte checks and protocol locks, while its
raw PCAP reconstruction, compact-corpus components and scientific execution
remain external or intentionally unopened. The C16 historical manifest's
scientific state was recovered but its original bytes were not.

For Stage20, historical raw exactness (637/675), the D5 source-faithful accepted
baseline (635/675), and the rejected global V1 result (318/675) are separate
states. C16's two pre-registered packet-geometry mechanisms passed within the
bounded disagreement population, but neither V1 nor a selective hybrid became
the published-label reconstruction rule. The direct notebook E4 lineage stops
at the prelock/Kaggle storage-gate attempt. Seven later Colab/Xet and completed
Friday artifacts exist as frozen evidence but have no execution cell in the
accepted 312-461 boundary.

Stage10 source review also resolves an important methodological boundary: its
cost-ratio threshold search does not apply an FPR filter. The 5% FPR constraint
is provenance for the frozen Stage04 security points only; the safe extraction
preserves that distinction.

Stages21-24 are classified **partially reproducible**. Each now has an
execution-disabled protocol, a dry-run/verify-only public entry point, exact
source classification and static equivalence coverage. Stage21 has strong
worker/checkpoint provenance but depends on external restored corpora. Stage22
has strong notebook/result coverage and 13 byte anchors, but lacks a standalone
historical scientific script and has unproven Python/GPU identity. Stage23 has
the strongest preserved executable methodology of this block, but the safe
interface intentionally does not import or run it and Python/GPU identity is
unproven. Stage24 has a complete executed chronology, frozen semantic bridges,
terminal fit/opening ledgers and stage-specific runtime evidence, while both
GROUNDED_S4 cells remain correctly non-evaluable.

The Stage21-Stage24 tests read notebook JSON and source text, inspect static
JSON/CSV metadata and stream 44 declared artifact identities. They never
deserialize a model/checkpoint/probability array. No training, inference,
threshold reselection, bootstrap generation, SHAP computation, corpus/data
materialization, target opening, source refit, feature-bridge modification or
cross-dataset evaluation occurred.

## Audit conclusion

The repository contains extensive frozen evidence and strong closure records,
but executable coverage remains uneven. The approved Stage01-Stage24 boundary
is now represented by provenance-bearing code/configuration and safety-gated
interfaces. Cell 171 remains mapped only to Stage16. Cells 462-488 remain the
initial Stage21 restoration range and are explicitly reconciled with the later
NB007 continuation rather than treated as a complete program.

Stage22 central temporal claims, Stage23 shortcut-audit claims and Stage24
bidirectional transfer claims now have 29 rows of manuscript-critical
traceability. Scientific execution remained prohibited throughout. This work
stops after Stage24; Stage25 requires new explicit approval.
