---
layout: default
title: "Reading a scenario corpus"
parent: Learn RAHP
nav_order: 5
has_toc: true
---
# Reading a scenario corpus

This guide is for people deciding whether a trust system deserves further examination, including community stewards, policymakers, funders and people affected by its operation. You do not need to be a specification author to read a scenario.

A **corpus** is a group of proposed situations in which an implementation or governance process should be tested. Each **scenario** describes one such situation; a **scenario pattern** (an `SP-*` identifier) names a pressure that can arise across different systems. The [corpora browser](../corpora/) lists the packaged collections. The [scenario-pattern catalogue](../method/scenario-patterns/) explains individual patterns.

## Five questions to ask

| Your question | What the corpus can tell you | What it cannot establish |
|---|---|---|
| What could go wrong? | The scenario title, `primary_pressure` and linked `SP-*` patterns name an adverse situation to probe. | That the failure occurred in a real deployment. |
| What was the system supposed to protect? | `primary_goal` states the intended safeguard or outcome. | That the safeguard is implemented or effective. |
| Who could be affected? | Relevant people and interests may be found in separate RAHP persona, risk and harm records, **if an evidenced link has been established**. | That every corpus row has a supported person-to-harm mapping. Many do not. |
| How urgent is the question? | `P0` marks a higher-priority pressure probe; `P1` a secondary probe. | A measured probability, incident severity, population harm or safety rating. |
| Where did it come from and has it been tested? | `source_anchor`, source repository and source commit may identify an originating text. Check relevant review evidence separately. | That a source pin proves conformance, or that a test was run merely because a scenario is listed. |

**Do not read a scenario row as a finding.** The scenario is a proposed test question. An **evidence grade** describes how the scenario adapter is grounded in source material, not whether a system is safe. `source-pinned` indicates declared pinned source grounding; `source-informed` draws from source semantics without a complete normative baseline; `scenario-baseline` is a working pressure-test hypothesis. **Not declared** means the canonical corpus has no grade field. Do not infer a stronger grade from descriptive provenance text.

## Worked reading: TT-002

Open the [Trust Tasks corpus](../corpora/trust-tasks/) and locate `TT-002`, *Proof-bearing document lacks safe audience binding*.

- **In everyday terms:** a document with a valid proof that was intended for one recipient might be accepted by a different recipient.
- **What should be protected?** Its `primary_goal` is *Bind a signed task to its intended recipient*.
- **What is the pressure?** Cross-recipient replay. The linked [SP-REPLAY-01](../method/scenario-patterns/#sp-replay-01) pattern concerns valid evidence reused outside its intended scope. [SP-AUTH-01](../method/scenario-patterns/#sp-auth-01) concerns compromised control.
- **Where did the scenario come from?** The corpus declares `trustoverip/dtgwg-trust-tasks-tf` at commit `4937c70df95e56ed6404b8c004106ecb121a23cf`, and source anchor `SPEC.md#482-audience-binding`. See the [pinned source passage](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/4937c70df95e56ed6404b8c004106ecb121a23cf/SPEC.md#482-audience-binding).
- **Who is harmed?** The row does not declare an authoritative persona or harm-pattern linkage. A reviewer must establish who relies on this task and what consequences would follow; the scenario alone cannot answer that.
- **Was it tested?** The corpus record does not include an execution result for this scenario. To establish a finding, locate a review, runnable test and its evidence. Absence of a reference on this page is not proof that no assessment exists.

This example explains *how to read* a proposed failure mode. It is **not** evidence that Trust Tasks fails audience binding.

## Two different scenario collections

Corpus-specific `TT-*`, `CS-*`, `UC-*` and `XSP-*` identifiers are domain or composed pressure-test scenarios in `corpora/*.yaml`. Separately, RAHP's `SC-*` scenarios in `data/scenarios.yaml` describe people-linked contexts with `legitimate_personas`, `adversarial_personas` and `user_stories`. They are **not interchangeable IDs**, and an `SC-*` scenario must not be assumed to prove a linkage to a corpus row. Likewise, a security finding such as `SEC-TT-002` is not automatically the corpus scenario `TT-002`.

To ask *who bears the consequence*, inspect the [personas](personas.md), relevant [harm patterns](../method/catalogue/harm-patterns/) and actual review evidence, and record explicit justified relationships rather than joining identifiers by resemblance.

## How to verify rather than assume

Begin with the [corpora browser](../corpora/), read the relevant scenario, follow its `SP-*` link and inspect its canonical YAML. Where a pinned source link is available, read that source passage. For any assertion that the pressure was actually tested, request the assessment record, test conditions, observed result, provenance and unresolved limitations. **If that evidence cannot be found, the testing status remains unknown**, not passed or failed.

The [scenario corpora reference](scenario-corpora.md) and [corpus synchronization and provenance](corpus-synchronization.md) explain adapter ownership, drift and re-baselining.
