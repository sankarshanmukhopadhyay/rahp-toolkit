---
layout: default
title: "Changelog"
nav_order: 7
has_toc: true
parent: Reference
---
# Changelog

This file records current release-level changes. The complete pre-v1.2 changelog, including accumulated historical `Unreleased` sections, is preserved at `archive/pre-v1.2/CHANGELOG-pre-v1.2.txt`.

## v1.7.0 — 2026-08-27 — Common Palmfly

### Added

- Deterministic no-regression coverage for `rahp`, `security`, `combined` and multi-target `--all` review paths.
- Full DTG cross-specification benchmark execution across 8 declared / 8 runnable compositions.
- Live instance-watch acceptance proving persisted monitored state can dispatch current-head validation and Pages evidence successfully.
- Workflow-dispatch contract validation and stale-head protection for post-monitor assurance regeneration.
- Repeatable execution benchmarking for representative DTG, full DTG and repository full-validation profiles.
- v1.7-specific machine-verifiable qualification manifest, validator and tests.

### Changed

- DTG assurance execution expands from a representative seam benchmark to the complete currently maintained runnable DTG composition set.
- Real ZKP Portfolio Monitor queue lineage is advanced through a durable combined RAHP + security disposition without manufacturing findings.
- Release qualification now treats the monitor → queue → substantive review → durable evidence → disposition path as an operational contract.
- Root/workspace package metadata advances to `1.7.0` while the stable v1 engine/result/retention contracts remain unchanged.

### Performance and coverage

Measured benchmark evidence records approximately 1.586 s for the representative DTG seam, 11.165 s for the full eight-composition DTG pressure surface and 11.517 s for repository full validation. Earlier like-for-like measurements do **not** support a speed-improvement claim, so v1.7.0 qualifies measurement capability and coverage refinement rather than faster execution.

### Compatibility

The stable v1 compatibility boundaries remain unchanged:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.7.0 is an additive minor release. Existing normalized results and historical assessment lineage remain valid.

### Release name

**Common Palmfly — *Elymnias hypermnestra***, selected on 2026-08-27 from the recorded West Bengal butterfly list under the random-at-release-time naming policy.

See [v1.7.0 release notes](docs/releases/v1.7.0.md).

## v1.6.0 — 2026-08-23 — Common Earl

### Added

- Source-pinned Trust Tasks and DTG Credential Specification corpora at immutable upstream revisions.
- Machine-readable coverage maps for the two primary corpora.
- Expanded Trust Tasks and Credential Specification corpora from 16 to 30 scenarios each.
- Expanded Trust Tasks × Credential Specification seam corpus from 12 to 20 composed scenarios.
- Durable pre-expansion assessment history and evidence-backed cross-specification reassessment.
- Guided documentation hubs for first-run adoption, development/integration and continuous assurance.
- Machine-verifiable v1.6 release qualification contract, validator and tests.
- Qualified, commit-bound GitHub tag/release publication workflow.

### Changed

- Packaged corpus coverage increases from 146 to 182 scenario vectors across 14 corpora and 28 portable scenario patterns.
- The Trust Tasks corpus is pinned to `4937c70df95e56ed6404b8c004106ecb121a23cf`.
- The DTG Credential Specification corpus is pinned to `b89f389abbdae77ba60b673c0836c781c2b54169`.
- The Trust Tasks × Credential Specification pressure test was rerun against the expanded current-source corpus; its three residual themes remain but are refined by stronger current ACL lifecycle, approval, redress and VWC binding evidence.
- The root README is now a concise front door rather than an accumulating handbook.
- Historical v1.5 qualification validation is release-history aware so later compatible v1 releases do not invalidate preserved v1.5 evidence.
- Root/workspace package metadata advances to `1.6.0` while the stable v1 engine/result/retention contracts remain unchanged.

### Compatibility

The stable v1 compatibility boundaries remain unchanged:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.6.0 is an additive minor release. Existing normalized results remain valid.

### Assurance and baseline policy

- Corpus growth broadens the pressure surface but is not itself an assurance conclusion.
- The expanded TT×CredSpec review refines existing residuals rather than manufacturing new findings from scenario count.
- Maintained example baselines remain at their separately evidenced v1.5 state until independently reassessed; the toolkit release does not silently promote them.
- Historical assessment records remain immutable lineage evidence.

### Release name

**Common Earl — *Tanaecia julii***, selected on 2026-08-23 from the recorded West Bengal butterfly list under the random-at-release-time naming policy.

See [v1.6.0 release notes](docs/releases/v1.6.0.md).

## v1.5.0 — 2026-08-22 — Purple Leaf Blue

### Added

- Durable assessment identity and finding lineage independent of individual assessment runs and issue trackers.
- Governed remediation obligations, acceptance criteria, closure evidence and executable retest lineage.
- Portable assurance graph with explicit impact-propagation semantics and deterministic reassessment selection.
- Evidence provenance manifests, conservative assurance freshness and machine-readable assurance deltas.
- Scoped executable authority with suspension, revocation and expiry state.
- Three-valued policy gates with `PASS`, `FAIL` and `INDETERMINATE` outcomes.
- Portable assurance posture for actionable operational/portfolio views without a synthetic assurance score.
- Machine-readable v1.5 capability/documentation registry and synchronization validation.
- Machine-readable v1.5 release qualification manifest and validator.
- Deployment-neutral conformance fixtures plus maintained deployment demonstrations.
- Release runbook and synchronized v1.5.0 release content.

### Changed

- The v1.5 lifecycle connects target change → impact → freshness → reassessment/retest → assurance delta → remediation → policy gate → authority verification → operational posture.
- Portfolio presentation keeps assurance conclusion, freshness, remediation, gate and authority state separate rather than collapsing them into a percentage.
- Documentation synchronization is a CI-enforced property across implemented v1.5 capabilities.
- Root/workspace package metadata advances to `1.5.0` while the stable v1 engine/result/retention contracts remain unchanged.

### Compatibility

The stable v1 compatibility boundaries remain unchanged:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.5.0 is an additive minor release. Existing v1.1 and v1.2 normalized results remain valid.

### Governance

- Policy evaluation never creates authority.
- Repository permissions are not automatically governance authority.
- Stale/retest-required assurance is not automatically a finding.
- Detector absence does not establish closure.
- Work-item deletion does not destroy canonical assurance lineage.
- Project-specific deployments remain demonstrations rather than portable-core dependencies.

### Release name

**Purple Leaf Blue — *Amblypodia anita***, selected from the recorded West Bengal butterfly list under the v1.5.x naming policy.

See [v1.5.0 release notes](docs/releases/v1.5.0.md) and the [v1.5 release runbook](docs/v1.5-release-runbook.md).

## v1.2.0 — 2026-08-20

### Added

- Evidence-driven assurance evaluation with seven residual states: `assured`, `controlled`, `finding`, `assurance-gap`, `review-required`, `not-assessed` and `not-applicable`.
- Typed evidence classification by repository/context surface and authority weight.
- First-class control credit so risk signals can be evaluated against controls and assurance evidence before a residual conclusion is assigned.
- `method/schema/assurance-evaluation.schema.json`.
- `method/schema/remediation-manifest.schema.json`.
- `method/schema/retest.schema.json`.
- `method/mappings/resilience-to-assurance.yaml` for semantically valid DRARM-to-portable-pattern mappings.
- Python assurance evaluation and CLI support.
- TypeScript schema/core/CLI support for assurance summaries, residual inference and retest outcomes.
- Cross-implementation conformance fixtures for confirmed findings, assurance gaps, controlled targets, remediation manifests and retest transitions.
- Documentation for assurance evaluation, evidence classification, result interpretation and remediation/retest lifecycle.

### Changed

- Detector output is explicitly a signal rather than an automatic finding.
- Normalized result schema version `1` gains optional assurance summaries, evaluations, remediations and retests while preserving v1.1 result validity.
- `rahp-engine-contract-v1` gains additive assurance-evaluation/remediation/retest operations without changing its stable contract identifier.
- Zero-finding semantics now prevent unresolved `assurance-gap`, `review-required` or `not-assessed` states from being represented as `no-material-assurance-impact`.
- DRARM is integrated as a specialized signal provider into the portable assurance graph where semantic equivalence exists; unmatched rules remain explicitly unmapped.
- Remediation ownership/routing is machine-readable while external publication authority remains separately governed.
- Root README and roadmap are aligned to the evidence-driven v1.2 lifecycle.
- TypeScript workspace, package and lockfile metadata advance to `1.2.0`.
- `method/versioning.yaml` advances the declared stable release to `v1.2.0`.

### Compatibility

The stable v1 boundaries remain unchanged:

```text
rahp-engine-contract-v1
normalized result schema version 1
rahp-evidence-retention-v1
```

v1.2.0 is an additive minor release. Existing v1.1 normalized results remain valid.

### Governance

- A remediation manifest can identify an owning repository/control plane but does not grant authority to publish externally.
- Observation, assessment and publication remain distinct capabilities.
- Evidence-based retesting is the closure mechanism; detector absence alone is not proof of resolution.

See [v1.2.0 release notes](docs/releases/v1.2.0.md).

## v1.1.0 — 2026-08-17

- Added the portable assurance knowledge model and catalogue.
- Added catalogue validation, catalogue-aware review mappings and portable scenario stress patterns.
- Added the governed simple-English glossary and explicit guardrail applicability semantics.
- Expanded maintained DTG, CAWG/C2PA, A2A and cross-specification examples.
- Added generated portable catalogue and assurance graph views.
- Preserved `rahp-engine-contract-v1`, normalized result schema version `1` and `rahp-evidence-retention-v1`.

See [v1.1.0 release notes](docs/releases/v1.1.0.md).

## v1.0.0

- Established the stable v1 method/versioning boundary.
- Added Python/TypeScript differential conformance.
- Formalized evidence retention and normalized-result compatibility.
- Added documentation information-architecture validation.

See [v1.0.0 release notes](docs/releases/v1.0.0.md).

## Historical releases

Detailed v0.x and early v1 release notes remain under [`docs/releases/`](docs/releases/). The full pre-v1.2 changelog is retained for provenance at `archive/pre-v1.2/CHANGELOG-pre-v1.2.txt`.
