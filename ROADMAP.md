---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Releases
---
# RAHP roadmap

## Current release — v2.7.0 Common Rose

**Published and qualified on 2026-10-08.** v2.7.0 advances assessment routing, queue reliability, onboarding and adoption guidance, with optional experimental R1–R3 reasoning profiles. The stable engine contract v1 revision 1.3, result schema 1 and evidence-retention v1 remain unchanged. Independent adoption remains NOT_YET_TESTED; optional profiles do not imply terminal assurance.

Post-release security hardening and deployment-specific evidence are tracked in [#958](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/958). That follow-up does not alter the historical v2.7.0 release decision or tag.

## Current release boundary — v2.7.0 Common Rose

v2.7.0 retains **Full-Stack Assurance Orchestration and Explicit Evidence State** from v2.6.0 while adding bounded post-v2.6 capabilities.

The release keeps the stable engine/result/evidence compatibility families unchanged while making orchestration completion, assurance outcome, and evidence maturity independently observable. Every configured material assurance lens must receive an explicit disposition, and every declared required evidence obligation must have an attributable attempt state.

## Completed v2.6 tranche

1. **Full-stack state:** process, assurance, and evidence-maturity dimensions are explicit and independently inspectable.
2. **Lens disposition:** RAHP, security, composition, DRARM, and specialist lenses cannot silently disappear from a configured full-stack campaign.
3. **Evidence attempts:** required evidence is attributable as executed, attempted-unavailable, or no-applicable-producer; omission is an orchestration defect.
4. **Composition and resilience:** portable version-skew propositions and explicit DRARM applicability prevent component success or workflow completion from standing in for composition/resilience assurance.
5. **Privacy depth:** reusable correlation, status-observability, downstream-purpose, privacy-subversion, and retention-concentration mechanisms are represented in the portable catalogue.
6. **Execution evidence:** profiling, scale characterization, batching, and the native-kernel decision are evidence-backed and remain operational engineering evidence rather than target assurance evidence.
7. **Research separation:** policy-as-subject #662/#667 and decision-resolution PR #817 remain experimental.

## Current operating model

RAHP remains materiality-bounded and evidence-conservative. Broader execution is not inherently stronger assurance. A completed campaign may legitimately remain INDETERMINATE; uncertainty is a valid terminal assurance condition when it is explicit, attributable, and bounded.

## Current portfolio context

- RAHP v2.7.0;
- DPIP v0.3.0;
- Trust Protocol Interop Lab v0.7.0.

These repositories remain independently versioned and governed. Compatibility is contract- and evidence-based, not date-based.

## Capability continuity retained in v2.6

The v2.6 operating model is additive and retains the previously qualified capability families:

- **Durable assessment and finding lineage** preserves assessment identity, finding lineage, and canonical identity across source changes and reassessment.
- **Governed remediation and retest** preserves remediation authority, acceptance criteria, closure evidence, and retest lineage.
- **Assurance graph and impact analysis** keeps dependency-aware reachability and retest selection explicit.
- **Evidence provenance, freshness and delta** preserves source identity, freshness state, and assurance delta rather than silently reusing stale evidence.
- **Executable authority and policy gates** keep authority scope, revocation, and policy evaluation separately inspectable with INDETERMINATE preserved as a real outcome.
- **Portfolio and deployment presentation** projects bounded operational posture without becoming an alternative assurance source of truth.
- **Release qualification** continues to bind declared version, qualification contract, release decision, release-cut evidence, and governed publication.

These capability names are retained because they remain registered stable capabilities; v2.6 extends rather than replaces them.

## Post-v2.7 priorities

Complete the security and privacy hardening and evidence follow-up tracked in [#958](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/958). Future assurance work should remain trigger-driven rather than release-driven: reassess waiting-external/evidence-required owners when their evidence trigger fires; deepen non-DTG adoption and higher-level resilience evidence; continue measured performance work only where semantic equivalence is preserved; and keep experimental research behind explicit graduation gates.

## Non-regression rules

- No human-only controller transition.
- Missing evidence never becomes PASS.
- Workflow success never substitutes for assurance success.
- Process completion never substitutes for explicit material-lens disposition.
- Required evidence attempts remain attributable.
- Applicable unexecuted lenses remain INDETERMINATE rather than PASS.
- DRARM silence is invalid where resilience is material.
- Component PASS never implies composition PASS.
- Normative convergence never silently becomes implementation conformance.
- Non-selected evidence is never silently refreshed or promoted to PASS.
- Generic RAHP core remains independent of consumer vocabulary.
- Experimental research is never silently graduated.

## Historical roadmap

The named release lineage is retained because each release validator treats those identities as part of the public compatibility history:

- v2.4.0 — **Redbreast Jezebel** — VTI Composition Assessment and Evidence-Conservative Reconciliation
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
