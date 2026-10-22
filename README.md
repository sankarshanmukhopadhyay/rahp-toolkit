# RAHP Toolkit

**Risk Assessment & Harms Prevention**  
Release v2.9.0 · Common Windmill · Documentation: CC BY 4.0 · Code: Apache 2.0

RAHP Toolkit is a reusable assurance method and execution plane for determining whether a trust system actually deserves confidence. It pressure-tests specifications, implementations, deployments, compositions and changes against explicit propositions, scenarios, harms, controls and evidence.

RAHP is deliberately evidence-conservative:

- **missing evidence never becomes PASS**;
- workflow success is not assurance success;
- a component PASS does not imply a composition PASS;
- normative convergence does not silently become implementation conformance;
- identity or lineage evidence does not silently become authorization.

## Current release — v2.9.0 Common Windmill

v2.9.0 **Evidence-Qualified Impact, Source Authority and Reproducible Assurance** was published and qualified on 2026-10-22.

It preserves the stable v1 engine/result/evidence compatibility boundary while adding evidence-bounded people-impact pathways, stronger source-qualified corpus provenance, lifecycle/control-consequence assurance, source-pinned runtime and witness evidence, a derived assurance-registry index, reproducible release qualification, repository-native DCO enforcement and explicit licensing.

See [v2.9.0 release notes](docs/releases/v2.9.0.md), [qualification contract](method/v2.9-release-qualification.yaml), [release evidence](method/v2.9-release-evidence.json), and [GitHub Release v2.9.0](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/releases/tag/v2.9.0).

Independent external adoption remains **NOT_YET_TESTED**. Method qualification does not manufacture independently adjudicated causal harm claims, deployment certification or independent audit.

## Stable compatibility boundary

The compatibility authority for v2.9.0 remains:

```text
rahp-engine-contract-v1 revision 1.3
normalized result schema version 1
rahp-evidence-retention-v1
```

Existing conforming v2.8 consumers do not require a schema migration solely to consume v2.9.

## How RAHP works

A RAHP examination connects a bounded assurance question to attributable evidence:

```text
persona/scenario
  → harm/risk
  → proposition
  → control/guardrail
  → evidence
  → inference
  → actionable recommendation
```

A controller-driven assessment typically follows:

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

The controller, not GitHub workflow choreography, owns assurance state.

RAHP is **materiality-governed**: the preferred scope is the smallest scope that completely covers the materially affected proposition set. Broader execution is not inherently stronger assurance. Evidence that remains valid is retained with provenance; stale, invalidated or unavailable evidence stays explicit; and a full campaign or rebaseline is used when bounded reassessment cannot defend the current conclusion.

For the code-level reasoning model, see [RAHP reasoning architecture](docs/reasoning-architecture.md). For external agents and tool callers, see [agent integration guidance](docs/reasoning-integration.md). RAHP does not require an agent or LLM.

## Start adopting RAHP

**You can start with RAHP alone.** A first bounded review does not require DPIP, the Trust Protocol Interop Lab, the DTG deployment, or any portfolio-specific machinery.

Use the [Adoption gateway](docs/adoption-guide.md) to choose the smallest useful path:

- **RAHP-only:** configure one bounded subject and run a first review;
- **specialist assessment:** add a compatible specialist such as DPIP only when the proposition requires specialist semantics;
- **executable evidence:** add a compatible evidence producer only when the proposition requires that evidence class;
- **continuous assurance:** add freshness, reassessment, remediation and governed disposition after the first assessment.

For a maintained executable first exercise, use [Hello RAHP](examples/hello-rahp/README.md).

For consumer-facing interaction evidence, see [Consumer-interaction assurance](docs/consumer-interaction-assurance.md).

## Current capability boundary

Current portable capabilities include:

- multi-granularity assurance subjects;
- deterministic assessment identity and replay;
- clean-room execution;
- semantic `rahp-assurance-obligation/v1` records;
- evidence-producer routing and `rahp-evidence-producer-result/v1`;
- portable specialist contracts including `rahp-assessor-result/v1`;
- explicit PASS / FAIL / NOT_APPLICABLE / INDETERMINATE outcomes;
- evidence provenance, integrity and freshness;
- normative-versus-realization separation;
- materiality-bounded reassessment and full-campaign escalation;
- generic comparative assurance;
- agent authority, delegation and continuity checks;
- lifecycle-continuation authority;
- framework-neutral consumer-interaction evidence;
- bounded adversarial and observability-harm evaluation;
- governed remediation and retest lineage.

Optional reasoning surfaces remain bounded:

- [Evidence adequacy](docs/evidence-adequacy.md)
- [Temporal and provenance](docs/temporal-provenance.md)
- [Reproducibility and challenge](docs/reproducibility-challenge.md)
- [Worked R1–R3 reasoning example](docs/reasoning-worked-example.md)

These surfaces do not silently change terminal RAHP assurance semantics.

## Current architecture

RAHP has a portable method/engine core plus consumer-specific profiles, instances, corpora and worked assessments. The generic engine owns lifecycle, proposition/evidence contracts, inference boundaries and terminal assurance semantics; consumer material demonstrates those contracts without becoming a dependency of the core.

The **Bundled DTG exemplar** remains the deepest maintained portfolio demonstration and includes Credentials, Trust Tasks, ZKP/VDS, OpenVTC realization evidence and composition pressure tests. **CAWG/C2PA** remains a separate maintained consumer family demonstrating that the portable model is not DTG-specific. A2A, ARPA and other consumers exercise additional portability and composition surfaces.

DPIP is an independently governed privacy specialist that can return portable examination results to a compatible RAHP controller. The Trust Protocol Interop Lab is an independently governed evidence producer and composition-test environment. Neither repository is folded into RAHP authority: evidence and specialist results cross repository boundaries through explicit versioned contracts and provenance.

The [Eucalyptus clean-room campaign](docs/reports/eucalyptus-clean-room-2026-10-08.md) examines the coordinated `VTI-Eucalyptus` portfolio with fresh source-pinned evidence and explicit component/composition limits. Its execution and assurance outcomes are separate; historical PASS is not inherited.

VTI and other upstream specifications remain normative or conformance authorities for their own semantics. RAHP records independent assurance evidence and does not replace those authorities.

## Quick start

```bash
pip install -r requirements.txt
python3 tools/review.py --help
python3 tools/validate.py
```

Useful starting points:

- [How RAHP works](docs/how-rahp-works.md)
- [RAHP data model](docs/data-model.md)
- [Assurance registry](docs/assurance-registry.md) — derived machine-discovery index over the portable assurance catalogue
- [Getting started](docs/getting-started.md)
- [Continuous assurance](docs/continuous-assurance.md)
- [Adopting RAHP](ADOPTION.md)
- [Comparative assurance digest](docs/comparative-assurance-digest.md)

## Release lineage

| Version | Codename | Release boundary |
|---|---|---|
| v2.9.0 | **Common Windmill** | Evidence-Qualified Impact, Source Authority and Reproducible Assurance |
| v2.8.0 | **Common Birdwing** | Comparative, Adversarial and Consumer Interaction Assurance |
| v2.7.0 | **Common Rose** | Maintenance, Adoption and Optional Reasoning Profiles |
| v2.6.0 | **Commander** | Full-Stack Assurance Orchestration and Explicit Evidence State |
| v2.5.0 | **Psyche** | Continuous Realization Assurance and Portable Adoption |
| v2.4.0 | **Redbreast Jezebel** | VTI Composition Assessment and Evidence-Conservative Reconciliation |
| v2.3.0 | **Common Five-ring** | Portable Coverage and Source-Preserving Assurance |
| v2.2.0 | **Common Four-ring** | Evidence Production and Realization Assurance |
| v2.1.0 | **Common Acacia Blue** | Qualified Autonomous Assurance Plane |
| v2.0.0 | **Blue Mormon** | Portable Assurance Engine Stabilization |
| v1.9.0 | **Lesser Mime** | Historical qualified release |
| v1.8.0 | **Common Map** | Historical qualified release |
| v1.7.0 | **Common Palmfly** | Historical qualified release |
| v1.6.0 | **Common Earl** | Historical qualified release |
| v1.5.0 | **Purple Leaf Blue** | Historical qualified release |

Historical qualification records and release notes remain authoritative for what each earlier release established. Release codenames are presentation metadata; semantic versioning and contract identifiers remain the compatibility authority.

## Repository map

| Path | Role |
|---|---|
| `method/` | Portable lifecycle, catalogue, schemas, mappings, resilience method and release contracts. |
| `tools/` | Orchestration, autonomous control, validation, evidence routing and build tooling. |
| `profiles/<id>/` | Deployment configuration and capability/cross-spec registries. |
| `instances/<id>/` | Deployment-owned state and review records. |
| `clean-room/` | Declarative clean-room run specifications and qualification evidence. |
| `corpora/` | Scenario adapters mapped to portable stress patterns. |
| `examples/` | Worked assessments and portability/conformance fixtures. |
| `packages/` | TypeScript schema/core/graph/CLI reference implementation. |
| `docs/` | Guided documentation, architecture, runbooks and release notes. |

## AI-assisted use and accountability

AI systems may assist with review, change analysis, scenario generation, evidence organization and drafting. AI output is not, by itself, assurance evidence and does not become a durable finding without the applicable evidence and assurance contract. See [AI-assisted RAHP](docs/ai-assisted-process.md).

## License and provenance

RAHP Toolkit preserves its DTG origin as provenance while operating as an independently reusable assurance toolkit.

- **Documentation, methodology, assessment narratives and original non-code content:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Source code and executable tooling:** [Apache License, Version 2.0](LICENSE), including Python and TypeScript code, tests, automation and executable scripts.
- **Third-party or imported material:** remains subject to its original license, copyright notices and attribution requirements. This repository's licensing declaration does not relicense third-party content or override upstream rights.

For mixed-purpose files (including schemas, configuration, fixtures and machine-readable method records), applicable original notices and provenance take precedence. Original executable software components are Apache-2.0; original substantive method and assessment content is CC-BY-4.0. Preserve existing notices when reusing or modifying material.

SPDX identifiers: `Apache-2.0` and `CC-BY-4.0`.
