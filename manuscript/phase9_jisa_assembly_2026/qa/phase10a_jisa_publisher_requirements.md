# Phase 10A JISA publisher-requirements verification

## Official sources

- Guide for Authors: https://www.sciencedirect.com/journal/journal-of-information-security-and-applications/publish/guide-for-authors
- Journal page: https://www.sciencedirect.com/journal/journal-of-information-security-and-applications

Automated ScienceDirect access returned HTTP 400. Search results exposed the official Guide URL and partial indexed text, but indexed snippets are not authoritative enough to close requirements. Manual browser verification remains required.

## Verification matrix

| Requirement | Status | Action |
|---|---|---|
| Accepted article type | UNVERIFIED | Author must inspect official guide and portal. |
| Abstract length/format | UNVERIFIED | Confirm current limit and structured/unstructured rule. |
| Highlights | UNVERIFIED | Confirm required count, length, file format, and wording rules. Existing `source/highlights.txt` is a draft asset only. |
| Keywords | UNVERIFIED | Confirm count and formatting. Existing manuscript contains six keywords; do not assume acceptance. |
| LaTeX template | UNVERIFIED | Confirm current Elsevier/JISA template and class requirements. Current source uses `elsarticle-num`; do not assume final compliance. |
| Citation/reference style | UNVERIFIED | Confirm numeric style, bibliography package, and journal-specific rules. Do not reformat from third-party guidance. |
| Main/supplement packaging | UNVERIFIED | Confirm whether supplement is separate supporting information, merged source, or portal item. |
| Figures/artwork | UNVERIFIED | Confirm file formats, resolution, color, captions, permissions, and separate upload rules. |
| Declarations | UNVERIFIED | Confirm required funding, competing-interest, ethics, acknowledgments, CRediT, data/code, and AI fields. |
| Data/code availability | UNVERIFIED | Confirm statement taxonomy and repository expectations. |
| Submission portal | UNVERIFIED | Confirm Editorial Manager route and required metadata. |
| Open access/publication cost | UNVERIFIED | Confirm subscription/open-access choices, APC, and funding workflow. |
| Cover letter | UNVERIFIED | Confirm required contents and scope statement. Prepare separately. |
| Reviewer suggestions/exclusions | UNVERIFIED | Confirm portal/cover-letter fields and conflict requirements. |
| Journal scope | PARTIAL | Search-indexed official description indicates original research and practice-driven applications relevant to information security. Full scope text and exclusions require manual official-page review. |

## Manual browser checklist

1. Open the official Guide URL in a current browser.
2. Record access date, article type, abstract/keyword/highlight limits, template/class, reference style, artwork rules, declarations, data/code fields, supplement rules, portal, APC/access, cover letter, and reviewer fields.
3. Save the authoritative page or PDF locally outside Git if permitted; record URL and version/date.
4. Compare requirements with the isolated source without modifying the manuscript.
5. Obtain author approval before any public declaration or formatting change.

No third-party summary is treated as authoritative. No manuscript or canonical submission change made.
