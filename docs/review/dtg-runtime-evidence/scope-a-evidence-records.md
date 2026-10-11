# Scope A evidence records — trigger-link, wallet sign-in and contact-DID binding

Issue: #994  
Scope: A — trigger-link, wallet sign-in and contact-DID binding  
Source issue: #990  
Source findings:

- `d6f06da6be6c24f2917a`
- `14345600ab746827b9d8`
- `5daf04aa9bf26ef41594`
- `c15ef701e115583e2756`

Primary upstream/source references carried into #994:

- `OpenVTC/verifiable-trust-infrastructure#2007` — member portal with wallet sign-in by trigger link.
- `OpenVTC/vta-browser-plugin#316` — trigger-link parser alignment with VTI-LNK.
- `OpenVTC/vta-browser-plugin#307` — operator-console sign-in wording / target distinction.
- `OpenVTC/vta-browser-plugin#317` — pluggable contact DID and domain-linked contacts.

## Purpose

This file starts Scope A evidence collection for the composed trigger-link, wallet sign-in and contact-DID assurance surface transferred into #994.

It does **not** mark any runtime case PASS. The currently available material is source/spec and implementation-change evidence from upstream repositories. That evidence is useful for identifying the assurance surface, but it is not a downstream runtime trace across the composed flow.

Scope A remains the broadest packet in #994 because it spans:

- member/operator portal surfaces;
- trigger-link construction and parsing;
- browser plugin / wallet handling;
- VTA interaction;
- TrustTaskHTTPS or equivalent task/session outcome;
- contact-DID and domain-linked-contact resolution;
- retained evidence / transcript inventory;
- privacy / DPIP applicability.

## Source/spec evidence available

The transferred Scope A finding set indicates that the upstream changes introduced or clarified:

1. wallet sign-in by trigger link for member portal flows;
2. trigger-link parser alignment with VTI-LNK expectations;
3. distinction between member portal and operator-console sign-in targets;
4. contact DID / domain-linked-contact behavior.

This supports a source/spec-informed finding that Scope A is a composed assurance surface. It does not yet establish that all positive and negative runtime paths produce the required results.

## Initial case records

| Case | Case purpose | Source/spec evidence status | Runtime evidence status | Current disposition |
|---|---|---|---|---|
| `A01-valid-member-portal` | Valid trigger-link sign-in to member portal binds page origin, community DID, wallet identity, session target and freshness. | Supported directionally by member-portal and trigger-link changes. | No downstream composed runtime trace yet. | `INDETERMINATE` pending runtime trace. |
| `A02-valid-operator-console` | Valid trigger-link sign-in to operator console is distinguishable from member portal sign-in. | Supported directionally by operator-console target distinction work. | No downstream composed runtime trace yet. | `INDETERMINATE` pending runtime trace. |
| `A03-wrong-target-member-console-mismatch` | Member portal and operator console targets cannot be silently confused. | Source/spec evidence suggests target distinction is recognized. | No negative runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |
| `A04-expired-trigger-link` | Expired trigger link is rejected or produces explicit non-positive result. | Freshness is an expected property of the composed flow, but not fully evidenced downstream. | No expired-link runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |
| `A05-replayed-trigger-link` | Reuse of a previously consumed trigger link is rejected or explicitly non-positive. | Replay resistance is an expected property, but not fully evidenced downstream. | No replay runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |
| `A06-wrong-page-origin` | Link clicked from a wrong or unbound page origin is rejected. | Source/spec evidence indicates origin binding is relevant. | No wrong-origin runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |
| `A07-wrong-community-did` | Community DID mismatch does not produce a successful sign-in. | Source/spec evidence indicates community DID participates in the flow. | No wrong-community-DID runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |
| `A08-disconnected-wallet` | No-wallet or disconnected-wallet path does not silently sign in. | Not fully evidenced by source/spec references alone. | No disconnected-wallet runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |
| `A09-locked-wallet` | Locked wallet requires unlock or explicit verification before claim/sign-in. | Not fully evidenced by source/spec references alone. | No locked-wallet runtime trace yet. | `INDETERMINATE` pending prompt / rejection / non-positive trace. |
| `A10-invalid-domain-linked-contact` | Invalid domain-linked contact fails before claim or binding, with no contact service use. | Supported directionally by domain-linked-contact changes. | No invalid-domain-linked-contact runtime trace yet. | `INDETERMINATE` pending rejection / non-positive trace. |

## Evidence records required next

Each case above needs a concrete trace file using `evidence-template.yaml`. Until those traces exist, the downstream RAHP disposition remains source/spec-informed but not runtime-complete.

Suggested paths:

```text
reproductions/dtg-runtime-evidence/scope-a/A01-valid-member-portal.yaml
reproductions/dtg-runtime-evidence/scope-a/A02-valid-operator-console.yaml
reproductions/dtg-runtime-evidence/scope-a/A03-wrong-target-member-console-mismatch.yaml
reproductions/dtg-runtime-evidence/scope-a/A04-expired-trigger-link.yaml
reproductions/dtg-runtime-evidence/scope-a/A05-replayed-trigger-link.yaml
reproductions/dtg-runtime-evidence/scope-a/A06-wrong-page-origin.yaml
reproductions/dtg-runtime-evidence/scope-a/A07-wrong-community-did.yaml
reproductions/dtg-runtime-evidence/scope-a/A08-disconnected-wallet.yaml
reproductions/dtg-runtime-evidence/scope-a/A09-locked-wallet.yaml
reproductions/dtg-runtime-evidence/scope-a/A10-invalid-domain-linked-contact.yaml
```

## Runtime trace requirements

A runtime trace for Scope A should include:

- source repository and commit/tag under test;
- portal surface under test: member portal or operator console;
- redacted trigger link or fixture reference;
- page origin and expected relying context;
- community DID;
- contact DID / domain-linked-contact route, where applicable;
- wallet identity reference or explicit no-wallet / locked-wallet condition;
- VTA / wallet / plugin interaction result;
- task/session/audit identifier or redacted retained-evidence reference;
- expected result;
- observed result;
- retained-evidence / transcript inventory;
- privacy / DPIP note.

## Local capability assessment

A downstream repository search found no local RAHP Toolkit runtime harness capable of executing the composed Scope A flow end-to-end. In particular, no downstream executable fixture was found for:

- member-portal trigger-link sign-in;
- operator-console trigger-link sign-in;
- browser plugin / wallet / VTA interaction;
- replay / expiry / wrong-target negative cases;
- wrong-origin / wrong-community-DID negative cases;
- invalid domain-linked-contact negative cases;
- retained transcript or task/session evidence capture.

This means downstream can record source/spec and assessment state, but cannot honestly mark Scope A PASS or FAIL from local runtime execution alone.

## Boundary after this pass

This pass completes the downstream Scope A evidence-record and local-capability assessment. It does not close Scope A.

Next options for #994 are:

1. wait for external runtime traces from the relevant implementation owners;
2. create a downstream-only upstream evidence-request draft for review before posting, if the user chooses to post later;
3. mark each Scope A case blocked with precise reason and retain #994 as the consolidated open evidence owner;
4. proceed to a final #994 status synthesis that summarizes Scopes A, B and C and identifies all remaining evidence dependencies.

Until one of those paths produces runtime traces or explicit transfer/blocking rationale, `#994` remains open.
