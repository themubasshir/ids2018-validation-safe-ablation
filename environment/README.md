# Environment Package

This directory separates the modern reproducibility tooling environment from
historical scientific execution environments.

## A. Modern reproducibility environment

The modern environment is intended for package imports, deterministic/toy
helpers, config and registry parsing, SHA256 verification, and the approved
static test suite. It is not presented as the historical runtime for every
stage.

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
python -m pip install -r environment/optional_requirements.txt  # optional
python -m unittest discover -s tests -v
```

`core_requirements.txt` contains the minimal non-standard dependency needed by
the extracted numerical helpers and tests. `optional_requirements.txt` records
receipt-supported packages useful for inspecting broader historical methods.
Installing optional packages does not authorize scientific execution.

## B. Historical execution environments

Historical environments are stage-scoped evidence. P100, T4 and CPU records
must not be merged into a fictitious universal runtime. The registry records
exact versions only when a receipt proves them and uses `VERSION_NOT_PROVEN`
otherwise.

The files under `historical/` summarize the principal isolated environments.
The complete stage-by-stage status is in `ENVIRONMENT_REGISTRY.csv` and in each
`configs/stageXX/protocol.json`.

## Safety

Environment setup does not enable fits, inference, target access, bootstrap or
explanation generation, timing, dataset reconstruction, or Stage29 science.
The public wrappers remain limited to `--dry-run` and `--verify-only`.
