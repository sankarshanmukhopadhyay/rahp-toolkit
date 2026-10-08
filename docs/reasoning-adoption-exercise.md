---
layout: default
title: "Independent R1–R3 adoption exercise"
parent: Learn RAHP
nav_order: 10
has_toc: true
permalink: /docs/reasoning-adoption-exercise/
---
# Independent R1–R3 adoption exercise

Tracking: [#939](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/939). This is an **uncoached participant exercise**. The maintainer's internal dry run is not independent adoption evidence.

## Participant brief

**Question:** Can you reconstruct a bounded historical-authority assessment and explain what the three optional profiles do *not* establish?

You may use only the public [adoption guide](adoption-guide.md), [R1](evidence-adequacy.md), [R2](temporal-provenance.md), [R3](reproducibility-challenge.md) and [worked example](reasoning-worked-example.md), plus the repository code needed to execute them. Do not ask the maintainer to interpret an outcome during the exercise. Record every ambiguity before seeking help.

The subject is an **invented registry authority answer**, not a real TRQP implementation or conformance claim. Choose a new proposition ID, two required evidence IDs, a bounded scope, target time T, knowledge cutoff K and evaluation time E (K ≤ E). Explain why you chose them. Declare exactly one in-scope SATISFIED R1 observation and one known R2 record per evidence ID, with declared source pins and effective intervals covering T. Construct two R3 run declarations. Do not use the example's original IDs verbatim.

## Required independent scenarios

| Scenario | Mutation | Expected invariant |
| --- | --- | --- |
| A — baseline | Two satisfied R1 observations; one known effective R2 record per requirement; matching R3 run declarations | R1 PASS; R2 APPLICABLE; R3 DECLARED_MATCH |
| B — missing | Remove one required R1 observation; leave R2 unchanged | R1 INDETERMINATE with MISSING; R2 remains APPLICABLE |
| C — later retroactive | Add a second R2 assertion recorded after K but before E, claiming effect at T | Earlier as-known-at R2 remains APPLICABLE; later record appears in later_record_ids |
| D — known conflict | Re-evaluate C with K moved after the later record's recorded_at (and K ≤ E) | R2 INDETERMINATE with CONFLICT for that evidence ID |
| E — disputed run | Same declared input pin and evaluator identity/version, but different outcomes; add challenge | R3 OUTPUT_DISAGREEMENT; challenge remains OPEN |

These are **separate mutations**, not cumulative unless stated. A declared R3 match is not proof of actual independent execution. The run outcomes are *declared records*, not computed by R3 from R1/R2.

## Commands and evidence capture

Pin a repository commit SHA and record the Python version. Run from repository root:

```bash
python3 --version
git rev-parse HEAD
python3 -m unittest tests.test_reasoning_worked_example -v
python3 -m tools.reasoning_worked_example --scenario baseline
python3 -m tools.reasoning_worked_example --scenario missing
python3 -m tools.reasoning_worked_example --scenario retroactive
python3 -m tools.reasoning_worked_example --scenario disagreement
```

The commands above are a **reference smoke check**, not the independent exercise. For the actual exercise, create **new input fixtures** and invoke `evaluate`, `evaluate_temporal` and `compare` using the documented APIs. Save each fixture, stdout/stderr, exit code, and SHA-256 hash. Do not publish private information, credentials, personal identifiers or real sensitive registry data.

Use [the evidence-recording template](reasoning-adoption-record.md). For each scenario, record expected versus observed status and an explanation. Note the elapsed time to first successful run, any documentation dead ends, and every point where you needed undocumented knowledge.

## Assurance questions to answer in writing

1. What authority determined the evidence requirements and scope?
2. Who attested the source pins and effective intervals, and what was actually verified?
3. Why is a later-recorded retroactive assertion disclosed but excluded from the earlier knowledge cutoff?
4. Who may decide precedence, supersession, revocation and challenge resolution?
5. Why do R1 PASS, R2 APPLICABLE and R3 DECLARED_MATCH **not** amount to a terminal RAHP PASS?

## Maintainer disposition

Classify each finding as DOCUMENTATION_DEFECT, INTERFACE_DEFECT, MISSING_CAPABILITY or DELIBERATE_BOUNDARY. Record one of ADOPTABLE, ADOPTABLE_WITH_FRICTION, INDETERMINATE, or NOT_YET_TESTED (no independent participant). Create only evidence-backed follow-ups. The exercise is complete only when an independent participant's evidence and determination are linked to #939.

No controller, stable assessor-result contract or R1–R3 schema is changed by this exercise.
