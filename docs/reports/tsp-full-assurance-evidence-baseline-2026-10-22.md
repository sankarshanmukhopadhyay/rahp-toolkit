---
layout: default
title: "TSP full-stack assurance: technical evidence baseline"
parent: Reference
---
# Trust Spanning Protocol: four-lens RAHP assessment — evidence baseline

**Tracker:** [#1103](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1103)  
**Status:** IN PROGRESS; **not** a terminal assurance result.  
**Review date:** 2026-10-22  
**Published target:** https://trustoverip.github.io/tswg-tsp-specification/  
**Source repository baseline:** [trustoverip/tswg-tsp-specification@ccda6b33159d860f05c328eb436dabe83548b705](https://github.com/trustoverip/tswg-tsp-specification/commit/ccda6b33159d860f05c328eb436dabe83548b705) (latest source commit discovered at intake; **render-to-commit equivalence not yet established**).

> **Source conflict:** the published HTML inspected at intake identifies itself as “vs1.0 Experimental Implementor’s Draft Rev 2”, whereas an earlier conversational review described Rev 3. The latter is not independently verified. All findings below are scoped to the inspected Rev 2 publication until the published artifact and source tree can be reconciled. The upstream repository README remains a specification-template README and is not normative TSP content.

## 1. Method and disposition rules

RAHP v2.8.0 defines the assurance chain **persona/scenario → harm/risk → proposition → control/guardrail → evidence → inference → actionable recommendation** ([method](../../docs/how-rahp-works.md)). A full-stack assessment has four independently attributable lenses: **RAHP, security, combination/composition, DRARM**. Do not promote a component PASS to a composition PASS; do not promote a successful tool invocation to assurance. Missing evidence is **INDETERMINATE**, not PASS. This baseline is a documentary intake, not a completed controller execution.

DRARM means **Distributed Resilience and Amplification Risk Model**. The established integration trail [#643](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/643) documents a resilience catalogue, detectors, default profile, a resilience command, DR-A1–DR-A5 depth and controller integration. [#873](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/873) and [#876](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/876) require per-lens dispositions and resilience depth. Actual current CLI paths, profile identifiers, and executed results still require checkout verification.

## 2. Source-grounded observations

| Anchor in published Rev 2 | Direct observation | Bounded inference |
|---|---|---|
| [Overview / Reference Architecture](https://trustoverip.github.io/tswg-tsp-specification/) | Direct and routed modes; intermediaries need not be trustworthy; VID verification relies on support systems. | Intermediary, VID and endpoint assurance must be separately assessed. |
| [Authenticity, Confidentiality, Metadata Privacy](https://trustoverip.github.io/tswg-tsp-specification/) | Authenticity is always intended; confidentiality and metadata protection are optional; routing and nesting are named mechanisms. | No general anonymity claim is justified without an adversary-specific evaluation. |
| [VID General Requirements / Handling Changes](https://trustoverip.github.io/tswg-tsp-specification/) | VID verification is method-specific; “Handling Changes” is explicitly marked TODO and links upstream issue #4. | Lifecycle/key-state uncertainty is a concrete editorial and assurance gap in the inspected Rev 2 publication. |
| [Messages / Relationships](https://trustoverip.github.io/tswg-tsp-specification/) | Relationships are directional and may be asynchronously inconsistent; verification and appraisal depend on local VID context. | Do not infer reciprocal relationship state or application authority. |
| [Sender Procedure](https://trustoverip.github.io/tswg-tsp-specification/) | Initial send example is explicitly illustrative, allows application data in the first message, and says dynamic changes/error conditions are not considered. | Counterparty binding, first-message effects and failure behavior require integration tests; this is not proof of an exploit. |
| [Envelope / Payload / Signature](https://trustoverip.github.io/tswg-tsp-specification/) | Message comprises envelope, payload, signature; CESR is used for framing; confidentiality may use PKAE. | Parser equivalence and cryptographic binding require executable evidence. |

## 3. RAHP risks and human harms

| ID | Persona / scenario | Harm | Proposition to test | Required evidence | Initial state |
|---|---|---|---|---|---|
| TSP-RH-01 | Receiver accepts an introduced VID for an unintended counterparty | Fraud, unauthorized disclosure | VID verification plus independent counterparty binding meets application policy | Introduction fixtures, policy traces, negative misbinding case | INDETERMINATE |
| TSP-RH-02 | User relies on a relationship after key compromise or changed authority | Impersonation, loss of access | Lifecycle invalidation is timely and authoritative | VID-method rotation/recovery fixtures, cache freshness, failure behavior | INDETERMINATE |
| TSP-RH-03 | Service treats authenticated TSP message as delegated authority | Unauthorized consequential action | Authentication and authorization remain independent | Application PDP and delegation checks at execution time | INDETERMINATE |
| TSP-RH-04 | Network observer correlates visible VIDs and routing patterns | Surveillance, exposure of sensitive associations | Claimed privacy properties hold for stated adversary and mode | Traffic analysis, logging/retention review, multi-vantage tests | INDETERMINATE |
| TSP-RH-05 | VID resolution unavailable for essential-service participant | Exclusion or denial of service | Safe failure plus governed recovery/alternative access | Availability/failover and user recovery evidence | INDETERMINATE |
| TSP-RH-06 | Automated operation is disputed | No accountability or remedy | Operation evidence remains distinct from legitimacy and contestability | Decision/authority provenance, redress procedure | INDETERMINATE |

## 4. Security examination

| ID | Attack/failure | Control proposition | Negative test | State |
|---|---|---|---|---|
| TSP-SEC-01 | Malicious OOBI / counterparty substitution | Expected-party binding not inferred from key validity | Valid attacker VID supplied for expected party | REQUIRED, NOT EXECUTED |
| TSP-SEC-02 | Stale or compromised signing/encryption key | Authorized key-state provenance and freshness | Rotate/revoke key while caches remain stale | REQUIRED, NOT EXECUTED |
| TSP-SEC-03 | Signature/envelope or ciphertext interpretation mismatch | Cryptographic context and exact serialized bytes agree | Mutated envelope, CESR alternate encoding, nested payload | REQUIRED, NOT EXECUTED |
| TSP-SEC-04 | Replayed valid instruction | No unauthorized duplicate application effects | Re-submit signed consequential payload | REQUIRED, NOT EXECUTED |
| TSP-SEC-05 | Unbounded parser or resolution | Resource use remains bounded | Deep nesting, oversized lengths, resolver timeout | REQUIRED, NOT EXECUTED |
| TSP-SEC-06 | Intermediary modification/suppression | End-to-end integrity and explicit availability limits | Tamper, reorder, delay and drop routed message | REQUIRED, NOT EXECUTED |

## 5. Combination / composition examination

| ID | Seam | False inference to prevent | Evidence obligation | State |
|---|---|---|---|---|
| TSP-COM-01 | VID support → TSP | Key verification proves real-world identity or governance recognition | Independent binding/trust framework evidence | INDETERMINATE |
| TSP-COM-02 | TSP → application | Relationship means delegated authorization | Policy evaluation and delegation scope/expiry | INDETERMINATE |
| TSP-COM-03 | TSP → intermediary → transport | Protected payload means unlinkable traffic | Traffic correlation and route observation | INDETERMINATE |
| TSP-COM-04 | Key lifecycle → persistent relationship | Historical valid relationship remains currently valid | Revalidation/revocation transition traces | INDETERMINATE |
| TSP-COM-05 | TSP → autonomous agent → consequential act | Authenticated agent is empowered to act for principal | Principal/delegate binding and use-time authorization | INDETERMINATE |

## 6. DRARM examination: distributed resilience and amplification

**Applicability:** provisionally **APPLICABLE**, because TSP expressly includes asynchronous messages, routed intermediaries, external VID resolution, relationship state and potentially repeated or nested processing. The precise catalogue rule mapping and required DR-A depth are **not yet established**.

| ID | Distributed failure or amplification hypothesis | Induced-failure evidence required | Achieved DR-A | State |
|---|---|---|---|---|
| TSP-DR-01 | VID resolver outage causes cascading failed introductions or excessive retries | Resolver fault injection, retry budgets, recovery timeline | Not established | INDETERMINATE |
| TSP-DR-02 | Routing intermediary outage causes queue buildup, redelivery or loss | Partition, backlog, backpressure and replay observations | Not established | INDETERMINATE |
| TSP-DR-03 | Key rotation propagates inconsistently among endpoints | Mixed old/new key-state transition and reconciliation traces | Not established | INDETERMINATE |
| TSP-DR-04 | Nested message processing amplifies resource demand | Depth/size/fanout stress and bounded termination evidence | Not established | INDETERMINATE |
| TSP-DR-05 | Duplicate delivery amplifies consequential downstream actions | At-least-once delivery, idempotency and recovery tests | Not established | INDETERMINATE |
| TSP-DR-06 | Partial endpoint/intermediary recovery produces divergent relationship tables | Restart/partition convergence and stale-state rejection | Not established | INDETERMINATE |

These are proposed scenarios for the existing DRARM model, **not** claims that a DRARM detector has fired or that a DR-A level was achieved.

## 7. Cross-lens reconciliation ledger

| Lens | Materiality | Execution | Assurance | Evidence depth | Next action |
|---|---|---|---|---|---|
| RAHP | Applicable | Documentary intake only | INDETERMINATE | Published specification observations | Complete proposition/control/evidence records |
| Security | Applicable | Not executed | INDETERMINATE | Proposed negative cases | Run security mode and validate cases |
| Combination | Applicable | Not executed | INDETERMINATE | Identified composition seams | Execute combination/combined assessment |
| DRARM | Applicable, provisional | Not executed | INDETERMINATE | Candidate distributed failure hypotheses | Verify model/profile and run resilience assessment |
| Specialist (privacy, where material) | Applicability to be resolved | Not executed/referred | INDETERMINATE | Metadata threat identified | Evaluate specialist routing; do not silently omit |

**Overall terminal outcome:** **NOT ISSUED**. No full-stack assurance PASS/FAIL/AMBER/GREEN certification is asserted from this intake.

## 8. Evidence and completion work

- [x] Locate and verify the published Rev 2 status and core architectural provisions.
- [x] Locate current RAHP method and prior DRARM integration requirements.
- [x] Record four-lens scenarios and an explicit non-terminal disposition ledger.
- [ ] Establish immutable equivalence between published HTML and source revision; reconcile any Rev 3 reference.
- [ ] Locate and run current RAHP, security, combined/composition and DRARM commands against a reproducible TSP subject.
- [ ] Map DRARM scenarios to existing catalogue rules and determine required/achieved DR-A depth.
- [ ] Reuse existing cases; add tested reusable cases only where missing.
- [ ] Produce source-pinned machine-readable evidence, logs and negative test results.
- [ ] Reconcile all four lenses and any applicable specialist returns.
- [ ] Publish final technical and table-rich human-readable reports with stable anchors and residual actions.
- [ ] Validate all output and record the terminal controller outcome.

**Follow-on, not included in this campaign:** a separate DTFC + RAHP synthesis with corpus-grounded negative cases and downloadable Markdown report.
