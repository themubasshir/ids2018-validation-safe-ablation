# Section 5 Results Handoff Outline

Section 5 is not drafted here. This handoff maps planned results to frozen evidence only.

| Results unit | Frozen result/artifact | Main destination | Supplement route | Limitation |
|---|---|---|---|---|
| Reference baseline, threshold, holdout metrics | `results/baseline/`, `results/tuning/`, `results/threshold/`, `results/holdout/`; `final_manuscript_numbers.csv` | Main reference results/table | S1, Table S1 | Processed within-reference population only |
| Reference uncertainty/calibration/category/seed diagnostics | `results/statistical_confidence/`, `results/calibration/`, `results/attack_category/`, `results/multiseed/` | Main qualification text | S1 | Stage-specific procedures; no universal uncertainty claim |
| Stage22R validation-to-forward ranking | `results/stage22r_training/`; `docs/STAGE22R_MANUSCRIPT_INTEGRATION.md` | Temporal main figures/results | S2; temporal evidence exhibit | K79 exact identity, not session/five-tuple independence; one historical holdout opening |
| Stage22R frozen operating-point transfer | `stage22r_final_holdout_result.json`; frozen threshold receipts | Main temporal operating-point figure/table | S2 | No post-holdout threshold repair |
| Stage23 shortcut audit | `results/stage23_shortcut_feature_audit/`; Stage23 synthesis/closure artifacts | Main shortcut qualification | S2, Tables S2–S3 | Sensitivity/attribution, not causal leakage proof |
| Stage24 bidirectional transfer | `results/stage24_cross_dataset/stage24_6_final_synthesis/`; publication package | Main transfer table/figure | S3, Tables S4–S5 | Directions distinct; bridge contracts distinct; two cancelled cells |
| Stage25 prevalence/workload/cost | `results/stage25_prevalence_stress/`; publication tables | Main operational projection | S4, Table S6 | Analytic projections, not SOC observations |
| Stage26 deployment profile | `results/stage26_deployment_profiling/`; native publication tables | Main deployment figure/table | S5, Table S7 | Prepared-input boundary; hardware-specific timing |
| Stage27 LOAO family metrics | `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/` | Main LOAO figure/table | S6, Table S8 | Five eligible families; Infiltration descriptive at 36 positives |
| Stage28 seed and random-control stability | `results/stage28_stability_novelty_control/stage28_final_synthesis/` | Main stability/LOAO qualification | S6, Table S9 | Finite-seed descriptive evidence; shared historical holdout |
| Stages15–21 architecture/representation diagnostics | Stage-specific result roots listed in `docs/reproducibility/STAGE_CODE_INVENTORY.csv` | Methods qualification only unless approved | S2 | Descriptive/supplement-only; no architecture-superiority claim |
| Provenance and reproducibility classification | `docs/reproducibility/FINAL_REPRODUCIBILITY_AUDIT.md`; source registries; equivalence matrix | Methods/limitations | S7, Table S10 | Mostly partial/static reproduction; Stage25 full scalar; Stage26 method-reproducible timing |

## Result-writing controls

- Report each metric with its population, representation, threshold role, and native uncertainty method.
- Keep PR-AUC/ROC-AUC distinct from threshold metrics.
- Do not average transfer directions or bridge conditions.
- Do not promote cancelled, unsupported, descriptive-only, or supplement-only evidence.
- Do not call Stage28 outputs a new blind holdout.
- Do not select a post-holdout winner.
- Do not reopen targets or recompute metrics during Section 5 drafting.
