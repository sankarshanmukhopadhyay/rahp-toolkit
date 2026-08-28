# Trust-laundering composition pressure test

This worked example promotes the TRUST-LAUNDERING proposition from issues #159, #193 and #201 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-003` |
| Status | complete |
| Title | DTG trust-laundering composition pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 159, 193 and 201 |
| Target commit | `941eb03909d1eb269afc11124ec91752f1a8a94a` |
| Target source paths | `examples/cross-spec/trust-laundering/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Provenance depth is traceability, not assurance depth; uplift requires materially new evidence and independence appropriate to the relying policy. |

### Review scope

**Included**

- affiliated-reissuance
- circular-reattestation
- multiple-artifact-forms-one-source
- intermediary-wrapping-lineage-preserved
- genuinely-new-independent-corroboration
- unknown-or-obscured-lineage

**Excluded**

- A prohibition on derived credentials, endorsements or trust chains.
- A rule that transformed evidence can never gain assurance.
- Universal numeric assurance arithmetic across specifications.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express trust laundering as unjustified assurance amplification while preserving legitimate derivation and endorsement. The remaining cross-specification requirement is sufficient lineage and evidence-grade semantics for a relying policy to distinguish transformation from new evidence.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Evidence transformation can be mistaken for independent assurance | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Evidence transformation can be mistaken for independent assurance

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
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/159` | The source proposition identifies re-issuance, wrapping, circular re-attestation and intermediary endorsement as possible assurance-laundering paths when no genuinely independent evidence is introduced. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The false-independence register distinguishes evidence lineage from evidence independence and records TRUST-LAUNDERING as a first-class threat class. |

**Potential harm**

A relying decision can gain false confidence when one weak, conflicted or common-source proposition is represented through several credentials, relationships, communities or intermediaries and the resulting provenance depth is mistaken for independent corroboration.

**Recommended treatment**

Require composed trust artifacts to preserve sufficient lineage and evidence-grade semantics to distinguish transformation from materially new evidence, detect circular or common-source provenance, and preserve bounded uncertainty when lineage is unavailable.

**Retest when**

- DTG Credentials, Relationships, Communities or Trust Tasks provide executable lineage and evidence-grade semantics sufficient to distinguish transformed evidence from materially new independent evidence.

<!-- END GENERATED PRESSURE TEST -->

