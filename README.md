# IDS Validation Under Distribution, Operational, and Provenance Constraints

This repository is a validation and evaluation framework for intrusion
detection systems. It asks a broader question than “which model scores best on
one benchmark?”:

> Which IDS conclusions remain credible when validation governance, time,
> shortcut features, dataset shift, deployment prevalence, hardware,
> unseen-family transfer, and seed/control stability are examined explicitly?

The repository preserves the complete Stage1–28 scientific history together
with a public, safety-gated reproducibility layer. Stage28 is the final
experimental wall; current tooling verifies frozen evidence and provenance
without reopening scientific targets.

## Canonical manuscript

The canonical scientific content is
[`manuscript/manuscript_final_content.md`](manuscript/manuscript_final_content.md).
The other manuscript candidates are preserved editorial baselines and must not
be used for formatting or submission. See [`manuscript/README.md`](manuscript/README.md)
for the canonicalization record.

## Research question

Benchmark metrics are useful but insufficient evidence of deployment validity.
This project evaluates how model rankings, operating points, explanations,
workload, transfer and stability change across increasingly demanding
validation conditions while keeping selection and holdout roles explicit.

The work is therefore best read as an IDS validity study, not a universal
model-performance claim.

## Validation framework

| Dimension | Question addressed |
|---|---|
| Benchmark reference | What do validation-selected models and operating points achieve on the frozen IDS2018 reference split? |
| Temporal validity | Do conclusions survive chronological session-safe evaluation rather than only random/rebalanced partitions? |
| Shortcut sensitivity | How much do rankings and explanations depend on shortcut-prone features? |
| Cross-dataset validity | How asymmetric is transfer between IDS2018 and CICIDS2017 under frozen semantic bridges? |
| Prevalence and SOC validity | What happens to PPV, alert burden and analyst capacity at realistic base rates? |
| Computational deployability | How do model, extraction and representation costs vary across CPU and T4 environments? |
| Unseen-family validity | Which attack families transfer under leave-one-attack-family-out evaluation, and how learner-dependent is that transfer? |
| Seed/control stability | Are conclusions stable across seeds, and how does random LOAO compare with chronological LOAO? |

## Main frozen findings

- The benchmark reference supports strong validation-selected operating points,
  but those results do not establish temporal, cross-dataset or deployment
  validity by themselves.
- Chronological evaluation and random/rebalanced evaluation are not
  interchangeable. The resulting discrepancy is part of the primary finding,
  not a nuisance to average away.
- Shortcut-sensitive features can affect predictive and explanation evidence;
  the final framing keeps those audits separate from the benchmark reference.
- Cross-dataset transfer is strongly asymmetric under the frozen bridges and
  extractor-semantic controls.
- Rare attack prevalence can sharply reduce positive predictive value and
  create infeasible alert workloads even when benchmark metrics look strong.
- Deployment latency and throughput are architecture- and hardware-dependent;
  historical Stage26 measurements are archival rather than portable promises.
- LOAO results support selective family transfer, with eligibility,
  learner-dependence and ranking/threshold divergence retained as limitations.
- Five-seed and control analyses support stability for several conclusions,
  while the frozen random-versus-chronological contrast remains directionally
  consistent. Stage28 closes the empirical program.

These statements summarize already-frozen results. No statistic was recomputed
for this README.

## Reproducibility

Start with [REPRODUCE.md](REPRODUCE.md). Every stage has:

- a machine-readable config under `configs/stageXX/`;
- a public `scripts/reproduce_stageXX.py` wrapper;
- an extracted namespace under `src/ids_validation/stages/stageXX/`;
- notebook/script provenance;
- frozen result dependencies and environment status;
- one or more equivalence records.

Public wrappers require `--dry-run` or `--verify-only`. They expose no default
scientific execution. Stage25 is deterministically reproducible from final
frozen scalar inputs; Stage26 preserves reproducible methodology and archival
timings; other stages are honestly classified as partial/static evidence.

## Repository structure

| Path | Contents |
|---|---|
| `manuscript/` | Canonical scientific content, historical editorial baselines and bibliography |
| `src/` | Reusable methodology and non-scientific infrastructure |
| `configs/` | Stage1–28 protocols and Stage20 scoped subconfigs |
| `scripts/` | Safety-gated wrappers and preserved historical scripts |
| `notebooks/archive/` | Immutable executed notebook evidence |
| `results/` | Frozen stage outputs, manifests, receipts and ledgers |
| `figures/`, `tables/`, `models/`, `metadata/` | Frozen publication and model evidence |
| `docs/reproducibility/` | Audits, source maps, equivalence, gaps, discrepancies and claim indexes |
| `docs/research_history/` | Preserved chronological project documentation |
| `environment/` | Modern tooling setup and stage-specific historical environments |
| `tests/` | Static, deterministic-scalar and toy-fixture verification |

## Scientific provenance

The evidence order is frozen results/receipts, original notebooks, existing
scripts, documentation, then interpretation. Historical execution provenance
wins over code cleanliness.

The intended trace is:

```text
claim -> frozen result/table/figure -> config + safe entry point
      -> extracted/preserved method -> notebook/script source
      -> provenance + equivalence record
```

Useful starting points:

- `docs/reproducibility/FINAL_REPRODUCIBILITY_AUDIT.md`
- `docs/reproducibility/STAGE_REPRODUCIBILITY_STATUS.csv`
- `docs/reproducibility/MANUSCRIPT_REPRODUCTION_INDEX.csv`
- `docs/reproducibility/EQUIVALENCE_MATRIX.csv`
- `docs/reproducibility/NOTEBOOK_ARCHIVE_REGISTRY.csv`
- `environment/ENVIRONMENT_REGISTRY.csv`

## Limitations

- Raw IDS2018/IDS2017 data and several historically materialized corpora are
  external to the repository.
- A processed/rebalanced benchmark is useful for controlled reference
  evaluation but is not representative of deployment prevalence.
- Some exact historical dependencies remain `VERSION_NOT_PROVEN`.
- Most stages are partial/static reproducibility cases because models,
  holdouts, explanations and bootstrap arrays are deliberately not reopened.
- Stage12 repeats fixed hyperparameters rather than a full search for every
  seed.
- Low-support families restrict inferential claims, including the descriptive-
  only Infiltration fold.
- Cross-dataset validity is asymmetric and depends on frozen semantic bridges.
- Hardware-specific timing cannot be expected to reproduce exactly elsewhere.
- Documentation volume reflects a long forensic research history; the public
  indexes and wrappers are the recommended review surface.

The full unresolved-gap register is
`docs/reproducibility/REPRODUCIBILITY_GAPS.csv`.

## Historical record

The former stage-by-stage README has been preserved at
`docs/research_history/README_STAGE_DIARY.md`. It is historical context, not
the current reproduction guide.

## Citation

A final manuscript citation is not yet available. Until then, cite the
repository, commit hash, and the specific frozen artifact or equivalence row
used in an analysis.

## License

No repository license file is currently present. Users must not assume rights
beyond those granted by applicable law or by the owners of upstream datasets
and dependencies. A formal project license should be added before broad reuse.
