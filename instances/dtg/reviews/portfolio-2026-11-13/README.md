---
layout: default
title: "DTG 13 November 2026 materiality replay"
nav_exclude: true
---

# Source-pinned replay packet for DTG Portfolio → RAHP #1191

The controller [#1191](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1191) was closed for **finding-level reconciliation and durable ownership**, not for proof that each successor is assured. This deployment-local packet records the **23 bounded consumer and negative cases** required to revisit [#1194](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1194), [#1195](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1195), [#1197](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1197), [#1196](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1196), and [#827](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/827). Its authority is confined to `instances/dtg/`; it changes neither portable RAHP methods nor upstream DTG specifications.

## Evidence and authority

The original 13 November snapshot is at [Portfolio Monitor findings](https://raw.githubusercontent.com/sankarshanmukhopadhyay/dtg-portfolio-monitor/main/data/findings/2026/11/13.json), digest `sha256:6b8f4bb2327b7319e6a0ff65708e50a7ae69ac04f07c6132d565a743e2a61da5`. #1191's ledger preserves the 45 originally unmapped finding IDs and their downstream owners. The packet pins **source baselines**, not current deployment configurations. Each case starts with `execution_state: not-run`, `result: INDETERMINATE`, and no evidence references, because a developer-reported test, merged PR, source inspection or this matrix is **not independent consumer execution**.

The current source-level judgments and false-success boundaries are recorded on each linked issue. In particular:

- Purpose-of-use: the earlier missing room/VAC enforcement was subsequently implemented through OpenVTC VTI PRs #2541, #2545, #2546 and #2549. Distinguish enforceable VAC chain purposes from VTA ACL purposes and old-version behavior.
- Collector/notification: VTI-NTF-093 (operator-level, default-off) was withdrawn. VTI-NTF-094–098 now specify per-context default-on, with an off-only operator suspension. A config from an earlier default-off installation is not evidence that its migrated deployment stays off. The `notCollectable` client exception needs candidate-set qualification.
- Memory/audit: post-change keyed commitments improve audit-key privacy; pre-change cleartext memory keys remain in historical immutable audit records until actual retention sweeps (VTI Spec PR #113). VTI-AUD-006 must not be silently asserted satisfied.
- DID lifecycle: did:webs operation-only implementations were followed by wire versions; the classed-create PR records an unresolved provisioned-service-context marker gap. Historical DID observation, control continuity and identity continuity remain distinct.
- Key roles: `vta/dids/*` method-neutral normative role/recovery tasks and resumed design work do **not** establish a deployed conforming role-separated/level-3 recovery implementation. Ordinary did:webs rotation must not be promoted to key-role assurance.

## Reproduction with locally available authoritative checkouts

The assessment operator supplies **separately obtained upstream repositories** at exactly the SHAs in [replay-cases.yaml](replay-cases.yaml). Never run against an unqualified moving `main` and label it as this packet's baseline.

```bash
# In the RAHP Toolkit checkout:
python3 -m unittest discover -s tests -p 'test_dtg_2026_november_replay_packet.py'
python3 tools/validate.py

# In separately checked out OpenVTC/verifiable-trust-infrastructure:
git rev-parse HEAD    # must equal the full pin in replay-cases.yaml
cargo test -p vta-service vti_ntf_095 -- --nocapture
cargo test -p vta-service vti_ntf_082 -- --nocapture
cargo test -p vta-service vti_acl_ -- --nocapture
# Inspect precise test target locations at the pinned revision before filtering.
# In separately checked out OpenVTC/openvtc:
git rev-parse HEAD    # must equal its own full pin
cargo test -p openvtc-core collection -- --nocapture
```

These commands are **candidate reproduction entry points, not claims of runs performed**. Cargo package/feature requirements and test names must be confirmed at the pinned source. In particular the positive tests do not simulate a deployed VTA + client + mediator or a multi-system room host; passing them is necessary evidence for their local claims but not sufficient for composition assurance. The operator should run actual producer and consumer through the documented entry points, record effective protocol version and actor/context, and retain minimal redacted observed responses and audit records.

For every replay case, use the existing [runtime evidence template](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/docs/review/dtg-runtime-evidence/evidence-template.yaml) as the evidence format. Pin each component, record expected and **actual** outcome, command/CI run and environment, no-effect/mutation and retry results, and privacy/non-repudiation limitations. An observer/provider fixture must remain distinguishable from an actual deployed trace. Preserve genuine failure and unavailable results without coercing them to PASS. Do not put secrets, raw bearer tokens, private memory content or unredacted human identifier metadata into Git.

## Acceptance and disposal

1. For **each case**, independently establish the source/checkouts and relevant preconditions; run the named consumer path (or explicitly retain `INDETERMINATE`).
2. Capture negative and false-success results as *observed* evidence. A failed client, an unsupported type, an omitted receipt and a deferred/missing audit reference must not become positive assurance evidence.
3. Reconcile each finding ID through its owning issue. **Only that owner** makes an assurance disposition. A source-positive or green unit suite is not a composed-privacy PASS.
4. Refer a **specific** observed privacy-composition or retention exposure through the canonical RAHP → DPIP path, retaining specialist authority.
5. Close each owner only when its genuine issue acceptance criteria are met, or a precisely scoped residual has been transferred with its evidence, accountable successor and retest trigger.
6. Do not reopen #1191 or its historically completed wrappers to serve as a growing journal.

No new continuous monitoring, automatic assessment claims, security permissions, schemas or upstream changes are created by this packet. It is a reviewable **unexecuted** test contract until execution evidence is recorded.
