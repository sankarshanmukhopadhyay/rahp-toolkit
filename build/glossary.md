# RAHP glossary

RAHP terms in simple English. The authoritative source is `method/glossary/terms/`.

## Adapter

A mapping that brings a source system or specification into RAHP's scenario and assessment vocabulary without replacing the source's authority.

**Example:** A Trust Tasks adapter maps selected source pressures to RAHP patterns.

**See also:** scenario-corpus, provenance

## Agent

A software or human actor that takes actions for itself or for another principal.

**Example:** A software agent requests a credential presentation on behalf of its user.

**See also:** principal, mandate, delegation

## Applicability

The conditions under which a risk, control, guardrail or test is relevant.

**Example:** A cross-context privacy guardrail applies only when correlation is not necessary for the declared purpose.

**See also:** scope, guardrail-requirement

## Assurance

Reasoned confidence, supported by evidence, that a system or control behaves as claimed.

**Example:** A replay test and its retained trace support confidence that duplicate execution is blocked.

**See also:** assurance-pattern, evidence

## Assurance level

A label for how strong the assurance evidence is, from basic inspection to stronger independent or automated evidence.

**Example:** A2 may require repeatable tests while A0 may only record that no assurance has been shown.

**See also:** assurance, evidence

## Assurance pattern

A reusable testable claim about a control or guardrail, including how to test it and what evidence to keep.

**Example:** Try a revoked delegation and confirm the action is blocked.

**See also:** assurance, evidence-pattern, control-pattern

## Audience

The party or set of parties for whom a message, credential, proof or authority grant is intended.

**Example:** A proof created for one verifier should not automatically be reused by another.

**See also:** purpose, context-binding

## Audit event

A recorded event that shows a control, guardrail, decision or override was evaluated or used.

**Example:** The log records that authority was checked and that an override was rejected.

**See also:** evidence, auditability

## Auditability

The ability to reconstruct what happened, which rules were used, who acted and what evidence supported the result.

**Example:** An investigator can trace a delegated action back to the principal and active mandate.

**See also:** audit-event, evidence, provenance

## Authentication

A process that establishes which actor, account, key or system is presenting itself.

**Example:** A signature verifies that a message came from a known key.

**See also:** authority, authorization

## Authority

The legitimate power to make a decision, request an action or change governed state.

**Example:** A valid signature proves who signed; it does not by itself prove that the signer had authority to approve payment.

**See also:** authentication, authorization, delegation

## Authorization

A decision about whether an actor is allowed to perform a particular action in a particular context.

**Example:** An authenticated agent may still be denied permission to transfer funds.

**See also:** authentication, authority, scope

## Composed corpus

A collection of scenarios about interactions between two or more systems or specifications. Its provenance and conclusions must be assessed for the composition.

**Example:** A credential and task scenario can test a failure that neither component shows alone.

**See also:** scenario-corpus, composition-boundary

## Composition boundary

The point where one specification, protocol or system relies on facts produced by another.

**Example:** A task engine accepts a credential status result from a separate credential system.

**See also:** cross-spec-composition, enforcement-point

## Consequential action

An action that can materially affect rights, money, access, safety, authority, privacy or an external system state.

**Example:** Revoking access, transferring money or publishing a credential are consequential actions.

**See also:** decision-boundary, authority

## Contestability

The ability to understand, challenge and seek correction or remedy for a consequential outcome.

**Example:** A person can see why access was denied and submit evidence for review.

**See also:** redress, evidence

## Context binding

A rule that ties evidence, authority or a credential to the task, transaction, audience or purpose where it is meant to be used.

**Example:** A witness credential names the trust task that produced it.

**See also:** purpose, audience

## Control

A deployment-specific measure used to reduce, detect, contain or recover from a risk.

**Example:** A verifier checks status immediately before approving a transaction.

**See also:** control-pattern, guardrail

## Control pattern

A reusable control objective that deployments can apply in their own way.

**Example:** Check current authority at the action boundary.

**See also:** control, risk-pattern, assurance-pattern

## Control side effect

A new risk or harm introduced or made worse by a control that was meant to reduce another risk.

**Example:** Extra identity checks reduce fraud but may increase exclusion or surveillance.

**See also:** control, risk-pattern

## Cross-spec composition

The combined behavior that appears when two or more specifications or protocols are used together.

**Example:** A credential can be valid under one specification but stale under the lifecycle rules of another.

**See also:** composition-boundary, lifecycle

## Decision boundary

The point where a system changes from gathering information to making or executing a consequential decision.

**Example:** The final approval step before an account is disabled is a decision boundary.

**See also:** enforcement-point, consequential-action

## Delegation

A grant of bounded authority from one actor to another.

**Example:** A person allows an agent to book one hotel within a price limit.

**See also:** authority, scope, revocation

## Enforcement point

The place in a system where a control or guardrail is actually checked and can stop, change or allow an action.

**Example:** A verifier checks current authorization just before it calls the payment API.

**See also:** control, guardrail, decision-boundary

## Evidence

Information kept to support or challenge an assurance claim, decision or finding.

**Example:** A signed authorization decision record shows what policy and authority were used.

**See also:** evidence-pattern, audit-event

## Evidence grade

A corpus label describing how its scenarios are grounded in source material, not whether an implementation is safe or has passed tests.

**Example:** A source-informed corpus can suggest useful tests without proving conformance.

**See also:** scenario-corpus, evidence

## Evidence pattern

A reusable description of what evidence should be produced, who produces it, how fresh it must be and when it becomes invalid.

**Example:** A revocation propagation trace records when each enforcement point learned about a revocation.

**See also:** evidence, assurance-pattern

## Fail closed

To stop or refuse a consequential action when a required safety or assurance condition cannot be established.

**Example:** If current revocation status cannot be checked, the verifier defers the high-impact action.

**See also:** fail-open, guardrail

## Fail open

To continue an action even though a check or dependency failed. This must be explicit when it can create risk.

**Example:** A low-impact read may use a short cached value during a network outage.

**See also:** fail-closed, risk-acceptance

## Finding

A specific observation from a pressure test or security review that needs attention or a recorded disposition.

**Example:** The specification does not say how a user can challenge an adverse decision.

**See also:** risk, recommendation, finding-disposition

## Finding disposition

The recorded outcome for an earlier finding, such as unchanged, weakened, resolved or superseded.

**Example:** A new normative replay rule changes a replay finding from open to resolved.

**See also:** finding, reassessment

## Freshness

How recent information or evidence must be for a decision to rely on it.

**Example:** A high-impact action may require status checked within the last minute.

**See also:** lifecycle, stale-state

## Guardrail

A rule that blocks or stops an unacceptable state. It is stronger than normal guidance.

**Example:** Do not let a consequential action proceed when current authority cannot be established.

**See also:** control, prohibited-state, fail-closed

## Guardrail pattern

A reusable guardrail that describes what must not be allowed, where it is enforced and what happens on failure.

**Example:** Do not treat a valid credential as permission for an unrelated action.

**See also:** guardrail, risk-pattern, assurance-pattern

## Guardrail requirement

The catalogue decision that says whether a risk needs a guardrail, needs one only in some conditions, or is adequately handled by controls.

**Example:** A privacy risk may need a guardrail only when cross-context correlation is not necessary.

**See also:** guardrail, applicability

## Harm

A bad effect on a person, group, organization or public interest.

**Example:** A person is wrongly locked out of an essential service.

**See also:** risk, harm-pattern

## Harm pattern

A reusable description of a kind of harm that can appear in many systems.

**Example:** Wrongful exclusion can happen in identity, payment or registry systems.

**See also:** harm, risk-pattern

## Lifecycle

The states an artefact, authority or policy moves through from creation to retirement or invalidation.

**Example:** A credential can be issued, active, suspended, revoked and expired.

**See also:** revocation, suspension, freshness

## Mandate

The purpose and limits under which an actor or agent is expected to act for a principal.

**Example:** An agent may compare travel options but may not buy one without approval.

**See also:** delegation, principal, scope

## Override

A governed exception that allows a normal control or guardrail outcome to be changed by an authorized actor.

**Example:** An emergency override may be allowed only to a named governance role and must be logged.

**See also:** override-authority, audit-event

## Override authority

The role or actor that is allowed to approve an override.

**Example:** Only the incident commander may approve an emergency continuity override.

**See also:** override, authority

## P0 priority

A high-priority scenario pressure to examine first. P0 is not a measurement of incident severity or probability.

**Example:** Recipient-binding replay is marked P0 for early attention.

**See also:** scenario, risk

## P1 priority

A secondary-priority scenario pressure. P1 is not a statement that harm is impossible or that a system is safe.

**Example:** A less immediate interoperability question may be marked P1.

**See also:** scenario, risk

## Principal

The person or organization whose authority, interests or instructions an agent or delegate is expected to serve.

**Example:** A traveller is the principal when a personal agent books on the traveller’s behalf.

**See also:** agent, delegation, mandate

## Prohibited state

A system state that a guardrail says must not be entered or continued.

**Example:** A payment proceeds even though required authority cannot be established.

**See also:** guardrail, protected-interest

## Protected interest

The person, group or institutional interest that a guardrail is meant to protect.

**Example:** Privacy is the protected interest behind a guardrail against unnecessary disclosure.

**See also:** guardrail, harm

## Provenance

Information about where an artefact, action, decision or claim came from and how it changed over time.

**Example:** A delegation trace shows which principal granted which delegate which scope.

**See also:** auditability, delegation

## Purpose

The stated reason for collecting information, making a decision or performing an action.

**Example:** A credential is requested to confirm age, not to build a marketing profile.

**See also:** scope, audience, context-binding

## Reassessment

A new review performed because the target, evidence, threat model or operating context has changed.

**Example:** A specification changes its revocation rules, so earlier findings are checked again.

**See also:** retest-condition, finding-disposition

## Recommendation

A proposed action to reduce a finding or risk.

**Example:** Require a fresh authority check immediately before a destructive action.

**See also:** finding, control

## Redress

A process that can correct, compensate for or otherwise remedy a harmful or incorrect outcome.

**Example:** A wrongly excluded user can appeal and have access restored.

**See also:** contestability, remedy

## Remedy

The action taken to correct or reduce the effect of a harmful or incorrect outcome.

**Example:** A registry corrects an entry and notifies affected relying parties.

**See also:** redress, contestability

## Residual risk

The risk that remains after controls and guardrails are applied.

**Example:** A cached status check lowers outage risk but still leaves a short stale-state window.

**See also:** risk, risk-acceptance

## Retest condition

A stated event that should cause an earlier assurance result or finding to be checked again.

**Example:** Retest when the specification changes its authorization model.

**See also:** reassessment, assurance

## Revocation

A governed act that ends previously granted authority, status or validity.

**Example:** A principal revokes an agent’s authority to make purchases.

**See also:** suspension, delegation, authority

## Risk

A possible way a specific deployment can cause harm or fail to meet its goals.

**Example:** A registry may keep an old key after it should have been removed.

**See also:** risk-pattern, finding

## Risk acceptance

A governed decision to live with a known residual risk for a stated period and reason.

**Example:** A deployment accepts a low-impact availability risk until a replacement service is ready.

**See also:** residual-risk, reassessment

## Risk pattern

A reusable failure mechanism that can appear in more than one deployment or specification.

**Example:** A system may mistake proof of identity for permission to act.

**See also:** risk, harm-pattern, control-pattern

## Scenario

A situation or condition used to ask what a system should do under pressure. A scenario is not evidence that a failure happened.

**Example:** A signed request might reach the wrong recipient.

**See also:** risk, finding

## Scenario corpus

A collection of domain-specific scenarios linked to reusable scenario patterns. A corpus suggests what to test, not what passed.

**Example:** The Trust Tasks corpus lists possible failure situations for task workflows.

**See also:** scenario, scenario-pattern

## Scenario pattern

A reusable kind of pressure or failure possibility that can be tested in many systems.

**Example:** Replay of a valid proof is a pattern that may appear in several corpora.

**See also:** scenario, risk-pattern

## Scenario-baseline

An evidence grade for a working pressure-test hypothesis where a source-grounded normative claim has not been established.

**Example:** A preliminary interface receives a scenario to explore before its specification is complete.

**See also:** evidence-grade, scenario

## Scope

The boundary of what an authority, control, assessment or claim applies to.

**Example:** A delegation may allow read access to one record for one hour.

**See also:** authority, applicability, purpose

## Source pin

A declared source revision used when preparing an adapter. A symbolic or descriptive value is not an immutable commit identifier.

**Example:** A full commit SHA can identify the revision of a specification used for review.

**See also:** provenance, evidence

## Source-informed

An evidence grade used when scenarios draw on known source semantics without claiming a complete pinned normative baseline.

**Example:** A scenario is based on published design concepts but not a complete frozen text.

**See also:** evidence-grade, source-pin

## Source-pinned

An evidence grade used when an adapter declares reviewable grounding in pinned source material. It does not certify the target.

**Example:** A scenario cites a checked specification revision, but still needs execution evidence.

**See also:** evidence-grade, source-pin

## Stale state

Old information that no longer reflects the current authority, status, policy or system condition.

**Example:** A cached registry entry still points to a key that has been revoked.

**See also:** freshness, revocation

## Suspension

A governed temporary stop that may later be lifted without creating a new grant from scratch.

**Example:** A credential is suspended during an investigation and later restored.

**See also:** revocation, lifecycle

