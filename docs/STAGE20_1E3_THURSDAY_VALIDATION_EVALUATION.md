# Stage20-1E3 — Thursday Validation Evaluation and Operating-Point Freeze

**THURSDAY EVALUATED ONCE; OPERATING POINTS FROZEN**

- flows: **8197**
- BENIGN: **8155**
- ATTACK: **42**
- probability SHA256: `d74c2c4abc52fc9b85b21db865390c4562e95b5153cbf35620c061d47719a42c`
- ROC_AUC: **0.929505708**
- PR_AUC: **0.065683604**

### Standard

- threshold: **0.50**
- TP/TN/FP/FN: **1 / 8154 / 1 / 41**
- Accuracy: **0.994876174**
- Precision: **0.500000000**
- Recall: **0.023809524**
- F1: **0.045454545**
- F2: **0.029411765**
- FPR: **0.000122624**
- FNR: **0.976190476**

### Balanced

- threshold: **0.17**
- TP/TN/FP/FN: **3 / 8113 / 42 / 39**
- Accuracy: **0.990118336**
- Precision: **0.066666667**
- Recall: **0.071428571**
- F1: **0.068965517**
- F2: **0.070422535**
- FPR: **0.005150215**
- FNR: **0.928571429**

### Security

- threshold: **0.17**
- TP/TN/FP/FN: **3 / 8113 / 42 / 39**
- Accuracy: **0.990118336**
- Precision: **0.066666667**
- Recall: **0.071428571**
- F1: **0.068965517**
- F2: **0.070422535**
- FPR: **0.005150215**
- FNR: **0.928571429**

## Boundary

- Thursday evaluation passes: **1**
- threshold selection: **COMPLETE AND FROZEN**
- model retraining: **NO**
- optimizer steps after E2: **0**
- Friday accessed: **NO**
- Friday status: **CLOSED**

Evaluation JSON SHA256: `86160777383f5bac25c85df7df6934f4713a3100208a168a4ccee7d36b63170c`

## Next

**Stage20-1E4 — open Friday once and report frozen holdout operating points.**
