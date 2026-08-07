# Stage 17 — Attention Explainability Scientific Closure

## Status

**SCIENTIFICALLY CLOSED**

Repository parent at closure:

`50327e10a97083e79c934b1874fd06360eeb15d5`

Stage 17 introduces no further model selection, threshold tuning, holdout access, or explanation recomputation.

---

## 1. Attention methodology

The frozen `FT_BALANCED` numerical FT-Transformer was analyzed using all five validation-selected checkpoints:

- seed 7
- seed 29
- seed 101
- seed 313
- seed 997

The model contains 70 feature-specific numerical tokens plus a CLS token, three Transformer encoder layers, and eight attention heads per layer.

A deterministic 64-case duplicate-safe validation panel was fixed before attention extraction:

- 16 TP
- 16 TN
- 16 FP
- 16 FN

The extraction produced:

- 7,680 head-level CLS-to-feature attention matrices
- 320 attention-rollout vectors
- zero additional training events
- zero holdout openings

Attention is interpreted as a **model-behavior diagnostic**, not as a causal attribution mechanism.

---

## 2. Global attention structure

Five-seed consensus rollout top three:

| Rank | Feature | Rollout attention |
|---:|---|---:|
| 1 | Fwd Seg Size Min | 0.033729732 |
| 2 | Init Fwd Win Byts | 0.028856766 |
| 3 | Dst Port | 0.023802902 |

Cross-seed stability:

| Measure | Result |
|---|---:|
| Mean Spearman | 0.448482198 |
| Minimum Spearman | 0.263756452 |
| Mean cosine | 0.970638085 |
| Minimum cosine | 0.955024311 |
| Mean top-10 Jaccard | 0.384798535 |
| Minimum top-10 Jaccard | 0.250000000 |

The checkpoints therefore share a highly similar broad attention distribution while showing only moderate stability in exact feature ordering and top-k membership.

---

## 3. Class and prediction-state behavior

| Comparison | Spearman | Cosine | Top-10 Jaccard |
|---|---:|---:|---:|
| True attack vs true benign | 0.864613770 | 0.988331099 | 0.666666667 |
| Predicted attack vs predicted benign | 0.754282215 | 0.984137273 | 0.666666667 |

True attack and benign observations retain broadly similar attention structures. Prediction-state separation produces somewhat greater rank reorganization.

---

## 4. Depth and head behavior

| Layer | Mean normalized entropy | Mean inter-head cosine |
|---:|---:|---:|
| 1 | 0.604121828 | 0.329222829 |
| 2 | 0.728813433 | 0.670422108 |
| 3 | 0.888300037 | 0.902316901 |

Attention becomes increasingly diffuse with depth while heads become increasingly similar. Early layers therefore display greater head specialization; the final layer displays strong head redundancy.

---

## 5. Cross-method XAI agreement

All comparisons use exactly the 70 shared feature names.

| Comparison | Spearman | Cosine | Top-10 Jaccard | Top-20 Jaccard |
|---|---:|---:|---:|---:|
| Attention vs XGBoost TreeSHAP | 0.456250547 | 0.585132613 | 0.333333333 | 0.428571429 |
| Attention vs LightGBM TreeSHAP | 0.398271352 | 0.568061045 | 0.333333333 | 0.333333333 |
| Attention vs MLP IG | 0.715650424 | 0.744964309 | 0.428571429 | 0.481481481 |
| Attention vs CNN IG | 0.695608052 | 0.779445852 | 0.333333333 | 0.481481481 |

Transformer rollout attention exhibits stronger whole-vector agreement with the two neural Integrated Gradients profiles than with the two TreeSHAP profiles.

However, top-k overlap remains partial across every comparison. The explanation mechanisms therefore share some global feature structure but remain method- and model-dependent.

---

## 6. Publication-safe interpretation

Stage 17 supports the following conclusions:

1. The Transformer learns a reproducible broad attention structure across independently trained checkpoints.
2. Exact feature ordering is substantially less stable than the overall attention distribution.
3. `Fwd Seg Size Min`, `Init Fwd Win Byts`, and `Dst Port` are the three strongest five-seed rollout features.
4. Early Transformer heads are comparatively diverse, while deeper heads become more diffuse and redundant.
5. Global attention structure is broadly similar between attack and benign cases.
6. Attention agrees more strongly with frozen neural IG profiles than with frozen TreeSHAP profiles.
7. Partial top-k overlap demonstrates that the explanation methods are not interchangeable.

---

## 7. Claims Stage 17 does not support

Stage 17 does **not** establish that:

- attention is causal attribution;
- attention, SHAP, and IG are equivalent explanations;
- agreement proves explanation correctness;
- IG is universally superior to TreeSHAP;
- the cross-method comparison is a same-case attribution experiment;
- the Stage 17 findings justify changing any previously frozen model or threshold decision.

---

## 8. Limitations

- Attention was evaluated on a deterministic 64-case validation panel.
- Exact attention rankings remain checkpoint-sensitive.
- Attention is an internal-routing diagnostic rather than an inherently causal explanation.
- SHAP/IG originated from an earlier 78-feature experiment; cross-method comparison therefore uses the exact 70-feature intersection.
- The explanation methods correspond to different model families.
- Cross-method agreement is global rather than same-case.
- Integrated Gradients carries previously documented reference sensitivity.

---

## 9. Scientific boundary

During Stage 17 closure:

- new metrics: **0**
- new model fits: **0**
- new Transformer inference: **0**
- new attention extraction: **0**
- SHAP recomputations: **0**
- IG recomputations: **0**
- checkpoint selections: **0**
- head selections: **0**
- method selections: **0**
- threshold searches: **0**
- Transformer holdout openings: **0**
- classical holdout openings: **0**

---

## 10. Final status

**Stage 17 Attention Explainability is scientifically complete and closed.**

The next research phase is a representation-feasibility audit for additional Transformer-family architectures. Temporal, vision, or graph models may proceed only where the IDS2018 data supports a scientifically defensible representation.
