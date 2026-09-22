---
layout: default
title: "Portable assurance catalogue"
parent: Reference
nav_order: 2
has_toc: true
---
# Portable assurance catalogue

RAHP v1.1 provides a **method-level assurance knowledge model** that can be reused across deployments without importing deployment governance state. The canonical source is `method/catalogue/`.

The chain is `harm ← risk → control → guardrail / assurance → evidence`. See the [RAHP glossary](glossary.md) for simple-English definitions.

## Guardrail completeness

Each `RKP-*` record declares `guardrail_requirement.status`: `required`, `conditional`, or `control_sufficient`. Only a missing **required** guardrail is a catalogue defect. The current catalogue has **zero required guardrail gaps**. `RKP-PE-02` is conditional because a guardrail is needed only when materially affected parties lack meaningful choice, exit or remedy.

## Harm patterns

### HRM-AUT-01 — Manipulation

A person or accountable principal is steered toward an outcome through materially misleading, asymmetric or exploitative influence.

| Field | Value |
|---|---|
| Family | Autonomy |

### HRM-AUT-02 — Coercion

A person faces material penalty, loss or threat unless they accept a system action, disclosure or decision.

| Field | Value |
|---|---|
| Family | Autonomy |

### HRM-AUT-03 — Loss of meaningful choice

Nominal consent or choice exists but practical alternatives, information or timing are insufficient for meaningful agency.

| Field | Value |
|---|---|
| Family | Autonomy |

### HRM-AUT-04 — Delegation beyond informed intent

A delegated actor performs or enables an action outside the principal’s reasonably understood mandate.

| Field | Value |
|---|---|
| Family | Autonomy |

### HRM-AUT-05 — Inability to withdraw or revoke

A person cannot effectively terminate consent, delegated authority, participation or continued processing.

| Field | Value |
|---|---|
| Family | Autonomy |

### HRM-ACC-01 — Wrongful exclusion

A legitimate person or organization is denied access, participation or recognition without a justified basis.

| Field | Value |
|---|---|
| Family | Access and inclusion |

### HRM-ACC-02 — Discriminatory burden

A rule or system imposes materially higher burdens on a protected, marginalized or structurally disadvantaged group.

| Field | Value |
|---|---|
| Family | Access and inclusion |

### HRM-ACC-03 — Accessibility failure

A legitimate participant cannot complete a required interaction because accessibility needs are not supported.

| Field | Value |
|---|---|
| Family | Access and inclusion |

### HRM-ACC-04 — Infrastructure dependency exclusion

Access depends on devices, networks, identity infrastructure or services unavailable to some legitimate participants.

| Field | Value |
|---|---|
| Family | Access and inclusion |

### HRM-PRV-01 — Unnecessary disclosure

Information beyond the minimum necessary is exposed to a party or system.

| Field | Value |
|---|---|
| Family | Privacy |

### HRM-PRV-02 — Linkability and correlation

Separate interactions can be linked to construct a broader profile of a person, organization or agent.

| Field | Value |
|---|---|
| Family | Privacy |

### HRM-PRV-03 — Inference beyond disclosed facts

Observed data or metadata enables sensitive conclusions not intentionally disclosed.

| Field | Value |
|---|---|
| Family | Privacy |

### HRM-PRV-04 — Persistent surveillance

System operation enables durable observation or reconstruction of activities across time or contexts.

| Field | Value |
|---|---|
| Family | Privacy |

### HRM-PRV-05 — Secondary use and context collapse

Information collected for one purpose or audience is reused in another materially different context.

| Field | Value |
|---|---|
| Family | Privacy |

### HRM-ECO-01 — Loss of economic opportunity

A system decision prevents or materially reduces access to employment, trade, finance or other economic participation.

| Field | Value |
|---|---|
| Family | Economic |

### HRM-ECO-02 — Fraudulent or misallocated liability

A person or organization bears financial or legal consequences for an action they did not authorize or control.

| Field | Value |
|---|---|
| Family | Economic |

### HRM-GOV-01 — Arbitrary decision

A consequential decision is taken without consistent rules, sufficient reasons or accountable authority.

| Field | Value |
|---|---|
| Family | Governance and due process |

### HRM-GOV-02 — Unavailable appeal or remedy

An affected party lacks a practical path to contest, correct or obtain remedy for an adverse outcome.

| Field | Value |
|---|---|
| Family | Governance and due process |

### HRM-GOV-03 — Unaccountable or captured authority

Decision power is exercised without effective oversight, contestability or independence.

| Field | Value |
|---|---|
| Family | Governance and due process |

### HRM-SEC-01 — Impersonation and false attribution

Actions or claims are attributed to the wrong person, organization or agent.

| Field | Value |
|---|---|
| Family | Security-mediated harm |

### HRM-SEC-02 — Unauthorized consequential action

A system performs a consequential action without current, sufficient authority from the accountable principal.

| Field | Value |
|---|---|
| Family | Security-mediated harm |

### HRM-SEC-03 — Denial or disruption of participation

Security or operational failure prevents legitimate use, continuity, recovery or participation.

| Field | Value |
|---|---|
| Family | Security-mediated harm |

### HRM-INF-01 — False provenance or trust inference

A party correctly observes an artefact or signature but infers legitimacy, endorsement, authority or quality that it does not establish.

| Field | Value |
|---|---|
| Family | Information integrity |

### HRM-SAF-01 — Physical or safeguarding exposure

Digital information or system action materially increases risk of physical harm, stalking, abuse or safeguarding failure.

| Field | Value |
|---|---|
| Family | Safety |

## Risk patterns

### RKP-AUTH-01 — Possession mistaken for authority

Authentication, key possession or identity proof is treated as sufficient evidence that the actor is authorized for the requested action.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02`, `HRM-INF-01` |

### RKP-AUTH-02 — Stale authority accepted

Authority is checked at an earlier lifecycle point and not re-evaluated when a consequential action occurs.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-05`, `HRM-SEC-02` |

### RKP-AUTH-03 — Authority scope ambiguity

Purpose, audience, resource, action, value or time bounds are insufficiently defined or inconsistently interpreted.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-04`, `HRM-ECO-02`, `HRM-SEC-02` |

### RKP-AUTH-04 — Commitment authority mismatch

An authenticated or generally authorized actor attempts a material commitment that is not covered by the exact active mandate, scope, constraints or policy at the commitment boundary.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Commitment admission must positively establish current action-specific authority rather than infer it from identity or general authorization. |
| Condition | exact action authority is not positively established |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02` |

### RKP-AUTH-05 — Approval not bound to exact commitment

A human or organizational approval is accepted for a materially different, superseded or stale action than the commitment being admitted.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Approval must be bound to the exact commitment digest and current policy context. |
| Condition | approval binding is absent, mismatched or stale |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02` |

### RKP-AUTH-06 — Reputation or capability substituted for authority

Reputation, capability advertisement, assurance posture or technical ability is treated as permission to create a material commitment.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Advisory or technical signals must not enlarge principal-derived authority. |
| Condition | non-authority evidence is used as an authorization grant |
| Harm Patterns | `HRM-AUT-04`, `HRM-INF-01` |

### RKP-AUTH-07 — Commitment authority cannot be reconstructed

A later verifier cannot establish which mandate, policy, status, approval and exact action were evaluated when a material commitment was admitted or rejected.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Material authority decisions need replayable evidence sufficient to distinguish historical authority from present state. |
| Condition | decision provenance or time-specific authority evidence is unavailable |
| Harm Patterns | `HRM-GOV-02`, `HRM-ECO-02` |

### RKP-DEL-01 — Transitive delegation expansion

A downstream delegate receives or infers broader authority than the upstream principal granted.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02` |

### RKP-DEL-02 — Delegation provenance loss

An execution chain cannot demonstrate which principal authorized which delegate under what scope.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-02`, `HRM-ECO-02`, `HRM-SEC-02` |

### RKP-DEL-03 — Revocation propagation failure

Withdrawal or suspension of delegated authority does not reach all parties or enforcement points before further action.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-05`, `HRM-SEC-02` |

### RKP-GOV-01 — Concentrated governance authority

A single actor or tightly aligned group can set, change or enforce rules without independent constraint.

| Field | Value |
|---|---|
| Family | Governance and capture |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-01`, `HRM-GOV-03` |

### RKP-GOV-02 — Governance capture or collusion

Actors expected to provide independent oversight coordinate, collude or are commonly controlled.

| Field | Value |
|---|---|
| Family | Governance and capture |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-03`, `HRM-ACC-02` |

### RKP-GOV-03 — Rule change without safe transition

Policy or governance semantics change while old artefacts or dependent implementations remain active without migration rules.

| Field | Value |
|---|---|
| Family | Governance and capture |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-01`, `HRM-SEC-03` |

### RKP-GOV-04 — Responsibility fragmentation

No single accountable path exists for an adverse outcome that spans specifications, operators or trust domains.

| Field | Value |
|---|---|
| Family | Governance and capture |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-02`, `HRM-ECO-02` |

### RKP-ID-01 — Identity or role misbinding

Identity layers or roles are substituted or conflated, binding a claim or action to the wrong subject, issuer, holder, operator or principal.

| Field | Value |
|---|---|
| Family | Identity and attribution |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-SEC-01`, `HRM-INF-01` |

### RKP-ID-02 — Uniqueness assumption failure

A system assumes uniqueness or one-person/one-actor semantics without a defensible mechanism or stated limitation.

| Field | Value |
|---|---|
| Family | Identity and attribution |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-03`, `HRM-ACC-02` |

### RKP-ID-03 — Recovery enables takeover or exclusion

Recovery is absent, inaccessible or weak enough to enable account/identity takeover.

| Field | Value |
|---|---|
| Family | Identity and attribution |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-ACC-01`, `HRM-SEC-01`, `HRM-SEC-03` |

### RKP-DISC-01 — Discovery interpreted as endorsement

Presence in a discovery document, registry or directory is treated as certification, endorsement or sufficient trust.

| Field | Value |
|---|---|
| Family | Discovery and trust inference |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-INF-01`, `HRM-SEC-02` |

### RKP-DISC-02 — Stale discovery metadata

Cached or unrefreshed discovery metadata preserves obsolete endpoints, keys, capabilities, authority or status.

| Field | Value |
|---|---|
| Family | Discovery and trust inference |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-SEC-01`, `HRM-SEC-03`, `HRM-INF-01` |

### RKP-DISC-03 — Registry governance ambiguity

Relying parties cannot determine who may add, remove, suspend or correct registry entries and under what authority.

| Field | Value |
|---|---|
| Family | Discovery and trust inference |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-03`, `HRM-INF-01` |

### RKP-CRD-01 — Credential validity interpreted as authorization

A valid credential or proof is treated as permission for an action outside the credential’s actual claim semantics.

| Field | Value |
|---|---|
| Family | Credentials and claims |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-SEC-02`, `HRM-INF-01` |

### RKP-CRD-02 — Credential status or issuer authority staleness

Credential validity or issuer authority is evaluated using stale status, registry or governance state.

| Field | Value |
|---|---|
| Family | Credentials and claims |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-SEC-02`, `HRM-SEC-03` |

### RKP-CRD-03 — Credential context detachment

A credential bound to a task, ceremony, transaction or context is later reused as a free-standing assurance claim.

| Field | Value |
|---|---|
| Family | Credentials and claims |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-INF-01`, `HRM-SEC-02` |

### RKP-CRD-04 — Credential audience or purpose expansion

A credential or secondary credential is forwarded, reused or presented to a broader audience or purpose than intended.

| Field | Value |
|---|---|
| Family | Credentials and claims |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-PRV-01`, `HRM-PRV-05`, `HRM-AUT-04` |

### RKP-PRV-01 — Stable identifier correlation

Persistent identifiers allow interactions across relying parties or contexts to be correlated.

| Field | Value |
|---|---|
| Family | Privacy and inference |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-PRV-02`, `HRM-PRV-04` |

### RKP-PRV-02 — Composition fingerprinting

Individually minimal proofs or metadata become identifying or sensitive when combined.

| Field | Value |
|---|---|
| Family | Privacy and inference |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-PRV-02`, `HRM-PRV-03` |

### RKP-PRV-03 — Failure channel disclosure

Errors, diagnostics or status responses reveal sensitive attributes, classifications or relationship information.

| Field | Value |
|---|---|
| Family | Privacy and inference |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-PRV-01`, `HRM-PRV-03` |

### RKP-EXC-01 — Single-path participation exclusion

A system requires one identity, device, interaction or proofing path without a viable alternative for legitimate participants.

| Field | Value |
|---|---|
| Family | Inclusion and accessibility |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-ACC-01`, `HRM-ACC-03`, `HRM-ACC-04` |

### RKP-EXC-02 — Social or institutional privilege dependency

Access depends on pre-existing social, institutional or documentation privilege that is unevenly distributed.

| Field | Value |
|---|---|
| Family | Inclusion and accessibility |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-ACC-01`, `HRM-ACC-02` |

### RKP-AGT-01 — Agent goal or mandate drift

An autonomous actor optimizes or continues execution in ways that depart from the principal’s current purpose or constraints.

| Field | Value |
|---|---|
| Family | Agentic systems |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02` |

### RKP-AGT-02 — Secondary credential transitivity

A credential obtained for one agent/task is forwarded or treated as authority for another without explicit onward delegation.

| Field | Value |
|---|---|
| Family | Agentic systems |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-04`, `HRM-PRV-05`, `HRM-SEC-02` |

### RKP-AGT-03 — Opaque execution accountability gap

Opaque internal execution is combined with insufficient external action provenance to reconstruct accountability.

| Field | Value |
|---|---|
| Family | Agentic systems |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-02`, `HRM-ECO-02` |

### RKP-OPS-01 — Dependency unavailability or stale fallback

A required registry, status, issuer, policy or network dependency is unavailable and fallback behavior is unsafe or undefined.

| Field | Value |
|---|---|
| Family | Operational resilience |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-SEC-03`, `HRM-INF-01` |

### RKP-OPS-02 — Replay or duplicate side effect

A valid request, proof or task can be replayed or retried in a way that repeats an externally consequential effect.

| Field | Value |
|---|---|
| Family | Operational resilience |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-ECO-02`, `HRM-SEC-02` |

### RKP-OPS-03 — Cascading invalidation

Compromise, deregistration or withdrawal of a dependency invalidates many downstream artefacts without a safe continuity path.

| Field | Value |
|---|---|
| Family | Operational resilience |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-ACC-01`, `HRM-SEC-03` |

### RKP-RED-01 — Evidence insufficient for contestability

The system cannot produce durable evidence necessary to explain, contest or remedy a consequential outcome.

| Field | Value |
|---|---|
| Family | Accountability and redress |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-02`, `HRM-ECO-02` |

### RKP-COMP-01 — Cross-spec authority mismatch

Two specifications use compatible-looking identity or authorization concepts with materially different semantics.

| Field | Value |
|---|---|
| Family | Composition |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02`, `HRM-INF-01` |

### RKP-COMP-02 — Cross-spec lifecycle mismatch

Validity, status, expiry, revocation or freshness is evaluated at different lifecycle points across dependent specifications.

| Field | Value |
|---|---|
| Family | Composition |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-AUT-05`, `HRM-SEC-02`, `HRM-SEC-03` |

### RKP-COMP-03 — Cross-system linkability

Composition across protocols exposes identifiers or metadata that defeat privacy separation present in each component.

| Field | Value |
|---|---|
| Family | Composition |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-PRV-02`, `HRM-PRV-05` |

### RKP-COMP-04 — Policy or evidence boundary conflict

Dependent systems disagree about which artefact establishes completion, authority, status or an auditable fact.

| Field | Value |
|---|---|
| Family | Composition |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-02`, `HRM-INF-01` |

### RKP-PE-01 — Infrastructure dependency capture

A critical governance or verification dependency is controlled by an actor that can extract rents, surveil participants or change access conditions.

| Field | Value |
|---|---|
| Family | Political economy |
| Guardrail requirement | required |
| Why | This risk can create an unacceptable state at a clear decision or execution boundary, so a portable guardrail should block or stop that state. |
| Harm Patterns | `HRM-GOV-03`, `HRM-PRV-04`, `HRM-ACC-04` |

### RKP-PE-02 — Failure cost externalization

Operators or intermediaries capture benefits while harmed participants bear disproportionate remediation, exclusion or liability costs.

| Field | Value |
|---|---|
| Family | Political economy |
| Guardrail requirement | conditional |
| Why | Failure costs are not always avoidable. A guardrail is required when affected people cannot reasonably choose, exit or seek remedy. |
| Condition | Applies to high-impact or involuntary use where materially affected parties lack meaningful choice, exit or remedy. |
| Harm Patterns | `HRM-ECO-01`, `HRM-ECO-02`, `HRM-GOV-02` |

### RKP-DEL-04 — Attribution lineage mistaken for authority

Caller-supplied delegation or actor-lineage metadata is treated as proof that the represented grants actually existed or remain valid.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Attribution metadata can be syntactically valid while fabricated, so consequential action requires independent authority evidence. |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02` |

### RKP-DEL-05 — Delegation lineage mutation

A delegating or forwarding actor rewrites prior lineage hops, making later audit unable to distinguish the forwarded representation from the chain originally received.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Prior-hop mutation destroys independent attribution evidence unless the received representation is retained or integrity-bound. |
| Harm Patterns | `HRM-GOV-02`, `HRM-SEC-02` |

### RKP-DEL-06 — Delegation evidence-state collapse

Missing, unresolvable, invalid, expired or revoked delegation evidence is collapsed into a generic denial or success state, obscuring what was actually established.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Distinct evidence and lifecycle states are necessary for safe enforcement, audit reconstruction and redress. |
| Harm Patterns | `HRM-GOV-02`, `HRM-SEC-02` |

### RKP-DEL-07 — Delegation evidence cross-context replay

A content or proof reference valid in one trust domain is replayed in another because the referenced commitment is not bound to the relevant context or domain.

| Field | Value |
|---|---|
| Family | Authority and delegation |
| Guardrail requirement | required |
| Why | Context-free evidence references can preserve byte integrity while misbinding authority semantics. |
| Harm Patterns | `HRM-AUT-04`, `HRM-SEC-02` |

### RKP-PRV-04 — Delegation lineage correlation exposure

Multi-hop actor lineage unnecessarily discloses durable principal or agent identifiers across contexts, creating a correlation surface beyond what the relying decision requires.

| Field | Value |
|---|---|
| Family | Privacy and data protection |
| Guardrail requirement | required |
| Why | Auditability should not require unnecessary durable cross-context correlation when a less disclosing proof can satisfy the assurance objective. |
| Harm Patterns | `HRM-PRV-01`, `HRM-AUT-03` |

## Control patterns

### CTP-AUTH-01 — Separate authentication from authorization

Require an explicit authorization decision independent of identity, authentication, credential validity or discovery integrity.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-AUTH-01`, `RKP-CRD-01`, `RKP-DISC-01`, `RKP-AUTH-04`, `RKP-AUTH-06` |

### CTP-AUTH-02 — Action-time authority evaluation

Evaluate current authority, status, expiry and revocation immediately before a consequential action.

| Field | Value |
|---|---|
| Control function | prevent |
| Risk Patterns | `RKP-AUTH-02`, `RKP-CRD-02`, `RKP-COMP-02` |
| Evidence Patterns | `EVP-AUTH-01` |

### CTP-AUTH-03 — Machine-readable authority envelope

Represent audience, action, resource, purpose, value, time and delegation bounds in a form that can be enforced.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-AUTH-03`, `RKP-DEL-01`, `RKP-AGT-01` |
| Evidence Patterns | `EVP-AUTH-02` |

### CTP-DEL-01 — Delegation chain continuity

Preserve the originating principal and bounded authority envelope across each delegation hop.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-DEL-01`, `RKP-DEL-02`, `RKP-AGT-02`, `RKP-COMP-01` |
| Evidence Patterns | `EVP-DEL-01` |

### CTP-DEL-02 — Revocation propagation

Distribute revocation/suspension rapidly to every enforcement point that can exercise delegated authority.

| Field | Value |
|---|---|
| Control function | interrupt |
| Risk Patterns | `RKP-DEL-03`, `RKP-AUTH-02` |
| Evidence Patterns | `EVP-DEL-02` |

### CTP-GOV-01 — Independent governance checks

Separate policy creation, approval, enforcement and appeal so no single actor can unilaterally control the full lifecycle.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-GOV-01`, `RKP-GOV-02`, `RKP-DISC-03` |
| Evidence Patterns | `EVP-GOV-01` |

### CTP-GOV-02 — Versioned policy transition

Publish effective dates, migration rules, compatibility constraints and rollback/retirement handling for governance changes.

| Field | Value |
|---|---|
| Control function | recover |
| Risk Patterns | `RKP-GOV-03`, `RKP-COMP-02` |
| Evidence Patterns | `EVP-GOV-02` |

### CTP-GOV-03 — Cross-boundary responsibility map

Assign accountable owners and redress paths for outcomes that span protocols, operators or trust domains.

| Field | Value |
|---|---|
| Control function | remediate |
| Risk Patterns | `RKP-GOV-04`, `RKP-RED-01`, `RKP-COMP-04` |
| Evidence Patterns | `EVP-RED-01` |

### CTP-ID-01 — Explicit role binding

Bind subject, issuer, holder, operator, principal and relying-party roles explicitly and reject role substitution.

| Field | Value |
|---|---|
| Control function | prevent |
| Risk Patterns | `RKP-ID-01`, `RKP-COMP-01` |

### CTP-ID-02 — Recovery with takeover resistance

Provide accessible recovery with independent checks, notification, delay or quorum protections appropriate to impact.

| Field | Value |
|---|---|
| Control function | recover |
| Risk Patterns | `RKP-ID-03` |
| Evidence Patterns | `EVP-REC-01` |

### CTP-DISC-01 — Discovery non-inference rule

State and enforce that discoverability, signed metadata or registry presence does not itself establish authorization, certification or endorsement.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-DISC-01`, `RKP-CRD-01` |

### CTP-DISC-02 — Discovery freshness and withdrawal

Define cache bounds, refresh rules, withdrawal semantics and stale-state behavior for discovery metadata.

| Field | Value |
|---|---|
| Control function | detect |
| Risk Patterns | `RKP-DISC-02`, `RKP-OPS-01` |
| Evidence Patterns | `EVP-OPS-01` |

### CTP-DISC-03 — Registry governance policy

Publish admission, update, suspension, removal, correction, audit and appeal authority for registry entries.

| Field | Value |
|---|---|
| Control function | govern |
| Risk Patterns | `RKP-DISC-03`, `RKP-GOV-01` |
| Evidence Patterns | `EVP-GOV-01` |

### CTP-CRD-01 — Context-bound credential use

Bind credential use to intended task, transaction, audience or purpose and reject detached reuse when context is material.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-CRD-03`, `RKP-CRD-04`, `RKP-OPS-02` |

### CTP-CRD-02 — Status-as-of semantics

Define which status and authority state must be evaluated and at what time for issuance, presentation and action.

| Field | Value |
|---|---|
| Control function | detect |
| Risk Patterns | `RKP-CRD-02`, `RKP-COMP-02` |
| Evidence Patterns | `EVP-AUTH-01` |

### CTP-PRV-01 — Pairwise or scoped identifiers

Use context-scoped identifiers and minimize stable metadata where correlation is not required.

| Field | Value |
|---|---|
| Control function | prevent |
| Risk Patterns | `RKP-PRV-01`, `RKP-COMP-03` |

### CTP-PRV-02 — Composition privacy analysis

Evaluate privacy and inference risks for the combined disclosure set, not only each credential or artefact independently.

| Field | Value |
|---|---|
| Control function | detect |
| Risk Patterns | `RKP-PRV-02`, `RKP-COMP-03` |
| Evidence Patterns | `EVP-PRV-01` |

### CTP-PRV-03 — Privacy-safe failure responses

Limit errors and diagnostics to information necessary for remediation, with sensitive detail protected or authenticated.

| Field | Value |
|---|---|
| Control function | prevent |
| Risk Patterns | `RKP-PRV-03` |

### CTP-EXC-01 — Alternative participation path

Provide at least one viable alternative when the primary identity, device, accessibility or connectivity path excludes legitimate participants.

| Field | Value |
|---|---|
| Control function | compensate |
| Risk Patterns | `RKP-EXC-01`, `RKP-EXC-02` |
| Evidence Patterns | `EVP-INCL-01` |

### CTP-AGT-01 — Principal intent checkpoint

Require step-up confirmation or reauthorization for material scope expansion, high-impact action or changed conditions.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-AGT-01`, `RKP-AUTH-03` |
| Evidence Patterns | `EVP-AUTH-02` |

### CTP-AGT-02 — Secondary credential non-transitivity

Do not forward or reuse secondary credentials across agents or purposes unless onward delegation is explicitly authorized.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-AGT-02`, `RKP-CRD-04` |

### CTP-AGT-03 — External action provenance

Record externally consequential actions, active delegation reference, accountable actor, target, time and outcome without requiring private chain-of-thought.

| Field | Value |
|---|---|
| Control function | audit |
| Risk Patterns | `RKP-AGT-03`, `RKP-DEL-02`, `RKP-RED-01` |
| Evidence Patterns | `EVP-AUD-01` |

### CTP-OPS-01 — Safe dependency degradation

Define fail-closed, defer, bounded-cache or explicit risk-accepted behavior for unavailable dependencies.

| Field | Value |
|---|---|
| Control function | contain |
| Risk Patterns | `RKP-OPS-01`, `RKP-CRD-02` |
| Evidence Patterns | `EVP-OPS-01` |

### CTP-OPS-02 — Idempotency and anti-replay

Bind freshness/uniqueness to consequential requests and make retries idempotent where duplicate effects are unsafe.

| Field | Value |
|---|---|
| Control function | prevent |
| Risk Patterns | `RKP-OPS-02`, `RKP-CRD-03` |
| Evidence Patterns | `EVP-OPS-02` |

### CTP-OPS-03 — Dependency invalidation continuity plan

Define notification, re-verification, grace, replacement and rollback behavior when a dependency is compromised or withdrawn.

| Field | Value |
|---|---|
| Control function | recover |
| Risk Patterns | `RKP-OPS-03` |
| Evidence Patterns | `EVP-GOV-02` |

### CTP-RED-01 — Contestability evidence package

Preserve sufficient decision, policy, identity/authority and action evidence to support explanation, appeal and remediation.

| Field | Value |
|---|---|
| Control function | audit |
| Risk Patterns | `RKP-RED-01`, `RKP-GOV-04` |
| Evidence Patterns | `EVP-RED-01`, `EVP-AUD-01` |

### CTP-COMP-01 — Cross-spec semantic contract

Define ownership and exact semantics of identity, authority, status, completion and evidence facts at each specification seam.

| Field | Value |
|---|---|
| Control function | prevent |
| Risk Patterns | `RKP-COMP-01`, `RKP-COMP-04` |
| Evidence Patterns | `EVP-COMP-01` |

### CTP-COMP-02 — Cross-spec lifecycle test matrix

Test dependent specifications across issue, authorize, present, execute, revoke, retry, migrate and appeal timing boundaries.

| Field | Value |
|---|---|
| Control function | detect |
| Risk Patterns | `RKP-COMP-02`, `RKP-OPS-02` |
| Evidence Patterns | `EVP-COMP-01` |

### CTP-PE-01 — Dependency governance and exit assessment

Document control, funding, surveillance capability, switching cost, shutdown authority and exit paths for critical dependencies.

| Field | Value |
|---|---|
| Control function | govern |
| Risk Patterns | `RKP-PE-01`, `RKP-PE-02` |
| Evidence Patterns | `EVP-GOV-01` |

### CTP-RISK-01 — Control side-effect assessment

Assess whether a mitigation introduces, amplifies or redistributes other risks and require explicit disposition of material side effects.

| Field | Value |
|---|---|
| Control function | detect |
| Risk Patterns | `RKP-EXC-02`, `RKP-PRV-01`, `RKP-PE-02` |
| Evidence Patterns | `EVP-RISK-01` |

### CTP-ID-03 — Explicit uniqueness assurance

Where uniqueness is required, define the population, assurance mechanism, false-positive/false-negative limits and non-uniqueness fallback explicitly.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-ID-02` |
| Evidence Patterns | `EVP-RISK-01` |

### CTP-DEL-03 — Independent delegation evidence resolution

Keep attribution lineage separate from authority by resolving grant evidence outside caller-supplied lineage metadata.

| Field | Value |
|---|---|
| Control function | verify |
| Risk Patterns | `RKP-DEL-04`, `RKP-DEL-06` |
| Evidence Patterns | `EVP-AUTH-01` |

### CTP-DEL-04 — Append-only lineage integrity

Detect or prevent rewriting of prior delegation lineage hops across receive and forwarding boundaries.

| Field | Value |
|---|---|
| Control function | detect |
| Risk Patterns | `RKP-DEL-05` |
| Evidence Patterns | `EVP-OPS-01` |

### CTP-DEL-05 — Context-bound delegation evidence

Bind portable delegation evidence references to the context or trust domain in which their authority semantics apply.

| Field | Value |
|---|---|
| Control function | constrain |
| Risk Patterns | `RKP-DEL-07` |
| Evidence Patterns | `EVP-AUTH-01` |

### CTP-PRV-04 — Delegation lineage minimization

Disclose only the delegation-lineage attributes required for the relying decision and accountable audit purpose.

| Field | Value |
|---|---|
| Control function | minimize |
| Risk Patterns | `RKP-PRV-04` |
| Evidence Patterns | `EVP-OPS-01` |

## Guardrail patterns

### GRP-AUTH-01 — No authority by inference

A consequential action is authorized solely from authentication, possession, credential validity, discovery metadata or registry presence.

| Field | Value |
|---|---|
| Protected interest | principal agency |
| Risk Patterns | `RKP-AUTH-01`, `RKP-CRD-01`, `RKP-DISC-01` |
| Control Patterns | `CTP-AUTH-01`, `CTP-DISC-01` |

### GRP-AUTH-02 — Current authority required

A consequential action proceeds when required authority, revocation or status state cannot be established at the action boundary.

| Field | Value |
|---|---|
| Protected interest | principal agency |
| Risk Patterns | `RKP-AUTH-02`, `RKP-DEL-03`, `RKP-CRD-02`, `RKP-AUTH-04`, `RKP-AUTH-05`, `RKP-AUTH-07` |
| Control Patterns | `CTP-AUTH-02`, `CTP-DEL-02` |

### GRP-DEL-01 — Delegation cannot silently expand

A delegate or downstream actor receives materially broader scope than was granted by the accountable principal.

| Field | Value |
|---|---|
| Protected interest | principal agency |
| Risk Patterns | `RKP-DEL-01`, `RKP-AUTH-03` |
| Control Patterns | `CTP-AUTH-03`, `CTP-DEL-01` |

### GRP-GOV-01 — No unilateral irreversible governance action

One actor can make an irreversible high-impact governance decision without defined independent check or later remedy.

| Field | Value |
|---|---|
| Protected interest | due process |
| Risk Patterns | `RKP-GOV-01`, `RKP-GOV-02` |
| Control Patterns | `CTP-GOV-01` |

### GRP-ID-01 — No role substitution

A verifier substitutes one identity/role layer for another without an explicit binding rule.

| Field | Value |
|---|---|
| Protected interest | identity integrity |
| Risk Patterns | `RKP-ID-01` |
| Control Patterns | `CTP-ID-01` |

### GRP-PRV-01 — No unnecessary disclosure

A required flow discloses information not necessary for the stated decision or function.

| Field | Value |
|---|---|
| Protected interest | privacy |
| Risk Patterns | `RKP-PRV-02`, `RKP-PRV-03` |
| Control Patterns | `CTP-PRV-02`, `CTP-PRV-03` |

### GRP-EXC-01 — No essential-service single path

A high-impact or essential participation path has no viable alternative for foreseeable legitimate users excluded by the primary mechanism.

| Field | Value |
|---|---|
| Protected interest | equitable access |
| Risk Patterns | `RKP-EXC-01`, `RKP-EXC-02` |
| Control Patterns | `CTP-EXC-01` |

### GRP-AGT-01 — No agent action beyond current mandate

An autonomous agent performs a consequential action outside the current bounded mandate.

| Field | Value |
|---|---|
| Protected interest | principal agency |
| Risk Patterns | `RKP-AGT-01`, `RKP-AGT-02` |
| Control Patterns | `CTP-AGT-01`, `CTP-AGT-02` |

### GRP-OPS-01 — No unsafe replay

A replay or retry can repeat an externally consequential side effect without a new authorized decision.

| Field | Value |
|---|---|
| Protected interest | transaction integrity |
| Risk Patterns | `RKP-OPS-02` |
| Control Patterns | `CTP-OPS-02` |

### GRP-RED-01 — No consequential decision without contestability evidence

A high-impact adverse decision is made without sufficient retained evidence and an accountable appeal/remedy path.

| Field | Value |
|---|---|
| Protected interest | due process |
| Risk Patterns | `RKP-RED-01`, `RKP-GOV-04` |
| Control Patterns | `CTP-RED-01`, `CTP-GOV-03` |

### GRP-COMP-01 — No implicit cross-spec semantic substitution

A fact established by one specification is treated as establishing a different authority, completion, identity or status fact in another without an explicit contract.

| Field | Value |
|---|---|
| Protected interest | composition integrity |
| Risk Patterns | `RKP-COMP-01`, `RKP-COMP-04` |
| Control Patterns | `CTP-COMP-01` |

### GRP-PE-01 — Critical dependency must have governed exit

A critical dependency can materially change access or surveillance conditions with no documented alternative, exit or governance response.

| Field | Value |
|---|---|
| Protected interest | institutional autonomy |
| Risk Patterns | `RKP-PE-01` |
| Control Patterns | `CTP-PE-01` |

### GRP-DEL-02 — Consequential delegated action needs provenance

A consequential delegated or agentic action happens without durable evidence linking the action to the accountable principal and the authority used.

| Field | Value |
|---|---|
| Protected interest | accountability |
| Risk Patterns | `RKP-DEL-02`, `RKP-AGT-03` |
| Control Patterns | `CTP-DEL-01`, `CTP-AGT-03` |

### GRP-GOV-02 — No unsafe governance transition

A governance or policy change takes effect for live artefacts or dependent systems without clear effective dates, migration rules, compatibility handling or retirement rules.

| Field | Value |
|---|---|
| Protected interest | continuity and due process |
| Risk Patterns | `RKP-GOV-03` |
| Control Patterns | `CTP-GOV-02` |

### GRP-GOV-03 — Registry authority must be explicit

Trust-relevant registry entries can be added, changed, suspended, removed or corrected without a published rule saying who has authority and how decisions can be reviewed.

| Field | Value |
|---|---|
| Protected interest | legitimate governance |
| Risk Patterns | `RKP-DISC-03` |
| Control Patterns | `CTP-DISC-03`, `CTP-GOV-01` |

### GRP-CRD-01 — No credential use outside its bound context

A credential is relied on outside its bound task, audience, purpose or authorization context without an explicit rule permitting the broader use.

| Field | Value |
|---|---|
| Protected interest | purpose integrity and principal agency |
| Risk Patterns | `RKP-CRD-03`, `RKP-CRD-04` |
| Control Patterns | `CTP-CRD-01`, `CTP-AGT-02` |

### GRP-OPS-02 — No silent assurance downgrade on dependency failure

A system treats stale, cached or unavailable trust-relevant dependency state as current without a declared and bounded fallback rule.

| Field | Value |
|---|---|
| Protected interest | assurance integrity |
| Risk Patterns | `RKP-OPS-01`, `RKP-DISC-02` |
| Control Patterns | `CTP-OPS-01`, `CTP-DISC-02` |

### GRP-OPS-03 — Systemic invalidation needs a continuity path

Withdrawal, compromise or deregistration of a shared dependency invalidates many downstream artefacts without notification, re-verification, replacement or recovery handling.

| Field | Value |
|---|---|
| Protected interest | service continuity and access |
| Risk Patterns | `RKP-OPS-03` |
| Control Patterns | `CTP-OPS-03` |

### GRP-COMP-02 — Cross-spec lifecycle semantics must reconcile

A consequential composed action proceeds when participating specifications disagree about the relevant validity, freshness, expiry, revocation or status point.

| Field | Value |
|---|---|
| Protected interest | composition integrity |
| Risk Patterns | `RKP-COMP-02` |
| Control Patterns | `CTP-COMP-02`, `CTP-AUTH-02`, `CTP-CRD-02` |

### GRP-PRV-02 — No unnecessary cross-context correlation

Stable identifiers or combined protocol data enable cross-context correlation that is not needed for the declared purpose.

| Field | Value |
|---|---|
| Protected interest | privacy |
| Risk Patterns | `RKP-PRV-01`, `RKP-COMP-03`, `RKP-PRV-04` |
| Control Patterns | `CTP-PRV-01`, `CTP-PRV-02`, `CTP-PRV-04` |

### GRP-ID-02 — No load-bearing uniqueness claim without evidence

A consequential decision relies on a uniqueness or one-person-one-actor claim when the system cannot state and support the scope and mechanism of that claim.

| Field | Value |
|---|---|
| Protected interest | fairness and identity integrity |
| Risk Patterns | `RKP-ID-02` |
| Control Patterns | `CTP-RISK-01` |

### GRP-ID-03 — High-impact recovery must resist takeover

A recovery path for a high-impact account or identity can bypass normal protections without independent checks, notice, delay or equivalent takeover resistance.

| Field | Value |
|---|---|
| Protected interest | identity continuity and access |
| Risk Patterns | `RKP-ID-03` |
| Control Patterns | `CTP-ID-02` |

### GRP-DEL-03 — No authority from lineage alone

A consequential delegated action is authorized solely because a caller-supplied actor or delegation chain is internally well formed.

| Field | Value |
|---|---|
| Protected interest | principal agency |
| Risk Patterns | `RKP-DEL-04`, `RKP-DEL-06` |
| Control Patterns | `CTP-DEL-03` |

### GRP-DEL-04 — No silent lineage rewrite

A forwarding actor modifies a prior delegation hop while the system continues to represent the lineage as append-only audit history.

| Field | Value |
|---|---|
| Protected interest | accountability |
| Risk Patterns | `RKP-DEL-05` |
| Control Patterns | `CTP-DEL-04` |

### GRP-DEL-05 — No cross-context authority by replay

Delegation evidence from one context is accepted as authority in another without a valid context/domain binding.

| Field | Value |
|---|---|
| Protected interest | principal agency |
| Risk Patterns | `RKP-DEL-07` |
| Control Patterns | `CTP-DEL-05` |

## Assurance patterns

### ATP-AUTH-01 — Authentication/authorization separation test

Identity or credential validity alone never authorizes a consequential action.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-AUTH-01` |
| Guardrail Patterns | `GRP-AUTH-01` |
| Evidence Patterns | `EVP-AUTH-01` |

### ATP-AUTH-02 — Action-time revocation test

A revoked or expired authority cannot be exercised after the effective revocation/expiry boundary.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-AUTH-02`, `CTP-DEL-02`, `CTP-CRD-02` |
| Guardrail Patterns | `GRP-AUTH-02` |
| Evidence Patterns | `EVP-AUTH-01` |

### ATP-DEL-01 — Delegation attenuation test

Each downstream delegation is equal to or narrower than the authority received upstream.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-DEL-01`, `CTP-AUTH-03` |
| Guardrail Patterns | `GRP-DEL-01` |
| Evidence Patterns | `EVP-DEL-01` |

### ATP-DEL-02 — Delegation provenance reconstruction

An auditor can reconstruct principal, delegation chain, scope and action for a consequential event.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-DEL-01`, `CTP-AGT-03` |
| Guardrail Patterns | `GRP-DEL-02` |
| Evidence Patterns | `EVP-DEL-01`, `EVP-AUD-01` |

### ATP-GOV-01 — Independent governance decision test

High-impact governance changes show required independent approval and immutable decision evidence.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-GOV-01` |
| Guardrail Patterns | `GRP-GOV-01` |
| Evidence Patterns | `EVP-GOV-01` |

### ATP-GOV-02 — Policy migration test

Artefacts created under prior policy versions follow documented migration, compatibility and retirement rules.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-GOV-02` |
| Guardrail Patterns | `GRP-GOV-02` |
| Evidence Patterns | `EVP-GOV-02` |

### ATP-ID-01 — Role-confusion negative test

Requests with mismatched principal, subject, holder, issuer or operator roles are rejected or escalated.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-ID-01`, `CTP-ID-02` |
| Guardrail Patterns | `GRP-ID-01`, `GRP-ID-03` |
| Evidence Patterns | `EVP-AUTH-01` |

### ATP-DISC-01 — Discovery non-inference test

A signed or registered discovery record without separate authorization cannot unlock a protected action.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-DISC-01`, `CTP-DISC-03` |
| Guardrail Patterns | `GRP-AUTH-01`, `GRP-GOV-03` |
| Evidence Patterns | `EVP-AUTH-01` |

### ATP-DISC-02 — Discovery freshness test

Withdrawn or stale discovery metadata is not used beyond the documented freshness bound.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-DISC-02` |
| Evidence Patterns | `EVP-OPS-01` |

### ATP-PRV-01 — Composed disclosure review

The combined disclosure set is assessed for linkability, inference and unnecessary attributes.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-PRV-02`, `CTP-PRV-01`, `CTP-PRV-03`, `CTP-PRV-04` |
| Guardrail Patterns | `GRP-PRV-01`, `GRP-PRV-02` |
| Evidence Patterns | `EVP-PRV-01` |

### ATP-EXC-01 — Alternative-path usability test

Representatively affected legitimate participants can complete an alternative path without materially worse unjustified burden.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-EXC-01` |
| Guardrail Patterns | `GRP-EXC-01` |
| Evidence Patterns | `EVP-INCL-01` |

### ATP-AGT-01 — Agent mandate boundary test

Agent attempts outside purpose, resource, value, time or onward-delegation scope are blocked.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-AGT-01`, `CTP-AGT-02` |
| Guardrail Patterns | `GRP-AGT-01` |
| Evidence Patterns | `EVP-AUTH-02` |

### ATP-OPS-01 — Dependency outage test

Loss or staleness of a dependency triggers the documented safe degradation behavior.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-OPS-01`, `CTP-OPS-03` |
| Guardrail Patterns | `GRP-OPS-02`, `GRP-OPS-03` |
| Evidence Patterns | `EVP-OPS-01` |

### ATP-OPS-02 — Replay/idempotency test

Replayed or retried requests do not repeat a protected side effect without fresh authorization.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-OPS-02` |
| Guardrail Patterns | `GRP-OPS-01` |
| Evidence Patterns | `EVP-OPS-02` |

### ATP-RED-01 — Contestability reconstruction test

An affected party and reviewer can reconstruct the consequential decision and identify an accountable remedy path.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-RED-01`, `CTP-GOV-03` |
| Guardrail Patterns | `GRP-RED-01` |
| Evidence Patterns | `EVP-RED-01`, `EVP-AUD-01` |

### ATP-COMP-01 — Cross-spec semantic seam test

Each cross-spec fact has a named owner and is not silently substituted for another semantic fact.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-COMP-01`, `CTP-CRD-01` |
| Guardrail Patterns | `GRP-COMP-01`, `GRP-CRD-01` |
| Evidence Patterns | `EVP-COMP-01` |

### ATP-COMP-02 — Cross-spec lifecycle matrix test

Composition behavior is tested across issuance, authorization, execution, revocation, retry, migration and appeal boundaries.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-COMP-02` |
| Guardrail Patterns | `GRP-COMP-02` |
| Evidence Patterns | `EVP-COMP-01` |

### ATP-RISK-01 — Control side-effect test

Material privacy, exclusion, autonomy or political-economy side effects of a proposed mitigation are identified and dispositioned.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-RISK-01`, `CTP-ID-03` |
| Guardrail Patterns | `GRP-ID-02` |
| Evidence Patterns | `EVP-RISK-01` |

### ATP-PE-01 — Critical dependency exit test

A critical dependency has explicit control ownership, material-change monitoring, a governed response and a viable exit or substitution path.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-PE-01` |
| Guardrail Patterns | `GRP-PE-01` |
| Evidence Patterns | `EVP-GOV-01` |

### ATP-DEL-03 — Actor-lineage authority separation test

Actor or delegation lineage remains attribution evidence only; independent grant evidence, append-only integrity and context binding are tested before consequential authority is inferred.

| Field | Value |
|---|---|
| Assurance level | A3 |
| Control Patterns | `CTP-DEL-03`, `CTP-DEL-04`, `CTP-DEL-05` |
| Guardrail Patterns | `GRP-DEL-03`, `GRP-DEL-04`, `GRP-DEL-05` |
| Evidence Patterns | `EVP-DEL-01`, `EVP-DEL-02`, `EVP-OPS-02` |

## Evidence patterns

### EVP-AUTH-01 — Authorization decision trace

Shows identity/authentication inputs separately from current authorization/status evaluation.

### EVP-AUTH-02 — Authority envelope fixture

Shows enforceable scope, purpose, audience, value, time and delegation limits plus negative vectors.

### EVP-DEL-01 — Delegation chain trace

Binds principal, each delegate, authority attenuation and resulting action.

### EVP-DEL-02 — Revocation propagation trace

Shows revocation effective time and observation/enforcement time at each relevant enforcement point.

### EVP-GOV-01 — Governance decision record

Shows authority, reviewers, rationale, version, effective date and approvals for a governance decision.

### EVP-GOV-02 — Policy migration record

Shows affected versions, migration rules, compatibility tests, notifications and retirement/rollback state.

### EVP-REC-01 — Recovery ceremony evidence

Shows recovery checks, approvals, notification and replacement/invalidation events without exposing unnecessary secrets.

### EVP-OPS-01 — Dependency freshness/outage trace

Shows dependency state, freshness age, fallback path and resulting decision.

### EVP-OPS-02 — Replay/idempotency evidence

Shows duplicate identifiers, freshness checks and side-effect suppression for replay/retry vectors.

### EVP-PRV-01 — Disclosure composition analysis

Records disclosed fields/metadata, audiences, correlation surfaces and minimization rationale for the composed transaction.

### EVP-INCL-01 — Inclusive-path test record

Records representative accessibility/exclusion conditions, completion outcomes and burden comparison across alternate paths.

### EVP-RED-01 — Appeal and remedy record

Binds adverse outcome, explanation evidence, appeal owner, timeline, decision and remedy.

### EVP-AUD-01 — Consequential action audit record

Binds accountable actor, delegation/authority reference, action category, target, time and outcome without private reasoning.

### EVP-COMP-01 — Cross-spec contract test matrix

Records semantic ownership, lifecycle boundary cases, expected outcomes and tested revisions for a composition.

### EVP-RISK-01 — Control side-effect assessment

Records risks mitigated, risks introduced/amplified, affected groups and explicit disposition.

