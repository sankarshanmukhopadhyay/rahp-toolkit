---
layout: default
title: "Assurance registry"
parent: Learn RAHP
nav_order: 6
has_toc: true
---

# RAHP assurance registry

RAHP already maintains reusable assurance knowledge under `method/catalogue/`.
The registry is a **derived discovery and consumption surface over that catalogue**.
It does not introduce a second assurance ontology or a second source of authority.

## Authority boundary

The six canonical portable object families remain:

| Prefix | Type |
|---|---|
| `HRM-*` | harm pattern |
| `RKP-*` | risk pattern |
| `CTP-*` | control pattern |
| `GRP-*` | guardrail pattern |
| `ATP-*` | assurance pattern |
| `EVP-*` | evidence pattern |

Their YAML records under `method/catalogue/` are authoritative for portable
assurance semantics. Existing identifiers remain the stable identifiers. The
registry does not mint replacement IDs.

Deployment-local findings, evidence and dispositions remain authoritative for
the particular assessment in which they were produced. Referencing a portable
catalogue ID does not establish that the corresponding risk, harm, control or
assurance conclusion exists in a target system.

## Build the registry index

Run:

```bash
python3 tools/build_assurance_registry.py
```

This produces:

```text
build/assurance-registry.json
```

The generated file contains, for every portable object:

- stable catalogue identifier;
- object type;
- human-readable name and concise semantic summary;
- canonical source path;
- typed relationships to other portable catalogue objects.

The registry builder rejects duplicate identifiers, unresolved portable
references, inconsistent catalogue versions and malformed relationship lists.

To verify that a committed generated index is current:

```bash
python3 tools/build_assurance_registry.py --check
```

To consume the index without writing a file:

```bash
python3 tools/build_assurance_registry.py --stdout
```

## Consumption pattern

Consumers should retain the portable catalogue identifier directly:

```yaml
portable_assurance:
  risk_patterns:
    - RKP-AUTH-02
  assurance_patterns:
    - ATP-AUTH-02
```

A consumer may use `build/assurance-registry.json` to discover the object type,
summary, source file and adjacent portable relationships for those identifiers.

The index is deliberately descriptive. It does not imply:

- that a portable pattern is applicable to a particular target;
- that an assessment finding exists;
- that evidence has been collected;
- that a control is implemented or effective;
- that RAHP supersedes an upstream specification or deployment authority.

## Why this is a registry rather than a second catalogue

The portable catalogue answers **what the reusable assurance semantics are**.

The derived registry index answers **how another tool or assessment can discover
and resolve those semantics by stable identifier**.

Keeping these concerns separate avoids semantic duplication while making the
existing catalogue easier to consume programmatically.

## Validation

The registry path is covered by unit tests that establish:

- the current catalogue can be indexed deterministically;
- IDs remain unique;
- entries are sorted deterministically;
- duplicate IDs fail closed;
- unresolved portable references fail closed.

The existing catalogue schema and `tools/validate_catalogue.py` remain the
authority for full catalogue-record validation.
