# Hello RAHP: examine a real specification

This is the next exercise after the [smallest Hello RAHP scaffold](../hello-rahp/README.md). It completes a bounded examination of the **Trust Registry Query Protocol (TRQP), v2-approved source snapshot**, using RAHP alone. DPIP, the Trust Protocol Interop Lab and a running registry are not required.

The subject is a real specification. The three response fixtures are constructed teaching inputs, not captured service traffic. The two specification examples checked by the replay come directly from the retained source. This exercise takes about 20–30 minutes after installing the repository's dependencies.

## 1. Bound the question and pin the source

**Question:** What does a schema-valid authorization response establish, and what additional evidence is needed before relying on its authority or time claim?

Use commit [`6863733878f3657e05f70764bb474a9fb918de9a`](https://github.com/trustoverip/tswg-trust-registry-protocol/tree/6863733878f3657e05f70764bb474a9fb918de9a/specification/v2-approved). The [source manifest](source-manifest.json) identifies every retained file by its upstream path, immutable URL, Git blob SHA and SHA-256. The review uses RAHP v2.6.0 at the toolkit revision recorded in [pressure-test.yaml](pressure-test.yaml).

Read only the authorization portions of the retained definitions/scope, API, HTTPS binding and response schema. Recognition chains, live behavior, transport security and system-of-record design are outside this examination. The source's own Scope section explicitly excludes systems of record and implementation code. That boundary matters when choosing who can resolve a finding.

The API's schema insertion names the `v2` directory, while its source link names the local `v2-approved` schema. Both response-schema paths have the same Git blob at this revision; the manifest records that check. Retained Markdown has a `.txt` suffix to preserve original bytes without treating upstream publication directives and relative links as RAHP documentation.

## 2. Select existing risk hypotheses

Use two existing portable hypotheses: **RKP-AUTH-01**, possession mistaken for authority, and **RKP-AUTH-02**, stale authority accepted. Here the first is an analogy: response validity can be mistaken for substantiated authority. The second asks whether a past permission is being reused for a later action. **HRM-INF-01** captures the resulting false trust inference.

The record also reuses **CRK-01** and **CRK-21** as catalogue analogues for authority conflation and historical validity. These are existing CAWG instance references supplied with this checkout, not CAWG requirements imposed on TRQP. The portable patterns carry the reasoning. Their reuse neither establishes full domain independence nor completes a separate portability research programme.

Illustrative scenario: a relying party uses an authorization response to decide whether an issuer may issue a license now. A response about a past moment does not by itself establish permission now. No actual issuer, harmed person, service defect or governance approval is asserted.

## 3. Separate evidence, inference and disposition

Inspect these immutable source anchors before reading the findings:

| Evidence | Observation | Inference and disposition |
| --- | --- | --- |
| [Response schema, lines 5–12](https://github.com/trustoverip/tswg-trust-registry-protocol/blob/6863733878f3657e05f70764bb474a9fb918de9a/specification/v2-approved/core/schema/trqp_authorization_response.schema.json#L5-L12) | Entity, authority, action, resource, authorization Boolean and evaluation time are required. | **Supported proposition:** those fields must be present for schema conformance. Presence does not verify their truth or bind them to a particular request. |
| [Schema timestamp descriptions, lines 34–42](https://github.com/trustoverip/tswg-trust-registry-protocol/blob/6863733878f3657e05f70764bb474a9fb918de9a/specification/v2-approved/core/schema/trqp_authorization_response.schema.json#L34-L42) and [Scope](https://github.com/trustoverip/tswg-trust-registry-protocol/blob/6863733878f3657e05f70764bb474a9fb918de9a/specification/v2-approved/core/spec.md#L69-L83) | Requested time means applicability; evaluation time means endpoint execution. Historical provenance is not a required response field; systems of record are excluded. | **F-001 remains open:** request deployment evidence and policy. This does not establish a missing core protocol requirement. |
| [API query and response, lines 24–57](https://github.com/trustoverip/tswg-trust-registry-protocol/blob/6863733878f3657e05f70764bb474a9fb918de9a/specification/v2-approved/core/api.md#L24-L57) | Query time is June 19; response `time_requested` is June 25. The response is schema-valid. | **F-002 remains open:** editors should clarify the example; schema checks alone cannot establish query/response semantic agreement. |

These are reviewer judgments grounded in the bounded source. `status: complete` means the examination record is finished; the findings remain open and independent review is pending. The specification editors are a proposed resolution role, not a confirmed assignee. F-001 needs a deployment policy owner and assessor; none has supplied evidence or accepted risk here.

## 4. Reproduce the checks offline

From the RAHP repository root, after `pip install -r requirements.txt`:

```bash
python3 examples/standalone-trqp/replay.py --check
python3 tools/validate_pressure_tests.py --file examples/standalone-trqp/pressure-test.yaml
python3 tools/render_pressure_tests.py --check
```

The replay verifies retained source bytes, validates the constructed responses against the unmodified upstream schema with date-time format checking enabled, and extracts the actual authorization examples from the retained API and HTTPS binding. The schema declares no dialect; the installed `jsonschema` library selects its default validator. These fixtures exercise shared required/type/date-time behavior rather than a claim of full dialect conformance.

Compare the output with [expected-replay.json](expected-replay.json):

| Check | Expected result | What it establishes |
| --- | --- | --- |
| Minimal required-fields response | Schema-valid | Optional provenance/time fields are not needed for this schema check. |
| Same response without `authority_id` | Schema-invalid | A negative control confirms the required-field boundary. |
| Constructed historical response without provenance | Schema-valid | Schema validity alone cannot support the broader historical-provenance claim. |
| Actual API authorization example | Schema-valid; requested time does not match query | A source example ambiguity survives schema validation. |
| Actual HTTPS authorization example | Schema-valid; requested time matches query | A contrasting source example preserves the applicable time. |

Successful commands establish reproduction of these bounded checks. They do not execute ATP-AUTH-02, demonstrate revocation handling, certify TRQP or establish deployment conformance. `runtime_authorization` and `authority_history` remain `not-assessed`; the overall posture remains `review-required`.

## 5. Make the next evidence request

For F-001, request a governed authority statement and decision trace showing which policy/state applied at the requested moment, then test an action after effective revocation. Keep the current authorization decision distinct from a historical authorization claim. Define who owns the policy, how fresh evidence must be, and who may accept residual risk. An example schema response cannot answer these questions.

For F-002, request editor clarification at a new immutable revision, then repeat the source comparison. A local tutorial change does not close an upstream finding. Rebaseline if the schema, timestamp semantics, authority policy or selected scope changes; retain this record as historical evidence.

Try challenging one inference yourself: write down a plausible alternative explanation, the evidence that would distinguish it, and whether it changes the disposition. For example, a deployment may already retain strong historical provenance outside the response. That could satisfy F-001 for that deployment without changing TRQP's core schema.

## Examination record

The following block is generated from [pressure-test.yaml](pressure-test.yaml); edit that record and run `python3 tools/render_pressure_tests.py` to update it.

<!-- BEGIN GENERATED PRESSURE TEST -->

## Generated pressure-test record

> This section is generated from [`pressure-test.yaml`](pressure-test.yaml). Do not edit it by hand. The YAML is the canonical review record; run `python3 tools/render_pressure_tests.py` after changing it.

### Review metadata

| Field | Value |
|---|---|
| Review ID | `SR-HELLO-TRQP-001` |
| Status | complete |
| Title | Standalone TRQP authorization response examination |
| Reviewed on | 2026-10-07 |
| Target repository | `trustoverip/tswg-trust-registry-protocol` |
| Target version | v2-approved source snapshot |
| Target commit | `6863733878f3657e05f70764bb474a9fb918de9a` |
| Target source paths | `specification/v2-approved/core/spec.md`, `specification/v2-approved/core/api.md`, `specification/v2-approved/core/https_binding.md`, `specification/v2-approved/core/schema/trqp_authorization_response.schema.json` |
| RAHP repository | `sankarshanmukhopadhyay/rahp-toolkit` |
| RAHP version | `v2.6.0` |
| Engine contract | `—` |
| RAHP corpus date | — |

### Method

| Field | Value |
|---|---|
| Workflow | `docs/pressure-testing-a-spec.md` |
| Rule | Separate source requirements, schema checks, reviewer inference and deployment evidence. |

### Review scope

**Included**

- Authorization response field requirements and their evidentiary limits
- Requested time versus evaluation time in the retained authorization examples

**Excluded**

- Live endpoints, transport security, recognition chains and system-of-record behavior
- Full TRQP conformance, ecosystem governance approval and deployment risk acceptance

### Summary

| Measure | Value |
|---|---:|
| Findings | 2 |
| Open findings | 2 |

**Overall assessment**

Required response fields support an explicit authorization tuple and evaluation-time label. They do not demonstrate truth, current authority or historical provenance. One deployment evidence obligation and one source example clarification remain open. The bounded examination is complete; TRQP as a whole and any implementation remain unassessed.

### Finding index

| ID | Finding | Severity | Status | Primary disposition | RAHP risks |
|---|---|---|---|---|---|
| `F-001` | Schema-valid authorization does not establish authority history or current permission | Medium | open | Implementation Guidance | [CRK-01 — Identity-validity and authority conflation](/rahp-toolkit/docs/cawg-risk-register.html#crk-01), [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| `F-002` | API authorization example does not preserve the queried historical time | Low | open | Specification | [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |

### Detailed findings

#### F-001 — Schema-valid authorization does not establish authority history or current permission

| Field | Value |
|---|---|
| Severity | Medium |
| Status | open |
| Primary disposition | Implementation Guidance |
| Secondary dispositions | Governance, Runtime Control |
| Scenarios | — |
| Scenario patterns | — |
| Personas | — |
| Risks | [CRK-01 — Identity-validity and authority conflation](/rahp-toolkit/docs/cawg-risk-register.html#crk-01), [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-INF-01`, `HRM-AUT-05` |
| Risks | `RKP-AUTH-01`, `RKP-AUTH-02` |
| Controls | `CTP-AUTH-01`, `CTP-AUTH-02` |
| Guardrails | `GRP-AUTH-01`, `GRP-AUTH-02` |
| Assurance | — |
| Evidence | `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `source/spec.md.txt — Definitions and Scope` | An authority makes governance statements; the registry operator may be delegated. Systems of record and implementation code are explicitly outside protocol scope. |
| `source/trqp_authorization_response.schema.json — required and timestamp properties` | The schema requires the authorization tuple, Boolean decision and evaluation time, but no authority-statement provenance or historical state identifier. Requested time is optional. |
| `cases.json — historical-response-without-provenance; expected-replay.json` | A constructed historical response without provenance satisfies the retained schema. This is a schema counterexample to an overbroad assurance claim, not an observed endpoint failure. |

**Potential harm**

In the illustrative license-issuance scenario, a relying party could act on a stale permission or an unsubstantiated historical authority assertion. Medium describes this bounded hypothetical scenario, not a deployment-wide impact rating.

**Recommended treatment**

Have the deployment policy owner define authority provenance and action-time freshness requirements. An assessor should request a decision trace binding the query tuple, applicable time, governed authority statement, policy and system-of-record state, plus a post-revocation negative case. Retain that evidence separately if it is unsuitable for the protocol response. No mandatory response extension or internal storage design is inferred from this source review.

**Retest when**

- A named deployment supplies its governance policy and reproducible authorization/revocation traces.
- The target schema or system-of-record scope changes.

#### F-002 — API authorization example does not preserve the queried historical time

| Field | Value |
|---|---|
| Severity | Low |
| Status | open |
| Primary disposition | Specification |
| Secondary dispositions | — |
| Scenarios | — |
| Scenario patterns | — |
| Personas | — |
| Risks | [CRK-21 — Timestamp or status evidence insufficiency](/rahp-toolkit/docs/cawg-risk-register.html#crk-21) |
| Controls | — |
| Guardrails | — |
| Assurance tests | — |

**Portable v1.1 assurance patterns**

| Layer | Patterns |
|---|---|
| Harms | `HRM-INF-01` |
| Risks | `RKP-AUTH-02` |
| Controls | `CTP-AUTH-02` |
| Guardrails | `GRP-AUTH-02` |
| Assurance | — |
| Evidence | `EVP-AUTH-01` |

**Evidence**

| Source | Observation |
|---|---|
| `source/api.md.txt — authorization query and response examples` | The query context.time is 2025-06-19T11:30:00Z, but its response time_requested is 2025-06-25T00:42:00Z. The response still satisfies the authorization response schema. |
| `source/trqp_authorization_response.schema.json — time_requested and time_evaluated descriptions` | Requested time identifies the moment the response applies to; evaluation time identifies endpoint execution time. These are distinct meanings, not inherently equal timestamps. |
| `source/https_binding.md.txt — authorization examples; expected-replay.json` | The HTTPS example preserves the query time in time_requested. Offline replay confirms the API mismatch and the HTTPS match. No live response was observed. |

**Potential harm**

A reader copying the API example could confuse historical applicability with endpoint execution time and evaluate permission at the wrong moment. Low rates this documentation ambiguity only.

**Recommended treatment**

Ask the specification editors to align the API example's time_requested with the query and explain time_evaluated separately. Add an example showing different requested and evaluation times. Relying-party tests should check response/query semantics in addition to schema validity.

**Retest when**

- Specification editors clarify the examples at a new immutable revision.
- A relying-party implementation provides query/response time-binding tests.

<!-- END GENERATED PRESSURE TEST -->

## Attribution and continuation

Retained source files reproduce the **Trust Registry Query Protocol (TRQP), v2-approved source snapshot**, published by the Trust over IP Foundation in `trustoverip/tswg-trust-registry-protocol`, at the commit above. They remain governed by the upstream [license notice](source/LICENSE.md.txt) and [copyright policy](source/COPYRIGHT_POLICY.md.txt), rather than acquiring RAHP's documentation license. This examination is a downstream educational assessment, not a specification-owner endorsement.

Continue with [Pressure-testing a specification](../../docs/pressure-testing-a-spec.md) for a broader assessment, or [Adopting RAHP](../../ADOPTION.md) to configure your own target. This teaching example is not registered as a canonical maintained portfolio baseline.
