# Stage24 Final Freeze

## Cross-Dataset Generalization & Artifact-Sensitivity Audit

**Status:** COMPLETE

**Directions are reported separately and are not averaged.**

---

## 1. Governance

- Scientific fits completed: **4 / 4**
- Additional fits authorized: **0**
- Evaluable target openings completed: **6 / 6**
- Original target-opening budget: **8**
- GROUNDED_S4 cells cancelled before opening: **2**
- Cancelled openings reallocated: **No**
- Remaining evaluable target cells: **0**
- Target threshold tuning: **None**
- Target calibration: **None**
- Post-opening feature/model adaptation: **None**

---

## 2. Primary Direction — IDS2018 → CICIDS2017

Target population: **2,830,743 rows**

| Cell | PR-AUC | ROC-AUC | Brier |
|---|---:|---:|---:|
| bridge62 PUBLISHED | 0.667483 | 0.733946 | 0.145756 |
| bridge62 FLAG_CORRECTED | 0.667483 | 0.733946 | 0.145756 |
| bridge70 PUBLISHED | 0.663981 | 0.741891 | 0.142912 |
| bridge70 FLAG_CORRECTED | 0.656252 | 0.744083 | 0.147998 |

bridge62 PUBLISHED and FLAG_CORRECTED are bitwise identical.

### Primary paired bootstrap — 2,000 replicates, seed 42

**bridge70 PUBLISHED − bridge62 PUBLISHED**

- PR-AUC: -0.003502 [-0.003856, -0.003152]
- ROC-AUC: +0.007945 [+0.007793, +0.008096]
- Brier: -0.002844 [-0.002915, -0.002766]

**bridge70 FLAG_CORRECTED − bridge62 FLAG_CORRECTED**

- PR-AUC: -0.011230 [-0.011619, -0.010858]
- ROC-AUC: +0.010137 [+0.009981, +0.010303]
- Brier: +0.002243 [+0.002153, +0.002336]

**bridge70 FLAG_CORRECTED − bridge70 PUBLISHED**

- PR-AUC: -0.007729 [-0.007921, -0.007534]
- ROC-AUC: +0.002192 [+0.002139, +0.002246]
- Brier: +0.005087 [+0.005023, +0.005152]

### GROUNDED_S4

Not evaluated.

Reason: the frozen Stage20 exact-S4 population could not be recovered as exact physical CICIDS2017 feature-table rows from the durable compact artifact without introducing a new heuristic matching rule.

No fuzzy or inferred substitute was used.

---

## 3. Secondary Direction — CICIDS2017 → IDS2018

Target: **IDS2018 Feb-28**

Target population:

- Rows: **593,780**
- Benign: **531,524**
- Attack: **62,256**
- Attack prevalence: **0.104847**

| Cell | PR-AUC | ROC-AUC | Brier |
|---|---:|---:|---:|
| bridge62 | 0.108176 | 0.525167 | 0.105758 |
| bridge70 | 0.107419 | 0.525302 | 0.105652 |

Chance PR-AUC anchor from target prevalence: **0.104847**

### Secondary paired bootstrap — bridge70 − bridge62

- PR-AUC: -0.000757 [-0.001058, -0.000435]
- ROC-AUC: +0.000135 [-0.000900, +0.001263]
- Brier: -0.000106 [-0.000124, -0.000089]

---

## 4. Cross-Direction Result

The two transfer directions produce materially different observed generalization behavior and are therefore retained separately, as preregistered.

### IDS2018 → CICIDS2017

The full-population CICIDS2017 evaluations retain substantial ranking signal:

- bridge62 PR-AUC: **0.667483**
- bridge62 ROC-AUC: **0.733946**
- bridge70 PUBLISHED PR-AUC: **0.663981**
- bridge70 PUBLISHED ROC-AUC: **0.741891**

The aggregate-flag serialization correction produces measurable changes in the bridge70 target predictions and in all three frozen paired-bootstrap metrics.

### CICIDS2017 → IDS2018

The reverse transfer is close to the IDS2018 Feb-28 prevalence/chance anchor:

- chance PR-AUC anchor: **0.104847**
- bridge62 PR-AUC: **0.108176**
- bridge70 PR-AUC: **0.107419**
- bridge62 ROC-AUC: **0.525167**
- bridge70 ROC-AUC: **0.525302**

The source-selected operating points also transferred with extremely low attack recall, which is retained as part of the frozen result rather than repaired post hoc.

---

## 5. Final Scientific Status

Stage24 demonstrates that cross-dataset IDS generalization is strongly direction-dependent under the frozen validation-safe protocol.

The study separately exposes:

1. **dataset/domain shift,**
2. **aggregate-flag extractor/serialization sensitivity,**
3. **bridge-feature sensitivity,**
4. **source-validation threshold transfer behavior,**
5. and the limitation that exact GROUNDED_S4 physical target membership was not durably recoverable.

No target-guided correction was introduced after any target result was observed.

---

## 6. Artifact Identities

- Primary freeze SHA256: `bdb6471be8b154662149eeb616dfdfb78f978dd3f337659e773ad9a21b3ba42f`
- Primary bootstrap SHA256: `96732023e0a1c9b52a79fafa59ea4b851ef7f8bae1814e4b4b4fde0ef0df09aa`
- Secondary bridge62 probability SHA256: `4c7cc6af61b8c4813c9241d526b6a473e46e4f69a058305eceb7fb4c30621640`
- Secondary bridge70 probability SHA256: `badf2e99f7b6a2aad9687ca30a2056271d18b47f089d29093151f6331adf8c3b`
- Secondary bootstrap SHA256: `28005e0f13d86658ba81e6b19dc154b94eedb316ea5ce0348287265c00541953`
- Final synthesis JSON SHA256: `785bbcb00140f4d7e07e9b49ad33924166b5995e66a229c986d5b1abcbcaee4b`

