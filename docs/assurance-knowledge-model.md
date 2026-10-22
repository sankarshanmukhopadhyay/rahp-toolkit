---
layout: default
title: "Assurance knowledge model"
parent: Learn RAHP
nav_order: 4
has_toc: true
---
# Assurance knowledge model

RAHP v1.1 separates **portable assurance semantics** from **deployment risk state**. A portable pattern describes a reusable mechanism such as stale authority, delegation expansion, composition linkability or unavailable redress. A deployment-specific record describes how that mechanism manifests in a particular specification, governance regime or implementation context.

## Six portable object types

| Prefix | Object | Question answered |
|---|---|---|
| `HRM-*` | Harm pattern | What interest can be harmed? |
| `RKP-*` | Risk pattern | By what reusable failure mechanism? |
| `CTP-*` | Control pattern | What should prevent, constrain, detect or remedy it? |
| `GRP-*` | Guardrail pattern | What state must the system never silently enter? |
| `ATP-*` | Assurance pattern | What proposition can be tested? |
| `EVP-*` | Evidence pattern | What evidence would support the assurance claim? |

## Controls and guardrails are not synonyms

A **control** reduces probability, impact or duration of a risk. A **guardrail** defines a prohibited state or non-negotiable boundary. This preserves the existing RAHP rule that Critical harms cannot simply be scored and tolerated: unacceptable states need enforceable boundaries and evidence.

## Causal and compositional reasoning

The catalogue is intended to support chains such as:

```text
signed discovery metadata
  → relying party infers endorsement
  → authority is not independently evaluated
  → unauthorized consequential action
  → financial / autonomy harm
```

and cross-spec chains such as:

```text
credential valid at presentation
  + task valid at receipt
  + authority revoked before execution
  → composition-level failure despite component-level success
```

## Control consequence assessment

A mitigation is not automatically harmless. RAHP requires material control side effects to remain visible through the existing control-side-effect mechanism. Assessors should identify affected actors, reuse existing risks where possible, preserve context-dependent trade-offs as residual evidence, and keep insufficient evidence non-PASS. See [Assess control consequences](control-consequence-assessment.md) and the [worked control-consequence example](../examples/control-consequence-assurance/).

## Evidence boundary

RAHP distinguishes existence from assurance:

```text
control documented
≠ control enforced
≠ control tested
≠ evidence retained
≠ evidence still fresh
```

The v1.1 `ATP-*` and `EVP-*` objects make those distinctions machine-checkable without changing `rahp-engine-contract-v1`.

## Deployment specialization

Deployments should keep local identifiers and governance state. They may map a local finding to portable patterns through `portable_assurance`, but must not treat the portable catalogue as a substitute for deployment-specific evidence, authority or disposition.

See the [portable assurance catalogue](portable-assurance-catalogue.md) and [cross-specification pressure testing](cross-spec-pressure-testing.md).
