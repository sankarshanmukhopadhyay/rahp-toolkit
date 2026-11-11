---
layout: default
title: "Issue queue disposition"
parent: Implement RAHP
nav_order: 12
---
# Issue queue disposition and assurance-obligation ownership

This guide governs human triage of RAHP Toolkit issues. It introduces no scheduled automation, new GitHub Actions workflow, external authority, or new assurance terminal state. GitHub issues and pull requests remain the authoritative work records; source repositories remain authoritative for their own normative and implementation claims. Derived queue views must not override either.

## Classify the obligation before deciding disposition

A queue item may be one of the following. These are **planning classes**, not new engine states or obligatory labels:

| Class | Work | Completion evidence |
| --- | --- | --- |
| Bounded execution | A defined implementation, test, or examination | Affected acceptance criteria, reproducible tests, and review |
| Independent judgment | Human, security, governance, or methodological acceptance | Named review decision and review target/evidence |
| Research | Test a bounded proposition without presuming productisation | Source-qualified study and explicit continue/stop/graduation decision |
| External remediation | An identified source-system or upstream defect | Authoritative change and corresponding reassessment, not RAHP code alone |
| Evidence acquisition | Missing, stale, or inadequate observation | Evidence matching the stated contract and provenance class |
| Coordination | Reconcile distinct records and triggers | Accepted ownership transfers or distinct retained responsibilities |

Assessment completion is separate from remediation completion. A completed source-pinned assessment may legitimately leave an open residual. Do not turn a source-review PASS into runtime or composition PASS; do not turn `INDETERMINATE`, unavailable, unknown, missing, stale or contradictory evidence into success.

## Triage decision contract

Before an issue is labelled executable or closed, check:

1. **Authority and proposition.** Identify the exact claim, affected canonical source/revision, and what RAHP does and does not own.
2. **Current evidence.** Inspect issue history, latest default-branch implementation, relevant merged/open PRs, affected test evidence, upstream state, and fresh contradictory evidence. Earlier comments are historical snapshots.
3. **Uniqueness.** Identify whether the issue is the durable obligation owner, an informative coordinator, or a historical trigger. A shared topic is not proof of duplicate obligations.
4. **Execution prerequisites.** Record a positively established runnable path, or name the external provider/authority, evidence artifact, and reassessment trigger. `open` does not imply `ready`.
5. **Closure and retained risk.** Identify whether all issue-specific acceptance conditions are met; distinguish engineering delivery, independent qualification, runtime reproduction and upstream adoption.
6. **Adversarial check.** For consequential claims, attempt to falsify a purported success through wrong or revoked authority, stale/replayed input, partial failure, missing evidence, incorrect source pin, or an actual consumer path.

Use an existing issue's body/last decision record for durable qualification. Add a comment only if it supplies new evidence, reconciles a materially wrong state, or records a meaningful decision.

## GitHub dispositions

- **Close as completed** only where the issue's actual proposition and acceptance criteria are supported by attributable evidence. Link the exact PR/commit/CI run or decision record. A success in an adjacent component does not establish closure.
- **Close as not planned or duplicate** only where a distinct obligation no longer exists, recording the surviving authoritative owner and why continuity is preserved. Never close an external risk just to reduce queue count.
- **Keep open, executable** only with an unblocked, bounded task and testable acceptance criteria.
- **Keep open, external evidence/remediation** with the exact source authority, required artifact/provenance, observation date, and material reassessment trigger. Do not post periodic no-change comments.
- **Keep open, judgment required** when independent human approval, security qualification, or a normative decision is genuinely necessary. AI-assisted self-review is not independent approval.
- **Keep experimental** when the research branch is not qualified for stable integration. A draft PR is not evidence of a graduation decision.

Prefer existing labels (`assessment-complete`, `evidence-required`, `state:waiting-external`, `reassessment-pending-upstream`, `remediation-required`, `research`, `experimental`, `upstream-watch`, etc.) only where their meaning is supported by the actual record. Do not apply `assessment-complete` to an unperformed assessment; do not infer readiness from absence of a blocking label. When multiple states describe independent dimensions, retain them distinctly.

## Reassessment and freshness

A material source revision, authoritative disposition, attributable new consuming-path observation, independent review, or proven regression may trigger reassessment. A dependency's closure, timestamp movement, release name, passing CI, or periodic scan alone does not establish the underlying assurance proposition. Preserve source pins and historical reports. Re-evaluate only affected propositions; explicitly mark older derived conclusions stale when their authoritative basis changes.

For DPIP referrals, keep canonical privacy obligations distinct by proposition and evidence contract. External producer fixtures and synthetic composition traces cannot silently become observations of the original deployment. For cross-repository work, use typed references and make non-implications explicit. The coordinator's closure must not close a specialist residual.

## Review output

A bounded queue pass should report: date and repository baseline; items inspected; issues closed with state reason and evidence; issues retained with authority/dependency and next trigger; implementation/PR status; missing evidence; and release impact. Absence of a justified closure is a valid outcome. Do not create an issue, PR, workflow, new schema, or release merely to document a completed sweep.

## Publication and contribution

Issue governance changes should follow the repository's current contribution and DCO policies. They require proportionate review; new or changed GitHub Actions workflows require separate maintainer discussion and authorization. A queue-documentation-only change does not warrant a release unless current release policy or consumers rely on a versioned documentation baseline.
