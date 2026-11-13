---
layout: default
title: "External conformance kit"
parent: Implement RAHP
nav_order: 8
has_toc: true
---
# External implementation conformance kit

This **bounded, executable consumer exercise** invokes an independently implemented local adapter against the existing RAHP shared fixture suite. It is an implementation aid, **not** certification, methodological acceptance, a deployment assurance determination, or evidence of independent adoption.

## Authority and scope

Authoritative inputs remain `method/engine-contract.yaml` (family `rahp-engine-contract-v1`, revision `1.3`), `method/versioning.yaml`, the normalized-result schema v1, the evidence-retention policy and `tests/conformance/`. This runner does **not** change any of them.

The current runner covers three operations: `validate-result`, `retention-plan`, and `correlate-trigger`. Remaining engine operations appear in `untested_operations`. A report with all tests passing demonstrates only the declared fixture subset.

## Run from a clean checkout

Install the repository's existing Python requirements, then from the repository root run:

~~~bash
python3 tools/run_external_conformance.py \
  --adapter examples/external-conformance/adapter.py \
  --implementation external-fixture-adapter \
  --implementation-version 0.1 > /tmp/rahp-external-conformance.json

python3 -m unittest tests.test_external_conformance -v
~~~

The example adapter implements its behavior using the **published JSON Schema and retention policy**, without importing RAHP Python reference-engine modules. It is a maintained teaching adapter, not an independent external project's adoption record. Its deliberate subset coverage must not be interpreted as support for the full engine contract.

## Executable adapter interface

The runner invokes a **trusted executable** without a shell:

~~~text
<adapter> <operation> <absolute-input-path> --contract-root <absolute-repository-root>
~~~

The adapter must return **one JSON object** on standard output and exit zero on a successful protocol invocation:

- `validate-result`: `{"valid":true}` or `{"valid":false}` (the latter is the correct answer for an invalid fixture).
- `retention-plan`: the existing normalized retention-plan shape, including `policy`, `assessment`, and ordered `actions`.
- `correlate-trigger`: the existing `{"action":"create",...}` or `{"action":"coalesce",...}` projection.

These are fixture-runner conventions for the **tested operations**, not a newly normative engine API. A custom implementation can use a wrapper script to translate its native command interface to this protocol. The runner supplies the authoritative contract root; the adapter must not import RAHP reference code for a claimed independent implementation exercise.

Only invoke executables you trust: the runner provides **no sandbox**, and local adapters have the operating system privileges of the invoking user. There is no network retrieval by the runner and no privileged repository mutation.

## Interpreting the report

The runner emits deterministic JSON `rahp-external-conformance-report/v1`, containing the declared implementation identity/version, claimed contract family/revision/result schema, each executed fixture, outcome (`PASS`, `FAIL`, `ERROR`), summary counts, untested operation IDs, and explicit limitations.

- `PASS`: the adapter's response matches a fixture or the authoritative evidence-retention policy.
- `FAIL`: the adapter responded but disagreed with the expected behavior.
- `ERROR`: preflight, timeout, process failure, or malformed response prevents determination.
- `NOT_TESTED`: reserved outcome for future fixture selection; untested operations are listed separately rather than represented by fabricated PASS results.

The exit status is **zero only when all executed fixtures pass**. An unsupported contract family, revision or result-schema claim is rejected before running the adapter.

## Negative-path reproduction

~~~bash
python3 tools/run_external_conformance.py \
  --adapter examples/external-conformance/adapter.py \
  --implementation example --implementation-version 0.1 \
  --revision 9.9
~~~

This command returns a machine-readable preflight `ERROR` and nonzero exit. The unit tests also inject an always-valid adapter, missing executable, and a timed-out adapter to demonstrate false-success refusal.

## Limitations and challenge

The adapter identity and version are caller-declared. The runner tests only fixture outputs; it neither authenticates executable provenance nor tests live deployment, security, risk judgments or complete engine behavior. It is **not a conformance certificate**, nor proof of independent third-party adoption. An independent reviewer can challenge claims by reviewing the selected fixtures, pinned version metadata, adapter source, negative tests and the report.

For the normative contract boundary and existing differential Python/TypeScript checks, see [Implementation conformance](conformance.md) and [Engine contract](engine-contract.md).
