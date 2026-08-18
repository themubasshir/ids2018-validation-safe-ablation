# Stage24 Publication Closeout

## Status

**Stage24 scientific execution: CLOSED**

- Scientific fits: **4 / 4**
- Evaluable target openings: **6 / 6**
- Administrative GROUNDED_S4 cancellations: **2**
- Cancelled slots reallocated: **No**
- Remaining Stage24 model fits: **0**
- Remaining Stage24 evaluable target openings: **0**

## Scientific final freeze

Commit before publication packaging:

`a4b6a3854109ba3d85954fb4a40afe6fe1ee6114`

Stage24 final synthesis SHA256:

`785bbcb00140f4d7e07e9b49ad33924166b5995e66a229c986d5b1abcbcaee4b`

## Publication package

### Manuscript

- `docs/STAGE24_MANUSCRIPT_INTEGRATION.md`
- `docs/STAGE24_MANUSCRIPT_INTEGRATION.tex`
- `docs/STAGE24_PUBLICATION_TABLES.md`
- `docs/STAGE24_PUBLICATION_TABLES.tex`

### Tables

- `results/stage24_cross_dataset/stage24_publication_package/tables/table24_1_bidirectional_generalization.csv`
- `results/stage24_cross_dataset/stage24_publication_package/tables/table24_2_paired_bootstrap_contrasts.csv`
- `results/stage24_cross_dataset/stage24_publication_package/tables/table24_3_secondary_threshold_transfer.csv`
- `results/stage24_cross_dataset/stage24_publication_package/tables/table24_4_governance_and_populations.csv`

### Figures

- `figures/stage24_cross_dataset/fig24_1_normalized_pr_auc_directionality.png`
- `figures/stage24_cross_dataset/fig24_2_roc_auc_directionality.png`
- `figures/stage24_cross_dataset/fig24_3_paired_effects_forest.png`
- `figures/stage24_cross_dataset/fig24_4_secondary_threshold_transfer.png`

Every figure is also exported as SVG.

### Reproducible notebook/script export

- `scripts/stage24/stage24_cross_dataset_generalization.ipynb`
- `scripts/stage24/stage24_cross_dataset_generalization.py`
- `scripts/stage24/README.md`

## Scientific interpretation

Stage24 demonstrates strongly asymmetric bidirectional cross-dataset
generalization. IDS2018-derived models retain substantial ranking signal on
CICIDS2017, whereas reciprocal CICIDS2017-to-IDS2018 transfer on the frozen
Feb-28 population is only marginally above chance/prevalence ranking.

It additionally shows that aggregate flag-count semantics materially influence
reported transfer performance and that source-validation operating thresholds
do not transfer reliably.

## Governance

Publication packaging is strictly post-processing of already-frozen Stage24
artifacts. It does not authorize any further Stage24 fitting, target inference,
threshold tuning, calibration, or feature modification.
