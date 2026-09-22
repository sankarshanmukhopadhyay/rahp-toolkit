---
layout: default
title: "Reusable negative-fixture contract"
parent: Reference
nav_order: 10
---

# Reusable negative-fixture contract

RAHP treats falsification evidence as an assurance primitive. A negative fixture
states a specific unsafe inference that must not occur when a material
proposition is missing, stale, contradicted, or unsupported.

The contract is intentionally small:

- schema: `schemas/negative-fixture.schema.json`;
- reusable fixture wrappers: `fixtures/negative/`;
- inventory of existing evidence: `data/negative-fixture-inventory.yaml`;
- validator: `tools/validate_negative_fixtures.py`.

The wrappers **reference existing authoritative tests and pressure tests**. They
do not duplicate or replace the underlying assessor behavior.

## Contract rule

Every `rahp-negative-fixture/v1` fixture identifies:

1. the claim under test and its owning lens;
2. established, missing, stale, contradicted, and unsupported evidence;
3. the unsafe inference being prevented;
4. the expected state and prohibited success states;
5. an authoritative source/reference;
6. a mandatory positive counter-case;
7. specialist, composition, and DRARM ownership boundaries;
8. reassessment triggers and evidence maturity.

The validator enforces the repository-wide invariant:

> If material evidence is missing, stale, contradicted, or unsupported, the
> fixture cannot declare PASS, VERIFIED, PERMIT, or GREEN.

This is a contract invariant, not a replacement for each assessor's own
fail-closed rules.

## Starter coverage

The v1 starter set deliberately proves the contract across five surfaces:

- **RAHP:** participant validity does not establish collective authority;
- **security:** one valid member signature does not satisfy a higher threshold;
- **composition:** component PASS does not synthesize a missing composition rule;
- **DRARM:** successful local resolution does not establish bounded recursive work;
- **specialist:** a privacy suspicion does not become a valid DPIP referral until
  the examination target is bounded.

The inventory also records existing resolution, false-independence, and
quorum-capture evidence that is not migrated into a new wrapper merely to make
the initial contract look comprehensive.

## Positive controls

A negative fixture without a positive counter-case is invalid. This prevents the
suite from becoming a generic rejection catalogue.

A positive control need not use the same implementation path, but it must be an
existing repository artifact that positively establishes the proposition or the
control needed to distinguish the safe case.

## Ownership boundaries

The contract does not transfer semantic ownership.

- Composition decides composition propositions, not individual component validity.
- DRARM owns amplification/resilience propositions, not authority semantics.
- A specialist owns the question explicitly promoted to it. For the DPIP starter
  case, DPIP owns privacy applicability and the scoped privacy conclusion; it
  does not decide authorization or collective authority.
- RAHP reconciliation consumes these results without turning absence of a
  detected failure into positive assurance.

## Adding a fixture

Before adding a wrapper:

1. find the existing authoritative fixture/test/pressure test;
2. add or update the inventory entry;
3. create a minimal `rahp-negative-fixture/v1` wrapper only when it contributes
   a reusable non-inference guarantee;
4. identify a positive control;
5. state ownership boundaries and reassessment triggers;
6. run `python3 tools/validate_negative_fixtures.py`;
7. run the underlying authoritative test as part of normal repository validation.

Use a new authoritative fixture only when no current evidence owner exists.
