# RAHP Increment 6 — contract ownership and accepted-dependency audit

Tracking: ToIP RAHP Task Force upstream convergence #17, Increment 6. This document records the **supported, declared compatibility surface**, not a claim about arbitrary external or dynamic consumers.

## Source-pinned baseline

- Accepted upstream source: `448e2ff4ca7f747ca899e0e845adfe45f750f094`.
- Downstream baseline: `a4134007c4bf09eda9587c31ff8de76dd7b57c86`.
- Proposed upstream validation-hardening PR #22 head `bbe06e3269a6330b64c52ce54ede4e74522ca292` is **unmerged** and cannot be used as authoritative input.
- Previously qualified bounded comparisons: downstream PRs #1137 (source integrity), #1138 (review schema), #1139 (evidence/reassessment) and #1140 (consumer-need decision).

## Ownership and dependency inventory

| Contract / function | Authority | Supported downstream behavior |
| --- | --- | --- |
| `review/spec-review.schema.json`, `review/validate_spec_review.py`, `method/vocabularies.yaml` | Accepted upstream task-force repository | Invoke accepted upstream validation; do not transplant the schema into a downstream canonical review definition |
| `review/source_integrity.py`, `review/examine.py` and VRC `evaluate.py` | Accepted upstream helpers and **example-local** evaluation | Execute pinned positive and negative probes; do not infer deployment assurance or universal evidence contract |
| `tools/review.py` | Downstream Toolkit | Its own pressure-test/security/combined records |
| `tools/assessor_contract.py`, `tools/evidence_provenance_router.py` | Downstream Toolkit | Specialist result and provenance obligations; not upstream review statuses |
| `examples/standalone-trqp/replay.py` | Downstream Toolkit example | Hardened source-integrity replay; bounded outcome comparison to upstream |
| `tools/upstream_*boundary.py`, `tools/upstream_review_consumer_decision.py`, `tools/source_integrity_compat.py` | Downstream test harness | Pin and **exercise** accepted upstream definitions, without copying their canonical source files |

No generic adapter was justified for the named downstream consumers at PR #1140. This is a conscious supported interface boundary, not a proof that all possible unexamined files have no overlapping definitions.

## Executable audit

```sh
python3 -m unittest discover -s tests -p 'test_upstream_contract_ownership_audit.py' -v
python3 tools/upstream_contract_ownership_audit.py --upstream /trusted/accepted/upstream --downstream . --output ownership.json
```

CI checks out the exact accepted upstream commit, verifies required owned interfaces are present and content-digested, checks upstream `rahp-spec-review/v1` authority and prevents a direct conflicting upstream schema clone at the targeted downstream canonical schema location. It confirms that the existing downstream `validate.yml` pins accepted upstream and does not substitute the unmerged PR #22 head. Missing source files fail closed. JSON output contains source file paths and SHA-256 digests for reproduction.

## Acceptance disposition and limits

**Canonical definitions:** For the **declared review/source/example compatibility surfaces**, ownership is explicit, the accepted upstream schema is referenced rather than redefined as the downstream canonical schema, and documented downstream contracts are separate. Do not claim repository-wide proof of zero conflicting definitions without a larger inventory.

**Unpublished dependency:** For the **supported cross-repository CI compatibility paths**, source is checked out by immutable accepted upstream revision; the known unmerged PR #22 head is not used. This is not a proof that no external/private third-party dependency exists anywhere, nor a prediction about future acceptance of PR #22. Reconcile when #22 is merged or explicitly rejected.

A clean run qualifies these bounded integration criteria and supports marking Increment 6 complete **for its declared supported surface**, while retaining the compatibility and unfamiliar-adopter limits for Increment 7. It does not establish a normative shared sidecar format, general schema conversion, target assurance or independently reviewed code. AI-assisted implementation; independent reviewability APPLICABLE, with reproducible commands and adversarial missing/unsafe input tests.
