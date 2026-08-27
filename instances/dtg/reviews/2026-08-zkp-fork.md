---
title: "DTG review: ZKP fork executable privacy and construction evidence"
parent: DTG RAHP review record
nav_order: 30
layout: default
nav_exclude: true
---

# DTG review: ZKP fork executable privacy and construction evidence

**Assessment ID:** `DTG-AR-2026-003`  
**Assessment key:** `dtg:repository:sankarshanmukhopadhyay/dtgwg-zkp-tf`  
**Mode:** combined RAHP + security  
**Status:** dispositioned  
**Disposition:** no-blocking-assurance-impact  
**Assessment queue disposition:** `no-material-assurance-impact`  
**Reviewed revision:** `6e1356812716dbd0e551272251e3e825132a8268`

## Scope and lineage

This durable review extends the previously dispositioned ZKP-fork baseline at
`546babc471130af751ed3a117a0d476f5e0a7e03` through two sequential DTG Portfolio
Monitor assessment windows:

1. `546babc471130af751ed3a117a0d476f5e0a7e03` →
   `6064c3428ca88471b5ec8271ec03e318c26d2a13` — RAHP queue issue **#72**;
2. `6064c3428ca88471b5ec8271ec03e318c26d2a13` →
   `6e1356812716dbd0e551272251e3e825132a8268` — RAHP queue issue **#86**.

The windows are reviewed together because #72 had not yet advanced the durable assessment
baseline when #86 was raised. The review does not skip that intervening history: the final
revision is accepted only after examining both deltas and preserving the residual states
introduced or clarified by each.

The review remains a **combined RAHP + security** assessment. It evaluates the changed
assurance semantics, privacy failure modes, construction evidence and security boundaries;
it is not a formal cryptographic audit or a claim that experimental constructions are
production-qualified.

## Window #72 — composed-presentation privacy and experimental constructions

The first window materially expands executable evidence. It adds composed-presentation
privacy semantics and concrete experimental evidence for BBS selective disclosure,
`PR-REL` relationship proofs, `PR-HID` hiding commitments and `PR-RES` resolution/currentness
profiles.

### RAHP / harms assessment

The change strengthens rather than weakens the assurance boundary:

- privacy is evaluated across the complete **evidence closure**, not inherited from an
  individually privacy-capable credential or proof;
- exact issuer, delegation, status or registry identifiers are not required merely because
  a predicate can be expressed using them;
- deterministic digests of enumerable values are explicitly rejected as a confidentiality
  mechanism;
- live status/resolution observations are treated as correlation surfaces that must be
  disclosed and governed;
- proof validity, authority, accreditation, lifecycle and governance recognition remain
  separate propositions even where they reuse cryptographic primitives.

This directly reduces the risk that a technically valid proof is over-promoted into a
stronger privacy, authority or trust conclusion.

### Security assessment

The experimental construction evidence includes material defensive properties:

- the `PR-HID` Pedersen-style example uses fresh cryptographic randomness for normal
  commitments and checks that two commitments to the same value are distinct;
- it includes a deliberate dictionary-recovery regression showing why a deterministic
  digest of a low-entropy value is not hiding;
- the `PR-REL` Sigma-style proof uses profile-specific domain separation and binds the
  Fiat-Shamir challenge to the commitments, prover commitments and application/verifier
  context;
- a proof generated under one context fails under a changed context;
- fresh proofs are checked for fresh prover randomness;
- the second commitment generator is independently hash-derived and the profile explicitly
  forbids choosing a generator with a known discrete-log relationship to the base point;
- the profile explicitly states that equality of attacker-chosen unauthenticated commitments
  is not evidence of a legitimate DTG relationship.

No new blocking security defect was identified in this experimental evidence window.
The construction material remains non-normative and requires independent implementation,
adversarial and interoperability evidence before production promotion.

## Window #86 — asymmetric relationship privacy and community-anchored proof

The second window adds executable pressure tests for asymmetric reciprocal relationship
edges and a construction-neutral semantic input contract for Community-Anchored Proof.

### RAHP / harms assessment

The change prevents several important overclaims:

- hiding a private reciprocal relationship half does not imply relationship-level or
  graph/context unlinkability when the other half is deliberately public;
- a reusable binder fails the cross-context privacy claim even when the proof itself is
  cryptographically valid;
- public graph composition is separately evaluated rather than erased by proof-level
  non-disclosure;
- proof validity cannot establish common VTN anchoring or policy acceptance unless those
  propositions are separately evidenced;
- Community-Anchored Proof Clause 3 is `INDETERMINATE` when independently checkable
  third-party membership evidence is unavailable; missing semantics cannot be promoted
  to PASS.

These are material coverage refinements and align the ZKP layer with the existing DPIP
boundary: ZKP reports scoped proof properties; DPIP evaluates effective privacy of the
composed interaction.

### Security assessment

The new semantic tests require holder and verifier-challenge binding, current credentials,
private status handling and absence of reusable binders. The Community-Anchored Proof
input contract also requires authenticated/determinable registry state and makes
currentness side channels part of the security/privacy analysis.

No new production cryptographic construction is introduced in this window, so the primary
security effect is stronger negative testing and clearer rejection/indeterminate semantics.

## Findings and residual assurance states

### F-001 — Experimental constructions are executable but not production-qualified

**Status:** open  
**Residual state:** `review-required`  
**Owner:** ZKP construction-selection / conformance workstream

The earlier construction-coverage gap is materially reduced: multiple concrete experimental
profiles and executable vectors now exist. That does not establish production suitability.
Independent implementation evidence, cryptographic/adversarial review, serialization and
encoding profiles, constrained-device evidence and ecosystem interoperability are still
required before promotion.

**Retest condition:** a construction is proposed for normative or production status, or
independent implementation/adversarial evidence materially changes the confidence level.

### F-002 — Cross-spec authority and lifecycle dependencies remain external

**Status:** open  
**Residual state:** `assurance-gap`  
**Owner:** cross-specification companion profiles

Proof validity still does not establish current delegated authority, relying-party purpose,
action-time lifecycle state, governance recognition or cross-community policy acceptance.
The reviewed changes correctly preserve those boundaries rather than attempting to solve
them inside the ZKP layer.

**Retest condition:** adopted Trust Tasks, Credential, delegation or governance profiles
supply new authority, purpose, audience, freshness or revocation semantics at the composed
decision boundary.

### F-003 — Community and registry proof inputs remain an owning-layer dependency

**Status:** open  
**Residual state:** `external-dependency`  
**Owner:** Credential / Registry / governance profile owners

Community-Anchored Proof can now reject or mark unsupported Clause 3 claims indeterminate,
but a production prover/verifier remains dependent on a concrete interoperable
representation of counterparty membership, common-community semantics, authenticated
registry state and privacy-preserving currentness evidence.

**Retest condition:** an owning specification or deployment profile exposes a concrete,
interoperable representation satisfying the construction-neutral input contract.

## Pressure tests / falsification evidence

The review specifically looked for evidence that would overturn the no-blocking-impact
disposition:

- deterministic or reusable hiding binders;
- missing domain/context separation in relationship proofs;
- proof validity being promoted to authority or governance acceptance;
- exact identifiers becoming mandatory where a predicate would suffice;
- live registry/status lookup being ignored as a correlation channel;
- missing third-party membership evidence being silently treated as PASS;
- experimental construction evidence being represented as normative production support.

The inspected changes contain explicit guards or negative cases for each of these classes.
No falsifying evidence was found in the reviewed windows.

## Assurance disposition

No new blocking RAHP or security defect is introduced across the two queued windows. The
combined delta is a **material strengthening of composed-privacy reasoning, negative-test
coverage, construction evidence and conformance honesty**.

The disposition is therefore `no-material-assurance-impact` for queue issues **#72** and
**#86**, while F-001 through F-003 remain explicit residual assurance states. This is not a
claim that the experimental constructions have completed production cryptographic review.

The durable assessment baseline advances to
`6e1356812716dbd0e551272251e3e825132a8268` only after this record and its machine-readable
result are merged and repository validation remains green.

## Sources

- <https://github.com/sankarshanmukhopadhyay/dtgwg-zkp-tf/compare/546babc471130af751ed3a117a0d476f5e0a7e03...6064c3428ca88471b5ec8271ec03e318c26d2a13>
- <https://github.com/sankarshanmukhopadhyay/dtgwg-zkp-tf/compare/6064c3428ca88471b5ec8271ec03e318c26d2a13...6e1356812716dbd0e551272251e3e825132a8268>
- `docs/implementation-guide/boundaries/composed-presentation-privacy.md`
- `docs/implementation-guide/conformance/experimental-pr-rel-sigma-profile.md`
- `benchmarks/pr-rel-sigma/relationship-proof.mjs`
- `benchmarks/pr-hid-pedersen/hiding-binder.mjs`
- `docs/implementation-guide/pressure-tests/asymmetric-cross-community-relationship-edge.md`
- `docs/implementation-guide/interoperability/community-anchored-proof-input-contract.md`
- `conformance-harness/tests/test_asymmetric_edge_privacy.py`
- `conformance-harness/tests/test_community_anchored_proof.py`
