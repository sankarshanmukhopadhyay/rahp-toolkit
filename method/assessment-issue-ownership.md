# Assessment issue ownership

RAHP distinguishes an **observation** from an **assurance proposition** and from the GitHub issue that owns work on that proposition.

## Ownership invariant

A new observation does not, by itself, create a new issue.

The durable ownership key is the assessment/proposition key carried in `rahp-assessment-key`. For bounded child reviews, that key should remain stable for as long as the proposition being assessed remains the same. Snapshot/controller records may remain epoch-scoped so that provenance is preserved without forcing child-review duplication.

The publisher applies the following lifecycle rules:

1. A genuinely new proposition with no existing keyed owner creates a new issue.
2. New evidence for an open proposition is coalesced into the existing open owner.
3. New evidence for a closed terminal proposition is recorded against that closed owner and does not create a replacement issue.
4. A closed proposition owner is reopened only when the event carries an explicit governed invalidation or retest trigger, such as `invalidation_reason`, `retest_reason`, or `reopen_closed_owner: true`.
5. If historic duplicate issues already exist for the same key, the earliest keyed issue is treated as the canonical durable owner. A later duplicate does not become authoritative merely because it is newer.

## What does not constitute invalidation

None of the following, by itself, is sufficient to create a new bounded review or reopen a terminal owner:

- a new repository SHA;
- a later monitor snapshot;
- repetition of the same finding identity or routing cluster;
- a workflow succeeding;
- an upstream repository changing outside the material semantic surface of the proposition.

A reassessment requires evidence that the prior proposition conclusion may no longer hold, or an explicit retest obligation defined by the relevant assurance workflow.

## Provenance

Repeated observations remain visible through trigger markers and observation appendices on the durable owner. This preserves evidence chronology while preventing GitHub issue count from becoming a proxy for monitor polling frequency.

Controller issues remain epoch-scoped where required. They may therefore be new per qualifying snapshot while their bounded child reviews coalesce into durable proposition owners.

## Regression expectation

The September 2026 `#611`–`#616` duplicate episode is the reference regression case: reprocessing the same proposition after its earlier owner was terminally closed must resolve to the earlier owner rather than creating a replacement review issue. A new issue is appropriate only when the proposition identity changes or no durable owner exists.
