# RAHP consumption of DTFC observability vectors

**Status:** experimental negative-test integration; not a controller, normative method, privacy assessment, or operational evidence adapter.

## Data flow

1. DTFC authors `research/observability/synthetic-vectors-v1.json` under contract `dtfc-observability-synthetic-vectors/v1`.
2. RAHP vendors the reviewed byte-identical snapshot at `examples/observability-dtfc/synthetic-vectors-v1.json`.
3. `tests/test_observability_dtfc_vectors.py` checks the snapshot's pinned Git blob SHA-1 (`d5844a78206ea442a23a2bdc0e9fdc4140485cb5`) and calls `tools.observability_harm.evaluate_observability` for every vector.
4. Exact `state` and `reason` must match. Neither the fixture nor the test establishes a verified real-world incident.

**Pinning distinction:** Git blob pinning detects changes to the vendored fixture bytes relative to the reviewed snapshot; it is not a digital signature, an independent attestation of source ownership, or proof that synthetic event assertions are true.

## Reproduce

From the RAHP repository root:

```sh
python -m unittest discover -s tests -p 'test_observability_harm.py' -v
python -m unittest discover -s tests -p 'test_observability_dtfc_vectors.py' -v
python3 tools/validate.py
python3 tools/validate_reference_links.py
```

Use the repository's standard CI for complete qualification. A failing exact-match test indicates fixture/consumer divergence, not by itself a deployed-system failure.

## Interpretation

- `FAIL / cross-context-trace-correlation`: a synthetic repeated identifier spans declared contexts while correlation is prohibited.
- `FAIL / telemetry-promoted-to-authority`: a synthetic consequential action explicitly declares telemetry as source.
- `INDETERMINATE / insufficient-observation-evidence`: evidence is absent or unavailable.
- `INDETERMINATE / no-failure-observed-not-proof-of-safety`: a clean fixture does not prove privacy or authorization safety.

The evaluator is deliberately narrow. It does not test data retention, deletion, processor access, independently authenticated decision provenance, or multi-event causality. Its `verified` field is an author assertion, not a verified assurance state. It does not alter the RAHP controller's decision states or permit telemetry to grant authorization.

## Maintenance and change control

DTFC is the vector source of truth. Review changes there first; verify new vector contract and exact expected results; then import the bytes into RAHP and update the Git blob pin in the regression test. Run both repositories' validation checks. If a vector changes semantics, record why and whether it affects previous results; do not claim automatic backward compatibility. Keep the fixture entirely synthetic.

## Completion evidence

RAHP original [#981](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/981) / [PR #982](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/982), squash commit `370519fcdf3626d01f0d5b20d36da9a2110ee20b`. DTFC original [#105](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/105) / [PR #106](https://github.com/qbf-consulting/digital-trust-failure-corpus/pull/106), squash commit `bb1ec2304643040836da348f0f1ca4e08d9dfbbb`.

DTFC vectors [#107](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/107) / [PR #108](https://github.com/qbf-consulting/digital-trust-failure-corpus/pull/108), squash commit `8c2a4ef1d8cefaa1457861bc5ecbd0c9f93afecf`. RAHP consumer [#983](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/983) / [PR #984](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/984), squash commit `dc45a2ed538831f57bf93a9d36b7cde6aada5066`.

All four PRs passed their respective GitHub Actions validation before merge. These checks support repository-level regression claims, not independent adoption or production privacy assurance. No standalone release was cut for this tranche.
