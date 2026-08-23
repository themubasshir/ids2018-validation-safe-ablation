# Abstract blueprint

This is a structured content plan, not polished final prose.

1. **Problem.** High benchmark discrimination is often treated as evidence of deployable intrusion detection, although those inferences depend on split geometry, feature cues, target domain, prevalence, computational context, unseen-family support, and model realization (CLM29-001).
2. **Gap.** These validity dimensions are often reported separately; the paper needs one claim-bounded chain without a heterogeneous composite score.
3. **Framework.** Describe eight distinct validity axes plus protocol locking and provenance. State that native metrics remain separate and every claim maps to frozen evidence.
4. **Strongest findings.** The processed reference holdout produced XGBoost F1 0.9285008671 and PR-AUC 0.9776433333 (E29-006). On the shared 1,374,133-row forward target, five-seed random-natural mean PR-AUC was 0.2599 (SD 0.0034) versus chronological-natural 0.6388 (SD 0.0322), with the ordering holding in 5/5 frozen seeds (E29-037; E29-038). Forward bridge62 transfer reached PR-AUC 0.667483 and ROC-AUC 0.733946, whereas reverse transfer reached 0.108176 and 0.525167 (E29-024; E29-025).
5. **Counterexample/nuance.** Stronger ranking did not guarantee threshold transfer (E29-021); shortcut effects were split- and learner-dependent rather than one causal mechanism (E29-022; E29-023); unseen-family results were selective, with BOT learner-dependent and Infiltration descriptive at support 36 (E29-034; E29-035; E29-039).
6. **Operational implication.** At 0.1% assumed prevalence, one frozen point projected PPV 0.965572 yet 33.5 analyst-hours/day, while another projected PPV 0.000551068 and only 0.0322 true alerts/day (E29-028; E29-029). Computational claims are restricted to measured Stage26 hardware (E29-032).
7. **Scope limitation.** State benchmark-specific datasets, bridge restrictions, prior-shift and analyst-cost assumptions, five-seed scope, low-support/ineligible families, hardware specificity, conditional uncertainty, and incomplete full-rerun reproducibility (LIM29-001–LIM29-018).

The abstract must not call Stage28 a new blind holdout, describe 5/5 as significance, average cross-stage metrics, or claim zero-day detection.
