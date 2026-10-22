# PR B: source-attribution evidence checkpoint (2026-10-22)

This tranche begins the substantive source reconciliation for [#481](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/481) and [#1074](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1074), after baseline PR #1130.

Five of 21 monitor observations have been linked to **full upstream commit SHAs** corroborated against actual upstream commit subjects. Those are `0883f0a9d45e86e0d674` (revocation host gate), `20bc88fe966b21280abf` (offer description), `fde49552f3a619512012` (KeyPackage acceptance), `93bb8641b0306b9106f3` (cross-surface acceptance), and `91cde01ddab22806125c` (normative pending-removal settlement).

Each record has a *candidate* P-ROOM proposition and an explicit `source_review_only` limit. These source matches neither reproduce upstream execution nor establish current-target assurance. The other 16 observations remain unqualified, including three release markers.

Validation accepts **only** a verified 40-hex SHA plus an exact repository commit URL and candidate proposition for an attributed source record; it requires `requires_target_retest` rather than PASS. All 21 findings must remain in the manifest, including unknowns.

**Not yet delivered:** source attribution for the other 16 identifiers; full P-ROOM materiality judgments; targeted executable cases; DPIP determination/returns; final residual transfers. This is a PR B *increment*, not completion of PR B or authority to close either parent issue.
