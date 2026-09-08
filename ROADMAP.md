---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Releases
---
# RAHP roadmap

## Current release boundary — v2.2.0 Common Four-ring

v2.2.0 packages **Evidence Production and Realization Assurance** on top of the stable v2.1 autonomous assurance lifecycle. The release makes semantic evidence/remediation obligations, producer ownership, provenance routing and realization/runtime evidence boundaries first-class without changing the stable engine/result/evidence compatibility authorities.

First-class capabilities now include:

- **Durable assessment and finding lineage** — extended in v2.2 with semantic assurance-obligation lineage.
- **Governed remediation and retest**
- **Assurance graph and impact analysis**
- **Evidence provenance, freshness and delta** — extended in v2.2 with accountable evidence production and producer routing.
- **Executable authority and policy gates** — extended in v2.2 with composition and realization pressure testing.
- **Normative-versus-realization separation**
- **Portfolio and deployment presentation**
- **Release qualification**

## Current development boundary — v2.3.0 unreleased

The current development target is **v2.3.0**. The release is intentionally held while the two durable residual owners created by the 2026-09-08 convergence/evidence tranche reach stable dispositions:

- [#481](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/481) — Data Rooms implementation/runtime/deployment evidence maturity;
- [#482](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/482) — WD02 common-control/same-subject proof semantics.

This is a release-management boundary, not an assurance shortcut: neither issue has to be forced to GREEN. Each must instead reach a stable, source-backed disposition that makes the remaining external or deployment dependency explicit.

## Completed post-v2.2 tranche

The first two former post-release priorities are now materially complete for the currently exposed implementation surfaces:

1. **Runtime/action-time evidence:** current VDC × VAC × Trust Task composition was executed and reconciled. Missing exact current-authority evaluation remains explicit as `INDETERMINATE/BLOCKED` rather than being inferred from credential/task validity.
2. **Privacy runtime evidence:** attributable OpenVTC A/B evidence now covers relationship/verifier, status, Trust Task and policy-discovery surfaces. DPIP returned a bounded SATISFIED result for the exercised runtime scope without claiming deployment-wide unlinkability.
3. **WD02 convergence and composition:** adopted WD02 source is pinned and reconciled; fresh VDC × VAC and common-control negative evidence exists; the unresolved normative common-control primitive is isolated under #482.
4. **Data Rooms capability/evidence:** the architectural proposition catalogue is canonical under `profiles/dtg/coverage/data-rooms.yaml`; current target-native OpenVTC room evidence advanced the propositions that the implementation can presently support; remaining gaps are isolated under #481 rather than treated as missing RAHP-core capability.

## Current priorities

1. **Stabilize #481:** reassess only when private-room ZK execution, witnessed anchoring/freshness, migration, operator-control, or composed agent/human runtime evidence becomes available.
2. **Stabilize #482:** consume upstream common-control/same-subject semantics when sufficiently normative and evidenceable; do not substitute identifier association, request PoP, or local reference behavior for the missing primitive.
3. **Release preparation:** once #481/#482 are stable, cut coordinated but independently versioned RAHP/DPIP/Interop releases through their governed release paths.
4. **Realization conformance:** continue selective retest when adopted normative semantics become implemented rather than rerunning unrelated portfolio surfaces.
5. **Adoption and portability:** validate additional non-DTG consumers against unchanged generic controller contracts.
6. **Specialist ecosystem:** add specialists through versioned contracts/shared fixtures rather than target-specific core logic.
7. **Operational observability:** improve controller telemetry and longitudinal posture while keeping workflow success separate from assurance success.
8. **Composition pressure testing:** expand end-to-end flow coverage without promoting component conclusions.

## Non-regression rules

- No human-only controller transition.
- Missing evidence never becomes PASS.
- Workflow success never substitutes for assurance success.
- Model and evidence gaps remain explicit residuals.
- Replay remains idempotent; new pins create lineage.
- Static/source, synthetic, runtime and governance evidence remain distinct.
- Normative convergence never silently becomes implementation conformance.
- Component PASS never implies composition PASS.
- Generic RAHP core remains independent of DTG, Dogwood, CAWG, A2A or any other target-specific controller vocabulary.

## Historical roadmap

v2.1.0 **Common Acacia Blue** remains the immutable Qualified Autonomous Assurance Plane boundary. v2.0.0 **Blue Mormon** remains the immutable Portable Assurance Engine Stabilization boundary. Historical v1.7.0 **Common Palmfly** remains the immutable Assurance Operations and Complete DTG Cross-Spec Coverage release boundary. Historical v1.6.0 **Common Earl** remains the immutable Source-Pinned Coverage and Guided Adoption release boundary. Historical release notes and qualification records remain evidence rather than being rewritten into the current roadmap.
