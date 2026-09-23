---
layout: default
title: "Negative assurance fixtures"
nav_order: 8
parent: Run assessments
---

# Negative assurance fixtures

RAHP maintains deliberate negative fixtures for claims that must fail closed or
remain indeterminate when required evidence is missing. These fixtures are not
examples of "bad inputs" only; they are executable falsification cases for
assurance propositions.

The original cross-mode matrix at
`tests/fixtures/negative-assurance-matrix.yaml` covers four lenses and remains authoritative evidence for those cases:

- **RAHP:** valid participant evidence does not establish collective authority.
- **Security:** an insufficient threshold subset cannot exercise collective authority.
- **Composition:** component PASS does not imply composition PASS when the
  composition rule itself is unestablished.
- **DRARM:** unbounded group fan-out is an amplification concern, without
  treating DRARM as an authority model.

The matrix also carries two adjacent negative propositions: a bounded but
unenumerated audience must not silently become unrestricted bearer permission,
and identifier authenticity must not silently become freshness, recognition, or
authorization.

## Design rule

A negative fixture should identify the exact unsafe inference being rejected and
include a legitimate counter-case elsewhere in the maintained evidence corpus.
Missing evidence is preserved as missing or indeterminate evidence; it is never
rewritten into PASS merely because all visible components validate.

The existing false-independence and quorum-capture pressure tests remain the
deeper authoritative worked examples. The compact matrix exists to keep these
non-inference rules executable across assessment modes.


## Reusable contract

The repository now layers a reusable `rahp-negative-fixture/v1` contract over
existing authoritative evidence. The contract adds a fifth **specialist**
surface and makes positive-control linkage, evidence state, ownership boundaries,
retest triggers, and the missing-evidence invariant mechanically validatable.

See [Reusable negative-fixture contract](negative-fixture-contract.html) for the
schema, starter wrappers, inventory, validator, and contributor workflow.
