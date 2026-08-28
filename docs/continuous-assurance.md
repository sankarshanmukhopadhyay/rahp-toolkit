---
layout: default
title: "Continuous assurance"
nav_order: 7
has_toc: true
parent: Learn RAHP
---
# Continuous assurance

RAHP does not treat an assessment as a timeless verdict. Continuous governed assurance preserves what was assessed, what changed, which evidence still carries weight, what must be retested and who is authorized to disposition the result.

This page is a map of that lifecycle. The detailed contracts remain in their dedicated pages.

## Lifecycle

```text
material target change
  → impact selection
  → evidence freshness evaluation
  → retained / weakened / invalidated evidence
  → focused assessment or retest
  → assurance delta
  → residual obligation + remediation
  → policy gate: PASS | FAIL | INDETERMINATE
  → independent authority verification
  → governed disposition / publication
  → current assurance posture
```

The purpose is to avoid two opposite failures: rerunning everything after every change, or allowing old assurance claims to survive after their evidence has become stale.

## Assurance states

RAHP uses normalized residual states rather than a single assurance score:

| State | Meaning |
|---|---|
| `assured` | Required propositions are supported by sufficient evidence. |
| `controlled` | The risk exists, but effective controls and assurance evidence are present. |
| `finding` | Evidence supports an actionable residual defect. |
| `assurance-gap` | The property/control may exist, but evidence is incomplete. |
| `review-required` | Automation cannot safely determine the conclusion. |
| `not-assessed` | The proposition was not sufficiently evaluated. |
| `not-applicable` | The proposition is outside applicable scope. |

**Zero findings is not equivalent to assured.** A successful workflow is likewise not an assurance conclusion: execution may be green while the current posture remains AMBER because evidence is incomplete or the policy gate is `INDETERMINATE`. `INDETERMINATE` is never silently converted to PASS. See [Assurance evaluation](assurance-evaluation.md) and [Interpreting results](interpreting-results.md).

## 1. Determine what changed

The assurance graph connects targets, evidence, controls and conclusions so a material change can select the propositions that require review rather than forcing a full restart.

See [Assurance graph and impact analysis](assurance-graph-impact.md).

## 2. Re-evaluate evidence

Evidence can remain current, become weaker, become invalid, or require human review. Provenance and freshness are explicit so a later assessment does not silently reuse an obsolete source.

See [Evidence provenance and freshness](evidence-freshness-delta.md) and [Evidence classification](evidence-classification.md).

## 3. Preserve assessment lineage

A reassessment should preserve the prior record and state the delta. Findings may be retained, refined, weakened, resolved or superseded depending on current evidence.

See [Assurance lineage](assurance-lineage.md) and [Review evidence and retention](evidence-retention.md).

## 4. Remediate and retest

Remediation is not closure. RAHP records the proposed or implemented change, the evidence needed to test it, the retest result and the remaining residual obligation.

See [Remediation and retesting](remediation-lifecycle.md).

## 5. Apply policy without manufacturing authority

A policy gate can return `PASS`, `FAIL` or `INDETERMINATE`. That result does not itself authorize publication, risk acceptance or closure. `INDETERMINATE` remains a non-green assurance outcome until evidence or governed disposition resolves the uncertainty.

Authority is independently scoped to actions such as `observe`, `assess`, `disposition`, `remediate`, `publish`, `accept-risk`, `close` and `reopen`. Repository permissions are not automatically governance authority.

See [Authority and policy gates](authority-policy-gates.md).

## 6. Publish current posture

Assurance posture presents the current state without hiding uncertainty behind a synthetic percentage. It can distinguish confirmed findings from evidence gaps, review obligations and controlled risks.

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
