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
