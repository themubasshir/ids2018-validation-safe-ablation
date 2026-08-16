# Stage21-XAI2 Decision and Stage21 Closure

## Final decision

**XAI2 comparative attribution figures are not produced.**

Stage21 is closed after the frozen XAI1B Integrated Gradients quality report.

## Why

The XAI0 protocol required attribution quality to be reported without tuning
the attribution method. If quality was poor, the limitation was to be reported
and the analysis stopped rather than replacing the method, baseline, or
integration parameters.

The frozen 64-step midpoint Integrated Gradients results show the following
relative completeness errors:

| Model | True class | Q1 | Median | Q3 | Mean | Maximum |
|---|---|---:|---:|---:|---:|---:|
| CNN | BENIGN | 0.136046 | 0.322617 | 0.745902 | 1.76538 | 122.84 |
| CNN | ATTACK | 0.0563507 | 0.142136 | 0.387983 | 0.335477 | 2.75794 |
| ViT | BENIGN | 0.00496837 | 0.0227182 | 0.0667427 | 1.15639 | 279.999 |
| ViT | ATTACK | 0.000249987 | 0.00118961 | 0.00436815 | 0.0128302 | 0.670116 |

No numeric accept/reject threshold had been preregistered, so none is introduced
after observing these results.

The decision is instead deliberately conservative: the CNN numerical
completeness residuals are sufficiently large and asymmetric relative to the
ViT that polished CNN-versus-ViT spatial attribution figures could imply
stronger cross-model attribution comparability than the quality diagnostics
support.

## What remains valid

The XAI1B execution itself is valid and remains durably preserved.

- frozen cohort: **512 Friday flows**
- method: **Integrated Gradients**
- integration: **64-step midpoint Riemann**
- baseline: **all-zero normalized image**
- padded-pixel attribution leakage: **none in the frozen reported results**
- endpoint reproduction: **PASS for CNN and ViT**
- all XAI1B arrays and summaries remain durable audit artifacts

The numerical attribution arrays are retained for transparency, but spatial
differences are not promoted into comparative figure evidence.

## What was not done

- additional IG steps: **NO**
- alternate attribution method: **NO**
- alternate baseline: **NO**
- method selection from the result: **NO**
- cohort change: **NO**
- architecture change: **NO**
- threshold search or reselection: **NO**
- retraining: **NO**
- optimizer steps: **0**
- causal claim: **NO**
- independent-confirmation claim: **NO**
- general ViT-superiority claim: **NO**

## Stage21 final status

**COMPLETE — architecture result frozen; post-result explainability reported
with a numerical-completeness limitation.**

The next preregistered research phase is **Stage22 — temporal/session-safe
flagship rerun**.
