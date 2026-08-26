# RAHP → DPIP assurance handoff

RAHP may recommend a DPIP examination when a monitored change plausibly affects a composed privacy property. The handoff is deliberately conservative: RAHP identifies a risk hypothesis and an examination question; DPIP determines applicability and the privacy result.

## Roles

The Portfolio Monitor answers **what changed**. RAHP answers **what could go wrong**. DPIP answers **what privacy property the composed implementation actually preserves**. The specification or implementation owner decides **what should change**.

RAHP MUST NOT infer a DPIP `PASS`, `FAIL`, `CONSTRAINED`, or `INDETERMINATE` result. A privacy-relevant RAHP finding is a request for examination, not a conformance conclusion.

## Lifecycle

RAHP uses the following labels as a state machine:

- `assurance:dpip-candidate` — the finding may affect a DPIP privacy property but has not passed the promotion gate;
- `assurance:dpip-requested` — the promotion gate is satisfied and a DPIP examination has been requested;
- `assurance:dpip-open` — the corresponding DPIP issue exists and is being examined;
- `assurance:dpip-complete` — DPIP has returned a disposition.

A finding SHOULD move through these states rather than accumulating all lifecycle labels indefinitely. During the manual validation phase `requested` and `open` may briefly coexist to preserve the transition in GitHub history.

## Promotion gate

A candidate is promoted only when all three conditions are satisfied:

1. **Specific source change** — a concrete monitored change is identified, preferably with an immutable commit/release and Portfolio Monitor finding/fingerprint.
2. **Specific DPIP target** — at least one interaction, reference flow, invariant, claim, requirement, test, or correlation surface is identified with enough specificity for DPIP triage.
3. **Actionable examination question** — the handoff asks what DPIP should determine, rather than merely stating that the change is privacy-relevant.

If any condition is missing, the issue remains `assurance:dpip-candidate`. Candidate status alone MUST NOT create a DPIP issue.

## Handoff payload

The RAHP issue SHOULD contain a machine-readable block of this form:

```yaml
dpip:
  recommendation: examine
  affected_interactions: [C3]
  affected_reference_flows: [RF-001]
  affected_invariants: [P2, P4]
  affected_claims: [C3-PC-2]
  suspected_surfaces: [identity, protocol-envelope]
  source_change:
    monitor_finding_id: <finding-id>
    monitor_fingerprint: <fingerprint>
    repository: owner/repository
    revision: <immutable-revision>
    pull_request: <number-or-null>
  question: >-
    A specific question that DPIP can answer from its existing interactions,
    reference flows, tests, or a bounded new examination.
```

Fields may be omitted when genuinely unknown, but the promotion gate still requires a sufficiently specific target and question.

## Provenance and deduplication

The preferred handoff identity is:

```text
Monitor fingerprint + source repository + immutable source revision + DPIP examination question/target
```

Before creating a DPIP issue, RAHP SHOULD search for an existing open or completed handoff with the same Monitor fingerprint and materially equivalent DPIP target. Repeated Monitor observations of the same logical change MUST NOT create duplicate DPIP issues.

A successor source revision may reopen examination only when it materially changes the evidence relevant to the DPIP question. Routine re-observation, report regeneration, or a new Monitor collection date is not sufficient.

## DPIP applicability outcomes

`NOT_APPLICABLE` is a handoff disposition, not a DPIP conformance status. It means the referral was reasonable but the changed artifact does not alter an evaluated DPIP privacy property in the stated scope.

`INDETERMINATE` is a valid DPIP result where required implementation, construction, deployment, or upstream semantic evidence is unavailable. An `INDETERMINATE` conclusion MUST NOT cause automatic weekly re-referral. Re-examination requires new material evidence or a changed source revision.

## Return contract

When DPIP completes the examination, RAHP receives a concise disposition block:

```yaml
dpip_disposition:
  dpip_issue: <number>
  applicability: applicable | not-applicable
  conclusion: PASS | FAIL | CONSTRAINED | INDETERMINATE | NOT_APPLICABLE
  affected_interactions: [C3]
  affected_reference_flows: [RF-001]
  affected_claims: [C3-PC-2]
  evidence_summary: >-
    Short statement of what the evidence establishes and what it does not.
  residual_correlation: >-
    Remaining correlation relevant to the scoped privacy claim.
  action: none | dpip-regression | upstream-clarification | upstream-defect | accepted-limitation | evidence-gap | implementation-specific
```

The RAHP issue SHOULD link to the DPIP issue and retain only the concise disposition; the DPIP issue remains the technical record.

## Manual validation before automation

Automation is gated on three materially different successful handoffs:

1. a change that genuinely requires DPIP examination;
2. a reasonable candidate that DPIP determines is `NOT_APPLICABLE`;
3. an applicable referral that concludes `INDETERMINATE` because evidence is missing.

The validation set must demonstrate deduplication, idempotent re-observation, clean lifecycle transitions, and a successful DPIP → RAHP return path before automated issue creation is enabled.

## Scheduling principle

Portfolio collection and RAHP triage should operate conservatively, preferably on a weekly logical-change-set basis. The unit of assurance is the consolidated semantic change, not each commit or transient repository event. DPIP examination is event-driven only after the promotion gate is satisfied.
