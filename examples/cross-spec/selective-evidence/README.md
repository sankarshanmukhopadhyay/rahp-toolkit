# Selective-evidence incompleteness pressure test

This worked example promotes the SELECTIVE-EVIDENCE proposition from issues #176, #193 and #212 into an executable RAHP pressure-test fixture. The YAML record is canonical; the generated section below is maintained by `tools/render_pressure_tests.py`.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-XSP-FI-007` |
| Status | complete |
| Title | DTG selective-evidence incompleteness pressure test |
| Reviewed on | 2026-08-28 |
| Target repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| Target version | pre-specification evidence model from issues 176, 193 and 212 |
| Target commit | `aeae87ab99d95459209dfa7782b1ee6954e89a8c` |
| Target source paths | `examples/cross-spec/selective-evidence/pressure-test.yaml` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v1.8.0` |
| Engine contract | `rahp-engine-contract-v1` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/cross-spec-pressure-testing.md` |
| Rule | Artifact validity and evidence completeness are separate propositions. Completeness is evaluated relative to the relying proposition and the materiality of omitted contradictory, superseding, provenance or lifecycle context; irrelevant information may remain undisclosed. |

### Review scope

**Included**

- valid-but-stale-credential
- contradictory-attestations-cherry-picked
- derived-claim-with-omitted-source-limitation
- selective-relationship-history
- legitimate-selective-disclosure
- privacy-sensitive-contradiction-handling
- unknown-completeness
- complete-relevant-disclosure

**Excluded**

- A requirement for maximal disclosure of all provenance or history.
- A rule that selective disclosure is inherently deceptive.
- A universal contradiction-discovery or provenance-indexing mechanism.
- A requirement to reveal privacy-sensitive data that is immaterial to the relying proposition.

### Summary

| Measure | Value |
|---|---:|
| Findings | 1 |
| Open findings | 1 |

**Overall assessment**

RAHP can express selective-evidence failure as a material incompleteness problem rather than a validity failure. A presented credential, attestation, relationship fact or derived claim may be technically valid while the evidence set remains insufficient because material contradictory, superseding, provenance or lifecycle context is omitted. The remaining cross-specification need is proposition-aware completeness semantics that preserve privacy-respecting minimization.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Valid evidence can be materially incomplete for the relying proposition | High | open | Companion Specification | [RK-G01 — Genesis Policy Capture](../../../build/site/catalogue.html#RK-G01) |

### Detailed findings

#### F-001 — Valid evidence can be materially incomplete for the relying proposition

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
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/176` | The source issue identifies stale credentials, contradictory attestations, omitted source limitations and selective relationship history as cases where technically valid evidence may be misleadingly incomplete. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193` | The false-independence register records SELECTIVE-EVIDENCE as the case in which validity of a subset must not be mistaken for completeness of the evidence relevant to a relying decision. |
| `https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/212` | The executable promotion records the materiality boundary, legitimate minimization counter-case, unknown-completeness treatment and DPIP privacy boundary. |

**Potential harm**

A relying party can make an adverse or falsely reassuring decision from a technically valid but materially incomplete evidence set, including where contradictory, superseding or provenance-limiting context is omitted.

**Recommended treatment**

Evaluate evidence sufficiency separately from artifact validity. Where the relying proposition depends on current state, contradiction handling, provenance limitations or lifecycle history, require evidence appropriate to those propositions while preserving minimization of immaterial data.

**Retest when**

- DTG Credentials, Relationships, Communities or Trust Tasks provide executable semantics for contradiction, superseding state, provenance limitations or proposition-scoped completeness evidence.
- DPIP provides or evaluates privacy-preserving mechanisms for completeness proofs, non-disclosure of irrelevant history, or contradiction handling.

<!-- END GENERATED PRESSURE TEST -->

