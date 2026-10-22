---
layout: default
title: "Assess control consequences"
parent: Implement RAHP
nav_order: 6
has_toc: true
---
# Assess control consequences

RAHP does not stop analysis when a candidate control mitigates its target risk. A control can also introduce, transfer, amplify or redistribute exposure among actors. Those effects must remain visible when they are material.

This is already represented by the portable method through `CTP-RISK-01`, `ATP-RISK-01`, `EVP-RISK-01`, the `introduces_or_amplifies_risks` field on control patterns, and the `Control side effect` glossary term. The method does **not** require a schema extension for ordinary control-consequence assessment.

## Assessment sequence

For each material candidate control:

1. **State the target mitigation.** Identify the risk/harm the control is intended to reduce and the actor who benefits.
2. **Inspect consequences.** Ask whether the control creates, transfers, amplifies or redistributes privacy, exclusion, autonomy, security, operational or political-economy exposure.
3. **Name affected actors.** Record whose exposure decreases and whose exposure increases or becomes uncertain. Do not collapse participant trade-offs into one blended score.
4. **Reuse existing patterns first.** Map the consequence to existing `HRM-*` / `RKP-*` records where the mechanism already exists.
5. **Disposition explicitly.** Use one of the bounded outcomes below.
6. **Record evidence.** Use `EVP-RISK-01` or equivalent assessment evidence. Missing or contradictory evidence remains non-PASS.
7. **Retest after change.** Reassess when the control design, authority, deployment context or evidence basis materially changes.

## Disposition vocabulary

| Disposition | Use when | Expected treatment |
|---|---|---|
| **existing coverage** | an existing portable mechanism describes the consequence without distortion | link the existing risk/harm/control relationship and retain evidence |
| **context-dependent residual / trade-off** | the consequence is material in this deployment but not a new reusable mechanism | keep it visible in assessment evidence/residual state |
| **candidate distinct reusable risk/harm** | evidence shows a recurrent mechanism that existing patterns cannot represent | open a bounded catalogue contribution and prove reuse before allocating an ID |
| **insufficient evidence** | the material consequence cannot yet be assessed | preserve `INDETERMINATE`/evidence-gap state; do not grant assurance credit by omission |

## Portable field versus assessment evidence

Use `introduces_or_amplifies_risks` on a portable `CTP-*` when the side-effect relationship is itself reusable and belongs to the control pattern. `CTP-ID-03` demonstrates this for uniqueness assurance, which can increase exclusion and stable-identifier correlation risk.

Do **not** add every plausible contextual consequence to every portable control. A side effect that depends on deployment policy, cadence, accessibility, topology, user population or implementation detail belongs in the assessment evidence until reuse is demonstrated.

## Actor redistribution

A valid assessment can conclude that a control lowers risk for one participant while increasing burden or exposure for another. For example, stronger renewal proofing may lower a relying party's stale-authority risk while increasing holder proofing burden and revealing lifecycle timing. This is neither automatically acceptable nor automatically a defect. It is a governed trade-off that needs evidence and disposition.

## Failure behavior

An unassessed material control consequence must not silently become PASS. The control can receive only the bounded credit supported by the available evidence. Where a guardrail or protected interest would be violated, the normal fail-closed/defer/escalate semantics still apply.

## Worked evidence

See [`examples/control-consequence-assurance/`](../examples/control-consequence-assurance/) for five cases spanning renewal, uniqueness, audit/contestability evidence, revocation propagation and a human intent checkpoint. The renewal case is grounded in #1106 and the generalization is tracked in #1089.
