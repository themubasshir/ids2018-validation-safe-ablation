# Journal Figure Index

| Filename | Stage | Recommended manuscript section | Proposed caption |
| --- | --- | --- | --- |
| `figures/statistical_confidence/figure_bootstrap_operating_point_intervals.png` | Stage 8 | Statistical confidence analysis | Bootstrap confidence intervals for selected operating-point metrics. |
| `figures/statistical_confidence/figure_paired_balanced_differences.png` | Stage 8 | Balanced model uncertainty | Paired bootstrap differences for XGBoost balanced versus LightGBM balanced. |
| `figures/statistical_confidence/figure_paired_security_differences.png` | Stage 8 | Security model uncertainty | Paired bootstrap differences for XGBoost security versus LightGBM security. |
| `figures/statistical_confidence/figure_auc_difference_intervals.png` | Stage 8 | Threshold-independent discrimination | Bootstrap intervals for ROC-AUC and PR-AUC differences. |
| `figures/calibration/figure_calibration_metric_intervals.png` | Stage 9 | Calibration assessment | Bootstrap intervals for calibration metrics of the selected models. |
| `figures/calibration/figure_calibration_reliability_equal_width.png` | Stage 9 | Reliability analysis | Equal-width reliability curves for XGBoost and LightGBM. |
| `figures/calibration/figure_calibration_reliability_equal_frequency.png` | Stage 9 | Reliability analysis | Equal-frequency reliability curves for XGBoost and LightGBM. |
| `figures/calibration/figure_paired_calibration_differences.png` | Stage 9 | Calibration uncertainty | Paired calibration-difference intervals. |
| `figures/operational_cost/figure_break_even_cost_ratios.png` | Stage 10 | Operational cost analysis | Break-even missed-attack to false-alert cost ratios. |
| `figures/operational_cost/figure_holdout_cost_by_ratio.png` | Stage 10 | Deployment trade-offs | Holdout operational cost across relative FN:FP cost ratios. |
| `figures/operational_cost/figure_validation_fp_fn_pareto_frontier.png` | Stage 10 | Threshold selection constraints | Validation false-positive and false-negative Pareto frontier. |
| `figures/attack_category/figure_attack_category_detection_rates.png` | Stage 11 | Attack-category analysis | Detection rates by attack category and operating point. |
| `figures/attack_category/figure_attack_category_missed_counts.png` | Stage 11 | Residual error analysis | Missed attack counts by category. |
| `figures/attack_category/figure_attack_category_paired_differences.png` | Stage 11 | Paired category testing | Paired category-level detection differences. |
| `figures/multiseed/figure_multiseed_winner_frequency.png` | Stage 12 | Robustness across seeds | Winner frequency across fixed-hyperparameter multi-seed runs. |
| `figures/multiseed/figure_multiseed_threshold_stability.png` | Stage 12 | Threshold robustness | Selected threshold stability across seeds. |
| `figures/multiseed/figure_multiseed_balanced_f1.png` | Stage 12 | Balanced objective robustness | Balanced holdout F1 across seeds. |
| `figures/multiseed/figure_multiseed_security_f2.png` | Stage 12 | Security objective robustness | Security holdout F2 across seeds. |
<!-- BEGIN STAGES 14-21 PUBLICATION ASSETS -->

## Stages 14–21 Publication Assets

The following later-stage figures were added after the original Stage 8–12
journal-extension index. Stage-local numbering is preserved here; final
manuscript numbering can be assigned during typesetting.

| Filename | Stage | Recommended manuscript section | Proposed caption |
| --- | --- | --- | --- |
| `results/stage14_integrated_gradients/publication_assets/figures/ig_cnn_global_top15_features.png` | Stage 14 | Integrated Gradients | Global CNN Integrated Gradients attribution ranking. |
| `results/stage14_integrated_gradients/publication_assets/figures/ig_mlp_global_top15_features.png` | Stage 14 | Integrated Gradients | Global MLP Integrated Gradients attribution ranking. |
| `results/stage14_integrated_gradients/publication_assets/figures/ig_reference_sensitivity_by_outcome.png` | Stage 14 | Explanation reliability | Attribution sensitivity across reference choices and outcome strata. |
| `results/stage14_integrated_gradients/publication_assets/figures/ig_reliability_classes_by_model_outcome.png` | Stage 14 | Explanation reliability | Reliability classes by neural model and prediction outcome. |
| `results/stage17_attention_explainability_checkpoint/stage17_2_attention_analysis_package/figures/stage17_2_global_rollout_top20.png` | Stage 17 | Transformer attention analysis | Global top-20 attention-rollout features. |
| `results/stage17_attention_explainability_checkpoint/stage17_2_attention_analysis_package/figures/stage17_2_cross_seed_rollout_spearman.png` | Stage 17 | Attention stability | Cross-seed attention-rollout rank agreement. |
| `results/stage17_attention_explainability_checkpoint/stage17_2_attention_analysis_package/figures/stage17_2_layer_head_entropy_heatmap.png` | Stage 17 | Attention structure | Layer/head attention entropy across the frozen Transformer ensemble. |
| `figures/stage16_classical_transformer/fig16_1_classical_vs_transformer_holdout_tradeoff.png` | Stage 16 | Cross-family benchmark | Same-holdout operating trade-off between the frozen classical ensemble and Transformer. |
| `figures/stage18_graph/fig18_1_graph_ranking_vs_frozen_operating_point.png` | Stage 18 | Graph representation | Graph ranking strength versus failure at the independently frozen operating threshold. |
| `figures/stage19_temporal/fig19_1_mtemporal_pooled_and_daily_heterogeneity.png` | Stage 19 | Temporal modeling | Pooled MTemporal benefit and day-specific chronological heterogeneity. |
| `figures/stage21_architecture/fig21_1_cnn_vit_ranking_comparison.png` | Stage 21 | Packet-image architecture ablation | CNN-versus-ViT ranking performance on validation and the locked Friday reuse benchmark. |
| `figures/stage21_architecture/fig21_2_paired_bootstrap_auc_deltas.png` | Stage 21 | Architecture uncertainty | Frozen paired-bootstrap ViT-minus-CNN ranking-metric deltas. |
| `figures/stage21_architecture/fig21_3_friday_frozen_operating_points.png` | Stage 21 | Operating behavior | Friday behavior at the standard and validation-selected frozen operating points. |
| `figures/stage21_architecture/fig21_4_ig_completeness_quality.png` | Stage 21 | Post-result XAI quality | Numerical-completeness diagnostic for the frozen Integrated Gradients analysis. |

### Deliberate non-duplication

Stage 15 does not receive a separate new performance figure here because its
frozen Transformer is compared directly against the classical strategy on the
same duplicate-safe holdout in the Stage 16 figure.

Stage 20 does not receive a duplicate performance figure because its frozen CNN
packet-image comparator is already shown directly in the Stage 21 architecture
figures.

The Stage 18 ViT feasibility decision applied to the then-available tabular
representations. Stage 20 subsequently constructed an authentic packet-image
representation, which enabled the separate Stage 21 CNN-versus-ViT experiment.

<!-- END STAGES 14-21 PUBLICATION ASSETS -->

<!-- BEGIN STAGE22R PUBLICATION ASSETS -->

## Stage22R Publication Assets

| Filename | Stage | Recommended manuscript section | Proposed caption |
| --- | --- | --- | --- |
| `figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.png` | Stage22R | Temporal validation / ranking transfer | PR-AUC transfer from each frozen development-validation cell to the common forward Mar1--Mar2 holdout; validation prevalence differs by split regime. |
| `figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.png` | Stage22R | Temporal validation / ranking transfer | ROC-AUC transfer from development validation to the common forward holdout, with chance ROC-AUC shown for reference. |
| `figures/stage22r_temporal_validation/fig22r_3_final_frozen_operating_points.png` | Stage22R | Deployment-threshold transfer | Recall-versus-FPR behavior of all 12 frozen cell/operating-point combinations on the shared final holdout. |
| `figures/stage22r_temporal_validation/fig22r_4_k79_final_holdout_cleaning.png` | Stage22R | Supplementary / reproducibility | Exact-K79 final-holdout exclusions and resulting common evaluation universe. |

Vector PDF versions are committed beside each PNG.

<!-- END STAGE22R PUBLICATION ASSETS -->
