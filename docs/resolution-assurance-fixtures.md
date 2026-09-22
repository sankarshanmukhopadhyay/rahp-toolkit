---
layout: default
title: "Resolution assurance fixtures"
nav_order: 9
parent: Run assessments
---

# Resolution assurance fixtures

RAHP treats trusted resolution as a chain of separately established
propositions rather than as a property of a URI scheme.

The executable matrix at `tests/fixtures/resolution-assurance-matrix.yaml`
tests that an implementation does not silently upgrade:

- identifier or transport authenticity into freshness;
- successful retrieval into ecosystem recognition;
- a recognized source into authorization;
- authenticated content into applicability for a requested version.

The positive case is deliberately bounded: all required resolution-chain
propositions are positively established, and the resulting assurance applies
only to that resolution chain. It does not itself authorize an application
operation.

## DRARM boundary

Resolver behavior has a separate resilience dimension. Recursive resolution
without an explicit depth/work budget or cycle tracking can amplify one input
into unbounded dependent work. The fixture executes DRARM and expects
`RLA-017` / `RLA-018` review evidence for an unbounded resolver, while a
resolver exposing `resolution_budget` and `visited` controls satisfies the
static control check.

This keeps provenance/authenticity judgment separate from distributed
resilience judgment while allowing a combined assurance process to consume both.
