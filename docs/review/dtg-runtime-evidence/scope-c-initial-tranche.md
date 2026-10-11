# Scope C initial runtime tranche — VTA-held-key protocol signatures

Issue: #994  
Source residual: #993  
Finding: `220fb4eea5c0200f190b`  
Scope: `keys/sign-jws/0.1` and `keys/sign-csr/0.1` protocol signatures from a VTA-held key

## Purpose

This file starts the first runtime evidence tranche for #994. It does not claim that the evidence has already been collected. It identifies the bounded cases that should be attempted first because they are most amenable to local or fixture-based reproduction.

## Why Scope C first

Scope C is the smallest executable surface among the three #994 scopes. It can be driven with protocol-signing request fixtures and expected positive/negative results before the broader VTC portal, browser plugin, wallet, VTA and foreign-protocol integration environments are available.

## Initial tranche cases

| Case | Operational state | Expected result | Evidence objective |
|---|---|---|---|
| `C01-valid-sign-jws` | `local-reproducible` | `PASS` | Valid `sign-jws` request produces a protocol-valid JWS from custodian-built signing input. |
| `C02-sign-jws-prohibited-header` | `local-reproducible` | `FAIL_CLOSED` | Prohibited/unsafe JWS header members are rejected. |
| `C04-sign-jws-wrong-purpose` | `local-reproducible` | `FAIL_CLOSED` | Wrong-purpose or wrong-audience `sign-jws` request is rejected. |
| `C05-valid-sign-csr` | `local-reproducible` | `PASS` | Valid `sign-csr` request binds subject, SANs and key public material under constrained CSR semantics. |
| `C06-sign-csr-wrong-subject` | `local-reproducible` | `FAIL_CLOSED` | Wrong-subject CSR request is rejected. |
| `C07-sign-csr-arbitrary-extension` | `local-reproducible` | `FAIL_CLOSED` | Arbitrary CSR extensions are refused unless explicitly permitted. |
| `C08-generic-sign-substitution` | `local-reproducible` | `FAIL_CLOSED` | Generic opaque signing cannot substitute for protocol-valid `sign-jws` or `sign-csr`. |

## Deferred Scope C cases

| Case | Operational state | Why deferred |
|---|---|---|
| `C03-sign-jws-replay` | `blocked` | Requires freshness or replay fixture from the implementation under test. |
| `C09-requester-no-authority` | `blocked` | Requires concrete requester-authority fixture from the implementation or upstream maintainer. |
| `C10-audit-reconstruction` | `upstream-evidence-needed` | Requires retained audit evidence and non-repudiation boundary data from the implementation. |

## Execution method

For each initial tranche case:

1. Use `evidence-template.yaml` as the case record.
2. Record exact source references for the Trust Tasks / VTA implementation under test.
3. Keep request payloads redacted; preserve only fields needed to show purpose, audience, subject, key reference, algorithm and policy outcome.
4. Store signed artifacts by digest where possible rather than retaining full payloads.
5. Record expected result, actual result and disposition as `PASS`, `FAIL`, `INDETERMINATE` or `transferred`.
6. Record retained audit evidence and non-repudiation limits.
7. Update `dpip-applicability-template.md` once retained evidence is known.

## Evidence packet layout

Recommended path for completed Scope C traces:

```text
docs/review/dtg-runtime-evidence/traces/scope-c/
  C01-valid-sign-jws.yaml
  C02-sign-jws-prohibited-header.yaml
  C04-sign-jws-wrong-purpose.yaml
  C05-valid-sign-csr.yaml
  C06-sign-csr-wrong-subject.yaml
  C07-sign-csr-arbitrary-extension.yaml
  C08-generic-sign-substitution.yaml
```

## Completion rule for this tranche

This tranche is complete only when each initial case has one of the following outcomes:

- evidence supplied and dispositioned;
- transferred to a more specific durable owner; or
- marked `INDETERMINATE` with the exact missing runtime evidence stated.

Do not close #994 from this tranche alone. Scope A, Scope B and deferred Scope C cases remain open unless separately resolved or transferred.
