# Guardianship and fiduciary authority: cross-spec RAHP pressure test

This worked example applies the portable RAHP method to a composed digital-trust problem: how a system represents, proves, exercises, reviews and terminates **guardianship, fiduciary and other constrained authority** without collapsing legal or governance distinctions into a single credential or cryptographic proof.

The Trust over IP Digital Trust Graph (DTG) is the first worked instance. This is not a DTG-specific extension to RAHP and is intentionally not listed in `examples/current-baselines.yaml` as a canonical maintained example.

## Assessment lifecycle

The case preserves the complete evidence trail:

1. [`hypothesis-baseline.yaml`](./hypothesis-baseline.yaml) preserves the initial hypotheses and candidate findings.
2. [`evidence-pass.yaml`](./evidence-pass.yaml) records the first source-pinned reassessment against current DTG revisions.
3. [`evidence-review.md`](./evidence-review.md) explains how that source review weakened or refined the starting claims.
4. Three machine-readable transaction constructions test the remaining hypotheses against concrete evidence closure:
   - [`transactions/routine-act.yaml`](./transactions/routine-act.yaml)
   - [`transactions/threshold-coapproval.yaml`](./transactions/threshold-coapproval.yaml)
   - [`transactions/suspension-restoration.yaml`](./transactions/suspension-restoration.yaml)
5. [`transaction-evidence-closure.md`](./transaction-evidence-closure.md) consolidates the construction results.
6. [`post-construction-rahp.yaml`](./post-construction-rahp.yaml) records the second RAHP pass after construction.
7. [`pressure-test.yaml`](./pressure-test.yaml) contains only the four residual findings that survived construction and satisfy the formal RAHP finding/evidence contract.

Maintainer discussion and disposition are tracked in [GitHub Discussion #51](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/51); this directory retains only reproducible assessment and evidence artifacts.

## What changed after construction

The initial hypothesis was deliberately broad. Source review already showed that DTG contains substantial reusable machinery for scoped authority, expiry, revocation, proof attribution, audience/context binding and source authorization.

The three evidence-closure cases narrow the problem further:

- **Routine bounded authority:** constructible with current mechanics; remaining work is profile semantics for appointment source, action scope, current state, minimization and non-inference.
- **Threshold/co-approval:** Trust Tasks already has strong approval patterns, including authorized approvers, challenge binding, single-use consumption, scope and expiry. The residual is a reusable threshold composition contract, not a missing approval primitive.
- **Suspension/restoration:** grant/revoke/expiry mechanics exist. The residual is lifecycle vocabulary, precedence, effective time, authoritative-state discovery and restoration semantics across artifacts.

The post-construction RAHP retest therefore reduces ten initial candidate findings to four evidence-backed residuals.

## Surviving residuals

| Residual | Classification | Result |
| --- | --- | --- |
| Constrained-authority composition | Cross-spec profile | Appointment, current state, action scope and transaction permission need a common composition contract. |
| Threshold/co-approval composition | Cross-spec / Trust Task profile | Existing approval building blocks need common decision binding, threshold semantics and private threshold satisfaction. |
| Lifecycle precedence and restoration | Governance profile with specification hooks | Suspension, supersession, restoration and effective-time precedence need explicit semantics across artifacts. |
| Privacy and governance boundary | Privacy profile + governance/assurance | Private proof inputs remain to be demonstrated upstream; retained agency and fiduciary propriety must not be inferred from proof validity. |

No construction demonstrates a need for a new generic base Credential, Trust Task approval, or revocation primitive.

## Evidence-closure rule

For a constrained-authority decision, the example requires:

1. the decision or harm-relevant claim;
2. the predicates required to justify it;
3. the authoritative source and lifecycle state for each predicate;
4. the composition rule connecting those predicates to the decision;
5. privacy constraints on the presentation;
6. retained governance judgment and redress obligations; and
7. evidence sufficient to disposition any residual finding.

Cryptographic verification of all component artifacts is not, by itself, evidence closure.

## Non-inference boundary

The central boundary survives every construction:

`appointment = valid` does not imply `transaction = permitted`.

Likewise, proof that a representative is authorized does not by itself establish that the principal lacks capacity or retained authority, that conflicts are absent, or that fiduciary duties, proportionality, best-interest or least-restrictive requirements were satisfied.

## Next gate

The technical construction pass and RAHP retest are complete. The next gate is **maintainer disposition in Discussion #51**.

No downstream DTG issue should be opened automatically. A residual should become downstream work only when maintainers agree that it is concrete, owned and actionable, with a clear completion condition.

## Intended use

The pattern extends beyond guardianship to trustees, attorneys-in-fact, executors, organizational representatives, regulated fiduciaries, delegated agents and similar relationships where **being authorized** and **acting permissibly under that authority** are distinct propositions.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `XSP-GF-001` |
| Status | complete |
| Title | Guardianship and fiduciary constrained-authority cross-spec pressure test |
| Reviewed on | 2026-08-23 |
| Target repository | `trustoverip/dtgwg-general` |
| Target version | cross-spec exploratory baseline 2026-08-23 |
| Target commit | `fa15044225ff447ad6564983a5ce0732b80cbdc1` |
| Target source paths | `README.md` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.5.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Preserve exploratory hypotheses, construct concrete evidence closures using current primitives first, then promote only residuals that survive the post-construction RAHP retest. |

### Review scope

**Included**

- cross-spec constrained-authority composition
- credential authority and lifecycle semantics
- transaction-bound evidence and approval composition
- privacy-preserving authority and relationship predicates
- retained agency, oversight, restoration and redress boundaries

**Excluded**

- jurisdiction-specific legal advice
- selection of a specific proof construction
- automatic creation of downstream DTG issues

### Summary

| Measure | Value |
|---|---:|
| Findings | 4 |
| Open findings | 4 |
| Primary disposition: Implementation Guidance | 1 |
| Primary disposition: Specification | 2 |
| Primary disposition: Governance | 1 |

**Overall assessment**

Three concrete evidence closures show that DTG already has substantial mechanics for proof, scoped authority, expiry, approval, challenge/replay resistance and revocation. Ten initial candidate findings collapse to four narrower residuals: constrained-authority composition, threshold/co-approval composition, lifecycle precedence/restoration, and the privacy/governance boundary. No case demonstrates a missing generic base Credential, Trust Task approval or revocation primitive.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Constrained-authority decisions lack a common cross-spec composition profile | High | open | Implementation Guidance | [CRK-14 — Trust-registry identity binding failure](/rahp-toolkit/docs/cawg-risk-register.html#crk-14) |
| `F-002` | Threshold and co-approval evidence lacks a reusable constrained-authority composition contract | High | open | Specification | [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| `F-003` | Suspension, supersession and restoration lack cross-artifact lifecycle precedence semantics | High | open | Specification | [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| `F-004` | Private authorization evidence must not collapse retained agency or fiduciary propriety into proof validity | High | open | Governance | [CRK-19 — Selective-disclosure correlation leakage](/rahp-toolkit/docs/cawg-risk-register.html#crk-19), [CRK-15 — Registry and governing-authority availability dependency](/rahp-toolkit/docs/cawg-risk-register.html#crk-15) |

### Detailed findings

#### F-001 — Constrained-authority decisions lack a common cross-spec composition profile

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Implementation Guidance |
| Secondary dispositions | Specification, Governance |
| Scenarios | — |
| Scenario patterns | — |
| Personas | — |
| Risks | [CRK-14 — Trust-registry identity binding failure](/rahp-toolkit/docs/cawg-risk-register.html#crk-14) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-INF-01`, `HRM-SEC-02` |
| Risks | `RKP-AUTH-01`, `RKP-COMP-02` |
| Controls | `CTP-AUTH-01`, `CTP-DISC-01` |
| Guardrails | `GRP-AUTH-01` |
| Assurance | `ATP-AUTH-01` |
| Evidence | `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `examples/cross-spec/guardianship-fiduciary/transactions/routine-act.yaml` | Routine authority can be constructed from current Credential and Trust Task mechanics only when a profile supplies appointment-source, action-scope, current-state and non-inference semantics. |
| `trustoverip/dtgwg-cred-spec@b89f389abbdae77ba60b673c0836c781c2b54169:spec/body.md` | Credential validity, taskContext, issuer authorization and relationship-proof mechanisms exist, but they do not define guardianship/fiduciary transaction permission. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/acl/grant/0.1/spec.md` | Scoped and expiring grants with authoritative post-state exist, while role and scope semantics are intentionally opaque to the framework. |

**Potential harm**

A verifier can either over-read a valid appointment as permission for the specific act or require excessive bespoke evidence because the propositions connecting appointment, scope, current state and transaction permission are not composed consistently.

**Recommended treatment**

Define a constrained-authority cross-spec profile that names authoritative source classes, separates appointment from transaction permission, maps action/domain scope, requires transaction-time state evaluation and carries explicit non-inference/minimal-disclosure rules.

**Retest when**

- a constrained-authority composition profile or equivalent cross-spec contract is published

#### F-002 — Threshold and co-approval evidence lacks a reusable constrained-authority composition contract

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Specification |
| Secondary dispositions | Implementation Guidance |
| Scenarios | — |
| Scenario patterns | — |
| Personas | — |
| Risks | [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-INF-01`, `HRM-SEC-02` |
| Risks | `RKP-AUTH-02`, `RKP-COMP-02` |
| Controls | `CTP-AUTH-02` |
| Guardrails | `GRP-AUTH-02` |
| Assurance | `ATP-AUTH-01` |
| Evidence | `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `examples/cross-spec/guardianship-fiduciary/transactions/threshold-coapproval.yaml` | Existing Trust Task approval patterns provide authenticated approvers, challenge matching, single-use consumption, scope and expiry, but do not define generic N-of-M/joint/sequential constrained-authority composition. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/consent/decision/1.0/spec.md` | A signed approval can be bound to a pending challenge and consumed single-use after authorization of the approver. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/consent/approver-set/1.0/spec.md` | Trust Tasks already demonstrates an admin-gated authoritative approver binding pattern. |

**Potential harm**

Independently valid approvals can be combined across different transaction versions, stale approver sets or incompatible threshold rules, or implementations may disclose the full representative graph merely to prove that the threshold was met.

**Recommended treatment**

Specify a reusable constrained-authority approval profile with a canonical decision object, threshold-policy semantics, authoritative/fresh approver-set state, common freshness rules and a privacy-preserving threshold-satisfaction interface.

**Retest when**

- a generic threshold/co-approval profile is defined or existing approval tasks gain equivalent composition semantics

#### F-003 — Suspension, supersession and restoration lack cross-artifact lifecycle precedence semantics

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Specification |
| Secondary dispositions | Governance, Implementation Guidance |
| Scenarios | — |
| Scenario patterns | — |
| Personas | — |
| Risks | [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-INF-01`, `HRM-GOV-02` |
| Risks | `RKP-AUTH-02`, `RKP-CRD-02`, `RKP-COMP-02` |
| Controls | `CTP-AUTH-02`, `CTP-DISC-02` |
| Guardrails | `GRP-AUTH-02` |
| Assurance | `ATP-AUTH-01` |
| Evidence | `EVP-AUTH-01`, `EVP-RED-01` |

**Evidence**

| Source | Observation |
|---|---|
| `examples/cross-spec/guardianship-fiduciary/transactions/suspension-restoration.yaml` | Credential validity plus ACL revoke/grant mechanics close removal, scope reduction and re-grant mechanics but do not determine lifecycle precedence or legal meaning across artifacts. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/acl/revoke/0.1/spec.md` | Full removal and scope reduction produce attributable evidentiary records and canonical resulting state. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/acl/grant/0.1/spec.md` | Grants can expire and are recoverable via re-grant, but the generic framework does not define constrained-authority restoration versus new appointment. |

**Potential harm**

A stale yet cryptographically valid authority or approval artifact can dominate a later suspension/restoration event, or a legitimate principal/representative can remain blocked because implementations disagree about which lifecycle event controls at decision time.

**Recommended treatment**

Define constrained-authority lifecycle vocabulary, effective-time and precedence rules, authoritative current-state discovery, approval freshness coupling, and explicit restoration versus replacement/new-appointment semantics.

**Retest when**

- lifecycle/status semantics define suspension, supersession, restoration and transaction-time precedence across composed evidence

#### F-004 — Private authorization evidence must not collapse retained agency or fiduciary propriety into proof validity

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Governance |
| Secondary dispositions | Specification, Implementation Guidance |
| Scenarios | — |
| Scenario patterns | — |
| Personas | — |
| Risks | [CRK-19 — Selective-disclosure correlation leakage](/rahp-toolkit/docs/cawg-risk-register.html#crk-19), [CRK-15 — Registry and governing-authority availability dependency](/rahp-toolkit/docs/cawg-risk-register.html#crk-15) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-PRV-02`, `HRM-GOV-02` |
| Risks | `RKP-PRV-01`, `RKP-GOV-04` |
| Controls | `CTP-PRV-01`, `CTP-GOV-03` |
| Guardrails | `GRP-PRV-01`, `GRP-RED-01` |
| Assurance | — |
| Evidence | `EVP-RED-01` |

**Evidence**

| Source | Observation |
|---|---|
| `examples/cross-spec/guardianship-fiduciary/transaction-evidence-closure.md` | All three constructions can authenticate authority-related evidence, but none makes fiduciary propriety, incapacity, retained agency or restoration a consequence of cryptographic validity. |
| `sankarshanmukhopadhyay/dtgwg-zkp-tf@6064c3428ca88471b5ec8271ec03e318c26d2a13:docs/implementation-guide/boundaries/composed-presentation-privacy.md` | The companion ZKP work requires privacy to be assessed across composed evidence and rejects correlation-prone hiding constructions, but this is not upstream adoption. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/acl/revoke/0.1/spec.md#authorization` | Trust Tasks explicitly separates proof of who asked from the consumer's authorization decision. |

**Potential harm**

A valid private proof of representative authority can become a durable incapacity signal, disclose sensitive relationship structure, or be treated as evidence that duties, conflicts, best-interest/proportionality rules or retained principal rights were satisfied.

**Recommended treatment**

Keep incapacity non-inference, retained/restored agency, conflicts and fiduciary propriety as explicit governance/assurance propositions. Where private proof is needed, define upstream predicate/input interfaces that reveal only the authority/current-state facts required by the decision and do not expose durable relationship correlators.

**Retest when**

- upstream privacy proof-input contracts and governance profiles define constrained-authority non-inference, retained agency and composed disclosure requirements

<!-- END GENERATED PRESSURE TEST -->
