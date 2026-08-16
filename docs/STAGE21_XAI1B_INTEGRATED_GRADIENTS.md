# Stage21-XAI1B — Locked Integrated Gradients

## Status

**LOCKED POST-RESULT INTEGRATED GRADIENTS COMPLETE**

Friday remains a **locked reuse benchmark / non-confirmatory** analysis.

The attribution method, cohort, baseline, integration rule, and step count were frozen before attribution execution.

## Frozen execution

- corrected harness commit: `9c429ff250f19918a19cddc0091c10676be4486d`
- corrected harness SHA256: `c9fcfa53c24009da51843a93da9bb0f9e4216c03856bf68cebbaf34ce461dfa2`
- cohort: **512 flows (256 true BENIGN / 256 true ATTACK)**
- method: **Integrated Gradients**
- target: **attack pre-sigmoid logit**
- baseline: **all-zero normalized image**
- validity mask: **fixed original flow mask**
- integration: **64-step midpoint Riemann**

## Endpoint reproduction

- CNN maximum absolute probability difference: `1.1324882507324219e-06`
- ViT maximum absolute probability difference: `1.7881393432617188e-07`

## True Benign

| Metric | CNN median | ViT median | Paired ViT−CNN median |
|---|---:|---:|---:|
| IG_RELATIVE_COMPLETENESS_ERROR | 0.3226167411 | 0.02271817718 | -0.2757964609 |
| PADDED_PIXEL_ATTRIBUTION_MASS_FRACTION | 0 | 0 | +0 |
| NORMALIZED_VALID_PATCH_ENTROPY | 0.9301664597 | 0.8140639921 | -0.09794656453 |
| TOP1_PATCH_MASS_FRACTION | 0.230026635 | 0.3188763742 | +0.07907355113 |
| TOP5_PATCH_MASS_FRACTION | 0.7849025299 | 0.8820969469 | +0.07095631952 |
| FIRST_16_PACKET_ROWS_MASS_FRACTION | 1 | 1 | +0 |
| MIDDLE_32_PACKET_ROWS_MASS_FRACTION | 0 | 0 | +0 |
| LAST_16_PACKET_ROWS_MASS_FRACTION | 0 | 0 | +0 |

## True Attack

| Metric | CNN median | ViT median | Paired ViT−CNN median |
|---|---:|---:|---:|
| IG_RELATIVE_COMPLETENESS_ERROR | 0.1421358883 | 0.001189607603 | -0.1304382227 |
| PADDED_PIXEL_ATTRIBUTION_MASS_FRACTION | 0 | 0 | +0 |
| NORMALIZED_VALID_PATCH_ENTROPY | 0.9130203755 | 0.8134399337 | -0.1331683767 |
| TOP1_PATCH_MASS_FRACTION | 0.4263545281 | 0.501769982 | +0.08222179282 |
| TOP5_PATCH_MASS_FRACTION | 0.9999999776 | 0.999999975 | +3.724240211e-08 |
| FIRST_16_PACKET_ROWS_MASS_FRACTION | 1 | 1 | +0 |
| MIDDLE_32_PACKET_ROWS_MASS_FRACTION | 0 | 0 | +0 |
| LAST_16_PACKET_ROWS_MASS_FRACTION | 0 | 0 | +0 |

## Interpretation boundary

These are post-result descriptive spatial attributions only. They do not establish causality, independent confirmation, network-field semantics from pixel position alone, or general ViT superiority.

No architecture, model, cohort, threshold, method, or baseline was selected from these attribution results.

## Scientific boundary

- training: **NO**
- optimizer steps: **0**
- threshold search/reselection: **NO**
- architecture search: **NO**
- attribution-method search: **NO**
- alternative baseline: **NO**
- cohort change: **NO**
