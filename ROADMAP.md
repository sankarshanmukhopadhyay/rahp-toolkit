---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Reference
---
# RAHP Toolkit Roadmap

This roadmap records the current portable RAHP direction. Historical pre-v1.2 roadmap material is preserved under `archive/pre-v1.2/` and is not current authority.

## v1.6.0 — Source-Pinned Coverage and Guided Adoption (stable release)

Status: **stable public release — Common Earl (*Tanaecia julii*)**.

v1.6 strengthens RAHP's reproducibility and usability without changing the stable v1 compatibility boundary. It makes scenario growth source-pinned and coverage-driven, preserves reassessment lineage across corpus change, and gives adopters clearer first-run, developer and continuous-assurance entry points.

### Delivered workstreams

1. **Source-pinned corpus expansion**
   - Trust Tasks and DTG Credential Specification corpora are pinned to immutable current source revisions;
   - both primary corpora expand from 16 to 30 scenarios;
   - machine-readable coverage maps make missing pressure dimensions visible.

2. **Composed seam reassessment**
   - Trust Tasks × Credential Specification coverage expands from 12 to 20 scenarios;
   - the pre-expansion assessment is preserved as durable lineage;
   - the current assessment is rerun against the new source pins rather than merely relabelled.

3. **Coverage discipline**
   - packaged coverage is 182 scenario vectors across 14 corpora and 28 portable scenario patterns;
   - scenario-count growth does not itself create findings or establish assurance;
   - the affected TT×CredSpec residuals are refined by current evidence rather than multiplied mechanically.

4. **Guided adoption and developer routing**
   - the root README is a stable front door;
   - `docs/getting-started.md` provides the first-run route;
   - `docs/developer-guide.md` routes repository validation, engine and integration work;
   - `docs/continuous-assurance.md` routes the v1.5 operational assurance capabilities without duplicating their authoritative topic pages.

5. **Release qualification and publication**
   - `method/v1.6-release-qualification.yaml` defines the v1.6 release boundary;
   - `tools/validate_v16_release.py` verifies source pins, coverage, reassessment lineage, documentation routing, workspace synchronization and compatibility;
   - the qualified publication workflow revalidates the exact main-branch release commit before creating `v1.6.0` and the GitHub Release.

### Baseline policy

A toolkit release does not automatically requalify maintained external targets. The maintained-example registry remains at its separately evidenced v1.5.0 baselines until each example is independently reassessed or retested. Historical records remain immutable lineage evidence.

## v1.5.0 — Continuous Governed Assurance

v1.5 turned evidence-driven point-in-time assessment into durable, continuously governed assurance while preserving deployment independence. It delivered durable assessment/finding lineage, governed remediation and retest, assurance graph and impact analysis, evidence provenance/freshness/delta, executable authority and policy gates, portable assurance posture and machine-verifiable release qualification.

The v1.5 lifecycle remains part of v1.6:

```text
material target change
        ↓
impact selection
        ↓
freshness evaluation
        ↓
evidence retained / weakened / invalidated
        ↓
assessment or retest
        ↓
assurance delta
        ↓
residual obligation + remediation
        ↓
policy gate: PASS | FAIL | INDETERMINATE
        ↓
independent authority verification
        ↓
governed disposition/publication
        ↓
portable assurance posture
```

See [v1.5.0 release notes](docs/releases/v1.5.0.md) and [Continuous assurance](docs/continuous-assurance.md).

## Compatibility

The stable v1 compatibility boundaries remain:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.6.0 is additive within that boundary. Existing normalized results remain valid.

See [v1.6.0 release notes](docs/releases/v1.6.0.md) and the [v1.6 qualification contract](method/v1.6-release-qualification.yaml).

## v1.2.0 — Evidence-Driven Assurance

v1.2 established typed assurance conclusions, first-class control credit, evidence classification, explicit zero-finding semantics, governed remediation/retest records, DRARM mappings, and Python/TypeScript conformance.

See [v1.2.0 release notes](docs/releases/v1.2.0.md).

## Future work

Subsequent v1.x releases may refine implementation, adoption, corpus coverage and operational tooling without breaking the stable v1 contracts. Each v1.5.0-and-later release receives its own randomly selected West Bengal butterfly release name at release time.

A v2 release is required for breaking changes to the stable method or normalized-result compatibility boundary.

## Explicit non-goals

RAHP does not make these default behaviours:

- automatic filing into arbitrary upstream repositories;
- treating repository permissions as governance authority;
- treating a policy-gate PASS as delegation, publication authority or risk acceptance;
- equating detector absence with assurance;
- coupling portable core to a maintained deployment;
- using a universal assurance score to hide materially different states.

## Historical roadmap

The full pre-v1.2 roadmap is retained at `archive/pre-v1.2/ROADMAP-pre-v1.2.txt`.
