# RAHP Toolkit

**Risk Assessment & Harms Prevention**  
Release v2.4.0 (stable) · Redbreast Jezebel · CC-BY 4.0

RAHP Toolkit is a reusable assurance method and execution plane for determining whether a trust system actually deserves confidence. It pressure-tests specifications, implementations, deployments, compositions and changes against explicit propositions, scenarios, harms, controls and evidence.

RAHP is deliberately evidence-conservative: **missing evidence never becomes PASS**. Workflow success is not assurance success. A component PASS does not imply a composition PASS, and normative convergence does not silently become implementation conformance.

## What v2.4.0 adds

v2.4.0 **VTI Composition Assessment and Evidence-Conservative Reconciliation** extends the v2.3 baseline with:

- a version-pinned VTI composition assessment profile;
- a machine-readable `rahp-vti-assessment/v1` submission contract;
- reusable validation across multiple VTI assessment families;
- deterministic assessment-index and programme-reconciliation surfaces;
- eight current supported VTI composition families with bounded executable evidence;
- a deliberately `indeterminate` privacy-composition assessment that preserves the specialist DPIP boundary;
- an explicit component-substitution evidence gate that refuses synthetic closure;
- first-class indeterminacy and material-configuration reassessment semantics;
- a deduplicated upstream clarification package that preserves VTI normative authority.

The release does **not** claim universal VTI conformance, complete privacy assurance, or successful component substitution without genuine implementation-pair evidence.
## How RAHP works

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

## Current capability boundary

Current capabilities include multi-granularity assurance subjects; deterministic assessment identity and replay; clean-room execution; semantic `rahp-assurance-obligation/v1` records; evidence-producer routing; portable specialist contracts including `rahp-assessor-result/v1`; durable specialist returns; explicit PASS/FAIL/NOT_APPLICABLE/INDETERMINATE outcomes; materially equivalent machine/human terminal records; evidence provenance and freshness; normative-versus-realization separation; action-target precision; human-harm traceability; source-pinned corpora; generic capability coverage; resilience proposition/evidence routing; and governed continuous reassessment.

The stable compatibility authority remains:

```text
rahp-engine-contract-v1 revision 1.3
normalized result schema version 1
rahp-evidence-retention-v1
```

## Current architecture

RAHP has a portable method/engine core plus consumer-specific profiles, instances, corpora and worked assessments. The generic engine owns lifecycle, proposition/evidence contracts, inference boundaries and terminal assurance semantics; consumer material demonstrates those contracts without becoming a dependency of the core.

The **Bundled DTG exemplar** remains the deepest maintained portfolio demonstration and includes Credentials, Trust Tasks, ZKP/VDS, OpenVTC realization evidence and composition pressure tests. **CAWG/C2PA** remains a separate maintained consumer family demonstrating that the portable assurance model is not DTG-specific. A2A, ARPA and other consumers exercise additional portability and composition surfaces.

DPIP is an independently governed privacy specialist that can return portable examination results to a compatible RAHP controller. The Trust Protocol Interop Lab is an independently governed evidence producer and composition-test environment. Neither repository is folded into RAHP authority: evidence and specialist results cross repository boundaries through explicit versioned contracts and provenance.

## Coordinated release context

v2.4.0 packages the completed VTI assessment programme as an additive RAHP product capability. VTI remains the normative and conformance authority; RAHP records independent assurance evidence. DPIP remains the specialist privacy authority for the composed privacy questions routed to it.

## Quick start

```bash
pip install -r requirements.txt
python3 tools/review.py --help
python3 tools/validate.py
```

Start with [How RAHP works](docs/how-rahp-works.md), [Getting started](docs/getting-started.md), [Continuous assurance](docs/continuous-assurance.md), and [Adopting RAHP](ADOPTION.md).

## Current release

v2.4.0 **Redbreast Jezebel** (*Delias acalis*) is the stable **VTI Composition Assessment and Evidence-Conservative Reconciliation** release.

- [v2.4.0 release notes](docs/releases/v2.4.0.md)
- [v2.4 qualification contract](method/v2.4-release-qualification.yaml)
- [VTI assessment index](docs/vti-assessment-index.md)
- [VTI programme reconciliation](docs/vti-programme-reconciliation.md)
- [Project status](PROJECT-STATUS.yaml)
- [Roadmap](ROADMAP.md)
- [Release history](CHANGELOG.md)

Historical release records remain immutable. Release presentation metadata follows the governed West Bengal butterfly naming policy; semantic versioning and contract identifiers remain the compatibility authority.

## Release lineage

| Version | Codename | Historical boundary |
|---|---|---|
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

The table preserves release identity only; historical qualification records and release notes remain authoritative for what each earlier release actually established.

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

RAHP Toolkit preserves its DTG origin as provenance while operating as an independently reusable assurance toolkit. **CC-BY 4.0 — reuse with attribution.**
