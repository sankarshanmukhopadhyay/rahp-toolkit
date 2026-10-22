---
layout: default
title: People-impact pathway pilot
parent: Learn RAHP
nav_order: 6
---

# People-impact pathway pilot: evidence, use and limitations

This document accompanies [issue #1091](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1091) and is **not** a normative interpretation of the upstream Trust Tasks or Credential Specification.

## Baseline

The bounded pilot covers all 30 `TT-*` scenarios in `corpora/trust-tasks.yaml` (adapter 1.1, pinned Trust Tasks source `4937c70df95e56ed6404b8c004106ecb121a23cf`) and all 20 `XSP-*` scenarios in `corpora/trust-tasks-credspec-composed.yaml` (adapter 1.2, derived from the separate Trust Tasks pin and Credential Spec pin `b89f389abbdae77ba60b673c0836c781c2b54169`). The composed adapter has no single canonical upstream commit.

The authoritative RAHP pilot input is `method/impact-pathways/pilot.json`; the schema is `method/schema/impact-pathways.schema.json`, and validation/reporting is `python3 tools/validate_impact_pathways.py --check --report`. No generated `build/` file is edited by hand.

## Model and judgment

Each pilot corpus contains an explicit disposition for **every** scenario. The statuses are `qualified` (direct source qualification plus accountable adjudication), `provisional` (an explicitly bounded analyst interpretation), `rejected`, and `not-established`. Qualified judgments require direct-source evidence **and** a recorded reviewer, date and decision evidence. This pilot makes **zero** qualified claims; it contains two provisional illustrations and 48 not-established dispositions.

A potential affected role is an *abstract relationship to a system action*, not a named DTG persona and not evidence of a harmed person. Harm-pattern IDs may be included only when they exist in the canonical harm catalogue and the causal argument supports them. This pilot intentionally assigns **no** `HRM-*` references to its illustrative provisional hypotheses; the composed corpus' pre-existing `portable_assurance.harm_patterns` tags have not been independently adjudicated as people-impact links.

An `SP-*` pattern, a similar `SC-*` record, or a finding identifier such as `SEC-TT-002` cannot be substituted for the exact corpus scenario ID. No mapping supplies runtime execution evidence, incident likelihood, numerical severity, population magnitude, or safety certification. Existing review backlinks remain governed by #1086 and do not create affected-person relationships.

## Two illustrations

**TT-002:** A signed task intended for one recipient might be accepted outside its intended audience. The draft affected role is the intended recipient or relying party. The protected interest concerns control over who can rely on an authorized task. The failure is *possible*, not demonstrated. The source-facing corpus contains a commit-pinned `SPEC.md#482-audience-binding` anchor, but that anchor alone does not establish person-specific harm, so the mapping is **provisional**.

**XSP-001:** A relying party might use a credential without evidence of the task outcome on which it relies. A consequential decision might therefore be made from incomplete assurance evidence. The composed scenario derives from multiple pinned upstream dependencies and contains a prose anchor rather than a single source-at-commit URL. The resulting impact statement remains **provisional**.

**Every other pilot scenario:** **not-established**, with an explicit negative disposition. This records that no independently qualified causal role/interest/harm pathway has yet been established for that scenario; it does *not* mean that no person could be affected.

## How to extend and qualify

1. Reconfirm both adapter versions, source pins and composition parent pins; rebaseline before accepting altered sources.
2. Identify a specific affected role and interest, articulate the failure-to-consequence mechanism, and attach the scenario's authentic source anchor.
3. Treat all candidate mapping prose as analyst interpretations until adjudicated. For `qualified`, require a cited source record and accountable reviewer/date/decision evidence.
4. Validate canonical scenario IDs, no duplicate/omitted rows, harm IDs, matching anchors, exact source/dependency pins, schema and negative cases.
5. Rebuild Jekyll and inspect `/rahp-toolkit/corpora/trust-tasks/` and `/rahp-toolkit/corpora/trust-tasks-credspec-composed/`; publish the HTTP observation and checked-in commit SHA.
6. Reassess #1077 from a non-specialist perspective. Do **not** claim that the pilot supplies independently qualified answers to *who is harmed* until those mappings are adjudicated.

## Remaining qualification gap

The 50-row pilot establishes a reproducible structure and exposes coverage gaps; it does **not** convert currently available specification or corpus evidence into a full set of accepted people-impact statements. The practical next activity is *independent adjudication of the two hypotheses and source-by-source qualification of additional scenarios*. This is a material evidence activity, not something validation alone can decide.

The public pages label provisional and not-established rows accordingly and retain an explanation of the authority boundary.

## Second increment: portable role identity and coverage evidence

The pilot now uses a bounded portable [affected-role vocabulary](../method/impact-pathways/roles.json). A role ID identifies an accountable or potentially affected *capacity* in a system, not an individual, demographic group or DTG-specific persona. The current two provisional hypotheses use `task-recipient-or-relying-party` and `credential-relying-party` respectively. The role identifiers provide a stable join key while avoiding automatic persona-to-role inference.

The validation command emits machine-readable status totals, per-role counts, harm-reference count, upstream baselines, unresolved scenario identifiers, and qualification totals. These figures describe coverage and evidence gaps; they are not a safety score. A zero-positive baseline is an expressly valid input and a regression test verifies that outcome.

**Outstanding source qualification:** There are still no adjudicated `qualified` pathways. A reviewed judgment needs a direct source claim, a defensible causal chain connecting role, protected interest and harm taxonomy, and accountable review evidence. The existence of a harm identifier in a composed adapter is not, by itself, such a judgment. Rebaseline dependency hashes before reusing composed impact conclusions.

## Pinned-source examination: 2026-10-20

The version-qualified [source-review packet](../method/impact-pathways/source-review-2026-10-20/) records a bounded examination of the two provisional hypotheses against the exact source revisions declared by the pilot. It distinguishes the **normative source statement**, the **RAHP analyst's causal extension**, and the **unestablished people-impact claim**. The packet is an independently reproducible evidence dossier, **not** a human reviewer's signed adjudication.

- **TT-002:** [Trust Tasks `SPEC.md` §4.8.2 at the adapter pin](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/4937c70df95e56ed6404b8c004106ecb121a23cf/SPEC.md#482-audience-binding) requires in-band recipient binding for proof-bearing, non-bearer tasks; §10.1 describes cross-recipient replay. This establishes the protocol failure mechanism, but not a demonstrated human consequence. A conforming consumer rejects the malformed document, and the bearer exception matters. **Retain provisional**.
- **XSP-001:** [Credential Specification `spec/body.md` at its exact pin](https://github.com/trustoverip/dtgwg-cred-spec/blob/b89f389abbdae77ba60b673c0836c781c2b54169/spec/body.md#trust-task-context-binding) requires verified corresponding outcome evidence before interpreting a `taskContext`-bearing credential as proof of completed task. The composed adapter draws on the separately pinned Trust Tasks specification; the source describes the verification boundary, not a demonstrated person's loss. **Retain provisional**.

The review compares candidate `HRM-INF-01`, `HRM-SEC-02` and `HRM-AUT-04` meanings against their canonical harm definitions. They remain candidates or unestablished, not automatically adopted mappings. Actual impact qualification requires accountable, independently challengeable review of the affected-role → interest → consequence chain. The source review deliberately makes **zero** claims of runtime PASS, real-world injury, independently qualified harm, or source authority transfer.

To reproduce the bounded checks, execute `python3 -m unittest tests.test_impact_source_review -v`, then `python3 tools/validate_impact_pathways.py --check --report`. Reassess if either source pin or the harm catalogue semantics change.

## People-impact qualification acceptance tranche

The [qualification acceptance packet](people-impact-qualification-acceptance.html) records six atomic candidate relationships across `TT-002`, `XSP-001`, `TT-005` and `XSP-018`, separating decision actors from potentially affected roles. Its reviewer acceptance status is **not recorded**, so no canonical pilot mapping is promoted to qualified. The packet includes source pins, harm candidates, falsification cases and a practical independent-review handoff.


## Method capability acceptance boundary

The people-impact pathway capability and the qualification of an individual pathway are separate decisions.

A conforming implementation may legitimately contain **zero qualified pathways**. The validator must still preserve complete scenario disposition coverage, source/dependency pins, portable-role validity, causal-evidence limits and truthful negative output. A lack of independently adjudicated positive mappings is therefore not itself a method failure.

The canonical pilot remains intentionally bounded to Trust Tasks and Trust Tasks × Credential Specification. Generality is tested without silently expanding that pilot: regression coverage adds the separately source-pinned Credential Specification corpus with all scenarios set to `not-established`, and requires the same validator to accept the third namespace while preserving the original two mandatory pilot corpora.

Qualification of any individual pathway remains stricter. It still requires direct source support, applicable harm mapping and accountable adjudication evidence. CI, AI assistance, source presence or method acceptance cannot substitute for that human judgment.

Source anchors used by positive/provisional records are also treated as trust-boundary inputs. Obvious absolute, traversal and executable-scheme values are rejected rather than rendered or followed as evidence references.
