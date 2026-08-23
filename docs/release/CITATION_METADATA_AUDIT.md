# Citation Metadata Audit

Date: 2026-08-23  
File: `CITATION.cff`  
Schema target: Citation File Format 1.2.0

## Supported metadata

- Repository title: the current `README.md` title.
- Software author: J. M. Mubasshir Rahman, supported by repository history and project-authored commits.
- Repository URL: the configured GitHub origin without the transport suffix.
- Version: `pre-release`, because no release tag exists.
- License: MIT, subject to the scope exclusions in `LICENSE` and `docs/release/LICENSE_AUDIT.md`.
- Associated canonical manuscript title: *A Multi-Axis Validation Framework for Machine-Learning Intrusion Detection*.

## Intentionally absent metadata

No DOI, journal, volume, issue, pages, publication date, ORCID, release date, or release tag is asserted. A `preferred-citation` block is intentionally absent because the manuscript author list and publication metadata have not been finalized in repository-supported form. These are explicit metadata gaps, not values to infer.

## Validation requirement

Pre-release tests must parse `CITATION.cff` as YAML, verify the required CFF 1.2.0 fields and supported values, reject invented publication fields, and confirm that no preferred manuscript citation is emitted while the author-metadata gap remains open.
