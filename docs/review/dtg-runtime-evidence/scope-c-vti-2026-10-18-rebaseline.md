# Scope C rebaseline: VTA protocol signing (18 October 2026)

Issue: [#994](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994). This is an **implementation-source and test-evidence assessment**, not an independently executed deployment trace. Do not treat source assertions or passing schema tests as observed production behavior.

## Pinned sources and authority boundaries

- [Trust Tasks #752, Glenn's response](https://github.com/trustoverip/dtgwg-trust-tasks-tf/issues/752#issuecomment-6211354820): specification/schema versus implementation distinction and per-case response.
- [Trust Tasks #749](https://github.com/trustoverip/dtgwg-trust-tasks-tf/pull/749): task specification and generated binding provenance.
- [Trust Tasks #792](https://github.com/trustoverip/dtgwg-trust-tasks-tf/pull/792): known-implementation registry (documentation, not runtime conformance).
- [VTI #2057](https://github.com/OpenVTC/verifiable-trust-infrastructure/pull/2057): merged 2026-10-13, merge commit `dda501dddf48540a3f4b1c36bc6ee917754f4c9b`. Implements the VTA custodian path for both tasks. Source/tests are evidence at this commit, not all deployments.
- Source/schema rejection evidence: `specs/keys/sign-{jws,csr}/0.1/payload.invalid-examples.json` (13 and 17 examples respectively), exercised through generated Rust conformance tests. These do not establish all runtime policy guarantees.

## Case-by-case evidence reconciliation

| Case | Evidence supported at pinned baseline | Disposition and remaining limit |
|---|---|---|
| C01 valid JWS | VTI #2057 constructs JWS input itself and has a test reproducing spec input and SHA-256 `e0c236e3a90999a1ab54699f308c0ad0468405da185731762396cd733e031257`. Audit: `keys.sign-jws`, alg, typ, digest; not payload. | **IMPLEMENTATION_EVIDENCED**; live/redacted request-response-audit trace not independently collected. |
| C02 forbidden header | VTI implementation refuses `alg`, `crit`, `b64`, `jwk`, `jku`, `x5u`; error `keys/sign-jws:headerMemberForbidden` with `details.member`, `trust-task-error` not signature response. This requires runtime logic because `header` is open. | **IMPLEMENTATION_EVIDENCED**; independent negative trace not collected. |
| C03 JWS replay | VTA SDK classifies signing operations as retry-safe/read-only; same signing input may legitimately be signed again, and this is not by itself a protocol-artifact replay vulnerability. | **INDETERMINATE**, reformulate as protocol consumer challenge/nonce/expiry enforcement where required; do not demand blanket task-level replay refusal. |
| C04 wrong purpose | `aud`, `nonce`, `exp` and other claims are producer-owned. Key-to-protocol binding is a SHOULD, restricting provisioned `typ` values a MAY. VTI #2057 explicitly does not implement either. | **NOT_ENFORCED (deployment policy controls)**, not PASS and not a universal normative violation. Separate consumer-side audience/claim validation. |
| C05 valid CSR | VTI builds `CertificationRequestInfo` from structured subject/SAN and key's own P-256/Ed25519 public key; test verifies CSR signature with `x509-parser`. Audit: subject, SANs, signed-DER SHA-256. | **IMPLEMENTATION_EVIDENCED**; independent live trace not collected. |
| C06 wrong subject | Implementation validates subject **form** against allowed attribute table, not legal authority over the asserted name. Spec does not warrant subject identity; CA verifies it. | **OUT_OF_TASK_GUARANTEE** for identity authority. Do not manufacture an expected wrong-subject rejection; validate malformed subjects separately. |
| C07 arbitrary extension | No arbitrary CSR extension input; schema `additionalProperties: false`; invalid example and generated Rust conformance rejection test. | **SCHEMA_CONFORMANCE_EVIDENCED**; no live custodian trace. |
| C08 opaque sign substitution | VTA `keys/sign` signs `vti.vta.opaque-signing.v1 || 0x00 || payload`. `sign` capability not accepted in place of `sign-jws` or `sign-csr`; protocol-specific capabilities required. | **IMPLEMENTATION_EVIDENCED** for this VTA, **not universal** for custodians which sign opaque payloads verbatim. |
| C09 requester lacks authority | VTI #2057 shows `require_write`, protocol-specific capability checks, context/scope policy and quota path. | **PARTIALLY_IMPLEMENTATION_EVIDENCED**; targeted negative test coverage for revoked, wrong-context, wrong-key, no-capability requesters and authority freshness still needs inspection/trace. |
| C10 audit reconstruction | Implementation describes per-task audit event/digest and selective fields, with JWS payload omitted and CSR subject/SAN retained. | **PARTIAL**; need emitted event verification, attribution/non-repudiation boundary and retention inventory (including cross-context correlation). |

## Retained-evidence and privacy boundary

Known from implementation description: `keys.sign-jws` retains `alg`, `typ`, and signing input digest, *not JWS payload*. `keys.sign-csr` includes subject, alternative names and digest of signed DER. Unknown here: event storage location, retention/deletion windows, access control, identifiers/correlation across contexts, audit sink failure behavior and whether additional request/task/transport records preserve payloads. **DPIP applicability is INDETERMINATE**, not ruled out. Subject/SAN is potentially identifying and must not be treated as content-free because the request body is not logged.

## Remaining bounded actions

1. Inspect or execute pinned VTI #2057 test paths for C09 invalid capability/authority/wrong key/context and document test command and outcome.
2. Pin the relevant protocol consumer path before treating C03 (claim expiry, nonce, audience, replay) as an enforceable requirement. Distinguish task retry from artifact reuse.
3. Decide how deployment wants to handle key-to-protocol SHOULD and provisioned `typ` MAY; VTI currently **does not enforce** these controls. Record residual without silently upgrading optional rules.
4. Obtain redacted actual audit event/schema and storage/retention metadata for C10; determine attribution and DPIP referral using inventory.
5. Keep #994 open because Scopes A/B remain INDETERMINATE, and C03/C09/C10 and DPIP are not terminal.

**Assurance vocabulary:** `IMPLEMENTATION_EVIDENCED` and `SCHEMA_CONFORMANCE_EVIDENCED` mean source and named test paths support a claim. They are not a claim that RAHP independently ran tests or collected runtime traces.
