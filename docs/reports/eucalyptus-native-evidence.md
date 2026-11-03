---
layout: default
title: "Eucalyptus native evidence follow-up"
parent: Reference
nav_order: 13
has_toc: true
---
# Eucalyptus native evidence follow-up

The [initial sealed campaign](eucalyptus-clean-room-2026-10-08.md) remains the assessment baseline. [Issue #960](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/960) tracks supplemental evidence; collecting native tests does not automatically close its consequential composition propositions.

## Published native result

The [retained native packet](../../instances/dtg/reviews/eucalyptus-native-2026-10-08/report.md) records the completed [CI run](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37733481776): 26 attempts, with 19 passing, four nonzero and three unavailable. Eight focused consuming-path fixture suites passed. Aggregate counts are 11,528 passing events, including partial passes from failed attempts; these counts overlap and are not assurance claims. The exact downloaded archive, original machine records and detailed residual disposition are retained with their verified hashes. Overall assurance remains INDETERMINATE and all 20 consequential propositions remain evidence-required.

## Run the supplemental collector

Provision Rust 1.95.0, Go 1.27.0, Dart 3.10.0, Python 3.11+ and RAHP dependencies. Linux Rust builds also need the system prerequisites declared by the tagged projects, including D-Bus development headers and `pkg-config`; OpenVTC also requires PC/SC headers. Apple tests require the actual supported Apple platform/toolchain and binary inputs.

Use the exact source trees collected by the original campaign, or acquire them through its source-verification helper. Never substitute current development branches. The collector checks commit/tag identities and tracked cleanliness before and after execution. Generated build inputs are recorded separately.

```bash
python3 tools/eucalyptus_native_evidence.py \
  --sources /tmp/eucalyptus-fresh-960/sources \
  --output /tmp/eucalyptus-native-960
python3 tools/eucalyptus_campaign.py --verify-package /tmp/eucalyptus-native-960
```

The output directory must be new. A completed indeterminate assessment returns zero; orchestration failure returns nonzero and preserves a failure record if output was created. Each attempt has a bounded timeout, recorded in the run contract. The optional `--timeout-seconds` accepts 30–3,600 seconds; its default is 900. Repeated `--suite` selects exact registered identifiers in the requested order.

For a bounded transport retest, resolve Dart dependencies from the tagged workspace first:

```bash
cd /tmp/eucalyptus-fresh-960/sources/affinidi-tsp-dart
dart pub get
```

Then, from RAHP:

```bash
python3 tools/eucalyptus_native_evidence.py \
  --sources /tmp/eucalyptus-fresh-960/sources \
  --output /tmp/eucalyptus-transport-960 \
  --suite go-tsp --suite dart-tsp-package
```

The original `dart-tsp` invocation is retained in the full plan. Its root-relative invocation encounters package-relative fixture paths; `dart-tsp-package` runs the unchanged tests from their package directory. Original nonzero output and the corrected run remain distinct.

The existing **Clean-room assurance executor** has `run_mode=eucalyptus-native`. It provisions exact toolchains, collects all source pins, resolves Dart dependencies, runs native component and selected consuming-path suites, verifies the seal and uploads full evidence. Evidence branches beginning `assessment/eucalyptus-evidence-` also trigger this job on pull requests, so an ordinary native runner can test the same inputs independently of the interactive execution substrate. A green collection job means collection completed, not that every target attempt passed.

## What the packet establishes

The collector records actual commands, version output, source identities, assessor implementation hashes, build environment, stdout/stderr, test events and actual build inputs. A snapshot of the assessor implementation accompanies each new packet. Cargo requires counted passing tests, Go counts test-level events rather than package success, and Dart excludes hidden setup and skipped events. Exit zero with no tests or contradictory events is not credited as a native PASS.

The tagged credentials library does not track a root `Cargo.lock`. Its supplemental command explicitly permits fresh dependency resolution and preserves the resulting lockfile. This is a bounded test of the tagged source with recorded resolved inputs; it is not falsely described as a release-locked build. Recorded `go.mod`/`go.sum` and Dart lockfiles similarly bind the actual inputs used.

The native plan separately exercises the tagged VTC sender-binding, self-edit and approval tests; VTA freshness and refresh tests; room lifecycle/host tests; hidden vetting; and native E2E fixtures. Source-compatible native fixture execution is useful evidence, but fixture identities do not demonstrate independent real people, and fixture mediators do not establish every deployed transport/observer surface.

## Issue #965: reproducible diagnostic retests

The historical Eucalyptus native packet remains unchanged. [Issue #965](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/965) owns three precise native-execution gaps: an OpenVTC vetting assertion, nine trust-registry DIDComm integration tests that lacked a configured client, and the full VTI workspace timeout. The following diagnostics add *new* evidence and never rewrite the original failures. The exact pinned revisions are in `profiles/dtg/eucalyptus/campaign.json`.

### Focused OpenVTC reproduction

Use an isolated source workspace with the pinned campaign checkouts. Rust 1.95.0 and the existing native workflow prerequisites are required.

```bash
python3 tools/eucalyptus_native_evidence.py \
  --sources /tmp/eucalyptus-fresh-960/sources \
  --output /tmp/eucalyptus-965-focus \
  --diagnostics-965 \
  --suite openvtc-vetting-focus \
  --timeout-seconds 900
python3 tools/eucalyptus_campaign.py --verify-package /tmp/eucalyptus-965-focus
```

This executes the **unchanged** target test `no_ticket_is_issued_for_requests_that_cannot_be_attested` under the release's `openvtc` crate. Interpret a failed assertion as a bounded target test failure, not by itself as a production exploit. A passing rerun establishes only this focused test at the recorded pin, environment and run. Repeat independently if distinguishing deterministic, order-dependent and resource-dependent outcomes.

### Trust-registry integration prerequisites

The test requires actual operator-controlled DIDComm integration infrastructure. Supply `CLIENT_DID`, `CLIENT_SECRETS` (nonempty JSON array), `MEDIATOR_DID` and `TRUST_REGISTRY_DID` via the runtime environment; do **not** commit `.env.test` credentials or fabricate a DID or mediator to make the checks run.

```bash
python3 tools/eucalyptus_native_evidence.py \
  --sources /tmp/eucalyptus-fresh-960/sources \
  --output /tmp/eucalyptus-965-registry \
  --diagnostics-965 \
  --suite registry-didcomm-integration
```

If prerequisites are missing or invalid, the sealed packet records `ATTEMPTED_UNAVAILABLE` and the **names** of missing variables. It does not execute the tests and does not retain their values. Present but unreachable or unauthorized external services may still yield a nonzero test execution, which requires diagnosis, not an automatic implementation FAIL. **The live test runtime may itself emit sensitive information**: only run with nonproduction controlled test accounts, restrict access to logs/artifacts and review their contents and retention before external publication. The PR-triggered probe deliberately supplies no credentials.

### Complete VTI workspace-member partition

To avoid interpreting a 900-second full-workspace timeout as a software failure, this tool can derive a **non-overlapping package selection** from the exact pinned VTI `Cargo.toml` workspace members and each member's package name. It rejects missing, wildcard or duplicate member manifests. Partition coverage means every *declared package* is selected once; it does **not** prove all feature combinations, cross-package behavior or that a package's tests executed.

```bash
python3 tools/eucalyptus_native_evidence.py \
  --sources /tmp/eucalyptus-fresh-960/sources \
  --output /tmp/eucalyptus-965-vti-partition \
  --diagnostics-965 --vti-partition \
  --timeout-seconds 900
python3 tools/eucalyptus_campaign.py --verify-package /tmp/eucalyptus-965-vti-partition
```

This optional partition is resource-intensive. Budget runner time and storage before invoking it; each package is tested independently using `cargo test --locked -p <package>`. The generated run contract preserves the exact selected member, command, source and resolved build inputs; attempts retain stdout, stderr, timeout/nonzero counts and reason. Evaluate unavailable or zero-test packages individually and do not aggregate partial package PASS into a full-workspace PASS.

### Qualification and closure

Review `run-contract.json`, `attempts.json`, `summary.json`, `report.md` and the verified evidence seal. Preserve the original #960/#964 immutable records. A successful packet-verification check proves local integrity against the generated manifest, **not** independent attestation or the absence of production defects.

Close #965 only when the focused OpenVTC failure, registry integrations and VTI workspace have each received a reproduced PASS, reproduced FAIL or explicit unavailable classification with a retest condition; all conclusions must be source-pinned and correctly distinguish target test execution from deployed composition. Unavailable infrastructure does not discharge the related EUC assurance obligations. Source-compatible Lab consuming-path evidence belongs separately to [#966](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/966).

## Completion boundary

Go and Dart component evidence can resolve their previously unavailable native-execution sub-obligations. Rust results must be read at their actual execution boundary: a compiler, linker, dependency or system-prerequisite failure before tests is not a demonstrated target-control defect. Original diagnostics are retained when prerequisites or build settings are changed for retest.

No consequential proposition is automatically marked PASS by this collector. The 20 retest contracts remain authoritative in [the campaign contract](../../profiles/dtg/eucalyptus/campaign.json). Closure still requires attributable evidence for the exact proposition, including expected/observed effects, relevant policy and state, and specialist or participant observations where applicable.

In particular, runtime privacy captures, real multi-party approval independence, hosted-forge effects, physical mobile approval, induced deployment failures, and accessibility/challenge/redress journeys cannot be inferred from component counts or compiler success. Keep these obligations explicit until those observations are obtained or the assessment scope is deliberately narrowed.
