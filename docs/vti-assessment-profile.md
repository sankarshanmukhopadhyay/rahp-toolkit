---
layout: default
title: "VTI composition assessment profile"
parent: Reference
nav_order: 4
has_toc: true
---
# VTI composition assessment profile

RAHP now treats the DTG Verifiable Trust Infrastructure (VTI) specification as an active upstream specification rather than a future consumer of pre-specification evidence.

The historical reasoning remains preserved in [Discussion #194](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/194), the completed [VTI composition evidence register #192](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/192), and the [pre-specification evidence pack](vti-pre-specification-evidence-pack.html). Those artifacts explain why composition-level assurance was needed before VTI had a normative home. They are provenance and should not be rewritten as though the VTI requirements already existed when the evidence was produced.

## Current operating boundary

RAHP is an **independent assessment programme** for VTI composition properties.

It may produce evidence that a pinned VTI property is:

- `supported` within the assessed scope and conditions;
- `refuted` by an observed or executable counterexample; or
- `indeterminate` because evidence is missing, stale, contradictory, unavailable, or insufficient.

RAHP does **not** make VTI requirements normative and does **not** decide VTI conformance. The upstream VTI specification and its governance remain authoritative for normative semantics and conformance.

## Pinned upstream baseline

The initial profile is pinned to:

| Field | Value |
|---|---|
| Repository | `trustoverip/dtgwg-vti-spec` |
| Document Status | Working Draft 0.1.0 |
| Commit | `75391a27a5d9a1794266b2e3bdeb8be68fa4db40` |
| RAHP profile | `rahp-vti-composition-assessment/v1` |

The pin is deliberate. A later VTI Working Draft does not silently inherit an assessment produced against this revision.

## Assessment contract

The authoritative machine-readable contract is [`schemas/vti-assessment.schema.json`](../schemas/vti-assessment.schema.json).

A submission records the VTI source pin, assessor programme, date, bounded scope, one of the three dispositions, method, VTI requirement identifiers, tested proposition, evidence references, legitimate counter-cases, residual uncertainty, and reassessment state/triggers.

The profile is [`profiles/dtg/vti-assessment-profile.yaml`](../profiles/dtg/vti-assessment-profile.yaml).

### Non-inference rules

The profile deliberately preserves these boundaries:

- missing evidence is not support;
- component conformance is not composition assurance;
- valid evidence is not necessarily complete evidence;
- multiplicity is not independence;
- protocol completion is not necessarily trust-outcome completion;
- cryptographic verification is not necessarily current authority;
- discovery is not recognition or authorization.

## Assessment submissions

[`RAHP-VTI-FI-001`](../examples/cross-spec/vti-assessment/false-independence.yaml) is the first complete VTI composition assessment submission.

It maps the completed false-independence corpus `SR-XSP-FI-001` through `SR-XSP-FI-007` to `VTI-CMP-070` through `VTI-CMP-074`.

The assessment disposition is `supported`: the existing executable corpus supports the non-inference property within its pinned scope. This does not assert a universal proof of independence and does not convert RAHP into a conformance authority.

Legitimate plurality, pairwise/contextual identifiers, privacy-preserving pseudonymity, genuinely independent issuers, and selective disclosure remain preserved counter-boundaries.

[`RAHP-VTI-SC-001`](../examples/cross-spec/vti-assessment/semantic-completion.yaml) is the second complete submission. It maps the existing semantic-completion evidence from issue #185 to `VTI-CMP-020` and `VTI-CMP-021`, preserving the distinction between technical exchange completion and establishment of the intended trust outcome. Its vectors deliberately include `COMPLETE / SATISFIED`, `COMPLETE / FAILED`, and `COMPLETE / INDETERMINATE` outcomes.

The generated [VTI assessment index](vti-assessment-index.html) is the human-readable inventory of complete submissions and remaining evidence-family states.

[`RAHP-VTI-AUTH-001`](../examples/cross-spec/vti-assessment/authority-continuity.yaml) is the third complete submission. It reconciles the existing constrained-authority evidence against `VTI-CMP-030` through `VTI-CMP-032`, preserving the separation between proof/credential validity and transaction-time authority and authorisation.

[`RAHP-VTI-LIFE-001`](../examples/cross-spec/vti-assessment/lifecycle-freshness.yaml) is the fourth complete submission. It adds executable freshness-bound evidence for `VTI-CMP-040` through `VTI-CMP-042`: historical evidence is not current state, currency is time-bounded, and stale or unavailable currency remains `INDETERMINATE` rather than inheriting the last-known state.

[`RAHP-VTI-DEL-001`](../examples/cross-spec/vti-assessment/delegation-lineage.yaml) is the fifth complete submission. It reconciles scope, lineage, expiry, revocation, re-delegation and action-time delegator authority with explicit acting-delegate identity propagation for `VTI-CMP-050` through `VTI-CMP-053`.

## Reassessment and invalidation

An assessment must be reconsidered when any materially relevant input changes. The current profile enumerates VTI revision change, assessed component/version change, relying policy or profile change, material configuration change, evidence supersession, and evidence contradiction.

A stale or superseded assessment must not be silently reused as current evidence.

## Requirement/evidence map

The profile provides the initial map for semantic completion, authority continuity, lifecycle/freshness, delegation lineage, privacy across composition, false independence, failure/indeterminacy, configuration materiality, component substitution, and human control.

Families are promoted to `verified` only when a complete assessment submission and its cited evidence satisfy the source-pinned requirement mapping. Unassessed families remain `partially_verified`, `specialist_evidence_required`, or `evidence_required` until their evidence is reconciled against the exact upstream requirements.

This preserves the evidence-first rule: **do not manufacture a PASS because a requirement exists.**

## Validation

Run:

    python3 tools/validate_vti_assessment_profile.py

The validator discovers every assessment submission and checks the upstream source pin, disposition vocabulary, known assessment family, exact family-to-requirement mapping, schema validity, assessment-ID uniqueness, evidence-ID uniqueness and existence, legitimate counter-cases, residual uncertainty, and negative fixtures showing that missing evidence or an unsafe `pass` disposition cannot validate.

Run `python3 tools/render_vti_assessment_index.py --check` to verify that the human-readable index is mechanically synchronized with the authoritative submissions and profile. Both checks are integrated into the repository's central validation workflow.

## Next evidence families

With false independence, semantic completion, authority continuity, lifecycle/freshness, and delegation lineage now flowing through the same assessment contract, subsequent work should progress family-by-family: human control; failure/indeterminacy; configuration materiality; privacy composition with DPIP where specialist depth is required; and component substitution once concrete implementation evidence exists.

Each family should reuse the same assessment contract rather than inventing a new output shape.
