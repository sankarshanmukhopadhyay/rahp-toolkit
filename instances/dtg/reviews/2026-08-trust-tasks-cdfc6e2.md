---
title: "DTG review: Trust Tasks through cdfc6e2"
parent: DTG RAHP review record
nav_order: 11
layout: default
nav_exclude: true
---

# DTG review: Trust Tasks through cdfc6e2

**Assessment ID:** `DTG-AR-2026-004`  
**Assessment key:** `dtg:repository:trustoverip/dtgwg-trust-tasks-tf`  
**Mode:** combined RAHP + security  
**Status:** dispositioned  
**Disposition:** assurance-strengthened-with-explicit-deployment-boundaries  
**Assessment queue issue:** `#70`  
**Previous durable baseline:** `2a40f6bd3b13c85c49123174fdbe4354b3c48d81`  
**Reviewed revision:** `cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a`

## Proposition tested

Do the material Trust Tasks changes after the previous durable baseline strengthen authority, lifecycle, privacy, replay/idempotency and redress assurances without introducing a new blocking harm or security regression?

The review covers the complete descendant window `2a40f6b...` → `cdfc6e2...` rather than only the first revision observed by #70. The window contains 60 commits and includes framework 0.5, application-state tasks, VTC membership/removal and relationship-publication changes, binding/security/privacy linting and generated binding updates.

## Evidence and pressure tests

### Framework 0.5

The framework 0.5 envelope remains wire-compatible with 0.4 while adding consumer/specification obligations outside the envelope. The important assurance changes include:

- action-time freshness requirements over `issuedAt` / `expiresAt` for consequential tasks;
- stronger lifecycle semantics and no inference from silence;
- retention, ingestion and identifier-scope declarations;
- bounded free-text surfaces;
- ceremony enactment and predecessor binding with salted digests to reduce confirmation/correlation leakage;
- explicit separation between proof verification and authorization decisions.

These changes reduce ambiguity in several earlier RAHP concerns, but do not make cross-spec lifecycle or delegated authority self-solving.

### Application state

The new VTA application-state family introduces versioned records and optimistic concurrency. `expectedVersion` makes lost updates detectable, `expectedVersion: 0` supports one-winner lease acquisition, and conflict responses return the current state needed to resolve contention without a racy re-read.

The security boundary is explicit rather than hidden: a namespace is a collision-avoidance partition, **not** an authorization boundary. Two applications with write access to the same context can read/overwrite each other's namespaces; deployments needing isolation must use separate contexts. This is not a specification defect because the limitation is normative and visible, but it remains a deployment assurance condition that must be tested.

### Relationship publication

VTC relationship publication 0.2 materially strengthens provenance and privacy. Where a relationship credential uses a relationship DID rather than the document issuer, a proof-of-possession binds the VRC issuer to the Trust Task document and credential digest. Consumers must reject absent/unbound authorization and must not retain the proof-of-possession after verification, specifically to avoid creating a durable member↔relationship-DID correlator.

This directly reduces the risk that possession of another party's VRC is mistaken for authority to publish that party's edge.

### Removal notice and redress

The new removal-notice task substantially strengthens adverse-decision evidence. A removal notice is signed, names the deciding administrator, records the decision time and reason when given, and is independently verifiable after transport.

The residual boundary is delivery and institutional follow-through. The specification recognizes that removal itself may terminate the channel through which a member could ask why; it therefore requires a channel that can survive removal as an implementation property, but does not mandate a transport or compel a community to send a notice. This improves contestability evidence without proving end-to-end redress availability.

## Prior finding delta

| Prior finding | Delta | Current judgment |
|---|---|---|
| `F-001` Retained outcome evidence remains a cross-spec dependency | `weakened-but-survives` | Framework lifecycle/freshness and richer receipts/notices improve evidence, but no universal cross-spec contract makes task completion equivalent to credential validity or proves exactly-once consequential effect. |
| `F-002` Generic task-control and lifecycle observability | `strengthened` | Remains `controlled`; framework 0.5 and additional task families make freshness, lifecycle and failure semantics more explicit and machine-testable. |
| `F-005` Supervising/delegated authority | `unchanged` | Remains an `assurance-gap`; proof and local ACL checks do not establish a universal cross-system delegation/governance model. |

## New bounded findings

### F-009 — Application-state namespace is not an authorization boundary

**State:** `deployment-control`

The specification explicitly states that namespace separation is not access isolation. A deployment that co-locates mutually untrusted applications in one context can expose cross-application state modification even while conforming to the task schema.

**Falsification / retest condition:** deployment tests demonstrate separate contexts or equivalent enforced authorization boundaries for applications that must not read/write one another's state.

### F-010 — Removal evidence does not guarantee durable redress delivery

**State:** `assurance-gap`

The removal notice makes an adverse decision attributable and contestable when received, but a community can still fail to deliver it, choose not to send it, or use a channel that disappears with membership. The task improves evidence semantics, not institutional availability.

**Falsification / retest condition:** deployment profile requires and tests durable post-removal delivery plus an appeal/redress endpoint that survives membership termination.

### F-011 — Relationship publication provenance/correlation control

**State:** `controlled`

Issuer proof-of-possession plus one-use/non-retention semantics materially close the earlier ambiguity between possessing a VRC and being authorized to publish the edge. Negative tests should continue to reject missing, mismatched or retained publication authorization.

## Security disposition

No new blocking security defect was identified in this change window. The material changes are net assurance-strengthening because they make freshness, concurrency, publication authority, correlation minimization and adverse-decision evidence more explicit.

The residual risks are deliberately not converted into generic PASS claims: namespace isolation remains a deployment choice; removal/redress availability remains a governance/deployment property; cross-system delegated authority and cross-spec lifecycle remain companion-profile obligations.

## Disposition

**Outcome:** `findings-raised`.

This outcome does not mean the change set is unsafe. It records that the changed semantics were reviewed, that several previous concerns were weakened or controlled, and that two bounded deployment/governance assurance gaps remain visible with falsifiable retest conditions.

Issue #70 is closure-eligible once this record is merged and identifies `cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a` as the reviewed revision.

## Retest triggers

- material Trust Tasks changes after `cdfc6e2...` affecting framework freshness/privacy/lifecycle;
- application-state authorization or namespace-isolation changes;
- relationship publication authorization or proof-retention changes;
- removal-notice delivery/redress semantics or deployment-profile changes;
- adoption/change of a cross-system delegation profile;
- companion Credential/ZKP changes that alter action-time authority or composed privacy.

## Sources

- <https://github.com/trustoverip/dtgwg-trust-tasks-tf/compare/2a40f6bd3b13c85c49123174fdbe4354b3c48d81...cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a>
- <https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a/specs/_framework/0.5/trust-task.schema.json>
- <https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a/specs/vta/app-state/put/1.0/spec.md>
- <https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a/specs/vtc/relationships/publish/0.2/spec.md>
- <https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/cdfc6e231dc6cc9ed901bbd27b4c6e8ea2f3e06a/specs/vtc/members/removal-notice/0.1/spec.md>
