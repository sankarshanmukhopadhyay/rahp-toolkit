# Credential renewal authority assurance example

This maintained regression example demonstrates the portable lifecycle-continuation proposition introduced by
`ATP-AUTH-03`. It is intentionally protocol-neutral. It does **not** define a credential-renewal protocol, a wallet
interaction model, or upstream DTG semantics.

## Assurance proposition

Renewal, reissuance or successor creation that extends consequential state is an authority boundary when continuation
requires a current decision. Unchanged claims, possession of the prior credential, successful reissuance, or an
existing automation preference are not sufficient evidence of current authority.

The example reuses existing portable risks rather than creating a renewal-specific risk:

- `RKP-AUTH-02` — stale authority accepted;
- `RKP-AUTH-05` — approval not bound to exact commitment;
- `RKP-DEL-03` — revocation propagation failure.

It exercises `CTP-AUTH-02`, `CTP-DEL-02`, `GRP-AUTH-02`, `ATP-AUTH-03`, `EVP-AUTH-01` and `EVP-DEL-02`.

## Cases

`cases.yaml` contains three required negative vectors and one positive control:

1. deliberate non-renewal must deny continuation;
2. a successor without fresh dependent binding remains indeterminate for the dependent state;
3. a partially completed cascade remains indeterminate for the unresolved graph;
4. unchanged claims may continue only when current continuation authority and required dependencies are positively established.

Historical evidence is preserved in every case. Preservation means an older object may remain usable to resolve a
historical statement. It does not establish current authority or successor applicability.

## Reproduce

From the repository root:

```bash
python3 -m unittest tests.test_credential_renewal_authority
python3 tools/validate_catalogue.py
python3 tools/validate_v04_method.py
python3 tools/validate.py
```

The unit test verifies the fixture's portable mappings and negative-case outcome rules. Catalogue and repository
validation verify that all referenced portable IDs resolve.

## Authority boundary and limitations

This example is downstream RAHP assurance evidence. HTX, credential specifications, trust-task specifications and
their governance frameworks remain authoritative for their own renewal and lifecycle semantics.

A PASS for this example establishes only that the assessed implementation or specification respects the tested
continuation boundary. It does not establish legal validity, production readiness, universal credential policy, or
upstream adoption.

## Provenance

Triggered by downstream analysis of trustoverip/dtgwg-htx-tf Discussion #22 and tracked in
[issue #1031](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1031).
