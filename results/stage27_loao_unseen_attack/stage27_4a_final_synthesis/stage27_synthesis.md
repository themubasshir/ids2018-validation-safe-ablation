# Stage27 Final Synthesis — Unseen Attack-Family Generalization Audit

Scientific parent: `4195be1c4fde26f76a3426728c5dd3b12d389e82`

## Scope and validity

Stage27 evaluated chronology-first, zero-training-exposure attack-family transfer under a frozen TRAIN < VALIDATION < TARGET protocol. It is an unseen attack-family generalization audit, not a formal proof of zero-day detection.

Of seven preregistered families, 5 were structurally executable and 2 were structurally ineligible. DOS was ineligible because the only earlier day-atomic training partition contained no known-family attack positives; AUTH_BRUTE_FORCE was ineligible because insufficient earlier weekday depth existed for separate training and validation days.

INFILTRATION was executable but remains descriptive-only because its held-out target support was 36 (<50). BOT, DDOS, PORT_SCAN, and WEB_ATTACK satisfy the frozen family-level inferential support rule.

All reported 95% intervals are the preregistered 2,000-replicate stratified row-bootstrap intervals and quantify target-sampling uncertainty conditional on the already-fitted model. They do not include training-seed, model-selection, or broader population uncertainty.

## Primary unseen-family ranking results

### BOT

- XGBOOST: ROC-AUC 0.3224 (95% CI 0.3102–0.3354), PR-AUC 0.0033 (95% CI 0.0032–0.0033), and BALANCED-threshold recall 0.00%.
- LIGHTGBM: ROC-AUC 0.5591 (95% CI 0.5521–0.5660), PR-AUC 0.0049 (95% CI 0.0048–0.0050), and BALANCED-threshold recall 0.00%.
- Frozen behavioral similarity: 0.6994; nearest seen family: AUTH_BRUTE_FORCE; nearest-seen distance: 0.4297.

### DDOS

- XGBOOST: ROC-AUC 0.9982 (95% CI 0.9981–0.9983), PR-AUC 0.9925 (95% CI 0.9918–0.9931), and BALANCED-threshold recall 66.20%.
- LIGHTGBM: ROC-AUC 0.9986 (95% CI 0.9985–0.9987), PR-AUC 0.9940 (95% CI 0.9933–0.9946), and BALANCED-threshold recall 26.25%.
- Frozen behavioral similarity: 0.3834; nearest seen family: DOS; nearest-seen distance: 1.6081.

### INFILTRATION

- XGBOOST: ROC-AUC 0.7816 (95% CI 0.7473–0.8142), PR-AUC 0.0002 (95% CI 0.0002–0.0002), and BALANCED-threshold recall 0.00%.
- LIGHTGBM: ROC-AUC 0.7537 (95% CI 0.7239–0.7865), PR-AUC 0.0002 (95% CI 0.0001–0.0002), and BALANCED-threshold recall 0.00%.
- Frozen behavioral similarity: 0.0156; nearest seen family: AUTH_BRUTE_FORCE; nearest-seen distance: 62.9628.
- Interpretation restriction: descriptive only because held-out support is 36.

### PORT_SCAN

- XGBOOST: ROC-AUC 0.5506 (95% CI 0.5487–0.5524), PR-AUC 0.3622 (95% CI 0.3605–0.3640), and BALANCED-threshold recall 0.48%.
- LIGHTGBM: ROC-AUC 0.7559 (95% CI 0.7546–0.7570), PR-AUC 0.4191 (95% CI 0.4176–0.4206), and BALANCED-threshold recall 1.17%.
- Frozen behavioral similarity: 0.6506; nearest seen family: AUTH_BRUTE_FORCE; nearest-seen distance: 0.5370.

### WEB_ATTACK

- XGBOOST: ROC-AUC 0.9693 (95% CI 0.9660–0.9726), PR-AUC 0.7206 (95% CI 0.7018–0.7396), and BALANCED-threshold recall 77.80%.
- LIGHTGBM: ROC-AUC 0.9901 (95% CI 0.9887–0.9914), PR-AUC 0.7605 (95% CI 0.7400–0.7817), and BALANCED-threshold recall 52.11%.
- Frozen behavioral similarity: 0.4600; nearest seen family: AUTH_BRUTE_FORCE; nearest-seen distance: 1.1739.

## High-level interpretation

The observed pattern is most consistent with selective family transfer rather than broad universal unseen-family generalization. DDOS and WEB_ATTACK retained strong ranking discrimination for both preregistered learners. BOT showed substantial collapse, including zero recall at the frozen operating points. PORT_SCAN was mixed and materially learner-dependent, with LightGBM retaining stronger ranking signal than XGBoost. INFILTRATION exhibited moderate ROC ranking values but is descriptive-only and had zero recall at its frozen operating points.

The results also support a ranking–threshold divergence interpretation: meaningful ranking information can survive for some unseen families even when frozen validation-selected operating points do not produce reliable held-out-family recall.

Learner choice matters for some families. The two learners agree strongly on DDOS and WEB_ATTACK transfer, while BOT and especially PORT_SCAN show materially different ranking behavior between XGBoost and LightGBM.

## Behavioral similarity

The preregistered 11-descriptor behavioral-similarity analysis is secondary and descriptive only. The five observed family similarities do not show a monotonic relationship with unseen-family ranking performance: BOT had the highest similarity to a seen family yet weak unseen-family discrimination, while DDOS had lower similarity but near-perfect ranking performance. WEB_ATTACK also retained strong ranking at an intermediate similarity value. Therefore behavioral proximity, as operationalized by this descriptor-centroid distance, does not appear sufficient by itself to explain the observed transfer pattern.

No formal correlation test, p-value, regression inference, causal claim, or strong-correlation claim is authorized from this secondary analysis.

## Scientific conclusion

Under the frozen chronology-first Stage27 protocol, unseen attack-family transfer was family-dependent. Strong discrimination survived for some held-out families, whereas others collapsed or showed substantial learner dependence. Consequently, performance on known attack families should not be treated as evidence of uniform generalization to unseen attack families. The Stage27 findings are best described as selective unseen-family transfer with important ranking–threshold and learner-dependent effects.

## Reporting restrictions

- Do not describe Stage27 as formal zero-day detection proof.
- Prefer: unseen attack family, zero-training-exposure family, attack-family novelty, or LOAO generalization.
- Do not make inferential family-level claims for INFILTRATION.
- Do not interpret raw PR-AUC known-minus-unseen differences as a prevalence-invariant primary novelty gap; PR-excess is the compatible primary PR gap.
- Do not infer causality or statistically significant correlation from behavioral similarity.
- Do not reopen targets, rerun model inference, refit models, or reselect thresholds.
