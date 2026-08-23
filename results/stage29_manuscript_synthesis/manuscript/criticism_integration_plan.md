# Criticism integration plan

This is an editorial prevention plan, not rebuttal rhetoric and not authorization for new experiments. It carries all 12 items from `docs/reproducibility/EXTERNAL_CRITICISM_RESPONSE.md` into the proposed manuscript.

| ID | Criticism | Existing classification | Manuscript action | Required location | Evidence/limitation link |
| --- | --- | --- | --- | --- | --- |
| CRIT-01 | Missing executable methodology | RESOLVED_BY_REPRODUCIBILITY_ENGINEERING | Cite reproducibility material; add a concise claim-to-provenance methods paragraph. Do not claim every scientific path is rerunnable. | Methods: reproducibility; data/code availability | FINAL_REPRODUCIBILITY_AUDIT; CONFIG_REGISTRY; EQUIVALENCE_MATRIX; LIM29-014 |
| CRIT-02 | Dependency/version ambiguity | CLARIFIED | Add methodological clarification separating the modern tooling environment from historical execution records and preserving VERSION_NOT_PROVEN. | Methods: reproducibility; limitations | environment/ENVIRONMENT_REGISTRY.csv; LIM29-010 |
| CRIT-03 | Processed/rebalanced reference data | SCIENTIFIC_LIMITATION_RETAINED | Fix any naturalistic wording; state construction near the first benchmark result and keep the limitation in main text. | Datasets; Results opening; Limitations | E29-001; E29-006; LIM29-002 |
| CRIT-04 | Fixed-hyperparameter Stage12 scope | CLARIFIED | Clarify that five seeds repeat frozen recipes, not full HPO. Avoid “HPO robustness.” | Methods: seed stability; Results reference | E29-014; LIM29-009 |
| CRIT-05 | Model-preprocessing fairness | CLARIFIED | Explain model/stage-specific frozen preprocessing and why a universal pipeline would be historically false. Retain representation comparisons as protocol-conditional. | Methods: reference models and representations | configs; claim-to-artifact map; LIM29-010; LIM29-017 |
| CRIT-06 | Repeated holdout analysis | SCIENTIFIC_LIMITATION_RETAINED | Add opening-governance clarification and explicitly state Stage28 reuses an already historically opened Stage22 target rather than a new blind holdout. | Methods: anti-adaptation; Limitations | E29-041; LIM29-018 |
| CRIT-07 | Low-support categories | SCIENTIFIC_LIMITATION_RETAINED | Publish eligibility/support rules; mark Infiltration descriptive; name ineligible families; never pool a substitute. | Unseen-family Methods/Results; Limitations | E29-013; E29-035; LIM29-006; LIM29-007 |
| CRIT-08 | Five-percent FPR interpretation | CLARIFIED | Fix wording so the 5% bound belongs only to Stage04 security selection; Stage10 is unconstrained and Stage25 inherits points. | Reference Methods; Operational Methods | E29-005; E29-012; E29-028–E29-031 |
| CRIT-09 | Random-versus-chronological discrepancy | PART_OF_PRIMARY_FINDING | Make no “software inconsistency” correction; present the direction as a primary validity result and the random arm as a control. Add causal limitation. | Temporal Results and Discussion | E29-020; E29-037; E29-038; E29-040; LIM29-003 |
| CRIT-10 | Cross-dataset asymmetry | PART_OF_PRIMARY_FINDING | Preserve as primary evidence; report directions separately, show bridge scope, and retain cancellations/conditional sensitivity. | Cross-dataset Results and Limitations | E29-024–E29-027; LIM29-004; LIM29-005 |
| CRIT-11 | Realistic-prevalence workload | PART_OF_PRIMARY_FINDING | Preserve the PPV/workload/yield distinction while labeling all outputs as prior-shift projections rather than a field trial. | Operational Results and Discussion | E29-028–E29-031; LIM29-012; LIM29-013 |
| CRIT-12 | Excessive documentation / limited code | RESOLVED_BY_REPRODUCIBILITY_ENGINEERING | Cite the concise README, REPRODUCE guide, registries, wrappers, and tests. Keep forensic detail in repository/supplement rather than main narrative. | Data/code availability; supplement | README; REPRODUCE; MANUSCRIPT_REPRODUCTION_INDEX; LIM29-014 |

## Integration rules

- The three retained scientific limitations (CRIT-03, CRIT-06, CRIT-07) must appear in the main manuscript, not only supplementary material.
- The three primary findings (CRIT-09, CRIT-10, CRIT-11) must not be softened into generic caveats or averaged away.
- The four clarifications (CRIT-02, CRIT-04, CRIT-05, CRIT-08) require precise methods wording rather than new analysis.
- The two engineering criticisms (CRIT-01, CRIT-12) are answered by traceability and concise entry points, with the incomplete-full-rerun limitation still disclosed.
