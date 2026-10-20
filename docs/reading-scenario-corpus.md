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

## Worked reading: TT-002 — five questions, one answer

Open [TT-002 in the Trust Tasks corpus](../corpora/trust-tasks/). It asks whether a signed task can be accepted by a recipient other than its intended audience.

| Reader's question | What the current evidence supports |
|---|---|
| **1. What could go wrong?** | A proof may verify cryptographically without binding the signed task to the intended recipient. Another consumer could then rely on it. This is a *scenario to test*, not a reported failure. |
| **2. Who could be affected?** | The producer or accountable principal might have an assertion used outside its intended audience; an unintended recipient might mistakenly rely on it. A further affected person would depend on a consequential downstream action. These **possible roles are provisional**, not independently accepted person–harm links. |
| **3. How serious is it?** | `P0` marks high priority for *pressure-testing*, **not** measured severity, probability, prevalence or a finding that the system is unsafe. Without deployment context and outcome evidence, real-world severity is **not established**. |
| **4. Has anybody checked?** | RAHP's [source-review packet](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/method/impact-pathways/source-review-2026-10-20.json) examines the *specification's mechanism*, but no exact, revision-qualified review-to-scenario execution reference was established by the current corpus inventory. **Execution status is unknown**, not PASS, FAIL or “never tested”. |
| **5. Where does this come from?** | [Trust Tasks §4.8.2 at pinned commit `4937c70`](https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/4937c70df95e56ed6404b8c004106ecb121a23cf/SPEC.md#482-audience-binding) requires recipient binding for proof-carrying non-bearer tasks; §10.1 discusses cross-recipient replay. Bearer specifications are a stated exception. |

**What the scenario protects:** `primary_goal` is *Bind a signed task to its intended recipient*. The [`SP-REPLAY-01`](../method/scenario-patterns/#sp-replay-01) pattern examines evidence reused outside its intended scope; [`SP-AUTH-01`](../method/scenario-patterns/#sp-auth-01) captures authorization pressure.

**What you can conclude:** The pinned source describes a technically meaningful threat and a normative safeguard. You **cannot** conclude that a compliant Trust Tasks implementation failed, that anyone was harmed, or that its proposed people-impact relationship has received independent acceptance.

**Where to go next:** Readers can stop here. For deeper review, open the [people-impact pilot](people-impact-pathway-pilot.html) for the two provisional mappings and 48 explicitly unestablished cases; specialist reviewers can inspect the [qualification acceptance explanation](people-impact-qualification-acceptance.html) and its cited evidence packet.

## Two different scenario collections

Corpus-specific `TT-*`, `CS-*`, `UC-*` and `XSP-*` identifiers are domain or composed pressure-test scenarios in `corpora/*.yaml`. Separately, RAHP's `SC-*` scenarios in `data/scenarios.yaml` describe people-linked contexts with `legitimate_personas`, `adversarial_personas` and `user_stories`. They are **not interchangeable IDs**, and an `SC-*` scenario must not be assumed to prove a linkage to a corpus row. Likewise, a security finding such as `SEC-TT-002` is not automatically the corpus scenario `TT-002`.

To ask *who bears the consequence*, inspect the [personas](personas.md), relevant [harm patterns](../method/catalogue/harm-patterns/) and actual review evidence, and record explicit justified relationships rather than joining identifiers by resemblance.

## How to verify rather than assume

Begin with the [corpora browser](../corpora/), read the relevant scenario, follow its `SP-*` link and inspect its canonical YAML. Where a pinned source link is available, read that source passage. For any assertion that the pressure was actually tested, request the assessment record, test conditions, observed result, provenance and unresolved limitations. **If that evidence cannot be found, the testing status remains unknown**, not passed or failed.

The [scenario corpora reference](scenario-corpora.md) and [corpus synchronization and provenance](corpus-synchronization.md) explain adapter ownership, drift and re-baselining.

## Evidence-qualified reverse references and affected people

A corpus page now has a **Review evidence links** section. A linked review means that its canonical structured review has an explicit `corpus_scenario_references` entry naming the exact corpus ID, scenario ID, source commit, and a resolvable evidence path within that review. It does **not** mean that the scenario passed, that a deployment was tested, or that harm occurred. If the page says **No linked review evidence identified**, read that literally. Reviews of a similarly named specification or security finding are not interchangeable with scenario-level evidence. Existing reviews without explicit, version-qualified citations are not silently assigned to scenarios.

`SC-*` records provide an independent, people-linked assurance path. Corpus scenario IDs do not automatically identify affected personas. Where a corpus explicitly lists `portable_assurance.harm_patterns`, those are proposed reusable catalogue mappings, not findings about a person. A future direct persona relationship would require an explicit, source-qualified method and an accountable review. For now, no `affected_personas` schema field or automatic `SP-*`-based mapping is introduced.

## Pilot people-impact pathways

The [Trust Tasks corpus](../corpora/trust-tasks/) and [Trust Tasks × Credential Spec composed corpus](../corpora/trust-tasks-credspec-composed/) now carry a **Potential people-impact pathways** section covering every scenario in each selected corpus. **Provisional** means an explicitly reasoned but not independently qualified RAHP analyst hypothesis; **not-established** means the available record does not justify assigning an affected role and potential harm. Neither state is an observed incident, an execution PASS, a source-specification requirement or a safety rating. In particular, do not infer named DTG personas from the portable affected roles.

For a worked source-facing example, inspect `TT-002`: a request intended for one recipient might be accepted outside its intended audience. The potential affected role is described, but person-specific harm and execution evidence remain unestablished. For a composed example, inspect `XSP-001`: relying on a credential without its originating task-outcome evidence might cause a decision based on incomplete assurance. Its composed parent sources must be independently qualified and no person-harm link is assumed.

The canonical dispositions are in [the impact mapping pilot](../method/impact-pathways/pilot.json). Run `python3 tools/validate_impact_pathways.py --check` to confirm the full 50-scenario pilot, per-corpus adapter/source baselines, and the explicit unresolved rows. These are research-level mappings, not an assertion about a live community or credential subject.
