---
layout: default
title: "VTI continuous convergence"
parent: Reference
nav_order: 11
---

# VTI continuous convergence

RAHP treats movement in the upstream VTI specification as an explicit
reconciliation event, not as permission to rewrite historical assessment pins.

The active v2.4.0 VTI assessment remains historically pinned to
`75391a27a5d9a1794266b2e3bdeb8be68fa4db40`. The affected Working Draft 0.2.0
propositions are now reconciled, so the convergence event is `rebaseline: ready`;
moving the active source pin remains a separate controlled change.

## Current live event

On 2026-09-23 the observed VTI head is
`3cbd7300a4f46bb2518e2b4b485609e7b5432b58` (Working Draft 0.2.0).
The earlier `c1c39b971dd535bd30bcd5c864998ebd8bf92123` observation is retained
as an intermediate point in baseline history.

The event contains three materially different drift classes:

| Upstream change | Class | RAHP consequence |
|---|---|---|
| PR #33 | normative semantic | selectively reassess semantic completion and privacy composition |
| PR #35 | evidence only | review new implementation evidence; do not stale unrelated assessment families |
| PR #36 | structural + normative assessment contract | preserve moved requirement IDs/text; review RAHP assessment-record compatibility with normative Appendix E.1 |

PR #33 adds `VTI-CMP-022`, `VTI-CMP-023`, and `VTI-CMP-064` to composition
semantics. These are not present in the active RAHP profile's requirement sets,
so semantic completion and privacy composition are the only composition families
invalidated for reassessment.

PR #36 states that requirement identifiers and requirement text are preserved
while making Appendix E.1's record form and ownership vocabulary normative.
That change therefore triggers an assessment-contract compatibility review rather
than whole-programme reassessment.

## Reconciled Working Draft 0.2.0 impacts

The two selectively affected families are terminal for this convergence epoch:

- `VTI-CMP-022/023` are **verified** by source-pinned completion
  non-inference vectors. Credential validity and exact citation binding cannot
  establish Trust Task completion without matching outcome evidence.
- `VTI-CMP-064` is **indeterminate**, not failed or supported. DPIP #271
  terminates the current specialist epoch as evidence-required and Interop Lab
  #233 records the target initiating-document + digest path as not implemented.
  This reconciles the requirement truthfully without promoting missing runtime
  evidence to privacy support.

Credential Spec #58, future ZKP opening/blinding construction, and a future
target implementation remain reassessment triggers rather than blockers to this
convergence epoch.

## Durable machinery

- `data/vti-baseline-history.yaml` records observed pins without rewriting them.
- `data/vti-convergence-events/75391a27-to-3cbd7300.yaml` is the current impact manifest.
- `tools/vti_convergence.py` validates selective impact and controlled-rebaseline rules.
- CI runs the convergence validator on every change.

The validator deliberately fails if evidence-only drift is used to stale
composition families or if a rebaseline is declared while impacted evidence or a
required contract review remains unresolved.

## Rebaseline rule

A new upstream head can be observed and classified without becoming the active
assessment baseline.

Controlled rebaseline requires:

1. every impacted family to have a truthful reconciled evidence state;
2. normative assessment-record compatibility to be resolved;
3. the convergence event to declare rebaseline ready;
4. a separate change to the active source pin and history.

Historical assessments remain immutable. A rebaseline creates a new assessment
epoch; it does not retroactively reinterpret v2.4.0 evidence.

## Negative-fixture rerun integration

Impacted families carry explicit `negative_fixture_ids` in the convergence
event. These identifiers reference the canonical reusable negative-fixture
registry under `fixtures/negative/`; VTI does not define a second fixture
schema.

For the current event:

| Impacted family | Changed requirements | Required falsification guard |
|---|---|---|
| semantic completion | `VTI-CMP-022`, `VTI-CMP-023` | `NF-VTI-VALIDITY-NOT-COMPLETION` |
| privacy composition | `VTI-CMP-064` | `NF-VTI-OUTCOME-EVIDENCE-CORRELATOR` |

The first guard wraps the existing semantic-completion evidence owner and proves
that a valid credential cannot establish completion of its cited Trust Task
exchange without the required outcome evidence.

The second wraps the existing privacy-composition specialist evidence owner and
keeps DPIP's boundary explicit: outcome evidence may introduce durable
correlators, but the privacy specialist does not decide semantic completion,
authorization, or authority.

`tools/vti_convergence.py` validates fixture references against the canonical
fixture IDs and fails closed on missing or unknown references. Only fixtures
declared by impacted families are selected for rerun. Unaffected VTI families
and unrelated RAHP/security/DRARM fixtures do not become stale merely because
the source pin moved.

When a future VTI change affects a proposition:

1. classify the changed requirement and impacted family;
2. identify an existing authoritative negative-fixture contract where one
   exists;
3. add its stable ID to that family impact;
4. create a new wrapper fixture only when no current contract represents the
   unsafe inference, and point it at the existing authoritative evidence owner;
5. keep the active VTI baseline unchanged until both positive evidence and the
   required falsification guards have been reconciled.

For the current event those conditions are satisfied. The event therefore
records the controlled rebaseline as **ready** while retaining
`baseline_mutated: false`.
