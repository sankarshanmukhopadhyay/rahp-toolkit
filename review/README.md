# RAHP independent review working pack

This directory is the reviewer entry point for the RAHP Toolkit independent-review candidate programme tracked in #747.

## Review posture

The purpose of this pack is to make RAHP easy to challenge, not easy to approve. Reviewers are invited to falsify material claims, force incomplete or contradictory evidence through the system, challenge provenance and independence, replay stale evidence, and distinguish workflow success from assurance success.

No document in this directory is itself assurance evidence. The normative portable surfaces remain the contracts and schemas identified by `method/versioning.yaml`.

## Start here

1. [External review charter](../docs/review/external-review-charter.md)
2. [Architecture and trust boundaries](../docs/review/architecture-and-trust-boundaries.md)
3. [Threat model](../docs/review/threat-model.md)
4. [Known limitations and residual risk](../docs/review/known-limitations.md)
5. [Reproduction guide](../docs/review/reproduction.md)
6. [Claim/evidence/falsification ledger](../method/review/claim-evidence-ledger.yaml)
7. [False-assurance challenge matrix](../method/review/false-assurance-challenges.yaml)

## Stable boundary under review

- Toolkit release: `v2.4.0`
- Engine contract: `rahp-engine-contract-v1`, revision `1.3`
- Normalized result schema: `1`
- Evidence retention contract: `rahp-evidence-retention-v1`

The release is already a qualified stable RAHP release. Independent-review readiness is a separate claim and is not implied by release qualification.

## Reviewer operating rule

A review result should be source-pinned and should preserve unresolved uncertainty. Unexpected PASS/GREEN under a challenge that removes required evidence is a defect. The fixture must not be weakened merely to make the test pass.

## Validation

Run:

```bash
pip install -r requirements.txt
python3 tools/validate_review_readiness.py
python3 tools/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

The repository CI performs the broader validation suite. A green workflow is operational evidence that the checks ran successfully; it is not an assurance conclusion.
