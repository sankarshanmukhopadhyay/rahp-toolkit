# Trust Tasks × DTG Credential Specification cross-specification example

This v1.5 worked example exercises the portable assurance catalogue against a **composition**, not a single specification. It uses the `XSP-*` corpus scenarios to show how portable `RKP-*`, `CTP-*`, `GRP-*`, `ATP-*` and `EVP-*` patterns can be applied while the deployment-specific DTG risk catalogue remains separate.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-001` |
| Status | complete |
| Title | Trust Tasks × DTG Credential Specification cross-specification pressure test |
| Reviewed on | 2026-08-23 |
| Target repository | `trustoverip/dtgwg-trust-tasks-tf + trustoverip/dtgwg-cred-spec` |
| Target version | Composition of Trust Tasks 4937c70d and Credentials b89f389a |
| Target commit | `4937c70df95e56ed6404b8c004106ecb121a23cf` |
| Target source paths | `Trust Tasks SPEC.md and VTA lifecycle specifications`, `DTG Credential Spec spec/body.md`, `corpora/trust-tasks-credspec-composed.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.5.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | 2026-08-23 |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | A component-level pass does not imply a composition-level pass. |

### Review scope

**Included**

- Authority and delegation at the Trust Task + credential seam.
- Execution/outcome binding, replay and idempotency.
- Lifecycle skew across task, credential, registry and policy state.
- Privacy composition across task, credential, transport and error evidence.
- Cross-boundary redress and contestability.

**Excluded**

- Independent implementation defects not caused or amplified by specification composition.

### Summary

| Measure | Value |
|---|---:|
| Findings | 3 |
| Open findings | 3 |

**Overall assessment**

Current Trust Tasks and Credential Spec primitives are materially stronger than the earlier baseline, including ACL lifecycle, approval, adverse-decision evidence and VWC edge binding. The expanded source-pinned corpus nevertheless retains three narrower cross-spec seams: action-time authority/lifecycle coherence, decision/replay/evidence closure, and privacy/contestability across composed evidence.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Authority and lifecycle coherence remains a cross-specification assurance gap | Critical | open | Companion Specification | [RK-AI01 — Agent Credential Scope Creep](../../../build/site/catalogue.html#RK-AI01) |
| `F-002` | Execution, outcome binding and replay remain incompletely composed | High | open | Companion Specification | [RK-EX05 — Organisational Identity Architecture Gap](../../../build/site/catalogue.html#RK-EX05) |
| `F-003` | Privacy composition and contestability remain cross-boundary governance obligations | High | open | Governance | [RK-EX05 — Organisational Identity Architecture Gap](../../../build/site/catalogue.html#RK-EX05) |

### Detailed findings

#### F-001 — Authority and lifecycle coherence remains a cross-specification assurance gap

| Field | Value |
|---|---|
| Severity | Critical |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Governance, Implementation Guidance |
| Scenarios | `XSP-002`, `XSP-007`, `XSP-009`, `XSP-010`, `XSP-013`, `XSP-014`, `XSP-016`, `XSP-019`, `XSP-020` |
| Scenario patterns | `SP-AUTH-02`, `SP-DEL-01`, `SP-DEL-02`, `SP-OPS-01`, `SP-OPS-02`, `SP-COMP-02` |
| Personas | [P1 — Principal / Rights-Bearing Party](../../../build/site/catalogue.html#P1), [P3 — Relying Party / Verifier](../../../build/site/catalogue.html#P3), [P5 — Delegated Service / Agent Operator](../../../build/site/catalogue.html#P5), [P6 — Registry / Discovery / Trust-Service Operator](../../../build/site/catalogue.html#P6) |
| Risks | [RK-AI01 — Agent Credential Scope Creep](../../../build/site/catalogue.html#RK-AI01) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-AUT-04`, `HRM-SEC-02`, `HRM-INF-01`, `HRM-AUT-05` |
| Risks | `RKP-COMP-01`, `RKP-AUTH-02`, `RKP-COMP-02` |
| Controls | `CTP-COMP-01`, `CTP-AUTH-02`, `CTP-COMP-02` |
| Guardrails | `GRP-COMP-01`, `GRP-AUTH-02` |
| Assurance | `ATP-COMP-01`, `ATP-AUTH-02`, `ATP-COMP-02` |
| Evidence | `EVP-COMP-01`, `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `instances/dtg/reviews/2026-08-trust-tasks.md` | Trust Tasks through 2a40f6bd explicitly separates proof from role/scope authorization and strengthens lifecycle semantics, but does not define a universal cross-system delegation model or synchronized credential/status policy. |
| `corpora/trust-tasks-credspec-composed.yaml#xsp-002` | Individually valid task and credential facts can still be combined beyond a principal's current mandate unless delegated authority is evaluated at action time. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/acl/grant/0.1/spec.md` | Current Trust Tasks supplies scoped, expiring and authoritative ACL post-state mechanics, but role/scope semantics remain profile-defined and cross-artifact authority must still be evaluated at action time. |
| `corpora/trust-tasks-credspec-composed.yaml#xsp-013-xsp-020` | Expanded seam cases show authority revocation, restoration, removal and fiduciary non-inference can diverge across otherwise valid task and credential evidence. |

**Potential harm**

A consumer can execute a consequential task using valid component evidence while relying on stale, revoked or out-of-scope delegated authority, especially when credential, registry and task lifecycle views diverge.

**Recommended treatment**

Define the narrowest cross-spec authority/lifecycle profile needed to align current task authority, credential/governance state, effective-time precedence and non-inference at consequential action time; reuse existing ACL/credential primitives rather than adding a parallel base authority object.

**Retest when**

- A companion profile or normative specification defines current delegated-authority verification across Trust Tasks and credentials.
- The profile defines lifecycle synchronization, offline status-as-of semantics and safe degradation.

#### F-002 — Execution, outcome binding and replay remain incompletely composed

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Implementation Guidance |
| Scenarios | `XSP-001`, `XSP-003`, `XSP-014`, `XSP-015`, `XSP-017` |
| Scenario patterns | `SP-COMP-01`, `SP-REPLAY-01` |
| Personas | [P1 — Principal / Rights-Bearing Party](../../../build/site/catalogue.html#P1), [P3 — Relying Party / Verifier](../../../build/site/catalogue.html#P3), [P5 — Delegated Service / Agent Operator](../../../build/site/catalogue.html#P5), [P6 — Registry / Discovery / Trust-Service Operator](../../../build/site/catalogue.html#P6) |
| Risks | [RK-EX05 — Organisational Identity Architecture Gap](../../../build/site/catalogue.html#RK-EX05) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-INF-01`, `HRM-SEC-02`, `HRM-ECO-02` |
| Risks | `RKP-CRD-03`, `RKP-OPS-02` |
| Controls | `CTP-CRD-01`, `CTP-OPS-02` |
| Guardrails | `GRP-OPS-01` |
| Assurance | `ATP-COMP-01`, `ATP-OPS-02` |
| Evidence | `EVP-COMP-01`, `EVP-OPS-02` |

**Evidence**

| Source | Observation |
|---|---|
| `https://github.com/trustoverip/dtgwg-cred-spec/commit/b89f389abbdae77ba60b673c0836c781c2b54169` | The VWC digest is now required and strengthens edge binding, but it does not itself prove task completion or one-time execution. |
| `corpora/trust-tasks-credspec-composed.yaml#xsp-003` | A valid credential and valid task can still be replayed together unless the composition binds freshness, task identity, credential use and side-effect execution. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/consent/decision/1.0/spec.md` | Current consent decisions provide stronger challenge binding, authorization and consumption semantics, weakening any claim that Trust Tasks lacks approval machinery. |
| `trustoverip/dtgwg-cred-spec@b89f389abbdae77ba60b673c0836c781c2b54169:spec/body.md` | VWC digest binding now requires the referenced VRC to identify the witnessed edge, sharpening the evidence-closure boundary rather than eliminating it. |
| `corpora/trust-tasks-credspec-composed.yaml#xsp-015-xsp-017` | Residual composition concerns are mixed-version quorum/decision binding and incomplete referenced evidence, not absence of generic approval or integrity primitives. |

**Potential harm**

A credential can be correctly bound to an edge yet still be misinterpreted as proof of successful task completion, or reused with a duplicate consequential task to repeat an effect authorized only once.

**Recommended treatment**

Retain task-level replay and outcome controls, but define reusable decision/evidence-closure composition rules for canonical transaction binding, threshold policy, authoritative approver state, freshness and referenced credential evidence.

**Retest when**

- A normative profile defines outcome evidence and one-time or idempotent execution binding across the two specifications.

#### F-003 — Privacy composition and contestability remain cross-boundary governance obligations

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Governance |
| Secondary dispositions | Companion Specification, Implementation Guidance |
| Scenarios | `XSP-005`, `XSP-006`, `XSP-011`, `XSP-012`, `XSP-016`, `XSP-018`, `XSP-020` |
| Scenario patterns | `SP-PRIV-01`, `SP-PRIV-02`, `SP-COMP-01`, `SP-GOV-03`, `SP-RED-01` |
| Personas | [P1 — Principal / Rights-Bearing Party](../../../build/site/catalogue.html#P1), [P3 — Relying Party / Verifier](../../../build/site/catalogue.html#P3), [P5 — Delegated Service / Agent Operator](../../../build/site/catalogue.html#P5), [P6 — Registry / Discovery / Trust-Service Operator](../../../build/site/catalogue.html#P6) |
| Risks | [RK-EX05 — Organisational Identity Architecture Gap](../../../build/site/catalogue.html#RK-EX05) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-PRV-02`, `HRM-PRV-05`, `HRM-GOV-02`, `HRM-ECO-02` |
| Risks | `RKP-COMP-03`, `RKP-GOV-04` |
| Controls | `CTP-PRV-02`, `CTP-GOV-03` |
| Guardrails | `GRP-PRV-01`, `GRP-RED-01` |
| Assurance | `ATP-PRV-01`, `ATP-RED-01` |
| Evidence | `EVP-PRV-01`, `EVP-RED-01` |

**Evidence**

| Source | Observation |
|---|---|
| `instances/dtg/reviews/2026-08-trust-tasks.md` | New VTA lifecycle and HTTPS discovery surfaces improve explicitness but add observable artifacts whose combined privacy impact is not bounded by either component specification alone. |
| `corpora/trust-tasks-credspec-composed.yaml#xsp-012` | Adverse outcomes can still span task policy, credential status and registry governance without a single accountable contestability boundary. |
| `trustoverip/dtgwg-trust-tasks-tf@4937c70df95e56ed6404b8c004106ecb121a23cf:specs/vtc/members/removal-notice/0.1/spec.md` | The new removal notice materially improves adverse-decision evidence and appealability, narrowing but not eliminating cross-system redress obligations. |
| `corpora/trust-tasks-credspec-composed.yaml#xsp-018-xsp-020` | Composed status lookup/task metadata can still create correlation, and technical authorization evidence must not be over-read as retained-agency or fiduciary-propriety proof. |

**Potential harm**

Individually minimal proofs, task identifiers, endpoint metadata, status checks, errors and retained evidence can compose into durable correlation, while an affected person may lack a single evidence package and accountable path for contesting a cross-spec decision.

**Recommended treatment**

Define privacy and contestability requirements across the complete evidence closure: minimize stable correlation surfaces, retain portable adverse-decision evidence, and preserve explicit non-inference between authorization proof and broader governance judgments.

**Retest when**

- A privacy profile bounds disclosure and correlation across the composed exchange.
- A governance profile defines the accountable decision owner, evidence package and contest/remedy path.

<!-- END GENERATED PRESSURE TEST -->

