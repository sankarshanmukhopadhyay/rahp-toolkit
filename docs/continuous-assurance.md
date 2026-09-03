---
layout: default
title: "Continuous assurance"
nav_order: 7
has_toc: true
parent: Learn RAHP
---
# Continuous assurance

RAHP does not treat an assessment as a timeless verdict. Continuous governed assurance preserves what was assessed, what changed, which evidence still carries weight, what must be retested and which authority may disposition resulting obligations.

This page is a map of that lifecycle. The detailed contracts remain in their dedicated pages.

## Lifecycle

```text
material target change
  → impact selection
  → evidence freshness evaluation
  → retained / weakened / invalidated evidence
  → focused reassessment
  → specialist routing when applicable
  → RAHP reconciliation
  → PASS | FAIL | NOT_APPLICABLE | INDETERMINATE
  → durable residual/action
  → citable terminal assurance record
  → separately governed disposition / publication when required
  → current assurance posture
```

The controller owns supported lifecycle transitions and terminalization. Governance authority remains separate: producing a terminal assurance record does not itself authorize publication, risk acceptance, closure or other governed action.

The purpose is to avoid two opposite failures: rerunning everything after every change, or allowing old assurance claims to survive after their evidence has become stale.

## Assurance outcomes and residual states

RAHP's current controller outcomes are evidence-conservative:

| Outcome | Meaning |
|---|---|
| `PASS` | The assessed proposition is supported within the recorded scope and evidence boundary. |
| `FAIL` | Evidence supports a material adverse finding or failed proposition. |
| `NOT_APPLICABLE` | The proposition or specialist path does not apply to the assessed subject/scope. |
| `INDETERMINATE/evidence-required` | The required evidence is absent or insufficient; missing evidence never becomes PASS. |
| `INDETERMINATE/model-gap` | The current model cannot safely classify or resolve the observed surface. |

Deployment posture may additionally describe retained conditions such as findings, controlled risks, evidence gaps, remediation obligations or unassessed surfaces. Those posture labels are projections over evidence and terminal records, not substitutes for the controller's canonical terminal outcome.

**Zero findings is not equivalent to assured.** A successful workflow is likewise not an assurance conclusion. Workflow execution may be green while the terminal assurance record is adverse or indeterminate. `INDETERMINATE` is never silently converted to PASS. See [Assurance evaluation](assurance-evaluation.md) and [Interpreting results](interpreting-results.md).

## 1. Determine what changed

The assurance graph connects targets, evidence, controls and conclusions so a material change can select the propositions that require review rather than forcing a full restart.

See [Assurance graph and impact analysis](assurance-graph-impact.md).

## 2. Re-evaluate evidence

Evidence can remain current, become weaker, become invalid, or require further examination. Provenance and freshness are explicit so a later assessment does not silently reuse an obsolete source.

See [Evidence provenance and freshness](evidence-freshness-delta.md) and [Evidence classification](evidence-classification.md).

## 3. Preserve assessment lineage

A reassessment should preserve the prior record and state the delta. Findings may be retained, refined, weakened, resolved or superseded depending on current evidence. Replay of the same immutable source pin remains idempotent; a new pin creates a new reassessment identity with lineage.

See [Assurance lineage](assurance-lineage.md) and [Review evidence and retention](evidence-retention.md).

## 4. Remediate and retest

Remediation is not closure. RAHP records the proposed or implemented change, the evidence needed to test it, the retest result and the remaining residual obligation.

See [Remediation and retesting](remediation-lifecycle.md).

## 5. Keep policy separate from authority

A policy or assurance evaluation can return a determinate or indeterminate result. That result does not itself authorize publication, risk acceptance or closure. Authority is independently scoped to actions such as `observe`, `assess`, `disposition`, `remediate`, `publish`, `accept-risk`, `close` and `reopen`. Repository permissions are not automatically governance authority.

This separation does **not** introduce a human-only controller transition. The controller can reach a citable terminal assurance state without operator lifecycle shepherding; a later governed business or governance action may still require an authorized actor.

See [Authority and policy gates](authority-policy-gates.md).

## 6. Publish current posture

Assurance posture presents the current state without hiding uncertainty behind a synthetic percentage. It can distinguish confirmed findings from evidence gaps, remediation obligations, controlled risks and unassessed surfaces.

See [Assurance posture](assurance-posture.md).

## Operational example

The deployment-neutral posture fixture can be rendered with:

```bash
python3 tools/assurance_posture.py \
  --input examples/assurance-lineage/generic-posture-input.yaml \
  --generated-at 2026-08-22T00:00:00Z \
  --json
```

## How this relates to one-time pressure testing

A normal pressure test answers what the evidence supports at a pinned target revision. Continuous assurance adds the machinery for what happens **afterward**:

- target changes;
- source corpora are re-baselined;
- controls are implemented;
- evidence expires or becomes unavailable;
- findings are challenged;
- remediation is completed; or
- a governance authority changes the disposition.

The original evidence remains part of lineage; the current posture is a new evidence-backed state, not a rewritten history.
