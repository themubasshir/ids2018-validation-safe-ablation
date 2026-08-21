# Stage27 Publication Tables

Scientific parent:

`0e1439565aedc7da9b7ca1207262e9061422bc22`

These tables are generated exclusively from frozen Stage27 artifacts.
No target reopening, inference, model fitting, threshold reselection,
bootstrap recomputation, or new statistical testing is performed.

---

## Table 27-1. Chronology-first family executability

| Family | Status | Held-out support | Target day | Interpretation |
|---|---|---:|---|---|
| BOT | ELIGIBLE | 1,966 | Friday | Inferential support eligible |
| DDOS | ELIGIBLE | 128,027 | Friday | Inferential support eligible |
| DOS | STRUCTURALLY_INELIGIBLE | — | Wednesday | No valid supervised day-atomic training geometry |
| AUTH_BRUTE_FORCE | STRUCTURALLY_INELIGIBLE | — | Tuesday | Insufficient earlier weekday depth |
| INFILTRATION | ELIGIBLE_DESCRIPTIVE_ONLY | 36 | Thursday | Descriptive only; held-out support < 50 |
| PORT_SCAN | ELIGIBLE | 158,930 | Friday | Inferential support eligible |
| WEB_ATTACK | ELIGIBLE | 2,180 | Thursday | Inferential support eligible |

---

## Table 27-2. Primary unseen-family performance

| Family | Learner | Held-out support | ROC-AUC (95% CI) | PR-AUC (95% CI) | BALANCED recall |
|---|---|---:|---:|---:|---:|
| BOT | XGBoost | 1,966 | 0.3224 (0.3102–0.3354) | 0.003256 (0.003194–0.003331) | 0.00% |
| BOT | LightGBM | 1,966 | 0.5591 (0.5521–0.5660) | 0.004879 (0.004810–0.004958) | 0.00% |
| DDOS | XGBoost | 128,027 | 0.9982 (0.9981–0.9983) | 0.992468 (0.991825–0.993074) | 66.20% |
| DDOS | LightGBM | 128,027 | 0.9986 (0.9985–0.9987) | 0.993961 (0.993305–0.994635) | 26.25% |
| INFILTRATION† | XGBoost | 36 | 0.7816 (0.7473–0.8142) | 0.000181 (0.000156–0.000230) | 0.00% |
| INFILTRATION† | LightGBM | 36 | 0.7537 (0.7239–0.7865) | 0.000156 (0.000144–0.000193) | 0.00% |
| PORT_SCAN | XGBoost | 158,930 | 0.5506 (0.5487–0.5524) | 0.362221 (0.360462–0.363995) | 0.48% |
| PORT_SCAN | LightGBM | 158,930 | 0.7559 (0.7546–0.7570) | 0.419106 (0.417611–0.420624) | 1.17% |
| WEB_ATTACK | XGBoost | 2,180 | 0.9693 (0.9660–0.9726) | 0.720597 (0.701792–0.739629) | 77.80% |
| WEB_ATTACK | LightGBM | 2,180 | 0.9901 (0.9887–0.9914) | 0.760500 (0.739955–0.781721) | 52.11% |

† INFILTRATION is descriptive only because held-out support is 36 (<50).

The 95% intervals are the frozen 2,000-replicate stratified
row-bootstrap intervals and quantify target-sampling uncertainty
conditional on the already-fitted model.

---

## Table 27-S1. Complete frozen operating points

| Family | Learner | Operating point | Threshold | Precision | Recall | FPR | F1 |
|---|---|---|---:|---:|---:|---:|---:|
| BOT | XGBoost | STANDARD | 0.50 | 0.000000 | 0.000000 | 0.000164 | 0.000000 |
| BOT | XGBoost | BALANCED | 0.03 | 0.000000 | 0.000000 | 0.000430 | 0.000000 |
| BOT | XGBoost | SECURITY | 0.03 | 0.000000 | 0.000000 | 0.000430 | 0.000000 |
| BOT | LightGBM | STANDARD | 0.50 | 0.000000 | 0.000000 | 0.000154 | 0.000000 |
| BOT | LightGBM | BALANCED | 0.04 | 0.000000 | 0.000000 | 0.000270 | 0.000000 |
| BOT | LightGBM | SECURITY | 0.01 | 0.000000 | 0.000000 | 0.000447 | 0.000000 |
| DDOS | XGBoost | STANDARD | 0.50 | 0.999150 | 0.624071 | 0.000164 | 0.768276 |
| DDOS | XGBoost | BALANCED | 0.03 | 0.997904 | 0.661970 | 0.000430 | 0.795943 |
| DDOS | XGBoost | SECURITY | 0.03 | 0.997904 | 0.661970 | 0.000430 | 0.795943 |
| DDOS | LightGBM | STANDARD | 0.50 | 0.997002 | 0.166254 | 0.000154 | 0.284986 |
| DDOS | LightGBM | BALANCED | 0.04 | 0.996679 | 0.262538 | 0.000270 | 0.415602 |
| DDOS | LightGBM | SECURITY | 0.01 | 0.997704 | 0.627836 | 0.000447 | 0.770691 |
| INFILTRATION | XGBoost | STANDARD | 0.50 | 0.000000 | 0.000000 | 0.000201 | 0.000000 |
| INFILTRATION | XGBoost | BALANCED | 0.01 | 0.000000 | 0.000000 | 0.001353 | 0.000000 |
| INFILTRATION | XGBoost | SECURITY | 0.01 | 0.000000 | 0.000000 | 0.001353 | 0.000000 |
| INFILTRATION | LightGBM | STANDARD | 0.50 | 0.000000 | 0.000000 | 0.000125 | 0.000000 |
| INFILTRATION | LightGBM | BALANCED | 0.01 | 0.000000 | 0.000000 | 0.000232 | 0.000000 |
| INFILTRATION | LightGBM | SECURITY | 0.01 | 0.000000 | 0.000000 | 0.000232 | 0.000000 |
| PORT_SCAN | XGBoost | STANDARD | 0.50 | 0.882759 | 0.003222 | 0.000164 | 0.006420 |
| PORT_SCAN | XGBoost | BALANCED | 0.03 | 0.810840 | 0.004801 | 0.000430 | 0.009545 |
| PORT_SCAN | XGBoost | SECURITY | 0.03 | 0.810840 | 0.004801 | 0.000430 | 0.009545 |
| PORT_SCAN | LightGBM | STANDARD | 0.50 | 0.841975 | 0.002146 | 0.000154 | 0.004280 |
| PORT_SCAN | LightGBM | BALANCED | 0.04 | 0.943089 | 0.011678 | 0.000270 | 0.023071 |
| PORT_SCAN | LightGBM | SECURITY | 0.01 | 0.915641 | 0.012634 | 0.000447 | 0.024925 |
| WEB_ATTACK | XGBoost | STANDARD | 0.50 | 0.924155 | 0.514220 | 0.000201 | 0.660772 |
| WEB_ATTACK | XGBoost | BALANCED | 0.01 | 0.732930 | 0.777982 | 0.001353 | 0.754784 |
| WEB_ATTACK | XGBoost | SECURITY | 0.01 | 0.732930 | 0.777982 | 0.001353 | 0.754784 |
| WEB_ATTACK | LightGBM | STANDARD | 0.50 | 0.668605 | 0.052752 | 0.000125 | 0.097789 |
| WEB_ATTACK | LightGBM | BALANCED | 0.01 | 0.914654 | 0.521101 | 0.000232 | 0.663939 |
| WEB_ATTACK | LightGBM | SECURITY | 0.01 | 0.914654 | 0.521101 | 0.000232 | 0.663939 |

---

## Table 27-S2. Compatible novelty-generalization gaps

| Family | Learner | ROC-AUC known−unseen gap | PR-excess known−unseen gap | BALANCED recall gap |
|---|---|---:|---:|---:|
| BOT | XGBoost | 0.670536 | 0.864212 | 0.926895 |
| BOT | LightGBM | 0.436039 | 0.906726 | 0.888989 |
| DDOS | XGBoost | -0.005274 | 0.106338 | 0.264926 |
| DDOS | LightGBM | -0.003481 | 0.148981 | 0.626451 |
| INFILTRATION | XGBoost | -0.011291 | 0.187876 | 0.000416 |
| INFILTRATION | LightGBM | 0.041479 | 0.217587 | 0.000075 |
| PORT_SCAN | XGBoost | 0.442332 | 0.777767 | 0.922094 |
| PORT_SCAN | LightGBM | 0.239215 | 0.765019 | 0.877311 |
| WEB_ATTACK | XGBoost | -0.199059 | -0.527868 | -0.777566 |
| WEB_ATTACK | LightGBM | -0.194914 | -0.538086 | -0.521026 |

Raw known-minus-unseen PR-AUC differences are not treated as prevalence-invariant primary novelty gaps because the comparison populations have different prevalence anchors.

---

## Table 27-S3. Behavioral similarity

| Held-out family | Nearest seen family | Distance | Similarity | Benign distance |
|---|---|---:|---:|---:|
| BOT | AUTH_BRUTE_FORCE | 0.429700 | 0.699448 | 1.051336 |
| DDOS | DOS | 1.608051 | 0.383428 | 3.478910 |
| INFILTRATION | AUTH_BRUTE_FORCE | 62.962762 | 0.015634 | 62.942114 |
| PORT_SCAN | AUTH_BRUTE_FORCE | 0.537022 | 0.650609 | 1.223807 |
| WEB_ATTACK | AUTH_BRUTE_FORCE | 1.173886 | 0.460006 | 1.528111 |

This analysis is secondary and descriptive only. No formal correlation test, p-value, regression inference, or causal interpretation is authorized.

---

## Figure placement

### Main manuscript

1. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`
2. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

### Supplementary material

3. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains a co-primary metric and must remain in the main
results table and manuscript text even when its separate figure is
placed in supplementary material.
