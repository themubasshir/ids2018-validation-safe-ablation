# Stage21 Publication Figures

## Figure 21-1 — CNN vs ViT ranking performance

**Caption.** Ranking performance of the frozen Stage20 CNN comparator and
Stage21 parameter-matched ViT on Thursday validation and the Friday
locked-reuse benchmark. Friday results are descriptive and non-confirmatory.

Friday frozen values:

- CNN ROC-AUC: `0.43921400808023464`
- ViT ROC-AUC: `0.5686939700294255`
- ViT−CNN ROC-AUC: `0.1294799619491908`
- CNN PR-AUC: `0.48945269459245255`
- ViT PR-AUC: `0.606536911289453`
- ViT−CNN PR-AUC: `0.11708421669700042`

---

## Figure 21-2 — Paired bootstrap ranking-metric deltas

**Caption.** Frozen 10,000-replicate paired flow bootstrap distributions for
the Friday ViT-minus-CNN ROC-AUC and PR-AUC differences. Vertical solid lines
indicate the observed deltas and dashed lines indicate the frozen 95%
percentile intervals. Friday remains a locked reuse benchmark and the
intervals are descriptive rather than confirmatory.

Frozen intervals:

- ΔROC-AUC observed: `0.1294799619491908`
- ΔROC-AUC 95% CI:
  `[0.11450416392517783, 0.1445674150992717]`
- ΔPR-AUC observed: `0.11708421669700042`
- ΔPR-AUC 95% CI:
  `[0.10292121582022004, 0.1315036442879295]`

---

## Figure 21-3 — Frozen Friday operating-point behavior

**Caption.** Friday classification behavior of the frozen CNN and ViT at the
standard 0.50 threshold and the operating points selected exclusively on
Thursday validation. No Friday threshold search or reselection was performed.

Thresholds:

- standard: CNN = `0.50`, ViT = `0.50`
- validation-selected balanced: CNN = `0.17`, ViT = `0.42`
- validation-selected security: CNN = `0.17`, ViT = `0.24`

The figure should be interpreted together with the ranking-metric results:
despite the ViT's descriptive Friday improvement, absolute attack recall
remains low for both architectures.

---

## Figure 21-4 — Integrated Gradients numerical-completeness quality

**Caption.** Numerical-completeness diagnostic for the preregistered 64-step
midpoint Integrated Gradients analysis on the locked 512-flow Friday cohort.
Points show medians and whiskers show interquartile ranges. Lower values
indicate closer satisfaction of the Integrated Gradients completeness
identity. No post-result numerical accept/reject threshold was introduced.

Frozen median relative completeness errors:

- CNN / true BENIGN:
  `0.32261674106121063`
- CNN / true ATTACK:
  `0.142135888338089`
- ViT / true BENIGN:
  `0.022718177177011967`
- ViT / true ATTACK:
  `0.0011896076030097902`

The XAI figure is a **quality diagnostic**, not evidence of causal feature
importance or general ViT superiority.

---

## Scientific boundary

These figures are post-hoc visualizations of already-frozen numerical
artifacts only.

- new model forwards: **0**
- new gradients: **0**
- new IG runs: **0**
- new bootstrap replicates: **0**
- threshold search/reselection: **NO**
- training: **NO**
- architecture search: **NO**
- scientific result modification: **NO**
