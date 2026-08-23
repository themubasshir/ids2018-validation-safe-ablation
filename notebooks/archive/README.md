# Archived Notebook Evidence

The notebooks in this directory are immutable historical execution evidence.
They preserve physical cell order, source, outputs and execution metadata where
available. They are not the recommended public execution surface and must not
be rewritten into cleaner synthetic histories.

Use `scripts/reproduce_stageXX.py` for safe inspection. Those wrappers expose
only `--dry-run` and `--verify-only` and never execute notebook science.

## Archive coverage

| Archive | Stages | Historical role |
|---|---|---|
| `stage01_to_stage20_original_kaggle_notebook.ipynb` | Stage01–20 plus initial Stage21 cells | Authoritative 488-cell source chronology |
| `stage21_stage22_research_continues.ipynb` | Stage21–22 | Continuation, training/evaluation and Stage22/22R chronology |
| `stage23_research_executed.ipynb` | Stage23 | Executed shortcut-audit chronology and outputs |
| `stage24_cross_dataset_executed.ipynb` | Stage24 | Full cross-dataset chronology and outputs |
| `stage25_prevalence_operational_stress_executed.ipynb` | Stage25 | Full analytic chronology and outputs |
| `stage26_deployment_profiling_executed.ipynb` | Stage26 | Full CPU/T4 measurement chronology and outputs |
| `stage27_loao_unseen_attack_executed.ipynb` | Stage27 | Full LOAO chronology and outputs |
| `stage28_stability_novelty_control_executed.ipynb` | Stage28 | Full seed/control chronology and final empirical wall |

Exact identities are in
`docs/reproducibility/NOTEBOOK_ARCHIVE_REGISTRY.csv`. Repository exports and
partial notebooks outside this archive remain separately inventoried in
`docs/reproducibility/NOTEBOOK_INVENTORY.csv`; they must not replace a fuller
executed archive.

Physical 1-based cell order is the canonical locator. Execution counters are
historical evidence only because they can be missing, repeated or
non-monotonic.
