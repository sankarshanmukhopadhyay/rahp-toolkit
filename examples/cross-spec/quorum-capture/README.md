# Quorum-capture and threshold-manipulation pressure test

This worked example promotes the QUORUM-CAPTURE proposition from issues #178, #193 and #208 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-005` |
| Status | complete |
| Title | DTG quorum-capture and threshold-manipulation pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 178, 193 and 208 |
| Target commit | `2160132bc7583971bddacd6b86491b30a6b9f094` |
| Target source paths | `examples/cross-spec/quorum-capture/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Threshold arithmetic establishes numeric satisfaction only; relying policy must separately evaluate the independence, eligibility, representativeness, weighting and current governance state that give the threshold meaning. |

### Review scope

**Included**

- captured-three-of-five
- duplicate-influence-across-roles
- lifecycle-denominator-change
- coordinated-abstention
- hidden-weighting
- genuinely-independent-threshold-approval
- unknown-independence-or-eligibility

**Excluded**

- A prohibition on threshold or quorum governance.
- A rule that abstention is inherently illegitimate.
- A rule that weighted voting is inherently illegitimate.
- A universal voting-system or constitutional-governance specification.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express quorum capture as a false-independence failure in which a numerically satisfied approval rule is over-read as independent, representative or legitimate consensus. The remaining cross-specification requirement is sufficient semantics for eligibility, control, weighting and governance-rule lifecycle to be evaluated alongside threshold arithmetic.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Numeric threshold satisfaction can conceal captured or stale governance | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Numeric threshold satisfaction can conceal captured or stale governance

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
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/178` | The source issue identifies threshold satisfaction under common control, duplicate roles, lifecycle changes and coordinated abstention as cases where arithmetic quorum can be over-read as legitimacy. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The false-independence register records QUORUM-CAPTURE as the case in which satisfying N-of-M does not automatically establish independent or legitimate approval. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/208` | The executable promotion records falsification and counter-cases for common control, role duplication, lifecycle, abstention, weighting, genuine independent quorum and unknown independence. |

**Potential harm**

A relying decision can treat captured, non-representative or stale approval as legitimate governance merely because the configured threshold is numerically satisfied.

**Recommended treatment**

Evaluate threshold satisfaction together with current participant eligibility, effective control, role occupancy, weighting, attendance semantics and governance-rule version where those properties are material to the relying policy.

**Retest when**

- DTG governance, Communities, Relationships or Trust Tasks provide executable quorum semantics including eligibility, weighting, lifecycle and independence evidence.

<!-- END GENERATED PRESSURE TEST -->

