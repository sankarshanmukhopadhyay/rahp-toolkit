---
layout: default
title: "Interpreting results"
nav_order: 6
has_toc: true
parent: Run assessments
---
# Interpreting RAHP results

A RAHP result is not a binary pass/fail statement. The v1.2 model separates **signals**, **controls**, **assurance evidence**, and the **residual conclusion** so a mature target can receive explicit control credit without unresolved evidence gaps being hidden by a green status.

| State | Meaning |
|---|---|
| `assured` | The proposition is positively supported by sufficient evidence. |
| `controlled` | A relevant risk exists, but an evidenced control and assurance test support the required outcome. |
| `finding` | Evidence supports an actionable residual defect or unsafe condition. |
| `assurance-gap` | A control/property may exist, but required assurance evidence is incomplete. |
| `review-required` | Available evidence cannot safely determine the residual state. |
| `not-assessed` | The proposition was not evaluated sufficiently. |
| `not-applicable` | The proposition is outside the applicable scope. |

**Zero findings is not equivalent to assured.** A report with `0 findings + 7 assurance-gap` records no confirmed defect, but it also records seven unresolved assurance obligations. Dashboards and downstream automation must preserve that distinction.

## Workflow state is not assurance state

A green GitHub Actions run, successful renderer, valid schema or completed RAHP workflow establishes that the configured machinery executed successfully. It does **not** establish that the proposition under review is safe, sufficient or assured. Workflow success can therefore coexist with an AMBER assurance posture when evidence is incomplete or materially uncertain.

`INDETERMINATE` is the explicit conservative outcome for a proposition that cannot be safely resolved from available evidence. It must not be silently converted to PASS merely because execution succeeded or no adverse detector fired. In portfolio presentation this remains non-green / AMBER until additional evidence or a governed disposition supports a different conclusion.

For every potential finding, ask: **What signal exists? What control is present? What evidence demonstrates the control? What residual gap remains?** Then separately ask who has authority to remediate it.
