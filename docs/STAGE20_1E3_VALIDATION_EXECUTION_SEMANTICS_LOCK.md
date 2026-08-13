# Stage20-1E3-PRE — Thursday Validation Execution Semantics Lock

**FROZEN BEFORE THURSDAY MODEL INFERENCE**

Parent: `134db5ed954ff0307e0db5a97c60abfa1f2f76b0`

- fixed epoch-10 model
- Thursday only
- batch size: **256**
- `model.eval()` + `torch.inference_mode()`
- persisted probability: **float32 sigmoid(logit)**
- prediction: **ATTACK iff probability >= threshold**
- grid: **0.05..0.95 by 0.01**
- standard: **0.50**
- ROC_AUC: grouped distinct-score trapezoid
- PR_AUC: grouped distinct-score non-interpolated Average Precision
- balanced: max F1, then lower FPR, higher recall, closer 0.50, lower threshold
- security: exact FPR <= 0.05, max F2, then lower FPR, higher recall, lower threshold
- no relaxation
- Thursday probabilities observed before this freeze: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**

JSON SHA256: `1cde2759aa0e99c1c399c16a2ee01cbdc732b07c930d0ecf9d83a98699694120`
