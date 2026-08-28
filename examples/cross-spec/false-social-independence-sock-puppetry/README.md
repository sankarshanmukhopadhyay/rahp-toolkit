# Sock-puppetry false social independence pressure test

This worked example promotes the SOCK-PUPPET proposition from issues #166, #193 and #206 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-004` |
| Status | complete |
| Title | DTG sock-puppetry false social independence pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 166, 193 and 206 |
| Target commit | `106cd1c74eef441a4785ebdf369c7a463016ead1` |
| Target source paths | `examples/cross-spec/false-social-independence-sock-puppetry/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Social multiplicity is not evidence of social independence; independence credit requires evidence appropriate to the relying policy. |

### Review scope

**Included**

- manufactured-endorsement-cluster
- apparent-community-consensus
- coordinated-negative-attestations
- cross-community-sock-puppetry
- genuinely-independent-social-support
- legitimate-multi-persona-use
- unknown-controller-independence

**Excluded**

- A prohibition on pseudonymity, pairwise identifiers or contextual personas.
- A universal person-to-identity uniqueness requirement.
- A claim that all repeated social evidence is deceptive.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express sock-puppetry as deceptive manufacture of social independence while preserving legitimate persona separation. The remaining cross-specification challenge is how relying policy can observe or bound effective-control independence without imposing privacy-harmful universal correlation.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Persona multiplicity can be mistaken for independent social corroboration | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Persona multiplicity can be mistaken for independent social corroboration

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
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/166` | The source issue distinguishes sock puppetry from Sybil resistance by focusing on false social independence rather than identity multiplication alone. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The false-independence register requires apparent multiplicity, consensus and corroboration to remain distinct from genuine independence. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/206` | The executable promotion records the seven falsification and counter-cases, including the privacy-preserving multi-persona boundary. |

**Potential harm**

A relying decision can gain false confidence, false distrust or false consensus when one controller generates multiple social signals that appear to originate from separate actors or communities.

**Recommended treatment**

Require relying policy to distinguish persona-level signals from effective-controller independence where that distinction is material, avoid treating cross-community or signature multiplicity as proof of independence, preserve bounded uncertainty when independence is unknown, and avoid privacy-harmful universal correlation.

**Retest when**

- DTG Credentials, Relationships, Communities or Trust Tasks provide executable semantics for controller-independence evidence or privacy-preserving anti-amplification controls.

<!-- END GENERATED PRESSURE TEST -->

