# Scope C initial evidence records — VTA-held-key protocol signatures

Issue: #994  
Scope: C — VTA-held-key protocol signatures  
Source finding: `220fb4eea5c0200f190b`  
Upstream source/spec PR: `trustoverip/dtgwg-trust-tasks-tf#749`  
Upstream merge commit: `e5354095432a9824e091b4e1889e8e0c2c8aca60`

## Purpose

This file starts Scope C evidence collection for the first runtime tranche identified in `scope-c-initial-tranche.md`.

It does **not** mark any runtime case PASS. The currently available upstream material is source/spec evidence from `trustoverip/dtgwg-trust-tasks-tf#749`, not an executable downstream trace. These records therefore distinguish:

- source/spec constraints that are already evidenced by the upstream PR description; and
- runtime traces still required before final PASS / FAIL / INDETERMINATE disposition under #994.

## Source/spec evidence available

The upstream PR states that the change adds two narrow tasks where the custodian builds protocol bytes itself before signing:

- `keys/sign-jws/0.1`
- `keys/sign-csr/0.1`

For `keys/sign-jws/0.1`, the upstream PR states that:

- the producer sends header members and payload or `payloadBase64Url`;
- the custodian sets `alg` from key type;
- `alg`, `crit`, `b64`, `jwk`, `jku` and `x5u` are refused;
- `x5c` leaf is checked against the key;
- both halves are serialized with RFC 8785;
- the custodian signs the bare JWS signing input;
- audit evidence records a digest of the signing input, not the payload.

For `keys/sign-csr/0.1`, the upstream PR states that:

- the producer names the subject as ordered typed attributes from a closed set;
- optional subject alternative names may be supplied;
- the custodian builds `CertificationRequestInfo` using the key's own public key;
- supported forms include P-256 with `ecdsa-with-SHA256` and Ed25519;
- the result is a PEM CSR with the key's multibase public key;
- no extension except `subjectAltName` is requested.

The PR also states that `signJws` and `signCsr` device capabilities are registered and that a custodian must not require generic `sign` for either. A custodian that frames `keys/sign` under its own opaque domain should not accept `sign` in their place.

## Initial case records

| Case | Case purpose | Source/spec evidence status | Runtime evidence status | Current disposition |
|---|---|---|---|---|
| `C01-valid-sign-jws` | Valid `sign-jws` request produces a protocol-valid JWS from custodian-built signing input. | Supported by upstream PR description. | No downstream runtime trace yet. | `INDETERMINATE` pending runtime trace. |
| `C02-sign-jws-prohibited-header` | Prohibited or unsafe JWS header members are rejected. | Supported by upstream PR description for `alg`, `crit`, `b64`, `jwk`, `jku`, `x5u`. | No rejection trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `C04-sign-jws-wrong-purpose` | Wrong-purpose or wrong-audience `sign-jws` request is rejected. | Not fully evidenced by source/spec PR text; purpose/audience policy appears deployment-context dependent. | No rejection trace yet. | `INDETERMINATE`; may need upstream/runtime fixture. |
| `C05-valid-sign-csr` | Valid `sign-csr` request binds subject, SANs and key public material under constrained CSR semantics. | Supported by upstream PR description. | No downstream runtime trace yet. | `INDETERMINATE` pending runtime trace. |
| `C06-sign-csr-wrong-subject` | Wrong-subject CSR request is rejected. | Partially supported by closed subject-attribute set, but wrong-subject authority check is not fully evidenced. | No rejection trace yet. | `INDETERMINATE`; likely needs requester/authority fixture. |
| `C07-sign-csr-arbitrary-extension` | Arbitrary CSR extensions are refused unless explicitly permitted. | Supported by upstream PR statement that no extension except SAN is requested. | No rejection trace yet. | `INDETERMINATE` pending negative runtime trace. |
| `C08-generic-sign-substitution` | Generic opaque `sign` cannot substitute for protocol-valid `sign-jws` or `sign-csr`. | Supported by upstream PR statement that generic `sign` must not be required or accepted in place. | No downstream substitution trace yet. | `INDETERMINATE` pending runtime trace. |

## Evidence records required next

Each case above needs a concrete trace file using `evidence-template.yaml`. Until those traces exist, the downstream RAHP disposition remains source/spec-informed but not runtime-complete.

Suggested paths:

```text
reproductions/dtg-runtime-evidence/scope-c/C01-valid-sign-jws.yaml
reproductions/dtg-runtime-evidence/scope-c/C02-sign-jws-prohibited-header.yaml
reproductions/dtg-runtime-evidence/scope-c/C04-sign-jws-wrong-purpose.yaml
reproductions/dtg-runtime-evidence/scope-c/C05-valid-sign-csr.yaml
reproductions/dtg-runtime-evidence/scope-c/C06-sign-csr-wrong-subject.yaml
reproductions/dtg-runtime-evidence/scope-c/C07-sign-csr-arbitrary-extension.yaml
reproductions/dtg-runtime-evidence/scope-c/C08-generic-sign-substitution.yaml
```

## Runtime trace requirements

A runtime trace for Scope C should include:

- source repository and commit/tag under test;
- exact task type under test;
- redacted request fixture;
- requester authority evidence or explicit statement that authority is outside the fixture;
- expected result;
- observed result;
- signed artifact digest, rejection record or verification failure record;
- audit / retained-evidence note;
- non-repudiation boundary note;
- privacy / DPIP note.

## Boundary after this pass

This pass starts evidence collection but does not close Scope C. The next substantive step is one of:

1. produce runnable fixtures and traces for the seven initial cases; or
2. transfer each case to a more specific upstream/runtime owner with a posted transfer matrix; or
3. mark a case blocked with a precise reason if the relevant implementation is not accessible.

Until one of those paths happens, `#994` remains open.
