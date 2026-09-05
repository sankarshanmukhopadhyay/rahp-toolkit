# Track A WD02 source-transition reconciliation

This companion records the bounded reassessment triggered when DTG Credentials PR #30 moved from a source-pinned proposal to the merged upstream `main` baseline.

The historical Track A artifact is intentionally unchanged. It remains evidence about PR #30 at `b3840f430f5bd01addab95881350a7f860e763e2`. The new reconciliation artifact records the adopted source at merge commit `c8ef706b4d407a3a68a26b5fe2ce554c43674683` and determines which proposition conclusions survive, change, or still require evidence.

## Result

`DTG-371-P01` and `P03` are confirmed and may treat the merged correlation-scope semantics as adopted upstream authority. `P02` and `P04` are confirmed but retain runtime/privacy and implementation evidence obligations. `P05` changes materially: declaration carriage is no longer the original open credential-vs-DID-document choice; the adopted direction is credential carriage, so the residual moves to profile/implementation consequences. `P13` remains a RAHP/DPIP composition proposition requiring fresh runtime A/B evidence. `P10`, `P12`, and `P14` are not made authoritative by the PR #30 merge and do not justify a broad rerun.

The privacy disposition therefore remains **INDETERMINATE / AMBER**. Stronger specification authority is not equivalent to stronger runtime privacy evidence.

Upstream issue #38 is tracked as a residual concerning enumerable digest-valued binders. RAHP records the dependency but does not invent its normative solution.

## Repository boundary

Upstream `trustoverip/*` repositories are read-only evidence/dependency sources for this work. All commits, tests, evidence and documentation produced by this reconciliation are confined to repositories owned by `sankarshanmukhopadhyay`.

## Next boundary

Do not promote VDC/VAC-derived propositions or rerun the complete actuation composition solely because PR #30 merged. The next source-transition tranche begins when PR #19 (VDC) is merged/disposed, followed by PR #29 (VAC).
