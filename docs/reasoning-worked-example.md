---
layout: default
title: "Worked R1–R3 reasoning example"
parent: Learn RAHP
nav_order: 9
has_toc: true
permalink: /docs/reasoning-worked-example/
---
# Worked R1–R3 reasoning example

Tracking: [#937](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/937).

This **synthetic, standalone** example exercises the three optional reasoning profiles against one illustrative TRQP historical-answer proposition. It does **not** assert conformance of the actual TRQP specification or its implementations. No network fetch or evidence authentication occurs.

## Run it

From the repository root, with Python 3:

```bash
python3 -m tools.reasoning_worked_example --scenario baseline
python3 -m tools.reasoning_worked_example --scenario missing
python3 -m tools.reasoning_worked_example --scenario retroactive
python3 -m tools.reasoning_worked_example --scenario disagreement
python3 -m unittest tests.test_reasoning_worked_example -v
```

Each command prints stable JSON with `scenario`, `r1`, `r2`, `r3`, and `assurance_note`. The evaluator is deterministic and the synthetic input pin is SHA-256 of canonicalized declared fixture JSON. **The source pins in R2 are declarations, not verified provenance.**

## Interpret the outcomes

| Scenario | R1 structural adequacy | R2 declared applicability | R3 comparison |
| --- | --- | --- | --- |
| baseline | PASS | APPLICABLE | DECLARED_MATCH |
| missing | INDETERMINATE (missing source snapshot) | APPLICABLE | DECLARED_MATCH |
| retroactive | PASS | APPLICABLE as known by 2026-05-01; later record explicitly disclosed | DECLARED_MATCH |
| disagreement | PASS | APPLICABLE | OUTPUT_DISAGREEMENT with OPEN challenge |

The **retroactive** case records a second authority assertion on 2026-08-15 claiming effect from 2026-04-01. Because the knowledge cutoff is 2026-05-01, it is disclosed in `later_record_ids` rather than silently changing the historical as-known-at result. A new determination with a later cutoff must explicitly consider that assertion and may produce a conflict.

The **disagreement** case deliberately gives two declared runs different outcomes for the same input pin and evaluator version, and leaves a METHOD challenge open. This is not an adjudication.

## Consumer interpretation and authority

R1 PASS says only that the supplied observations satisfy a **declared structural requirement set**. R2 APPLICABLE says only that **declared** source metadata covers the requested time. R3 DECLARED_MATCH says only that **declared** inputs, evaluator identity/version and outcomes agree. Their conjunction is **not** an RAHP terminal PASS, nor proof of authenticity, authority, independence or correctness.

This example is a *consumer orchestration*, not a new versioned RAHP profile or an authoritative policy composition. The example's run outcome mapping is illustrative and must not be used as a production assurance rule. It does not modify the assessor-result v1, reasoning trace, R1–R3 APIs, or assurance controller.

To run an uncoached assessment with fresh fixtures, use the [independent adoption exercise](reasoning-adoption-exercise.md) and [evidence-recording template](reasoning-adoption-record.md). Release decisions are tracked in the [readiness record](reasoning-release-readiness.md).

## What an adopter still needs

An independent adopter must retrieve and authenticate real source material, govern authority and source selection, declare a justified freshness/temporal policy, verify actual run independence, and retain challenge handling and terminal assurance within its authorized processes.

Related: [R1 evidence adequacy](evidence-adequacy.md), [R2 temporal provenance](temporal-provenance.md), [R3 reproducibility and challenges](reproducibility-challenge.md), [reasoning architecture](reasoning-architecture.md).
