---
layout: default
title: "CI assurance propositions"
nav_order: 9
parent: Learn RAHP
---
# CI assurance propositions

RAHP treats expensive CI checks as assurance propositions rather than optional build conveniences. A check may be skipped only when a governed impact decision establishes that the changed surface cannot affect the proposition the check proves.

## Python-TypeScript conformance

The repository-wide contract is `method/ci-assurance-propositions.yaml`. It declares the affected path surface, workflow owner, fail-safe behavior and full-validation backstops for Python↔TypeScript reference conformance.

For ordinary pull requests and pushes to `main`, `.github/workflows/validate.yml` classifies the changed paths with `tools/typescript_ci_impact.py`.

- **REQUIRED — affected assurance paths:** the TypeScript workspace and Python↔TypeScript conformance validator run.
- **SKIPPED — proposition unaffected:** the `TypeScript conformance` job remains visible and records why Node/npm/TypeScript execution was not required.
- **REQUIRED — fail-safe:** unavailable, empty or otherwise unclassifiable change information cannot produce a skip.

Scheduled and manually dispatched full validation always require the proposition regardless of changed paths. `.github/workflows/release.yml` is an independent unconditional backstop and runs Python↔TypeScript conformance before release publication; it does not consult the impact classifier.

## Repository-wide ownership

`tools/validate_ci_assurance.py` verifies that the declared contract and actual workflow topology remain synchronized. In particular it checks that:

- the normal validation workflow owns proposition-sensitive execution;
- schedule and manual-dispatch full validation retain the `--full` backstop;
- release publication runs conformance unconditionally;
- no specialist workflow silently acquires duplicate ownership of Python↔TypeScript conformance;
- changes to the policy, classifier, repository validator, conformance validator and owning workflows themselves force conformance.

`tests/test_ci_assurance.py` binds this repository contract into the normal `test_*.py` discovery gate, so ownership drift fails ordinary validation.

Run the checks locally with:

```bash
python3 tools/typescript_ci_impact.py --self-test
python3 tools/validate_ci_assurance.py
python3 -m unittest tests.test_ci_assurance
```

## Scope boundary

This contract governs Python↔TypeScript conformance only. It does not imply that CAWG checks, DTG cross-specification tests, historical release qualification, Pages validation or other RAHP assurance domains should become path-sensitive. Any such expansion requires its own proposition definition, pressure tests and evidence.
