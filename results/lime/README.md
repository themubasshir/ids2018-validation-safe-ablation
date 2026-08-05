# Stage 13 — Local Explanation Reliability

This directory contains the detailed results for the Stage 13 local
explanation reliability analysis.

## Methodological decision

- **Primary local explanation method:** TreeSHAP
- **Supplementary method:** LIME
- **Role of LIME:** surrogate-reliability stress test and supplementary
  local diagnostic

TreeSHAP was retained as the primary local attribution method because
its local values reconstruct the raw outputs of both tree ensembles.
LIME was repeatable across perturbation seeds but frequently failed to
provide a faithful local linear approximation.

## Principal result

Across the representative 64-case TP/TN/FP/FN panel:

- 2 explanations qualified under all study-specific criteria.
- 30 explanations were fidelity-limited.
- 31 explanations failed to preserve the model's local decision.
- 1 explanation was cross-method divergent.

## Directory map

- Case-selection files define the deterministic TP/TN/FP/FN and
  cross-model disagreement panels.
- `lime_fidelity_configuration_*` contains the six-configuration
  sensitivity analysis.
- `lime_seed_stability_*` contains the five-seed stability experiment.
- `local_shap_lime_*` contains the 12-case hard-panel TreeSHAP–LIME
  comparison.
- `lime_full_panel_*` and `lime_shap_full_panel_*` contain the complete
  64-case outcome-stratified analysis.
- Publication-ready tables are stored under `tables/lime/`.
- Publication-ready figures are stored under `figures/lime/`.
- Reproducibility metadata and reconstructed split artifacts are stored
  under `metadata/lime/`.

The LIME HTML explanations and the initial per-explanation PNG files are
not committed because they were produced before the final reliability
synthesis and should not be interpreted without the associated fidelity
metrics.
