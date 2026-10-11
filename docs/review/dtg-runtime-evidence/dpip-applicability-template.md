# DPIP applicability note

Use this template for each scope or for the consolidated packet when assessing whether runtime evidence requires DPIP promotion.

## Scope

- Scope:
- Related issue: #994
- Case IDs covered:
- Finding IDs covered:

## Retained evidence inventory

| Evidence item | Retained? | Location / owner | Redaction | Correlation risk |
|---|---:|---|---|---|
| Initiating task record | TBD | TBD | TBD | TBD |
| Session or exchange identifier | TBD | TBD | TBD | TBD |
| Verifier / client identifier | TBD | TBD | TBD | TBD |
| Community DID / contact DID | TBD | TBD | TBD | TBD |
| Wallet identity reference | TBD | TBD | TBD | TBD |
| Device enrollment state | TBD | TBD | TBD | TBD |
| Presentation or signing transcript | TBD | TBD | TBD | TBD |
| Audit event | TBD | TBD | TBD | TBD |
| Failure / rejection record | TBD | TBD | TBD | TBD |

## Correlation surfaces

Describe whether the runtime evidence links any of the following across contexts:

- task or exchange identifier;
- verifier/client identifier;
- credential holder, presenter or wallet identity;
- community membership;
- contact DID or domain-linked contact;
- device enrollment or user-verification state;
- retained transcript or status/discovery traffic;
- task outcome or rejection reason.

## DPIP decision

Choose one:

- `DPIP not required`: retained evidence remains local, minimal and non-correlating across material contexts.
- `DPIP required`: retained evidence materially expands observable privacy/correlation risk and should be promoted.
- `INDETERMINATE`: evidence is incomplete or insufficiently attributable.

Decision:

## Rationale

Explain the decision using only observed runtime evidence. Do not infer privacy safety from source/spec intent alone.

## Follow-up

If DPIP is required, record the RAHP issue/comment where the DPIP referral is created and the DPIP target issue once opened.
