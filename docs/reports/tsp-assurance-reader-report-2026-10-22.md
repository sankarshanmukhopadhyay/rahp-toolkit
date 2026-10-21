---
layout: default
title: "TSP assurance: reader's guide and risk tables"
parent: Reference
---
# Trust Spanning Protocol: assurance review for implementers and decision-makers

**Review status:** preliminary, documentary, **not a completed full-stack assessment**.  
**Tracking:** [#1103](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1103) · [Technical evidence baseline](tsp-full-assurance-evidence-baseline-2026-10-22.md)  
**Source:** [TSP editor's publication](https://trustoverip.github.io/tswg-tsp-specification/), inspected as Experimental Implementor's Draft Rev 2; its equivalence to the [intake source commit](https://github.com/trustoverip/tswg-tsp-specification/commit/ccda6b33159d860f05c328eb436dabe83548b705) is not established. A previously discussed Rev 3 must be verified separately.

## Executive interpretation

TSP provides protocol mechanisms for authenticated interactions between verifiable identifiers, with optional confidentiality and routing arrangements. It does **not**, by itself, establish the authority of a person or agent to perform a consequential action, certify a VID's social or legal meaning, guarantee anonymity, or supply a deployment's redress mechanism. These are **boundaries for assurance**, not findings of confirmed vulnerabilities.

The review examines four lenses separately. The current outcome is **INDETERMINATE**, because required implementation, failure-injection, authorization, and human-context evidence has not been executed or supplied. No overall GREEN/AMBER/RED terminal judgment is issued.

## 1. What the protocol does and does not establish

| Question | What the reviewed material supports | What remains outside that observation | Responsible assurance surface |
|---|---|---|---|
| Can a message be authenticated? | The specification describes sender authentication using VID/key material and message signatures. | Whether the verified key corresponds to the *intended* real-world counterparty or role. | VID method + onboarding/binding policy |
| Is a relationship the same as permission? | Relationships provide communication context and can be directional/asynchronous. | Application authorization, delegation scope, expiry, purpose and use-time policy. | Application / PDP / governance |
| Is message content confidential? | Confidentiality is supported in applicable message modes. | Mandatory encryption in every mode, endpoint compromise, access to metadata. | Protocol profile + endpoints |
| Is communication private? | Routing and nesting can support metadata protection. | Anonymity against a defined network or infrastructure observer. | Threat model + deployment traffic tests |
| Are intermediaries trustworthy? | The architecture anticipates intermediaries that need not be trusted. | Guaranteed delivery, absence of suppression, metadata invisibility or availability. | Routing composition + operators |
| Does cryptographic validity prove legitimacy? | Cryptographic verification can establish bounded technical properties. | Recognition, authorization, accountable decision-making and remedy. | Trust framework + consuming service |

## 2. Risk, harm and responsibility

| Priority for examination | Scenario | Who could be harmed | Preventive control to verify | Detection and recovery evidence | Current status |
|---|---|---|---|---|---|
| High concern, not measured severity | A valid VID is substituted for an expected party. | Correspondents, relying organizations | Explicit expected-counterparty binding | Mismatch logs; rejected introduction fixtures | Not tested |
| High concern, not measured severity | A valid signed message is interpreted as delegated authority. | Principal, customer, affected third party | Separate use-time policy/delegation check | Denied-action trace; contestation | Not tested |
| High concern, not measured severity | Revoked/rotated key remains accepted. | Account holders, correspondents | Fresh authoritative key state and recovery | Revocation lag measurements | Not tested |
| Context dependent | Traffic metadata permits relationship mapping. | Participants and associates | Defined privacy profile and retention controls | Multi-vantage traffic study | Not tested |
| Context dependent | Resolver outage excludes legitimate participants. | Service users | Bounded retries, alternatives and safe failure | Recovery journey, outage metrics | Not tested |
| Context dependent | Disputed automated transaction lacks redress. | Subject of decision | Audit provenance, appeal and reversal | Actual redress exercise | Not tested |

*“High concern” here is a prioritization for testing, not a quantitative risk score or verified severity determination.*

## 3. Four-lens examination

| Lens | Central question | Example test | What a passing test would establish | What it would **not** establish |
|---|---|---|---|---|
| RAHP | Whose interests are affected if a trust proposition fails? | Model an unauthorized automated instruction and trace consequences. | The specific harm/control proposition has supported evidence. | Universal safety of TSP deployments. |
| Security | Can an adversary exploit protocol, parser, key or routing behavior? | Replay, substitution, malformed CESR, key rotation. | Resistance under the tested configuration and threat assumptions. | All implementations conform. |
| Combination | Do individually acceptable components remain safe together? | Valid VID + stale delegation + TSP relationship. | Correct authority boundaries in the tested composed flow. | A component PASS transfers to another deployment. |
| DRARM | Can distributed failure multiply load, delay, duplicate effects or lost work? | Resolver outage + layered retries + intermediary recovery. | Bounded recovery for the measured failure conditions. | Fleet-scale resilience without fleet-scale evidence. |

## 4. DRARM: catalogue-grounded mapping

The [DRARM catalogue](../../method/resilience/catalogue.yaml) defines six principles and five assurance depths. This table maps *hypotheses* to existing catalogue rules; it does not assert a detector match or an executed assessment.

| TSP scenario | Relevant catalogue risk | Control evidence needed | Minimum plausible evidence depth for an implementation claim |
|---|---|---|---|
| Resolver outage with client retries | RLA-001 Retry storm; RLA-010 Timeout amplification | Retry policy, deadlines, backoff/jitter, terminal-failure test | DR-A3 for automated tests; DR-A4 for measured induced outage |
| Application, transport and intermediary all retry | RLA-004 Retry multiplication | Single retry-owner map, correlation/idempotency, failure-domain test | DR-A3; DR-A4 for measured multiplication |
| Intermediary restarts and clients reconnect together | RLA-002 Reconnect herd | Reconnect jitter/cap and fleet recovery test | DR-A4; DR-A5 for bounded fleet-scale evidence |
| Backlogged routed delivery overflows | RLA-005 Unbounded queue growth; RLA-006 Destructive overflow | Queue capacity, overload and acknowledgement-order tests | DR-A4 for induced overload |
| Poison message is repeatedly redelivered | RLA-008 Poison-message redelivery loop | Attempt accounting, quarantine and operator evidence | DR-A3; DR-A4 for induced redelivery |
| A slow message blocks healthy work | RLA-009 Head-of-line blocking | Failure isolation, bounded processing time and HOL test | DR-A3; DR-A4 for induced stall |

**Depth legend:** DR-A1 documented control; DR-A2 normative/implementation evidence; DR-A3 automated conformance test; DR-A4 measured induced failure/load; DR-A5 fleet-scale/adversarial amplification demonstration. The table proposes *evidence targets*, not achieved levels.

## 5. Decisions and evidence gaps

| Decision or question | Evidence needed before closure | Interim treatment |
|---|---|---|
| Which specification revision is being assured? | Published artifact, source commit and rendered equivalence | Keep source discrepancy open |
| Can a TSP message authorize an action? | Application policy, delegation, use-time checks | No authorization inference from authentication |
| Does a routed composition preserve security and privacy? | End-to-end traces, intermediary threat model, metadata tests | No inherited composition PASS |
| Is the system resilient to distributed failure? | Actual DRARM run and induced-failure measurements | DRARM INDETERMINATE |
| Can a harmed party recover or contest? | Concrete deployment and governance process | Human-harms outcome INDETERMINATE |
| Are findings transferable across implementations? | Conformance, version, environment and configuration evidence | No generalization beyond tested scope |

## 6. How to use this review

**Specification editors** can use the questions to clarify obligations and boundaries, after checking the exact authoritative revision. **Implementers** can turn the negative scenarios into test cases and collect runtime evidence. **Operators and governance teams** should examine user recovery, authorization, privacy and redress in a named deployment. **Assurance reviewers** should use the technical baseline and the controller's per-lens disposition ledger rather than treating this explanatory report as a certification.

**Next execution steps:** reconcile the source; instantiate canonical RAHP/security/combined review records; run DRARM against a pinned source checkout with an applicable profile; capture machine-readable evidence; conduct applicable specialist referrals; reconcile the four lenses; then issue validated final technical and reader reports. The subsequent DTFC + RAHP synthesis is a separate follow-on exercise.
