"""Static Stage20-1E0/1E2 training protocol metadata."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingSpec:
    """Frozen training settings; not a trainer or estimator."""

    seed: int
    epochs: int
    batch_size: int
    optimizer: str
    learning_rate: float
    weight_decay: float
    loss: str
    gradient_clip_norm: float
    precision: str
    validation_during_training: bool


TRAINING_SPEC = TrainingSpec(
    seed=42,
    epochs=10,
    batch_size=256,
    optimizer="AdamW",
    learning_rate=0.001,
    weight_decay=0.0001,
    loss="BCEWithLogitsLoss(TRAIN_benign/TRAIN_attack pos_weight)",
    gradient_clip_norm=5.0,
    precision="FLOAT32_NO_AMP",
    validation_during_training=False,
)

TRAINING_DAYS = ("Monday", "Tuesday", "Wednesday")
TRAINING_COUNTS = {"BENIGN": 541_174, "ATTACK": 4_456, "TOTAL": 545_630}
FINAL_CHECKPOINT_SHA256 = "3ebc71e579dc8e0e545981b2d60eea643148fe53e0902f8df8e47556243ad30b"
FINAL_CANONICAL_STATE_SHA256 = "ae9c913b13db62ab933198dd7721f0d1826b26a55773e3b560dc735cbb8c8092"
