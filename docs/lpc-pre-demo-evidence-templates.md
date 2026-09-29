# LPC pre-demo RAHP evidence templates

Status: **candidate / scope-unfrozen**  
Campaign owner: RAHP #851  
Purpose: reusable evidence contracts for the DTG/VTC LPC end-to-end assurance run.

These templates are not evidence that a proposition is currently satisfied. They become runnable assessment cases only after the authoritative LPC demo path binds the placeholders to exact actors, Trust Task/document types, transports, configuration and source revisions.

## 1. Instantiation header

Every selected test case MUST record:

```yaml
lpc_case:
  campaign: rahp-851
  case_id: LPC-<family>-<nn>
  historical_anchor: <RAHP issue(s)>
  applicability: IN-SCOPE-RETEST | IN-SCOPE-KNOWN-RESIDUAL
  proposition: <falsifiable claim>
  source_pins:
    - repository: <owner/repo>
      revision: <immutable SHA/tag>
  configuration:
    profile: <demo profile>
    feature_flags: []
    transport: <DIDComm|TSP|HTTPS|other>
  actors:
    initiator: <actor>
    responder: <actor>
    authority_source: <component/artifact>
  task:
    type: <exact Trust Task/document type>
    instance: <runtime id if safe to retain>
  observed_at: <timestamp>
```

Do not execute an unbound placeholder as though it were the LPC configuration.

## 2. Common verdict model

Each case records two distinct results.

**Test result**
- `PASS`: observed behavior matches the expected assertion.
- `FAIL`: observed behavior contradicts the expected assertion.
- `NOT_RUN`: case could not be executed.

**Assurance disposition**
- `PASS`: required positive and negative evidence is attributable to the pinned target and supports the proposition.
- `FAIL`: attributable evidence demonstrates the prohibited behavior/material failure.
- `INDETERMINATE`: required evidence is missing, ambiguous, non-attributable, or the environment cannot establish the proposition.
- `KNOWN_RESIDUAL`: the path exercises a proposition already explicitly unresolved; record current observations without laundering it into PASS.
- `N/A`: scope reconciliation establishes that the demo path does not exercise the proposition.

A negative test **passes when the prohibited action is refused without consequential side effect**.

## 3. Required evidence envelope

For every executed case retain, where applicable:

- immutable source/configuration pins;
- input/task/proof identity or privacy-preserving digest;
- actor/issuer/controller and verification relationship used;
- challenge, issued-at, expiry/acceptance-window and relevant clock basis;
- authority/status/policy state consulted at the decision boundary;
- transport receipt/delivery/acceptance observations;
- decision/result/error classification;
- before/after authoritative state or side-effect observation;
- replay/idempotency/audit record;
- logs/traces sufficient to attribute the observation to the pinned implementation.

Sanitize secrets and unnecessary personal data. A log from a fixture or different implementation is not target evidence.

---

# Family A — authority at effect time

Historical anchors: #609, #781, #780.

## Proposition

A consequential task produces effect only when the actor's authority is valid **at the action boundary**, including required current credential/status/policy state. Valid proof, authentication, holder binding, a valid chain, or `validUntil` alone is not sufficient.

## Positive control A1

Execute the selected consequential task with current, in-scope authority and all required live state available.

Expected:
- current authority is evaluated at/near effect time;
- requested action/scope matches the authority;
- one authoritative effect occurs;
- evidence identifies the state used for the decision.

## Negative cases

**A2 — revoked authority:** revoke the relevant authority/status before execution; resend otherwise-valid task/proof.  
Expected: refusal/no effect.

**A3 — stale status/policy:** present otherwise-valid evidence while the required current state is stale beyond its accepted freshness contract.  
Expected: refusal or explicit INDETERMINATE according to governing policy; never implicit permission.

**A4 — lookup failure:** make required live status/policy unavailable.  
Expected: fail closed or explicit governed INDETERMINATE; no unauthorized effect.

**A5 — scope widening:** use valid authority for action/scope X to request X+ or Y.  
Expected: refusal/no widened effect.

## Disposition

PASS requires attributable evidence for the positive control and every negative case required by the instantiated authority model. If live revocation/policy freshness remains unimplemented or unobservable, classify `KNOWN_RESIDUAL` against #609 rather than PASS.

---

# Family B — proof/authentication is not authorization

Historical anchors: #767, #780, #781.

## Proposition

Possession of a bearer/session credential, valid signature, ZK proof, liveness/personhood proof or successful authentication cannot substitute for the separate authorization required by the consequential Trust Task.

## Positive control B1

Execute with both valid producer proof/authentication **and** valid task authority.

Expected: task proceeds subject to all other gates.

## Negative cases

**B2 — proof without authority:** retain valid proof/authentication but remove task authority.  
Expected: refusal/no effect.

**B3 — authority without required producer proof:** retain authority but omit the proof required by the task.  
Expected: refusal/no effect.

**B4 — bearer substitution:** where a proof-REQUIRED task has/has had a bearer path, attempt the consequential operation using bearer/session authentication without the required signed operation document.  
Expected: bearer authentication is not credited as equivalent proof.

## Disposition

Any successful consequential effect in B2–B4 is FAIL for this proposition. Transitional bearer routes must be reported as residual/divergence rather than hidden by a successful authenticated request.

---

# Family C — exact operation binding and step-up

Historical anchors: #795, #799, #837.

## Proposition

An operation-bound approval/step-up authorizes exactly one canonical operation and cannot be rebound, replayed, or redeemed after its freshness/current-authority basis ceases to hold.

## Positive control C1

Create the approval for exact task type + canonical payload + actor; redeem that operation once.

Expected: one effect, attributable to the bounded approval.

## Negative cases

**C2 — exact replay:** redeem the identical approval/operation again.  
Expected: refusal/no second effect.

**C3 — payload/target/role/scope substitution:** modify one consequential field while reusing the approval.  
Expected: refusal/no effect.

**C4 — cross-operation reuse:** reuse approval for another task type.  
Expected: refusal/no effect.

**C5 — expired approval:** advance/inject time beyond the configured approval TTL before redemption.  
Expected: refusal/re-challenge/no effect.

**C6 — intervening authority change:** approve, then revoke/demote/expire the actor before redemption.  
Expected: current-authority check refuses/no effect.

**C7 — delegated signer:** where supported, let a console/delegated signing key redeem a human-created approval, then attempt to create the human approval using that delegated key.  
Expected: redemption only where authorized; delegated key cannot manufacture human approval.

## Disposition

C5 and C6 are known historical evidence gaps owned by #837. If the LPC path exercises step-up and target-native evidence for them still does not exist, disposition is `KNOWN_RESIDUAL`, not PASS.

---

# Family D — proofPurpose / key-role binding

Historical anchor: #820.

## Proposition

Cryptographic validity is insufficient unless the verification method is authorized under the declared/required verification relationship for the exact document role.

## Positive control D1

Sign a selected operational or attestation document with a key authorized for its required proofPurpose.

Expected: proof verifies subject to other gates.

## Negative cases

**D2 — wrong relationship:** valid signature by issuer-controlled key present in the DID document but not authorized for required proofPurpose.  
Expected: refusal.

**D3 — purpose substitution:** alter/claim a different proofPurpose without changing the underlying authorization relationship.  
Expected: refusal.

**D4 — wrong controller/DID:** use a cryptographically valid key controlled by a different identity.  
Expected: refusal.

**D5 — stale/rotated/deactivated key:** use a key no longer authorized under current DID state.  
Expected: refusal according to current resolver/freshness semantics.

## Disposition

PASS requires producer and consumer observations. Do not infer application authorization from D-family PASS; this family proves only the verification-relationship boundary.

---

# Family E — freshness, replay, acceptance and idempotency

Historical anchors: #767, #833, #836.

## Proposition

Stale, duplicate, replayed or late artifacts cannot be converted into fresh execution/delivery evidence, and retries do not silently reset the original freshness semantics.

## Positive control E1

Deliver/execute a fresh task inside all applicable issue-time, challenge and recipient acceptance windows.

Expected: normal acceptance and at-most-once authoritative effect.

## Negative cases

**E2 — stale issuedAt/challenge:** exceed task/proof freshness.  
Expected: refusal/no effect.

**E3 — duplicate document:** replay same document/task identity.  
Expected: refusal/idempotent no-second-effect.

**E4 — late collection:** make a copy available only after the recipient's applicable acceptance window.  
Expected: late availability is not recorded as timely accepted delivery.

**E5 — retry/reissue:** retry after failure/late delivery.  
Expected: new document/proof identity where required while preserving operation idempotency; no double effect.

**E6 — window disagreement:** producer and recipient use conflicting/stale acceptance-window information.  
Expected: explicit refusal/non-authoritative/INDETERMINATE state according to contract, not false timely delivery.

## Disposition

If producer consumption of recipient-advertised windows remains absent and the demo depends on it, carry #836 as `KNOWN_RESIDUAL`.

---

# Family F — cross-component non-inference

Historical anchors: #780, #781.

## Proposition

Individually valid credential, ZKP and Trust Task artifacts do not compose into claims they do not establish: current authority, task completion, authoritative outcome, or permission for a different relying context.

## Positive control F1

Use the exact credential/proof/task combination defined by the demo profile, with explicit binding to intended action, audience/purpose and current authority.

Expected: each component result remains distinguishable and only the profile-authorized composite decision is made.

## Negative cases

**F2 — valid credential + invalid/currently unauthorized task authority.**  
Expected: no effect.

**F3 — valid proof from different purpose/audience/task context.**  
Expected: no semantic upgrade/reuse.

**F4 — valid credential interpreted as task-completion/outcome evidence.**  
Expected: consumer does not infer completion unless authoritative outcome evidence exists.

**F5 — lifecycle skew:** credential/proof remains valid while authority/policy/task state changes.  
Expected: current consequential decision follows the action-time state.

## Disposition

PASS requires explicit evidence of the composition decision boundary. Component unit-test success alone is insufficient.

---

# Family G — fail-closed consequential boundary

Historical anchors: #609, #767, #780, #781 and the Dogwood full-stack assessment lineage #225.

## Proposition

A required assurance dependency becoming absent, invalid or unavailable cannot silently become permission.

## Negative cases

Instantiate only dependencies actually required by the demo path:

- G1 missing required proof;
- G2 malformed proof/document;
- G3 unsupported task/profile/version;
- G4 verifier/resolver failure;
- G5 missing required authority/status/policy state;
- G6 ambiguous/conflicting state;
- G7 wrong recipient/audience/context.

Expected for every selected case: no unauthorized authoritative effect. If policy permits an explicit INDETERMINATE outcome, it must remain distinguishable from success.

## Disposition

Any permissive fallback that produces a consequential effect is FAIL unless the governing profile explicitly authorizes that fallback and the fallback itself is within the assessed proposition.

---

# Family H — outcome and evidence integrity

Historical anchors: #781, #833, #225/#228.

## Proposition

The system preserves distinctions between request, transport receipt, delivery, acceptance, execution, authoritative outcome and retained audit evidence, and can reconstruct the consequential decision from attributable evidence.

## Positive control H1

Run the normal demo path and collect the evidence chain from initiation to authoritative outcome.

Expected:
`request → proof/authentication → authority decision → acceptance → execution → authoritative state/outcome → audit/provenance`.

## Negative cases

**H2 — delivered but not accepted/executed.**  
Expected: no completion claim.

**H3 — accepted but side effect fails.**  
Expected: failure/partial state is visible; no false successful outcome.

**H4 — retry after partial failure.**  
Expected: causal/idempotency evidence distinguishes retry from duplicate success.

**H5 — evidence loss/ambiguity:** remove one required evidence source in a controlled test.  
Expected: assurance becomes INDETERMINATE where reconstruction is no longer possible; it does not remain PASS by assumption.

---

# Family P — privacy/correlation (conditional)

Historical anchors: #310, #338/#339 and, when enabled, #849.

Run this family only if the LPC path exercises or claims a privacy/unlinkability property.

## Proposition

The demonstrated composition does not create a prohibited stable join across contexts through relationship identifiers, credential identifiers, status/policy discovery, retained Trust Task evidence, verifier transcripts, device metadata or hidden-vetter representations.

## Method

Use at least two independently scoped observer/relying contexts A and B. Capture only the surfaces authorized by the evidence contract. Attempt the specified joins and retain provenance sufficient for DPIP assessment.

## Cases

- P1 relationship/binder comparison across A/B;
- P2 credential/presentation/request identifier comparison;
- P3 status/policy-discovery metadata comparison;
- P4 retained task/evidence identifier comparison;
- P5 verifier/challenge/purpose/context transcript comparison;
- P6 device/transport metadata comparison where in scope;
- P7 hidden-vetter masked/pseudonymous representation and retained-proof comparison where `vetting-pcs` is enabled.

## Disposition

RAHP records the attributable evidence package and routes the privacy conclusion through DPIP where required. Absence of an observed join in non-attributable fixtures is not privacy PASS.

---

# 4. LPC run matrix

Populate after scope freeze.

| Case | Applicability | Bound task/path | Source pin(s) | Expected | Test result | Assurance disposition | Evidence |
|---|---|---|---|---|---|---|---|
| A1–A5 | TBD | | | | NOT_RUN | | |
| B1–B4 | TBD | | | | NOT_RUN | | |
| C1–C7 | TBD | | | | NOT_RUN | | |
| D1–D5 | TBD | | | | NOT_RUN | | |
| E1–E6 | TBD | | | | NOT_RUN | | |
| F1–F5 | TBD | | | | NOT_RUN | | |
| G1–G7 | TBD | | | | NOT_RUN | | |
| H1–H5 | TBD | | | | NOT_RUN | | |
| P1–P7 | TBD | | | | NOT_RUN | | |

# 5. Final evidence rule

The LPC summary MUST be generated from the instantiated run matrix, not from historical issue states.

Historical findings supply propositions and regression expectations. Current pinned observations supply the LPC evidence.

The final record must therefore make it possible to say, precisely:

> For this exact demonstrated configuration, these consequential propositions were exercised; these negative cases were refused as expected; these known residuals remain; these evidence gaps remain; and no broader system-wide assurance claim is being made.
