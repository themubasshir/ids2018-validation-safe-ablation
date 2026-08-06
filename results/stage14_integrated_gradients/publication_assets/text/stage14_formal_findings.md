# Stage 14 — Integrated Gradients Analysis

## Experimental scope

Integrated Gradients was applied to the archived validation-selected MLP
and one-dimensional CNN checkpoints. Both models used the original
repository StandardScaler and the untouched seed-42 holdout partition.
The operating threshold was 0.50 for both neural models.

The MLP achieved holdout accuracy 0.9395, recall
0.8536, F1 0.9189, and FPR
0.0028. The CNN achieved accuracy
0.9370, recall 0.8520, F1
0.9158, and FPR 0.0058.

## Attribution configuration

Attributions targeted the pre-sigmoid attack logit. A distribution-aware
baseline was constructed from 32 deterministic benign training records.
Integrated Gradients was averaged across these references. Numerical
integration used the trapezoidal rule with 128 steps, selected through a
16-, 32-, 64-, and 128-step convergence audit.

All 64 model-specific explanations satisfied the prespecified absolute
and normalized completeness tolerances. Numerical completeness therefore
supports reconstruction of the selected logit difference.

## Reference robustness

Completeness did not imply reference invariance. Under explicit
study-specific criteria, 10 of 64 explanations
(15.6%) were reference-robust, 29
(45.3%) were moderately reference-stable, and
25 (39.1%) were reference-sensitive.
At least one negatively oriented reference attribution occurred in
22 cases.

No false-negative explanation from either architecture satisfied every
reference-robustness criterion. Consequently, false-negative case
explanations should be treated as diagnostic rather than definitive.

## Global feature patterns

The MLP's five highest mean absolute attributions were:
Fwd Seg Size Min, Fwd Pkt Len Max, Bwd Pkt Len Std, Init Fwd Win Byts, Fwd Seg Size Avg.

The CNN's five highest mean absolute attributions were:
Fwd Seg Size Min, RST Flag Cnt, ECE Flag Cnt, Init Fwd Win Byts, Fwd Pkt Len Max.

The two models shared 6 top-10
features: Bwd Pkt Len Std, ECE Flag Cnt, Fwd Pkt Len Max, Fwd Pkt Len Std, Fwd Seg Size Min, Init Fwd Win Byts. Their top-10 Jaccard similarity
was 0.429. The cosine similarity
between global absolute-importance vectors was
0.911, while
the signed-attribution cosine was
0.791. Thus,
the architectures emphasized broadly similar feature magnitudes but
differed more substantially in ranking and attribution direction.

## Baseline sensitivity

The scaled-zero vector was retained only as a sensitivity control because
it represented sharply different model states: approximately 0.931
attack probability for the MLP and nearly zero for the CNN. The benign
median was a more meaningful single-reference comparator, but baseline
agreement remained case-dependent, particularly for the MLP
cross-model-disagreement cases.

## Reporting decision

Aggregate feature recurrence and reference-stable direction patterns are
the primary neural explanation results. Individual explanations may be
shown as main-text examples only when they satisfy every study-specific
reference-robustness criterion. Moderately stable cases require an
explicit sensitivity caveat, and reference-sensitive cases should remain
supplementary diagnostics.

The CNN operates on an ordered 78-feature vector. These results establish
feature-position sensitivity, not validated spatial locality between
adjacent tabular variables.
