# DTG runtime evidence dependency matrix

Issue: #994  
Packet: DTG runtime evidence — consolidated Scopes A, B and C  
Status: downstream dependency matrix

## Purpose

This matrix consolidates the current downstream state after Scope A, Scope B and Scope C have each been recorded in the RAHP Toolkit runtime evidence packet.

It does not mark any runtime case as PASS. The available evidence remains source/spec and implementation-change evidence. Runtime traces, retained-evidence inventories and privacy/DPIP dispositions remain incomplete.

## Source documents in this packet

- `scope-a-evidence-records.md`
- `scope-b-evidence-records.md`
- `scope-c-evidence-records.md`
- `scope-c-local-capability-assessment.md`
- `cases.yaml`
- `evidence-template.yaml`
- `dpip-applicability-template.md`

## Scope-level disposition

| Scope | Assurance surface | Cases | Source/spec evidence | Runtime traces | Local downstream execution | External/runtime dependency | Current disposition |
|---|---|---:|---|---|---|---|---|
| Scope A | Trigger-link, wallet sign-in and contact-DID binding | 10 | Present from transferred implementation/source findings. | Missing. | No local RAHP Toolkit harness found for the composed flow. | Runtime owner or implementation traces needed. | `INDETERMINATE` |
| Scope B | VTI foreign-protocol binding | 9 | Present from `trustoverip/dtgwg-vti-spec#60`. | Missing. | No local RAHP Toolkit harness found for task-bound foreign-protocol exchange. | Runtime owner or implementation traces needed. | `INDETERMINATE` |
| Scope C | VTA-held-key `sign-jws` / `sign-csr` protocol signatures | 7 initial cases, with additional deferred cases in `cases.yaml` | Present from `trustoverip/dtgwg-trust-tasks-tf#749`. | Missing. | No local RAHP Toolkit custodian/runtime harness found. | Evidence request filed as `trustoverip/dtgwg-trust-tasks-tf#752`. | `INDETERMINATE` |

## Case dependency matrix

### Scope A — trigger-link, wallet sign-in and contact-DID binding

| Case | Current disposition | Missing runtime evidence | Local execution state | Closure blocker |
|---|---|---|---|---|
| `A01-valid-member-portal` | `INDETERMINATE` | Valid member portal sign-in trace, target/session/audit record, retained-evidence note. | No local composed-flow harness. | Runtime trace absent. |
| `A02-valid-operator-console` | `INDETERMINATE` | Valid operator-console sign-in trace distinguishable from member portal. | No local composed-flow harness. | Runtime trace absent. |
| `A03-wrong-target-member-console-mismatch` | `INDETERMINATE` | Negative trace proving member/operator target mismatch fails closed. | No local composed-flow harness. | Negative runtime trace absent. |
| `A04-expired-trigger-link` | `INDETERMINATE` | Expired-link rejection trace. | No local composed-flow harness. | Negative runtime trace absent. |
| `A05-replayed-trigger-link` | `INDETERMINATE` | First-use and replay rejection traces. | No local composed-flow harness. | Negative runtime trace absent. |
| `A06-wrong-page-origin` | `INDETERMINATE` | Wrong-origin rejection trace and origin-binding evidence. | No local composed-flow harness. | Negative runtime trace absent. |
| `A07-wrong-community-did` | `INDETERMINATE` | Community-DID mismatch rejection trace. | No local composed-flow harness. | Negative runtime trace absent. |
| `A08-disconnected-wallet` | `INDETERMINATE` | Disconnected/no-wallet non-positive path trace. | No local composed-flow harness. | Runtime trace absent. |
| `A09-locked-wallet` | `INDETERMINATE` | Locked-wallet prompt or non-positive outcome trace. | No local composed-flow harness. | Runtime trace absent. |
| `A10-invalid-domain-linked-contact` | `INDETERMINATE` | Invalid domain-linked contact / well-known DID configuration rejection trace. | No local composed-flow harness. | Runtime trace absent. |

### Scope B — VTI foreign-protocol binding

| Case | Current disposition | Missing runtime evidence | Local execution state | Closure blocker |
|---|---|---|---|---|
| `B01-valid-task-bound-foreign-protocol` | `INDETERMINATE` | Task-bound exchange trace with task authority, challenge, audience and task-visible outcome. | No local task/protocol harness. | Runtime trace absent. |
| `B02-direct-endpoint-no-task` | `INDETERMINATE` | Direct endpoint invocation rejection without task context. | No local task/protocol harness. | Negative runtime trace absent. |
| `B03-reuse-after-completion` | `INDETERMINATE` | First-use and reuse rejection traces. | No local task/protocol harness. | Negative runtime trace absent. |
| `B04-expired-exchange` | `INDETERMINATE` | Expired exchange non-success task outcome. | No local task/protocol harness. | Negative runtime trace absent. |
| `B05-wrong-audience` | `INDETERMINATE` | Wrong verifier/client audience rejection trace. | No local task/protocol harness. | Negative runtime trace absent. |
| `B06-wrong-challenge` | `INDETERMINATE` | Challenge mismatch rejection trace. | No local task/protocol harness. | Negative runtime trace absent. |
| `B07-task-authority-invalid` | `INDETERMINATE` | Protocol success with invalid/stale task authority producing no authoritative success. | No local task/protocol harness. | Runtime trace absent. |
| `B08-protocol-fails-task-records-failure` | `INDETERMINATE` | Protocol failure reflected distinctly in task-visible outcome. | No local task/protocol harness. | Runtime trace absent. |
| `B09-holder-initiator-distinct` | `INDETERMINATE` | Holder/initiator distinction trace and audit note. | No local task/protocol harness. | Runtime trace absent. |

### Scope C — VTA-held-key protocol signatures

| Case | Current disposition | Missing runtime evidence | Local execution state | Closure blocker |
|---|---|---|---|---|
| `C01-valid-sign-jws` | `INDETERMINATE` | Valid `sign-jws` request/response trace and signing-input digest. | No local custodian/runtime harness. | Runtime trace absent; upstream evidence request #752 pending. |
| `C02-sign-jws-prohibited-header` | `INDETERMINATE` | Rejection trace for prohibited JWS header members. | No local custodian/runtime harness. | Negative runtime trace absent; upstream evidence request #752 pending. |
| `C04-sign-jws-wrong-purpose` | `INDETERMINATE` | Wrong-purpose/audience rejection trace or non-applicability boundary. | No local custodian/runtime harness. | Runtime trace or boundary statement absent; upstream evidence request #752 pending. |
| `C05-valid-sign-csr` | `INDETERMINATE` | Valid `sign-csr` request/response trace and CSR digest/redacted PEM. | No local custodian/runtime harness. | Runtime trace absent; upstream evidence request #752 pending. |
| `C06-sign-csr-wrong-subject` | `INDETERMINATE` | Wrong-subject rejection trace or authority-boundary statement. | No local custodian/runtime harness. | Runtime trace or boundary statement absent; upstream evidence request #752 pending. |
| `C07-sign-csr-arbitrary-extension` | `INDETERMINATE` | Arbitrary-extension rejection trace. | No local custodian/runtime harness. | Negative runtime trace absent; upstream evidence request #752 pending. |
| `C08-generic-sign-substitution` | `INDETERMINATE` | Generic-sign substitution rejection or verification-failure trace. | No local custodian/runtime harness. | Runtime trace absent; upstream evidence request #752 pending. |

## Privacy and retained-evidence dependency

All scopes require retained-evidence inventory before final closure. The retained-evidence inventory should identify:

- task records;
- trigger-link records;
- session or exchange identifiers;
- verifier/client identifiers;
- wallet, holder, presenter or credential-subject identifiers;
- audit events;
- signed artifact digests;
- rejected request records;
- deliberately non-retained sensitive material.

DPIP/privacy disposition remains unresolved until those inventories are available.

## Closure posture for #994

#994 should remain open.

Closure is not appropriate merely because Scopes A, B and C have been documented downstream. Closure requires one of the following per case:

1. runtime evidence supplied and dispositioned as `PASS`, `FAIL` or `INDETERMINATE` with rationale;
2. explicit transfer to a more specific runtime owner with durable tracking;
3. durable blocked status with reason and no current evidence path;
4. retained-evidence inventory and DPIP/privacy disposition completed where applicable.

## Recommended next work

1. Monitor `trustoverip/dtgwg-trust-tasks-tf#752` for Scope C runtime evidence or owner clarification.
2. Decide whether to prepare downstream-only evidence-request drafts for Scope A and Scope B without posting upstream.
3. Add a final #994 status comment pointing to this matrix after this file merges.
4. Keep #994 open as the durable consolidated runtime-evidence issue.
