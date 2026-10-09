---
layout: default
title: "Comparative assurance digest"
nav_order: 8
has_toc: true
parent: Implement RAHP
---
# Comparative assurance digest

The Comparative Assurance Digest is a profile-bound, machine-readable comparison of two RAHP assessments. It helps a reader understand what changed without replacing either assessment, its evidence, or the accountable human decision.

The contract is defined by [`method/schema/comparative-assurance-digest.schema.json`](../method/schema/comparative-assurance-digest.schema.json).

## Semantic boundary

The digest keeps four questions separate:

1. Did the assessment process become more capable?
2. Did the breadth, quality or preservation of evidence improve?
3. Did the assurance outcome improve?
4. Is the candidate acceptable for release?

An affirmative answer to an earlier question does not determine an answer to a later one. In particular:

```text
assessment capability improvement != release assurance improvement
evidence volume != proposition closure
comparative improvement != release acceptability
```

The digest uses bounded ordinal judgments. It does not define a universal score or permit lower-materiality improvements to conceal a blocking regression.

## Comparability

Top-level and dimension-level comparability use:

- `compatible`: the declared comparison profile establishes a sufficient common basis;
- `partial`: some dimensions or propositions have a defensible common basis and others do not; and
- `not_comparable`: a comparative conclusion would be misleading.

Partial comparability is not a degraded form of compatibility. It identifies the exact basis on which bounded judgments can be made while preserving unmatched scope, semantics, policy or evidence as an explicit limitation.

When top-level comparability is `not_comparable`, the overall judgment must also be `not_comparable`. RAHP must not synthesize an improvement or regression from incompatible inputs.

## Judgment and confidence

Comparative judgments are:

```text
materially_improved
improved
mixed
no_material_change
regressed
materially_regressed
indeterminate
not_comparable
```

Confidence is a separate field: `high`, `moderate`, `low`, or `insufficient`. Confidence describes the evidence basis for the judgment; it does not make the judgment more favourable.

Release disposition is also separate. A candidate may be materially improved relative to a deficient baseline while remaining unacceptable for release.

Every overall and dimension judgment retains:

- a human-readable justification;
- evidence references;
- counterevidence references; and
- unresolved limitations.

Justification records judgment. Evidence supports or falsifies it. The two are not interchangeable.

## Scope and dependencies

The digest distinguishes directly assessed components, supporting dependencies and excluded components. A dependency that was downloaded, imported, resolved or exercised transitively remains `observed_not_assessed` unless an independent assessment artifact is referenced.

Every excluded component requires a reason. Coverage limitations remain visible even when the available evidence supports a favourable bounded judgment.

## Finding deltas

Finding identity must not depend solely on titles. A future deterministic differ may use stable finding identifiers, criteria identifiers, affected components, claims and profile-declared matching keys.

The contract supports:

```text
resolved
introduced
unchanged
changed
reopened
not_reassessed
evidence_strengthened
evidence_weakened
no_longer_applicable
unmatched
```

An unmatched baseline finding is not resolved. Evidence change is represented independently from disposition change so that stronger or weaker evidence does not silently become a different assurance conclusion.

## Profile author obligations

A comparison profile should declare:

- the dimensions and proposition-matching basis;
- compatible schema, profile, taxonomy and policy versions;
- materiality and blocking conditions;
- minimum coverage for an overall judgment;
- treatment of missing, stale and conflicting evidence;
- treatment of scope expansion; and
- any permitted cross-version equivalence or migration rule.

Aggregation policy is governance-bearing behavior. It must be explicit and testable rather than hidden in arithmetic.

## Required invariants

- Missing evidence is not PASS.
- An unmatched baseline finding is not automatically resolved.
- A blocking regression is not compensated for by unrelated improvements.
- No overall comparative judgment is generated for non-comparable assessments.
- Dependency use does not imply independent assessment.
- Test or evidence counts do not substitute for proposition closure.
- Newly admitted propositions are not automatically regressions.
- Human-readable prose is not the machine contract.
- Comparative improvement does not establish release acceptability.

## Initial worked fixture

[`fixtures/comparative-assurance/valid-partial.json`](../fixtures/comparative-assurance/valid-partial.json) captures the bounded result exposed by the Dogwood-to-Eucalyptus manual comparison: assessment capability and evidence preservation improved materially, while release-assurance superiority remains unestablished.

This fixture validates the contract. It is not yet the output of a deterministic comparison engine. Finding matching, profile execution, CLI integration and Markdown rendering remain later delivery increments.
