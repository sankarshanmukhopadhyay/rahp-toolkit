# RAHP Toolkit

**Risk Assessment & Harms Prevention**  
Release v2.2.0 (stable) · Common Four-ring · CC-BY 4.0

RAHP Toolkit helps teams determine whether a trust system actually deserves confidence.

Standards, protocols and implementations can all appear correct in isolation while still producing privacy failures, governance gaps, security weaknesses, resilience failures or human harms when used in practice or combined with other components. A green workflow, a passing component test, or the absence of an obvious finding is not enough to establish assurance.

RAHP provides a reusable assurance method and execution plane for pressure-testing those systems against explicit propositions, scenarios, risks and evidence. It can assess a specification, requirement, protocol surface, implementation, deployment, changeset, cross-specification interaction, composition, flow or portfolio.

A typical RAHP assessment traces:

```text
persona/scenario
  → harm/risk
  → proposition
  → control/guardrail
  → evidence
  → inference
  → actionable recommendation
```

The result is not merely a list of findings. RAHP produces a citable assurance record that identifies what was tested, what evidence was available, what remains unknown, where remediation belongs, and what terminal conclusion is justified.

RAHP is deliberately evidence-conservative: **missing evidence never becomes PASS**. Workflow success is not assurance success. A component PASS never automatically implies a composition PASS.

> **Bounded product claim:** RAHP is qualified, within the tested contract and subject boundaries, as an autonomous assurance plane that can turn evidence/model/remediation gaps into attributable obligations and evidence-production paths while preserving fail-closed terminal semantics and explicit realization/runtime uncertainty.

This does not mean every assessment is GREEN, and it is not a claim of universal or production-wide assurance. Trustworthy autonomous termination includes adverse and indeterminate outcomes.

## When RAHP is useful

RAHP is useful when you need to:

- evaluate whether a specification actually supports the trust, governance, security, privacy or resilience claims made about it;
- pressure-test interactions between multiple specifications or protocols rather than assuming component correctness composes safely;
- assess whether an implementation or deployment preserves the assumptions of its normative baseline;
- determine whether a material change invalidates prior assurance evidence and requires reassessment;
- run continuous or repeated assurance without silently converting missing, stale or insufficient evidence into success.

## How the engine executes the method

RAHP turns a source/change observation into attributable assurance knowledge through a canonical lifecycle:

```text
subject/change observation
  → gather + subject model
  → materiality
  → bounded RAHP assessment
  → specialist routing when applicable
  → specialist examination + durable return
  → assurance obligation / evidence production when required
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
- semantic `rahp-assurance-obligation/v1` identity for evidence/model/remediation residuals;
- registered evidence-producer ownership, scheduling and provenance routing;
- versioned portable specialist contracts, including `rahp-assessor-result/v1`;
- durable retryable specialist-return/outbox semantics with compatible specialists;
- watchdog detection of stranded transient states;
- explicit PASS, FAIL, NOT_APPLICABLE, INDETERMINATE/evidence-required and INDETERMINATE/model-gap outcomes;
- citable materially equivalent machine-readable and human-readable terminal records;
- evidence-class integrity across static specification evidence, fixtures/synthetic tests, runtime observations and governance evidence;
- explicit normative-baseline versus implementation/realization separation;
- bounded assurance invariants across authority/actor dependency, evidence topology and human choice;
- action-target precision across specification, composition/profile, implementation, evidence/test, deployment/operator, governance/redress and consumer-experience surfaces;
- human-harm traceability from persona/scenario through harm/risk, proposition, control/guardrail, evidence, inference and recommendation;
- source-pinned corpora, cross-specification scenarios and bounded source/specification assertion adapters;
- continuous governed assurance through freshness, impact analysis, scoped authority and current posture.

## Current architecture

v2.2.0 builds on the v2.1.0 autonomous lifecycle by making evidence-production obligations and realization evidence first-class. The current-portfolio clean-room #446 / PR #447 demonstrates that bounded executable propositions can PASS while implementation, actuation, replay and privacy propositions remain explicitly INDETERMINATE when current evidence is absent.

The source-pinned current-portfolio run `34073261344` produced assessment `rahp:6b0ca36772a0184645c5` and a durable AMBER terminal record under `instances/dtg/reviews/current-portfolio-2026-09-07/`. This consumer result is qualification evidence for RAHP's inference discipline; it is not a claim that the DTG/OpenVTC portfolio is GREEN.

For the conceptual model, including the distinction between the assurance method and the assurance execution plane, see [How RAHP works](docs/how-rahp-works.md).

**Bundled DTG exemplar:** RAHP originated in Trust over IP Digital Trust Ecosystem work, where the method was developed and pressure-tested against concrete trust-architecture questions. This repository preserves that provenance while operating as an independently reusable assurance toolkit. The bundled DTG deployment profile, source-pinned scenario corpora and cross-specification examples are qualification/adoption consumers rather than dependencies of the generic method or engine contracts. A2A, CAWG/C2PA, OpenVTC, ARPA and other projects can likewise act as independently scoped assurance subjects or consumers.

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
| Review v2.2 release qualification | [v2.2.0 release notes](docs/releases/v2.2.0.md) |

## Scenario and assurance coverage

The reusable catalogue under `method/catalogue/` contains portable assurance patterns across harms, risks, controls, guardrails, assurance tests and evidence patterns. Packaged scenario adapters include DTG, CAWG/C2PA and other interface/composition cases, including adversarial false-independence and authority/composition cases. Apparent multiplicity, depth, threshold satisfaction, actor distinctness or artifact validity must not automatically be upgraded into evidence independence or completeness.

See [Scenario corpora](docs/scenario-corpora.md) and [Cross-spec pressure testing](docs/cross-spec-pressure-testing.md).

## Current release

v2.2.0 **Common Four-ring** (*Ypthima huebneri*) is the stable **Evidence Production and Realization Assurance** release.

The release is additive at the product level and preserves the existing compatibility authorities:

```text
rahp-engine-contract-v1 revision 1.3
normalized result schema version 1
rahp-evidence-retention-v1
```

v2.2.0 packages semantic assurance obligations, evidence-producer control and provenance routing, bounded assurance invariants, current-portfolio clean-room execution and explicit normative-versus-realization separation. Historical v2.1.0 **Common Acacia Blue** remains the immutable Qualified Autonomous Assurance Plane release. Historical v2.0.0 **Blue Mormon** remains the immutable Portable Assurance Engine Stabilization release. Historical v1.7.0 **Common Palmfly** remains the immutable Assurance Operations and Complete DTG Cross-Spec Coverage release record. Historical v1.6.0 **Common Earl** remains the immutable Source-Pinned Coverage and Guided Adoption release record.

Useful release surfaces:

- [v2.2.0 release notes](docs/releases/v2.2.0.md)
- [v2.2 qualification contract](method/v2.2-release-qualification.yaml)
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
