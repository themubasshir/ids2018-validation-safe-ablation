# Stage27 Publication and Reproducibility Closeout

## Scientific Status

**STAGE27 = SCIENTIFICALLY CLOSED**

Stage27 completed the frozen chronology-first zero-training-exposure
attack-family generalization audit before manuscript integration began.

No publication step reopened the target, refit a model, reran inference,
reselected a threshold, recomputed bootstrap intervals, or introduced
new formal statistical testing.

## Frozen Scientific Parent

`0e1439565aedc7da9b7ca1207262e9061422bc22`

## Publication Package Commit

`9254170fccbad47134d2dc3803bca5cecb3f9ecf`

Commit subject:

`stage27-pub1: freeze manuscript integration package`

## Final Stage27 Scientific Outcome

The publication-safe Stage27 synthesis is:

1. `SELECTIVE_FAMILY_TRANSFER`
2. `RANKING_THRESHOLD_DIVERGENCE`
3. `LEARNER_DEPENDENCE`

Five of seven preregistered attack families were structurally
executable under strict chronology.

- BOT: executable
- DDOS: executable
- DOS: structurally ineligible
- AUTH_BRUTE_FORCE: structurally ineligible
- INFILTRATION: executable, descriptive only because support = 36
- PORT_SCAN: executable
- WEB_ATTACK: executable

Stage27 is an unseen attack-family generalization audit and is not
formal proof of universal zero-day detection.

## Publication Artifacts

| Artifact | SHA256 |
|---|---|
| `docs/STAGE27_MANUSCRIPT_INTEGRATION.md` | `dbce1fe919533ba271ffc3748863ed1290121428e4a242fb9b4d2252d589e83a` |
| `docs/STAGE27_MANUSCRIPT_INTEGRATION.tex` | `8b9d7a82654a1a0e7171e86714fcaf5a9d9e4d211a7e537a16e4c28d7d67f5ea` |
| `docs/STAGE27_PUBLICATION_TABLES.md` | `7d269c5bb92d3af0dcab7b8720b42296005411ab34423e92f4245e25c999dd7e` |
| `docs/STAGE27_PUBLICATION_TABLES.tex` | `eb8f6e490fbd9cc3882a2100e19770fdf955800ca97300e251f6ee90af12d444` |
| `results/stage27_loao_unseen_attack/stage27_publication_package/stage27_publication_manifest.json` | `e52b6cf97da8234c35587a41898da3fd5097f4f3ba489f045fc06c95464d8236` |
| `scripts/stage27/stage27_publication_integration.py` | `ad763a2ab7ab9ebe0705abbc5af19ad5670d57c1b3d55e8a96f1546be189ff6b` |

## Manifest

Publication manifest:

`results/stage27_loao_unseen_attack/stage27_publication_package/stage27_publication_manifest.json`

SHA256:

`e52b6cf97da8234c35587a41898da3fd5097f4f3ba489f045fc06c95464d8236`

Manifest state:

`PUBLICATION_CONTENT_FROZEN`

## Reproducible Generator

`scripts/stage27/stage27_publication_integration.py`

SHA256:

`ad763a2ab7ab9ebe0705abbc5af19ad5670d57c1b3d55e8a96f1546be189ff6b`

The generator verifies the canonical frozen Stage27 source hashes,
reconstructs the manuscript-facing tables and prose from those frozen
artifacts, and supports a read-only `--check` mode.

## Main-Manuscript Figure Policy

### Main Figure 27-1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`

Purpose:

Selective unseen-family ranking transfer and learner dependence.

### Main Figure 27-2

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

Purpose:

Ranking--threshold divergence at the frozen BALANCED operating point.

### Supplementary Figure 27-S1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains a co-primary metric and must remain in the main results
table and manuscript text even when its separate visualization is
supplementary.

## Reporting Guardrails

The manuscript must not claim:

1. formal or universal zero-day detection;
2. universal unseen-family generalization;
3. that all seven families produced executable target folds;
4. an inferential family-level INFILTRATION conclusion;
5. statistically significant behavioral-similarity correlation;
6. causal explanation from behavioral similarity;
7. universal superiority of XGBoost or LightGBM;
8. target-guided threshold optimization or model adaptation;
9. that raw PR-AUC novelty gaps are prevalence invariant.

## Final Accounting

- preregistered primary families: 7
- executable families: 5
- structurally ineligible families: 2
- descriptive-only executable families: 1
- preregistered learners: 2
- frozen Stage27 fits: 10
- new publication-phase fits: 0
- new publication-phase inference: 0
- target reopenings during publication: 0
- threshold reselections during publication: 0
- bootstrap recomputations during publication: 0
- new formal statistical tests during publication: 0

## Remote Verification

The publication package commit was pushed to `origin/main`, fetched
back from GitHub, and verified by exact commit identity and byte-level
SHA256 comparison of each publication artifact.

## Next Manuscript Phase

Stage27 publication integration is complete.

The next authorized work is whole-manuscript assembly and
claim-to-artifact consistency review across the already-frozen
experimental stages.

No further Stage27 scientific computation is authorized.
