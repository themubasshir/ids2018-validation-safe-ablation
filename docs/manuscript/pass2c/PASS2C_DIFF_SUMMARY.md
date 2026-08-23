# Pass 2C Diff Summary

Comparison:

- immutable baseline: `manuscript/manuscript_submission_candidate.md`;
- reviewer-polished candidate: `manuscript/manuscript_submission_candidate_pass2c.md`.

Mechanical diff at final prose state: **56 insertions, 69 deletions**. Whitespace-delimited length changed from **7,523** to **7,177** words. The change is editorial compression and structural distillation, not scientific deletion.

## Meaningful change classes

### TITLE

Replaced the Pass 2B title with **A Multi-Axis Validation Framework for Machine-Learning Intrusion Detection**. The new title is more direct and keeps the empirical scope limited to machine-learning systems.

### ABSTRACT

Reordered the abstract around the validation problem, framework, five-realization temporal contrast, processed reference contrast, directional transfer, operational tension, and bounded thesis. The abstract changed from 222 to 201 words. Registered values and meanings are unchanged; six-decimal cross-dataset display was retained because shorter rounding is not registered.

### CONTRIBUTION

Consolidated six overlapping contribution statements into four: framework, claim-to-provenance traceability, heterogeneous empirical findings, and the practical checklist. The contribution audit maps every former item to the new structure with no substantive loss.

### FRAMEWORK_CHECKLIST

Replaced dense Discussion 6.6 prose with eight numbered checks. Each check identifies its native evidence or metric, required control, and qualification, and resolves through `VALIDATION_CHECKLIST_TRACEABILITY.csv`.

### LIMITATION_PRESENTATION

Compressed 18 bullet-level limitations into six conceptual main-text groups. All 18 IDs and claim ceilings remain explicit, and readers are directed to the complete matrix in the supplementary/repository materials.

### READABILITY

Split dense Discussion and Conclusion sentences, reduced subordinate clauses and multi-item semicolon chains, replaced project-specific labels where conventional methodological names were clearer, and preserved immediate scope qualifications.

### INTERNAL_METADATA_REMOVAL

Removed the manuscript-status block, Pass-development statements, and reviewer-facing internal Stage/Pass labels. Scientific methods, values, and provenance boundaries remain.

## Prohibited change classes

| Change class | Count | Verification |
| --- | ---: | --- |
| `SCIENTIFIC_RESULT_CHANGE` | 0 | Final number audit maps every scientific occurrence to a frozen registered value. |
| `NEW_CLAIM` | 0 | Final claim audit uses only governed claim IDs and bounded checklist traceability. |
| `NEW_EVIDENCE` | 0 | No evidence row, figure source, table source, dataset, or artifact was added. |
| `NEW_ANALYSIS` | 0 | No computation, artifact deserialization, target access, or empirical procedure occurred. |

The Pass 2B candidate remains present and unchanged.
