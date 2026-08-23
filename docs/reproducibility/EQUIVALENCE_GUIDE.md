# Equivalence Guide

## What an equivalence row means

Each row in `EQUIVALENCE_MATRIX.csv` states one bounded comparison between an
authoritative source/evidence item and a reproducibility check. The level
describes the strength of that comparison—not the reproducibility of an entire
stage.

At the accepted Stage25–28 checkpoint, the matrix contained 112 passing rows
and the approved static suite contained 127 passing tests. Those are checkpoint
facts, not constants embedded in the methodology. Use the commands below to
obtain current totals after any legitimate maintenance change.

## Levels

### Level A — byte/hash identity

The compared source or artifact has exact byte identity under the declared
hash representation. Examples include archived notebook SHA256, frozen model
or checkpoint bytes, and exact notebook-to-script cell preservation.

Level A does not mean the artifact was deserialized or executed. A checkpoint
can have Level A identity while the associated stage remains partial/static.

### Level B — exact static/numerical identity

Declared values, schemas, formulas, counts, memberships, ledgers, or allowed
deterministic outputs are exactly equal. Examples include Stage25's analytic
tables from frozen scalars and Stage28's terminal fit/reuse counts.

Level B may parse frozen JSON/CSV evidence but does not authorize a target
opening or new analysis.

### Level C — tolerance-equivalent

A mathematical helper is exercised on a synthetic or explicitly approved
fixture and agrees within a declared numerical tolerance. This supports method
semantics without claiming equality of a historical hardware/runtime run.

### Level D — structural/provenance equivalence

The preserved source structure, configuration, sequencing or provenance is
consistent where byte or numerical evidence is unavailable. Level D is an
honest ceiling, not a failed stronger check.

## Equivalence versus reproducibility class

A stage can contain Level A evidence and still be only partially reproducible.
For example, exact checkpoint bytes do not supply an external dataset, an exact
historical runtime, or permission to reopen a holdout. Reproducibility class is
therefore determined from the complete chain: source, config, environment,
inputs, frozen outputs, governance and equivalence scope.

The public classification is in `STAGE_REPRODUCIBILITY_STATUS.csv`:

- `FULLY_REPRODUCIBLE_FROM_FROZEN_INPUT_SCALARS` — Stage25 only;
- `METHODOLOGY_REPRODUCIBLE_HISTORICAL_TIMINGS_ARCHIVAL` — Stage26 only;
- `PARTIALLY_REPRODUCIBLE_STATIC_SCIENTIFIC_EVIDENCE` — all other stages.

## Obtaining current counts

PowerShell:

```text
$matrix = Import-Csv docs/reproducibility/EQUIVALENCE_MATRIX.csv
$matrix.Count
$matrix | Group-Object equivalence_level | Select-Object Name, Count
python -m unittest discover -s tests -v
```

Python:

```text
python -c "import csv; rows=list(csv.DictReader(open('docs/reproducibility/EQUIVALENCE_MATRIX.csv', encoding='utf-8'))); print(len(rows)); print({level: sum(r['equivalence_level']==level for r in rows) for level in 'ABCD'})"
```

## Safety boundary

Approved tests may parse source and static metadata, stream bytes, exercise
pure deterministic Stage25 scalar formulas, and use toy fixtures. They may not
fit/load models, infer, open targets, regenerate probability or explanation
arrays, rerun timing, reconstruct data, select thresholds, generate bootstrap
samples, or alter frozen artifacts.
