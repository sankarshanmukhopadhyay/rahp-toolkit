# Materiality → evidence invalidation → reassessment audit

## Purpose

The DTG Portfolio Monitor → RAHP pipeline intentionally coalesces repeated observations into durable proposition owners. This keeps the issue queue bounded, but creates an assurance obligation: coalescing must never hide a material change that invalidates evidence or a prior conclusion.

This audit defines the control boundary that must hold before a closed durable owner may remain closed after a new material observation.

## Required control loop

1. Detect an upstream change and retain source identity/revision.
2. Classify materiality and assurance impact.
3. Route the finding to the affected durable assurance proposition.
4. Compare the new observation with the material finding identities already represented by the durable owner and its journal.
5. Classify evidence impact as one of:
   - `preserved`: the routed material finding set is already represented by the owner/journal;
   - `new-proposition`: no durable owner yet exists for the proposition;
   - `uncertain`: one or more material findings are new to an existing proposition and preservation is not established.
6. A closed durable owner receiving `uncertain` must be reopened for reassessment.
7. Every material observation must update the durable owner with the routed finding identities so the issue becomes the running assurance journal for that proposition.

## Fail-closed invariant

For a material observation against a closed durable proposition owner:

`new material finding + no evidence-backed preservation decision` → `reassessment required`

The absence of an invalidation marker is not evidence that prior evidence remains valid.

## Implemented control

The handoff now runs `tools/materiality_journal_gate.py` against the generated combined-review and DPIP event streams before publication.

The gate:

- resolves the existing durable owner by assessment key;
- extracts the actual routed finding IDs, repositories and change summaries;
- recovers finding IDs already present in the owner's original routed-findings table and prior materiality-journal entries;
- records `evidence_impact` on every routed material event;
- records a compact, machine-readable materiality journal entry containing each finding identity, repository and change summary;
- treats a previously represented finding set as `preserved`;
- treats a new finding mapped to an existing proposition as `uncertain` rather than silently covered;
- emits `retest_reason` and `reopen_closed_owner=true` when such a new finding reaches a closed owner;
- leaves the existing publisher responsible for the actual reopen/coalescing lifecycle.

The existing publisher already understands explicit retest/reopen events, so no second issue-lifecycle mechanism was introduced.

## Durable journal semantics

Issue identity remains proposition identity.

Materiality observations are journal entries on that proposition.

A journal entry retains a machine-readable finding identity in the form:

`finding=<finding-id> @ <repository>: <change-summary>`

This matters after reassessment and re-closure. A finding already journaled during an earlier reassessment remains discoverable as represented evidence and is not incorrectly treated as new again merely because it was not part of the issue's original finding table.

## Evidence-impact interpretation

`preserved` is deliberately narrow. It means the currently routed material finding IDs are already represented by the durable owner or its materiality journal.

It does **not** assert that arbitrary semantic change is safe merely because it maps to the same proposition.

A previously unseen material finding produces `uncertain`. This is the fail-closed state that requires reassessment when the owner is closed.

Future evidence-dependency work may refine this into richer states such as `strengthened`, `invalidated` or `scope-expanded`, but those richer claims require stronger source-revision/evidence-dependency comparison than the current monitor event contract exposes.

## DPIP boundary

The same gate runs over DPIP-routed materiality events. Privacy applicability and privacy conclusions remain owned by the canonical RAHP → DPIP lifecycle; the materiality gate does not infer a privacy PASS/FAIL locally.

## Regression coverage

The tranche tests that:

1. a repeated material finding is classified `preserved` and does not reopen a closed owner;
2. a new material finding mapped to a closed owner is classified `uncertain` and triggers reassessment;
3. the exact finding identity/repository/change summary is retained in the journal payload;
4. a journaled finding remains recognizable after reassessment and re-closure and therefore does not cause a reopen loop;
5. a genuinely new proposition is distinguished from reassessment of an existing proposition.

## Operational interpretation

A quiet RAHP issue queue should now mean that routed material observations are either new propositions already being handled, already represented by the durable owner's evidence journal, or have triggered reassessment where preservation could not be established.

It must not mean only that the system found an existing issue key.
