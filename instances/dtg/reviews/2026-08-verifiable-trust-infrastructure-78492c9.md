---
title: "DTG review: Verifiable Trust Infrastructure through 78492c9"
parent: DTG RAHP review record
nav_order: 12
layout: default
nav_exclude: true
---

# DTG review: Verifiable Trust Infrastructure through 78492c9

**Assessment ID:** `DTG-AR-2026-005`  
**Assessment key:** `dtg:repository:OpenVTC/verifiable-trust-infrastructure`  
**Mode:** combined RAHP + security  
**Status:** dispositioned  
**Assessment queue issue:** `#21`  
**Previous durable baseline:** `187ad9cde4cf5c5f8add3732a661816a650d631c`  
**Reviewed revision:** `78492c9d5c35419a9d47c8ad4f16fbef77fe94a4`

## Proposition tested

Do the material VTI implementation changes after the previous durable baseline materially strengthen retry/idempotency, publication authority, privacy/correlation, lifecycle and operational security without introducing a new blocking harm or security regression?

The assessment uses the complete descendant window from the last durable reviewed revision through the latest revision coalesced into #21. It does not infer safety merely from test success and does not reclassify deployment/governance dependencies as implementation guarantees.

## Executive judgment

The change window is **net assurance-strengthening**. No new blocking harm or security defect was identified. The strongest improvements are the explicit lost-reply/idempotency contract, request-bound relationship publication/revocation proof-of-possession, non-retention of correlation-sensitive authorization proofs, stronger concurrency semantics for application state, and more explicit negative/boundary testing.

The review nevertheless retains bounded residuals. In particular, availability is preferred over duplicate-effect prevention when the idempotency store itself fails; audit attribution intentionally permits a privileged operator to map a member to pairwise relationship edges; VTC publication still transiently observes the membership DID and relationship DID in one request; application-state namespaces are not authorization boundaries; DID-resolution privacy is partly a deployment-policy choice; and one relationship authorization digest construction has an acknowledged interoperability/canonicalization dependency.

These residuals are visible, owned and retestable. They do not justify representing the implementation as universally private, exactly-once, or independent of deployment governance.

## Pressure-test results

### Lost reply, retries and duplicate consequential effects

The implementation now assigns exactly one application-layer retry owner: `VtaClient::idempotent`. Consequential Trust Task URIs are classified by retry consequence, and a census test prevents new tasks from silently joining the catalogue without classification. Stable idempotency keys are signed as part of the Trust Task document, scoped by principal and bound to both task type and request payload. Claims are taken atomically before dispatch, closing the ordinary get-then-put race.

The design also avoids turning retry bookkeeping into a second secret store: secret-bearing responses record completion without caching/replaying the response body. Retry hints are bounded, and conflicting use of one key for different requests is rejected.

**Residual:** if the idempotency store fails, the service logs the error and dispatches the operation unguarded. This is an explicit availability-over-duplicate-prevention tradeoff. It is not a hidden defect, but deployments that require hard exactly-once semantics cannot derive that guarantee from this implementation.

### Relationship publication, revocation and correlation

The earlier equality `authenticated member DID == credential issuer DID` is replaced for pairwise relationship identifiers by request-bound issuer proof-of-possession. The authorization is bound to the credential digest, audience, authenticated session and freshness window. This preserves the distinction between possession of a VRC and authority to publish it.

The proof-of-possession is verified and discarded rather than persisted or logged, avoiding a durable session/M-DID to R-DID linkage in ordinary relationship storage. The same identity-equality audit was correctly extended to issuer revocation rather than fixing publication alone.

The graph now distinguishes unilateral half-edges from reciprocated complete edges, so reciprocal publication can serve as explicit counterparty consent evidence rather than inferring consent from mere membership.

**Residual:** the VTC necessarily sees the membership DID and relationship DID together transiently during this flow. Full unlinkability at the operator boundary requires the community-anchored ZKP construction or equivalent proof mechanism. Also, the privileged audit store deliberately retains sufficient attribution to map an edge back to the authenticated member for moderation and accountability. That is an accepted controlled correlation surface, not a zero-linkage property.

### Audit and redress tradeoff

Audit attribution records the authenticated member rather than the relationship DID. The design narrows exposure through admin-gated access, HMAC-based actor hashing and a plaintext field designed for RTBF redaction without breaking the tamper-evidence chain.

This is a defensible accountability tradeoff, but it must remain explicit: an operator with audit access can correlate pairwise activity to the member. A future change that emits the same linkage into ordinary logs would materially worsen the privacy boundary and must be treated as a regression.

### Application-state concurrency and isolation

Application state now has versioned records, per-namespace monotonic sequencing, optimistic concurrency, conflict responses carrying the winning state, tombstones for convergent incremental sync, bounded record sizes and batch operations. These are meaningful recoverability and concurrency improvements.

**Residual:** namespace is a naming/collision boundary, not an authorization boundary. Mutually untrusted applications that share one context can still require separate contexts or another enforceable access boundary. Schema conformance alone therefore does not establish application isolation.

### DID resolution and accepted-method policy

Relationship identifiers are method-independent, which is useful for portability, but the privacy of resolving a relationship DID depends on the accepted DID method and resolver behavior. The implementation notes that accepted methods should become community/deployment policy rather than relying accidentally on library defaults.

**Residual:** until that policy is explicit and tested, a deployment can choose a DID method whose resolution leaks relationship information to a third party while the relationship protocol itself remains conformant.

### Canonicalization and interoperability

The relationship publication authorization binds to a credential hash computed using the implementation's recursive key-sorting canonicalization. The design note itself identifies this as not yet a sufficiently specified cross-implementation canonicalization algorithm.

**Residual:** this is primarily an interoperability/assurance dependency rather than an immediate local signature bypass: both creation and verification within one implementation agree, but independent implementations need a normative reproducible digest construction before this can be treated as portable conformance evidence.

## Prior finding lineage

| Prior finding | Delta | Current judgment |
|---|---|---|
| `F-003` Onboarding depends on verification of attested configuration | `not-materially-retested` | Remains a watch condition; this change window does not provide evidence that eliminates the onboarding-attestation dependency. |
| `F-004` Parent retains availability and routing influence | `unchanged` | Remains residual. The new retry machinery improves operation recovery but does not remove upstream/parent availability or routing dependencies. |
| `F-006` IACA trust-anchor lifecycle dependency | `unchanged` | Remains a watch condition outside the principal changed surfaces. |
| `F-007` Certificate revocation deliberately not checked | `unchanged` | Remains an accepted limitation unless the mdoc/status model changes. |
| `F-008` Non-extractable keys trade recoverability for stronger custody | `unchanged` | Remains an operational-control tradeoff; application-state recovery does not imply key recoverability. |

## Current findings and controlled residuals

### F-009 — Idempotency-store failure can re-open duplicate-effect risk

**Status:** `assurance-gap`

If idempotency storage fails, a keyed consequential operation is dispatched unguarded. This preserves availability but means the implementation does not provide a hard exactly-once guarantee under storage failure plus lost reply.

**Retest/falsification condition:** an explicit deployment profile either demonstrates resilient idempotency storage within the required failure model or defines a fail-closed policy for operations whose duplicate effect is unacceptable.

### F-010 — Pairwise relationship privacy is controlled, not operator-unlinkable

**Status:** `controlled`

Request-bound PoP and non-retention materially reduce durable public/member linkage, but the VTC observes M-DID and R-DID together transiently and the privileged audit store deliberately preserves accountable attribution.

**Retest/falsification condition:** a composed privacy test demonstrates an accepted ZK/anonymous authorization construction for publication/revocation, or a deployment privacy profile explicitly accepts and constrains the operator correlation boundary.

### F-011 — Application-state namespace does not enforce isolation

**Status:** `assurance-gap`

Namespace separation prevents accidental key collision but does not establish authorization between mutually untrusted applications sharing a context.

**Retest/falsification condition:** deployment evidence demonstrates separate contexts or another enforced access-control boundary for applications that must not access each other's state.

### F-012 — Relationship identifier resolution privacy depends on DID-method policy

**Status:** `review-required`

Method-independent relationship identifiers are portable, but resolution can leak relationship information depending on the method/resolver selected by a deployment.

**Retest/falsification condition:** community/deployment policy publishes an allowed-method set and tests that accepted resolution paths meet the required relationship-privacy property.

### F-013 — Relationship authorization digest needs portable canonicalization

**Status:** `review-required`

The local digest construction is deterministic inside this implementation but is not yet a normative, independently reproducible cross-implementation canonicalization contract.

**Retest/falsification condition:** the relevant specification or shared implementation contract defines and tests a portable canonicalization/digest algorithm across independent implementations.

## Security disposition

No new blocking security defect was identified. The change set closes important replay and authorization ambiguities, adds negative tests around request binding and reuse, reduces unnecessary proof retention and strengthens concurrency/retry behavior.

The most important security boundary to preserve is that implementation convenience must not silently erase the documented fail-open/fail-closed tradeoffs. In particular, idempotency-store failure, audit attribution, accepted DID methods and application-state isolation are deployment/security-policy decisions with observable consequences.

## Disposition

**Outcome:** `findings-raised`.

This does not mean the VTI change window is unsafe. The implementation is materially stronger than the prior reviewed baseline. The disposition keeps five bounded residual conditions visible because the evidence does not justify promoting them to universal assurance properties.

Issue #21 is closure-eligible once the normalized result and this record are merged with reviewed revision `78492c9d5c35419a9d47c8ad4f16fbef77fe94a4` and repository validation is green.

## Retest triggers

- material VTI change after `78492c9...` affecting retry/idempotency or consequential effect semantics;
- relationship publication/revocation authorization, proof retention, logging or audit-attribution changes;
- adoption of community-anchored ZKP or another operator-unlinkable publication authorization mechanism;
- application-state authorization/isolation model changes;
- accepted DID-method or resolver privacy policy changes;
- portable VRC canonicalization/digest contract changes;
- IACA/mdoc trust-anchor or revocation/status model changes;
- internal-key custody/recovery policy changes.

## Source evidence

- `OpenVTC/verifiable-trust-infrastructure` compare window `187ad9c...` → `78492c9...`.
- `docs/05-design-notes/retry-and-idempotency.md` at `78492c9...`.
- `docs/05-design-notes/vrc-publish-proof-of-possession.md` at `78492c9...`.
- `docs/05-design-notes/appstate-store.md` at `78492c9...`.
- Prior durable RAHP VTI result `instances/dtg/reviews/2026-08-verifiable-trust-infrastructure.result.json`.
