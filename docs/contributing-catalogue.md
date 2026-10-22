---
layout: default
title: "Extend the assurance catalogue"
nav_order: 1
has_toc: true
parent: Implement RAHP
---
# Extend the assurance catalogue

Use the [RAHP glossary](glossary.md) when naming concepts. Prefer simple English. If a new pattern introduces a term that a reader may not understand, add or update the glossary in the same change.

Use this workflow when contributing **portable** harms, risks, controls, guardrails, assurance patterns or evidence patterns. The portable catalogue is reusable method knowledge, not a collection of every finding encountered in a deployment.

## Outcome

A successful catalogue contribution produces a reusable pattern with a stable ID, explicit relationships to adjacent assurance layers, sufficient provenance/rationale, and validator evidence that the graph remains coherent.

## Step 1 — Decide whether the concept is actually portable

Before allocating an ID, ask:

1. Can the concept plausibly recur in more than one deployment or specification family?
2. Is the concept independent of one project's local governance vocabulary or implementation detail?
3. Can its meaning be stated without naming the deployment that first exposed it?

If the answer is **no**, add the concept to the deployment-local vocabulary (`instances/<id>/data/`), corpus, or pressure-test finding instead.

If the answer is **yes**, continue under `method/catalogue/`.

## Step 2 — Select the correct catalogue family

| Contribution | File | Namespace | What it represents |
|---|---|---|---|
| Human harm | `method/catalogue/harm-patterns.yaml` | `HRM-*` | The adverse human interest/outcome |
| Risk pattern | `method/catalogue/risk-patterns.yaml` | `RKP-*` | A reusable failure mechanism that can produce harm |
| Control pattern | `method/catalogue/control-patterns.yaml` | `CTP-*` | A mechanism that prevents, constrains, detects, contains or remediates risk |
| Guardrail pattern | `method/catalogue/guardrail-patterns.yaml` | `GRP-*` | A non-negotiable constraint preventing an unacceptable state |
| Assurance pattern | `method/catalogue/assurance-patterns.yaml` | `ATP-*` | A testable proposition/procedure about control or guardrail effectiveness |
| Evidence pattern | `method/catalogue/evidence-patterns.yaml` | `EVP-*` | The evidence contract supporting an assurance claim |

Do not put portable patterns in root `data/`. Root `data/` remains the bundled DTG exemplar.

## Step 3 — Search for an existing concept before creating one

Search both titles and descriptions:

```bash
grep -Rni "<keyword>" method/catalogue/
```

Then inspect adjacent patterns. Prefer extending an existing pattern's applicability or relationships when that preserves meaning. Create a new ID only when the failure mechanism, protected interest, enforcement semantics or evidence proposition is genuinely different.

## Step 4 — Allocate a stable ID and write the minimal semantic core

Follow the existing namespace and sequence in the target file. Never repurpose an existing ID.

For a **harm**, define the protected/affected human interest and recognizable manifestations.

For a **risk**, state the failure mechanism and causal path to one or more harms. Do not describe only a bad outcome.

For a **control**, state the control objective and function (`prevent`, `constrain`, `detect`, `contain`, `recover`, `remediate`, and so on), plus the authority/enforcement point where applicable.

For a **guardrail**, identify the prohibited state or non-negotiable condition and the enforcement point that prevents progression when it fails.

For an **assurance pattern**, state something two independent assessors can test and reach the same result on.

For an **evidence pattern**, state who produces the evidence, what claim it supports, integrity/freshness expectations, and when it becomes invalid.

Use the fields already established by neighboring records rather than inventing a one-off shape.

## Step 5 — Link the contribution into the assurance graph

A portable record should not be an island. Add the relationships required by its layer.

The intended trace is:

```text
HRM harm
  ↑
RKP risk pattern
  ↓
CTP control pattern / GRP guardrail
  ↓
ATP assurance pattern
  ↓
EVP evidence pattern
```

At minimum:

- a new `RKP-*` should identify the human harms it can produce;
- a new `CTP-*` should identify the risks/control objective it addresses;
- a new `GRP-*` should identify the unacceptable state/risk and its enforcement semantics;
- a new `ATP-*` should identify the control or guardrail proposition it tests;
- a new `EVP-*` should identify the assurance claim/test it can support.

Also record control side effects or introduced risks where relevant. A mitigation is not automatically harmless.

## Step 6 — Check authority, enforcement and evidence semantics

Before validation, review the contribution using these questions:

- **Authority:** Who is allowed to impose, operate, override or revoke this control/guardrail?
- **Scope:** Under what system/deployment properties is the pattern applicable?
- **Enforcement:** Where does failure stop or alter execution?
- **Revocation/change:** What happens when the authority, delegation or supporting evidence changes?
- **Auditability:** What observable event proves the control operated or failed?
- **Evidence freshness:** How long can evidence reasonably support the assurance claim?

If those questions cannot be answered, the pattern may still be useful as a risk/harm hypothesis, but it should not claim stronger control or assurance semantics than the evidence supports.

## Step 7 — Validate the portable catalogue

Run:

```bash
python3 tools/validate_catalogue.py
python3 tools/validate_v04_method.py
python3 tools/validate.py
```

**Errors must be fixed.** Warnings must be reviewed and either addressed or explained in the PR.

Common failures include:

- risk with no linked harm;
- unknown relationship ID;
- Critical risk without a guardrail;
- assurance test referencing an unknown control;
- guardrail override with no authority;
- evidence with no meaningful freshness/invalidation semantics;
- circular causal relationships.

## Step 8 — Add or update a real use of the pattern

Portable patterns should be demonstrated, not merely declared. Where practical, map the new pattern from at least one maintained pressure-test finding, scenario pattern or corpus adapter.

For a maintained example, add or refine its `portable_assurance` mapping rather than replacing deployment-local risk IDs.

Then run the applicable validator, for example:

```bash
python3 tools/validate_pressure_tests.py
python3 tools/validate_scenario_corpora.py
```

A portable mapping is explanatory reuse. The local finding and pinned source evidence remain authoritative for the assessment.

## Step 9 — Rebuild human-readable catalogue views

Run:

```bash
python3 tools/build.py
python3 tools/build_assurance_registry.py
python3 tools/build_assurance_registry.py --check
python3 tools/validate_reference_links.py
```

Confirm that the new ID is discoverable from the generated catalogue, appears in the derived assurance registry, and that references resolve. The registry is a derived discovery surface only; `method/catalogue/` remains authoritative for portable semantics.

## Step 10 — Update documentation and changelog when the public method surface changed

For a material reusable addition, update as applicable:

- `docs/portable-assurance-catalogue.md`
- `docs/assurance-knowledge-model.md`
- `CHANGELOG.md`
- release notes if the change is being shipped in a release

Do not document a deployment-specific interpretation as though every adopter must use it.

## Step 11 — Submit the PR with catalogue evidence

The PR should state:

1. which portable IDs were added or changed;
2. why existing patterns were insufficient;
3. the source/review that triggered the contribution;
4. the relationships added to the assurance graph;
5. any authority/enforcement assumptions;
6. validation commands and results;
7. a maintained example or scenario demonstrating the pattern, where available.

## Done when

The contribution is complete when:

- [ ] the concept is demonstrably portable;
- [ ] the stable namespace and ID are correct;
- [ ] adjacent assurance relationships resolve;
- [ ] control/guardrail authority and enforcement are explicit where applicable;
- [ ] assurance/evidence semantics are testable rather than aspirational;
- [ ] `validate_catalogue.py` and core validation pass;
- [ ] at least one real mapping/use exists when practical;
- [ ] generated catalogue/reference views are current;
- [ ] documentation explains any new method concept.
