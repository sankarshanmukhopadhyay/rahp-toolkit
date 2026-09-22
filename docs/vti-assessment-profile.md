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

## First assessment submission

[`RAHP-VTI-FI-001`](../examples/cross-spec/vti-assessment/false-independence.yaml) is the first complete VTI composition assessment submission.

It maps the completed false-independence corpus `SR-XSP-FI-001` through `SR-XSP-FI-007` to `VTI-CMP-070` through `VTI-CMP-074`.

The assessment disposition is `supported`: the existing executable corpus supports the non-inference property within its pinned scope. This does not assert a universal proof of independence and does not convert RAHP into a conformance authority.

Legitimate plurality, pairwise/contextual identifiers, privacy-preserving pseudonymity, genuinely independent issuers, and selective disclosure remain preserved counter-boundaries.

## Reassessment and invalidation

An assessment must be reconsidered when any materially relevant input changes. The current profile enumerates VTI revision change, assessed component/version change, relying policy or profile change, material configuration change, evidence supersession, and evidence contradiction.

A stale or superseded assessment must not be silently reused as current evidence.

## Requirement/evidence map

The profile provides the initial map for semantic completion, authority continuity, lifecycle/freshness, delegation lineage, privacy across composition, false independence, failure/indeterminacy, configuration materiality, component substitution, and human control.

Only false independence is promoted as the first complete submission in this tranche. Other families remain `partially_verified`, `specialist_evidence_required`, or `evidence_required` until their existing evidence is reconciled against the exact upstream requirements.

This preserves the evidence-first rule: **do not manufacture a PASS because a requirement exists.**

## Validation

Run:

    python3 tools/validate_vti_assessment_profile.py

The validator checks the upstream source pin, disposition vocabulary, false-independence requirement mapping, schema validity, evidence uniqueness and existence, legitimate counter-cases, residual uncertainty, and negative fixtures showing that missing evidence or an unsafe `pass` disposition cannot validate.

The dedicated GitHub Actions workflow runs this validator on changes to the assessment profile, schema, first submission, validator, or documentation.

## Next evidence families

After this first end-to-end path is stable, subsequent work should progress family-by-family: semantic completion; authority continuity; lifecycle/freshness; delegation lineage; privacy composition with DPIP where specialist depth is required; failure/indeterminacy; configuration materiality; human control; and component substitution once concrete implementation evidence exists.

Each family should reuse the same assessment contract rather than inventing a new output shape.
