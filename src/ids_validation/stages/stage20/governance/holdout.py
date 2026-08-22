"""Stage 20 Friday opening ledger; no opener or evaluator is implemented."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HoldoutRecord:
    """One immutable description of the direct notebook E4 boundary."""

    source_cells: tuple[int, ...]
    maximum_openings: int
    attempted_openings: int
    scientific_content_reads: int
    inference_passes: int
    status: str


DIRECT_NOTEBOOK_RECORD = HoldoutRecord(
    source_cells=tuple(range(455, 462)),
    maximum_openings=1,
    attempted_openings=1,
    scientific_content_reads=0,
    inference_passes=0,
    status="PRELOCK_VERIFIED_KAGGLE_ATTEMPT_STOPPED_AT_OPERATIONAL_STORAGE_GATE",
)

UNMAPPED_LATER_ARTIFACTS = (
    "results/stage20_1e_training/stage20_1e4_colab_execution_environment_amendment.json",
    "results/stage20_1e_training/stage20_1e4_colab_xet_fixed4_transport_lock.json",
    "results/stage20_1e_training/stage20_1e4_colab_xet_interruption_recovery_lock.json",
    "results/stage20_1e_training/stage20_1e4_friday_holdout_compact_corpus_manifest.json",
    "results/stage20_1e_training/stage20_1e4_friday_probabilities.npy",
    "results/stage20_1e_training/stage20_1e4_friday_holdout_evaluation.json",
    "results/stage20_1e_training/stage20_1e4_friday_raw_source_release_receipt.json",
)

UNMAPPED_STATUS = "NOTEBOOK_CELL_NOT_MAPPED"
CURRENT_AUTHORIZATION = "VERIFY_FROZEN_BYTES_ONLY_NO_HOLDOUT_OPENING"
