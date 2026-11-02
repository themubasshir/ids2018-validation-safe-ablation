# Section 6 Discussion Handoff Outline

Section 6 is not drafted here. The outline below anchors discussion claims to frozen evidence and explicit ceilings.

## 6.1 Benchmark performance is not deployment evidence

- Start with the narrow reference finding: strong processed-reference holdout discrimination.
- Contrast Table 1 with temporal, transfer, prevalence, and LOAO results.
- Emphasize that high F1/ROC-AUC/PR-AUC is conditional on processed membership, representation, threshold, and prevalence.
- Cite CLM29-001; CLM29-002; CLM29-003.
- Avoid learner-equivalence or universal calibration claims.

## 6.2 Temporal validity changes the estimate and the operating decision

- Discuss the random-versus-chronological contrast on the common forward target.
- Separate ranking from threshold transfer: chronological ranking survived five seeds; thresholds transferred poorly.
- Explain why chronology and attack-family composition remain entangled.
- State that K79 excludes exact available-record reuse only; it does not establish session, endpoint, source-IP, five-tuple, or S4 independence.
- Use CLM29-008, CLM29-009, CLM29-016; Figures 1 and Table 2.

## 6.3 Shortcut and explanation evidence narrows mechanism claims

- Interpret Stage23 as conditional feature/split/learner sensitivity.
- Explain why placebo and family-composition controls prevent a causal leakage claim.
- Contrast TreeSHAP component agreement with LIME local-fidelity failures.
- Retain Stage14 Integrated Gradients and Stage17 attention evidence within documented neural contexts.
- Keep Stage18 graph and Stage21 CNN/ViT results supplement-only.
- Use CLM29-004 and CLM29-010; Figure 2; Supplement S1–S2.

## 6.4 Transferability is directional and semantic

- Discuss forward bridge62 signal versus reciprocal near-baseline transfer.
- Explain why direction-specific populations, learners, prevalence, and feature bridges preclude averaging.
- Interpret bridge70 correction as metric-specific serialization sensitivity, not a common degradation score.
- Retain the two cancelled `GROUNDED_S4` cells as evidence of an eligibility boundary, not negative model results.
- Use CLM29-011 and CLM29-012; Figure 3; Table 3; Supplement S3.

## 6.5 Ranking, threshold utility, prevalence, and workload are distinct

- Connect temporal/transfer threshold failures with Stage25 prior-shift projections.
- Discuss high PPV with high analyst workload and low workload with negligible yield.
- State fixed TPR/FPR, one-million-flow, two-minute service-time, capacity, and relative-cost assumptions.
- Avoid SOC deployment or economic claims.
- Use CLM29-009 and CLM29-013; Figure 4; Table 4; Supplement S4.

## 6.6 Computational feasibility is boundary-specific

- Interpret Stage26 p95 ratios as component-level, hardware/software/batch-specific evidence.
- Explain architecture-dependent CPU/GPU direction.
- Preserve unsupported backend statuses; do not impute missing timings.
- Separate Stage15–21 historical architecture chronology from Stage26 profiling.
- Avoid end-to-end latency, portable timing, energy, or universal architecture claims.
- Use CLM29-014; Figure 5; Supplement S5.

## 6.7 Withheld-family evidence is selective, not universal zero-day detection

- Discuss strong DDoS/Web Attack ranking, learner-dependent Bot/Port Scan outcomes, and ranking/threshold divergence.
- Preserve five eligible families, DOS/AUTH_BRUTE_FORCE ineligibility, and Infiltration support 36.
- Distinguish known-category `Infilteration` support 3,967 from LOAO `Infiltration` support 36.
- Explain why no aggregate novelty score or universal zero-day claim is justified.
- Use CLM29-015; Figure 6; Table 5; Supplement S6.

## 6.8 Stability strengthens bounded claims, not universality

- Report 108/108 new fits, 12 reuses, and closure as governance evidence.
- Interpret 5/5 temporal ordering as finite fixed-recipe descriptive stability.
- Discuss family-level stability classifications and mixed random-LOAO controls.
- Explain that controls did not isolate one causal temporal/family mechanism.
- Separate seed variation from bootstrap uncertainty.
- Use CLM29-016; Tables 2 and 5.

## 6.9 Reproducibility and evidence boundary

- Distinguish full scalar reproduction (Stage25), method-reproducible archival timing (Stage26), and partial/static evidence for most stages.
- Discuss external datasets, closed targets, hash-only arrays/checkpoints, unavailable environments, and static verification.
- Explain that Stage29 added synthesis, not empirical computation.
- Route detailed provenance to Supplement S7/Table S10.

## 6.10 Practical evaluation implications

Use the study-derived checklist without presenting it as a universal framework:

1. Define population, prevalence, duplicate handling, and split.
2. Test forward temporal validity.
3. Probe shortcut sensitivity with matched controls.
4. Evaluate transfer in both directions with semantic bridges.
5. Translate frozen rates under explicit prevalence/workload assumptions.
6. Profile the declared inference boundary.
7. Gate LOAO by eligibility and support.
8. Repeat critical claims across registered realizations.

## Discussion exclusions

- No new numerical score or robustness index.
- No claim that chronology universally improves IDS.
- No causal concept-drift explanation.
- No arbitrary-dataset portability claim.
- No universal zero-day claim.
- No real-SOC deployment claim.
- No end-to-end latency claim.
- No architecture-superiority claim from Stage18/21.
- No integration into canonical manuscript until separately authorized.
