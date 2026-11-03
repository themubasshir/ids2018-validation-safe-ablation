# Phase 9C.2 numeric closure report

## Coverage

- Numeric-bearing rows retained: 207.
- Original Phase 9C.1 scientific classification: 128.
- Classification corrections: 61 rows reclassified as non-result identifiers, section/exhibit numbers, citation metadata, headings, or non-result counts.
- Corrected scientific numerical rows: 67.
- Corrected scientific rows with final verification status: 67/67.
- Original row IDs and manuscript locators preserved.

## Final status counts

| Status | Scientific rows |
|---|---:|
| `VERIFIED_SOURCE_FIELD` | 14 |
| `VERIFIED_ORIGINAL_REPORT` | 50 |
| `VERIFIED_PROTOCOL` | 3 |
| `VERIFIED_STAGE29_ONLY` | 0 |
| `SOURCE_UNAVAILABLE` | 0 |
| `SOURCE_CONFLICT` | 0 |
| `VALUE_MISMATCH` | 0 |
| `NOT_YET_VERIFIED` | 0 |

All 61 corrected non-result rows are marked `NOT_APPLICABLE_TO_STAGE29`; they remain in the audit and ledger. No denominator was removed.

## Important source checks

- Stage24 paired bridge contrasts were checked against `stage24_6_final_synthesis.json`. N9C-157--N9C-160 do not correspond to NUM29-096/097; their E29-026 report mappings are retained without fabricated NUM29 IDs.
- Stage26 supplement warm-inference rows were checked against `T26_CPU_WARM_INFERENCE.csv`; these are not CPU/GPU ratios NUM29-111--116.
- Stage27 supplement LOAO rows were checked against `stage27_final_primary_metrics.csv`; unregistered scalar cells retain original report verification without invented NUM29 IDs.
- Stage28 mean/SD values were checked against `stage28_final_stage22_shared_holdout_five_seed_summary.csv`; median/minimum/maximum values remain source-located where not registered as NUM29 entries.
- Stage23 placebo population counts were checked against the frozen source table; no NUM29 IDs were invented.

## Decision

Scientific numerical verification is closed for the corrected 67 scientific rows, with verification level disclosed. The result supports `SCIENTIFIC_PROVENANCE_PASS` for numerical provenance only. This does not constitute final manuscript approval or submission readiness.
