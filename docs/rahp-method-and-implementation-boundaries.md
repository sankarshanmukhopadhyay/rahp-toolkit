---
layout: default
title: "RAHP method and implementation boundaries"
parent: Implement RAHP
nav_order: 2
has_toc: true
---
# RAHP Method and Implementation Boundaries

Status: **discussion draft**  
Scope: **informative / non-normative**  
Tracking: [RAHP #1007](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1007)

This note explains how to distinguish the RAHP assurance method from the RAHP Toolkit implementation. It is intended to make the repository easier to reason about and easier to discuss upstream without prematurely creating a separate repository, formal specification, or new governance workstream.

This document does **not** change the RAHP engine contract, schemas, validators, controller behavior, release qualification state, or conformance boundary. Where this document differs from `method/engine-contract.yaml`, schemas under `method/schema/`, or other normative machine-readable surfaces, those artifacts remain authoritative.

## Executive summary

RAHP Toolkit is both:

1. a downstream implementation/tooling system; and
2. the current place where a substantial amount of RAHP methodological thinking is being captured.

That dual role is useful during development, but it can blur boundaries. A reader may not know whether a concept is:

- part of the portable assurance method;
- part of the stable execution/control-plane contract;
- part of this repository's reference implementation;
- part of a consumer profile or exemplar; or
- an experimental research/documentation surface.

The working distinction is:

```text
RAHP method
  = the assurance reasoning discipline:
    claim/proposition, affected interest, harm/risk, control/guardrail,
    evidence, inference, residual uncertainty, action.

RAHP execution/control plane
  = the governed machinery that makes that method reproducible:
    identity, lifecycle, source pins, routing, contracts, reconciliation,
    freshness, lineage, terminal records.

RAHP Toolkit
  = this repository's implementation and documentation of that method/control plane:
    tools, schemas, validators, examples, profiles, release records,
    reports, tests, and adoption material.
```

The practical goal is not to split the repository now. The practical goal is to make the boundary visible enough that future upstream discussion can decide which concepts, if any, should become more formal.

## Why this document exists

The repository already states that RAHP is a reusable assurance method and execution plane for determining whether a trust system deserves confidence. The README also states several core constraints: missing evidence never becomes PASS; workflow success is not assurance success; component PASS does not imply composition PASS; and normative convergence does not silently become implementation conformance. See [README](../README.md).

Those statements are not merely product positioning. They express the underlying assurance discipline that the toolkit is implementing.

The problem is that the discipline is currently distributed across:

- [How RAHP works](how-rahp-works.md);
- [RAHP data model](data-model.md);
- [Engine contract](engine-contract.md);
- [Continuous assurance](continuous-assurance.md);
- [Reasoning architecture and boundaries](reasoning-architecture.md);
- schemas under [`method/schema/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/method/schema);
- portable method material under [`method/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/method);
- implementation code under [`tools/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/tools) and [`packages/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/packages);
- examples under [`examples/`](../examples/);
- profile/instance material under [`profiles/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/profiles) and [`instances/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/instances); and
- release qualification and review records.

This is manageable for maintainers. It is harder for new adopters, upstream reviewers, and future implementers.

This document therefore records a reader-facing boundary model:

- what belongs to the method;
- what belongs to stable execution semantics;
- what belongs to the current reference implementation;
- what belongs to profiles and examples;
- what should not be inferred from implementation convenience; and
- what questions remain suitable for upstream discussion.

## Theory of change

RAHP's implicit theory of change can be stated as follows:

> Trust-system decisions become more reliable when consequential claims are examined through structured, repeatable, evidence-conservative assessment before those claims are relied upon.

A shorter engineering version is:

> Decisions should rely only on claims that have evidence appropriate to their consequence.

The method operationalizes this by forcing a reviewable chain:

```text
persona/scenario
  -> harm/risk
  -> proposition
  -> control/guardrail
  -> evidence
  -> inference
  -> actionable recommendation
```

This chain is already used in [How RAHP works](how-rahp-works.md) and [Reasoning architecture and boundaries](reasoning-architecture.md). The implementation exists to make this chain reproducible, source-pinned, challengeable and reusable across subjects.

## Core invariant

The central RAHP invariant is:

> Assurance conclusions must not exceed the evidence, scope, authority and contract under which they were established.

Most RAHP design choices follow from this invariant:

- missing evidence remains missing evidence;
- no finding observed is not the same as PASS;
- workflow success is not an assurance outcome;
- component PASS does not imply composition PASS;
- stale evidence cannot silently support a new conclusion;
- specialist or producer success must still be reconciled by RAHP;
- historical evidence must retain source pins and lineage;
- deployment-specific policy must not silently become portable method; and
- implementation convenience must not redefine assurance semantics.

This invariant is stronger than a tooling preference. It is the reason the toolkit keeps lifecycle, evidence, inference, residual state and disposition separate.

## Layer model

The current repository can be read as six layers.

```text
1. Method concepts
2. Portable execution semantics
3. Machine-readable contracts and schemas
4. Toolkit implementation
5. Profiles, instances and examples
6. Reports, releases and operational evidence
```

The layers are related, but they do not have the same authority.

### 1. Method concepts

Method concepts explain **what must be reasoned about**.

Examples include:

- assurance subject;
- proposition;
- affected actor/persona;
- harm/risk;
- control/guardrail;
- evidence requirement;
- evidence class;
- inference;
- residual uncertainty;
- finding;
- remediation;
- reassessment;
- composition boundary;
- authority boundary; and
- terminal assurance conclusion.

Primary reader-facing entry points:

- [How RAHP works](how-rahp-works.md);
- [Assurance knowledge model](assurance-knowledge-model.md);
- [RAHP data model](data-model.md);
- [Interpreting results](interpreting-results.md);
- [Review evidence and retention](evidence-retention.md).

These concepts should be stable enough that another implementation could reason about them without copying this repository's internal code structure.

### 2. Portable execution semantics

Execution semantics explain **how the method is governed over time**.

They include:

- assessment identity;
- source pins;
- lifecycle state;
- materiality-bounded selection;
- specialist routing;
- evidence obligations;
- durable returns;
- reconciliation;
- evidence freshness;
- reassessment lineage;
- terminal records; and
- explicit residual/action states.

Primary entry points:

- [Engine contract](engine-contract.md);
- [`method/engine-contract.yaml`](../method/engine-contract.yaml);
- [Continuous assurance](continuous-assurance.md);
- [`method/evidence-retention.yaml`](../method/evidence-retention.yaml);
- [`method/versioning.yaml`](../method/versioning.yaml).

These surfaces are closer to conformance and compatibility than general explanatory documentation. Changes here may affect whether another implementation remains compatible.

### 3. Machine-readable contracts and schemas

Contracts and schemas define the portable machine boundary.

Important examples include:

- [`method/schema/rahp-result.schema.json`](../method/schema/rahp-result.schema.json);
- [`method/schema/assessment-lifecycle.schema.json`](../method/schema/assessment-lifecycle.schema.json);
- [`method/schema/assessment-lineage.schema.json`](../method/schema/assessment-lineage.schema.json);
- [`method/schema/assurance-evaluation.schema.json`](../method/schema/assurance-evaluation.schema.json);
- [`method/schema/evidence-manifest.schema.json`](../method/schema/evidence-manifest.schema.json);
- [`method/schema/assurance-freshness.schema.json`](../method/schema/assurance-freshness.schema.json);
- [`method/schema/assurance-graph.schema.json`](../method/schema/assurance-graph.schema.json);
- [`schemas/rahp-assessor-result-v1.schema.json`](../schemas/rahp-assessor-result-v1.schema.json);
- [`schemas/rahp-assurance-obligation-v1.schema.json`](../schemas/rahp-assurance-obligation-v1.schema.json);
- [`schemas/rahp-evidence-producer-result-v1.schema.json`](../schemas/rahp-evidence-producer-result-v1.schema.json).

Reader guidance should not contradict these contracts. Reference implementations may use richer internal structures, but portable behavior must preserve the normalized proposition, evidence, reasoning and lifecycle semantics required by the engine contract.

### 4. Toolkit implementation

Implementation explains **how this repository realizes the method and contracts**.

Important implementation surfaces include:

- [`tools/assessment_controller.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/assessment_controller.py);
- [`tools/autonomous_assurance_controller.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/autonomous_assurance_controller.py);
- [`tools/assurance_fsm.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/assurance_fsm.py);
- [`tools/evidence_assertion_assessor.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/evidence_assertion_assessor.py);
- [`tools/validate.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/validate.py);
- [`tools/validate_engine_contract.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/validate_engine_contract.py);
- [`tools/assurance_posture.py`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/assurance_posture.py);
- [`packages/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/packages).

Implementation choices are not automatically method concepts. For example, a file layout, function name, CLI argument, local cache strategy or workflow job name may be a useful implementation decision without being a portable RAHP rule.

The contribution guide already warns contributors to edit the canonical source for the layer being changed and identifies distinct authority boundaries such as `method/`, `method/catalogue/`, `instances/`, `profiles/`, `examples/`, `tools/`, `packages/` and `build/`. See [Contributing](../CONTRIBUTING.md).

### 5. Profiles, instances and examples

Profiles, instances and examples demonstrate or configure RAHP for particular subjects.

Examples:

- [`examples/hello-rahp/`](../examples/hello-rahp/);
- [`examples/standalone-trqp/`](../examples/standalone-trqp/);
- [`examples/composed-assurance/`](../examples/composed-assurance/);
- [`profiles/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/profiles);
- [`instances/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/instances);
- [`corpora/`](../corpora/).

The adoption gateway states that an adopter can start with RAHP alone and that DPIP and the Trust Protocol Interop Lab are optional independently governed capabilities used only when a proposition requires their specialist or evidence role. See [Adoption gateway](adoption-guide.md).

A maintained example can be strong evidence that the method is usable. It is not, by itself, a normative definition of RAHP.

### 6. Reports, releases and operational evidence

Reports and releases record what a bounded run or packaged release established.

Examples:

- [v2.7.0 release notes](releases/v2.7.0.md);
- [`method/v2.7-release-qualification.yaml`](../method/v2.7-release-qualification.yaml);
- [`method/v2.7-release-evidence.json`](../method/v2.7-release-evidence.json);
- [v2.7.0 security disposition](review/v27-release-security-disposition.md);
- [Eucalyptus clean-room campaign report](reports/eucalyptus-clean-room-2026-10-08.md).

These records are evidence about a release or run. They do not create unlimited assurance for other subjects, future commits, untested deployments or unrelated profiles.

## Boundary table

| Question | Method answer | Implementation answer | Boundary risk |
|---|---|---|---|
| What is being assessed? | A bounded assurance subject and proposition set. | A configured input, source pin, path, profile or run target. | Treating a repository as the only possible assurance subject. |
| What makes a conclusion valid? | Admissible evidence supports the proposition within scope and authority. | Validators, controllers, tests, schemas and reports produce bounded records. | Treating successful execution as PASS. |
| What happens when evidence is missing? | Missing evidence remains missing, indeterminate or evidence-required. | The controller/result model must preserve explicit residual state. | Collapsing missing evidence to success because no finding was emitted. |
| What does a specialist do? | Examines a bounded question requiring specialist semantics. | Returns a versioned portable result for RAHP reconciliation. | Treating specialist completion as final RAHP assurance. |
| What does an evidence producer do? | Produces evidence for an obligation. | Emits source-pinned producer results or fixtures. | Treating producer workflow success as substantive assurance. |
| What does composition require? | Composition propositions must be assessed at the seam. | Profiles/examples may encode specific seams and evidence routes. | Inferring composition PASS from component PASS. |
| What changes after source mutation? | Prior assurance must be re-evaluated for freshness and materiality. | Lineage/freshness contracts and reassessment tooling select affected scope. | Reusing old assurance against new source state. |
| What is portable? | Concepts and contracts that another implementation can preserve. | Code structure, CLI behavior, test harnesses and workflow details may vary. | Treating this repository's internal shape as the method. |

## What belongs to the method

The following should normally be treated as method-level concepts:

1. **Evidence-conservative assurance** — absence of evidence or absence of observed defects is not PASS.
2. **Proposition-centered review** — assessments are organized around claims that can be supported, falsified or left indeterminate.
3. **Affected-interest reasoning** — harms and risks matter because real actors or interests can be affected.
4. **Control and guardrail mapping** — controls explain how a risk is constrained; guardrails define states the system must not silently enter.
5. **Evidence class separation** — static documentation, schema conformance, executable tests, runtime observations and governance evidence answer different questions.
6. **Inference discipline** — conclusions must state what the evidence justifies and what remains residual or out of scope.
7. **Authority separation** — assessment, disposition, publication, remediation and risk acceptance are distinct authority surfaces.
8. **Composition awareness** — assurance of parts does not automatically establish assurance of flows, seams or compositions.
9. **Lineage and freshness** — assurance is bounded to the source state and evidence state against which it was produced.
10. **Challengeability** — significant conclusions should preserve enough evidence and reasoning to be reviewed, challenged or superseded.

These concepts should be discussed as RAHP concepts, not merely as implementation conveniences.

## What belongs to the execution/control plane

The following are not merely prose method ideas. They are execution responsibilities that any compatible implementation should preserve at the relevant contract boundary:

- stable assessment identity;
- immutable source pins;
- finite lifecycle state;
- explicit process/assurance/evidence dimensions where applicable;
- materiality-bounded reassessment selection;
- evidence provenance and freshness;
- versioned specialist requests and results;
- versioned evidence obligations and producer results;
- terminal reconciliation;
- residual/action records;
- reassessment lineage;
- compatibility versioning; and
- validation of the declared engine contract.

The toolkit currently realizes these through schemas, controllers, validators and examples. A future implementation may choose a different internal architecture, but it should not silently change these semantics while claiming compatibility with the same engine contract.

## What belongs to this implementation

The following should normally be treated as RAHP Toolkit implementation choices unless promoted through a deliberate method/contract change:

- Python module boundaries and internal function names;
- TypeScript package layout;
- CLI command names and flags;
- workflow/job decomposition;
- local directory structure outside the portable contract boundary;
- optimization strategies;
- fixture organization;
- rendered documentation layout;
- release-codename policy;
- repository-specific label conventions;
- bundled DTG exemplar topology; and
- current example selection.

These choices matter. They affect maintainability, adoption and reproducibility. They should not, however, be mistaken for the assurance method itself.

## What belongs to profiles and exemplars

Profiles and exemplars make the method concrete for a subject. They can also expose gaps in the method. But they do not automatically become portable RAHP semantics.

For example:

- DTG profile execution classes such as `core`, `conditional` and `reference` are described in [Continuous assurance](continuous-assurance.md) as DTG profile policy, not portable RAHP vocabulary.
- The standalone TRQP example demonstrates source-pinned bounded examination of a real specification surface; it does not make TRQP the only or privileged RAHP subject. See [standalone TRQP example](../examples/standalone-trqp/README.md).
- The composed-assurance example demonstrates specialist/evidence-producer routing; it does not require all adopters to install DPIP or the Interop Lab. See [composed assurance walkthrough](../examples/composed-assurance/README.md).

A recurring profile pattern may become a candidate method concept. That promotion should be explicit, reviewed, and supported by evidence that the concept is reusable beyond the originating profile.

## What should not be inferred

The following inferences are deliberately unsafe:

| Unsafe inference | Correct RAHP reading |
|---|---|
| A green GitHub Actions workflow means the subject is assured. | Workflow success is operational evidence, not an assurance conclusion. |
| Zero findings means PASS. | Zero findings may coexist with evidence gaps, model gaps or unassessed propositions. |
| A component PASS implies composition PASS. | Composition seams require their own proposition/evidence assessment. |
| A specialist PASS is automatically a RAHP PASS. | Specialist returns must be reconciled under RAHP's scope and contract. |
| A schema-valid result is substantively correct. | Schema validity is necessary but not sufficient for assurance. |
| A release qualification applies to all future subjects. | Release qualification is bounded to the tested release, contracts and evidence. |
| A profile policy term is portable RAHP vocabulary. | Profile policy remains profile policy unless promoted deliberately. |
| AI-generated reasoning is assurance evidence by itself. | AI output may assist drafting or organization; durable assurance still requires admissible evidence and accountable review. |
| Documentation prose can override schemas. | Machine-readable contracts and schemas remain authoritative at the portable boundary. |

## Relationship to existing documentation

This document is a boundary map, not a replacement for existing docs.

Use this reading order:

1. [README](../README.md) — current capability and release boundary.
2. [How RAHP works](how-rahp-works.md) — method and execution-plane overview.
3. [RAHP data model](data-model.md) — record families and authority map.
4. [Engine contract](engine-contract.md) — stable portable execution boundary.
5. [Continuous assurance](continuous-assurance.md) — reassessment, freshness and lineage.
6. [Reasoning architecture and boundaries](reasoning-architecture.md) — reasoning distribution and agent independence.
7. [Adoption gateway](adoption-guide.md) — adoption roles and dependency boundaries.
8. Schemas under [`method/schema/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/method/schema) — authoritative machine-readable structures.
9. Implementation under [`tools/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/tools) and [`packages/`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/main/packages) — current reference implementation.

## Compatibility implications

This document introduces no compatibility change. It is intended to reduce accidental compatibility claims by making boundaries more explicit.

Future changes should use the following rule:

```text
If the change alters what a compatible RAHP implementation must preserve,
it is not merely documentation or implementation cleanup.
```

Potentially compatibility-significant changes include:

- changing the meaning of PASS, FAIL, NOT_APPLICABLE or INDETERMINATE;
- changing lifecycle transitions or terminalization semantics;
- changing evidence freshness semantics;
- changing specialist-result or evidence-producer-result meaning;
- changing result-schema requirements;
- making an optional profile mandatory;
- changing composition-assessment semantics; or
- changing what counts as admissible evidence for a proposition.

Such changes should be evaluated against [Engine contract](engine-contract.md), [`method/engine-contract.yaml`](../method/engine-contract.yaml), [`method/versioning.yaml`](../method/versioning.yaml), and the relevant schemas.

## Contribution implications

When contributing, ask which layer is changing.

| Change type | Likely canonical surface | Review question |
|---|---|---|
| New assurance pattern | `method/catalogue/` | Is this portable or deployment-local? |
| New schema field | `method/schema/` or `schemas/` | Does this alter the portable contract? |
| New controller behavior | `tools/` plus tests/docs | Does lifecycle or terminal semantics change? |
| New example | `examples/` | Is it teaching material, conformance evidence, or a maintained exemplar? |
| New profile rule | `profiles/` | Is it profile policy or portable method? |
| New release claim | release notes / qualification evidence | What evidence bounds the claim? |
| New explanatory page | `docs/` | Does it explain existing semantics or introduce new ones? |

The contribution guide's key rule remains: edit the canonical source for the layer being changed and do not hand-edit generated output. See [Contributing](../CONTRIBUTING.md).

## Upstream discussion questions

This downstream note is useful precisely because it does not force a conclusion. It creates a concrete artifact around which to ask upstream questions.

Possible upstream questions:

1. **Does RAHP need an explicit method/implementation distinction?**
   - Or is the current toolkit-first structure acceptable for the current maturity stage?

2. **Which concepts should be considered RAHP method concepts?**
   - For example: evidence-conservative PASS, proposition-centered review, materiality-bounded reassessment, component/composition separation, and source-pinned lineage.

3. **Which concepts should remain implementation-specific?**
   - For example: CLI design, controller module layout, workflow orchestration, local fixture organization, and documentation navigation.

4. **Is the engine contract the correct portable boundary?**
   - If not, what is missing or over-specified?

5. **What would another implementation need to preserve to be recognizably compatible?**
   - Schemas only? Engine contract? Lifecycle semantics? Evidence/freshness rules? Examples and conformance fixtures?

6. **When should an experimental profile become method material?**
   - What evidence should be required before promotion?

7. **How should upstream avoid over-formalizing too early?**
   - The current practical path may be to keep this as a discussion draft while collecting recurring boundary questions from implementation work.

8. **What vocabulary is least likely to create process drag?**
   - Terms such as method, boundary, execution plane and reference implementation may be more useful at this stage than specification, standard or theory.

## Decision posture

For now, the recommended downstream posture is conservative:

- keep the document in this repository;
- mark it informative and non-normative;
- use it to guide local contribution review;
- use it as upstream agenda material when helpful;
- do not create a new repository merely for the concept boundary;
- do not claim a new conformance layer until there is evidence that multiple implementations or profiles need it; and
- revisit after upstream discussion or after repeated implementation work exposes the same boundary issue.

## Maintenance rule

This document should be updated when repository evolution makes the method/implementation boundary clearer or more ambiguous.

Update it when:

- a method concept is promoted into a schema or engine contract;
- a profile-specific rule is generalized;
- an implementation-specific behavior is mistaken for a portable requirement;
- a new specialist or evidence producer exercises the same contract boundary;
- a release changes stable assurance semantics; or
- upstream discussion settles a boundary question.

Do not update it merely to narrate every implementation change.

## Current conclusion

The RAHP Toolkit should continue to function as the downstream implementation and documentation home for this work. The immediate need is not a new name, new repo or new formal standard. The immediate need is a clear boundary map so that method, contract, implementation, profile, example and evidence claims do not collapse into one undifferentiated toolkit narrative.

That boundary map is now explicit enough to support upstream discussion without forcing an architectural decision before the need is validated.
