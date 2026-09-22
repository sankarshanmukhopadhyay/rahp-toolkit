---
layout: default
title: "VTI release and upstream packaging judgment"
parent: Reference
nav_order: 8
has_toc: true
---
# VTI release and upstream packaging judgment

This document records the T12 disposition for the RAHP VTI composition-assessment programme. It completes the approved downstream engineering programme by making the release judgment and preparing the upstream-facing evidence and clarification package.

It does **not** cut a RAHP release and does **not** write to the upstream VTI repository.

## Source and reconciliation baseline

The active assessment baseline remains:

- repository: `trustoverip/dtgwg-vti-spec`;
- Document Status: `Working Draft 0.1.0`;
- commit: `75391a27a5d9a1794266b2e3bdeb8be68fa4db40`.

The upstream `main` branch was rechecked during T11/T12 and remained at that exact commit. No source-drift invalidation was therefore required.

The reconciled programme contains ten VTI composition families:

- eight families are `verified` with current `supported` RAHP submissions;
- privacy composition remains `specialist_evidence_required`, with `RAHP-VTI-PRV-001` deliberately `indeterminate`;
- component substitution remains `evidence_required`, with no synthetic assessment submission;
- nine current assessment submissions exist;
- no stale or superseded assessment submission was detected.

The authoritative reconciliation report is [VTI programme reconciliation](vti-programme-reconciliation.html).

## Release judgment

The current stable RAHP release remains **v2.3.0 — Common Five-ring**.

The T12 judgment is:

> **An additive product-minor release is warranted.**

The mechanically expected next minor version would therefore be **v2.4.0**, if a release cut is separately approved.

This judgment is based on the fact that the VTI work has become a reusable RAHP product capability rather than a set of isolated examples. Since v2.3.0, RAHP has gained:

- a version-pinned VTI composition assessment profile;
- a machine-readable `rahp-vti-assessment/v1` submission contract;
- multi-submission validation and source-pin consistency checking;
- deterministic human-readable assessment indexing;
- complete supported assessment families for semantic completion, authority continuity, lifecycle/freshness, delegation lineage, false independence, failure/indeterminacy, configuration materiality and human control;
- a deliberately indeterminate privacy assessment preserving the specialist-evidence boundary;
- an explicit evidence gate preventing synthetic closure of component substitution;
- deterministic programme-level reconciliation.

### Compatibility judgment

No compatibility-family break is indicated.

The existing compatibility authorities remain:

- `rahp-engine-contract-v1`, revision `1.3`;
- normalized result schema `1`;
- `rahp-evidence-retention-v1`.

The VTI assessment contract is additive. It does not alter those stable engine/result/retention contracts.

### Release gate preserved

No release surfaces have been changed as part of T12. In particular:

- `package.json` remains at `2.3.0`;
- `PROJECT-STATUS.yaml` remains on v2.3.0;
- no v2.4 qualification manifest has been created;
- no release codename has been selected;
- no release tag has been created;
- no GitHub Release has been published.

This is intentional. The repository's governed release workflow publishes automatically after the release declaration and synchronized release surfaces move to `main`. A release cut therefore remains a separate consequential decision.

The release naming policy also selects a random unused West Bengal butterfly name **at release time**. T12 does not pre-select or reserve one.

## Upstream packaging boundary

RAHP's role is to provide independent assurance evidence and concrete clarification questions. The upstream VTI specification remains authoritative for normative requirements, conformance semantics and admission of external assessment evidence.

No upstream issue or PR is created by this tranche.

### Existing upstream work already covering possible topics

#### `trustoverip/dtgwg-vti-spec#32`

The open structural-review issue already covers the tension between Appendix E being labelled informative while normative composition requirements depend on it. It also records the unresolved location of the conformance test suite.

**Disposition:** do not file another Appendix E normativity issue.

#### `trustoverip/dtgwg-vti-spec#33`

The open semantic-completion PR already advances the composition boundary between credential validity and exchange completion, and adds the outcome-evidence privacy/correlation consideration.

**Disposition:** do not duplicate semantic-completion or outcome-evidence-correlation requirement changes.

#### `trustoverip/dtgwg-vti-spec#35`

The open PR records observed implementation evidence against VTI requirements.

**Disposition:** treat this as evidence that upstream evidence cataloguing is active. It does not, by itself, define a canonical independent-assessment submission contract.

## Prepared clarification candidates

The following questions survive deduplication against current upstream work.

### VTI-CLAR-001 — Clarify specification evidence, conformance evidence and independent assessment evidence

How should the following be distinguished in authority, lifecycle and admissibility?

1. evidence that motivated or pressure-tested a VTI composition requirement;
2. evidence used by an implementation to establish conformance;
3. evidence produced by an independent assessor against a VTI requirement.

The concern is not terminology alone. Each evidence class may have different authority, freshness, admission and invalidation semantics.

This topic is **related to #32**, but not fully duplicated by it.

### VTI-CLAR-002 — Define assessment disposition semantics for `supported`, `refuted` and `indeterminate`

The VTI assessment interface would benefit from an exact statement of:

- what proposition a disposition applies to;
- what evidence threshold establishes `supported`;
- what kind of counterexample establishes `refuted`;
- when insufficient, stale, contradictory or unavailable evidence remains `indeterminate`;
- how an assessor avoids turning “not established” into “refuted”.

RAHP's current contract can supply one implementation example, but the semantics should belong upstream if VTI intends interoperable external assessments.

### VTI-CLAR-003 — Define assessment context, freshness and reassessment triggers

Which contextual fields must travel with a VTI assessment so its evidence cannot be silently reused outside the conditions under which it was produced?

Candidate context includes:

- VTI Document Status and exact source revision;
- assessed component names and versions;
- applicable profiles;
- relying policy and policy version;
- material deployment configuration;
- freshness bounds;
- assessment date;
- supersession or contradiction triggers.

This is the upstream analogue of RAHP's explicit reassessment model.

### VTI-CLAR-004 — Clarify ownership classification versus normative requirement status

This topic should **not** be filed independently while #32 remains unresolved.

The narrower question is whether a VTI composition requirement can be normative while semantic ownership remains `JOINTLY-OWNED` or `UNRESOLVED`. If so, Appendix E should make clear that ownership classification concerns the semantic/evidence responsibility boundary, not whether the VTI requirement itself is normative.

**Disposition:** defer pending #32; if useful, contribute as a focused comment there rather than creating another issue.

### VTI-CLAR-005 — Clarify evidence semantics for independence under `VTI-CMP-071`

The false-independence corpus shows that multiplicity, actor distinctness, provenance depth and quorum arithmetic cannot automatically be promoted into evidence independence.

The remaining upstream question is:

> What may establish effective independence, at what scope and freshness, and how can a relying party establish enough independence for the decision without turning independence evidence into a persistent cross-context correlator?

This is particularly important because “prove independence” can otherwise conflict with privacy-preserving pseudonymity, legitimate shared infrastructure and contextual identifiers.

### VTI-CLAR-006 — Define a machine-readable independent assessment submission format and admission process

If VTI expects independent assessments, a canonical machine-readable submission shape would improve comparability and tooling.

Candidate fields include:

- VTI requirement identifiers;
- assessment disposition;
- method;
- evidence artifact references;
- assessor;
- assessment date;
- assessed components and versions;
- profile/policy/configuration context;
- VTI source revision;
- evidence URI and/or digest;
- confidentiality handling where evidence cannot be public;
- reassessment/supersession state.

The separate process question is where and how such submissions are admitted, versioned and retained.

This topic is **related to #35**, because #35 demonstrates evidence cataloguing, but it is not duplicated by that PR.

## Topics explicitly not duplicated

The package deliberately does not propose new upstream work for:

- **Appendix E informative-versus-normative status** — already #32;
- **semantic completion and outcome-evidence correlation requirements** — already PR #33;
- **observed implementation evidence catalogue entries** — already demonstrated by PR #35.

## Recommended upstream packaging shape

If upstream engagement is approved, the least noisy sequence is:

1. raise one assessment-evidence-model topic combining **VTI-CLAR-001, VTI-CLAR-002 and VTI-CLAR-006** where doing so remains readable;
2. raise **VTI-CLAR-003** separately because freshness/reassessment is operationally distinct;
3. contribute **VTI-CLAR-004** only as a narrowly scoped addition to #32 if still relevant after that issue moves;
4. raise **VTI-CLAR-005** separately because effective independence is a substantive composition-assurance question with privacy consequences.

This packaging avoids six fragmented upstream issues while preserving the distinct technical questions.

## T12 disposition

The approved T3–T12 downstream engineering programme is complete.

The programme terminates with truthful bounded states:

- eight supported assessment families;
- one indeterminate privacy family awaiting specialist/runtime evidence;
- one component-substitution family awaiting genuine A/B implementation evidence;
- no stale assessment submissions;
- no VTI source drift at the T12 checkpoint;
- a product-minor RAHP release judged warranted;
- an upstream clarification package prepared and deduplicated.

Two consequential actions remain intentionally outside the completed engineering programme:

1. **release cut** — whether to turn the v2.4.0 minor-release judgment into an actual governed RAHP release;
2. **upstream write** — whether to submit the prepared clarification package to `trustoverip/dtgwg-vti-spec`.

Both remain explicit approval gates rather than implicit consequences of successful downstream work.

The machine-readable T12 record is `data/vti-programme-t12.yaml`.
