# Scope B evidence records — VTI foreign-protocol binding

Issue: #994  
Scope: B — VTI foreign-protocol binding  
Source finding: `1c2869a18869681e741b`  
Upstream source/spec PR: `trustoverip/dtgwg-vti-spec#60`  
Upstream merge commit: `dc1ec07d42ec5c0054037795c06dbead608fbc5b`

## Purpose

This file starts Scope B evidence collection for the VTI foreign-protocol binding residual transferred into #994.

It does **not** mark any runtime case PASS. The currently available upstream material is source/spec evidence from `trustoverip/dtgwg-vti-spec#60`, not a downstream runtime trace. These records therefore distinguish:

- source/spec constraints that are already evidenced by the upstream PR description; and
- runtime traces still required before final PASS / FAIL / INDETERMINATE disposition under #994.

No upstream issue or PR comment is created by this downstream record.

## Source/spec evidence available

The upstream VTI PR defines a foreign-protocol interface as an endpoint whose wire format is fixed by an external protocol for a counterparty that cannot produce an operation document.

The PR records the following source/spec constraints:

- `VTI-OPS-095`: defines the foreign-protocol interface and states that an interface meeting `VTI-OPS-096` through `VTI-OPS-099` is not a parallel interface under `VTI-OPS-002`.
- `VTI-OPS-096`: the interface serves an exchange a catalogue task began, begins no operation of its own, and is reachable only within that exchange.
- `VTI-OPS-097`: the interface confers no authority; material arriving over the protocol is evidence, and the decision is taken under the beginning task's authority.
- `VTI-OPS-098`: the exchange is single-use, expires, and the interface meets its protocol's security requirements in full.
- `VTI-OPS-099`: the outcome is readable through a task, and each interface is documented with the task it serves.
- `VTI-CRD-024`: a presentation arriving this way names the verifier identifier in that protocol as its audience and commits to the beginning task's challenge.
- `VTI-CRD-025`: the holder of a presented credential and the party who began the exchange are kept apart unless the protocol binds them.

The upstream PR also cites OpenVTC implementation/design context at `OpenVTC/verifiable-trust-infrastructure#1988` and `docs/05-design-notes/oid4vp-wallet-verifier.md` in the OpenVTC repository.

## Initial case records

| Case | Case purpose | Source/spec evidence status | Runtime evidence status | Current disposition |
|---|---|---|---|---|
| `B01-valid-task-bound-foreign-protocol` | Foreign-protocol response is bound to an exchange begun by a task and accepted under original task authority. | Supported by `VTI-OPS-095` through `VTI-OPS-099` and `VTI-CRD-024`. | No downstream runtime trace yet. | `INDETERMINATE` pending task-bound runtime trace. |
| `B02-direct-endpoint-no-task` | Direct foreign-protocol endpoint invocation without task context fails. | Supported directionally by `VTI-OPS-096`. | No rejection trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `B03-reuse-after-completion` | Reuse after successful completion is rejected. | Supported directionally by `VTI-OPS-098`. | No first-use/reuse trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `B04-expired-exchange` | Expired exchange cannot produce authoritative task success. | Supported directionally by `VTI-OPS-098`. | No expiry trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `B05-wrong-audience` | Wrong verifier/client identifier audience is rejected. | Supported by `VTI-CRD-024`. | No presentation rejection trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `B06-wrong-challenge` | Presentation not committed to the beginning task challenge is rejected. | Supported by `VTI-CRD-024`. | No challenge mismatch trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `B07-task-authority-invalid` | Foreign-protocol success does not create authority when beginning task authority is invalid or stale. | Supported directionally by `VTI-OPS-097`. | No invalid-authority runtime trace yet. | `INDETERMINATE`; likely needs implementation fixture. |
| `B08-protocol-fails-task-records-failure` | Task records decline, timeout or protocol failure distinctly. | Supported directionally by `VTI-OPS-099`. | No failed-protocol task outcome trace yet. | `INDETERMINATE` pending runtime trace. |
| `B09-holder-initiator-distinct` | Holder, presenter, credential subject and initiating party are not silently conflated unless protocol binding proves equivalence. | Supported by `VTI-CRD-025`. | No holder/initiator distinction trace yet. | `INDETERMINATE` pending runtime trace. |

## Downstream local capability assessment

A downstream search of `rahp-toolkit` did not identify a runnable foreign-protocol runtime harness, OID4VP endpoint fixture, task-bound exchange fixture, or negative-test runner for the Scope B cases.

That means `rahp-toolkit` can currently record source/spec evidence and case requirements, but it cannot honestly mark the Scope B cases PASS or FAIL from local runtime execution.

## Runtime trace requirements

A runtime trace for Scope B should include:

- source repository and commit/tag under test;
- task record initiating the foreign-protocol exchange;
- endpoint/session identifier or equivalent redacted reference;
- challenge and audience/client identifier binding;
- redacted protocol transcript or digest;
- task-visible outcome;
- rejection or non-positive outcome for negative cases;
- retained-evidence / audit note;
- holder / initiator / subject distinction note where relevant;
- privacy / DPIP note.

## Evidence records required next

Suggested paths for future trace records:

```text
reproductions/dtg-runtime-evidence/scope-b/B01-valid-task-bound-foreign-protocol.yaml
reproductions/dtg-runtime-evidence/scope-b/B02-direct-endpoint-no-task.yaml
reproductions/dtg-runtime-evidence/scope-b/B03-reuse-after-completion.yaml
reproductions/dtg-runtime-evidence/scope-b/B04-expired-exchange.yaml
reproductions/dtg-runtime-evidence/scope-b/B05-wrong-audience.yaml
reproductions/dtg-runtime-evidence/scope-b/B06-wrong-challenge.yaml
reproductions/dtg-runtime-evidence/scope-b/B07-task-authority-invalid.yaml
reproductions/dtg-runtime-evidence/scope-b/B08-protocol-fails-task-records-failure.yaml
reproductions/dtg-runtime-evidence/scope-b/B09-holder-initiator-distinct.yaml
```

## Boundary after this pass

This pass starts Scope B evidence records but does not close Scope B. The next substantive step is one of:

1. produce runnable fixtures and traces for the nine Scope B cases;
2. record a downstream-only evidence request if a precise runtime owner is identified;
3. transfer each case to a more specific durable owner with a posted transfer matrix; or
4. mark a case blocked with a precise reason if the relevant implementation is not accessible.

Until one of those paths happens, `#994` remains open.
