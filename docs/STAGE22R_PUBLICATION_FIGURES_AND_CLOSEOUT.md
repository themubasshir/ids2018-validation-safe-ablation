# Stage22R Publication Figures and Closeout

Scientific result commit: `b5e44615269198426cc8a9aa3b3e701c2ca9e48e`  
Scientific result tag: `stage22r-final-single-holdout-v1`  
Publication closeout tag: `stage22r-publication-closeout-v1`

Stage22R's Mar1--Mar2 holdout has been consumed **1 / 1** and is
**PERMANENTLY CLOSED**. The figures below are post-result visualizations of
already-committed summary artifacts only.

## Figure 22R-1 — Validation-to-final PR-AUC transfer

**Files**

- `figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.png`
- `figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.pdf`

**Caption.** Development-validation and single forward Mar1--Mar2 PR-AUC for
the four precommitted Stage22R cells. Random and chronological development
validation use different memberships and prevalences, and the common final
holdout has attack prevalence 0.273150; PR-AUC
movement must therefore be interpreted with this prevalence sensitivity in
mind. The figure shows the pronounced reversal between near-perfect random
development validation and stronger final ranking by the chronological cells.

## Figure 22R-2 — Validation-to-final ROC-AUC transfer

**Files**

- `figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.png`
- `figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.pdf`

**Caption.** ROC-AUC transfer from each cell's frozen development validation
membership to the one common forward final holdout. The dashed line marks
chance ROC-AUC = 0.5. Random validation cells fall from approximately 0.999 to
0.520--0.542 on the final period, whereas chronological cells rise from
approximately 0.499--0.515 on Feb28 to 0.806--0.832 on Mar1--Mar2.

## Figure 22R-3 — Frozen operating-point behavior

**Files**

- `figures/stage22r_temporal_validation/fig22r_3_final_frozen_operating_points.png`
- `figures/stage22r_temporal_validation/fig22r_3_final_frozen_operating_points.pdf`

**Caption.** Recall versus false-positive rate on the shared K79-clean final
holdout for all 12 already-frozen cell/operating-point combinations. Both axes
use logarithmic scales, and the dashed vertical line marks a 5% FPR reference.
The chronological cells preserve useful ranking while their validation-selected
thresholds almost never fire; the random security operating points recover
some recall but exceed the validation-era 5% FPR constraint.

## Supplementary Figure 22R-S1 — Exact-K79 holdout cleaning

**Files**

- `figures/stage22r_temporal_validation/fig22r_4_k79_final_holdout_cleaning.png`
- `figures/stage22r_temporal_validation/fig22r_4_k79_final_holdout_cleaning.pdf`

**Caption.** Row exclusions applied during the single final holdout opening
under frozen exact-K79 rules. There were zero retained-development exact
overlaps, 10 mixed-label conflict rows, and 5,532 same-label duplicate rows.
The final common evaluation universe contains 1,374,133 rows.

## Scientific boundary

This publication closeout performs:

- raw Mar1/Mar2 reads: **0**
- model forwards: **0**
- training: **0**
- threshold search/reselection: **0**
- calibration: **0**
- model selection: **0**
- bootstrap/resampling: **0**
- scientific result modification: **0**

The figures and manuscript text are descriptive views of the already-frozen
Stage22R numerical artifacts. The scientific result remains anchored at
`b5e44615269198426cc8a9aa3b3e701c2ca9e48e`.
