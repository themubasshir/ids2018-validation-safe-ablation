# Stage 15 Transformer Experiment

This package preserves the complete duplicate-safe Transformer
feasibility experiment, including architecture screening,
convergence repair, five-seed confirmation, threshold
stabilization, the immutable pre-holdout decision lock, and the
single final holdout evaluation.

## Frozen model policy

- Architecture: FT_BALANCED
- Trainable parameters: 159,169
- Predictors: 70 numerical features
- Checkpoint seeds: 7, 29, 101, 313, 997
- Ensemble: unweighted arithmetic mean probabilities
- Operating threshold: 0.73
- Decision rule: ensemble probability >= 0.73 predicts attack

## Duplicate-safe holdout

- Rows: 46,849
- Benign: 33,674
- Attack: 13,175
- Holdout evaluations: 1
- Status: EVALUATED_ONCE

## Primary ensemble holdout result

- Accuracy: 0.9331042284787295
- Precision: 0.9909064241713113
- Recall: 0.7691840607210626
- F1: 0.8660798222374156
- F2: 0.8052187455305353
- False-positive rate: 0.002761774662944705
- False-negative rate: 0.23081593927893737
- Matthews correlation coefficient: 0.8341528410178524
- ROC-AUC: 0.9543620498317444
- PR-AUC: 0.9287861970480663
- Brier score: 0.06361848212645473
- Log loss: 0.21022838568430788

## Confusion matrix

- True negatives: 33581
- False positives: 93
- False negatives: 3041
- True positives: 10134

## Individual-checkpoint robustness

- Mean F1: 0.8653187697770944
- F1 standard deviation: 0.0014939135859888047
- Minimum F1: 0.8628659476117103
- Maximum F1: 0.8665730934456213
- Mean PR-AUC: 0.925171859943149

## Validation-to-holdout generalization

- F1 gap: -0.0002331472430696646
- Precision gap: 0.002769815423558142
- Recall gap: -0.0020467660653197273
- PR-AUC gap: -0.000785395771920272

## Scientific integrity

The architecture, operating threshold, five checkpoint hashes,
and ensemble rule were committed before the holdout was opened.

No architecture selection, checkpoint selection, threshold search,
threshold adjustment, calibration fitting, hyperparameter tuning,
or retraining was performed using holdout results.

The holdout must not be reopened for additional model-selection
decisions.

## Interpretation boundary

These results establish Transformer feasibility and stable
duplicate-safe generalization. Claims of superiority over
classical models require a direct comparison under the same
duplicate-safe split and evaluation policy.

## Packaging policy

Runtime-generated `__pycache__` directories, `.pyc` files, and
`.DS_Store` files are excluded.
