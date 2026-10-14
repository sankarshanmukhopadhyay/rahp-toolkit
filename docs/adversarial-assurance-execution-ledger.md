---
layout: default
title: "Adversarial assurance execution ledger"
parent: Learn RAHP
---
# Campaign #1023: maintainer-side execution evidence

**Status:** maintainer-authored, CI-executed synthetic controls; not independent red-team testing. Source baseline: `main@88cf85e09375483b526e57d4873274ca8860d82d` before the remediation; remediation merged by [PR #1024](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1024) at `700d672adcc12d5854ce77a4551ae2d4a7590aec`.

## Execution evidence and limits

- Reproduction target: `tests/test_adversarial_assurance_1023.py`, committed to PR #1024.
- Successful latest PR-head [validate run 38593567128](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/38593567128) on `f805f76939f29ab7657693ca863c0edc1296898e`; [documentation run 38593567398](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/38593567398) succeeded.
- CI executes `python3 -m unittest discover -s tests -p 'test_*.py'` among wider validators. Reproduce focused tests with `python3 -m unittest tests.test_adversarial_assurance_1023 -v`.
- The repository commit SHA identifies exact checked-in fixture/code bytes. Individual test input and stdout hashes are **not separately captured** for these in-process synthetic unit tests; consult the immutable commit and CI run as the primary evidence. This is a limitation for detailed forensic replay, not a reason to invent digests.
- These tests assert expected exceptions and retained state. A green unittest run establishes those assertions held on the tested head. It does not prove broader controller reachability, source authenticity, production deployment, or independent human challenge.

## Observed outcomes

All negative cases share the threat objective of inducing unjustified full-stack PASS. The attacker controls **only synthetic Python lifecycle-record fields**, not external services or repository governance. **Delivery** means the malicious input reaches the tested function; **integrity result** means the particular asserted invariant holds or fails. `RESISTED` here is scoped to that function and fixture, not a universal security claim.

| Test | Injected condition / expected safe result | Observed assertion on latest green CI | Attack delivered | Narrow integrity result |
| --- | --- | --- | --- | --- |
| `test_positive_control_is_terminalizable` | All five declared applicable lenses executed and PASS; no missing required evidence; terminalization gate accepts. | Empty error list and no guard exception. | N/A (positive control) | Positive control passed |
| `test_AA09_missing_material_lens_blocks_pass` | Remove security lens; reject full-stack PASS. | ValueError contains `security: lens disposition missing`. | YES (synthetic) | RESISTED |
| `test_AA09_unexecuted_material_lens_blocks_pass` | Composition applicable but unexecuted/INDETERMINATE; reject full-stack PASS. | ValueError contains `composition: full-stack PASS prohibited`. | YES (synthetic) | RESISTED |
| `test_AA09_terminal_transition_cannot_bypass_lens_guard` | Direct legal lifecycle transition attempts PASS while security lens absent; no terminal mutation. | ValueError contains missing security lens; state remains ASSESSED. | YES (synthetic) | RESISTED after remediation |
| `test_AA09_removed_entire_lens_ledger_cannot_bypass_guard` | Delete all lens records and attempt terminal PASS; preserve prior state. | ValueError contains `full-stack lens ledger missing`; state remains ASSESSED. | YES (synthetic) | RESISTED after remediation |
| `test_AA07_missing_required_probe_blocks_pass` | Require REQ-A but supply no attributable probe ledger; reject full-stack PASS. | ValueError identifies missing ledger. | YES (synthetic) | RESISTED |
| `test_AA07_unattempted_requirement_blocks_pass` | Require REQ-A and REQ-B but ledger attempts only REQ-A; reject full-stack PASS. | ValueError identifies missing REQ-B attempt. | YES (synthetic) | RESISTED |
| `test_AA07_unavailable_probe_is_attributed_not_conflated_with_success` | Supply `ATTEMPTED_UNAVAILABLE` and `NOT_EVIDENCED`; set applicable RAHP lens unexecuted/INDETERMINATE; reject full-stack PASS. | ValueError contains `rahp: full-stack PASS prohibited`. | YES (synthetic) | RESISTED |

## Confirmed issue and correction

Initial source inspection established that generic `assessment_controller.transition()` allowed terminal PASS without calling the separate full-stack gate. The first broad fix failed compatibility tests by also blocking the established portable specialist-result path. A subsequent edit failed Python parsing and was corrected. These are explicit failed validation attempts, not concealed or reclassified successes.

The successful final change gates a **declared positive full-stack claim** (`process_state=complete`, `assurance_state=pass`, or explicit `full_stack_assurance_required=True`) before terminal PASS, retaining legacy specialist behaviour. This is a *bounded implementation fix*. A caller that omits or misstates scope may still misrepresent a narrow specialist result as full-stack assurance **outside this gate**. That remains an assessor/reporting integration boundary.

## Coverage accounting and non-executed surfaces

The [campaign inventory](adversarial-assurance-qualification.md) records six threat surfaces and twelve hypotheses. This tranche materially exercised **controller/state manipulation (AA-07)** and **coverage omission (AA-09)**. These are not twelve distinct executed cases: eight unittest methods cover portions of two scenario families.

| Other attack surface | Status | Reason not counted as new executed red-team coverage |
| --- | --- | --- |
| False assurance / omitted declared obligations (AA-01, AA-02) | PARTIALLY_SUPPORTED, NOT_CAMPAIGN_EXECUTED | R1 documents structural completeness and existing duplicate/missing tests; caller-controlled omitted requirements cannot be detected without an external authoritative scope source. Requires caller/report integration test. |
| Authority laundering (AA-03) | NOT_EXECUTED | R2 only accepts declared source pins, no authentication. A controlled authoritative source/recognition policy must be explicitly provided rather than invented. |
| Evidence corruption/replay (AA-04–06) | NOT_CAMPAIGN_EXECUTED | R2/R3 and standalone replay already contain bounded synthetic exercises, but they do not establish cryptographic source verification or independent re-execution. |
| Assessor/report manipulation (AA-11/12) | NOT_EXECUTED | R3 challenges remain OPEN by contract; no concrete consumer-facing presentation boundary has been selected and executed under adversarial input. |

A green CI run for an existing R1/R2/R3 test is **not** retroactively classified as successful red-team execution of these surfaces. All unexecuted hypotheses remain visible.

## Independent-review and release disposition

External protocol: [independent adversarial challenge](adversarial-assurance-reviewer-protocol.md). An external reviewer can select a new hypothesis, create fresh fixtures, record raw results/hashes, challenge methodological scope and issue independently owned findings. **No independent execution has been received**.

**Release decision: commit-only.** This increment contains a narrow fix, synthetic regression evidence and reviewer documentation. Revisit versioning only for a materially consumable baseline under normal release gates; neither maintenance activity nor a green campaign justifies an assertion of independent assurance.

## Residual risk and completion statement

This is a completed **maintainer-side AA-07/AA-09 regression tranche**, not a completed six-surface adversarial campaign. Residuals are: authenticated source/authority binding, caller-supplied assessment scope, report truthfulness, end-to-end guard reachability outside exercised functions, and independent attack invention. No acceptance criterion requiring those properties should be checked based on this record alone.
