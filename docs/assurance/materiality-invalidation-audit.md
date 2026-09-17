# Materiality → evidence invalidation → reassessment audit

## Purpose

The DTG Portfolio Monitor → RAHP pipeline intentionally coalesces repeated observations into durable proposition owners. This keeps the issue queue bounded, but creates an assurance obligation: coalescing must never hide a material change that invalidates evidence or a prior conclusion.

This audit defines the control boundary that must hold before a closed durable owner may remain closed after a new material observation.

## Required control loop

1. Detect an upstream change and retain source identity/revision.
2. Classify materiality and assurance impact.
3. Route the finding to the affected durable assurance proposition.
4. Compare the new observation with the evidence/baseline supporting the latest disposition of that proposition.
5. Classify evidence impact as one of:
   - `preserved`: evidence remains applicable and the conclusion is not invalidated;
   - `strengthened`: new evidence supports the proposition without invalidating the previous basis;
   - `invalidated`: one or more relied-upon evidence claims are no longer valid;
   - `scope-expanded`: the change creates behaviour outside the assessed boundary;
   - `uncertain`: available evidence is insufficient to prove preservation.
6. Reassessment is mandatory for `invalidated`, `scope-expanded`, and `uncertain` when the affected proposition is consequential.
7. A closed durable owner may remain closed only when preservation/strengthening is evidenced. A new material observation must not be silently coalesced merely because proposition identity is stable.

## Fail-closed invariant

For a material observation against a closed durable proposition owner:

`no explicit evidence-preservation decision` → `retest/invalidation required`

The absence of an invalidation marker is not evidence that prior evidence remains valid.

## Audit questions

- Does routing retain enough source revision/change identity to compare epochs?
- Is proposition identity distinct from observation identity?
- Is the evidence/baseline used for the previous disposition addressable?
- Can the controller determine that a new observation changes an evidence dependency?
- Can it emit an explicit invalidation/retest trigger?
- Does issue publication reopen a closed owner on that trigger?
- Are privacy conclusions invalidated through the RAHP → DPIP lifecycle rather than locally inferred?
- Is an `uncertain` comparison retained as an assurance obligation rather than PASS/no-action?

## Current implementation audit

The current routing path correctly performs qualification, semantic normalization and disposition routing, and deliberately uses stable assessment keys for steady-state coalescing. The combined review asks whether a material change preserves, strengthens, weakens, or creates assurance propositions.

The current handoff also states that a closed owner is not reopened unless the event carries an explicit invalidation or retest trigger.

The gap is between those two controls: the portfolio routing layer does not currently establish, as a machine-enforced precondition to coalescing, whether the evidence supporting a closed durable proposition remains valid. Stable proposition identity therefore can suppress reassessment unless another component has already emitted an invalidation/retest signal.

## Required implementation tranche

### M1 — Evidence dependency identity

Define a machine-readable representation linking a durable proposition/disposition to the source revisions, evidence artifacts, composition boundary and policy/profile versions on which it depends.

### M2 — Delta comparator

For each new material observation routed to an existing proposition, compare the observation with those dependencies and produce an evidence-impact decision: `preserved`, `strengthened`, `invalidated`, `scope-expanded`, or `uncertain`.

### M3 — Reassessment trigger

Translate `invalidated`, `scope-expanded`, and consequential `uncertain` outcomes into an explicit invalidation/retest trigger understood by the issue publisher/controller. Closed owners must reopen or a fresh lineage-scoped reassessment owner must be created according to the proposition lifecycle contract.

### M4 — DPIP propagation

Where an invalidated dependency underpins a privacy conclusion, issue the canonical RAHP → DPIP referral/reassessment event and retain the returned DPIP disposition before reconciliation.

### M5 — Regression tests

At minimum cover:

1. same finding / same evidence → idempotent coalescing;
2. new finding / same proposition / evidence demonstrably preserved → closed owner stays closed;
3. new finding / same proposition / evidence invalidated → reassessment;
4. new finding expands assessed scope → reassessment;
5. material change with insufficient comparison evidence → `uncertain`, not silent coalescing;
6. privacy evidence invalidation → DPIP lifecycle invoked;
7. non-material changes remain bounded/no-action where policy permits.

## Acceptance criteria

- Every material observation routed to an existing closed proposition receives an explicit evidence-impact decision.
- `invalidated`, `scope-expanded`, and consequential `uncertain` cannot terminate as silent coalescing.
- Preservation is evidence-backed rather than inferred from stable proposition identity.
- Reassessment provenance links the new observation, prior disposition, invalidated/preserved evidence, and resulting conclusion.
- Existing idempotency is retained for genuinely unchanged evidence.
- Tests demonstrate both non-churn and fail-closed reassessment behaviour.

## Operational interpretation

A quiet RAHP issue queue should mean that observed portfolio changes were either non-material, already covered by still-valid evidence, or explicitly dispositioned. It must not mean only that the system found an existing issue key.