# Current DTG/VTC portfolio assurance — 2026-09-07

- Assessment ID: `rahp:6b0ca36772a0184645c5`
- Terminal outcome: **INDETERMINATE**
- Reason: `portfolio-evidence-required`
- Portfolio posture: **AMBER**
- Clean-room workflow run: `34073261344`
- Assurance artifact digest: `sha256:9dfd8c91bdb28394d1455f678bf3fba9c0e3f392208af6fdd5e489d02bb29dca`

## Source pins

- `OpenVTC/verifiable-trust-infrastructure@3f21929ae5ce870f7c17726120d4aa1c1acbf13c`
- `trustoverip/dtgwg-cred-spec@37074bdcd861c51f3e5b7868ce700832b17b73ce`
- `trustoverip/dtgwg-trust-tasks-tf@84a4329a5f797dec9d240c83ab5d564c120dde8f`
- `OpenVTC/dtg-credentials@5cb04fab2d9272ee891b352a4886343ccc86b52b`
- `sankarshanmukhopadhyay/dtg-privacy-implementation-profile@49060d7ddbd83020568a2d83a694392e8b305819`
- `sankarshanmukhopadhyay/trust-protocol-interop-lab@52dbb22479a05554e7fa2745362b22c01f714095`

## Portfolio judgment

The portfolio proves bounded delegation/authority non-substitution and explicit spec/implementation separation, but current implementation conformance, actuation, replay and privacy evidence remain incomplete.

This result is deliberately not a certification claim. It is bounded to the immutable source epoch above and the evidence classes actually executed by the clean-room run. A successful workflow does not convert the AMBER/INDETERMINATE assurance result into GREEN.

## Proposition matrix

| ID | Judgment | Evidence | Implementation | Proposition |
|---|---|---|---|---|
| P01 | **PASS** | `verified` | `supported` | delegation cannot substitute for current authority and authority cannot substitute for representation |
| P02 | **INDETERMINATE** | `partially_verified` | `divergent` | current implementation materially conforms to adopted VDC semantics where it claims support |
| P03 | **INDETERMINATE** | `execution_evidence_pending` | `not-observable` | Trust Task authorization and invocation boundaries do not enlarge credential authority |
| P04 | **INDETERMINATE** | `execution_evidence_pending` | `not-observable` | replay/idempotency behavior does not create a second authorization path |
| P05 | **INDETERMINATE** | `partially_verified` | `not-observable` | presenter, subject and relationship bindings are preserved across the composed path |
| P06 | **INDETERMINATE** | `execution_evidence_pending` | `not-observable` | correlation scope and disclosure behavior do not create unnecessary durable cross-context joins |
| P07 | **INDETERMINATE** | `execution_evidence_pending` | `not-observable` | status/policy discovery and retained task evidence do not silently become correlation surfaces |
| P08 | **INDETERMINATE** | `partially_verified` | `not-observable` | capability, key possession and authority remain non-collapsible at consequential actuation boundaries |
| P09 | **INDETERMINATE** | `partially_verified` | `not-observable` | Trust Tasks and Credential Specification compose without introducing a semantic authority gap |
| P10 | **PASS** | `verified` | `supported` | the current OpenVTC realization is distinguishable from the normative baseline wherever it is divergent or incomplete |

## Rationale by proposition

### P01 — PASS

The pinned Interop Lab negative vectors execute both substitution directions and all expected deny/allow outcomes match.

### P02 — INDETERMINATE

The current dtg-credentials tree exposes a VDC constructor, but the assessor does not find the merged `delegation.scope` and `delegation.accepts` surfaces required by adopted #19. This is implementation-version divergence, not a defect in the specification.

### P03 — INDETERMINATE

Current normative and implementation sources are pinned, but this clean run has no current end-to-end actuation trace proving the credential-to-task authorization boundary.

### P04 — INDETERMINATE

Trust Tasks defines replay/idempotency semantics, but the portfolio run lacks a current cross-layer replay trace through the consuming OpenVTC path.

### P05 — INDETERMINATE

Existing source-compatible evidence is bounded to selected paths; this run does not establish preservation across all current credential/task compositions.

### P06 — INDETERMINATE

The pinned DPIP source continues to record evidence-required privacy disposition; successful bounded no-join observations are insufficient for portfolio-wide effective-correlation PASS.

### P07 — INDETERMINATE

Current-source A/B execution for status/policy discovery and retained Trust Task evidence is not supplied by this run.

### P08 — INDETERMINATE

Current Trust Tasks/VTI sources contain increasingly explicit capability separation, but source structure alone cannot prove consequential actuation non-collapsibility end to end.

### P09 — INDETERMINATE

Semantic non-substitution is proven, but current invocation, lifecycle, replay and implementation-conformance evidence is incomplete for the full composition.

### P10 — PASS

The clean run keeps normative Credential Spec and Trust Tasks pins separate from VTI and dtg-credentials realization pins and records implementation divergence instead of collapsing it into normative PASS.

## Executed evidence

- `ER-VDC-VAC-NON-SUBSTITUTION` — source-pinned Interop Lab semantic negative vectors; all expected allow/deny outcomes matched.

The bounded human-harm trace for this evidence is **PASS**: delegation cannot substitute for current authority, and authority cannot substitute for representation. The overall portfolio remains INDETERMINATE because this single verified proposition does not resolve the remaining composition and implementation questions.

## Residual owners / retest conditions

- **OpenVTC implementation / future retest — VDC merged #19 realization**: Current implementation exposes the adopted VDC scope, acceptance, lifecycle and binding contract.
- **Interop Lab — credential-to-Trust-Task actuation**: A current source-pinned consuming path can execute negative authority/invocation/replay vectors.
- **DPIP + Interop Lab — effective correlation**: Current A/B evidence exercises status/policy, retained task evidence and credential-carriage surfaces where implemented.

## Terminal inference

The current portfolio has bounded executable assurance but lacks enough current realization/runtime evidence to defend end-to-end GREEN, especially for merged VDC conformance, credential-to-task actuation/replay, and effective-correlation surfaces.

## Lineage

- New clean-room epoch; historical Dogwood evidence was not used as an inherited assurance conclusion.
- Existing RAHP/DPIP/Interop evidence is reusable only where source compatibility is demonstrated.
- Upstream `trustoverip/*` and `OpenVTC/*` repositories were read-only inputs; no upstream writes were made.
- Generated package contained `assurance-terminal-machine.json`, `assurance-terminal-human.md`, `clean-room-terminal.json`, `current-portfolio-matrix.json`, the evidence ledger, source resolution, and executed VDC/VAC evidence.

## Reproduction

Run the declared clean-room executor with `clean-room/current-portfolio-run-spec.json`. The run verifies every immutable checkout before assessment and fails closed when required evidence or assessor contracts are missing.
