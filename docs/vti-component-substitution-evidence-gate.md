---
layout: default
title: "VTI component-substitution evidence gate"
parent: Reference
nav_order: 6
has_toc: true
---
# VTI component-substitution evidence gate

RAHP does not currently publish a VTI component-substitution assessment submission for `VTI-CMP-100` and `VTI-CMP-101`.

The normative substitution proposition has graduated to the upstream VTI composition requirements, but the deliberately narrow runtime evidence gate identified by RAHP remains unmet: the corpus does not contain a genuine A/B exercise in which **two independently meaningful conformant implementations of the same replaceable component are substituted under one composition** while a declared composition-visible property is observed.

## Current disposition

**Evidence state: `EVIDENCE_REQUIRED`.**

Existing Dogwood A/B evidence does not satisfy this gate because it compares relying contexts against one pinned implementation rather than replacing one implementation with another.

RAHP therefore does not manufacture a synthetic pair merely to publish a successful assessment.

## Required evidence

A future bounded substitution experiment must establish both:

1. two genuine implementations satisfy the applicable component-local expectations independently; and
2. at least one composition-visible property can be compared before and after substitution.

Candidate properties include authority, lifecycle, failure/indeterminate semantics, privacy/correlation, and human control.

A preserving substitution must remain a legitimate counter-case; the assessment is not intended to make substitution impossible.

## Re-entry

Re-enter active assessment work only when the two evidence conditions above are true. At that point the new experiment should be evaluated against the then-current upstream VTI requirement revision rather than treating historical RAHP issue #188 as the normative source.

The machine-readable gate is `examples/cross-spec/vti-component-substitution/evidence-gate.yaml`.
