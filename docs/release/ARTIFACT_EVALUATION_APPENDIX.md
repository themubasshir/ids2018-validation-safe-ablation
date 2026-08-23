# Artifact-Evaluation Appendix

Status: pre-release skeleton  
Scope: static, provenance-preserving evaluation of the frozen Stage 1–28 repository

This appendix defines the reviewer-facing artifact surface. It does not claim full end-to-end reproduction and does not authorize scientific execution. Stage 28 is the final empirical wall; Stage 29 and the present release work are synthesis/publication engineering only.

## 1. Artifact overview

The artifact contains safety-gated reproduction interfaces, frozen configurations, executed-notebook provenance, models and results, claim-to-artifact indexes, and static/equivalence tests for a multi-axis intrusion-detection validation study. Reviewers can inspect methodology, verify file identity and registry consistency, reproduce Stage 25 analytic tables from frozen scalars, and examine Stage 26's archival profiling evidence.

## 2. Repository organization

| Path | Reviewer purpose |
| --- | --- |
| `manuscript/manuscript_final_content.md` | Canonical scientific content |
| `src/ids_validation/` | Extracted reusable methods and safe infrastructure |
| `scripts/reproduce_stageXX.py` | Public dry-run/verify-only interfaces |
| `configs/stageXX/` | Machine-readable stage protocols |
| `notebooks/archive/` | Immutable historical execution evidence |
| `results/`, `figures/`, `tables/`, `models/`, `metadata/` | Frozen scientific artifacts |
| `docs/reproducibility/` | Provenance, equivalence, gap, and traceability registries |
| `environment/` | Modern tooling setup and historical environment receipts |
| `tests/` | Approved static, toy-fixture, and deterministic-scalar checks |

## 3. Scientific execution boundary

The binding boundary is `docs/reproducibility/SCIENTIFIC_EXECUTION_BOUNDARY.md`. Review activity may parse metadata, hash files, inspect sources, run static tests, exercise generic helpers on toy fixtures, and reproduce Stage 25 equations from frozen scalars. It may not fit/load models, infer on data, open targets or holdouts, select thresholds, regenerate metrics/figures, profile hardware, reconstruct datasets, or reopen Stage 28.

## 4. Reproducibility classifications

- **Fully reproducible from frozen input scalars:** Stage 25 only.
- **Methodology reproducible; historical timings archival:** Stage 26 only.
- **Partially reproducible/static scientific evidence:** Stages 1–24 and 27–28.

The authoritative per-stage classification is `docs/reproducibility/STAGE_REPRODUCIBILITY_STATUS.csv`. “Partial” is not a failed full-reproduction claim; it is the declared ceiling imposed by external inputs, closed targets, missing historical runtimes, or nonportable observations.

## 5. Environment setup

Use Python 3.12 for the modern verification environment:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Optional inspection packages are listed in `environment/optional_requirements.txt`. Installing them does not enable scientific execution. Historical runtimes remain stage-specific evidence in `environment/ENVIRONMENT_REGISTRY.csv` and must not be collapsed into a universal environment.

## 6. Stage wrappers

Each Stage 1–28 wrapper requires exactly one safe mode:

```text
python scripts/reproduce_stage22.py --dry-run
python scripts/reproduce_stage22.py --verify-only
```

`--dry-run` reports governed methodology and paths. `--verify-only` streams configured files for size/SHA-256 checks and validates declarations. Neither mode deserializes models or scientific arrays. No unrestricted or default scientific execution mode is exposed.

## 7. Config registry

The authoritative registry is `docs/reproducibility/CONFIG_REGISTRY.csv`; stage files live under `configs/stageXX/`. Every row identifies its historical source, protocol, frozen dependencies, environment evidence, and `scientific_execution_allowed=FALSE` boundary. All JSON configs must parse before release.

## 8. Equivalence levels

| Level | Meaning |
| --- | --- |
| A | Byte/hash identity |
| B | Exact static or numerical identity |
| C | Tolerance-equivalent behavior on synthetic/approved fixtures |
| D | Structural or provenance equivalence |

The exact scope and limitation of each assertion are recorded in `docs/reproducibility/EQUIVALENCE_MATRIX.csv`. A component-level equivalence row does not imply full-stage scientific rerun capability.

## 9. Test suite

Run the approved suite from the repository root:

```text
python -m unittest discover -s tests
```

Tests cover archive identity, protocols, configs, registries, safe wrapper behavior, deterministic formulas, toy numeric helpers, manuscript integrity, and pre-release metadata. They do not access datasets, load scientific models, or generate new results.

## 10. Claim-to-artifact traceability

Begin with `docs/reproducibility/MANUSCRIPT_REPRODUCTION_INDEX.csv`, then follow the claim to its frozen result, figure/table, config, safe entry point, canonical source, equivalence row, environment receipt, and limitation. The final manuscript claim audit and Stage 29 claim-to-artifact registry provide the publication layer.

## 11. Fully reproducible component (Stage 25)

Stage 25 regenerates prevalence, PPV, workload, capacity, and break-even tables from already-frozen TPR/FPR/confusion scalars. It needs no predictions, labels, targets, models, or hardware profiling. The focused verification is:

```text
python -m unittest tests.test_stage25_to_stage28_equivalence.Stage25AnalyticEquivalenceTests
```

This is deterministic analytic reproduction of frozen formulas, not a new prevalence experiment.

## 12. Hardware-specific archival component (Stage 26)

Stage 26 preserves CPU and single-T4 profiling protocols, raw historical samples, manifests, and receipts. Reviewers can verify their identity and inspect the method. Latency, throughput, memory, cold-start, and extraction timings must not be rerun or expected to match on another system; operating system, affinity, thread settings, drivers, runtime versions, and synchronization affect them.

## 13. Partial/static evidence stages

Stages 1–24 and 27–28 expose their source maps, configs, receipts, frozen results, and strongest supported equivalence checks. Typical ceilings include unavailable external data, incomplete dependency receipts, closed target/holdout ledgers, missing bootstrap arrays, and deliberately disabled inference. See `docs/reproducibility/REPRODUCIBILITY_GAPS.csv` for the complete gap register.

## 14. Known gaps

- External raw datasets and some historically materialized corpora are absent.
- Some exact historical dependency versions remain `VERSION_NOT_PROVEN`.
- Frozen targets, predictions, explanation arrays, and models are intentionally not reopened by public interfaces.
- Stage 24 retains two cancelled `GROUNDED_S4` cells.
- Stage 26 observations are hardware-specific.
- Low-support families and frozen realizations limit inference.
- The requested two-decimal abstract rounding remains blocked by six-decimal registry rules.

## 15. Dataset access requirements

No raw dataset is distributed. `DATASET.md` identifies the processed CSE-CIC-IDS2018 reference file and acquisition boundary; later stages also require external CICIDS2017 inputs. Users must obtain data under current upstream terms and verify expected hashes/provenance. Data acquisition alone does not authorize scientific reruns in this release.

## 16. Expected storage requirements

The tracked repository is approximately 2.3 GB, dominated by frozen results and model artifacts. Allow additional working space for Git operations and verification. External raw datasets and reconstructed corpora require substantial separate storage; no consolidated estimate is asserted because those inputs are outside the release and scientific execution is disabled.

## 17. Verification commands

```text
python -m unittest discover -s tests
python scripts/reproduce_stage25.py --dry-run
python scripts/reproduce_stage25.py --verify-only
python scripts/reproduce_stage28.py --dry-run
python scripts/reproduce_stage28.py --verify-only
```

For all wrappers in PowerShell:

```text
1..28 | ForEach-Object {
    python ("scripts/reproduce_stage{0:D2}.py" -f $_) --verify-only
    if ($LASTEXITCODE -ne 0) { throw "verification failed at Stage $_" }
}
```

Verification checks the available frozen package. Missing external inputs remain declared gaps; reviewers should not substitute or reconstruct them inside this release evaluation.

## 18. Limitations of artifact reproducibility

The artifact supports strong provenance and static consistency but not universal bitwise or end-to-end reproduction. Hash identity establishes artifact identity, not scientific validity by itself. Deterministic scalar equality does not reopen the population that produced the scalars. Toy-fixture equivalence does not reproduce historical observations. Hardware methodology portability does not imply timing portability. The artifact should therefore be evaluated against its declared component-level classifications and claim ceilings, not against an unasserted full-rerun standard.
