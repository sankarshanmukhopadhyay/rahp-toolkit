# Track A — current implementation evidence wave

This note accompanies the machine-readable current-implementation evidence plan. It does not replace the historical Track A judgment or the WD02 source-transition reconciliation.

## Boundary

Dogwood RC-1 is a previous OpenVTC/VTI release. Its source-pinned runtime observations remain useful historical evidence and regression comparators, but they do **not** establish the behaviour of the current implementation.

For this wave, the implementation target is `OpenVTC/verifiable-trust-infrastructure@e393e38da4941202143e293b555413d8c86ef3b3`, the observed `main` revision on 2026-09-06. The latest published `vta-service` release observed is `vta-service-v0.23.4` at `d294ecb36014d00cf1262a5c732aa47870fc1566` (published 2026-09-01); current `main` is 26 commits ahead. We therefore avoid silently treating either Dogwood or that component release as the current implementation baseline.

The exact revision actually executed by the Interop Lab must be recorded in every resulting evidence package. If current `main` moves before execution, the evidence package should pin the new executed revision rather than preserve the planning pin in this note.

## Minimum wave

The current WD02 Track A residual is narrowed to `DTG-371-P02`, `DTG-371-P13`, and the implementation-facing part of `DTG-371-P04`. The evidence contract remains the existing DPIP contract: `ER-REL-DID-AB`, `ER-STATUS-AB`, `ER-TASK-AB`, and `ER-VERIFIER-AB`.

No new evidence framework is required. The Interop Lab should reuse `composed-unlinkability-v1` as orchestration/test machinery, but the observations must be attributable to the pinned OpenVTC target rather than merely to the Lab composition. The run must materially exercise relationship/binder, status/policy-discovery, Trust Task/retention, and verifier/deliberate-correlation surfaces across two distinct verifier contexts. Absence and non-execution must remain distinguishable.

Dogwood's observed identical equivalent relationship binder is retained as a regression pressure case: the current implementation should be observed rather than presumed either to preserve or to fix that behaviour.

## Evaluation

The resulting package goes to a **new pinned comparable DPIP examination**. DPIP owns evidence admission, sufficiency and privacy interpretation. RAHP then reconciles the specialist result against the current Track A propositions.

A successful workflow is not a privacy PASS. A no-join observation is not automatically GREEN. A current implementation surface that cannot be exercised or no longer exists is itself a bounded implementation/evidence finding and should be recorded rather than replaced with a synthetic equivalent.