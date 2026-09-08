---
layout: default
title: "Changelog"
nav_order: 7
has_toc: true
parent: Reference
---
# Changelog

## Unreleased — v2.3.0 development line

### Added / advanced

- Generic capability-coverage validation across DTG Persona and Data Rooms without adding consumer-specific semantics to RAHP core.
- Canonical Data Rooms proposition catalogue under `profiles/dtg/coverage/data-rooms.yaml`, with later evidence maturity tracked separately under #481.
- WD02 source/evidence reconciliation against the adopted Credential Specification baseline, including fresh VDC × VAC composition and action-time VDC × VAC × Trust Task evidence.
- Attributable OpenVTC A/B privacy evidence returned through DPIP for relationship/verifier, status, Trust Task and policy-discovery surfaces.
- Current OpenVTC Data Rooms target-native evidence advancing the propositions presently supported by the implementation while retaining explicit residuals for absent private-room, witnessed-anchoring, migration, operator and composed-runtime surfaces.
- Durable WD02 common-control residual isolation under #482 rather than treating identifier association, request-level proof-of-possession or local reference behavior as normative common-control proof.

### Release posture

v2.3.0 is **not released**. Release preparation is intentionally held until #481 and #482 reach stable, source-backed dispositions. This does not require either residual to become GREEN; it requires the remaining external/runtime dependency to be explicit and terminally understandable.

The stable release remains v2.2.0 **Common Four-ring**. No unreleased development result changes the v2.2.0 qualification contract or its immutable release record.

## v2.2.0 — 2026-09-07 — Common Four-ring

### Added

- Semantic `rahp-assurance-obligation/v1` identity and accountable evidence/remediation ownership.
- Registered evidence-producer controller, scheduler and provenance routing.
- Bounded assurance invariant waves for actor dependency, evidence topology and human choice.
- Current-portfolio source-pinned clean-room assessor with durable proposition matrix and terminal records.
- Explicit normative-baseline versus implementation/realization separation and runtime-evidence residual routing.

### Qualified behavior

Current portfolio clean-room #446 / PR #447, run `34073261344`, terminated `TERMINAL_INDETERMINATE_EVIDENCE_REQUIRED` with an AMBER consumer posture. The result demonstrates evidence-conservative behavior: bounded executable propositions can PASS while implementation, actuation, replay and privacy properties remain INDETERMINATE until adequate evidence exists.

### Compatibility

`rahp-engine-contract-v1` revision 1.3, normalized result schema 1 and `rahp-evidence-retention-v1` remain unchanged.

### Release name

**Common Four-ring — *Ypthima huebneri***.

See [v2.2.0 release notes](docs/releases/v2.2.0.md).

## v2.1.0 — 2026-08-31 — Common Acacia Blue

v2.1.0 remains the immutable Qualified Autonomous Assurance Plane release. See [v2.1.0 release notes](docs/releases/v2.1.0.md).

## Prior release history

v2.0.0 **Blue Mormon** and the complete earlier release history remain immutable in Git history and release tags. Historical v1.7.0 **Common Palmfly** remains the immutable Assurance Operations and Complete DTG Cross-Spec Coverage release record. Historical v1.6.0 **Common Earl** remains the immutable Source-Pinned Coverage and Guided Adoption release record. Historical release-note files remain under [`docs/releases/`](docs/releases/), and pre-v1.2 accumulated history remains under `archive/pre-v1.2/`.
