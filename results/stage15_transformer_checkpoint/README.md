# Stage 15 Transformer Checkpoint

This package contains the complete Transformer feasibility,
duplicate-safe data partitioning, preprocessing, architecture
screening, convergence repair, five-seed confirmation, and
operating-threshold stabilization artifacts.

## Frozen model policy

- Architecture: FT_BALANCED
- Trainable parameters: 159169
- Numerical predictors: 70
- Independent confirmation seeds: 7, 29, 101, 313, 997
- Operating threshold: 0.73
- Decision rule: probability >= 0.73 predicts attack

## Five-seed architecture confirmation

- Mean validation F1: 0.8657764121097257
- F1 standard deviation: 0.0013195381641824143
- Worst-seed validation F1: 0.8635455023671751
- Mean validation recall: 0.77433595211373
- Mean validation PR-AUC: 0.9261649995539398
- Seed wins: 4 of 5
- Mean F1 margin over runner-up: 0.002301870050082866
- Best-checkpoint ceiling hits: 0

## Frozen-threshold validation performance

- Threshold: 0.73
- Mean accuracy: 0.9322320602616625
- Mean precision: 0.9859272946228013
- Mean recall: 0.7712121212121211
- Mean F1: 0.8654450257424102
- F1 standard deviation: 0.001142542079354036
- Worst-seed F1: 0.8635455023671751
- Mean F2: 0.8063296130739867
- Mean FPR: 0.004339977158014959
- Mean FNR: 0.22878787878787882

## Pre-holdout lock

The architecture, common operating threshold, and exact five
checkpoint hashes were locked before any holdout evaluation.

At package creation:

- Holdout opened: false
- Holdout evaluations: 0
- Holdout status: UNTOUCHED

The next permitted action is one final duplicate-safe holdout
evaluation using only the locked checkpoints and threshold.

## Packaging policy

Runtime-generated `__pycache__` directories, `.pyc` files, and
`.DS_Store` files are excluded.
