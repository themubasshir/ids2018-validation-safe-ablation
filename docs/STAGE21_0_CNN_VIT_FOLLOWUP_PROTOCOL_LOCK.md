# Stage21-0 — CNN vs ViT Follow-up Protocol Lock

**FROZEN BEFORE ANY STAGE21 REAL-DATA FORWARD PASS OR TRAINING**

Parent sealed Stage20 commit: `166d2a13020c0961fe703fa3103f9b29a9cdf340`

Protocol JSON SHA256: `1a60a0e6b12e88e9c8ceefb83278b71011b4fa396e821c22a093b69fcdb364f5`

ViT module SHA256: `3af99e4ea7061c68a676dc8fa7e485a7d13278f8947e4f8a8fbf2069dc31e3cb`

## Study status

Stage21 is a **preregistered post-Stage20 architecture follow-up**.

Friday is **not** described as a new blind holdout. Stage20 Friday outcomes are
already known, and the decision to test a ViT follows the observed temporal
generalization failure of the CNN.

Friday's Stage21 role is therefore:

**LOCKED REUSE BENCHMARK — NON-CONFIRMATORY**

A future claim of independently confirmed architecture superiority requires a
new preregistered evaluation on unseen data.

## Frozen comparison

Comparator:

- `Stage20MaskedCNNv1`
- immutable Stage20 checkpoint
- 93,025 trainable parameters
- no Stage21 retraining

Single Stage21 candidate:

- `Stage21MaskedViTv1`
- 91,969 trainable parameters
- parameter difference: −1,056 (−1.135%)
- training from scratch
- no external pretrained weights

No second candidate may be substituted if the ViT performs poorly.

## Frozen ViT

- input: 64 × 256 × 1
- patch: 8 packet rows × 16 byte columns
- grid: 8 × 16 = 128 patch tokens
- embedding: 64
- heads: 4
- depth: 2
- MLP: 160
- pre-LayerNorm
- GELU
- trainable CLS token
- trainable positional embedding
- classifier dropout: 0.25
- attention dropout: 0
- MLP dropout: 0
- stochastic depth: none
- explicit padding-aware attention-key masking
- mask is never concatenated as a learned feature channel

Synthetic verification proved that changing values only in padded positions
leaves logits **exactly identical** when the Boolean mask is unchanged.

## Frozen optimization budget

Identical to Stage20 CNN:

- seed 42
- exactly 10 epochs
- batch 256
- AdamW
- lr 0.001
- weight decay 0.0001
- betas (0.9, 0.999)
- eps 1e-8
- BCEWithLogitsLoss
- frozen TRAIN pos_weight 121.448384201077
- gradient clip 5
- no scheduler
- no augmentation
- no early stopping
- no validation during training
- no hyperparameter search

## Data roles

TRAIN: Monday + Tuesday + Wednesday.

VALIDATION: Thursday only.

Friday: locked reuse benchmark only. It may not select the architecture,
epoch, optimizer, threshold, representation, join, or any model change.

The Stage20 exact S4 supervision, packet-image representation, encoder, masks,
and compact-corpus semantics remain unchanged.

## Evaluation

Thursday uses the exact Stage20 E3 threshold grid and tie rules.

Friday performs no threshold search. Stage21 reports the standard 0.50
operating point and ViT operating points selected on Thursday.

The co-primary descriptive architecture deltas are:

- ViT − CNN Friday ROC-AUC
- ViT − CNN Friday PR-AUC

A fixed paired 10,000-replicate flow bootstrap (seed 21042) will provide
descriptive 95% percentile intervals for those two deltas.

These are not presented as independent confirmatory inference because Friday
was already observed before Stage21 was conceived.

## Next checkpoint

`Stage21-1R`: restore or source-faithfully reconstitute the Stage20
Monday/Tuesday/Wednesday/Thursday compact corpora with frozen hash/order
equivalence before any ViT training.
