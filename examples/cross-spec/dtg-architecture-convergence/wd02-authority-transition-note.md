# WD02 source authority transition note

The canonical proposition matrix is historical/source-pinned evidence and is not rewritten in place when an upstream proposal is adopted. Current assurance consumers should apply `source-authority-overrides.yaml` together with the relevant reconciliation artifact.

For the 2026-09-06 Track A transition, only merged PR #30 semantics are promoted to adopted upstream authority. PR #19 (VDC) and PR #29 (VAC) remain proposed upstream. RAHP-inferred composition propositions retain their existing authority class.

This additive convention prevents experimental implementation success or later source movement from laundering historical evidence into a stronger authority claim.
