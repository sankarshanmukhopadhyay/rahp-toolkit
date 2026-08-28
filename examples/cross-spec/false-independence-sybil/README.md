# False-independence / Sybil composition pressure test

This worked example promotes the adversarial-independence proposition from issues #158, #193 and #198 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-001` |
| Status | complete |
| Title | DTG false-independence / Sybil composition pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 158, 193 and 198 |
| Target commit | `726dd14defb0b647a52aea1c8859af2dd2afeb8b` |
| Target source paths | `examples/cross-spec/false-independence-sybil/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Multiplicity is not evidence of independence; independence must be established at the assurance level relied upon by policy. |

### Review scope

**Included**

- common-control-multiplicity
- genuinely-independent-corroboration
- legitimate-contextual-identifiers
- context-specific-uniqueness
- unknown-independence

**Excluded**

- Universal proof-of-personhood requirements.
- A universal identifier or cross-context subject correlator.
- Claims that zero-knowledge proof alone establishes Sybil resistance.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express the false-independence invariant without equating identifier plurality with attack behavior. The remaining assurance gap is evidence sufficient to establish effective independence in a given relying policy.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Apparent multiplicity can be over-read as independent corroboration | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Apparent multiplicity can be over-read as independent corroboration

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
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/158` | The source proposition explicitly distinguishes identity multiplicity from trust multiplicity and requires independent evidentiary provenance before assurance amplification. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The evidence register generalizes the threat family across Sybil, sock-puppet, false-diversity, trust-laundering, collusion, quorum-capture and selective-evidence cases. |

**Potential harm**

A relying decision can grant disproportionate authority, eligibility, reputation, governance weight or trust when many controlled identities, issuers, communities or attestations are mistaken for independent corroboration.

**Recommended treatment**

Require relying policy to treat multiplicity and independence as separate propositions, preserve uncertainty when effective control cannot be established, and avoid universal correlation as an anti-Sybil shortcut.

**Retest when**

- A DTG composition provides executable independence evidence and privacy-preserving contextual uniqueness controls for the relevant relying decision.

<!-- END GENERATED PRESSURE TEST -->
