# External Criticism Response Register

## Purpose

This is an internal manuscript-preparation register. It translates common
external criticisms into evidence-backed editorial handling. It does not name
or characterize any critic, and it does not authorize new experiments.

The classifications are:

- `RESOLVED_BY_REPRODUCIBILITY_ENGINEERING`
- `CLARIFIED`
- `SCIENTIFIC_LIMITATION_RETAINED`
- `PART_OF_PRIMARY_FINDING`
- `NOT_APPLICABLE_TO_FINAL_FRAMING`

## 1. Missing executable methodology

**Classification:** `RESOLVED_BY_REPRODUCIBILITY_ENGINEERING`

All 28 stages now have configs, package namespaces and safety-gated public
wrappers. Original notebooks/scripts, frozen outputs and equivalence evidence
are linked through source registries. “Executable” here means inspectable
methodology and approved deterministic/toy verification; it does not override
closed-target governance.

**Evidence:** `FINAL_REPRODUCIBILITY_AUDIT.md`, `CONFIG_REGISTRY.csv`,
`scripts/README.md`, `EQUIVALENCE_MATRIX.csv`.

## 2. Dependency/version ambiguity

**Classification:** `CLARIFIED`

The repository no longer presents one requirements file as a universal
historical runtime. The modern tooling environment is separated from 32
historical environment records. Exact versions are reported where proven and
all remaining unknowns stay `VERSION_NOT_PROVEN`.

**Residual limitation:** Some historical environments cannot be reconstructed
exactly from surviving receipts.

**Evidence:** `environment/ENVIRONMENT_REGISTRY.csv` and
`environment/historical/`.

## 3. Processed/rebalanced reference data

**Classification:** `SCIENTIFIC_LIMITATION_RETAINED`

The IDS2018 reference benchmark used a processed/rebalanced binary dataset.
That supports controlled validation but does not establish natural prevalence,
temporal validity or external transfer. Later stages analyze those boundaries;
they do not make the original benchmark distribution naturalistic.

**Manuscript handling:** State the dataset construction and distinguish
benchmark discrimination from deployment validity.

## 4. Fixed-hyperparameter Stage12 scope

**Classification:** `CLARIFIED`

Stage12 repeats the frozen hyperparameters across five seeds; it does not repeat
the complete hyperparameter search for every seed. The claim is robustness of
the fixed selected recipes to split/training seed, not robustness of the HPO
procedure.

**Evidence:** `configs/stage12/protocol.json` and frozen Stage12 metadata.

## 5. Model-preprocessing fairness

**Classification:** `CLARIFIED`

Preprocessing is model- and stage-specific where historically declared:
training-only scaler fitting, scaled inputs for models requiring them, and raw
tabular inputs for tree boosting where recorded. Later packet, temporal and
cross-dataset representations retain their own locks. A universal preprocessing
pipeline would be historically inaccurate.

**Residual limitation:** Comparisons across fundamentally different
representations remain conditional on their frozen protocols.

## 6. Repeated holdout analysis

**Classification:** `SCIENTIFIC_LIMITATION_RETAINED`

The research program contains multiple prospectively governed target/holdout
analyses across later stages. Terminal opening ledgers, pre-opening locks and
separate evidence layers reduce but do not erase the risk that an extended
research program accumulates knowledge about held-out populations.

**Manuscript handling:** Report opening governance and avoid presenting every
later analysis as an untouched first look. Current reproducibility tooling
never reopens a target.

## 7. Low-support categories

**Classification:** `SCIENTIFIC_LIMITATION_RETAINED`

Low-support attack categories and families limit inferential precision.
Stage27 keeps Infiltration descriptive-only and retains two structurally
ineligible LOAO folds. No pooled or inferred substitute is used to manufacture
support.

**Manuscript handling:** Separate descriptive evidence from inferential claims
and publish eligibility/support rules.

## 8. Five-percent FPR interpretation

**Classification:** `CLARIFIED`

The 5% FPR bound belongs to the Stage04 security operating-point selection.
Stage10's cost-ratio threshold search is unconstrained and must not be described
as applying the Stage04 FPR filter. Stage25 inherits identified frozen
operating points rather than selecting a new one.

**Evidence:** Stage04/10 configs, discrepancy register and equivalence matrix.

## 9. Random-versus-chronological discrepancy

**Classification:** `PART_OF_PRIMARY_FINDING`

Random/rebalanced and chronological session-safe evaluation answer different
validity questions. Stage28's frozen control makes the directional discrepancy
explicit across seeds. It should not be averaged away or framed as a software
inconsistency.

**Manuscript handling:** Present chronology as a validity stress test and the
random control as evidence about partition sensitivity.

## 10. Cross-dataset asymmetry

**Classification:** `PART_OF_PRIMARY_FINDING`

Stage24's bidirectional transfer is asymmetric under frozen semantic bridges
and extractor controls. This is central evidence against treating good
single-benchmark performance as portable validity.

**Residual limitation:** Transfer conclusions are conditional on the two
datasets, frozen bridges, source-trained models and available target support.

## 11. Realistic-prevalence workload

**Classification:** `PART_OF_PRIMARY_FINDING`

Stage25 analytically shows why benchmark precision/F1 do not determine PPV,
false-alert volume or SOC capacity at rare attack prevalence. The analysis is
fully reproducible from inherited frozen scalar operating points.

**Residual limitation:** It assumes prior-probability shift with invariant
TPR/FPR and fixed analyst service/capacity scenarios; it is not a field trial.

## 12. Excessive documentation / limited code

**Classification:** `RESOLVED_BY_REPRODUCIBILITY_ENGINEERING`

The public review surface now includes 28 configs, 28 wrappers, 28 package
namespaces, common read-only infrastructure, tests, archive/config/environment
indexes and a claim-level reproduction index. Detailed documentation remains
because it preserves long forensic and governance history, but the README,
`REPRODUCE.md` and registries provide concise entry points.

**Residual limitation:** Many scientific paths intentionally remain disabled;
more runnable science would violate the accepted boundary rather than improve
this phase.

## Editorial conclusion

Engineering criticisms should be answered with the public evidence chain.
Scientific limitations should remain visible in the abstract, methods,
discussion and stage-status table. Primary findings should not be softened into
generic caveats merely because they expose benchmark fragility. No new
experiment is needed or authorized to complete this register.
