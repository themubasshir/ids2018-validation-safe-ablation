# LaTeX Migration Plan

Status: **planning only; venue template not selected**

The Markdown submission candidate remains authoritative until a venue and template are explicitly approved. Migration must be mechanical and evidence-preserving.

## Section map

| Markdown source | Eventual LaTeX target |
| --- | --- |
| Title and status | `\title{}`; omit internal status note from submitted copy |
| Abstract | `abstract` environment |
| Sections 1-8 | `\section{}` and `\subsection{}` in current order |
| Inline Pandoc citations | Venue-native `\cite{}` generated from `references.bib` |
| Tables 1-6 | `table`/`table*` plus `tabular` or venue-approved table package |
| Figures 1-6 | `figure`/`figure*`; combine only registered panel groups |
| Supplement plan | Separate supplement source with `S` numbering |
| Limitation IDs and internal status text | Preserve in source comments or audit crosswalk; remove IDs from reader-facing prose only after audit |

## Figures and tables

Use `FINAL_FIGURE_REGISTRY.csv` as the sole source for numbering, panel order, asset paths, captions, and qualifications. Do not rescale in a way that removes legible labels, and do not redraw scientific plots. Convert SVG only if the selected toolchain requires it and verify visual identity. Use `FINAL_TABLE_REGISTRY.csv` for numbering and captions; preserve native metrics, dashes, ranges, abbreviations, and the non-composite interpretation of Table 6.

## Citations and bibliography

`manuscript/references.bib` remains canonical. The migration must preserve all 27 keys and their verified metadata. Any bibliography-style transformation is presentational only. Run key-resolution, uniqueness, citation-coverage, and unused-entry checks after conversion; do not replace sources or strengthen the supported wording during style conversion.

## Supplement

Create supplement sections S1-S7 from `FINAL_SUPPLEMENT_PLAN.md`. Reference frozen repository artifacts rather than embedding the repository wholesale. Preserve supplement-only, cancelled, descriptive, conditional, low-support, and hardware-specific statuses.

## Post-migration verification

After a venue is approved, compare every candidate scientific number, claim occurrence, citation key, figure/table caption, limitation, and evidence tension against the Pass 2B final audits. Render the LaTeX output and inspect line breaks, tables, equations, vector/raster figures, references, cross-references, and supplement numbering. Venue formatting must not begin under the present authorization.
