# False governance-diversity composition pressure test

This worked example promotes the FALSE-DIVERSITY proposition from issues #160 and #193 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-002` |
| Status | complete |
| Title | DTG false governance-diversity composition pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 160 and 193 |
| Target commit | `29eff9bef26ce7ceeb7766f78b81f7954a7cd588` |
| Target source paths | `examples/cross-spec/false-governance-diversity/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Nominal source count is not evidence of governance independence; the relying policy must evaluate the control or policy authority relevant to the assurance claim. |

### Review scope

**Included**

- nominal-issuer-diversity-common-controller
- branded-community-diversity-common-policy-authority
- operational-separation-common-decisive-root
- genuinely-independent-governance-roots
- unknown-governance-dependence

**Excluded**

- Claims that organizational centralization is inherently a failure.
- A requirement that every relying decision use multiple governance roots.
- Universal proof that two organizations can never coordinate or collude.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express false governance diversity without treating centralization itself as a defect. The unresolved assurance question is whether the relying policy has evidence sufficient to establish the independence of the governance roots it intends to count.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Nominal trust-root diversity can conceal common decisive governance control | High | open | Governance | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Nominal trust-root diversity can conceal common decisive governance control

| Field | Value |
|---|---|
| Severity | High |
| Status | open |
| Primary disposition | Governance |
| Secondary dispositions | Companion Specification, Implementation Guidance |
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
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/160` | The source proposition requires nominal diversity to be distinguished from governance independence where issuers, communities, registries or roots share effective control or policy authority. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The evidence register requires many issuers to be distinguished from many governance roots and treats FALSE-DIVERSITY as a first-class false-independence threat. |

**Potential harm**

A relying decision can overstate decentralization, corroboration or legitimacy when several nominal sources are counted as independent even though materially decisive authority remains concentrated in one effective governance domain.

**Recommended treatment**

Require relying policy to separate nominal source diversity, operational separation and governance independence; identify the authority material to the decision; withhold diversity uplift under common decisive control; and preserve bounded uncertainty when dependence cannot be established.

**Retest when**

- A DTG composition provides executable evidence about governance-root control, delegated authority or policy dependence for the relevant relying decision.

<!-- END GENERATED PRESSURE TEST -->

