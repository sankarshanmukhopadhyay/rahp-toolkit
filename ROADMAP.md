---
layout: default
title: "Roadmap"
nav_order: 6
has_toc: true
parent: Reference
---
# RAHP Toolkit Roadmap

This roadmap records the current portable RAHP direction. Historical pre-v1.2 roadmap material is preserved under `archive/pre-v1.2/` and is not current authority.

## v1.7.0 — Assurance Operations and Cross-Spec Execution (stable release)

Status: **stable public release — Common Palmfly (*Elymnias hypermnestra*)**.

v1.7 strengthens RAHP's operational assurance loop without changing the stable v1 compatibility boundary. It qualifies monitor-driven assessment queueing, explicit review modes, live current-head assurance regeneration, full DTG cross-spec execution coverage and release-grade regression evidence.

### Delivered workstreams

1. **Monitor → assessment operations**
   - material portfolio changes are queued without being misrepresented as findings;
   - a live state-changing instance-watch run persisted observed state and successfully dispatched validation and Pages against the exact resulting `main` SHA.

2. **Review-mode regression contract**
   - `rahp`, `security` and `combined` modes are deterministically exercised;
   - `--all` multi-target selection is covered;
   - unsupported mode/target combinations fail closed.

3. **Full DTG cross-spec execution**
   - all 8 declared runnable DTG compositions are exercised;
   - coverage spans authority/delegation, lifecycle, privacy composition, proof semantics, persistent state, provenance, linkability and identifier/control semantics.

4. **Performance measurement**
   - representative DTG, full DTG and full-validation wall times are recorded through a repeatable benchmark surface;
   - current evidence does not support a like-for-like speed-improvement claim, and the release says so explicitly.

5. **Release qualification and publication**
   - `method/v1.7-release-qualification.yaml` defines the v1.7 release boundary;
   - `tools/validate_v17_release.py` verifies review-mode evidence, live-operation evidence, 8/8 DTG coverage, workspace synchronization and compatibility;
   - the qualified publication workflow revalidates the exact main-branch release commit before creating `v1.7.0` and the GitHub Release.

### Retained v1.5 capability contracts

v1.6 retains the previously qualified continuous-assurance capability set unchanged:

- **Durable assessment and finding lineage**;
- **Governed remediation and retest**;
- **Assurance graph and impact analysis**;
- **Evidence provenance, freshness and delta**;
- **Executable authority and policy gates**; and
- **Portfolio and deployment presentation**.

These remain registered, documented and executable capability surfaces; v1.6 adds coverage and adoption qualification around them rather than replacing their contracts.

### Baseline policy

A toolkit release does not automatically requalify maintained external targets. The maintained-example registry remains at its separately evidenced v1.5.0 baselines until each example is independently reassessed or retested. Historical records remain immutable lineage evidence.

## v1.5.0 — Continuous Governed Assurance

v1.5 turned evidence-driven point-in-time assessment into durable, continuously governed assurance while preserving deployment independence. It delivered the retained capability contracts above plus machine-verifiable v1.5 release qualification.

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

v1.7.0 is additive within that boundary. Existing normalized results remain valid.

See [v1.7.0 release notes](docs/releases/v1.7.0.md) and the [v1.7 qualification contract](method/v1.7-release-qualification.yaml).

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
