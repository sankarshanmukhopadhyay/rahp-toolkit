---
layout: default
title: "Adversarial cross-boundary qualification"
parent: Learn RAHP
---
# RAHP #1023: remaining adversarial surfaces

**Maintainer-authored and synthetic. No independent red-team execution is claimed.**

Tracking: [#1023](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1023). Earlier controller and coverage tranche: [execution ledger](adversarial-assurance-execution-ledger.md). Reviewer instructions: [independent challenge protocol](adversarial-assurance-reviewer-protocol.md).

## Test design and targeted surfaces

The dedicated `tests/test_adversarial_boundaries_1023.py` suite uses existing optional R1 (evidence adequacy), R2 (temporal applicability) and R3 (declared run comparison) public APIs. No new engine or assurance state has been introduced.

| Case | Controlled adversarial change | Safe or explicitly bounded observed property | Surface |
| --- | --- | --- | --- |
| AA-01 | Remove a material requirement from caller-declared R1 scope, along with its observation. | R1 can still return structural PASS for **the reduced declared scope**. Explicit `authority_note` says this is not RAHP terminal assurance; an external authoritative coverage manifest would be required to detect omission. | False assurance: demonstrated scope-declaration blind spot |
| AA-02 | Add contradictory observation to one requirement. | R1 returns INDETERMINATE and CONFLICT. | False assurance: conflicting evidence |
| AA-03 | Supply an arbitrary synthetic repository/revision source pin. | R2 may return APPLICABLE only for **declared** temporal state, while declining authenticity or authority claims. | Authority laundering |
| AA-04 | Insert late-recorded retroactive assertion; move cutoff. | Original as-known-at result is preserved; later cutoff produces CONFLICT and INDETERMINATE. | Evidence replay / temporal distortion |
| AA-05 | Assert matching arbitrary SHA-256 digests and matching evaluator outcomes, without real input hashing. | R3 returns DECLARED_MATCH, not proof of independent replay or actual byte equality. | Evidence identity / provenance laundering |
| AA-06 | Change one asserted input digest. | R3 returns DIFFERENT_INPUT. | Evidence substitution detection in declared records |
| AA-11 | Combine structurally positive R1 and temporally applicable R2 results. | Both outputs preserve qualification notes, neither includes `terminal_outcome`. A third-party report can still lie by omission; that lies outside these evaluators. | Assessor/report manipulation |
| AA-12 | Add unresolved scope challenge while runs remain declared-equal. | R3 preserves OPEN challenge alongside DECLARED_MATCH. | Challenge suppression at presentation boundary |

The executable tests check **the bounded API properties shown**, not generalized end-to-end attack resistance. Positive R1/R2/R3 results with synthetic attacker-controlled declarations are important counterexamples: an external consumer *could* overclaim assurance even when these evaluators behave exactly as designed.

## Reproduce

From the repository root at an exact pinned commit:

```sh
git rev-parse HEAD
python3 --version
python3 -m unittest tests.test_adversarial_assurance_1023 tests.test_adversarial_boundaries_1023 -v
python3 -m unittest discover -s tests -p 'test_*.py'
```

Inspect CI for exact SHA and validate workflow run. Green tests mean that these expectations held at that commit. Runtime evidence should be linked before recording a RESISTED or boundary-demonstrated disposition.

## Classification / residual risk

- **Implementation remediation** (AA-07/AA-09) was delivered through merged PR #1024, with CI-backed evidence in the earlier ledger.
- **Methodology/caller responsibility** (AA-01): required scope is declared by the caller, not checked against independently established authoritative obligations; changing R1 to presume a normative completeness source would exceed its contract.
- **External authority prerequisite** (AA-03): R2 cannot verify whether a source pin belongs to a legitimate authority; a provenance fetch/verifier and governed recognition policy would be required.
- **Integrity prerequisite** (AA-05): a declared hash cannot prove actual input-byte equality, source integrity, evaluator execution or independence.
- **Presentation responsibility** (AA-11/12): a consumer could suppress authority notes or unresolved challenges when summarizing bounded outputs. No claim that all report generation or other controller entry points were red-teamed.

These limitations are **documented residuals**, not unqualified findings of an evaluator defect. Do not reclassify a declared structural PASS as compromise without evidence of prohibited terminalization or false consumer claims.

## Acceptance and independent challenge

This tranche permits a bounded assertion that **all six planned surfaces received explicit analysis plus executable synthetic pressure tests** when the current test commit's CI is green. It does **not** mean all plausible attacks are covered or independent red teaming has happened. An independent participant must devise novel controlled attacks, reproduce claims with raw evidence, and challenge the assessment's coverage and underlying assumptions.
