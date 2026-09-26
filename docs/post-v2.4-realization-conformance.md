---
layout: default
title: Post-v2.4 realization conformance
parent: Operate assurance
nav_order: 9
---
# Post-v2.4 realization conformance

This record reconciles the first post-v2.4 realization-conformance tranche under programme #800.

The purpose is to distinguish **adopted/current semantics** from **runtime realization evidence**. A normative change, generated binding, design note or passing library test can narrow an assurance obligation, but none of those automatically establish that a target implementation preserves the required semantics at the consequential boundary.

## Current programme matrix

| Owner | Current normative / design state | Current realization evidence | Disposition | Reassessment trigger |
|---|---|---|---|---|
| #799 — operation-bound step-up | Trust Tasks sessionless operation-bound semantics adopted; OpenVTC design documented | OpenVTC #1718/#1719 now provide target-native signed `acl/grant` and `acl/change-role` tests | **EVIDENCE_REQUIRED, narrowed** | explicit expiry-at-redemption, authority-change-between-approval-and-redemption, and remaining second-party-consent/widening evidence |
| #609 — live VAC status/policy freshness | action-time authority model exists; lifecycle machinery exists for adjacent artifact classes | no current evidence of live VAC `credentialStatus`/revocation + required policy freshness at the action boundary | **EVIDENCE_REQUIRED / WAITING_EXTERNAL** | real target status surface or explicit normative reassignment to another authoritative component with freshness evidence |
| #691 — declared Trust Task error semantics | trust-tasks-tf #575 merged; canonical generated error-code/retryability vocabulary exists | RAHP semantic-loss tests exist; OpenVTC #1600 still records incomplete target response-boundary coverage | **EVIDENCE_REQUIRED / WAITING_EXTERNAL** | target-native census/tests prove assurance-relevant code + retryability fidelity |
| #797 — forge projection provenance | forge/bridge implementation semantics exist; DID-log proposal withdrawn; normative VTI alignment incomplete | strong source-pinned bridge/projection implementation evidence | **WAITING_EXTERNAL** | stable VTI normative alignment; reassess current OpenVTC #1745 separation-of-duties/break-glass semantics when settled |
| #690 — task citation/outcome/correlation | Credential #56 and VTI #33 merged; Trust Tasks completion non-inference semantics adopted | dtg-credentials #31/#32 adds `taskDigestMultibase`; complete target path and committed-citation privacy construction remain incomplete | **WAITING_EXTERNAL** | Credential #58 / ZKP construction materially settles or a target exposes initiating-document + digest + outcome-evidence runtime path |

## Assurance rules applied

### Normative convergence is not realization conformance

A merged specification PR changes what a conforming implementation is expected to do. It does not prove that any target currently does it.

### Library capability is not end-to-end target evidence

A helper crate can expose the right data member or digest algorithm while a service, route, persistence layer or relying component still fails to preserve the semantics. RAHP therefore keeps the target boundary explicit.

### Target-native tests can materially narrow a residual

The operation-bound step-up residual demonstrates the intended progression. Design evidence under #1713 was insufficient. Target-native OpenVTC tests under #1718/#1719 materially strengthened the evidence and removed broad uncertainty, but the durable owner remains open because its exact closure contract still includes expiry, authority-change and second-party-consent cases.

### Waiting-external is a valid assurance state

When the required implementation surface or stable normative boundary does not exist, the correct result is not to manufacture a fixture that stands in for it. The durable owner records the trigger for a fresh source-pinned epoch.

## Programme consequence

The first G1 sweep does **not** identify missing generic RAHP controller machinery. The remaining work is predominantly target/runtime or upstream normative evidence.

Therefore the next RAHP engineering work should focus on:

1. observing and scheduling reassessment when the recorded triggers fire;
2. keeping source pins and current-state comments fresh;
3. producing executable evidence only where the target surface is real;
4. avoiding duplicate issue creation for propositions that already have durable owners.

## Release consequence

This realization sweep by itself does not establish a new RAHP stable capability boundary. It is evidence that the post-v2.4 operating model is working: residuals become narrower as evidence improves, without converting partial progress into PASS.
