# Stage Configuration Registry

Each `stageXX/protocol.json` file is the machine-readable contract for one
historical stage. These files preserve source locations, frozen inputs and
outputs, methodology declarations, environment evidence, target/holdout
policy, and the read-only verification inventory.

The configurations are intentionally not forced into one universal schema.
Stages accumulated different evidence over time: early stages use explicit
`proven`/`unproven` environment maps, Stage20 has multiple subconfigs and
runtime lineages, and Stages21–28 include canonical-source and byte-identity
registries. Normalizing those differences would erase provenance.

## Safety contract

All 28 protocols set `scientific_execution_enabled` to `false`. Their public
wrappers support only:

```text
python scripts/reproduce_stageXX.py --dry-run
python scripts/reproduce_stageXX.py --verify-only
```

`--dry-run` describes historical operations. `--verify-only` checks declared
paths and streams configured bytes for SHA256. Neither mode authorizes a model
load, fit, inference, target opening, threshold search, bootstrap generation,
explanation generation, timing run, dataset reconstruction, or frozen-output
write.

## Index

`docs/reproducibility/CONFIG_REGISTRY.csv` provides one public row per stage.
Stage20 additionally retains the following scoped contracts:

- `provenance.json`
- `reconstruction.json`
- `representation.json`
- `compact_corpus.json`
- `cnn_governance.json`

These are subordinate historical contracts, not alternate public entry
points. Consult `REPRODUCE.md` for setup and reviewer workflows.
