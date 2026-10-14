---
layout: default
title: "RAHP adversarial assurance qualification"
parent: Learn RAHP
has_toc: true
---
# Adversarial assurance qualification: campaign 1023

Tracking: [#1023](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1023).

**Status:** threat-model and coverage inventory established; attack outcomes **NOT_YET_EXECUTED**. This is a maintainer-authored evaluation plan, not evidence of an independent red team, security certification, or target-system conformance.

## Pinned starting point and authorized scope

- Starting source baseline: `88cf85e09375483b526e57d4873274ca8860d82d` (main at inventory on 2026-10-14).
- Published baseline: `v2.7.0` (qualified 2026-10-08). Do not confuse release contents with subsequent main commits.
- Exercise only local synthetic fixtures, repository-owned scripts and controlled runners. No live attack traffic against OpenVTC, DTG infrastructure, GitHub accounts, or unrelated targets.
- Retain the original inputs, source pins, stdout/stderr, executed commands, runtime versions, exit status and SHA-256 hashes for completed cases.
- Do not claim `PASS` from execution success, schema validation, structural agreement or the lack of findings. A partial/incomplete execution remains explicit.
- This campaign does not change R1/R2/R3 schema semantics, existing assessor-result v1, the stable controller, or upstream authority.

## Current evidence inventory and limits

| Claim / mechanism | Reviewed source | Existing protection / limit | Red-team implication |
| --- | --- | --- | --- |
| Evidence adequacy R1 | [R1 contract](evidence-adequacy.md); `tools/evidence_adequacy.py`; `tests/test_evidence_adequacy.py` | Missing, duplicate, unavailable and contradictory declarations cannot structurally PASS; source authority and declared scope are not independently authenticated. | Try scope and evidence declaration laundering; no claim of real source verification. |
| Temporal applicability R2 | [R2 contract](temporal-provenance.md); `tools/temporal_provenance.py`; `tests/test_temporal_provenance.py` | Known-at cutoff, intervals and optional freshness are modelled; declared source pins are not independently authenticated. | Exercise late retroactive and stale/cross-source claims. |
| Reproducibility R3 | [R3 contract](reproducibility-challenge.md); `tools/reproducibility_challenge.py`; `tests/test_reproducibility_challenge.py` | Compares *declared* records; same declared inputs/results do not prove actual execution or correctness. | Attempt provenance and declared-match laundering. |
| Independent adoption | [exercise](reasoning-adoption-exercise.md), [evidence record](reasoning-adoption-record.md) | Synthetic uncoached task exists; independent adoption is not yet established. | Blind challenge must stay distinct from maintainer replay. |
| Controller / terminal assurance | [architecture](reasoning-architecture.md), `tools/assurance_fsm.py`, `tools/assessment_controller.py`, `tools/autonomous_assurance_controller.py` | Controller owns terminalization; review of actual fail-closed paths is still required in this campaign. | Interrupt required evidence production and attempt invalid state promotion. |
| Standalone replay | `examples/standalone-trqp/replay.py`, `tests/test_standalone_trqp.py` | Pinned bounded propositions, not general runtime or normative conformance. | Try making a limited replay appear to cover a broader proposition. |

The existing R1–R3 participant scenario inventory already covers missing R1 evidence, later-known R2 evidence, R2 conflict and declared R3 disagreement. **Reuse it** instead of creating duplicates. The inventory above is documentation/source-path reconnaissance, not a source-code audit or proof those protections currently pass tests.

## Threat surfaces and initial priority

Priority indicates *testing value*, not a proven defect. Evidence must establish whether a defect exists.

| ID | Attack surface / control | Trust boundary and attacker capability | Adversarial hypothesis | Expected safe behaviour | Priority / reuse |
| --- | --- | --- | --- | --- | --- |
| AA-01 | False assurance | Attacker controls R1 declared scope and evidence list | Removes a material requirement while supplying a syntactically complete set. | R1 may correctly return structural PASS for the declared scope, but caller/report must never interpret it as full coverage or authoritative RAHP PASS. | High; new **cross-layer** check; R1 alone cannot know undeclared obligations. |
| AA-02 | Evidence contradiction | Attacker adds a second otherwise valid observation for one requirement | Conflicting or repeated observations are silently deduplicated. | R1 INDETERMINATE with conflict; preserve both observations. | Medium; reuse R1 tests. |
| AA-03 | Authority laundering | Attacker declares arbitrary repository/revision as authoritative R2 source pin | Source pin is mistaken for verified source authority. | R2 reports only claimed applicability; no source-authentication or terminal assurance claim. | High; report/consumer boundary needs examination. |
| AA-04 | Temporal replay | Attacker shifts `knowledge_cutoff` to suppress a retroactive known conflicting assertion | As-known-at and currently-known determinations are conflated. | Earlier cutoff result remains historically scoped; later cutoff reveals conflict; neither establishes source truth. | High; reuse adoption scenarios C/D. |
| AA-05 | Evidence identity laundering | Attacker supplies matching declared R3 hashes without hashing real artifacts | Declared match represented as independently reproduced assurance. | R3 DECLARED_MATCH is limited to declared records; independent re-hash required outside R3. | High; reviewer-facing/report boundary. |
| AA-06 | Source substitution | Attacker changes fixture content while retaining a descriptive source pointer | Standalone case accepts stale source material as fresh evidence. | Pinned digest/provenance verification or explicit unavailable/uncertain disposition; no unsupported PASS. | High; inspect existing standalone replay tests. |
| AA-07 | Controller skip | Attacker interrupts a mandatory evidence producer | Workflow completion is promoted to terminal PASS. | Missing required evidence remains INDETERMINATE/blocked according to existing controller contract. | Critical; reuse controller tests then add missing negative path. |
| AA-08 | Controller mixed state | Attacker provides out-of-order/stale specialist return | Terminal state accepts superseded evidence or missing reassessment. | Reject/invalidate stale return or retain explicit indeterminacy. | High; inspect controller evidence/freshness tests. |
| AA-09 | Coverage omission | Attacker selects only favourable material lenses | No findings is treated as fully assessed system. | Explicit materiality and lens coverage record; unexamined applicable lens cannot silently PASS. | Critical; inspect full-stack orchestration tests. |
| AA-10 | Unsupported input | Attacker supplies an unrecognized case/profile structure | Permissive handling drops adversarial case without trace. | Explicit rejection or justified non-applicability; no false full coverage. | High; validate case loading paths. |
| AA-11 | Reviewer narrative manipulation | Attacker supplies a persuasive report that mislabels optional R1/R2/R3 results as terminal PASS | Human-facing summary obscures assessment authority. | Reader can identify bounded/experimental profile and nonterminal meaning. | Medium; check output/report templates. |
| AA-12 | Challenge suppression | Attacker supplies an R3 declared match alongside unresolved challenge | Final summary presents consensus despite an open challenge. | Preserve OPEN challenge without silent resolution or legitimacy claim. | Medium; reuse R3 tests; report boundary. |

## Execution and adjudication protocol

For each *executed* scenario, write an evidence record with:
- stable scenario ID; threat actor/control, target version and scope;
- hypothesis, targeted invariant, expected safe behaviour;
- actual input files, SHA-256 digests, execution command, environment and exit code;
- literal observed result and output artifact hash;
- separately classified attack-delivery outcome and assurance-integrity outcome;
- failure owner (method, code or governance/process), remediation link and retest evidence.

Results: `RESISTED` (attack exercised, invariant held), `COMPROMISED` (demonstrated unsafe assurance behaviour), `INDETERMINATE` (insufficient evidence), or `NOT_EXECUTED`. A documented legitimate R1 PASS or R3 DECLARED_MATCH **is not itself compromise**. Do not mark a scenario RESISTED merely because an existing test name suggests resistance.

Recommended current commands from documented interfaces (not yet executed in this campaign):

```bash
git rev-parse HEAD
python3 --version
python3 -m unittest tests.test_evidence_adequacy tests.test_temporal_provenance tests.test_reproducibility_challenge -v
python3 -m unittest tests.test_reasoning_worked_example -v
python3 -m unittest tests.test_standalone_trqp -v
python3 tools/evidence_assertion_assessor.py --self-test
```

Broader CI/controller tests and repository validation must be discovered from the current codebase before declaring campaign completion. Commands above are **instructions, not success claims**.

## Executable first tranche: AA-07 and AA-09

The synthetic test module [`tests/test_adversarial_assurance_1023.py`](../tests/test_adversarial_assurance_1023.py) adds six narrow tests: a positive full-stack terminalization control, missing material security-lens disposition, unexecuted applicable composition lens, absent mandatory evidence-probe ledger, a ledger missing one required attempt, and an attributable but unavailable evidence attempt whose material RAHP lens remains indeterminate.

**Important scope limitation:** `assert_full_stack_terminalizable` checks the declared full-stack record. The new tests do not establish that *all controller entry points* call this gate, nor do they prove substantive evidence authenticity or sufficiency. In particular, `ATTEMPTED_UNAVAILABLE` is evidence of a recorded attempt, **not** proof of successful evidence acquisition or satisfaction. The separate applicable-lens check must prevent PASS.

Run:

```bash
python3 -m unittest tests.test_adversarial_assurance_1023 -v
python3 -m unittest discover -s tests -p 'test_*.py'
```

The repository's `.github/workflows/validate.yml` runs the full unittest discovery command on pull requests. **CI results and runtime execution must be linked before these test cases can be marked RESISTED or accepted as validated.** Further controller entry-point inspection remains necessary.

## Findings and independent challenge

Maintain a separate ledger of observed failures with reproduction and regression references. Unexecuted hypotheses are *not findings*. An external reviewer should receive a pinned baseline, supported command set, evidence-record template, safety/scope rules and enough architecture to discover **novel** attacks without receiving only a script for repeating the maintainer's results.

The assessor may challenge evidence provenance, declared coverage, authority interpretation, report clarity or the threat model itself. Preserve disagreements rather than editing historical outcomes. An independent red-team claim requires actual independent participant execution and evidence.

## Next decision

Implement **AA-07 and AA-09 first**, only after source-level inspection demonstrates missing negative coverage. In parallel inspect AA-01/03/05 reporting boundary, as false interpretation of *correct* optional-profile outputs is a credible assurance-integrity risk. Do not add a new framework or release solely because this inventory exists.
