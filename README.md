# RAHP Toolkit

**Risk Assessment & Harms Prevention**  
Release v1.6.0 (stable) · Common Earl · CC-BY 4.0

RAHP Toolkit is a **portable specification-assurance toolkit** for pressure-testing standards, protocols, implementations and composed systems against human harms, governance failures, adversarial conditions and resilience risks.

> **Project identity:** RAHP Toolkit is the portable method and engine contract. DTG, CAWG/C2PA, OpenVTC, ARPA and other portfolios or projects are independently scoped deployments and examples. No deployment defines the portable method for another adopter. The **Bundled DTG exemplar** is project provenance and an exercised deployment, not a core dependency.

## What RAHP does

RAHP helps an implementer, maintainer or reviewer turn a broad question such as “what could go wrong here?” into reproducible assurance evidence. It provides:

- **scenario-driven pressure testing** against harms, adversarial conditions and governance failure;
- a **portable assurance catalogue** linking harm, risk, control, guardrail, assurance and evidence patterns;
- **source-pinned corpora** and cross-specification scenarios for repeatable coverage;
- **evidence classification and closure rules** so cryptographic or structural validity is not mistaken for sufficient assurance;
- **durable remediation and retest lineage** when targets, evidence or controls change; and
- **continuous governed assurance** through freshness, impact analysis, policy gates, scoped authority and current posture.

RAHP is deliberately evidence-conservative: **zero findings is not equivalent to assured**. A target can have no confirmed findings while still carrying assurance gaps, unresolved review obligations or insufficient evidence.

## Current architecture

```text
target revision
  → scenarios and evidence
  → risks / harms / controls / guardrails
  → assurance evaluation
  → finding | gap | controlled | assured
  → remediation
  → retest and assurance delta
  → governed disposition
  → current assurance posture
```

The portable method is shared; deployment context remains independent. Structured method data is authoritative, while Markdown, JSON, JSON-LD and rendered site views are publication surfaces.

For the full conceptual walkthrough, see [How RAHP works](docs/how-rahp-works.md). For the operational lifecycle, see [Continuous assurance](docs/continuous-assurance.md).

## Quick start

```bash
pip install -r requirements.txt
python3 tools/review.py --help
python3 tools/validate.py
```

For a guided first run, configuration examples and the wider command set, use [Getting started](docs/getting-started.md). For repository internals, validation, the engine contract and the TypeScript implementation, use the [Developer guide](docs/developer-guide.md).

## Choose your path

| I want to… | Start here |
|---|---|
| Understand RAHP | [How RAHP works](docs/how-rahp-works.md) |
| Run my first assessment | [Getting started](docs/getting-started.md) |
| Pressure-test a specification | [Pressure-testing a specification](docs/pressure-testing-a-spec.md) |
| Test multiple specifications together | [Cross-spec pressure testing](docs/cross-spec-pressure-testing.md) |
| Browse scenario coverage | [Scenario corpora](docs/scenario-corpora.md) and [corpora browser](corpora/) |
| Interpret findings and assurance states | [Interpreting results](docs/interpreting-results.md) |
| Understand continuous reassessment | [Continuous assurance](docs/continuous-assurance.md) |
| Adopt RAHP for another project | [Adopting RAHP](ADOPTION.md) and [Configuration](docs/configuration.md) |
| Browse reusable assurance patterns | [Portable catalogue](method/catalogue/) |
| Develop or integrate the toolkit | [Developer guide](docs/developer-guide.md) |
| Contribute | [How to contribute](docs/how-to-contribute.md) and [CONTRIBUTING.md](CONTRIBUTING.md) |

## Scenario and assurance coverage

The reusable catalogue under `method/catalogue/` currently contains **162 portable assurance patterns** across harms, risks, controls, guardrails, assurance tests and evidence patterns.

The packaged scenario adapters expose **182 scenario test vectors across 14 corpora and 28 portable scenario patterns**. They include source-pinned Trust Tasks and DTG Credential Specification corpora, their composed seam corpus, DTG ZKP, CAWG/C2PA and smaller interface-baseline/composed adapters. A larger corpus broadens review coverage; it does not by itself establish that a target is safe or conformant.

See [Scenario corpora](docs/scenario-corpora.md) for provenance, coverage maps and maintenance rules.

## Current release

v1.6.0 **Common Earl** (*Tanaecia julii*) is the stable release of **Source-Pinned Coverage and Guided Adoption**. It preserves the stable v1 compatibility boundaries:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.6.0 qualifies the expanded source-pinned corpora, dependent-corpus recomposition and evidence-backed TT×CredSpec reassessment, while retaining the v1.5 Continuous Governed Assurance contracts. Maintained example baselines are not promoted merely because the toolkit version changes; they advance through their own retest or reassessment evidence.

Useful release surfaces:

- [v1.6.0 release notes](docs/releases/v1.6.0.md)
- [v1.6 qualification contract](method/v1.6-release-qualification.yaml)
- [Project status](PROJECT-STATUS.yaml)
- [Roadmap](ROADMAP.md)
- [Getting started](docs/getting-started.md)
- [Developer guide](docs/developer-guide.md)
- [Continuous assurance](docs/continuous-assurance.md)
- [Release history](CHANGELOG.md)

From v1.5.0 onward, release presentation metadata follows the [West Bengal butterfly naming policy](docs/release-naming.md); semantic versioning remains the compatibility authority.

## Repository map

| Path | Role |
|---|---|
| `method/` | Portable lifecycle, catalogue, schemas, glossary, mappings, qualification and engine/version contracts. |
| `tools/` | Portable orchestration, validation, monitoring, rendering, posture and build tooling. |
| `profiles/<id>/` | Deployment configuration and cross-specification registries. |
| `instances/<id>/` | Deployment-owned state, review records and local assurance vocabulary. |
| `corpora/` | Scenario adapters mapped to portable stress patterns. |
| `examples/` | Curated worked assessments and portability/conformance fixtures. |
| `packages/` | TypeScript schema/core/graph/CLI reference implementation. |
| `build/` | Generated evidence and publication views; do not hand-edit. |
| `docs/` | Guided documentation, reference material, runbooks and release notes. |
| `archive/` | Historical provenance; not current authority. |

## AI-assisted use and accountability

AI systems may assist with review, change analysis, scenario generation, evidence organization and drafting. AI output is not, by itself, assurance evidence and does not become a durable finding without review. See [AI-assisted RAHP](docs/ai-assisted-process.md).

## License and provenance

RAHP Toolkit preserves its DTG origin as provenance while operating as an independently reusable assurance toolkit.

**CC-BY 4.0 — reuse with attribution.**
