# Reproducing the Frozen IDS Validation Study

## 1. Scientific scope

This repository preserves and verifies a 28-stage IDS validation program. Its
research focus is evaluation validity: benchmark performance, temporal
validity, shortcut sensitivity, cross-dataset transfer, realistic prevalence
and SOC workload, deployability, unseen-family transfer, and seed/control
stability.

The public reproducibility layer traces claims to frozen evidence and
historical source. It does not silently rerun experiments.

## 2. Stage28 final execution boundary

Stage28 is the final empirical stage. The boundary is defined in
`docs/reproducibility/SCIENTIFIC_EXECUTION_BOUNDARY.md` and enforced by every
public stage wrapper.

No wrapper can fit or load a model, run inference, open a target or holdout,
select a threshold, generate a bootstrap sample, recompute SHAP/LIME/IG,
profile hardware, reconstruct data, or create a new scientific result.
Stage29 and later repository work is non-experimental unless a separate future
research project explicitly authorizes new science.

## 3. Repository layout

| Path | Purpose |
|---|---|
| `src/ids_validation/` | Extracted methodology and shared read-only infrastructure |
| `configs/stageXX/` | Stage-specific machine-readable safety/method contracts |
| `scripts/reproduce_stageXX.py` | Public dry-run and verify-only interfaces |
| `notebooks/archive/` | Immutable historical execution evidence |
| `results/`, `figures/`, `tables/`, `models/`, `metadata/` | Frozen scientific evidence |
| `docs/reproducibility/` | Source maps, equivalence, gaps, discrepancies and claim traceability |
| `environment/` | Modern tooling environment and separate historical receipts |
| `tests/` | Approved static, toy and deterministic-scalar verification |

## 4. Dataset acquisition

The raw and processed datasets are not redistributed. The original benchmark
used the processed binary CSE-CIC-IDS2018 file described in `DATASET.md`; later
stages also depend on external IDS2017 PCAPs and historically materialized
corpora.

If a future separately authorized scientific project reconstructs those
inputs, obtain them under their applicable terms and verify every available
source hash, feature signature, split membership and protocol lock. Placing a
file under `data/raw/` does not authorize current wrappers to read it.

## 5. Reproducibility classes

- Stage25 is **fully reproducible from frozen input scalars**. Exact analytic
  tables can be regenerated without predictions, targets, models or hardware.
- Stage26 is **methodology reproducible / historical timings archival**.
- Stages01–24 and 27–28 are **partially reproducible / static scientific
  evidence**. Their source, configs, receipts and frozen outputs are preserved,
  but end-to-end scientific reruns are not performed by this package.

The public stage table is
`docs/reproducibility/STAGE_REPRODUCIBILITY_STATUS.csv`.

## 6. Modern environment setup

Python 3.12 is the supported modern tooling runtime. From the repository root:

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m unittest discover -s tests -v
```

Optional packages for broader source inspection are listed separately:

```text
python -m pip install -r environment/optional_requirements.txt
```

These are modern reproducibility dependencies, not a claim that one package
set reproduces every historical runtime. Consult
`environment/ENVIRONMENT_REGISTRY.csv` for stage-specific evidence.

## 7. Dry-run usage

Dry-run describes what a historical stage did and which frozen targets it
would have touched. It performs no scientific work:

```text
python scripts/reproduce_stage22.py --dry-run
python scripts/reproduce_stage26.py --dry-run
```

Exactly one mode is required. Calling a wrapper without a mode exits with an
argument error; there is no default execution path.

## 8. Verify-only usage

Verify-only validates the safety declaration, checks configured paths, and
streams configured files for size/SHA256 identity:

```text
python scripts/reproduce_stage22.py --verify-only
python scripts/reproduce_stage28.py --verify-only
```

It does not deserialize checkpoints, models or probability arrays. A reported
hash match means byte identity only.

To verify every stage in PowerShell:

```text
1..28 | ForEach-Object {
    python ("scripts/reproduce_stage{0:D2}.py" -f $_) --verify-only
    if ($LASTEXITCODE -ne 0) { throw "verification failed at Stage $_" }
}
```

## 9. Deterministic Stage25 reproduction

Stage25 is tested from final inherited TPR/FPR/confusion scalars only. The test
recreates the historical projection and break-even tables and compares every
row with the frozen CSVs:

```text
python -m unittest tests.test_stage25_to_stage28_equivalence.Stage25AnalyticEquivalenceTests -v
```

This is deterministic analytic reproduction, not prediction regeneration or a
new prevalence experiment.

## 10. Why Stage26 timings will differ elsewhere

Latency, memory, cold start, throughput and component timing depend on
hardware, operating system, affinity, threads, drivers, runtime versions and
synchronization. Stage26 preserves separate CPU and single-T4 receipts plus
raw historical samples. A different machine should reproduce the measurement
method, not identical milliseconds.

The safe tests use toy numeric arrays for percentile/statistic semantics and
never call a clock or profiler.

## 11. Why frozen targets are not reopened

Stages22, 24, 27 and 28 use terminal target/holdout ledgers. Their scientific
design depends on limited, prospectively governed openings. Automatically
reopening a target would create a new analysis event and weaken that boundary.

Verify-only therefore checks receipts and artifact identities. It never loads
the target, model or frozen probability arrays. Stage24's two unavailable
GROUNDED_S4 cells remain cancelled rather than approximated.

## 12. Equivalence levels

- **Level A — byte/hash identity:** exact source or artifact bytes.
- **Level B — exact static/numerical identity:** exact values, schemas,
  formulas, counts or deterministic outputs from allowed frozen inputs.
- **Level C — tolerance-equivalent:** numerical equivalence on synthetic or
  approved fixtures within an explicit tolerance.
- **Level D — structural/provenance equivalence:** source structure, declared
  methodology or provenance is preserved where stronger evidence is absent.

Equivalence is scoped to the statement in its matrix row. It does not imply
that an entire stage can be scientifically rerun.

## 13. Tracing a manuscript claim

Start with `docs/reproducibility/MANUSCRIPT_REPRODUCTION_INDEX.csv`. Follow its
claim ID to the frozen result/table/figure, config, public entry point,
canonical notebook/script source, equivalence row and environment record.

For deeper provenance consult:

- `MANUSCRIPT_CRITICAL_TRACEABILITY.csv`
- `CONFIG_REGISTRY.csv`
- `EQUIVALENCE_MATRIX.csv`
- `NOTEBOOK_SOURCE_MAP.md`
- `STAGE21_24_SOURCE_REGISTRY.csv`
- `STAGE25_28_SOURCE_REGISTRY.csv`

## 14. Expected compute and storage

The repository payload is roughly 2.3 GB, primarily frozen results and model
artifacts. Static tests normally finish in seconds on a conventional CPU.
Verify-only time is dominated by streaming configured artifact bytes; it does
not require a GPU.

No estimate is supplied for end-to-end model training, explanation,
cross-dataset evaluation or profiling because those paths are deliberately not
exposed. External raw datasets and reconstructed corpora would require
additional storage in a separate authorized project.

## 15. Honest limitations

- Several raw datasets and exact processed corpora are external.
- Some historical dependencies remain `VERSION_NOT_PROVEN`.
- Frozen targets and probability arrays are intentionally unopened.
- Stage26 measurements are hardware-specific.
- Low-support attack families limit some inferential claims.
- Cross-dataset transfer is asymmetric.
- The work evaluates validity boundaries; it does not establish universal IDS
  deployment performance.
