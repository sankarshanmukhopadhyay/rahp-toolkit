---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Releases
---
# RAHP roadmap

## Current release boundary — v2.4.0 Redbreast Jezebel

v2.4.0 packages **VTI Composition Assessment and Evidence-Conservative Reconciliation** on top of the v2.3 portable-coverage baseline. It establishes a reusable, source-pinned assessment programme with machine-readable submissions, executable family evidence, deterministic reconciliation and explicit residual states.

The release qualifies eight supported VTI composition families while preserving two bounded residuals: privacy remains specialist-evidence-required with an indeterminate assessment, and component substitution remains evidence-required pending genuine implementation-pair evidence.

## Completed v2.4 tranche

1. **Assessment profile and contract:** version-pinned VTI profile plus `rahp-vti-assessment/v1` submission contract.
2. **Reusable evidence pipeline:** multi-submission validation, exact family mapping, source-pin consistency and reassessment semantics.
3. **Eight supported families:** semantic completion, authority, lifecycle, delegation, false independence, indeterminacy, configuration materiality and human control.
4. **Truthful residuals:** privacy remains indeterminate; substitution remains evidence-required.
5. **Programme reconciliation:** deterministic family-level reconciliation and release/upstream packaging judgment.

## Capability continuity retained in v2.4

The release preserves the capabilities established in earlier qualified tranches while extending their VTI composition-assessment surfaces:

- **Durable assessment and finding lineage** keeps terminal findings and their provenance inspectable across reassessment and source changes.
- **Governed remediation and retest** preserves explicit remediation authority, closure evidence and retest lineage.
- **Assurance graph and impact analysis** keeps dependency-aware change impact deterministic rather than inferred from repository activity alone.
- **Evidence provenance, freshness and delta** preserves source identity, freshness semantics and explicit assurance-state transition evidence.
- **Executable authority and policy gates** keep scope, revocation posture and PASS/FAIL/INDETERMINATE semantics machine-checkable.
- **Portfolio and deployment presentation** remains a presentation layer over bounded assurance state rather than an alternative source of truth.
- **Release qualification** remains an executable gate binding declared version, compatibility contracts, release notes and qualification evidence.
## Post-v2.4 priorities

1. **Realization conformance:** selectively retest when adopted normative semantics become implemented.
2. **Deferred evidence triggers:** reactivate portability/substitution and other deferred propositions only when genuine independently meaningful implementations or deployments exist.
3. **Adoption and portability:** qualify additional non-DTG consumers against unchanged generic contracts.
4. **Specialist ecosystem:** add specialists through versioned contracts/shared fixtures rather than target-specific core logic.
5. **Operational observability:** improve controller telemetry, longitudinal posture and evidence freshness without conflating workflow success with assurance success.
6. **Composition pressure testing:** expand end-to-end flow coverage and redress/continuity surfaces while preserving component/composition boundaries.
7. **Resilience evidence depth:** exercise higher DRARM assurance levels with attributable runtime and operational evidence producers.

## Non-regression rules

- No human-only controller transition.
- Missing evidence never becomes PASS.
- Workflow success never substitutes for assurance success.
- Model and evidence gaps remain explicit residuals.
- Replay remains idempotent; new pins create lineage.
- Static/source, synthetic, runtime and governance evidence remain distinct.
- Normative convergence never silently becomes implementation conformance.
- Component PASS never implies composition PASS.
- Source findings are not silently reinterpreted to fit a local catalogue.
- Generic RAHP core remains independent of DTG, OpenVTC, CAWG, A2A or any other consumer vocabulary.

## Historical roadmap

The named release lineage is retained because each release validator treats those identities as part of the public compatibility history:

- v2.3.0 — **Common Five-ring** — Portable Coverage and Source-Preserving Assurance
- v2.2.0 — **Common Four-ring** — Evidence Production and Realization Assurance
- v2.1.0 — **Common Acacia Blue** — Qualified Autonomous Assurance Plane
- v2.0.0 — **Blue Mormon** — Portable Assurance Engine Stabilization
- v1.9.0 — **Lesser Mime** — historical qualified boundary
- v1.8.0 — **Common Map** — historical qualified boundary
- v1.7.0 — **Common Palmfly** — historical qualified boundary
- v1.6.0 — **Common Earl** — historical qualified boundary
- v1.5.0 — **Purple Leaf Blue** — historical qualified boundary

Historical release notes and qualification records remain evidence rather than being rewritten into the current roadmap.
