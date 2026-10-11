# Scope C local runtime capability assessment

Issue: #994  
Scope: C — VTA-held-key protocol signatures  
Finding: `220fb4eea5c0200f190b`  
Assessment date: 2026-10-12

## Purpose

This note records whether the downstream `rahp-toolkit` repository can itself produce runtime traces for the first Scope C tranche:

- `C01-valid-sign-jws`
- `C02-sign-jws-prohibited-header`
- `C04-sign-jws-wrong-purpose`
- `C05-valid-sign-csr`
- `C06-sign-csr-wrong-subject`
- `C07-sign-csr-arbitrary-extension`
- `C08-generic-sign-substitution`

The constraint for this pass is that no upstream issue, upstream PR comment, or upstream evidence request is posted. The assessment is recorded only downstream.

## Inspection performed

The downstream repository was searched for local executable material related to:

- `sign-jws`
- `sign-csr`
- `keys/sign-jws`
- `keys/sign-csr`
- `signJws`
- `signCsr`
- opaque signing substitution
- runtime fixtures
- negative-test traces

The relevant upstream Trust Tasks material was also inspected as source/spec evidence only. No upstream request was filed.

## Finding

The downstream `rahp-toolkit` repository does **not** presently contain a runnable Scope C harness, request fixture set, custodian/runtime implementation, or negative-test runner capable of producing PASS / FAIL runtime traces for the seven initial Scope C cases.

The available downstream evidence remains source/spec-informed. It can record what upstream PR `trustoverip/dtgwg-trust-tasks-tf#749` claims and what runtime evidence would be required, but it cannot itself prove the runtime behavior of a custodian handling `keys/sign-jws/0.1` or `keys/sign-csr/0.1`.

## Upstream source/spec evidence observed

Upstream source/spec material includes generated bindings and changelog/spec descriptions for `keys/sign-jws/0.1` and `keys/sign-csr/0.1`.

The material supports the source/spec conclusion that:

- `keys/sign-jws/0.1` is intended to have the custodian construct and sign protocol JWS input;
- prohibited JWS header members include `alg`, `crit`, `b64`, `jwk`, `jku`, and `x5u`;
- `keys/sign-csr/0.1` is intended to constrain subject attributes, optional SANs, public-key material, and CSR extensions;
- generic opaque `keys/sign` is not intended to substitute for protocol-valid JWS or CSR signing.

However, the inspected material does not provide downstream runtime traces for the seven Scope C cases.

## Case-level local capability status

| Case | Local downstream capability | Current downstream disposition |
|---|---|---|
| `C01-valid-sign-jws` | No runnable custodian/runtime fixture found downstream. | `INDETERMINATE`; source/spec evidence only. |
| `C02-sign-jws-prohibited-header` | No downstream negative-test harness found for prohibited headers. | `INDETERMINATE`; source/spec evidence only. |
| `C04-sign-jws-wrong-purpose` | No downstream policy/runtime fixture found for purpose or audience enforcement. | `INDETERMINATE`; runtime evidence absent. |
| `C05-valid-sign-csr` | No runnable custodian/runtime fixture found downstream. | `INDETERMINATE`; source/spec evidence only. |
| `C06-sign-csr-wrong-subject` | No downstream requester-authority or wrong-subject fixture found. | `INDETERMINATE`; runtime evidence absent. |
| `C07-sign-csr-arbitrary-extension` | No downstream negative-test harness found for arbitrary CSR extension rejection. | `INDETERMINATE`; source/spec evidence only. |
| `C08-generic-sign-substitution` | No downstream substitution trace or verifier-failure fixture found. | `INDETERMINATE`; source/spec evidence only. |

## Practical implication for #994

Scope C cannot be closed as PASS or FAIL from downstream evidence at this time.

The correct downstream disposition is:

1. retain the seven Scope C cases as `INDETERMINATE`;
2. mark local runtime execution as blocked by absence of downstream runtime fixtures and custodian implementation;
3. do not promote an upstream request from this pass, because the current operating instruction is to avoid upstream posting;
4. keep #994 open as the durable owner until either:
   - a local harness is added downstream;
   - runtime evidence becomes available from another source and is imported downstream; or
   - the Scope C residual is transferred to a more specific downstream owner.

## Recommended next downstream-only step

Create a downstream-only evidence request note under #994 identifying the exact external/runtime evidence that would be needed if it later becomes available. This should not be posted upstream unless a separate decision is made.

The note should ask for evidence artifacts, not narrative assurance claims:

- accepted `sign-jws` trace;
- rejected `sign-jws` prohibited-header trace;
- rejected wrong-purpose or wrong-audience `sign-jws` trace;
- accepted `sign-csr` trace;
- rejected wrong-subject `sign-csr` trace;
- rejected arbitrary-extension `sign-csr` trace;
- rejected or verification-failing generic `keys/sign` substitution trace;
- retained evidence / audit / non-repudiation boundary note.
