---
layout: default
title: "Adoption gateway"
nav_order: 1
has_toc: true
parent: Adopt RAHP
---
# Adoption gateway

This is the canonical starting point for adopting RAHP in a project, specification, implementation, deployment or portfolio.

**You can start with RAHP alone.** DPIP and the Trust Protocol Interop Lab are independently governed optional capabilities that become relevant only when an assessment needs the specialist or evidence role they provide.

## The four roles

| Role | Responsibility | Current implementation/example |
|---|---|---|
| **Assurance subject** | The thing being assessed: specification, implementation, deployment, composition, flow, change or other bounded target. | Your project or a configured example. |
| **Assurance orchestrator** | Owns assessment identity/lifecycle, proposition/evidence boundaries, specialist routing, reconciliation, residuals and terminal assurance records. | **RAHP Toolkit**. |
| **Specialist assessor** | Examines a bounded question requiring specialist semantics and returns a portable assessor result. | **DPIP** for composed privacy questions. |
| **Evidence producer** | Produces bounded executable/implementation evidence for an assurance obligation without becoming the authority for the final assurance conclusion. | **Trust Protocol Interop Lab**. |

These are architectural roles, not mandatory products. A compatible future specialist or evidence producer can participate through the same versioned contracts.

## What do I actually need?

| Need | RAHP | DPIP | Interop Lab |
|---|---:|---:|---:|
| First bounded RAHP review | Required | No | No |
| Risk/harm/security review with source-pinned evidence | Required | No | No |
| Composed privacy examination | Required | When routed | Only if the privacy proposition requires executable evidence that the Lab can produce |
| Executable interoperability/composition evidence | Required | No, unless privacy is also in scope | When the applicable obligation maps to a supported Lab evidence surface |
| Continuous assurance after material change | Required | When a specialist privacy question is selected | When fresh executable evidence is required |
| Other specialist domain | Required | No | No, unless it is a suitable evidence producer |

The governing rule is **capability-driven composition, not repository-driven installation**. Do not add a specialist or evidence producer merely because it exists.

The same rule applies to execution breadth: **select the minimum assurance/evidence surface required by the proposition and material change**. Do not run every available assessment, specialist or composition simply because RAHP can. Retain valid evidence, preserve explicit uncertainty, and widen to a full campaign only when the materiality boundary cannot be defended.

## Choose an adoption track

### Track A — first RAHP assessment

Use this when you want to understand the method and run a bounded review without cross-repository dependencies.

~~~text
assurance subject
  -> RAHP configuration
  -> bounded review
  -> evidence-backed findings / residuals
~~~

Start with [Hello RAHP](../examples/hello-rahp/README.md), then use [Configuration-driven adoption](configuration.md).

### Track B — evidence-backed assurance

Use this when propositions have explicit evidence requirements and you need stronger provenance, evidence classification and reconciliation.

~~~text
subject
  -> proposition
  -> required evidence class
  -> evidence acquisition/production
  -> inference
  -> residual/action
~~~

Read [How RAHP works](how-rahp-works.md), [Evidence classification](evidence-classification.md), [Assurance evaluation](assurance-evaluation.md) and [Interpreting results](interpreting-results.md).

### Track C — composed assurance

Use this when RAHP determines that a bounded question needs a specialist assessor, an external evidence producer, or both.

~~~text
RAHP controller
  -> bounded RAHP assessment
  -> specialist request (when applicable)
  -> evidence obligation (when applicable)
  -> specialist/evidence producer return
  -> RAHP reconciliation
  -> residual/action
  -> terminal assurance record
~~~

See the [composed-assurance walkthrough](../examples/composed-assurance/README.md).

### Track D — continuous assurance

Use this after the initial assessment when source changes, evidence freshness, reassessment lineage, remediation and governed disposition matter.

Continue with [Continuous assurance](continuous-assurance.md).

## Decision tree

~~~text
Do you have a bounded subject and a question to assess?
  |
  +-- no -> define subject, source pin and scope first
  |
  +-- yes
       |
       +-- Can RAHP assess the proposition with admissible evidence directly?
       |     |
       |     +-- yes -> RAHP-only path
       |     |
       |     +-- no
       |          |
       |          +-- Is this a composed privacy question?
       |          |     |
       |          |     +-- yes -> route to a compatible privacy specialist such as DPIP
       |          |
       |          +-- Does the proposition require executable implementation/composition evidence?
       |                |
       |                +-- yes -> route an assurance obligation to a compatible evidence producer
       |                         (the Interop Lab where it supports the needed evidence surface)
       |
       +-- Reconcile every returned result/evidence item in RAHP.
~~~

A specialist PASS is not automatically a RAHP PASS. A successful evidence-producing experiment is not automatically a RAHP PASS. Missing evidence remains missing evidence.

## Current cross-repository boundary

As of the current stable coordinated portfolio boundary:

- **RAHP v2.5.0** owns the assurance lifecycle and orchestration.
- **DPIP v0.3.0** owns composed privacy examination and returns compatible **rahp-assessor-result/v1** results.
- **Trust Protocol Interop Lab v0.7.0** owns bounded executable interoperability/implementation evidence.

The repositories are independently versioned and governed. Compatibility is established through contracts and evidence provenance, not by assuming that matching release dates imply compatibility. The version list above records the current maintained portfolio context; it does not mean that every proposition requires all three repositories.

Authoritative RAHP integration surfaces:

- [rahp-assessor-result/v1 schema](../schemas/rahp-assessor-result-v1.schema.json)
- [assessor-result contract guide](assessor-result-contract.md)
- [rahp-assurance-obligation/v1 schema](../schemas/rahp-assurance-obligation-v1.schema.json)
- [rahp-evidence-producer-result/v1 schema](../schemas/rahp-evidence-producer-result-v1.schema.json)

Current external implementation documentation:

- [DPIP repository](https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile)
- [DPIP understanding guide](https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile/blob/main/docs/understanding-dpip.md)
- [DPIP RAHP return operations](https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile/blob/main/docs/rahp-return-operations.md)
- [Trust Protocol Interop Lab](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab)
- [Lab evidence and assurance guide](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/blob/main/docs/evidence-and-assurance.md)

## What you do not need to learn first

A new adopter does not need to understand the bundled DTG deployment, VTI programme, DTG Portfolio Monitor, CAWG deployment, historical release lineage, DPIP internals or Interop Lab case catalogue before starting.

Those become relevant only when your subject, proposition or evidence obligation reaches those surfaces.

## First success criterion

A newcomer has successfully crossed the adoption gateway when they can answer:

1. What is my assurance subject and immutable source boundary?
2. What proposition or review question am I testing?
3. Can RAHP handle it directly?
4. If not, what specialist or evidence capability is required and why?
5. What evidence supports the conclusion?
6. What remains residual, indeterminate or out of scope?
7. Why is this the minimum sufficient assessment scope for the material proposition set, and what would trigger a broader rebaseline?

Then move from [Hello RAHP](../examples/hello-rahp/README.md) to the full [Adopting RAHP](../ADOPTION.md) guide.
