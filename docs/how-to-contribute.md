---
layout: default
title: "How to contribute"
nav_order: 4
has_toc: true
parent: Implement RAHP
---
# Contributing to the RAHP Toolkit

RAHP contributions are easiest to review when the contributor first identifies **which authority boundary is changing** and then follows the workflow for that contribution type. This section is intentionally procedural: each path tells you what to change, in what order, what evidence to produce, and what must pass before a pull request is ready.

**Material assurance changes:** apply the [independent reviewability acceptance criterion](../CONTRIBUTING.md#independent-reviewability-and-assurance-evidence) when writing an issue or PR. The criterion requires reproducible, challengeable claims **or a justified NOT_APPLICABLE disposition**, not a completed external audit or new tests for routine housekeeping.

## Choose the contribution path

| I want to… | Start here | Primary authority |
|---|---|---|
| Add or improve reusable harms, risks, controls, guardrails, assurance or evidence patterns | [Extend the assurance catalogue](contributing-catalogue.md) | `method/catalogue/` |
| Add a toolkit capability, command, validator, renderer, monitor or other executable behaviour | [Add a toolkit capability](contributing-capability.md) | `tools/`, `packages/`, schemas and tests as applicable |
| Add a RAHP pressure test for a specification or protocol | [Add a specification pressure test](contributing-pressure-test.md) | `.rahp/reviews/` while working; `examples/` only for maintained exemplars |

If your change crosses more than one row, follow every applicable workflow. A new capability that introduces a new portable method concept, for example, must satisfy both the capability workflow and the catalogue/method workflow.

## The one rule

**Edit the canonical source for the layer you are changing; never hand-edit `build/`.**

RAHP has several authority boundaries:

- `method/` is portable method authority.
- `method/catalogue/` owns reusable assurance patterns (`HRM-*`, `RKP-*`, `CTP-*`, `GRP-*`, `ATP-*`, `EVP-*`).
- root `data/` is the bundled DTG exemplar catalogue retained for compatibility and generated evidence; it is **not** the portable method.
- `instances/<id>/` owns deployment-local assessment state and vocabulary.
- `profiles/<id>/` declares deployment targets and review configuration.
- `.rahp/reviews/` is the ordinary working location for review runs.
- `examples/` contains deliberately maintained teaching/conformance exemplars.
- `tools/` and `packages/` implement executable toolkit behaviour.
- `build/` is generated output and must be regenerated, never hand-edited.

## Before you change anything

1. **Fork or branch from a green baseline.**
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. Establish that the baseline is valid:

   ```bash
   python3 tools/validate.py
   python3 -m unittest discover -s tests -p 'test_*.py'
   ```

4. If you are changing TypeScript code or the stable engine boundary, also run:

   ```bash
   npm run build:ts
   npm run conformance
   ```

Do not start by editing generated files to make a failing check green. Find the canonical source or generator responsible for the output.

## Repository layout

```text
method/            Portable RAHP method, schemas and assurance catalogue.
  catalogue/       Reusable HRM/RKP/CTP/GRP/ATP/EVP assurance patterns.
  schema/          JSON Schema for portable records and engine contracts.
data/              Bundled DTG exemplar catalogue; not portable method authority.
profiles/          Deployment configuration and assessment targets.
instances/         Deployment-owned state, findings and local vocabularies.
corpora/           Reusable scenario corpora/adapters.
examples/          Maintained pressure-test/security/combined exemplars.
tools/             Python CLI, validators, renderers, monitors and build tooling.
packages/          TypeScript reference implementation/workspace.
tests/             Regression and conformance tests.
docs/              Human documentation.
build/             Generated artefacts. Do not hand-edit.
```

## Provenance requirement

Every catalogue or deployment record you add or materially change must retain enough provenance for a later reviewer to answer **what evidence caused this record to exist or change**.

For record types that carry a `provenance` block, use the established shape:

```yaml
provenance:
  source: "Target Specification v1.2 §5.2"
  triggered_by: "spec-review-2026-09"
  contributor: "your name or handle"
  imported: 2026-09-14
```

Provenance is assurance evidence. It should point to a source, review, issue, experiment or other reproducible trigger rather than merely state that a contributor thought the change was useful.

## Contribution-wide review gates

Regardless of contribution type, a pull request is not ready until the following are true:

1. **Authority is clear.** The change is made in the layer that is entitled to define it.
2. **Scope is bounded.** A deployment-specific rule has not silently become portable method, and a toolkit implementation choice has not silently become a governance requirement.
3. **Enforcement is explicit.** If the change creates an obligation, the validator, engine, consumer, governance process or other enforcement point is named.
4. **Evidence is obtainable.** A claimed control, guardrail, assurance rule or capability can produce evidence showing whether it works.
5. **Tests exist at the right level.** New executable behaviour has a regression/conformance test; new catalogue relationships validate; new pressure-test findings trace to pinned source evidence.
6. **Generated outputs are current.** Run the relevant renderer/build after canonical changes.
7. **Documentation is updated.** A new contributor or adopter should be able to discover and use the change without reading the implementation diff.
8. **Repository validation is green.** At minimum:

   ```bash
   python3 tools/validate.py
   python3 -m unittest discover -s tests -p 'test_*.py'
   python3 tools/build.py
   python3 tools/validate_reference_links.py
   ```

Run the additional commands specified by the workflow you followed.

## Identifier and naming rules

- Files in `data/` and `method/`: lowercase, hyphenated, `.yaml` where the format is YAML.
- Do not encode version numbers in ordinary filenames. Git tags and `CHANGELOG.md` carry release history.
- Stable identifiers never change meaning. If a concept is superseded, retire or supersede the old ID and record the relationship; do not reuse it.
- Do not allocate a deployment namespace for a portable pattern merely because an equivalent local ID already exists. Portable and local records have different authority and lifecycle.

## Critical risks

`Critical` is not a larger value of `High`. It means non-zero incidence is unacceptable because of legal, criminal, safeguarding or equivalent consequence. Critical risks have no numeric score, must be protected by a guardrail, and may not be risk-accepted. The validator enforces this.

## Using an AI assistant

See [AI-assisted process](ai-assisted-process.md). AI-assisted contributions follow exactly the same review and evidence requirements as human-drafted changes.

When a record was substantially drafted by an assistant, use the repository's provenance convention, for example:

```yaml
contributor: "Your Name (AI-assisted)"
```

An assistant may help discover candidate risks or draft prose, but risk acceptance, governance authority, normative decisions and assurance claims still require accountable human review.

## Pull-request evidence

A good PR description contains:

- what authority boundary changed;
- why the change is needed and what triggered it;
- which files are canonical versus generated;
- tests and validators run;
- evidence produced;
- compatibility or migration impact;
- any unresolved warning or follow-up.

Include the validator summary where applicable:

```bash
python3 tools/validate.py --summary
```

The three workflow pages below provide more specific completion checklists.
