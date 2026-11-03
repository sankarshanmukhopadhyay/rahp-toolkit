# Trust Tasks Rust releases 0.24.4–0.29.0: normative delta and RAHP consumer-impact disposition

**Owner:** [RAHP #272](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/272)  
**Source repository:** [trustoverip/dtgwg-trust-tasks-tf](https://github.com/trustoverip/dtgwg-trust-tasks-tf)  
**Assessment date:** 2026-11-03  
**State:** source-tree inventory complete; RAHP scoped ownership/negative-coverage judgment; **NOT** downstream implementation/conformance assurance  
**Audit dataset:** [frozen delta manifest](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/data/assurance/trust-tasks-release-delta-272.json)

## Decision

The later Trust Tasks releases do **not** merely regenerate bindings. They introduce and modify substantive specification and schema surfaces. The correct overall source-delta classification is **NEW**, with certain precise propositions **TRANSFERRED** to existing issue owners, and other task families explicitly **NOT_ASSESSED** by the historical RAHP reviews.

These three statements are deliberately separate:

1. The four declared release tags and the exact changed normative paths are **source-inventoried**.
2. The existence and narrowness of named RAHP residual owners are **documented**.
3. Whether a particular current VTA/VTC, VTC integration or other consumer uses and correctly enforces each changed task version is **not established** by this work.

No reviewed assurance claim is upgraded to PASS; no historical #282, #826 or #837 finding is overwritten. The generic release-delta wrapper can be **closed after the source/owner ledger is accepted**, with the newly identified document-size consumer contract transferred to [#1174](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1174), because the ledger records these limits, preserves the non-covered families explicitly, and leaves specific consumer questions to their actual owners or future activation on a defined assessed consumer. Closure must not be interpreted as universal compatibility or as an assertion that all new task families have an owner or were tested.

## Exact release scope

Every `git/trees/{tag}?recursive=1` response reported `truncated=false`. The retained JSON inventory records **every changed path** ending in `spec.md` or `.schema.json` below `specs/`, including before/after Git blob IDs, interval, and one longest-prefix family classification.

| Tag | Immutable Git tree SHA |
| --- | --- |
| `trust-tasks-rs-v0.24.4` | `9e65cdc32754e64be82db66db7605401668931d3` |
| `trust-tasks-rs-v0.26.3` | `b0da6bcda5a54eda479c53e861ec2e4d4ad5d05d` |
| `trust-tasks-rs-v0.27.1` | `2b50e6ef165777c348525a676c66b56dea1c2387` |
| `trust-tasks-rs-v0.29.0` | `a8d5959fd9e5a585b05f3c7722f111d89f8ad84b` |

| Interval | All changed Git blob paths | Changed normative/schema paths in the manifest |
| --- | ---: | ---: |
| `0.24.4 → 0.26.3` | 967 | 226 |
| `0.26.3 → 0.27.1` | 1,339 | 14 |
| `0.27.1 → 0.29.0` | 1,259 | 152 |
| **Total interval observations** | **3,565** | **392** |

These are **interval-path observations**, not 392 independent requirements. A path modified in two intervals is counted twice; generated binding changes and non-normative files are excluded from the detailed 392-path census. The GitHub compare endpoint can truncate changed files at 300; this reconciliation uses complete Git trees, not that incomplete list.

## Actual RAHP consumption boundary

RAHP is **not** an importer of `trust-tasks-rs` itself; the repository contains Python/npm assessment tooling, source-pinned specification reviews and cross-specification scenarios. In particular:

- [`SR-002`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/examples/trust-tasks-spec/pressure-test.yaml) reviewed Trust Tasks `fbe196a8a17ba3f99d0657a64be5ac58621023a1` in August 2026.
- [`SR-XSP-001`](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/examples/cross-spec/trust-tasks-credspec/v1.9-current-pressure-test.yaml) reviewed Trust Tasks `134733ff934775db522522dc26cb79836da29256` with Credential Specification `2b403b607aaec9d84f78189a55337c677f3cd2ed`, and retained its own historical case results.
- The [runtime evidence Scope C rebaseline](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/docs/review/dtg-runtime-evidence/scope-c-vti-2026-10-18-rebaseline.md) separately evaluates VTI #2057 source/test behavior for JWS and CSR at a named implementation commit. It does **not** claim full current Trust Tasks release adoption.

Thus the observed consumer version for the first two RAHP records is **their separately pinned upstream commit**, not automatically 0.24.4, 0.26.3, 0.27.1 or 0.29.0. The new release tags are **triggers for reassessment**, not retroactive changes to already frozen review targets. No current VTI `Cargo.lock` or deployed integration was asserted or tested in this tranche.

## Normative change families and narrow ownership

The [machine-readable manifest](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/data/assurance/trust-tasks-release-delta-272.json) preserves all exact paths and interval/family counts. This table explains the assurance judgment; **a link to an owner indicates relevance only to its explicitly stated subset**.

| Family / representative changed contract | Nature of change | RAHP consumer/owner disposition |
| --- | --- | --- |
| `specs/spec.meta.schema.json`: new per-task `maxDocumentBytes` | **New** normative size/acceptance surface, not an editorial version bump. A declared bound limits refusal of an in-bound document *on size grounds alone*; oversized bodies and transport limits remain distinct. | **Transferred** to [#1174](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1174) for bounded per-task size admission, threshold/undeclared-limit and error-fidelity evidence. No generic compatibility PASS. |
| `specs/acl/**` 0.2; `specs/auth/step-up/**` | **New/changed** approval, grant, role/scope and proof semantics. | [#826](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/826) owns wire/proof version; [#837](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/837) owns stale/expired approval; [#908](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/908) owns a particular waiver/audit failure. **Not** blanket ACL 0.2 acceptance. |
| `specs/auth/signing-key/**` | **New** key authorization/enrolment/atomic replacement contracts. | [#899](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/899): exact enrolment and replacement residual; broader auth variants unassessed. |
| `specs/device/_shared/{0.1,0.2}/device-binding.schema.json` | **New values** in named capability sets: `sign-sshsig`, `sign-jws`, `sign-csr`, `external-accounts-manage`, `external-auth-use` (0.1; corresponding camelCase in 0.2). | [#994](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994) Scope C covers **JWS/CSR only**. SSHSIG and external auth capability enforcement are explicitly **NOT_ASSESSED** here. A schema enum is not a capability-enforcement trace. |
| `specs/keys/sign-{jws,csr}/0.1` | **New** protocol-signing task contracts. | **Transferred** to [#994 Scope C](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994), with source/test evidence and runtime residuals already recorded. |
| `specs/keys/sign-sshsig/0.1` | **New** SSH signature signing contract. | **NOT_ASSESSED** by the JWS/CSR Scope C cases; requires a defined user/relying-consumer target before activation. |
| `specs/auth/oob/**`, `specs/auth/authenticate|refresh`, shared session types | **New** out-of-band authentication and session tasks. | [#994](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994) Scope A covers a **subset** of wallet sign-in/trigger-link flows, not all OOB family semantics. Other auth variants **NOT_ASSESSED**. |
| `specs/external/**` | **New** external account provisioning, secrets, keys, credentials and signing operations. | **NOT_ASSESSED** in scoped historic RAHP reviews. Neither #994 Scope C nor #899 implicitly covers external-account authority. |
| `specs/rooms/**`, `specs/vtc/rooms/**`, `specs/vtc/storage/**`, room-storage shared schema | **New/changed** record, blob, room visibility, ownership and storage semantics. | [#481](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/481) is the existing **data-room coordination** owner, not a claim of exhaustive room-task or storage implementation assurance. |
| `specs/vtc/vetting/**`, `specs/vetting/**` | **New/changed** vetter identity, hidden-vetting publish/admission, disclosure and retention semantics. | [#889](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/889) and [#642](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/642) cover bounded privacy/binder concerns; no blanket source-version conformance. |
| `specs/vtc/join-requests/**`; `specs/vtc/members/**` | **New/changed** applicant recovery, wallet sessions, member authority/lifecycle and structured errors. | [#898](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/898) redelivery, [#689](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/689) public discovery, [#691](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/691) error fidelity, [#610](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/610) contestability: narrow **partial** coverage. |
| `specs/vtc/admin/**`, `specs/vtc/operator/**`, other VTC admin/community/website contracts | **New/changed** cooling-off, offline actions, events and administrative tasks. | [#908](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/908) for mandatory audit waiver, [#610](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/610) for redress; general new task surface **NOT_ASSESSED**. |
| `specs/git-ns/**` | **New/changed** forge-rights, bridge status, task error and administrative projection contracts. | [#797](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/797) provenance and [#908](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/908) limited waiver/audit. No conclusion that every grant/bridge task now conforms. |
| `specs/task-consent/**`, `specs/witness/**`, `specs/webvh/witness/**` | **New/changed** consent decision, witness signature/lifecycle. | [#610](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/610) contestability; [#1051](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1051) witness authority and [#1082](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1082) witness lifecycle. Partial transfer only. |
| `specs/vta/**`, `specs/vault/credentials/**`, residual `specs/vtc/**` | Other new VTA/admin variants and edited credential task text. | **NOT_ASSESSED / UNCERTAIN** where not directly tied to an existing asserted RAHP review case. No preservation or runtime conclusion inferred from pathname alone. |
| Codegen/error declaration and changed `permissionDenied` semantics | Framework generator and source-level error meaning can change consumer decisions without affecting HTTP status. | [#691](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/691) owns semantic outcome fidelity; merged Trust Tasks #575 and VTI #1600 are source/test progress, **not** a composition PASS. |

**Important:** the per-family grouping is exhaustive for the manifest's scoped `spec.md` / `.schema.json` files, but it is **not** an assertion that every sentence in each specification was semantically compared. The groups without a concrete existing RAHP consumer obligation are marked **NOT_ASSESSED** deliberately, not secretly classified `preserved`.

## Why a new issue is not automatically required for every new task

Historical RAHP reviews contain specific, version-pinned assurance propositions, not a contract to evaluate every task added to the Trust Tasks catalogue in perpetuity. A change in an unconsumed family is **new source scope**, not necessarily a regression in an earlier assessment. A new RAHP issue becomes warranted when a defined relying consumer, normative constraint and falsifiable test show a material unowned proposition. If the operator chooses to assess external accounts, SSHSIG or other new families, that is a **new bounded assessment**, not an implicit extension of #272.

This decision prevents both silent false compatibility and an issue explosion from counting generated files as independently actionable vulnerabilities.

## Reproduction and acceptance

Run on a clean RAHP checkout:

```bash
python3 -m unittest tests.test_trust_tasks_release_delta_272 -v
python3 tools/validate.py
```

The ledger regression checks four immutable non-truncated Git tree pins; **392 changed normative path observations**; one-and-only-one longest-prefix classification per path; Git blob identifiers; exact per-interval and per-family counts; scoped owner references; and preservation of `runtime_pass=false` and `composition_pass=false`. The checked-in historical inventory provides offline evidence; the test does not fetch or certify the upstream repositories at execution time.

Reperforming the source census independently requires fetching the four same immutable Git tree refs and comparing `path → Git blob SHA` maps for all `specs/**/spec.md` and `specs/**/*.schema.json`. The 300-file GitHub compare output must not be treated as complete.

## Final scope-limited judgment

**Release-delta:** `NEW` with specific `TRANSFERRED` cases and explicit `NOT_ASSESSED` additions.  
**Existing RAHP review invariants:** not invalidated solely by the new tags; historical findings remain at original pins.  
**Current cross-repo implementation compatibility:** `INDETERMINATE`; not tested here.  
**Future activation:** new source-version adoption by an assessed VTI/VTC or other consuming implementation, or a new material RAHP proposition, requires another exact-target review; prior wrapper closure is not a permanent exemption.  
**Human risk acceptance:** not supplied, not inferred.

**Suggested #272 disposition:** close as **source delta and affected-assurance ownership reconciled**, not as specification/implementation alignment PASS. Preserve #282, #826, #837 and all specialist residual issues unchanged. Do not publish a release based on this housekeeping change.
