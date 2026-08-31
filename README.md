# RAHP Toolkit

**Risk Assessment & Harms Prevention**  
Release v2.1.0 (stable) · Common Acacia Blue · CC-BY 4.0

RAHP Toolkit is a **portable assurance execution and monitoring plane** for pressure-testing standards, protocols, implementations, changesets and composed trust systems against human harms, governance failures, adversarial conditions, privacy/security risks and resilience failures.

> **Project identity:** RAHP is the reusable method, contracts and machine-owned assurance lifecycle. Repositories are evidence/source containers; the unit of assurance may instead be a specification, requirement, protocol surface, cross-specification interaction, composition, flow, implementation, deployment proposition, portfolio or changeset. DTG, CAWG/C2PA, A2A, OpenVTC, ARPA and other projects remain independently scoped deployments or qualification consumers.

## What RAHP does

RAHP turns a source/change observation into attributable assurance knowledge through a canonical lifecycle:

```text
subject/change observation
  → gather + subject model
  → materiality
  → bounded RAHP assessment
  → specialist routing when applicable
  → specialist examination + durable return
  → RAHP reconciliation
  → residual/action
  → citable terminal assurance record
```

The controller, not GitHub workflow choreography, owns assurance state. Workflows are triggers and transports around that state machine.

Current capabilities include:

- multi-granularity assurance subjects distinct from repository identity;
- scenario-driven harms, risk, governance, security and composition pressure testing;
- deterministic assessment identity, replay/idempotency and new-pin reassessment lineage;
- engine-owned clean-room isolation and terminal execution;
- target-agnostic autonomous assessment control;
- versioned portable specialist contracts, including `rahp-assessor-result/v1`;
- durable retryable specialist-return/outbox semantics with compatible specialists;
- watchdog detection of stranded transient states;
- explicit PASS, FAIL, NOT_APPLICABLE, INDETERMINATE/evidence-required and INDETERMINATE/model-gap outcomes;
- citable materially equivalent machine-readable and human-readable terminal records;
- evidence-class integrity across static specification evidence, fixtures/synthetic tests, runtime observations and governance evidence;
- action-target precision across specification, composition/profile, implementation, evidence/test, deployment/operator, governance/redress and consumer-experience surfaces;
- human-harm traceability from persona/scenario through harm/risk, proposition, control/guardrail, evidence, inference and recommendation;
- source-pinned corpora, cross-specification scenarios and bounded source/specification assertion adapters;
- continuous governed assurance through freshness, impact analysis, scoped authority and current posture.

RAHP is deliberately evidence-conservative: **zero findings is not equivalent to assured**. Missing evidence never becomes PASS. Workflow success is not assurance success. A component PASS never automatically implies a composition PASS.

## Qualified zero-touch architecture

The post-v2.0 architecture was qualified through #311/#318 and PR #319 across materially different A2A, CAWG/C2PA and DTG subjects. The clean-room qualification exercised standalone specification, cross-specification, implementation/source-code and composition subjects; no-specialist and specialist terminal paths; NOT_APPLICABLE and INDETERMINATE outcomes; model gaps; replay identity; new-pin reassessment lineage; durable outbox state; deliberately injected cross-repository transport failure and automatic recovery.

Qualification run `33350790322` completed with **zero operator actions after the trigger and zero stranded runs**. Durable evidence is committed at `clean-room/qualification/evidence-33350790322.json`; the human report is `docs/zero-touch-qualification-2026-08-31.md`.

The bounded product claim is:

> RAHP is qualified, within the tested contract and subject boundaries, as a zero-touch autonomous assurance monitoring plane that can fail closed into citable, actionable terminal assurance states without operator lifecycle shepherding.

This does not mean every assessment is GREEN. Trustworthy autonomous termination includes adverse and indeterminate outcomes.

## Quick start

```bash
pip install -r requirements.txt
python3 tools/review.py --help
python3 tools/validate.py
```

For a guided first run, use [Getting started](docs/getting-started.md). For the conceptual model, see [How RAHP works](docs/how-rahp-works.md). For continuous operation, see [Continuous assurance](docs/continuous-assurance.md). For repository internals and contracts, see the [Developer guide](docs/developer-guide.md).

## Choose your path

| I want to… | Start here |
|---|---|
| Understand RAHP | [How RAHP works](docs/how-rahp-works.md) |
| Run my first assessment | [Getting started](docs/getting-started.md) |
| Pressure-test a specification | [Pressure-testing a specification](docs/pressure-testing-a-spec.md) |
| Test multiple specifications together | [Cross-spec pressure testing](docs/cross-spec-pressure-testing.md) |
| Interpret findings and terminal states | [Interpreting results](docs/interpreting-results.md) |
| Understand continuous reassessment | [Continuous assurance](docs/continuous-assurance.md) |
| Adopt RAHP for another project | [Adopting RAHP](ADOPTION.md) and [Configuration](docs/configuration.md) |
| Develop or integrate the toolkit | [Developer guide](docs/developer-guide.md) |
| Review zero-touch qualification | [Qualification report](docs/zero-touch-qualification-2026-08-31.md) |

## Scenario and assurance coverage

The reusable catalogue under `method/catalogue/` contains portable assurance patterns across harms, risks, controls, guardrails, assurance tests and evidence patterns. Packaged scenario adapters include DTG, CAWG/C2PA and other interface/composition cases, including the seven-row adversarial false-independence corpus. Apparent multiplicity, depth, threshold satisfaction, actor distinctness or artifact validity must not automatically be upgraded into evidence independence or completeness.

See [Scenario corpora](docs/scenario-corpora.md) and [Cross-spec pressure testing](docs/cross-spec-pressure-testing.md).

## Current release

v2.1.0 **Common Acacia Blue** (*Surendra quercetorum*) is the stable **Qualified Autonomous Assurance Plane** release.

The release is additive at the product level and preserves the existing compatibility authorities:

```text
rahp-engine-contract-v1 revision 1.3
normalized result schema version 1
rahp-evidence-retention-v1
```

v2.1.0 packages the post-#311 canonical assurance FSM, autonomous controller, watchdog, terminal assurance records, multi-subject clean-room execution, source/spec assertion adapters and the multi-target zero-touch qualification evidence. Historical v2.0.0 **Blue Mormon** remains the immutable Portable Assurance Engine Stabilization record. Historical v1.6.0 **Common Earl** remains the immutable Source-Pinned Coverage and Guided Adoption release record.

Useful release surfaces:

- [v2.1.0 release notes](docs/releases/v2.1.0.md)
- [v2.1 qualification contract](method/v2.1-release-qualification.yaml)
- [Project status](PROJECT-STATUS.yaml)
- [Roadmap](ROADMAP.md)
- [Release history](CHANGELOG.md)

Release presentation metadata follows the governed West Bengal butterfly naming policy; semantic versioning and contract identifiers remain the compatibility authority.

## Repository map

| Path | Role |
|---|---|
| `method/` | Portable lifecycle, catalogue, schemas, glossary, mappings, qualification and engine/version contracts. |
| `tools/` | Portable orchestration, autonomous control, validation, monitoring, rendering, posture and build tooling. |
| `profiles/<id>/` | Deployment configuration and cross-specification registries. |
| `instances/<id>/` | Deployment-owned state, review records and local assurance vocabulary. |
| `clean-room/` | Declarative clean-room run specifications and committed qualification evidence. |
| `corpora/` | Scenario adapters mapped to portable stress patterns. |
| `examples/` | Curated worked assessments and portability/conformance fixtures. |
| `packages/` | TypeScript schema/core/graph/CLI reference implementation. |
| `docs/` | Guided documentation, architecture, runbooks, qualification and release notes. |
| `archive/` | Historical provenance; not current authority. |

## AI-assisted use and accountability

AI systems may assist with review, change analysis, scenario generation, evidence organization and drafting. AI output is not, by itself, assurance evidence and does not become a durable finding without the applicable evidence and assurance contract. See [AI-assisted RAHP](docs/ai-assisted-process.md).

## License and provenance

RAHP Toolkit preserves its DTG origin as provenance while operating as an independently reusable assurance toolkit.

**CC-BY 4.0 — reuse with attribution.**
