---
layout: default
title: "VTI pre-specification residual evidence families"
parent: Reference
nav_order: 4
has_toc: true
---
# DTG VTI pre-specification evidence — residual families and handoff

This document completes the bounded disposition wave for the working evidence register in RAHP #192. It complements `vti-pre-specification-evidence-pack.md`, which defines the evidence-pack contract and packages the false-independence family.

This is **tested pre-specification evidence, not VTI normative text**. RAHP does not own a future VTI specification. The purpose of this document is to preserve what RAHP/DPIP/Interop evidence establishes, what it does not establish, and which questions require a future composition-level normative owner.

## Disposition summary

| Family | Source | Evidence posture | Disposition |
|---|---|---|---|
| Constrained authority | #64 | strong executable/source-pinned evidence; reusable contract absent | upstream VTI input |
| Lifecycle precedence | #66, #187, PR #236 | executable lifecycle/stale-state evidence; reusable contract absent | upstream VTI input |
| Privacy composition | #184, #231, DPIP #127, #237/#240 | real A/B evidence; bounded correlator observed; residual uncertainty preserved | upstream VTI input + future evidence where real surfaces exist |
| Semantic completion | #185 | executable evidence complete | upstream-packageable |
| Delegation lineage | #186 | executable evidence complete | upstream-packageable |
| Principal authorization | #189 | executable evidence complete | upstream-packageable |
| Discovery vs authority | #191 | executable evidence complete | upstream-packageable |
| Component substitution | #188 | `EVIDENCE_REQUIRED` | deferred evidence trigger; requires genuine conformant A/B implementations |
| Portability / migration | #190 | `EVIDENCE_REQUIRED` | deferred evidence trigger; requires genuine two-implementation migration |

## Constrained authority — #64

**Proposition.** Valid identity, appointment or provenance does not by itself establish current permission for a particular consequential act.

**Why composition exposes it.** Credential/source authority, Trust Task context, current authority state and transaction-specific permission span artifacts and specifications.

**Falsifier / adversarial case.** A valid standing appointment is over-read as permission for an action outside current scope or without transaction-time authority evaluation.

**Legitimate counter-case.** A bounded, current, authoritative appointment may legitimately support action when the transaction is within explicit scope and permission.

**Executable evidence.** #64 and the guardianship/fiduciary pressure-test evidence closure, including the routine bounded-authority transaction.

**Ownership assessment.** `COMPOSITION-OWNED / VTI-CANDIDATE`.

**Residual uncertainty.** No reusable cross-spec constrained-authority composition contract currently satisfies the #64 retest condition.

**Upstream question.** What common composition profile binds authoritative source class, current state, action/domain scope, transaction permission, minimisation and non-inference?

## Lifecycle precedence and restoration — #66

**Proposition.** Historical or cryptographic validity must not override authoritative current lifecycle state across composed authority evidence.

**Why composition exposes it.** Suspension, revocation, supersession, restoration, approvals and effective-time ordering can be represented by different artifacts and services.

**Falsifier / adversarial case.** A stale but valid artifact remains actionable after suspension/supersession, or restoration is interpreted inconsistently across implementations.

**Legitimate counter-case.** Historical evidence can remain available for audit while current authoritative state governs consequential action.

**Executable evidence.** #66, #187 and PR #236 (`c557c0e521ece1290a4f69d7220aec111f53f8e3`), including suspend/revoke/supersede/restore/stale-state vectors.

**Ownership assessment.** `JOINTLY-OWNED / VTI-CANDIDATE`.

**Residual uncertainty.** The #66 retest condition still requires a reusable lifecycle/status composition contract with deterministic precedence semantics.

**Upstream question.** Which lifecycle vocabulary, effective-time rules and precedence semantics govern composed authority state at decision time?

## Privacy and correlation resistance — #184

**Proposition.** A privacy property claimed for a composed interaction must survive the complete interaction boundary; proof-level unlinkability is insufficient when another composed surface introduces a durable correlator.

**Why composition exposes it.** Identifiers, endpoints, status/policy discovery, Trust Tasks, retained relationship evidence, verifier behavior and proof transcripts can each be locally conformant while jointly enabling correlation.

**Falsifier / adversarial case.** Context-distinct interactions use privacy-preserving proofs but expose or retain a stable relationship/task/status/verifier correlator.

**Legitimate counter-case.** Explicitly permitted continuity within a declared context is not automatically a privacy failure; positive-control same-context joins must be distinguished from unintended cross-context joins.

**Executable evidence.** Immutable Dogwood target `OpenVTC/verifiable-trust-infrastructure@cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b`; Interop #65; Actions `33290185572`; artifact `9725752935`, digest `sha256:5ee2cce404cf5f3f021eaadcd54e6826fe2cfd7aff5cac8f0ceaa48240ce315c`; RAHP #231; DPIP #127. The A/B run observed the same protocol-visible relationship binder `did:key:z6MktULudTtAsAhRegYPiZ6631RV3viv12qd4GQF8z1xB22S`. Status + Trust Task A/B evidence subsequently landed through #237/#240 and Interop Lab PR #68 (`12c4917cc1a522c16ee0fe3bfe832143fb17479a`), run `33294651029`, artifact `9727021348`, digest `sha256:ca04d8d8acc30ade555e6da5bbec91ac9d935022f71afaac48eefdb4e57efd01`.

**Ownership assessment.** `JOINTLY-OWNED / VTI-CANDIDATE`; DPIP remains the specialist privacy evaluator where material.

**Residual uncertainty.** Evidence is composition-bounded and must not be promoted into a whole-VTI privacy PASS. Full verifier/deliberate-correlation behavior and any unobserved implementation surfaces remain evidence-dependent.

**Upstream question.** What correlation boundary must a VTI composition declare and preserve across identifiers, discovery, task state, retention and verifier behavior?

## Completed executable families

The following families have sufficient bounded RAHP evidence for upstream review. Their source issues are already completed and should not be reopened merely to draft normative VTI language.

### Semantic completion — #185

**Proposition.** Protocol/workflow completion is not automatically semantic satisfaction of the intended trust outcome.

**Evidence.** #185, closed via PR #233. Technical completion remains distinct from semantic `SATISFIED`, `FAILED` or `INDETERMINATE`.

**Upstream question.** How must VTI distinguish execution completion from semantic trust outcome?

### Delegation lineage — #186

**Proposition.** Executable capability is not equivalent to current delegated authority; composed execution must preserve scope and lineage.

**Evidence.** #186 and PR #236 bounded A→B→C scope, revocation, re-delegation and missing-lineage vectors.

**Upstream question.** What lineage and current-state semantics must survive delegation across component boundaries?

### Meaningful principal authorization — #189

**Proposition.** Machine completion must not substitute for required principal authorization of the exact consequential action.

**Evidence.** #189 and PR #236 exact-scope, overbroad and missing-authorization vectors.

**Upstream question.** Which actions require explicit principal authorization, and how is exact scope bound to composed execution?

### Discovery is not authority — #191

**Proposition.** Successful discovery/resolution must not be elevated into proof of trust, authorization or current authority.

**Evidence.** #191 and PR #236, including resolution success with authority `DENIED` / `INDETERMINATE` and a legitimate authorized counter-case.

**Upstream question.** How should VTI prevent discovery/resolution success from being over-read as trust or permission?

## Deferred evidence triggers

### Component substitution — #188

**Proposition.** Replacing one individually conformant component must not silently change claimed composition-level trust, privacy, authority, lifecycle or human-control properties.

**Evidence posture.** `EVIDENCE_REQUIRED`.

A synthetic pair built only for RAHP would not establish whether real independent implementations preserve or alter the relevant semantics. Future RAHP work should trigger only when two genuine, independently meaningful implementations of a replaceable component can be exercised A/B under the same composition.

**Upstream question.** What composition claims must be re-evaluated when a conformant component implementation is substituted?

### Portability / migration — #190

**Proposition.** Migration between implementations must preserve required semantic meaning and lifecycle state, or explicitly identify what cannot be preserved.

**Evidence posture.** `EVIDENCE_REQUIRED`.

A meaningful portability conclusion requires a genuine A→B migration covering independently implemented state and semantics. Future RAHP work should trigger only when two real implementations support export/import of the relevant credentials, relationships, governance references, delegation and lifecycle state.

**Upstream question.** Which semantic and lifecycle properties constitute VTI portability rather than byte-level artifact portability?

## Handoff and re-entry rule

1. Do not reopen completed RAHP evidence families merely to draft VTI normative language.
2. Route normative composition questions to the future upstream VTI owner.
3. Re-enter RAHP when a published composition contract creates a concrete retest condition or genuine implementations create new executable evidence.
4. Use DPIP for specialist privacy examination when RAHP materiality warrants it; return DPIP evidence without making DPIP the VTI owner.
5. Preserve `INDETERMINATE` and missing evidence as bounded uncertainty rather than converting them to PASS.
6. Do not create synthetic substitution or migration implementations solely to satisfy #188 or #190.

Closing #192 after this handoff means the working register has been packaged into durable repository evidence. It does **not** mean that a VTI specification exists or that every composition proposition has been normatively resolved.
