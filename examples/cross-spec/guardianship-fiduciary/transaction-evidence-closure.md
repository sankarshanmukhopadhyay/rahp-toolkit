# Constrained-authority transaction evidence closures

This document records the construction pass that follows the source-pinned evidence review for the guardianship/fiduciary RAHP case. It tests three concrete decision flows against the pinned DTG Credential, Trust Task and companion ZKP material before treating any residual as a specification gap.

The detailed machine-readable cases are:

- [`transactions/routine-act.yaml`](./transactions/routine-act.yaml)
- [`transactions/threshold-coapproval.yaml`](./transactions/threshold-coapproval.yaml)
- [`transactions/suspension-restoration.yaml`](./transactions/suspension-restoration.yaml)

## Construction rule

Each case is evaluated as:

`scenario -> required predicates -> existing DTG artifact -> authoritative evidence source -> binding/proof -> verifier decision -> residual`

A residual is classified as one of:

- **existing primitive sufficient**;
- **profile clarification required**;
- **genuine missing primitive**;
- **governance-only**; or
- **unresolved**.

The test deliberately prefers reuse over invention. A missing guardianship-specific label is not a missing primitive if an existing DTG mechanism can express the required proposition under a profile-defined vocabulary.

## Case A — routine bounded-authority act

**Decision:** may a currently appointed representative perform an ordinary in-scope transaction?

The construction reuses Credential validity and issuer-authorization checks; `taskContext` where exchange binding is needed; Trust Task proof/audience/correlation machinery; and the ACL grant pattern for scoped, expiring authority with authoritative post-state.

### Result

**Existing primitives are sufficient for the mechanics.** The remaining work is primarily a constrained-authority profile defining:

- which authoritative source establishes appointment/current status;
- how appointment scope maps to decision-relevant action scope;
- how transaction-time current state is evaluated; and
- what minimal disclosure/non-inference rules apply.

No new generic Credential or Trust Task primitive is demonstrated by this case.

A governance rule remains necessary to prevent a valid representative proof from being interpreted as evidence that the principal lacks capacity or retained authority. Fiduciary propriety also remains outside cryptographic authorization.

## Case B — threshold/co-approval act

**Decision:** may a representative perform an act that requires an additional authorized approval?

The construction found more reusable machinery than the initial hypothesis assumed. Trust Tasks already demonstrates:

- authorized-approver registration (`consent/approver-set`);
- signed approval decisions (`consent/decision`);
- challenge echo/matching and single-use consumption;
- expiry and scope;
- issuer/recipient proof binding; and
- task-specific authorization checks.

### Result

The claim that DTG lacks approval machinery is **weakened further**.

The residual is not a generic approval primitive. It is a reusable constrained-authority composition profile defining:

- a canonical decision object/version to which every approval commits;
- threshold semantics such as joint, sequential or N-of-M approval;
- authoritative and fresh approver-set state; and
- a privacy-preserving proof/input contract that can establish threshold satisfaction without exposing the full representative graph.

The reviewed sources do not demonstrate that generic composition, but they provide strong building blocks for it.

## Case C — suspension/restoration act

**Decision:** what authority state controls when earlier credentials/evidence exist but authority has subsequently been suspended, narrowed, superseded or restored?

The construction reuses Credential validity/revocation checks and Trust Task ACL revoke/grant mechanics. `acl/revoke` supports full removal and scope reduction; `acl/grant` provides a recoverable re-grant pattern and authoritative maintainer post-state.

### Result

Existing lifecycle primitives are substantial. The remaining closure problem is **state semantics and precedence**, not revocation mechanics.

A constrained-authority profile still needs to define:

- suspension, supersession, restoration and replacement semantics;
- effective-time and precedence rules across conflicting historical artifacts;
- how a verifier discovers authoritative transaction-time state;
- when a later grant is restoration versus a new appointment; and
- how retained/restored principal agency is represented without stale representative evidence dominating the decision.

The case therefore refines the original stale-authority finding into a cross-artifact lifecycle/profile gap.

## Cross-case result

| Question | Case A | Case B | Case C |
| --- | --- | --- | --- |
| Proof/attribution mechanics | Sufficient | Sufficient | Sufficient |
| Scope/expiry mechanics | Sufficient | Sufficient building blocks | Sufficient building blocks |
| Replay/context binding | Sufficient with profile-defined decision fields | Strong existing challenge/task patterns | Must include current-state freshness |
| Authoritative-source semantics | Profile required | Profile required | Profile required |
| Threshold/co-approval composition | Not applicable | Profile unresolved | Not applicable |
| Lifecycle precedence | Basic checks sufficient | Must be freshness-bound | Profile unresolved |
| Privacy-preserving composition | Partially demonstrated | Unresolved upstream interface | Unresolved status/freshness interface |
| Fiduciary propriety / retained agency | Governance-only | Governance-only | Governance-first |
| New generic base primitive demonstrated | No | No | No |

## What survives the construction pass

The evidence no longer supports a broad statement that DTG lacks guardianship/fiduciary support. Nor does it support adding a monolithic guardianship credential or a new generic approval/revocation primitive.

Four narrower residuals survive:

1. **Constrained-authority composition profile.** Appointment, current scope, transaction permission and authoritative-source semantics need a common cross-spec contract.
2. **Threshold/co-approval composition.** Existing approval patterns need a reusable decision-binding and threshold-policy profile if constrained-authority use cases are to interoperate.
3. **Lifecycle precedence and restoration.** Existing grant/revoke/validity primitives need profile semantics for suspension, supersession, effective time and restoration across artifacts.
4. **Privacy/governance boundary.** Private proof inputs for authority/co-approval/current-state predicates remain to be demonstrated upstream, while incapacity non-inference, retained agency, conflicts and fiduciary propriety remain governance/assurance concerns.

## Negative-test result

The original adversarial set was also narrowed:

- replay of an approval is substantially controlled by challenge/task-context/audience mechanisms when profiles bind all decision-critical fields;
- low-entropy deterministic digests remain a construction guardrail, not a defect in the current VWC integrity digest;
- stale authority remains material only where current-state/lifecycle evaluation is omitted or precedence is undefined;
- co-approval privacy remains open at the composed proof-input boundary;
- emergency authority and cross-jurisdiction equivalence remain governance/profile questions with insufficient evidence for a concrete base-spec defect;
- valid mathematics or authenticated task evidence must still not be promoted into proof of fiduciary propriety.

## Post-construction RAHP retest

After the three constructions, RAHP is run again as a **retest**, not as a fresh independent assessment. The retest asks which original findings survive, whether their severity/ownership changes, and whether multiple candidate findings collapse into fewer dispositionable residuals.

The machine-readable result is [`post-construction-rahp.yaml`](./post-construction-rahp.yaml). The formal `pressure-test.yaml` is updated only with residuals that now satisfy the finding/evidence contract.

No upstream DTG issue is created by this construction pass. Maintainer review in [Discussion #51](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/51) remains the next disposition gate.
