---
layout: default
title: "Concepts"
nav_order: 1
has_toc: true
parent: Learn RAHP
---
# RAHP concepts

**RAHP Toolkit is deployment-neutral.** The concepts below belong to the portable method unless a section explicitly labels a DTG, CAWG/C2PA, or other deployment-specific example.

RAHP treats harm prevention as an assurance chain rather than a standalone risk register.

| Artefact | Plain-language meaning |
|---|---|
| Persona | Who may be affected |
| User Story | What that participant is trying to achieve |
| Scenario | What happens in a concrete context |
| Scenario Pattern | A reusable failure or stress condition that can apply across domains |
| Scenario Corpus | A domain-owned collection of concrete scenarios mapped to portable patterns |
| Risk | What can go wrong |
| Harm | Who bears the consequence and how |
| Control | What reduces likelihood or impact |
| Guardrail | What must be true before progression |
| Assurance Test | How a guardrail or control is proven |
| Metric | How behaviour is observed over time |
| Recommendation | What should change |
| Risk Acceptance | Where residual risk is consciously accepted |
| Governance Precedent | Existing governance practice that informs treatment |

Corpus scenarios in `corpora/*.yaml` are source/domain pressure-test vectors. The separately maintained `SC-*` scenarios in `data/scenarios.yaml` include people-linked context through personas and user stories. Their identifiers do not imply a validated relationship. See [Reading a scenario corpus](reading-scenario-corpus.md).

The relationship model is visualised in [Artefact relationships](diagrams/artefact-relationships.md).

## Authority is part of assurance

A control is incomplete if no actor has authority to operate it, no evidence shows whether it operated, or no revocation/escalation path exists when it fails. RAHP therefore distinguishes the existence of a risk from the layer with legitimate authority to mitigate it.

## Portable assurance patterns

RAHP v1.1 adds a reusable assurance layer above deployment records. `HRM-*` names harms, `RKP-*` names recurring failure mechanisms, `CTP-*` names control objectives, `GRP-*` defines prohibited-state boundaries, `ATP-*` defines testable propositions and `EVP-*` defines evidence contracts. A finding may map to these patterns through `portable_assurance` while retaining local risk/control IDs and source evidence. See [Assurance knowledge model](assurance-knowledge-model.md).
