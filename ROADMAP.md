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
## Completed post-v2.4 operating-model work

After the v2.4.0 release boundary, RAHP completed a materiality-governed execution tranche without changing the stable engine/result/evidence compatibility contracts.

- Cross-specification execution can now be selected by materiality rather than treating every runnable composition as routine.
- The bundled DTG profile distinguishes routinely material, conditionally material and reference evidence surfaces while preserving every runnable composition for explicit rebaseline/campaign use.
- Full campaign capability remains available, but it is an escalation/rebaseline mechanism rather than the default path after every change.
- The 2026-09-24 DTG/VTC current-pin rebaseline preserves the August assessments as historical lineage and establishes a new comparison point for future selective execution.
- Scheduled/recovery and benchmark execution was rationalised without weakening evidence requirements or converting non-execution into PASS.

The governing principle is that **assurance quality depends on complete coverage of the materially affected proposition set, not on maximizing execution breadth**.

## Post-v2.4 execution programme

The current programme is tracked by [#800](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/800): **Continuous Realization Assurance and Portable Adoption**. It converts the strategic post-v2.4 direction into evidence-gated engineering work without pre-committing to a v2.5.0 release.

### G1 — realization conformance

Selectively close the gap between adopted/current semantics and runtime realization evidence. Durable residual owners remain authoritative rather than being duplicated. The first programme set is #799, #609, #691, #797 and #690.

A proposition closes only when current source-pinned evidence supports a bounded disposition. A missing implementation surface or unresolved external dependency remains `EVIDENCE_REQUIRED`, `INDETERMINATE` or waiting-external with an explicit reassessment trigger.

### G2 — longitudinal observability and telemetry

Add assurance-safe operational telemetry for controller and reassessment execution: run identity, elapsed time, selected scope, retained/weakened/invalidated evidence counts where available, phase timings, terminal outcome distribution and explicit blocker/indeterminate reasons.

Telemetry describes how assurance work executed. It is **not** target assurance evidence, cannot create PASS, and must not become an independent assurance state machine.

### G3 — performance engineering

Use the versioned execution benchmark contract to measure and reduce avoidable work while preserving semantic outputs, evidence lineage and complete coverage of the materially affected proposition set.

Optimization priorities include repeated parsing/validation, duplicate setup, unaffected execution, unnecessary regeneration and evidence recomputation. Performance policy should detect meaningful regression without making wall-clock noise an assurance result.

### G4 — portable adoption proof

Exercise the stable generic RAHP contracts against a non-DTG consumer without importing target-specific vocabulary into the portable core. The proof must include a bounded assessment, explicit evidence obligation, material-change reassessment, terminal posture and residual ownership.

### G5 — documentation and compatibility audit

Keep README, adoption, operational, performance and specialist/evidence-producer guidance aligned with the actual implementation. The current coordinated portfolio boundary is RAHP v2.4.0, DPIP v0.3.0 and Trust Protocol Interop Lab v0.7.0; versions remain independently governed.

Policy-as-subject research (#662/#668) continues as a separate experimental lane until its own evidence supports a stable-integration decision.

### G6 — release judgment

After G1–G5, make an evidence-backed release judgment. Cut v2.5.0 only if the completed work establishes a coherent new stable capability boundary. Issue count, elapsed time and cleanup volume are not release criteria.

### Engineering requirements across all gates

- documentation changes accompany user/operator-visible behavior;
- code changes include regression tests;
- telemetry and performance metrics remain operational evidence rather than target assurance evidence;
- performance optimizations preserve normalized semantics and lineage;
- issue → branch → PR → required checks → merge remains the default change path;
- full campaign/rebaseline remains available when materiality-bounded reassessment cannot defend the current conclusion.

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
- Broader execution is not treated as stronger assurance by definition; reassessment scope follows material proposition coverage.
- Non-selected evidence is never silently refreshed or promoted to PASS.

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
