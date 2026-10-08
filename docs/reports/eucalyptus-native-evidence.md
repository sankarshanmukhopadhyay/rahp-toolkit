---
layout: default
title: "Eucalyptus native evidence follow-up"
parent: Reference
nav_order: 13
has_toc: true
---
# Eucalyptus native evidence follow-up

The [initial sealed campaign](eucalyptus-clean-room-2026-10-08.md) remains the assessment baseline. [Issue #960](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/960) tracks supplemental evidence; collecting native tests does not automatically close its consequential composition propositions.

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

## Completion boundary

Go and Dart component evidence can resolve their previously unavailable native-execution sub-obligations. Rust results must be read at their actual execution boundary: a compiler, linker, dependency or system-prerequisite failure before tests is not a demonstrated target-control defect. Original diagnostics are retained when prerequisites or build settings are changed for retest.

No consequential proposition is automatically marked PASS by this collector. The 20 retest contracts remain authoritative in [the campaign contract](../../profiles/dtg/eucalyptus/campaign.json). Closure still requires attributable evidence for the exact proposition, including expected/observed effects, relevant policy and state, and specialist or participant observations where applicable.

In particular, runtime privacy captures, real multi-party approval independence, hosted-forge effects, physical mobile approval, induced deployment failures, and accessibility/challenge/redress journeys cannot be inferred from component counts or compiler success. Keep these obligations explicit until those observations are obtained or the assessment scope is deliberately narrowed.
