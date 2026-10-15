---
layout: default
title: "Consumer-interaction assurance"
parent: Adopt RAHP
nav_order: 9
has_toc: true
---

# Consumer-interaction assurance

Tracking: [#1029](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1029).

RAHP can consume attributable observations from consumer-facing trust interactions without becoming a browser, wallet, VTA, mobile or agent automation framework. The portable boundary is `rahp-evidence-producer-result/v1`: an external harness executes the interaction; RAHP validates provenance, source pins, artifact integrity, freshness and claim boundaries; domain-specific observations remain opaque until interpreted by the applicable assurance proposition or specialist.

This page records the bounded feasibility conclusion from #1029. It does **not** certify OpenVTC, a wallet, a VTA, a browser, or any deployment.

## Architectural boundary

Keep these roles separate:

1. **Interaction harness** — Playwright, Selenium, Appium, native UI automation, accessibility tooling, protocol/API harnesses or equivalent tooling executes and observes the interaction.
2. **Evidence producer envelope** — the harness returns `rahp-evidence-producer-result/v1` with immutable source pins, execution metadata, integrity-bearing artifacts, bounded observations, freshness and explicit unsupported claims.
3. **RAHP assessment** — existing ATP/EVP patterns determine what the observations can support. UI success is never authorization, protocol conformance or terminal assurance by itself.
4. **Specialist / runtime authority** — specialist semantics and authoritative enforcement evidence remain with the relevant specialist, verifier, authorization service, execution service or deployment authority.

The existing registered Interop producer still emits `interop-evidence-bundle/v1`. That is a maintained compatibility path for that producer. It is not a requirement that every external evidence producer adopt the Interop bundle. Generic producers should prefer the portable RAHP envelope unless a registered producer contract requires otherwise.

## Minimal interaction-observation mapping

No core schema change is required. Put interaction-specific fields inside `evidence.observations[]`.

A useful minimum convention is:

| Field | Purpose |
|---|---|
| `requirement_id` | Evidence requirement served by the observation. |
| `interaction_id` | Stable identifier within the producer run. |
| `component` | Wallet, VTA, browser, relying-party UI, agent interface, console, etc. |
| `action` | Consumer-visible action such as approve, reject, sign-in, present, confirm. |
| `consumer_visible_state` | What the component represented to the consumer. |
| `ui_observed_outcome` | What the harness observed at the interaction surface. |
| `protocol_trace_ref` | Optional reference to an integrity-bearing protocol/runtime artifact. |
| `authority_decision_ref` | Optional reference to an authoritative authorization/enforcement artifact. |
| `accessibility_observation_ref` | Optional reference to representative accessibility/usability evidence. |
| `interpretation` | Bounded producer statement; must not claim terminal RAHP assurance. |

These names are an adoption convention, not a new normative schema. Producers may use different nested vocabularies where a specialist or profile owns the semantics.

## Existing RAHP patterns that apply

| Concern | Existing portable patterns | Required evidence boundary |
|---|---|---|
| Authentication versus authorization | `ATP-AUTH-01`, `EVP-AUTH-01` | UI authentication success must be correlated with a current authorization decision before authority is inferred. |
| Current authority / revocation | `ATP-AUTH-02`, `EVP-AUTH-01` | Action-time status and enforcement evidence. |
| Delegation and agent authority | `ATP-DEL-01`, `ATP-DEL-02`, `ATP-DEL-03`, `ATP-AGT-01` | Delegation/mandate evidence independent of interface representation. |
| Disclosure / presentation | `ATP-PRV-01`, `EVP-PRV-01` | Actual disclosed fields, audience and correlation surface, not merely the UI selection. |
| Alternative / accessible paths | `ATP-EXC-01`, `EVP-INCL-01` | Representative usability/accessibility evidence; automation alone does not establish comprehension or burden parity. |
| Replay / duplicate action | `ATP-OPS-02`, `EVP-OPS-02` | Runtime side-effect and freshness evidence. |
| Contestability / explanation | `ATP-RED-01`, `EVP-RED-01`, `EVP-AUD-01` | Adverse-decision and remedy evidence, not interface copy alone. |
| Cross-component fidelity | `ATP-COMP-01`, `ATP-COMP-02`, `EVP-COMP-01` | Correlated interface, protocol, authority and outcome evidence across the flow. |

No dedicated portable ATP is required merely because an interface exists. A new pattern would be justified only if a recurring assurance proposition cannot be expressed by composition of existing patterns.

## Reference workflow A — OpenVTC trigger-link wallet sign-in

Existing runtime-evidence owner: [#994](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994), Scope A. This guide does not duplicate or disposition those runtime obligations.

### Bounded proposition

What the wallet/browser represents as a successful sign-in must correspond to the intended portal/session target, current trigger-link state and authoritative runtime outcome.

### Positive path

An external harness may observe:

- trigger link opened at the intended relying-party origin;
- wallet identifies the requested community/session target;
- consumer confirms the intended action;
- UI reports successful sign-in.

That UI evidence can support **interaction-surface observations only** until correlated with authoritative runtime evidence.

For a stronger RAHP conclusion, correlate it with:

- immutable implementation/configuration pins;
- trigger-link/session identifier or digest;
- target and community binding;
- freshness/single-use state;
- authorization/session creation decision;
- resulting audit or session record.

### Negative paths

Use #994 Scope A cases as the source of runtime obligations, including:

- member portal versus operator-console target mismatch;
- expired trigger link;
- replayed trigger link;
- wrong page origin;
- wrong community DID;
- disconnected or locked wallet;
- invalid domain-linked contact.

Expected RAHP behavior is evidence-conservative: the harness may report a UI rejection, but the proposition is not PASS unless the required runtime/authority evidence supports the intended failure behavior.

### Indeterminate path

If the UI reports success but no attributable authority/session record is available, preserve the interface observation and return an incomplete/indeterminate evidence state. Do not infer authorization.

## Reference workflow B — VTA Trust Task approval

This second workflow demonstrates reuse across a materially different consumer-facing component.

### Bounded proposition

A VTA representation and approval of a consequential Trust Task must remain consistent with the task's purpose, resource, authority envelope, freshness and executed outcome.

### Evidence mapping

The same portable producer envelope can carry:

- VTA-visible request summary;
- approval/rejection interaction;
- task identifier/digest;
- protocol trace reference;
- authority/delegation reference;
- executed outcome reference;
- explicit claim boundary.

Relevant existing patterns include `ATP-AUTH-01`, `ATP-AGT-01`, `ATP-DEL-03`, `ATP-OPS-02` and `ATP-COMP-01/02`.

### Negative and indeterminate cases

Exercise wrong purpose/resource/audience, stale authority, replayed task, altered task after presentation, and missing runtime outcome. A VTA displaying "approved" without an attributable execution/authority trace remains an interaction observation, not proof that a protected action was authorized.

The same contract shape therefore works for a wallet/browser sign-in and a VTA approval without introducing component-specific fields into the portable RAHP schema.

## Framework-neutral producer guidance

RAHP does not require a particular automation library.

A producer should:

1. pin the subject and producer revisions;
2. execute the interaction using an appropriate external tool;
3. retain only the artifacts necessary to support the bounded proposition;
4. hash referenced artifacts and identify producer provenance;
5. place raw/domain-specific observations under `evidence.observations`;
6. state what those observations support and explicitly what they do not support;
7. declare freshness/invalidation keys;
8. validate the result with `tools/validate_evidence_producer_result.py`;
9. hand the validated evidence to the applicable assessment/reconciliation path.

Tool-specific selectors, screenshots, DOM snapshots, mobile accessibility trees or conversational transcripts are evidence artifacts, not RAHP method semantics.

## Provenance, retention and privacy

Apply `method/evidence-retention.yaml`:

- raw browser/mobile logs and reproducible execution exhaust are normally **ephemeral**;
- screenshots, machine traces and large transcripts used to support a disposition are normally **referenced**, with immutable/versioned locator, SHA-256, collection time and sensitivity;
- compact assessment identity, findings, disposition and manifest entries are **durable**;
- worked synthetic fixtures are **exemplars** only when deliberately promoted.

Do not commit secrets, bearer tokens, private keys, full credentials, unredacted personal transcripts or unnecessary identifiers.

Consumer-interaction evidence can materially increase correlation surface because it may join session/task identifiers, relying-party identifiers, wallet or holder references, device state, presentation metadata and outcomes. Where the retained evidence links identities or activity across contexts, use the existing RAHP → DPIP route. Where evidence is minimal, local and non-correlating, record the rationale for not invoking DPIP. If the retained-evidence inventory is incomplete, the privacy disposition remains INDETERMINATE.

## Feasibility decision

The #1029 investigation supports the following decision:

- **Core schema change:** not justified.
- **New portable assurance pattern:** not justified by the current evidence.
- **Mandatory browser/mobile dependency:** rejected.
- **Generic external producer support:** already available through `rahp-evidence-producer-result/v1`.
- **Registered Interop producer compatibility path:** remains `interop-evidence-bundle/v1` until separately migrated with equivalence evidence.
- **Recommended adoption path:** documentation + worked contract tests using the portable producer result, with domain-specific mapping inside `evidence.observations`.
- **Possible future adapter:** optional convenience only, justified when a concrete automation framework or producer needs deterministic translation; it must not acquire assurance authority.

## Reproduce the bounded contract checks

From the repository root:

```bash
python3 -m unittest tests.test_evidence_producer_result -v
python3 -m unittest tests.test_portable_producer_generic_ingestion -v
python3 -m unittest tests.test_consumer_interaction_evidence_contract -v
python3 tools/validate.py
```

These checks establish contract compatibility and fail-closed boundaries for synthetic/generic producer records. They do not establish live OpenVTC runtime assurance.

## Closure boundary

A consumer-interaction examination remains bounded by the exact proposition, source pins, evidence classes and authority traces supplied. The absence of a UI defect is not PASS; a green automation run is not PASS; and a consumer-visible "success" is not authorization unless the authoritative runtime evidence required by the proposition establishes it.
