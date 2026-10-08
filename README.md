# RAHP Toolkit

**Risk Assessment & Harms Prevention**  
Release v2.7.0 · Common Rose · CC-BY 4.0

RAHP Toolkit is a reusable assurance method and execution plane for determining whether a trust system actually deserves confidence. It pressure-tests specifications, implementations, deployments, compositions and changes against explicit propositions, scenarios, harms, controls and evidence.

RAHP is deliberately evidence-conservative: **missing evidence never becomes PASS**. Workflow success is not assurance success. A component PASS does not imply a composition PASS, and normative convergence does not silently become implementation conformance.

## v2.7.0 — qualified release: maintenance and optional profiles

**Published and qualified on 2026-10-08.** v2.7.0 consolidates post-v2.6 maintenance of assessment ownership, routing and onboarding, alongside optional experimental sociotechnical and reasoning profiles. It retains the v2.6.0 stable engine, result and evidence-retention contracts.

- Assessment and queue-ownership reliability, standalone specification examination, and adoption guidance.
- Optional R1 evidence adequacy, R2 temporal provenance and R3 reproducibility/challenge profiles, with synthetic worked examples and an independent-consumer exercise kit.
- Independent adoption remains **NOT_YET_TESTED**. Optional profiles do not establish terminal assurance or independent reproduction.

The release security disposition was bounded and non-independent; documented residual risks were accepted for this release, not remediated or independently audited. See the [v2.7.0 release notes](docs/releases/v2.7.0.md), [qualification record](method/v2.7-release-qualification.yaml), [security disposition](docs/review/v27-release-security-disposition.md), and [GitHub release](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/releases/tag/v2.7.0).

## Stable foundation established in v2.6.0

v2.6.0 **Full-Stack Assurance Orchestration and Explicit Evidence State** made three claims independently inspectable: whether orchestration completed, what assurance outcome the evidence supports, and how mature that evidence is.

- explicit `process_state`, `assurance_state`, and `evidence_maturity` dimensions;
- explicit dispositions for RAHP, security, composition, DRARM, and specialist-assessment lenses;
- attributable required-evidence attempts using executed, attempted-unavailable, or no-applicable-producer states;
- evidence-required terminal indeterminacy rather than silent PASS;
- portable old/new producer-consumer version-skew propositions;
- reusable privacy/correlation risk, guardrail, and control mechanisms;
- exact-snapshot portfolio assurance binding and tighter DTG/VSC routing;
- measured performance characterization and semantic-preserving execution optimization;
- LPC pre-demo scope/evidence/assurance artifacts that informed the generic full-stack contract without becoming a core dependency.

Policy-as-assurance-subject work under #662/#667 and decision-resolution research under PR #817 remain experimental and are not part of the v2.6.0 stable boundary.

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

RAHP is **materiality-governed**: the preferred assurance scope is the smallest scope that completely covers the materially affected proposition set. Broader execution is not inherently stronger assurance. Evidence that remains valid is retained with provenance; stale, invalidated or unavailable evidence stays explicit; and a full campaign/rebaseline is used when bounded reassessment cannot defend the current conclusion.

For a code-level explanation of where assessment reasoning occurs, see [RAHP reasoning architecture](docs/reasoning-architecture.md). For external agents and tool callers, see [agent integration guidance](docs/reasoning-integration.md). RAHP can be used without an agent or LLM.

The optional [evidence adequacy profile](docs/evidence-adequacy.md) experiments with deterministic sufficiency and contradiction semantics; it does not change stable assessor or controller contracts.

The experimental [temporal and provenance profile](docs/temporal-provenance.md) evaluates claimed historical applicability and as-known-at cutoffs without changing controller or assessor contracts.

The optional [R3 reproducibility and challenge profile](docs/reproducibility-challenge.md) compares declared runs and preserves open challenges without changing assurance outcomes.

A runnable [R1–R3 worked reasoning example](docs/reasoning-worked-example.md) demonstrates bounded evidence adequacy, historical applicability and challenge handling with deterministic tests.

For independent evaluation, use the [R1–R3 adoption exercise](docs/reasoning-adoption-exercise.md), [evidence record](docs/reasoning-adoption-record.md), and [release-readiness decision record](docs/reasoning-release-readiness.md). These distinguish internal checks from external consumer evidence.

## Start adopting RAHP

**You can start with RAHP alone.** A first bounded review does not require DPIP, the Trust Protocol Interop Lab, the DTG deployment, or any portfolio-specific machinery.

Use the [Adoption gateway](docs/adoption-guide.md) to decide which path fits your assurance question:

- **RAHP-only:** configure one bounded subject and run a first review;
- **specialist assessment:** add a compatible specialist such as DPIP only when the proposition requires specialist semantics;
- **executable evidence:** add a compatible evidence producer such as the Trust Protocol Interop Lab only when the proposition requires that evidence class;
- **continuous assurance:** add freshness, reassessment, remediation and governed disposition after the first assessment.

For a maintained executable first exercise, use [Hello RAHP](examples/hello-rahp/README.md).


## Current capability boundary

Current capabilities include multi-granularity assurance subjects; deterministic assessment identity and replay; clean-room execution; semantic `rahp-assurance-obligation/v1` records; evidence-producer routing; portable specialist contracts including `rahp-assessor-result/v1`; durable specialist returns; explicit PASS/FAIL/NOT_APPLICABLE/INDETERMINATE outcomes; materially equivalent machine/human terminal records; evidence provenance and freshness; normative-versus-realization separation; action-target precision; human-harm traceability; source-pinned corpora; generic capability coverage; resilience proposition/evidence routing; materiality-bounded reassessment; and governed continuous reassessment with explicit full-campaign escalation when warranted.

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

## Coordinated portfolio context

v2.7.0 preserves Full-Stack Assurance Orchestration and Explicit Evidence State as the stable RAHP product foundation. VTI and other upstream specifications remain normative/conformance authorities for their own semantics; RAHP records independent assurance evidence. DPIP remains the specialist privacy authority for composed privacy questions routed to it.

DPIP and the Trust Protocol Interop Lab remain independently governed collaborators. Consult each repository’s release records for current versions. The repositories are joined only through explicit contracts, source-pinned evidence and bounded hand-offs. A matching date or green workflow is not a compatibility or assurance claim.

The v2.7.0 release retains the stable v1 engine/result/evidence contracts and adds optional experimental profiles and adoption material without making those profiles part of terminal assurance.

## Quick start

```bash
pip install -r requirements.txt
python3 tools/review.py --help
python3 tools/validate.py
```

Start with [How RAHP works](docs/how-rahp-works.md), [RAHP data model](docs/data-model.md), [Getting started](docs/getting-started.md), [Continuous assurance](docs/continuous-assurance.md), and [Adopting RAHP](ADOPTION.md).

## Current release

v2.7.0 **Common Rose** (*Pachliopta aristolochiae*) is the current **published and qualified** release. It retains the v2.6 stable assurance contracts and adds maintenance, adoption guidance, and optional experimental profiles. R1–R3 and sociotechnical assurance do not change terminal assurance semantics; independent adoption remains **NOT_YET_TESTED**.

- [v2.7.0 release notes](docs/releases/v2.7.0.md)
- [v2.7.0 qualification contract](method/v2.7-release-qualification.yaml)
- [v2.7.0 release evidence](method/v2.7-release-evidence.json)
- [v2.7.0 security disposition](docs/review/v27-release-security-disposition.md)
- [GitHub Release v2.7.0](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/releases/tag/v2.7.0)
- [VTI assessment index](docs/vti-assessment-index.md)
- [VTI programme reconciliation](docs/vti-programme-reconciliation.md)
- [Project status](PROJECT-STATUS.yaml)
- [Roadmap](ROADMAP.md)
- [Release history](CHANGELOG.md)

Historical release records remain immutable. Release presentation metadata follows the governed West Bengal butterfly naming policy; semantic versioning and contract identifiers remain the compatibility authority.

## Release lineage

| Version | Codename | Release boundary |
|---|---|---|
| v2.7.0 | **Common Rose** | Qualified maintenance and optional experimental profiles |
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
