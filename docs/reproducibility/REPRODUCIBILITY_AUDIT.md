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

Key findings:

- Stages01-14 are executable primarily through the authoritative notebook.
- Stage15 preserves nine Python sources and extensive checkpoints.
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

Historical environments are stage-specific.

Examples proven by receipts include:

- core seed-42 tree environment: Python 3.12.13, NumPy 2.4.6, pandas 2.3.3,
  scikit-learn 1.6.1, XGBoost 3.2.0, LightGBM 4.6.0 and CatBoost 1.2.10;
- Stage15 isolated runtime: PyTorch 2.7.1+cu118 on a Tesla P100;
- Stage20 final holdout runtime amendment: PyTorch 2.10.0+cu126 on a Tesla T4;
- Stage26 GPU receipt: PyTorch 2.10.0+cu128 on a Tesla T4.

The unpinned historical versions of TensorFlow, SHAP, SciPy, Matplotlib and
Joblib are `VERSION_NOT_PROVEN` unless a more specific stage receipt is later
identified. No convenient modern version may be substituted as historical
fact.

## Audit conclusion

The repository contains extensive frozen evidence and strong closure records,
but executable coverage is uneven. The authoritative notebook closes the
largest source-preservation gap for Stages01-20. Extraction must proceed in
small stage blocks with explicit source-cell provenance and the strongest
honest equivalence level available. Scientific execution remains prohibited
during extraction.
