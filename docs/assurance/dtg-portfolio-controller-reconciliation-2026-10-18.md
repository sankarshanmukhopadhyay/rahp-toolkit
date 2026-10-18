# DTG portfolio snapshot controller reconciliation — 2026-10-18

**Purpose:** Auditable transfer/disposal record for RAHP issues [#1028](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1028), [#1040](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1040), [#1042](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1042), [#1043](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1043), [#1045](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1045), [#1046](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1046) and [#1047](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1047). These issues are immutable snapshot-specific controller records. This file consolidates *their explicit UNMAPPED subsets*, not all qualifying findings, and never marks implementation assurance PASS.

## Snapshot inventory

| Controller | Snapshot date | SHA-256 prefix | Qualifying findings | UNMAPPED entries |
|---|---|---|---:|---:|
| #1028 | 2026-10-14 | `d9376b63c67a` | 19 | 10 |
| #1040 | 2026-10-15 | `9cc5d6aadf3d` | 21 | 10 |
| #1042 | 2026-10-15 | `dfd064bd455b` | 24 | 12 |
| #1043 | 2026-10-16 | `71712d87c90d` | 31 | 12 |
| #1045 | 2026-10-16 | `b6d91818a00b` | 38 | 12 |
| #1046 | 2026-10-17 | `46a8f7a819cf` | 40 | 12 |
| #1047 | 2026-10-17 | `b5f7925b2105` | 44 | 13 |

The seven lists contain **14 distinct UNMAPPED finding IDs**. A finding disappearing from the newest snapshot is **not** proof that its older disposition was completed; the earlier `3b62...` dependency finding is present in six earlier controllers but not in #1047.

## Unique UNMAPPED finding-to-owner ledger

| Finding ID | Snapshot controllers | Durable owner | Transfer status and unresolved evidence |
|---|---|---|---|
| `58f3e21a7dd7227a41ab` | 1028,1040,1042,1043,1045,1046,1047 | [#272](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/272) | Dependency update; transitive assurance changes not yet classified, not automatic no-action |
| `d6f06da6be6c24f2917a` | all 7 | [#994 Scope A](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994) | Member-portal trigger-link runtime evidence outstanding |
| `14345600ab746827b9d8` | all 7 | #994 Scope A | Trigger-link parser binding evidence outstanding |
| `3b62b0cd590b9b45b3da` | 1028,1040,1042,1043,1045,1046 | [#272](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/272) | Trust Tasks dependency 0.23.0→0.23.1; semantic equivalence unverified |
| `5daf04aa9bf26ef41594` | all 7 | #994 Scope A | Member-console target distinction evidence outstanding |
| `c15ef701e115583e2756` | all 7 | #994 Scope A | Contact DID/domain binding evidence outstanding |
| `ffa81bd16533fbada219` | all 7 | #994 Scope A | Unknown-community join from sign-in code; confirm residual coverage within Scope A before terminal disposition |
| `220fb4eea5c0200f190b` | all 7 | [#994 Scope C](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994) | Source/test rebaseline via merged [#1048](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1048); C03/C04/C09/C10 nonterminal |
| `1c2869a18869681e741b` | all 7 | #994 Scope B | Task-initiated foreign-protocol binding runtime evidence outstanding |
| `e0da9d8b03dd7f460a60` | all 7 | [#1022](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1022) | First-administrator bootstrap spec interpretation and runtime evidence unresolved |
| `2a5769f69aaf67636efe` | 1042,1043,1045,1046,1047 | [#691](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/691) | Provisional task-visible vetter-refusal semantics; assess scope and transfer further if outside Trust Task error contract |
| `93dc1d4c3ed05d832936` | 1042,1043,1045,1046,1047 | [#1051](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1051) | New bounded witness task owner. VTI PR [#2123](https://github.com/OpenVTC/verifiable-trust-infrastructure/pull/2123), merged 2026-10-15; source/test evidenced, independent consuming path still needed |
| `3b5cd4abd5496f985033` | 1047 | [#481](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/481) | Community-room metadata and administrator update, with authorization and disclosure reassessment; spec [#805](https://github.com/trustoverip/dtgwg-trust-tasks-tf/issues/805) |
| `d6faa3f201a07951f331` | 1047 | [#1022](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1022) | TEE bootstrap claim-DID implementation movement, VTI PR #2182; not proof of prior authority |

**Meaning of “durable owner”:** the issue has been linked and, for newer residuals, received an explicit reassessment comment; it does not mean the security proposition is proven, that privacy has been assessed, or that every downstream case has been exercised.

## Controller closure gate

The snapshot issue bodies themselves impose a broader closure rule: **all qualifying findings**, including `combined`, `covered`, `no-action`, external DPIP referrals and unresolved child reviews, must have accountable dispositions or transfers. The table above accounts for the union of **UNMAPPED** items only. It does not itself authorize closure of the seven controllers.

Before closing an individual controller:

1. Reconcile its full source finding roster, not only UNMAPPED IDs, against the routing journal and current durable issue states.
2. Confirm `no-action` is reasoned, not a default caused by unknown semantics.
3. Confirm every `combined`/cross-spec/DPIP child either has a terminal decision or an explicitly accepted successor issue.
4. Record source snapshot full SHA-256, unique IDs, reassessment conditions, and whether the source has changed since the snapshot.
5. Close as **transferred** only when no qualifying item remains without ownership; unresolved evidence can remain open on the accepted narrow owner. Never mark a source-only or unexecuted trace PASS.

The provisional map in #1047 has been superseded in part by direct verification of [VTI PR #2123](https://github.com/OpenVTC/verifiable-trust-infrastructure/pull/2123), and room/vetter/first-boot transfer comments on #481/#691/#1022. Cross-repository specification authority remains upstream. **No controller was closed solely by preparing this report.**

## Addendum: controller #1054 and the lifecycle-safety boundary

[Controller #1054](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1054), 2026-10-18 exact snapshot digest `f2aac57efb2cb547b79de37f86242dfdaead40f2cefc2f05fdde185355c2dc78`, reports 48 qualifying findings: 15 UNMAPPED, 9 no-action, 21 combined, 3 covered. Its machine-readable [UNMAPPED ledger](../../data/assurance/controller-1054-routing.json) is tested by `python3 tools/validate_controller_routing_manifest.py` and `python3 -m unittest tests.test_controller_routing_manifest -v`. It explicitly forbids deriving full controller closure from an UNMAPPED-only mapping.

Existing durable owners: #691 (vetter refusal, provisional), #481 (room administration), #272 (dependency delta), #1051 (VTA witness), #994 (sign-in and protocol-signing), and closed bounded assessment #1022 for the *historical implemented* TEE bootstrap changes. The three observed TEE finding IDs `3474aeed99edbff13c5c`, `d6faa3f201a07951f331`, and `f25a1dc1e894092b09d0` link to #1022 **as already-assessed source triggers, not a new authority-conformance PASS**. Normative interpretation remains with [VTI #64](https://github.com/trustoverip/dtgwg-vti-spec/issues/64). A genuinely new implementation/interpretation change must receive a fresh bounded assessment and cannot be silently routed into closed #1022.

Two new substantive finding IDs need exact semantic owner verification, and remain **unresolved** in the ledger rather than assigned by title resemblance:

- `ffae6e60e266a4363cc4`: Trust Tasks persona/contact stars, petnames and holder-agent lists, and the addition of administrative directory/group events. Verify the exact change against the current DTG directory/privacy reviews; test cross-context disclosure, agency and retention semantics.
- `e11d65af7635eafb7ecb`: VTI community directory and group publication for non-recognition purposes. Verify VTI-DIR-001–130 and VTI-REG-001/004 against the specification status and actual consuming path; decide if #689 or #690 cover anything specific or if a narrower durable review is needed.

**Lifecycle defect still unresolved:** #121 and #527 are OPEN despite explicit completed/transferred closure comments. These are historical wrappers, and must not be used as ever-growing journals for fresh materiality. Investigate the publishing workflow's closed-owner reactivation rule in its authoritative source before changing it; only transfer truly unowned new propositions to narrower owners. A checkpoint that merely closes these two again is not a durable fix. No automatic GitHub mutation is performed by this manifest validator.

Remaining mandatory closure gate for #1054: all **48** qualifying finding dispositions, including 21 combined, 3 covered, 9 no-action and any linked DPIP referrals, independently reconciled. The other seven snapshot controllers likewise remain open pending full routed-child reconciliation.

## Post-merge owner convergence

The two initially unassigned #1054 findings have since been explicitly transferred to [#1057](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1057), a bounded holder-private contact vs community directory/group publication assessment, supported by pinned Trust Tasks PR #815 and VTI spec PR #68. They are **owned for review**, not assurance-passed. The machine-readable ledger now contains 15 mapped/reviewed findings, zero unowned UNMAPPED entries. **Controller closure remains forbidden** until combined/covered/no-action/DPIP routing for all 48 qualifying findings is reconciled.

## Proposed terminal-wrapper lifecycle guardrail

The reviewed root cause is in `tools/materiality_journal_gate.py`: any previously unseen finding directed to a closed owner sets `reopen_closed_owner=True`, even if the issue is an explicitly transferred historical wrapper, and `tools/publish_assessment_issues.py` honors that signal. This conservative policy is correct for normal closed assessments, but it can turn completed historical wrappers into rolling journals.

The guarded change introduces an **explicit opt-in marker** (`<!-- rahp-terminal-wrapper:transferred -->`) for a wrapper that has a documented and independently reviewed transfer matrix. With the marker and no separate invalidation reason:

- A new material finding goes into a **new bounded successor assessment**, uniquely identified by the historical wrapper key and the SHA-256 digest prefix of the sorted new finding identities.
- Repeated observations of the same novel finding set reuse the same successor identity. No novel findings means no successor or reopening.
- The successor body includes only the previously unseen finding rows and mandatory evidence/ownership/DPIP acceptance steps. It is not a substantive PASS.
- The historical wrapper remains CLOSED and its terminal history is preserved.
- An explicit invalidation of the old terminal conclusion still reopens the original issue. Unmarked normal closed owners retain their existing fail-closed reopening behavior.

The marker **must not** be placed on open or unresolved assessments merely to suppress queue growth. In this tranche it is reserved for #121 and #527, whose transfer decisions and successor owners are documented. The marker is not a claim that their successors are complete. Regression coverage is in `tests/test_portfolio_materiality_journal.py`, and the existing issue publisher continues to enforce unique assessment keys/idempotence.
