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


## November 3 source-pinned diagnostic disposition (#965)

The first focused retest produced [workflow run 41566442929](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/41566442929) and [artifact 13198987565](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/41566442929/artifacts/13198987565) (`eucalyptus-native-evidence-41566442929`). The downloaded ZIP digest was independently checked against the uploaded artifact digest, `sha256:cc383775a85af7c84165caace5d569f97538f6c81458c5d4f8bcfac830b643cf`. The inner OpenVTC stdout and stderr match the machine-recorded SHA-256 digests, respectively `5909271bf63df3884dd8d852353032e29e1743686e2012061d8e54625b065f40` and `800d613de59285f837304a49c1bfb9642092949ad5addac84443971bd0281fd5`. No credentials are included here.

### Observed test failure and cause classification

The exact Eucalyptus source `OpenVTC/openvtc@2a4fa2b3c8e831dbe3184a1119c4c87b6f197220` executed:

```text
cargo test --locked -p openvtc no_ticket_is_issued_for_requests_that_cannot_be_attested
```

Its native output reports **one failed test, zero passing tests and 957 filtered-out tests**, with exit code 101. The failed assertion is at [`openvtc/src/state_handler/vetting_actions.rs:7280–7283`](https://github.com/OpenVTC/openvtc/blob/2a4fa2b3c8e831dbe3184a1119c4c87b6f197220/openvtc/src/state_handler/vetting_actions.rs#L7280-L7283). It expects the token-drawing explanation, but the refusal says the community has **no token label to draw under yet**. The underlying refusal remains a *denial*; this particular failure does **not** demonstrate issuance of an unauthorized vetting ticket.

The frozen fixture defines October 2026 token labels in [`hidden_vetter_book`](https://github.com/OpenVTC/openvtc/blob/2a4fa2b3c8e831dbe3184a1119c4c87b6f197220/openvtc/src/state_handler/vetting_actions.rs#L6723-L6769), while the failing test uses wall-clock `Utc::now()`. The expected token-window wording depends on that clock. The evidence supports a **time-dependent test expectation/fixture defect** at the frozen revision, not a demonstrated target-control failure. It was observed in the initial October native packet and again under the focused November 3 command.

An independently inspected *later upstream source commit*, [`OpenVTC/openvtc@f8bc18d`](https://github.com/OpenVTC/openvtc/commit/f8bc18d632e3f48af64b7fe226dc34ef87172c9b) (October 14, 2026), changes this test to a fixed October 5 time and explicitly documents why the wall clock was inappropriate. That is **source-observed correction in a later revision**, not an executed regression PASS for that revision and not permission to change the Eucalyptus tag. The original artifact remains a valid historical observation.

### Other two execution boundaries

The trust-registry integration was **not executed** in the November 3 job. `CLIENT_DID`, `CLIENT_SECRETS`, `MEDIATOR_DID` and `TRUST_REGISTRY_DID` were absent, and the collector correctly retained `ATTEMPTED_UNAVAILABLE`, return code null and empty logs. No actual registry or mediator test outcome is established. This work needs controlled test identities and external runtime access; do not use placeholder credentials to turn unavailability into success.

The full VTI `cargo test --locked --workspace` remains unqualified after its historical 900-second timeout. PR #1168 introduced manifest-driven package partitions, but **this retest packet did not execute the complete partition**. The retained timeout is a resource/execution boundary, not evidence of defective VTI behavior. Partition coverage and runtime test results remain to be produced independently.

### Current assessment and retest gates

| Boundary | Established | Not established | Next qualification |
|---|---|---|---|
| Frozen OpenVTC test | Repeat observed FAIL, attributable clock-dependent expectation; later upstream source correction | Later-source executable PASS or deployed defect | Optional targeted execution against *explicitly separately pinned* corrected upstream revision, preserving release/tag separation |
| Registry DIDComm suite | External prerequisites absent; no tests executed | PASS, FAIL, or interoperability | Controlled nonproduction mediator + registry execution, private logs and attributable result |
| Full VTI workspace | Historical timeout; optional package-partition tool exists | Complete partition execution or workspace PASS | Bounded partition with per-member status, verified source manifest and sealed logs |

**Result:** the diagnostic analysis has materially narrowed the first #965 uncertainty. **#965 remains open** for the unexecuted integration and partition boundaries. The twenty consequential Eucalyptus propositions remain evidence-required. No finding is automatically elevated from a component-level test, later-source inspection, or workflow success to composition assurance. The first test finding should not be escalated to an upstream implementation-defect report without contrary target-runtime evidence.

## Completion boundary

Go and Dart component evidence can resolve their previously unavailable native-execution sub-obligations. Rust results must be read at their actual execution boundary: a compiler, linker, dependency or system-prerequisite failure before tests is not a demonstrated target-control defect. Original diagnostics are retained when prerequisites or build settings are changed for retest.

No consequential proposition is automatically marked PASS by this collector. The 20 retest contracts remain authoritative in [the campaign contract](../../profiles/dtg/eucalyptus/campaign.json). Closure still requires attributable evidence for the exact proposition, including expected/observed effects, relevant policy and state, and specialist or participant observations where applicable.

In particular, runtime privacy captures, real multi-party approval independence, hosted-forge effects, physical mobile approval, induced deployment failures, and accessibility/challenge/redress journeys cannot be inferred from component counts or compiler success. Keep these obligations explicit until those observations are obtained or the assessment scope is deliberately narrowed.
