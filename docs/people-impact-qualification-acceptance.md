---
layout: default
title: People-impact qualification acceptance
parent: Learn RAHP
nav_order: 7
---

# People-impact qualification acceptance packet

This is a **bounded proposed adjudication**, not a record of independent reviewer approval, actual injury, incident detection, test execution or upstream normative authority.

## Qualification decision rule

A **qualified potential people-impact relationship** requires (1) a version-pinned technical failure mechanism, (2) a specific potentially affected *role*, distinguished from the party making the decision, (3) an articulated protected interest, (4) an explicit causal chain from failure through consequence, (5) an applicable canonical harm definition and meaningful countercases, and (6) an **accountable, independently reviewable acceptance decision**. It does not mean the failure has been observed or that harm occurred. Analyst-proposed source analyses stay provisional or not established until that review decision exists.

The canonical machine-readable [qualification packet](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/method/impact-pathways/qualification-acceptance-2026-10-20.json) contains **six atomic propositions across four scenarios** and deliberately records `independent_acceptance.status = not-recorded`.

| Scenario | Evidence is sufficient for | Proposed people-impact disposition | Still needs independent judgment |
|---|---|---|---|
| `TT-002` | Source defines audience binding and describes cross-recipient replay | Producer/principal and unintended recipient relationships **provisional** | Whether a downstream action affects a protected interest; bearer and conforming-rejection countercases |
| `XSP-001` | Credential Spec requires verified task outcome before inferring completion | Relying-party inference **provisional**; affected credential subject **not established** | Which subject experiences which consequential decision, if any |
| `TT-005` | Trust Tasks requires duplicate-execution protection for consequential tasks | Principal/consumer consequence **provisional** | Specific repeated operation and demonstrable affected interest |
| `XSP-018` | Composed scenario proposes a correlation threat | Person/relationship impact **not established** | Whether observable joint identifiers actually permit correlation in the deployment |

These are **packet dispositions** for review propositions. They do not modify the 50-row pilot's canonical scenario classification, which remains 0 qualified, 2 provisional and 48 not established. Candidate `HRM-*` IDs in the packet are **not accepted relationships**; their semantic applicability still requires review.

## Pinned sources and countercases

For `TT-002` and `TT-005`, the source-facing baseline is [Trust Tasks `SPEC.md` at `4937c70d`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/4937c70df95e56ed6404b8c004106ecb121a23cf/SPEC.md). Audience binding (§4.8.2), cross-recipient replay (§10.1) and duplicate-execution protection (§7.2, §10.1) establish technical requirements and threat mechanisms. A conforming consumer's rejection or idempotence mechanism is a meaningful countercase, not evidence that a person was harmed.

For `XSP-001` and `XSP-018`, the baseline comprises separate pins for [Trust Tasks](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/4937c70df95e56ed6404b8c004106ecb121a23cf/SPEC.md) and [Credential Specification](https://github.com/trustoverip/dtgwg-cred-spec/blob/b89f389abbdae77ba60b673c0836c781c2b54169/spec/body.md). Trust Task Context Binding provides a normative outcome-verification boundary relevant to `XSP-001`; this does **not** independently prove a consequential decision affecting a credential subject. `XSP-018` requires source- and implementation-specific evidence of common observer visibility and correlatable identifiers; its pathway is **not established**.

## Reproduction and acceptance

Run `python3 -m unittest tests.test_impact_qualification_packet -v` and `python3 tools/validate_impact_pathways.py --check --report`. Negative cases cover unsupported qualification, fictitious reviewer approval, direct and composed source drift, namespace collisions (`SEC-TT-002`), invalid harms, incomplete causal chains and invented persona/test claims.

**Independent adjudicator handoff:** Read the precise source clauses and each packet causal step; confirm or challenge the affected role, protected interest, candidate harm definition and countercases. Record an attributable acceptance/rejection decision with evidence and source revision. Do not change `independent_acceptance` to approved without a genuine reviewer record and accompanying validation changes. A human reviewer's independent judgment cannot be substituted with CI success or an assistant-generated recommendation.

**Acceptance impact:** This tranche completes a *review-ready qualification proposal*, not the original issue's requirement for at least one independently accepted people-impact pathway. [#1091](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1091) and [#1077](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1077) remain open.


## Capability qualification versus pathway qualification

This packet distinguishes two acceptance questions:

1. **Is the RAHP people-impact method usable and fail-closed?** This can be established through schema, validation, negative tests, source/dependency pinning, truthful zero-positive behavior, additional-corpus generality and reader-facing evidence boundaries.
2. **Has a particular affected-role → protected-interest → harm proposition been independently accepted?** That requires attributable human adjudication and cannot be created by CI or implementation work.

Accordingly, a stable method capability does not require manufacturing a `qualified` pathway. A release may accurately state that the capability is available while the current canonical pilot remains **0 qualified / 2 provisional / 48 not-established**. Any future `qualified` record still has to satisfy the existing direct-source and accountable-adjudication rules.
