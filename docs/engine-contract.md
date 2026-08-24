---
layout: default
title: "Engine contract"
nav_order: 1
has_toc: true
parent: Implement RAHP
---
# RAHP engine contract

RAHP separates **toolkit releases**, the **engine contract family**, the **engine contract revision**, and the **normalized result schema**. These versions are related but do not advance together.

The current stable engine state is:

| Surface | Current value | Meaning |
|---|---|---|
| Toolkit release | `v1.6.0` | Packaged RAHP release |
| Engine contract family | `rahp-engine-contract-v1` | Stable interoperability/semantic boundary |
| Engine contract revision | `1.2` | Current additive capability level inside the v1 family |
| Normalized result schema | `1` | Portable result-document compatibility boundary |

An implementation can therefore state, for example: **engine contract `rahp-engine-contract-v1`, revision `1.2`, normalized result schema `1`**.

## Current stable revision

Revision `1.2` is stable. It extends the v1 contract family additively so a conforming implementation can represent evidence classification, residual assurance evaluation, governed remediation, and evidence-based retesting without making Python or TypeScript behaviour normative.

The revision 1.2 lifecycle is:

```text
source → observation → trigger → assessment → evidence → evaluation
       → finding → disposition → remediation → retest → baseline
```

A detector signal is not automatically a finding. Evidence must be classified, relevant controls and assurance tests credited, and the residual state recorded. A result with zero findings is not equivalent to assured when unresolved assurance gaps, review-required propositions, or unassessed propositions remain.

The normalized result remains schema version `1`. Revision 1.2 adds optional `assurance_summary`, `evaluations`, `remediations`, and `retests` fields while preserving the v1 result compatibility boundary.

## How the engine contract increments

The family identifier is intentionally stable across compatible additive evolution.

### Clarification or non-semantic fix

A wording correction, documentation clarification, validator bug fix, or other change that does not alter the portable engine semantics does **not** increment the engine revision.

### Additive compatible change

A new optional operation, additive invariant, or compatible capability increments the **minor engine revision** while remaining in the same contract family.

For example:

```text
rahp-engine-contract-v1, revision 1.2
                  ↓ additive compatible change
rahp-engine-contract-v1, revision 1.3
```

A revision claim is cumulative: an implementation claiming revision `1.3` must satisfy all requirements and conformance fixtures inherited from `1.0`, `1.1`, and `1.2` in addition to the new `1.3` requirements.

### Breaking engine change

A change that makes an existing conforming implementation semantically incompatible requires a **new contract family identifier**, not a larger minor revision. Examples include removing or renaming a required operation, changing the meaning of an existing required operation, making previously optional semantics mandatory in an incompatible way, or changing lifecycle/disposition semantics such that existing conforming implementations would produce materially different valid outcomes.

Such a change moves to a new family such as:

```text
rahp-engine-contract-v2, revision 2.0
```

The prior v1 contract and its conformance evidence remain historical compatibility evidence.

## Result-schema versioning is separate

Engine evolution does not automatically require a new normalized result schema. Compatible optional fields may preserve schema version `1`. A change that causes a previously conforming result document to become invalid, or changes required result semantics incompatibly, requires a new normalized result schema version.

## Toolkit releases are also separate

A RAHP Toolkit release may change corpora, documentation, workflows, examples, release machinery, or other non-engine surfaces without changing the engine revision. Conversely, an additive engine revision may be introduced as part of whichever toolkit release carries and qualifies that change.

Do not infer the engine revision from the toolkit version number.

## Normative sources and conformance

Normative portable surfaces are `method/engine-contract.yaml`, the schemas under `method/schema/`, `method/evidence-retention.yaml`, `method/versioning.yaml`, mappings, and shared conformance fixtures. Reference implementations may use richer internal logic but must preserve normalized proposition, evidence, reasoning, and lifecycle semantics.

`tools/validate_engine_contract.py` verifies that the declared family/revision agrees with versioning metadata and that the stable conformance fixtures continue to pass.
