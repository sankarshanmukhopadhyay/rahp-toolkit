# DTG runtime evidence packet

This directory supports the consolidated DTG Portfolio runtime-evidence owner tracked in issue #994.

The purpose of this packet is to collect executable or observed runtime evidence for three assurance residuals:

1. Trigger-link, wallet sign-in and contact-DID binding.
2. VTI foreign-protocol binding.
3. VTA-held-key protocol signatures using `keys/sign-jws/0.1` and `keys/sign-csr/0.1`.

The earlier source/spec review issues (#990, #992 and #993) were closed after their residuals were transferred to #994. Their closure does not mean the runtime assurance questions are resolved. This packet is the evidence collection surface for resolving #994.

## Evidence classes

Every runtime case should produce, at minimum:

| Class | Purpose |
|---|---|
| Positive execution trace | Shows that the intended flow works under valid inputs. |
| Negative execution trace | Shows that stale, replayed, mismatched, unauthorized or malformed inputs fail closed or produce an explicit non-positive result. |
| Retained-evidence inventory | Shows what logs, task records, identifiers, transcripts and audit events are retained or deliberately not retained. |
| Privacy / DPIP determination | Determines whether retained evidence expands observable correlation enough to require DPIP promotion. |

## Directory layout

```text
docs/review/dtg-runtime-evidence/
  README.md
  cases.yaml
  evidence-template.yaml
  dpip-applicability-template.md
```

Future evidence traces may be added under:

```text
docs/review/dtg-runtime-evidence/traces/
  trigger-link/
  foreign-protocol-binding/
  vta-held-key-signing/
```

Do not commit secrets, bearer tokens, private keys, full unredacted transcripts, private user data, or credentials. Use redacted traces and stable digests where full payloads are unnecessary or unsafe.

## Scope A — trigger-link, wallet sign-in and contact-DID binding

This scope covers findings formerly owned by #990:

| Finding | Change |
|---|---|
| `d6f06da6be6c24f2917a` | Member portal with wallet sign-in by trigger link |
| `14345600ab746827b9d8` | Trigger-link parser alignment with VTI-LNK |
| `5daf04aa9bf26ef41594` | Operator-console sign-in wording and target distinction |
| `c15ef701e115583e2756` | Pluggable contact DID methods and domain-linked contacts |

Runtime evidence must distinguish member portal, operator console, page origin, community DID, wallet identity, session target, freshness, replay handling, wallet connection state and retained evidence.

## Scope B — VTI foreign-protocol binding

This scope covers finding `1c2869a18869681e741b`, formerly owned by #992.

The runtime question is whether a foreign-protocol interface is actually bound to an exchange begun by a task, rather than operating as a parallel authority surface. Evidence must cover task linkage, challenge, audience, single-use, expiry, task-visible outcome, failure asymmetry and privacy/correlation effects.

## Scope C — VTA-held-key protocol signatures

This scope covers finding `220fb4eea5c0200f190b`, formerly owned by #991/#993.

Runtime evidence must show that `keys/sign-jws/0.1` and `keys/sign-csr/0.1` are constrained protocol-signing tasks, not substitutes for generic opaque signing. Evidence must cover requester authority, purpose, audience, freshness, subject binding, denied wrong-purpose/wrong-subject cases, audit reconstruction and non-repudiation limits.

## Disposition values

Use these values consistently:

| Value | Meaning |
|---|---|
| `PASS` | Runtime evidence supports the proposition. |
| `FAIL` | Runtime evidence contradicts the proposition or shows unsafe behavior. |
| `FAIL_CLOSED` | Negative case produced the expected rejection or non-positive result. |
| `INDETERMINATE` | Evidence is insufficient, missing, ambiguous or not attributable. |
| `TRANSFERRED` | Residual moved to a more specific durable owner with a posted transfer matrix. |

## Closure gate for #994

Issue #994 should not close merely because source/spec evidence exists. It should close only when all three scopes are resolved or transferred, each finding has an explicit disposition, retained evidence is inventoried, and DPIP applicability is ruled out with rationale or promoted to DPIP.
