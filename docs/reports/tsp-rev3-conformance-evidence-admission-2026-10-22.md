---
layout: default
title: "TSP Rev 3 conformance evidence admission"
parent: Reference
---
# TSP conformance evidence admission and source-revision reconciliation

**Campaign:** [#1103](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1103) · **PR:** [#1104](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1104)  
**Evidence class:** third-party, committed historical conformance report; **not** a fresh RAHP test run.  
**Conformance repository pin:** [OpenVTC/tsp-conformance@b89e62869c686841fc98a4386f3b297babad0194](https://github.com/OpenVTC/tsp-conformance/commit/b89e62869c686841fc98a4386f3b297babad0194)  
**Report:** [reports/report.md](https://github.com/OpenVTC/tsp-conformance/blob/b89e62869c686841fc98a4386f3b297babad0194/reports/report.md) (generated 2026-09-16T16:50:41Z, seed 20260916).  
**Source attribution:** suite README and case catalogue identify **TSP Rev 3**, version marker `YTSP-AAC`, upstream source commit abbreviated `f5b8668`. Resolve to full SHA and independently confirm the exact source content before binding this evidence to a final assurance subject.

## 1. Revision boundary

The original RAHP intake pinned upstream repository HEAD `ccda6b33159d860f05c328eb436dabe83548b705`, source file `spec/spec.md`, whose header states **Specification Status: Release 1.0**. The inspected GitHub Pages publication was previously identified as Experimental Implementor's Draft Rev 2. The separate OpenVTC conformance suite targets Rev 3 at `f5b8668`.

**Do not conflate these three labels or silently treat a historical Rev 3 conformance run as evidence for the source at HEAD.** Establish a revision lineage and identify which target is authoritative for the intended review. The source preflight currently targets the HEAD commit, not the conformance suite's Rev 3 pin.

## 2. Historical report admission

| Suite | Pass | Fail | Error | Skip | Bounded interpretation |
|---|---:|---:|---:|---:|---|
| Interoperability | 893 | 0 | 0 | 157 | Tested pairs and supported cases interoperated in that historical run; unsupported paths remain skipped. |
| Negative | 377 | **8** | 0 | 70 | Eight failures require case-level root-cause attribution and regression verification. |
| Relationship | 250 | 0 | 0 | 0 | Tested relationship transitions passed in that run; not proof of deployment authorization. |
| Specification vectors | 152 | 0 | 0 | 23 | Supported vector operations passed; skipped capability cases cannot be counted as passes. |
| **Total** | **1672** | **8** | **0** | **250** | Historical test-case totals only; **not** an assurance score. |

The suite README distinguishes `--gate known` from `--gate all`. The former can succeed with previously catalogued failures, while the latter returns nonzero for any failure. Consequently, a green CI run under the known-failure gate **does not mean zero conformance failures**.

The historical run describes five drivers: affinidi-rust 0.2.0, reference-rust tsp_sdk 0.11.0, tsp-js 0.3.0, Go 0.1.0, and Dart 0.1.0. Their capability matrix contains unsupported operations and unavailable reported fields; do not infer equivalence across all algorithms or modes.

## 3. Case-family-to-assurance mapping

| Case family | Evidence admissible for | Does not establish | Follow-up |
|---|---|---|---|
| Appendix A vectors | Serialization, decoding, expected fields and deterministic encoding in supported drivers | Source-to-deployment identity binding, privacy or governance | Resolve exact Rev 3 pin; verify vector provenance |
| Cross-driver interop | Supported message interchange across tested driver pairs | Untested modes, runtime availability, adverse intermediary behavior | Record per-driver skips and build pins |
| Negative mutations | Bounded rejection behavior for malformed/modified messages | Universal exploit resistance, application-level replay protection | Classify all eight failures by case, driver and cause |
| Relationship protocol | Tested invite/accept/cancel/race transitions | Delegation, authorization, consent or user redress | Add composition policy cases |
| Routed and nested cases | Specific envelope/nesting interoperability | Traffic unlinkability, delivery guarantees, route failure resilience | Route manipulation and metadata tests |
| 2 MiB and long-field cases | Selected large-message encoding/interoperability | Memory/CPU ceilings or overload resilience | DRARM stress/induced-failure tests |

## 4. Cross-lens evidence disposition

| Lens | Historical conformance evidence | Remaining required evidence | Status |
|---|---|---|---|
| RAHP | Indirectly informs scenarios involving relationship correctness | Harm, affected-person, policy and remedy evidence | INDETERMINATE |
| Security | Direct evidence for specific negative mutations; eight failures | Root-cause triage, fresh regressions, threat coverage | INDETERMINATE |
| Combination | Limited multi-implementation interoperability | VID resolution + authority + transport + consuming application | INDETERMINATE |
| DRARM | Some large payload and routing functional cases | Actual resilience catalogue execution, induced failure, DR-A depth | INDETERMINATE |

## 5. Next executable acceptance conditions

- [ ] Resolve `f5b8668` to an immutable full SHA and reconcile Rev 2, Rev 3 and HEAD Release 1.0.
- [ ] Inspect `reports/report.json` and `findings.toml` at the same suite commit to attribute each of the eight negative failures; do not guess their causes.
- [ ] Re-run the suite against exact pinned driver source identities, or explicitly retain the September run as historical evidence.
- [ ] Run canonical RAHP/security records and independent combination review with version-specific assertions.
- [ ] Run DRARM against the selected source and collect induced-failure/runtime evidence where material.
- [ ] Record per-lens source pins, evidence class, achieved depth, residual owner and terminal disposition.
- [ ] Finalize the technical and human-readable reports only after validation.

**Assurance decision:** Evidence **admitted with provenance and scope restrictions**, not promoted to a terminal PASS or certification.
