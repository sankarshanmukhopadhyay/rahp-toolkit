---
layout: default
title: "Portable assurance catalogue browser"
has_toc: true
nav_exclude: true
---
# Portable assurance catalogue browser

RAHP v1.1's method-level assurance catalogue is available in two forms at the same repository boundary:

- **rendered reader views** on clean GitHub Pages routes; and
- **canonical YAML** for tools, validators and downstream adopters.

| Pattern family | Prefix | Rendered view | Canonical YAML |
|---|---|---|---|
| Harm patterns | `HRM-*` | [Browse harms](harm-patterns/) | [YAML](harm-patterns.yaml) |
| Risk patterns | `RKP-*` | [Browse risks](risk-patterns/) | [YAML](risk-patterns.yaml) |
| Control patterns | `CTP-*` | [Browse controls](control-patterns/) | [YAML](control-patterns.yaml) |
| Guardrail patterns | `GRP-*` | [Browse guardrails](guardrail-patterns/) | [YAML](guardrail-patterns.yaml) |
| Assurance patterns | `ATP-*` | [Browse assurance tests](assurance-patterns/) | [YAML](assurance-patterns.yaml) |
| Evidence patterns | `EVP-*` | [Browse evidence contracts](evidence-patterns/) | [YAML](evidence-patterns.yaml) |

The reader views are generated from the YAML at build time; they are not separately maintained catalogues. The YAML remains authoritative.

For the conceptual model and complete cross-layer explanation, see the [portable assurance catalogue documentation](../../docs/portable-assurance-catalogue.md) and [assurance knowledge model](../../docs/assurance-knowledge-model.md).


## Authority at commitment

The authority/delegation catalogue includes `RKP-AUTH-04` through `RKP-AUTH-07` for action-specific commitment authority. See [Authority-at-Commitment Assurance Pattern](../authority-at-commitment.md).
