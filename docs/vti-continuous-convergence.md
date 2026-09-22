---
layout: default
title: "VTI continuous convergence"
parent: Reference
nav_order: 11
---

# VTI continuous convergence

RAHP treats movement in the upstream VTI specification as an explicit
reconciliation event, not as permission to rewrite historical assessment pins.

The active v2.4.0 VTI assessment remains pinned to
`75391a27a5d9a1794266b2e3bdeb8be68fa4db40` until the affected propositions
have been reconciled.

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
