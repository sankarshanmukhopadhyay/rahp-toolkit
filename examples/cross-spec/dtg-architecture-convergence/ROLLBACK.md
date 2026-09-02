# Discussion #371 rollback and reversibility policy

This directory contains the machine-readable rollback contract for the DTG architecture-convergence wave initiated by [Discussion #371](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/371).

The canonical manifest is [`rollback-manifest.yaml`](./rollback-manifest.yaml).

## What the manifest guarantees

The #371 work was intentionally developed as source-pinned experimental assurance and executable evidence rather than as an irreversible rewrite of RAHP around proposed DTG semantics. The rollback manifest records the exact pre-wave `main` baseline for RAHP Toolkit, DPIP and the Trust Protocol Interop Lab; every merged PR introduced specifically for this wave; the reverse dependency order for a full reversal; and dependency-scoped invalidation rules for a partial upstream reversal.

The preferred restoration target is **semantic pre-#371**, not a forced reset to an old repository snapshot. A reversal should remove or disable abandoned DTG assumptions while preserving unrelated later work, historical evidence and generic assurance improvements that remain valid independently of the upstream proposal.

## Why the baseline SHAs matter

The baseline SHAs are forensic anchors. They allow a temporary reconstruction branch or exact comparison with the repository shape immediately before the #371 wave began:

| Repository | Pre-wave baseline |
| --- | --- |
| `sankarshanmukhopadhyay/rahp-toolkit` | `01709444949458961ba6edf416eeb4dda63d3cba` |
| `sankarshanmukhopadhyay/dtg-privacy-implementation-profile` | `4f3a4f559c0a1dbc6deb08f9078ebdc9d28828ee` |
| `sankarshanmukhopadhyay/trust-protocol-interop-lab` | `0a43f59981c7ff7c62fc306b009511521e851ead` |

They are **not** instructions to force-reset `main`.

## Full rollback order

A complete reversal proceeds from consumers back toward the proposition foundation: Track G, then F/E/D/C/B/A, then the #372 proposition matrix. Within a track, executable Interop/DPIP artifacts are removed together with the corresponding RAHP conclusion. The exact repository/PR sequence is machine-readable in the manifest.

This order prevents a foundational proposition from disappearing while downstream experiments or active assurance conclusions still depend on it.

## Partial upstream reversal

A complete rollback is not required when upstream changes only one primitive. The manifest records representative dependency scopes for correlation scope, VDC and VAC. The operational rule is:

1. mark affected proposition evidence stale or superseded;
2. find dependent tracks from the canonical proposition matrix;
3. revert only executable or semantic-assumption artifacts that no longer correspond to current upstream semantics;
4. preserve unaffected tracks;
5. rerun remaining evidence against current immutable source pins.

This allows, for example, a rejected VDC proposal to invalidate the VDC-dependent parts of Tracks B/D/F/G without automatically discarding unrelated correlation-scope work.

## Historical evidence is not deleted

If upstream rejects or supersedes a proposal, the source-pinned RAHP result remains useful historical evidence. The preferred transition is conceptually:

```yaml
authority_status: superseded-upstream
assurance_status: historical
```

The historical assessment then answers: **what did we learn about the proposal that existed at that immutable source revision?** It must no longer be represented as assurance of current upstream semantics.

## Generic capabilities survive proposal reversal

The manifest explicitly preserves generic assurance properties learned or exercised during the wave, including component-PASS/composition-PASS separation, immutable source pinning, stale-evidence invalidation, evidence provenance, specialist routing and semantic residual ownership. These are RAHP/DPIP/Interop capabilities, not adoption of VAC, VDC, correlation scope or Data Rooms.

## Execution discipline

Any actual rollback should be a visible issue/PR wave against current `main`, with the upstream reversal source pinned, affected proposition IDs identified before editing, full repository CI run after each bounded PR, and cross-repository references reconciled before closure.

The manifest is a reversibility contract. It does **not** itself trigger or authorize a rollback.
