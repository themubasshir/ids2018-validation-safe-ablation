# Stage20-1E4 — Final Friday Holdout Evaluation

**FINAL HOLDOUT EVALUATION COMPLETE WITH MODEL AND THRESHOLDS FROZEN BEFORE FRIDAY ACCESS**

Original pre-execution lock: `df6a13158651c2b5e7d1f69b7341ac15af01394e`

Colab execution amendment: `b70ef87fddafae4803531a617d2e074cac988ad5`

XET interruption recovery lock: `1c15d614e2f79f9bb209cc607f93c0da5249be64`

Authenticated XET fixed-4 transport lock: `035f5972bea9fdd65efeeb6d2e2ba0251bbe6732`

Friday supervised exact-match flows: **12088**

Probability SHA256: `e46a112e1e0320f645ec9d9502f0b3c0d8bdcf3987b50b2cd2352ef7484e2124`

## Score metrics

- ROC_AUC: **0.439214008**
- PR_AUC: **0.489452695**

## Standard — frozen threshold 0.50

- TP/TN/FP/FN: **183 / 6456 / 30 / 5419**
- Accuracy: **0.549222369**
- Precision: **0.859154930**
- Recall: **0.032666905**
- F1: **0.062940671**
- F2: **0.040449140**
- FPR: **0.004625347**
- FNR: **0.967333095**

## Balanced — Thursday-frozen threshold 0.17

- TP/TN/FP/FN: **183 / 6444 / 42 / 5419**
- Accuracy: **0.548229649**
- Precision: **0.813333333**
- Recall: **0.032666905**
- F1: **0.062811052**
- F2: **0.040427694**
- FPR: **0.006475486**
- FNR: **0.967333095**

## Security — Thursday-frozen threshold 0.17

Identical to balanced because both operating points were frozen at the same threshold before Friday access.

## Protocol integrity

- Friday PCAP reconstruction passes: **1**
- Friday CNN inference passes: **1**
- Friday threshold search: **NO**
- Friday threshold reselection: **NO**
- model retraining: **NO**
- optimizer steps after E2: **0**
- architecture change: **NO**
- representation change: **NO**
- join change: **NO**

Evaluation JSON SHA256: `39693543a1cf139d144742c43593c78b6cb9e9ca0123b8390dbd6781cb92363d`
