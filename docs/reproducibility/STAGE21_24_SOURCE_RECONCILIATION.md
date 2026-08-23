# Stage 21-24 notebook, script and result reconciliation

## Scope and evidence rule

This inventory was completed before Stage 21-24 methodology consolidation.
It is a provenance reconciliation, not permission to execute the historical
scientific code. Historical execution evidence wins over cleanliness. The
canonical-source decisions are enumerated in
`STAGE21_24_SOURCE_REGISTRY.csv` using only the approved status vocabulary.

No Stage 25 source was inspected for scientific content. The supplied
`stage-25.ipynb` is outside the approved boundary. The earlier supplied
`research-continues.xpynb` is a zero-byte file with SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649a1f8b7433c16f72b1f6f0`
and is unusable as notebook evidence.

## Archived notebook identities

The three usable user-supplied notebooks are preserved byte-for-byte under
`notebooks/archive/`. Physical one-based cell order is canonical; execution
counts are non-monotonic historical evidence only.

| Repository archive | SHA256 | Bytes | Cells | Code cells | Code cells with outputs | Scope |
|---|---|---:|---:|---:|---:|---|
| `stage21_stage22_research_continues.ipynb` | `dab6efa73600d36b1a6324ffa4036d6b02453b3b6c4ea84f995875d74a35a5db` | 24,673,089 | 139 | 139 | 138 | Cell 1 generic precursor; Stage21 cells 2-85; Stage22/22R cells 86-139. |
| `stage23_research_executed.ipynb` | `a33b83e09261aed6f7b772049bcfb7f4691e63e0cf2e13202c4cd00afeae007e` | 3,263,936 | 78 | 78 | 77 | Stage23 execution history plus post-closure script-export cells 76-78. |
| `stage24_cross_dataset_executed.ipynb` | `395465a0b72d718c997583ac3838fe12731d990799cadb134c20a548e669b8ac` | 2,688,147 | 62 | 62 | 45 | Full Stage24 history; cells 1-17 predate the repository export, cells 18-60 contain the recovered scientific continuation, and cells 61-62 are packaging recovery. |

The earlier authoritative archive remains the direct source for Stage21 cells
462-488. Those cells cover the initial Monday and Tuesday restoration chain;
they are not the complete Stage21 program.

## Repository source inventory

### Stage21

Preserved public or executed Python sources are:

- `scripts/stage21_masked_vit.py`: frozen `Stage21MaskedViTv1` model
  implementation referenced by the Stage21-0 protocol;
- `results/stage21_architecture/stage21_2_train_fast_executed.py`: exact
  training worker embedded in notebook cell 49;
- `stage21_3_thursday_eval_executed.py`: exact notebook-cell-51 worker;
- `stage21_4_friday_eval_executed.py`: exact notebook-cell-66 worker;
- `stage21_5_cnn_vit_compare_executed.py`: preserved comparison worker after
  the notebook's numerical-tolerance recovery;
- `scripts/stage21_xai1b_locked_ig.py`: frozen post-result IG harness;
- `scripts/stage21_generate_publication_figures.py`: exact notebook-cell-82
  publication source;
- `scripts/generate_publication_gap_figures_through_stage21.py`: exact
  notebook-cell-84 source.

The result root has 60 files and 3,412,736 bytes. It preserves the epoch-10
checkpoint, exact training/validation/Friday workers, probability and
bootstrap arrays, restoration receipts, model-identity locks, XAI receipts,
and publication manifests. Stage18's earlier `ViT unsupported` conclusion
remains historically separate: Stage20/21 later restored the representation
needed for this controlled architecture follow-up.

### Stage22 and Stage22R

There is no standalone historical Stage22 or Stage22R Python script in the
repository. The executed notebook cells 86-139 are therefore the historical
implementation source. The durable evidence is divided into:

- `results/stage22_temporal_session_safe/`: 32 files, 63,907,383 bytes;
- `results/stage22r_protocol_recovery/`: 27 files, 8,583,846 bytes;
- `results/stage22r_training/`: 44 files, 102,097,657 bytes.

The first root records the original protocol and provenance-recovery path.
Stage22R then freezes the Kaggle-faithful protocol, K79 cleaning, four exact
development memberships, the 70-feature model-input contract, four validation
cells, and one shared final-holdout opening. The absence of a standalone
scientific script is an executability gap, not a scientific-result gap. Safe
consolidation must expose configuration and static verification while citing
notebook cells 110-139 as the historical execution source.

Development validation and forward final-holdout performance remain distinct.
The four cells are RANDOM_NATURAL, RANDOM_REBALANCED,
CHRONOLOGICAL_NATURAL and CHRONOLOGICAL_REBALANCED. Their validation artifacts
were frozen before the single Mar1-Mar2 final-holdout opening. The final record
states one of one openings consumed and permanently closed, with no
post-holdout model, feature, preprocessing, calibration or threshold change.

### Stage23

`scripts/stage23_shortcut_feature_audit_kaggle.py` is the historically
preserved 75-cell percent-format export committed after scientific closure.
After newline normalization, 72 of the 78 supplied notebook cells occur
byte-for-byte in the script. Three scientific-synthesis cells differ because
the export hoists repeated `from __future__ import annotations` statements.
Cells 76-78 are later post-closure script export/upload/commit operations and
are not part of the 75-cell export. The script header identifies the earlier
source-notebook identity and the final scientific commit.

The script is canonical for the executable methodology because it preserves
the executed cell order and is tied to the frozen results. The supplied
notebook remains the canonical output/execution-history evidence. The result
root contains 339 files and 608,737,479 bytes across protocol, 12 reduced
primary cells, ten placebo cells, six stumps, uncertainty, SHAP, attack-family
analysis, and final synthesis. The frozen fit budget is exactly 50: 44 boosted
component fits plus six stumps. FULL reuses Stage22R and adds no fit.

### Stage24

The full executed notebook and the repository export have complementary
coverage. Repository notebook code cells 2-45 map exactly to supplied notebook
cells 18-60 after newline normalization; the Stage24-1C-EX1 cell appears twice
in the sanitized repository notebook, so 44 repository code cells correspond
to 43 unique supplied cells. Supplied cells 1-17 contain bootstrap, bridge
lock, source sanity and bridge62 source-fit history that is absent from the
sanitized export. Supplied cells 61-62 record post-scientific packaging
recovery and are also absent.

`scripts/stage24/stage24_cross_dataset_generalization.py` is a percent-format
export of the sanitized notebook, not proof that every earlier executed cell
was included. Stage24 is therefore `NOTEBOOK_PLUS_SCRIPT`: notebook outputs
prove execution, the script is the reusable preserved continuation, protocol
artifacts prove prospective decisions, and frozen results prove the final
state.

The result root contains 88 files and 57,438,267 bytes. It preserves the
bridge62/bridge70 specifications, four-of-four source fit budget, primary and
secondary directions, six completed evaluable target openings, two
GROUNDED_S4 cells administratively cancelled before opening, paired bootstrap
artifacts and final synthesis. Cancelled slots were not reallocated. Transfer
directions use different source models, populations and prevalence structures
and must never be averaged.

## Canonical-source decision summary

| Stage | Canonical classification | Reason |
|---:|---|---|
| 21 | `NOTEBOOK_PLUS_SCRIPT` | Restoration chronology spans two notebooks; exact executed workers and model/XAI/publication scripts exist for later substages. |
| 22 | `NOTEBOOK_CANONICAL` with safe consolidation required | The executed Stage22/22R notebook and extensive artifacts are present, but no standalone historical scientific script exists. |
| 23 | `SCRIPT_CANONICAL` for methodology; notebook canonical for execution outputs | The 75-cell export and frozen results are commit-linked; notebook cells 76-78 are archival post-closure operations. |
| 24 | `NOTEBOOK_PLUS_SCRIPT` | The repository script covers the recovered cells 18-60, while the executed notebook uniquely preserves cells 1-17 and 61-62 plus outputs. |

## Scientific safety boundary

Inventory and reconciliation read notebook JSON, text source, small JSON/CSV
metadata, Git history, file sizes and SHA256 bytes only. No notebook or
historical script was executed. No model/checkpoint/probability array was
loaded, no scientific dataset or target was opened, no bootstrap was generated
and no frozen result was modified.
