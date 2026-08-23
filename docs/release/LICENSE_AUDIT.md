# Repository License Audit

Date: 2026-08-23  
Decision: **MIT for repository-authored source code and original documentation, with explicit scope exclusions**

This is a repository rights audit, not legal advice. It establishes a conservative license boundary for release preparation.

## Evidence inspected

- No pre-existing `LICENSE`, `COPYING`, `NOTICE`, `.gitmodules`, or vendored-license tree was present at the accepted baseline.
- Git history supports one human repository author identity, J. M. Mubasshir Rahman; the other recurring identities are project-stage or archival aliases.
- Static scans of `src/`, `scripts/`, `tests/`, configuration, environment, and root documentation found no third-party copyright header, embedded license, or statement that repository source was copied or adapted from an external codebase. Internal statements about copying figures or values refer to earlier stages of this repository.
- Runtime libraries are declared as external dependencies and are not vendored. Their own licenses continue to govern them.
- Raw CSE-CIC-IDS2018/CICIDS2017 data are not tracked. `DATASET.md` requires users to obtain data separately. The official CSE-CIC-IDS2018 page permits redistribution subject to citation and a link, but that upstream permission is independent of this repository license: <https://www.unb.ca/cic/datasets/ids-2018.html>.
- The repository tracks 730 binary or publication-artifact files across historical models, arrays, figures, tables, and archives. This audit cannot establish independent relicensing rights for every data-derived artifact.

## Compatibility assessment

No evidence conflicts with permissive release of the repository author's original source code and documentation. MIT is a standard, widely understood permissive license; the canonical text is registered as SPDX identifier `MIT`: <https://spdx.org/licenses/MIT.html>.

The MIT grant is therefore safe only with the scope below. The audit does not assert that every tracked scientific artifact is independently licensable under MIT.

## Covered material

The MIT grant covers repository-authored source code, safety-gated wrappers, tests, configuration logic, and original project documentation to the extent J. M. Mubasshir Rahman owns the applicable copyright.

## Excluded material

The MIT grant does **not** apply to:

- CSE-CIC-IDS2018, CICIDS2017, or any other external raw or processed dataset;
- third-party packages named in dependency or environment files;
- third-party code, media, or documentation if later identified;
- model checkpoints, probability arrays, reconstructed corpora, archived notebooks, and other frozen/data-derived evidence where ownership or upstream terms are not established by this audit;
- third-party marks, dataset names, or citation content.

Those materials remain under their own applicable terms. Inclusion or a path reference does not imply a license grant.

## Release recommendation

Add the scoped root `LICENSE`, retain the dataset non-redistribution guidance, and make the scope visible in `README.md`. Before depositing a Zenodo archive, review the archive file list against these exclusions and either omit restricted/uncertain artifacts or attach their independently verified terms. No DOI or release tag is created by this audit.
