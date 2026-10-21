---
layout: default
title: "TSP negative-test failure triage"
parent: Reference
---
# TSP Rev 3 negative-test failures: evidence-grounded triage

**Campaign:** [#1103](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1103) · [draft PR #1104](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1104)  
**Evidence source:** [OpenVTC/tsp-conformance@b89e62869c686841fc98a4386f3b297babad0194](https://github.com/OpenVTC/tsp-conformance/commit/b89e62869c686841fc98a4386f3b297babad0194), `reports/report.md` and `findings.toml`. Historical report generated 2026-09-16.  
**Affected driver in that run:** `reference-rust`, library `tsp_sdk` 0.11.0.  
**Scope:** historical test observations, not independently reproduced in this RAHP tranche.

## Case-level accounting

| Finding | Case identifier | Historical observation |
|---|---|---|
| sdk-non-canonical-lead-bytes | `negative/resigned/direct-signed-only/non-canonical-lead-byte` | Re-signed noncanonical data accepted |
| sdk-trailing-bytes | `negative/self/hpke-base/trailing-bytes` | Appended bytes accepted |
| sdk-trailing-bytes | `negative/vector/direct-hpke-base/trailing-bytes` | Appended bytes accepted |
| sdk-trailing-bytes | `negative/vector/direct-signed-only/trailing-bytes` | Appended bytes accepted |
| sdk-trailing-bytes | `negative/vector/direct-sealed-box/trailing-bytes` | Appended bytes accepted |
| sdk-trailing-bytes | `negative/vector/control-rfi-direct/trailing-bytes` | Appended bytes accepted |
| sdk-trailing-bytes | `negative/vector/direct-hpke-base-pq/trailing-bytes` | Appended bytes accepted |
| sdk-signed-only-essr | `negative/resigned/direct-signed-only/essr-sender-mismatch` | Re-signed mismatched ESSR sender accepted |

**Reconciliation:** 1 + 6 + 1 = **8**. All eight appear in the historical report's *Findings* section, with no need to invent an unclassified failure category.

## Findings and implications

### TSP-NEG-01 — Noncanonical CESR lead bytes

**Source classification:** `spec-violation`. The conformance finding cites §3.7's mandatory rejection of primitives with non-zero pad bits. The test edits the signed-only vector's lead byte, re-signs with the published sender key, and observes `tsp_sdk` returning a decoded payload. The findings register attributes this to `cesr/decode.rs` skipping rather than validating lead bytes. **Consequence hypothesis:** alternative byte representations of one decoded value may undermine canonicalization-sensitive equality, digest, deduplication or policy decisions. This is **not** proof of an exploitable authorization bypass.

**Next evidence:** reproduce on a pinned `tsp_sdk` checkout; inspect current decoder and regression tests; determine whether the defect remains in maintained versions; measure any composition effects.

### TSP-NEG-02 — Trailing bytes after signature attachment

**Source classification:** `disagreement`. The reference SDK deliberately treats trailing data as potentially subsequent transport content; other drivers reject it as trailing bytes. The findings register states that the specification does not explicitly settle whether a TSP message must occupy the whole transport unit. Six message sources exercise the same interpretive boundary. **Consequence hypothesis:** inconsistent wire-byte identity and message boundary assumptions could affect a mediator's deduplication, framing or audit records.

**Next evidence:** decide normative message-boundary semantics; specify stream framing versus whole-message validation; test mixed-implementation transport and deduplication behavior. Do not classify this as an unequivocal violation before the rule is settled.

### TSP-NEG-03 — Signed-only ESSR sender mismatch

**Source classification:** `disagreement`. A re-signed signed-only message contains the sender VID of a different party in the payload while the envelope names the signer. The reference SDK accepts; other drivers reject. The findings register says sender-field matching is explicit for confidential variants but not explicitly settled for signed-only messages. **Consequence hypothesis:** applications that consume the payload sender without binding it to the authenticated envelope sender could misattribute actions.

**Next evidence:** clarify the signed-only sender-binding requirement; check actual application behavior and delegation/authorization controls; rerun negative tests against the clarified rule.

## Cross-lens routing

| Finding | Security | Combination | RAHP / human harm | DRARM |
|---|---|---|---|---|
| NEG-01 | Canonical parser rejection and digest behavior | Parser → cache/dedup/signature interpretation | Disputed or misattributed transaction only if downstream effects are demonstrated | Not directly established |
| NEG-02 | Frame boundary and trailing data | SDK → transport → mediator dedup/audit | Duplicate or disputed effects require application evidence | Possible duplicate-work amplification; requires induced failure |
| NEG-03 | Sender identity consistency | Authenticated envelope → application principal/authorization | Potential impersonation or misattribution; conditional on consumption | Not directly established |

**Assurance dispositions:** Security **INDETERMINATE**, composition **INDETERMINATE**, RAHP **INDETERMINATE**, DRARM **INDETERMINATE**. The historical findings are evidence of specific observed nonconformances/disagreements, not an overall security certification or a complete four-lens run.

## Evidence limitations

- No claim is made that the September failures persist in current library releases.
- The conformance suite targets Rev 3 (`YTSP-AAC`, abbreviated source `f5b8668`); the RAHP source preflight targets a later HEAD commit. Source equivalence is unresolved.
- The conformance suite's `known` CI gate may accept catalogued failures. Its green status cannot be read as a zero-failure result.
- Driver capability skips are not passes, and historical conformance results do not demonstrate runtime resilience or harms outcomes.
