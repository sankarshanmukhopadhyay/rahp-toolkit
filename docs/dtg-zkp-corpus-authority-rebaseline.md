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

For those reasons the corpus remains without an explicit `evidence_grade` and carries
`provenance_status: authoritative-source-pinned-scenario-review-pending`.

## Validation invariant

The scenario-corpus validator now checks two relevant invariants for ordinary
(non-derived) corpora:

1. when `corpora/sources.yaml` declares an `authority_pin`, the corpus
   `source_commit` must match it;
2. an explicit evidence grade is rejected while
   `authoritative-source-pinned-scenario-review-pending` is active.

Focused regression tests cover the matching-pin case, mismatched-pin rejection and
premature-grade rejection.

## Next evidence step

A later semantic requalification should inspect each retained UC-* scenario against a
reviewed immutable `dtgwg-zkp-spec` revision and record, for each scenario, whether it
is retained, revised, split, retired or replaced by a specification-owned construction
or conformance proposition.

Only that review should decide whether the standalone corpus can move from **Not
declared** to an explicit evidence grade.
