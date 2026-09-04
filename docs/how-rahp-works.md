---
layout: default
title: "How RAHP works"
nav_order: 2
has_toc: true
parent: Learn RAHP
---
# How RAHP works

RAHP converts changes in trust-system artefacts into attributable, reproducible and actionable assurance knowledge.

The easiest way to understand RAHP is to separate two layers that work together.

## Assurance method

The assurance method defines the chain of reasoning RAHP expects to make visible and testable:

`persona/scenario → harm/risk → proposition → control/guardrail → evidence → inference → actionable recommendation`

This layer asks questions such as:

- what claim or proposition is the system relying on;
- who can be affected if that proposition is false or incomplete;
- what harm, risk, governance, security, privacy or resilience failure could follow;
- what control or guardrail is supposed to prevent that failure;
- what evidence actually supports the control or proposition;
- what conclusion is justified by that evidence; and
- where remediation belongs if the proposition is not adequately supported.

RAHP therefore does not treat the absence of a discovered defect as equivalent to assurance. A valid assurance conclusion depends on the evidence required by the proposition being examined.

## Assurance execution plane

The execution plane makes that reasoning reproducible, source-pinned, replayable, specialist-aware and continuously reassessable.

It owns assessment identity and lifecycle state, keeps evidence classes distinct, routes bounded questions to compatible specialist assessors where necessary, reconciles their returns, records residual uncertainty and produces citable terminal assurance records. It also preserves reassessment lineage so that a material source change cannot silently inherit a conclusion established against an older immutable state.

The method explains **what must be reasoned about**. The execution plane explains **how that reasoning is governed and reproduced over time**.

## The assurance subject is not the repository

A repository is an evidence/source container. RAHP can assure a repository, but the actual subject can instead be an artefact, standard, specification, requirement, protocol surface, cross-specification interaction, composition, flow, implementation, deployment, portfolio or changeset. Subject identity, source pins and scope are therefore explicit controller inputs.

## Canonical machine-owned lifecycle

The execution plane implements the method through a canonical lifecycle:

```text
subject/change observation
→ gather
→ subject model
→ materiality
→ bounded RAHP assessment
→ specialist routing when applicable
→ specialist examination
→ return-ready
→ durable specialist return
→ RAHP reconciliation
→ durable residual/action
→ terminal assurance record
```

The state machine is authoritative. GitHub Actions workflows are transports and triggers; a green workflow is not itself an assurance conclusion.

Every transition is designed to be machine-owned, idempotent and source-pinned. Replay attaches to the same assessment identity. A new immutable source pin creates a new reassessment identity with explicit lineage/supersession semantics.

## Terminal outcomes are evidence-conservative

RAHP does not optimize for GREEN. Valid terminal outcomes include PASS, FAIL, NOT_APPLICABLE, INDETERMINATE/evidence-required, INDETERMINATE/model-gap, upstream-action and defined controller/contract error states.

Three statements that can look similar are deliberately kept distinct:

- **No finding observed** means the assessment did not identify a qualifying adverse finding within its tested scope.
- **PASS** means the applicable proposition was supported by the evidence required by the assessment contract.
- **Assured** is always bounded by the subject, scope, evidence class, source pin, contracts and qualification conditions that justify the conclusion.

Missing evidence never becomes PASS. Unknown or unmapped evidence surfaces become explicit model-gap residuals. Transport failure is retryable machine state rather than a human-only transition.

## Specialist assurance

Specialists consume versioned portable requests and return finite portable assessor results. A specialist `run:complete` must imply that a valid returnable result already exists. Cross-repository delivery is represented as durable outbox state with acknowledgement and idempotent retry.

DPIP is the first qualified privacy specialist, but RAHP is not version-locked to DPIP: compatibility is governed by contract/schema versions and shared fixtures.

## Evidence classes stay distinct

Static specification evidence, repository fixtures/synthetic tests, executable conformance evidence, attributable runtime observations and governance evidence answer different questions. One class cannot silently satisfy a proposition requiring another.

This is especially important for composition. **Component PASS does not imply composition PASS.** RAHP must separately evaluate cross-specification assumptions, authority/lifecycle interactions, correlation/privacy surfaces, substitution, redress, weakest-link behavior and evidence continuity at the composition/flow boundary.

## Citable terminal assurance records

A completed run produces materially equivalent machine-readable and human-readable facts, including subject/type, immutable pins, scope/non-scope, affected actors/personas, propositions, evidence and provenance, inference/boundedness, terminal outcome, residuals, required actions, remediation surface/owner and reassessment lineage.

Material findings should identify where remediation belongs: normative specification, composition/profile contract, implementation/code, evidence/test gap, deployment/operator control, governance/redress or consumer/user experience.

For a guided first run, see [Getting started](getting-started.md). For result interpretation, see [Interpreting results](interpreting-results.md). For adoption into another project, see [Adopting RAHP](../ADOPTION.md).

## Clean-room and continuous assurance

Clean-room execution is engine-owned: historical evidence/state cannot silently coalesce into a fresh qualification run. Continuous assurance uses the same lifecycle with explicit freshness, materiality, evidence and reassessment rules.

The post-#311 architecture was qualified across A2A, CAWG/C2PA and DTG in run `33350790322` with zero operator actions after the initial trigger and zero stranded runs. See [the qualification report](zero-touch-qualification-2026-08-31.md).

That qualification is bounded to the tested contract and subject conditions. It demonstrates autonomous assurance execution across the exercised cases; it is not a claim that every possible subject, deployment or future change is already assured.

## Portable assurance patterns

RAHP can project a deployment finding onto a portable assurance chain: `HRM-* ← RKP-* → CTP-* → GRP-*/ATP-* → EVP-*`. The local finding remains authoritative for the reviewed subject; the portable mapping makes recurring mechanisms comparable and testable across specifications. See [Assurance knowledge model](assurance-knowledge-model.md), [Engine contract](engine-contract.md) and [Review evidence and retention](evidence-retention.md).
