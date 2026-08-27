# DTG Credential Specification × ZKP × Trust Tasks Framework v0.5.0 pressure test

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-CZT-001` |
| Status | complete |
| Title | DTG Credential Specification × ZKP × Trust Tasks Framework v0.5.0 pressure test |
| Reviewed on | 2026-08-27 |
| Target repository | `trustoverip/dtgwg-cred-spec + trustoverip/dtgwg-zkp-tf + trustoverip/dtgwg-trust-tasks-spec` |
| Target version | Credential Specification current main × ZKP current main × Trust Tasks Framework v0.5.0 |
| Target commit | `6425a74136c1d2dfa7115889abe0b3521700e887` |
| Target source paths | `corpora/credential-zkp-trust-tasks-composed.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.5.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | A pass at each pairwise seam does not imply a pass for the three-spec consequential flow. |

### Review scope

**Included**

- authority-composition
- privacy-composition
- lifecycle-and-freshness
- task-specific-proof-binding
- consequential-execution
- retained-evidence-correlation

**Excluded**

- Independent implementation defects not caused or amplified by composition.
- Deployment-specific behavior not evidenced by the source-pinned specifications.

### Summary

| Measure | Value |
|---|---:|
| Findings | 4 |
| Open findings | 4 |

**Overall assessment**

Component-level controls materially reduce several risks, but the complete Credential × ZKP × Trust Tasks consequential flow retains four cross-specification obligations that require explicit composition contracts or executable evidence before assurance can be raised.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Valid evidence does not establish current authority at consequential execution time | Critical | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| `F-002` | One-effect execution is not established by component validity | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| `F-003` | Task-specific proof commitment remains a three-spec composition obligation | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| `F-004` | Composed privacy can fail despite pairwise identifiers and zero-knowledge disclosure | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Valid evidence does not establish current authority at consequential execution time

| Field | Value |
|---|---|
| Severity | Critical |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Governance, Implementation Guidance |
| Scenarios | `XSP-CZT-001`, `XSP-CZT-003`, `XSP-CZT-007` |
| Scenario patterns | `SP-AUTH-02`, `SP-GOV-01`, `SP-COMP-01`, `SP-COMP-02` |
| Personas | [D1 — Daniel Wright](../../../build/site/catalogue.html#D1) |
| Risks | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-SEC-02`, `HRM-INF-01`, `HRM-AUT-04`, `HRM-GOV-02` |
| Risks | `RKP-COMP-01`, `RKP-AUTH-02` |
| Controls | `CTP-COMP-01`, `CTP-AUTH-02` |
| Guardrails | `GRP-COMP-01`, `GRP-AUTH-02` |
| Assurance | `ATP-COMP-01`, `ATP-AUTH-02` |
| Evidence | `EVP-COMP-01`, `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-001` | A valid credential and proof can remain acceptable while authoritative mandate state changes before a consequential task effect. |
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-003` | Proof freshness and task freshness do not establish credential or mandate freshness. |

**Potential harm**

A valid credential and ZK proof can be combined with a fresh Trust Task after delegated authority has been revoked, expired, superseded or narrowed if proof and task freshness are treated as substitutes for authoritative mandate state.

**Recommended treatment**

Define a reusable action-time authority decision contract binding principal, delegate, action, scope, constraints, credential/status evidence and current lifecycle state immediately before the side effect.

**Retest when**

- Negative vectors reject valid credential + valid proof + valid task after authority revocation, expiry, supersession or scope reduction.

#### F-002 — One-effect execution is not established by component validity

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Implementation Guidance, Governance |
| Scenarios | `XSP-CZT-004`, `XSP-CZT-005`, `XSP-CZT-007` |
| Scenario patterns | `SP-COMP-01`, `SP-OPS-01`, `SP-OPS-02`, `SP-REPLAY-01` |
| Personas | [D1 — Daniel Wright](../../../build/site/catalogue.html#D1) |
| Risks | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-SEC-02`, `HRM-INF-01`, `HRM-AUT-04`, `HRM-GOV-02` |
| Risks | `RKP-COMP-01`, `RKP-AUTH-02` |
| Controls | `CTP-COMP-01`, `CTP-AUTH-02` |
| Guardrails | `GRP-COMP-01`, `GRP-AUTH-02` |
| Assurance | `ATP-COMP-01`, `ATP-AUTH-02` |
| Evidence | `EVP-COMP-01`, `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-004` | Successful transport delivery does not establish successful task execution. |
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-005` | Duplicate consequential execution can occur even when reused credential and proof evidence remain valid. |

**Potential harm**

Delivery, proof verification and credential validity can all succeed while execution remains unknown or a duplicate retry creates a second consequential effect.

**Recommended treatment**

Bind the authoritative task instance, evidence set and outcome receipt to one logical effect, preserving Trust Tasks v0.5.0 lifecycle semantics and explicit idempotency/reconciliation behavior.

**Retest when**

- Lost-reply and duplicate vectors demonstrate exactly one logical effect and never infer execution from transport delivery or proof success.

#### F-003 — Task-specific proof commitment remains a three-spec composition obligation

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Implementation Guidance, Governance |
| Scenarios | `XSP-CZT-002`, `XSP-CZT-005`, `XSP-CZT-007` |
| Scenario patterns | `SP-PRIV-01`, `SP-REPLAY-01`, `SP-COMP-01` |
| Personas | [D1 — Daniel Wright](../../../build/site/catalogue.html#D1) |
| Risks | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-SEC-02`, `HRM-INF-01`, `HRM-AUT-04`, `HRM-GOV-02` |
| Risks | `RKP-COMP-01`, `RKP-AUTH-02` |
| Controls | `CTP-COMP-01`, `CTP-AUTH-02` |
| Guardrails | `GRP-COMP-01`, `GRP-AUTH-02` |
| Assurance | `ATP-COMP-01`, `ATP-AUTH-02` |
| Evidence | `EVP-COMP-01`, `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-002` | Privacy-preserving proof validity does not by itself establish binding to the intended task wrapper, purpose or audience. |
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-007` | Proof validity can be semantically upgraded into authorization or task completion if composition boundaries are not explicit. |

**Potential harm**

A privacy-preserving proof valid for one context can be replayed or semantically upgraded into another task if the transcript or companion evidence does not commit to the intended action, purpose, audience and freshness domain.

**Recommended treatment**

Define the minimum privacy-preserving task-context commitment and require cross-task/cross-audience negative vectors.

**Retest when**

- Proof reuse outside the committed task/action/purpose/audience boundary is deterministically rejected.

#### F-004 — Composed privacy can fail despite pairwise identifiers and zero-knowledge disclosure

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Governance, Implementation Guidance |
| Scenarios | `XSP-CZT-002`, `XSP-CZT-006` |
| Scenario patterns | `SP-PRIV-01`, `SP-PRIV-02`, `SP-COMP-01` |
| Personas | [D1 — Daniel Wright](../../../build/site/catalogue.html#D1) |
| Risks | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-SEC-02`, `HRM-INF-01`, `HRM-AUT-04`, `HRM-GOV-02` |
| Risks | `RKP-COMP-01`, `RKP-AUTH-02` |
| Controls | `CTP-COMP-01`, `CTP-AUTH-02` |
| Guardrails | `GRP-COMP-01`, `GRP-AUTH-02` |
| Assurance | `ATP-COMP-01`, `ATP-AUTH-02` |
| Evidence | `EVP-COMP-01`, `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-002` | A private credential proof can still be wrapped in task-level metadata that creates a broader correlation surface. |
| `corpora/credential-zkp-trust-tasks-composed.yaml#xsp-czt-006` | Pairwise parties can remain correlatable through ceremony metadata or retained protocol evidence. |

**Potential harm**

Pairwise issuer/recipient identifiers and selective disclosure can coexist with linkability through ceremony enactment, timestamps, retained task documents, status lookups or outcome evidence.

**Recommended treatment**

Evaluate declared, observable and effective correlation scope over the complete retained interaction, including task wrapper, proof transcript, credential/status evidence, ceremony metadata and outcome records.

**Retest when**

- Composed privacy vectors demonstrate that two unrelated relying contexts cannot correlate the same subject or relationship from retained protocol-visible evidence beyond the explicitly declared scope.

<!-- END GENERATED PRESSURE TEST -->
