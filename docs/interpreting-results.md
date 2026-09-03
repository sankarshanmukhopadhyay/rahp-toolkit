---
layout: default
title: "Interpreting results"
nav_order: 6
has_toc: true
parent: Run assessments
---
# Interpreting RAHP results

RAHP exposes more than one result layer. Do not collapse them into a single green/red score.

At the controller boundary, a supported autonomous assurance run terminates with a defined outcome such as `PASS`, `FAIL`, `NOT_APPLICABLE`, `INDETERMINATE/evidence-required`, `INDETERMINATE/model-gap`, an upstream-action state, or a defined controller/contract error state. Those outcomes describe the terminal state of the assessed proposition within its recorded subject, scope and evidence boundary.

Within an assessment, the portable assurance-evaluation object can preserve richer residual reasoning such as `assured`, `controlled`, `finding`, `assurance-gap`, `review-required`, `not-assessed`, and `not-applicable`. These residual states describe evidence and control conditions; they are not a competing controller state machine.

| Evaluation residual | Meaning |
|---|---|
| `assured` | The proposition is positively supported by sufficient evidence. |
| `controlled` | A relevant risk exists, but an evidenced control and assurance test support the required outcome. |
| `finding` | Evidence supports an actionable residual defect or unsafe condition. |
| `assurance-gap` | A control/property may exist, but required assurance evidence is incomplete. |
| `review-required` | Available evidence cannot safely determine the residual evaluation state. |
| `not-assessed` | The proposition was not evaluated sufficiently. |
| `not-applicable` | The proposition is outside the applicable scope. |

**Zero findings is not equivalent to assured.** A report with `0 findings + 7 assurance-gap` records no confirmed defect, but it also records seven unresolved assurance obligations. Dashboards and downstream automation must preserve that distinction.

## Workflow state is not assurance state

A green GitHub Actions run, successful renderer, valid schema or completed CLI command establishes that configured machinery executed successfully. It does **not** establish that the proposition under review is safe, sufficient or assured.

For autonomous controller flows, execution success must be read together with the terminal assurance record. A successful workflow can legitimately carry `FAIL` or `INDETERMINATE`; deterministic attributable termination is the operational success property, not universal PASS/GREEN.

`INDETERMINATE` is the explicit conservative outcome when the proposition cannot be safely resolved from available evidence or the current model. It must not be silently converted to PASS merely because execution succeeded or no adverse detector fired.

## Keep posture separate too

A portfolio or deployment may project current evidence into presentation states such as GREEN/AMBER/RED or into retained conditions such as controlled risk, evidence gap or remediation obligation. Those presentation states are useful summaries, but the citable terminal record and underlying evidence remain authoritative for what was actually assessed.

For every potential finding, ask: **What signal exists? What control is present? What evidence demonstrates the control? What residual gap remains?** Then separately ask what the controller concluded and who has authority to remediate, disposition, publish or accept risk.

See [Assurance evaluation](assurance-evaluation.md), [Continuous assurance](continuous-assurance.md), and [Authority and policy gates](authority-policy-gates.md).
