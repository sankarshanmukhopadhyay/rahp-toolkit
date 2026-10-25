---
layout: default
title: "DTG ZKP corpus authority rebaseline"
parent: "Scenario corpora"
has_toc: true
nav_exclude: true
---
# DTG ZKP corpus authority rebaseline

**Tracker:** [#1145](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1145).  
**Authority decision:** [#782](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/782).

## Decision

The maintained standalone ZKP corpus now uses
`trustoverip/dtgwg-zkp-spec` as its specification and conformance authority.

The immutable baseline for this correction is:

`cfd94063e5cfee7ba6df4dcfd28c10399a0ffd0a`

That revision was already reviewed in #782 as part of the 2026-09-24 DTG
current-authority rebaseline. This tranche deliberately reuses that reviewed pin rather
than advancing to a newer upstream HEAD without another semantic review.

The authority split established by #782 remains:

| Surface | Repository | Role |
|---|---|---|
| ZKP specification and conformance | `trustoverip/dtgwg-zkp-spec` | Current normative/conformance authority used for maintained RAHP conclusions |
| ZKP task force | `trustoverip/dtgwg-zkp-tf` | Requirements, discussion, requests and informative guide lineage |
| Historical downstream adapter | `sankarshanmukhopadhyay/dtgwg-zkp-tf` | Origin of the legacy standalone UC-* scenario collection; not current specification authority |

## What changed

`CORPUS-DTG-ZKP` no longer describes the downstream fork or an unverified
`archive-snapshot` as its current source authority. The corpus and source registry now
identify the reviewed upstream specification pin directly.

The 30 existing `UC-001` through `UC-030` scenarios are retained to avoid silently
rewriting scenario history. Their identifiers originated in the historical adapter.
They must not be represented as normative identifiers owned by
`trustoverip/dtgwg-zkp-spec`.

## What this does not establish

This authority correction is **not** a scenario-by-scenario semantic requalification.

In particular it does not establish that:

- every legacy UC-* scenario remains complete against the current specification;
- every scenario title, goal, predicate or pressure maps to a current normative clause;
- the standalone corpus qualifies for `evidence_grade: source-pinned`;
- historical findings against the task-force repository can be re-attributed to the
  current specification repository; or
- a newer upstream ZKP revision than the #782 baseline has been assessed.

Issue #1147 has now completed that scenario-by-scenario review. The corpus remains without an explicit `evidence_grade`, but now carries
`provenance_status: semantic-requalification-complete-mixed-grounding` because eight of the 30 retained scenarios remain scenario-baseline hypotheses rather than source-grounded current ZKP claims.

## Validation invariant

The scenario-corpus validator now checks two relevant invariants for ordinary
(non-derived) corpora:

1. when `corpora/sources.yaml` declares an `authority_pin`, the corpus
   `source_commit` must match it;
2. an explicit evidence grade is rejected while
   `authoritative-source-pinned-scenario-review-pending` is active.

Focused regression tests cover the matching-pin case, mismatched-pin rejection and
premature-grade rejection.

## Semantic requalification outcome

That next evidence step is now complete in #1147. The 30-scenario review produced 13 retained, 9 revised and 8 scenario-baseline dispositions. See [DTG ZKP legacy-scenario semantic requalification](dtg-zkp-scenario-requalification.md).

The result is intentionally **mixed grounding**. The review therefore does not promote the corpus to `source-pinned`; any future corpus-wide grade would require either a grade definition compatible with mixed grounding or a corpus restructuring that separates source-grounded scenarios from historical hypotheses.
