# Reproducibility Audit

## Scope and safety boundary

This audit was materialized on branch `manuscript-reproducibility-cleanup`
from starting HEAD `ca538faa4d39ef7f8921d98399c261944c905f28`.

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

Key findings after the approved Stage01-Stage15 extraction checkpoint:

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
- Stage16-18 remain notebook-centric.
- Stage19 preserves a window constructor and two model implementations.
- Stage20 preserves four reusable Python modules, but extensive forensic and
  recovery logic remains notebook-only.
- Stage21 preserves eight Python sources in addition to the embedded notebook
  cells.
- Stage22/Stage22R has extensive frozen evidence but no standalone scientific
  script or notebook in the repository.
- Stages23-28 have substantially stronger script/notebook preservation.

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
- Stage20 final holdout runtime amendment: PyTorch 2.10.0+cu126 on a Tesla T4;
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

## Stage01-Stage15 equivalence checkpoint

The non-scientific suite contains 66 tests and passes in full. The 52 rows in
`EQUIVALENCE_MATRIX.csv` are distributed across the approved evidence levels
as follows: two Level A byte-identity checks, 28 Level B exact static/numerical
checks, 14 Level C fixture/tolerance checks and eight Level D
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

Stage10 source review also resolves an important methodological boundary: its
cost-ratio threshold search does not apply an FPR filter. The 5% FPR constraint
is provenance for the frozen Stage04 security points only; the safe extraction
preserves that distinction.

## Audit conclusion

The repository contains extensive frozen evidence and strong closure records,
but executable coverage remains uneven. The authoritative notebook closes the
largest source-preservation gap for Stages01-20, and the approved Stage01-15
block is now represented by explicit, safety-gated code and configuration.
Cell 171 remains mapped only to Stage16 and was not included in Stage15.
Further extraction, beginning with Stage16, requires a new explicit approval.
Scientific execution remained prohibited throughout this extraction.
