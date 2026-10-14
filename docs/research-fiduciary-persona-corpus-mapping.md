---
layout: default
title: "Fiduciary persona to corpus mapping"
nav_order: 21
---

# Fiduciary persona to corpus mapping

Issue: #1011  
Related PR: #1015  
Status: research design note

## Purpose

This note records how the fiduciary assurance profile should relate its role-based personas to RAHP scenario-corpus personas, affected-person contexts, harms, controls, guardrails, and risks.

The implementation should not replace existing corpus persona or scenario semantics with a fiduciary-agent taxonomy. It should layer fiduciary role semantics over corpus pressure dimensions so the fixture can answer both questions:

1. who is acting, authorizing, enforcing, relying, or reviewing; and
2. who is affected, under what context, with what amplified harm.

## Core rule

Fiduciary personas and demographic or affected-context personas are orthogonal dimensions.

Use:

```text
functional fiduciary role + affected-context overlay + harm amplifier + corpus pressure dimension
```

Do not use:

```text
functional fiduciary role = demographic persona
```

For example, `beneficiary_principal` is a role in the fiduciary relationship. `older adult`, `low digital literacy`, `financially constrained`, or `assistive-technology dependent` are affected-context overlays that may change severity, required evidence, coverage, and recourse requirements. They do not replace the authority or evidence failure mechanism.

## Functional fiduciary roles

The booking-withdrawal fixture should start with a deliberately small role set.

| ID | Functional role | Assurance relevance |
|---|---|---|
| P1 | Beneficiary / principal | Person whose authority, interest, withdrawal, or reliance is central to the claim. |
| P2 | Fiduciary agent / acting system | System attempting to exercise delegated capability. |
| P3 | Workspace / policy gate | Runtime environment enforcing authority and capability limits. |
| P4 | Merchant / booking counterparty | External system that may complete the transaction. |
| P5 | Assessor / reviewer | Party or process judging whether the evidence supports the proposition. |
| P6 | Responsible operator | Entity accountable for deployment, restriction, repair, restoration, and evidence retention. |

These roles are not demographics. They are authority and responsibility positions in the assurance claim.

## Affected-context overlays

Affected-context overlays describe conditions under which a failure has different consequences, requires different evidence, or needs broader coverage.

Candidate overlays for the first fixture include:

| Overlay | Why it matters |
|---|---|
| older_adult | Reversal, explanation, and recourse burden may be materially higher. |
| low_digital_literacy | A recorded consent event may not establish meaningful understanding or control. |
| financial_constraint | A paid booking completed after withdrawal may cause disproportionate harm. |
| assistive_technology_dependent | A fallback path or inaccessible override may remove practical control. |
| caregiver_mediated | Authority, preference, and relationship state may be ambiguous or contested. |
| time_sensitive_travel | Delay or denial may itself create harm, so positive authorized execution remains important. |

The profile should use these overlays only when they change the assurance question. They should not be added merely for demographic completeness.

## Harm-amplifier model

A harm amplifier records how an affected context changes the consequences of the same underlying control failure.

| Failure mechanism | Affected-context overlay | Harm amplification |
|---|---|---|
| Booking after withdrawal | financial_constraint | Higher impact from unauthorized charge or cancellation penalty. |
| Consent log treated as meaningful control | low_digital_literacy | Consent evidence may not establish comprehension or free choice. |
| Gate denial but external booking completed | older_adult | Higher recourse and reversal burden. |
| Fallback path bypasses policy gate | assistive_technology_dependent | Accessible control path may be bypassed or unavailable. |
| Prior caregiver grant reused after relationship change | caregiver_mediated | Relationship-state evidence may be stale or conflicted. |

The same functional failure can therefore produce different severity, coverage, and evidence requirements without changing the core risk hypothesis.

## Mapping to corpus pressure dimensions

The fixture should map fiduciary scenarios to existing corpus pressure dimensions rather than inventing a separate coverage model.

| Fiduciary fixture concern | Corpus pressure dimension |
|---|---|
| Permission withdrawal before execution | lifecycle / current state |
| Historical approval reused as current authority | replay / freshness |
| Agent acts beyond withdrawn or narrowed authority | delegation / constrained authority |
| Booking path bypasses gate | approval / threshold; control enforcement |
| Missing evidence of external booking outcome | evidence closure |
| User cannot reverse the booking | redress / adverse decisions |
| Booking metadata shared after withdrawal | privacy / correlation |
| Relationship or caregiver authority changes | suspension / restoration; relationship state |
| Prior successful test reused after configuration change | evidence applicability / reassessment trigger |

This preserves RAHP's existing corpus discipline: source or profile scenarios broaden pressure coverage; they do not by themselves establish assurance.

## Suggested record shape

The implementation can use a compact record shape like this in a profile fixture or research example:

```yaml
persona_contexts:
  - id: PC-FID-001
    functional_persona: beneficiary_principal
    affected_context:
      - low_digital_literacy
      - financial_constraint
    harm_amplifiers:
      - invalid_consent_inference
      - disproportionate_financial_loss
      - increased_recourse_burden
    corpus_pressure_dimensions:
      - lifecycle_current_state
      - replay_freshness
      - redress_adverse_decisions
    evidence_implications:
      - consent_log_alone_is_insufficient_for_meaningful_control
      - withdrawal_record_must_be_bound_to_execution_time
      - external_booking_outcome_must_be observed_or_indeterminate
```

The exact field names should follow existing RAHP schema conventions when implemented. This note is conceptual, not a schema change.

## Scenario design implication

A single core booking-withdrawal scenario can be specialized into affected-context variants without duplicating the underlying risk model.

Example:

| Scenario variant | Functional persona | Overlay | Expected assurance impact |
|---|---|---|---|
| Valid booking with current authority | beneficiary_principal | time_sensitive_travel | Positive case remains necessary; controls must not over-block valid action. |
| Withdrawal before execution | beneficiary_principal | financial_constraint | Unauthorized completion is higher severity. |
| Prior consent reused after withdrawal | beneficiary_principal | low_digital_literacy | Consent evidence must not be over-read as meaningful current control. |
| Fallback path after gate denial | beneficiary_principal | assistive_technology_dependent | Coverage must include accessible and fallback execution paths. |
| Caregiver approval reused after relationship change | beneficiary_principal | caregiver_mediated | Relationship-state freshness becomes mandatory. |

## Controls and guardrails impact

Affected-context overlays can change required evidence and severity, but they should not weaken guardrails.

The following guardrails remain invariant:

1. unknown current authority must not authorize execution;
2. withdrawal dominates cached permission for future execution;
3. fallback paths must not bypass authority checks;
4. missing evidence must not become PASS;
5. stale evidence must not become PASS;
6. technical consent logging must not become proof of meaningful human control;
7. recorded operational disposition requires deployed enforcement evidence.

Affected context may add controls, such as accessible withdrawal, confirmation, notice, cancellation support, or assisted redress. It must not convert an authority failure into a demographic-only issue.

## Implementation recommendation

For the next executable tranche, represent the mapping as profile-local fixture metadata first. Do not promote any affected-context vocabulary into portable RAHP method until at least two independent profiles demonstrate that the same overlay semantics are reusable.

Initial implementation surface:

```text
.rahp/reviews/fiduciary-booking-withdrawal/
```

Candidate fixture records:

```text
personas.yaml
persona-contexts.yaml
scenarios.yaml
risks.yaml
controls.yaml
guardrails.yaml
evidence-manifest.yaml
expected-results.yaml
```

If current validators do not support a distinct `persona-contexts.yaml` concept, the first tranche should either encode the information in existing scenario/persona fields or record the incompatibility as a research finding. It should not change core schemas prematurely.

## Decision rule

A demographic or affected-context overlay is justified only when it changes at least one of:

- severity;
- evidence required;
- coverage required;
- recourse requirements;
- retest trigger;
- operational disposition.

Otherwise it is descriptive only and should not be added to the executable fixture.

## Conclusion

The persona mapping is feasible and strategically useful if it remains two-dimensional. The fiduciary role model tells RAHP who holds authority, who acts, who enforces, and who reviews. The corpus or demographic overlay tells RAHP who bears differentiated harm and what coverage or evidence is needed to avoid false assurance.

The implementation should therefore preserve the following invariant:

```text
role determines authority semantics; affected context determines harm amplification and evidence/coverage obligations.
```
