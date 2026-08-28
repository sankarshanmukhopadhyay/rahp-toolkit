# Collusion and cartel-formation false-independence pressure test

This worked example promotes the COLLUSION proposition from issues #167, #193 and #210 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-006` |
| Status | complete |
| Title | DTG collusion and cartel-formation false-independence pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 167, 193 and 210 |
| Target commit | `8b17e9f39ba3be8de8b35e9012d3508f7e0ebd68` |
| Target source paths | `examples/cross-spec/collusion/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Actor distinctness and decision or evidence independence are separate propositions. Established coordination may defeat independence credit where relying policy expects independent judgment; agreement, shared interest or disclosed coalition action alone does not establish collusion. |

### Review scope

**Included**

- coordinated-cross-endorsement
- cartelized-exclusion
- pre-arranged-threshold-approval
- collusive-negative-attestations
- aligned-interest-without-observed-coordination
- genuinely-independent-agreement
- legitimate-disclosed-coalition
- unknown-coordination

**Excluded**

- A rule that agreement among multiple actors is inherently suspicious.
- A rule that shared strategic interest alone proves collusion.
- A universal collusion-detection mechanism.
- A replacement for the separate Sybil, false-diversity or quorum-capture cases.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express collusion as a false-independence failure where genuinely distinct actors coordinate to manufacture corroboration, exclusion or approval. The remaining cross-specification challenge is obtaining sufficient, privacy-respecting evidence about coordination without treating agreement or shared incentives as misconduct by default.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Distinct actors can coordinate to manufacture apparent independent corroboration | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Distinct actors can coordinate to manufacture apparent independent corroboration

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Companion Specification |
| Secondary dispositions | Governance, Implementation Guidance |
| Scenarios | — |
| Scenario patterns | `SP-COMP-01` |
| Personas | [D1 — Daniel Wright](../../../build/site/catalogue.html#D1) |
| Risks | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-GOV-02` |
| Risks | `RKP-COMP-01` |
| Controls | `CTP-COMP-01` |
| Guardrails | `GRP-COMP-01` |
| Assurance | `ATP-COMP-01` |
| Evidence | `EVP-COMP-01` |

**Evidence**

| Source | Observation |
|---|---|
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/167` | The source issue distinguishes collusion from Sybil and false-diversity cases: genuinely distinct actors may coordinate endorsements, exclusions, attestations or approvals. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The false-independence register records COLLUSION as the case in which actor distinctness does not automatically establish independent corroboration. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/210` | The executable promotion records falsification boundaries for established coordination, aligned interests, genuine agreement, disclosed coalitions and unknown coordination. |

**Potential harm**

A relying decision can over-count coordinated evidence or governance actions as independent corroboration, allowing cartels to manufacture trust, distrust, exclusion or approval while satisfying nominal diversity requirements.

**Recommended treatment**

Where independence is material, represent actor distinctness, coordination evidence, strategic alignment and decision/evidence independence separately; reduce independence credit for established coordination without treating agreement or shared interest alone as collusion.

**Retest when**

- DTG Credentials, Communities, Relationships, Trust Tasks or governance surfaces provide executable semantics for coordination, coalition identity or independent-decision evidence.

<!-- END GENERATED PRESSURE TEST -->

