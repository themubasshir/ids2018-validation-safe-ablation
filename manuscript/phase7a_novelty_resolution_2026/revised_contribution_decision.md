# Revised contribution decision

## Evidence base

Decisions use the frozen Stage 29 registry, validity-axis matrix, Sections 3–8, and inspected prior-art sources. No experiments or recomputation performed.

## A — Source-faithful IDS2018 temporal and frozen-operating-point evaluation with five-seed stability

- **Our stages:** Stage18/22/22R/28 temporal provenance, forward target, threshold transfer, five registered seed linkages, controls.
- **Claim IDs:** `CLM29-005`, `CLM29-008`, `CLM29-009`, `CLM29-016`; evidence `E29-016`, `E29-020`–`E29-023`, `E29-037`–`E29-040`.
- **Strongest competitors:** Berhili (validation/seed/protocol overlap; temporal procedure NOT_VERIFIED), Elangovan (temporal evaluation verified at article-record level), Biswas (2026 preprint: IDS2018 random, stratified-temporal, and class-blind chronological protocols), Buriboyev (temporal factor and protocol audit; peer-review status unverified).
- **Established already:** temporal/forward evaluation and seed sensitivity are prior methods.
- **Distinct observation:** chronology produced higher forward ranking for all five frozen linkages, while inherited thresholds transferred poorly; controls did not isolate one mechanism.
- **Limitations:** one shared target; chronology and family composition entangled; incomplete timestamp recovery; historical target reuse; no prospective deployment.
- **Additional conflict:** Biswas establishes the temporal-protocol sensitivity question conceptually and empirically on CSE-CIC-IDS2018, including chronological evaluation and unseen-family framing. This manuscript's distinction is its different source-faithful forward-target contract, five-seed threshold-transfer analysis, and bounded findings; it must not claim conceptual priority for temporal or attack-family evaluation.
- **Decision:** **RETAIN, NARROW.** Call it a bounded source-faithful empirical result, not a new temporal method or general temporal superiority claim.

## B — Registered shortcut controls and direction-specific semantic transfer sensitivity

- **Our stages:** Stage6/13/23 feature and explanation audits; Stage24 bridge; Stage28 controls.
- **Claim IDs:** `CLM29-004`, `CLM29-010`, `CLM29-011`, `CLM29-016`, `CLM29-020`; evidence `E29-015`, `E29-022`–`E29-027`, `E29-040`.
- **Strongest competitors:** Berhili (semantic alignment, bidirectional transfer, leakage, ablations); Elangovan (semantic/cross-domain generalization); Mishra (harmonization); Buriboyev (shortcut factor).
- **Established already:** semantic alignment, feature ablation, and cross-dataset transfer.
- **Distinct observation:** IDS2018-to-CICIDS2017 and reciprocal bridge behavior was strongly directional; subset effects depended on split and learner; placebo/control evidence blocks a single causal shortcut claim.
- **Limitations:** bridge-specific populations; two cancelled `GROUNDED_S4` cells; observational controls; no arbitrary-dataset portability.
- **Decision:** **MERGE** with A as “protocol-conditioned validity and transfer,” while retaining the direction-specific empirical findings. Do not present semantic bridges or shortcut analysis as inventions.

## C — Prevalence/workload projections, eligible-family LOAO, and hardware-specific computational profiling

- **Our stages:** Stage10/25 operational projections; Stage21/26 profiling; Stage11/27/28 LOAO and eligibility closure.
- **Claim IDs:** `CLM29-013`, `CLM29-014`, `CLM29-015`; evidence `E29-028`–`E29-039`.
- **Strongest competitors:** Ha Thanh (deployment-oriented transfer); Berhili (operating/calibration overlap; workload and LOAO NOT_VERIFIED); Buriboyev (base-rate framing; exact workload NOT_VERIFIED); recent LOAO papers identified in search but not sufficiently inspected.
- **Established already:** prevalence matters; deployment costs and unseen-family evaluation are recognized concerns.
- **Distinct observation:** PPV, alert volume, analyst-hours, yield, and cost can diverge; measured computational feasibility is hardware/software-specific; eligible-family transfer is selective, with ineligible families and low-support Infiltration retained as boundaries.
- **Limitations:** projections are not SOC observations; profiling is not end-to-end IDS latency; two LOAO families ineligible; Infiltration support 36; no universal zero-day claim.
- **Decision:** **RETAIN, NARROW.** This is the strongest bounded empirical differentiator, but combine as “operational and eligibility-gated stress tests,” not a novel framework.

## D — Claim-to-artifact synthesis with availability, cancellation, and reproducibility boundaries

- **Our stages/artifacts:** Stage29 synthesis; final claim registry; validity matrix; reproducibility audit; frozen artifact and cancellation records.
- **Claim IDs:** all retained `CLM29-*`, especially `CLM29-012`, `CLM29-014`–`CLM29-016`; limitations `LIM29-001`–`LIM29-018`.
- **Strongest competitors:** Berhili reproducibility package provides code, indices, seeds, and results; Mishra reports statistical/reproducibility procedures; general reproducibility literature establishes the broader practice.
- **Established already:** code/data/configuration documentation and reproducibility reporting.
- **Distinct observation:** study-specific claim-to-evidence mapping distinguishes direct, supported, descriptive, unavailable, cancelled, and unsupported states; cancelled cells remain non-results; static verification is not called complete rerun.
- **Limitations:** documentation is not methodological novelty or independent replication; source inputs and some historical artifacts remain unavailable.
- **Decision:** **MERGE** into the paper's evidence-governance method. Retain as a reporting/evidence contribution only if demonstrated through concrete claim boundaries, never as priority over reproducibility guidance.

## Final four-to-three structure

1. **Bounded protocol-conditioned audit:** merge A+B; source-faithful temporal evaluation, frozen operating-point transfer, registered shortcut controls, and directional semantic bridges.
2. **Operational and unseen-family stress tests:** retain narrowed C; prevalence/workload projections, hardware-specific measured paths, and eligible LOAO.
3. **Evidence-governed interpretation:** merge D; claim-level provenance, cancellation governance, and reproducibility-state boundaries.

If a four-item Introduction structure is required editorially, split item 2 into operational projections and eligibility-gated family evaluation, but do not imply four independent novelty claims.
