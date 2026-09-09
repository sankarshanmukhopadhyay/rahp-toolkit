# Portable assurance catalogue

The v1.1 portable assurance catalogue is a method-level library of reusable **harm, risk, control, guardrail, assurance and evidence patterns**. It is not a deployment risk register. DTG, CAWG/C2PA, A2A and other deployments may specialize or reference these patterns while retaining their own identifiers, governance state and evidence.

## Namespaces

| Prefix | Object | Purpose |
|---|---|---|
| `HRM-*` | Harm pattern | Human or institutional interest harmed |
| `RKP-*` | Risk pattern | Reusable failure mechanism |
| `CTP-*` | Control pattern | Reusable mitigation/control objective |
| `GRP-*` | Guardrail pattern | Non-negotiable prohibited-state boundary |
| `ATP-*` | Assurance pattern | Testable proposition about controls/guardrails |
| `EVP-*` | Evidence pattern | Evidence contract supporting an assurance claim |

The assurance chain is `harm ← risk → control → guardrail/assurance → evidence`. A deployment-specific record may specialize one or more portable patterns, but portable patterns never import deployment governance state.

## Guardrail requirement

Every `RKP-*` record says whether a guardrail is `required`, `conditional`, or `control_sufficient`. This prevents the coverage report from treating every risk without a guardrail as the same kind of gap. A required guardrail that has no `GRP-*` mapping is a validation error.

## Pattern graduation

Interop/implementation pressure cases do not automatically become new generic catalogue patterns. Candidate abstractions are dispositioned against existing catalogue semantics and portability evidence first. The current machine-readable graduation decisions live in [`interop-graduation-dispositions.yaml`](interop-graduation-dispositions.yaml); the method and review checklist are documented in [`docs/interop-pattern-graduation.md`](../../docs/interop-pattern-graduation.md).

The default is to reuse or refine existing generic patterns. A new core pattern is justified only when the proposition remains meaningful after replacing the original target and cannot be represented without semantic distortion.

For simple-English definitions of these terms, see [`method/glossary/`](../glossary/README.md).
