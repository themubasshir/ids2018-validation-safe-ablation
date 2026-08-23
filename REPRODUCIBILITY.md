# Reproducibility Status

The Stage1–28 reproducibility extraction is complete. The repository now has:

- 28 stage-specific configs;
- 28 safety-gated public wrappers;
- 28 extracted stage namespaces;
- eight immutable executed notebook archives, plus separately classified
  partial/export notebooks;
- frozen result, environment, source and manuscript-claim registries;
- an approved static equivalence/test suite.

The complete user guide is [REPRODUCE.md](REPRODUCE.md). The reviewer-facing
audit is
`docs/reproducibility/FINAL_REPRODUCIBILITY_AUDIT.md`.

## Scientific boundary

Stage28 is the final empirical wall. Reproducibility engineering does not
authorize fits, inference, target/holdout openings, threshold selection,
bootstrap or explanation generation, timing, data reconstruction, feature
analysis, new statistics, or Stage29 experiments.

Every `scripts/reproduce_stageXX.py` wrapper requires exactly one of:

```text
--dry-run
--verify-only
```

There is no default scientific execution mode.

## Current classifications

- Stage25 is fully reproducible from final frozen scalar inputs.
- Stage26 methodology is reproducible; historical timings are archival and
  hardware-specific.
- Stages01–24 and 27–28 preserve partial/static scientific evidence and do not
  claim end-to-end rerun reproducibility.

Exact per-stage limitations are published in
`docs/reproducibility/STAGE_REPRODUCIBILITY_STATUS.csv`.

## Notebook availability

The earlier statement that stage-specific notebooks were unavailable is no
longer current. The repository now preserves complete executed archives for
the Stage01–20 backbone and the Stage21–28 continuation notebooks. Their byte
identities, sizes, cell counts and canonical roles are in
`docs/reproducibility/NOTEBOOK_ARCHIVE_REGISTRY.csv`.

Partial and sanitized exports remain separately classified; a smaller export
must never replace a fuller historical execution archive.

## Environments

The modern tooling environment is defined under `environment/`. Historical
environments remain stage-scoped and use `VERSION_NOT_PROVEN` wherever exact
evidence is absent. P100, T4 and CPU records are not merged into one fictional
runtime.

## Data and targets

Raw/processed source datasets and several historically materialized corpora
remain external. Closed targets, holdouts, model artifacts and probability
arrays are not automatically opened or deserialized. Static verification
checks declarations, schemas and byte identities only.

## Historical note

The former pre-extraction reproducibility document is preserved at
`docs/research_history/REPRODUCIBILITY_PRE_EXTRACTION.md` so its earlier state
is auditable rather than silently rewritten.
