---
layout: default
title: "VTI pre-specification evidence pack"
parent: Reference
nav_order: 3
has_toc: true
---
# DTG VTI pre-specification evidence pack

This page packages mature RAHP composition evidence so a future DTG Verifiable Trust Infrastructure (VTI) specification effort can review evidence-backed propositions without having to rediscover the underlying failure modes.

This is **not a VTI specification, draft architecture, or source of upstream normative requirements**. RAHP contributes tested evidence. A future upstream VTI process remains responsible for accepting, rejecting, reformulating, relocating, or declining each proposition.

The working evidence register is [RAHP issue #192](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/192). The synthesis discussion is [Discussion #194](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/194). Packaging work is tracked in [issue #218](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/218).

## Evidence-pack contract

A mature entry uses the same eight fields so evidence can be reviewed proposition-by-proposition:

| Field | Required content |
|---|---|
| **Proposition** | The composition claim that has been pressure-tested. |
| **Why composition exposes it** | Why component-local validity or conformance is insufficient to establish the claim. |
| **Falsifier / adversarial case** | A concrete case that defeats an unsafe inference. |
| **Legitimate counter-case** | Similar-looking behaviour that must not be rejected without evidence. |
| **Executable evidence** | Fixture, test, review, issue and PR lineage sufficient to inspect the claim. |
| **Ownership assessment** | `COMPONENT-OWNED`, `COMPOSITION-OWNED / VTI-CANDIDATE`, `JOINTLY-OWNED`, `ASSURANCE-ONLY`, or `UNRESOLVED`. |
| **Residual uncertainty** | What the evidence does not establish and what remains indeterminate. |
| **Upstream question** | The question a future VTI drafting process should decide. |

An entry is not mature merely because a plausible requirement can be written. It needs evidence, a falsifier, a legitimate counter-case, and an explicit account of uncertainty and ownership.

## Ownership vocabulary

`COMPONENT-OWNED` means an existing component specification can own the proposition normatively and operationally. `COMPOSITION-OWNED / VTI-CANDIDATE` means the invariant emerges across components and plausibly needs a composition-level owner. `JOINTLY-OWNED` means a component owns local semantics while composition must preserve those semantics across the full interaction. `ASSURANCE-ONLY` means the evidence is useful for assurance but does not currently justify a normative VTI requirement. `UNRESOLVED` means the evidence does not yet support a stable ownership conclusion.

The purpose of these dispositions is to expose ownership boundaries, not to maximize the number of future VTI requirements.

---

# Evidence family 1 — false independence

**Source register:** [#193 — Adversarial identity and trust-independence evidence register](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193)

**Status:** executable evidence family complete

## Proposition

The completed corpus supports this assurance proposition:

> Apparent multiplicity, depth, threshold satisfaction, actor distinctness, or artifact validity MUST NOT automatically be upgraded into evidence independence or evidence completeness.

This wording records the proposition tested by the RAHP corpus. It is **not proposed VTI normative text**.

## Why composition exposes it

The unsafe inference can emerge even when individual components are locally valid. A relying system may receive valid identifiers, credentials, attestations, registry records, relationship assertions, provenance chains, votes, or threshold results and then combine their count or apparent diversity into a stronger trust conclusion.

No single component necessarily knows whether apparently separate actors share effective control, whether evidence paths derive from one source, whether a quorum is independently representative, whether social endorsements are operated by one controller, or whether a valid evidence subset omits provenance that materially changes the relying decision.

The composition-level question is therefore not only whether each input is valid. It is whether the **independence or completeness property relied upon by the final decision is actually established**.

## Falsifier / adversarial cases

The corpus pressure-tests seven distinct ways in which apparent corroboration can fail:

| Threat class | Unsafe inference defeated by the test |
|---|---|
| **SYBIL** | Many identifiers or identities imply many independent actors. |
| **FALSE-DIVERSITY** | Nominally different issuers, communities, registries or roots imply independent governance. |
| **TRUST-LAUNDERING** | More re-issuance, wrapping, transformations or provenance layers imply more assurance. |
| **SOCK-PUPPET** | More personas, endorsements or social relationships imply independent social evidence. |
| **QUORUM-CAPTURE** | Satisfying N-of-M arithmetic proves independent, representative or legitimate approval. |
| **COLLUSION** | Distinct actors are necessarily independent decision-makers or evidence sources. |
| **SELECTIVE-EVIDENCE** | A technically valid evidence subset is necessarily complete for the decision being made. |

Any architecture that silently grants independence or completeness solely from one of those observations would contradict the executable evidence in this family.

## Legitimate counter-cases

The corpus deliberately rejects the opposite overreach as well. It does not treat multiplicity or coordination-like surface characteristics as attack evidence by themselves.

Legitimate cases preserved by the tests include pairwise or contextual identifiers, privacy- or safety-preserving pseudonymity, genuinely independent issuers, shared infrastructure without common decisive governance control, transformations that preserve lineage, genuinely new independent evidence, legitimate multi-persona use, independently reached agreement, disclosed coalition action, legitimate weighted or versioned quorum rules, selective disclosure, and privacy-preserving minimisation.

Where independence, control, coordination, eligibility, provenance or completeness cannot be established, the result remains bounded uncertainty / `INDETERMINATE`; missing evidence is not silently upgraded into corroboration.

## Executable evidence

Each row below has issue/PR lineage, an executable fixture and claim-level tests in the repository.

| Review | Threat | Fixture | Claim-level test | PR / merged evidence | Preserved judgment |
|---|---|---|---|---|---|
| `SR-XSP-FI-001` | SYBIL | [`examples/cross-spec/false-independence-sybil/pressure-test.yaml`](../examples/cross-spec/false-independence-sybil/pressure-test.yaml) | [`tests/test_false_independence_pressure_test.py`](../tests/test_false_independence_pressure_test.py) | [#158](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/158) → [#198](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/198) → [PR #199](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/199) → `29eff9bef26ce7ceeb7766f78b81f7954a7cd588` | multiplicity ≠ independence |
| `SR-XSP-FI-002` | FALSE-DIVERSITY | [`examples/cross-spec/false-governance-diversity/pressure-test.yaml`](../examples/cross-spec/false-governance-diversity/pressure-test.yaml) | [`tests/test_false_governance_diversity_pressure_test.py`](../tests/test_false_governance_diversity_pressure_test.py) | [#160](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/160) → [PR #200](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/200) → `941eb03909d1eb269afc11124ec91752f1a8a94a` | nominal diversity ≠ governance independence |
| `SR-XSP-FI-003` | TRUST-LAUNDERING | [`examples/cross-spec/trust-laundering/pressure-test.yaml`](../examples/cross-spec/trust-laundering/pressure-test.yaml) | [`tests/test_trust_laundering_pressure_test.py`](../tests/test_trust_laundering_pressure_test.py) | [#159](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/159) → [#201](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/201) → [PR #205](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/205) → `15c27a40299e0223e9cc852916405458c32edede` | provenance depth ≠ assurance depth |
| `SR-XSP-FI-004` | SOCK-PUPPET | [`examples/cross-spec/false-social-independence-sock-puppetry/pressure-test.yaml`](../examples/cross-spec/false-social-independence-sock-puppetry/pressure-test.yaml) | [`tests/test_false_social_independence_sock_puppetry_pressure_test.py`](../tests/test_false_social_independence_sock_puppetry_pressure_test.py) | [#166](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/166) → [#206](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/206) → [PR #207](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/207) → `2160132bc7583971bddacd6b86491b30a6b9f094` | persona/social multiplicity ≠ social independence |
| `SR-XSP-FI-005` | QUORUM-CAPTURE | [`examples/cross-spec/quorum-capture/pressure-test.yaml`](../examples/cross-spec/quorum-capture/pressure-test.yaml) | [`tests/test_quorum_capture_pressure_test.py`](../tests/test_quorum_capture_pressure_test.py) | [#178](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/178) → [#208](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/208) → [PR #209](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/209) → `8b17e9f39ba3be8de8b35e9012d3508f7e0ebd68` | threshold arithmetic ≠ independent/legitimate approval |
| `SR-XSP-FI-006` | COLLUSION | [`examples/cross-spec/collusion/pressure-test.yaml`](../examples/cross-spec/collusion/pressure-test.yaml) | [`tests/test_collusion_pressure_test.py`](../tests/test_collusion_pressure_test.py) | [#167](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/167) → [#210](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/210) → [PR #211](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/211) → `aeae87ab99d95459209dfa7782b1ee6954e89a8c` | distinct actors ≠ necessarily independent actors |
| `SR-XSP-FI-007` | SELECTIVE-EVIDENCE | [`examples/cross-spec/selective-evidence/pressure-test.yaml`](../examples/cross-spec/selective-evidence/pressure-test.yaml) | [`tests/test_selective_evidence_pressure_test.py`](../tests/test_selective_evidence_pressure_test.py) | [#176](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/176) → [#212](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/212) → [PR #213](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/213) → `3f5c5931d1569193afa98e99e342339b799ff241` | valid evidence ≠ necessarily complete evidence |

The source register [#193](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/193) preserves the corpus-level synthesis and closure decision.

## Ownership assessment

**Current disposition: `UNRESOLVED`, with strong `COMPOSITION-OWNED / VTI-CANDIDATE` evidence.**

The evidence clearly establishes a system-level failure mode: locally valid or apparently diverse inputs can be composed into an unjustified independence or completeness inference. What it does **not** yet establish is that every resulting semantic obligation belongs in one future VTI layer.

Some controls may remain component-owned. A credentials specification may own provenance semantics; a governance mechanism may own voting eligibility and weighting; a relationship model may own controller or lineage semantics; relying policy may own the assurance weight granted to corroboration. Composition may nevertheless need to preserve or require enough of those semantics for the relying decision to avoid manufacturing independence.

That is why this entry is not promoted directly to a VTI requirement. Future evidence may narrow the ownership to `JOINTLY-OWNED`, `COMPOSITION-OWNED / VTI-CANDIDATE`, or multiple component-owned obligations.

## Residual uncertainty

The completed corpus establishes that independence and completeness cannot be inferred from count, nominal diversity, depth, actor distinctness, threshold satisfaction or technical validity alone. It does not yet establish a universal mechanism for proving independence.

Open questions include what evidence can establish effective control without creating unacceptable correlation; how circular or derivative evidence should be represented across component boundaries; how independence claims remain fresh as governance/control relationships change; what assurance policy should do when independence is unknowable; and which privacy-sensitive mechanisms require specialist DPIP examination.

The SOCK-PUPPET evidence specifically preserves the boundary that privacy-sensitive correlation, nullifier or retention mechanisms must not be smuggled into composition as a universal cross-context identity requirement.

## Upstream questions

A future VTI process should be able to consider at least these questions without presuming their answers:

1. When a relying decision materially depends on corroboration or consensus, what composition-level semantics are needed to distinguish apparent multiplicity from evidenced independence?
2. Which independence, control, lineage, eligibility, coordination, completeness and contradiction semantics belong to existing component specifications, and which must survive across the composed interaction?
3. When evidence of independence is incomplete, how should a conformant composed system preserve uncertainty rather than silently increase assurance?
4. Which privacy-preserving mechanisms can support independence claims without introducing durable cross-context correlation?
5. Does VTI need a composition-level invariant, a vocabulary for carrying component-owned semantics, a conformance test, relying-policy guidance, or some combination of these?

These are upstream decision questions. The RAHP evidence pack records why they exist and what tested failures they must account for; it does not answer them normatively.

---

# How additional evidence families enter the pack

The evidence register in [#192](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/192) currently identifies privacy composition, authority continuity, delegation lineage, lifecycle integrity, human control, configuration materiality, component substitution, failure/indeterminacy, semantic completion, portability and discovery-versus-authority as candidate families.

The workflow is evidence-first:

```text
Observed behaviour
      ↓
Composition question
      ↓
Falsifiable proposition
      ↓
Inventory existing RAHP / DPIP / interoperability evidence
      ↓
Build a new pressure test only where an evidence gap exists
      ↓
Record evidence + legitimate counter-case + uncertainty
      ↓
Classify ownership
      ↓
Admit mature evidence to this pack
      ↓
Potential upstream VTI input
```

A candidate family should not be added simply because it looks architecturally important. Existing RAHP, DPIP and interoperability evidence should be inventoried first; new implementation work should be opened only for a real evidence gap.

## RAHP and DPIP boundary

RAHP owns the composition-level assurance question. When specialist privacy depth is materially required, DPIP can examine a bounded proposition and return supporting evidence, counterevidence, missing evidence, residual uncertainty or `INDETERMINATE`. The returned result can strengthen or narrow an evidence-pack entry without making DPIP or RAHP the normative VTI owner.

## Review rule

Before admitting an evidence family, ask:

> What judgment should remain visible when a future VTI editor reads this evidence?

The answer should include the tested proposition, the evidence that survived pressure testing, the legitimate behaviour that must remain allowed, the uncertainty that remains, and the ownership question still left for upstream governance.