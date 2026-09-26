---
layout: default
title: Post-v2.4 non-DTG portability proof
parent: Adopt RAHP
nav_order: 8
---
# Post-v2.4 non-DTG portability proof

RAHP's deepest maintained exemplar is DTG, but the portable engine must not depend on DTG vocabulary or deployment assumptions. The post-v2.4 portability gate therefore uses the maintained **CAWG/C2PA assessment instance** as a real non-DTG consumer rather than introducing a synthetic target solely for release qualification.

## What is exercised

The machine-readable proof at `examples/cawg-c2pa/post-v2.4-portability-proof.yaml` binds two existing evidence lineages.

First, the CAWG Identity Assertion pressure test remains source-pinned to `decentralized-identity/cawg-identity-assertion@8a9c4925df7e8ccbcabce9d754fc27739e11dc12`. It preserves two open residual propositions: identity validity is not automatically role/domain authority, and historical validity requires durable as-of evidence.

Second, the CAWG/C2PA monitor's issue #765 records a later material-change reassessment for `c2pa-org/specifications`, from `9c58c8c27044e44e8601f6ab13f1bcac1376eb1f` to `4eb2c67f49bd21f188e7842afa16dfa642bb578c`. The changed surface was the supplemental soft-binding algorithm registry. Review found the delta added WebP media-type metadata to an existing algorithm and did not alter C2PA manifest, signature, trust-list or revocation semantics.

The correct reassessment result was therefore **no material assurance impact for that bounded delta**, with the observed baseline advanced. It was not a universal PASS and it did not close unrelated CAWG/C2PA findings.

## Why this is portability evidence

The consumer uses the same stable RAHP compatibility authority as the DTG exemplar:

- `rahp-engine-contract-v1` revision 1.3;
- normalized result schema 1;
- `rahp-evidence-retention-v1`.

Consumer-specific vocabulary remains in the CAWG profile, instance, examples and review records. It does not enter the portable core.

The reassessment also demonstrates the post-v2.4 operating rule: a material repository change does not require rerunning every available proposition. RAHP may disposition the exact affected surface, preserve still-valid evidence and residual ownership, and widen scope only when the materiality boundary cannot be defended.

## What this does not prove

This proof does not establish CAWG or C2PA conformance, upstream endorsement, universal portability to every domain, or the absence of unresolved CAWG/C2PA assurance questions. It proves that a maintained non-DTG consumer can use the stable generic RAHP contracts and can preserve bounded reassessment lineage without target-specific changes to the core.

The existing consumer-independence invariant remains authoritative for dependency direction: consumers may depend on RAHP's portable contracts; the portable core must not depend on consumers.
