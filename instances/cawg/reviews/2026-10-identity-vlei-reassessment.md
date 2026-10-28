---
title: "CAWG vLEI: October 2026 change reassessment"
layout: default
nav_exclude: true
---

# CAWG vLEI change reassessment: evidence baseline

**Tracking issue:** [RAHP #1163](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1163)  
**Assessment key:** `cawg:repository:decentralized-identity/cawg-identity-assertion@vlei`  
**Status:** evidence baseline established; technical scenario execution pending  
**Previous reviewed upstream revision:** `1fbff9683fb692667a81206274d4b24d17078c0b`  
**Observed new upstream revision:** `464ee8a937f467ec42be4587e425bd56e7350f9f`  
**Common ancestor:** `1d45eb40970e1592f463bd60e19537ab62ec68f6`  
**Existing curated review:** [CAWG-SR-011](../../../examples/cawg-c2pa/identity-vlei/README.md) (preserved as historical evidence)

## Evidence method and boundaries

This record is an upstream-source examination and finding-by-finding reassessment baseline, **not** a completed executable verifier conformance test or a fresh RAHP/security/combined run. It must not be used as an assertion that CAWG, DIF, GLEIF or a relying-party implementation has accepted a control. The branch-aware identity and revision pin are deliberate. Preserve the original `CAWG-SR-011` target commit and historical evidence; do not rewrite it to imply it was originally assessed in October.

GitHub's compare endpoint reports `diverged` for the old and new revisions (`ahead_by=1`, `behind_by=1`), not a fast-forward update. The merge-base-to-old comparison reports four commits ahead and the merge-base-to-new comparison reports four commits ahead. Examine the *net source difference* and both branch histories: the apparent single new commit does not establish a linear successor relationship.

## Revision-specific semantic evidence

| Topic | Earlier evidence at `1fbff968` | New evidence at `464ee8a` | Immediate assurance consequence |
|---|---|---|---|
| vLEI CBOR signature payload | `signer_aid_oobi: tstr` | `signer_aid_oobi: [+tstr]` | Wire representation changes: legacy string-shaped inputs and empty arrays are not equivalent to the new required nonempty array. Test strict rejection and documented compatibility boundaries. |
| Witness/OOBI resolution | Use the single supplied OOBI; TODO on rotated witnesses | Try any resolvable OOBI; abort when all are exhausted, or KEL absent/invalid or sequence unavailable | A positive KEL fetch is not enough; validation and the exact signing key state remain required. Distinguish unresolved from invalid evidence in assurance reporting. |
| Archival continuity | TODO considers retaining signed time evidence and relevant KELs | Explicit archival-quality note states witness/QVI availability can limit future verification; proposed alternatives are embedded KEL/TEL evidence or external archival service; no ecosystem retention commitment stated | Explicit acknowledgment **does not** establish interoperable as-of proof, evidence retention or availability guarantees. |
| vLEI trust model | Section says `TO DO: Write this section.` | Defines GLEIF ROOT/GEDA/QVI delegation, ACDC dependency graph, KEL/TEL checks, watcher monitoring, conflicting histories and superseding recovery | Model clarifies trust dependencies but requires tests for revoked credentials, inconsistent KEL histories, missing chain members and recovery. |
| Role credential/authorization | QVI-issued OOR/ECR authorization and entity-issued ECR rules present | Substantially retained in the reviewed validation text | The revision does not itself demonstrate changed mandate verification; preserve the distinction between role evidence and authorization. |
| X.509 validation | Existing file | Expanded validation, time/revocation/status requirements in the revision comparison | Requires a separate focused cross-lane examination before claiming equivalence with the vLEI path. |

### Source references

- [Old vLEI payload definition](https://github.com/decentralized-identity/cawg-identity-assertion/blob/1fbff9683fb692667a81206274d4b24d17078c0b/docs/modules/ROOT/partials/credential-types/vlei/keri_payload.adoc)
- [New vLEI payload definition](https://github.com/decentralized-identity/cawg-identity-assertion/blob/464ee8a937f467ec42be4587e425bd56e7350f9f/docs/modules/ROOT/partials/credential-types/vlei/keri_payload.adoc)
- [Old validation](https://github.com/decentralized-identity/cawg-identity-assertion/blob/1fbff9683fb692667a81206274d4b24d17078c0b/docs/modules/ROOT/partials/credential-types/vlei/validating.adoc) and [new validation](https://github.com/decentralized-identity/cawg-identity-assertion/blob/464ee8a937f467ec42be4587e425bd56e7350f9f/docs/modules/ROOT/partials/credential-types/vlei/validating.adoc)
- [New trust model](https://github.com/decentralized-identity/cawg-identity-assertion/blob/464ee8a937f467ec42be4587e425bd56e7350f9f/docs/modules/ROOT/partials/credential-types/vlei/trust-model.adoc)
- [New generation requirements](https://github.com/decentralized-identity/cawg-identity-assertion/blob/464ee8a937f467ec42be4587e425bd56e7350f9f/docs/modules/ROOT/partials/credential-types/vlei/generating.adoc)
- [New X.509 validation](https://github.com/decentralized-identity/cawg-identity-assertion/blob/464ee8a937f467ec42be4587e425bd56e7350f9f/docs/modules/ROOT/partials/credential-types/x509/validating.adoc)
- [Comparison](https://github.com/decentralized-identity/cawg-identity-assertion/compare/1fbff9683fb692667a81206274d4b24d17078c0b...464ee8a937f467ec42be4587e425bd56e7350f9f)

## Disposition of pre-existing CAWG-SR-011 findings

| Finding | Source-backed current judgment | State |
|---|---|---|
| F-001: Role credentials need durable as-of validation | The former TODO has been replaced by explicit archival limitations, without a normative retained as-of evidence format or demonstrated signing-time role status. Removal of TODO is **not** verified remediation. | **Retain open; executable historical-status tests pending** |
| F-002: KERI dependency retention becomes part of content durability | New text positively acknowledges OOBI unavailability and lack of commitment to perpetual ecosystem KEL/TEL retention. It offers alternatives rather than requiring either. | **Retain open; stronger documentary evidence, no retention guarantee** |
| F-003: Multiple identity trust lanes need explicit equivalence boundaries | vLEI now details trust dependencies and X.509 validation expands substantially; neither source proves cross-lane decision equivalence or common UX status semantics. | **Retain open; focused cross-lane assessment pending** |

All three statuses refer to findings in the *historic* curated review. No old finding is silently closed by this baseline.

## Bounded scenario matrix for the next assessment pass

The pre-existing scenarios `CAWG-033`, `CAWG-034`, `CAWG-006` and `CAWG-028` should be reused before adding any new case. Their fitness for the following explicit conditions needs to be checked against actual scenario definitions. These are expected tests, **not executed results**.

| Condition | Expected assessment distinction |
|---|---|
| New payload with at least one valid OOBI and a matching verified KEL sequence | Potentially valid only after full credential chain, signatures and status validation |
| Empty `signer_aid_oobi` array or legacy scalar | Fails new payload contract; if migration is supported, it must be explicit |
| All OOBIs unavailable | Verification cannot succeed; record missing evidence without pretending historical invalidity |
| A resolvable OOBI returns a KEL lacking the requested sequence, or invalid KEL | Reject validation; do not equate a successful network retrieval with verified key state |
| LE or role credential TEL has a valid revocation event | Reject the affected chain under the specified current-state procedure; evaluate separately any as-of claim |
| Historical role credential once valid, subsequently revoked, with incomplete signing-time status evidence | Do not infer either historical authority or historical invalidity without competent evidence |
| Conflicting KEL histories / superseding recovery invalidates an earlier anchor | Explicitly assess conflict and affected dependency and do not accept a cached earlier success unconditionally |
| An ECR issued by LE vs ECR issued by QVI, or OOR without authorization credential | Exercise distinct conditional authorization chains; reject missing required authorization |
| vLEI and X.509 outcomes shown as a single undifferentiated verified status | Identify any trust-lane-specific assurance and status distinctions that the display erases |


## Increment 2: scenario-corpus fit and cross-lane source assessment

**Scenario inventory inspected:** `corpora/cawg.yaml`, with existing records `CAWG-006`, `CAWG-028`, `CAWG-033` and `CAWG-034`. All four exist and align with the inherited finding references. They are concise pressure-test *descriptions*, not executable verification fixtures.

| Scenario | Actual corpus title | Reassessment purpose | Coverage determination |
|---|---|---|---|
| `CAWG-033` | vLEI role credential revoked after signing | Signing-time versus current role credential status | Relevant; needs pinned negative and historical evidence fixtures |
| `CAWG-034` | KERI validation material unavailable years later | Long-lived KEL/TEL and OOBI dependency failure | Relevant; needs all-OOBIs-unavailable and inconsistent-state variants |
| `CAWG-006` | Cross-scheme Level of Assurance comparison | Prevent equivalence between different trust mechanisms | Relevant; needs vLEI-versus-X.509 decision evidence |
| `CAWG-028` | Cryptographically valid asset shown with misleading green state | Prevent collapsing evidence-known, invalid and indeterminate states | Relevant; needs explicit result/UX assertions |

**Coverage decision:** No new scenario identifiers are justified solely by the source change. The four existing records cover the *classes* of harm; they do not yet demonstrate execution of the new CBOR wire-contract or the new witness-array failure modes. Add targeted fixtures or condition extensions before declaring this review tested. In particular, `signer_aid_oobi` scalar versus nonempty-array encoding is a **new format change**, but that alone does not prove a new domain-level harm requiring a new risk ID.

**Security review linkage:** The existing `examples/security-hardening/cawg-identity/findings.yaml` (review `SEC-CW-001`) identifies external URI resolution and network dependency as an attack surface. The expanded OOBI-list contract increases the number of candidate network fetches and requires the same bounded resolver safety controls. This is an implementation/testing concern; it is not evidence of an exploit.

**X.509 cross-lane source inspection:** The new `x509/validating.adoc` contains expanded instructions on certificate-path validation, status and timestamp handling. Its inclusion in the net revision difference does **not** by itself establish vLEI/X.509 assurance equivalence or successful validation under unavailable revocation evidence. F-003 remains open; produce a source-clause-to-result mapping and negative fixtures before changing the disposition. No X.509 verifier was executed during this increment.

**Limitations:** This increment completed document-to-corpus traceability, not RAHP/security/combined run validation. No positive conformance claims are supported. The documented scenario conditions remain hypotheses until exercised with pinned inputs and recorded outputs.


### X.509 clause-level observations (source inspection only)

The new [X.509 validation procedure](https://github.com/decentralized-identity/cawg-identity-assertion/blob/464ee8a937f467ec42be4587e425bd56e7350f9/docs/modules/ROOT/partials/credential-types/x509/validating.adoc) explicitly refers to C2PA 2.4 signature, timestamp and revocation-information procedures. Its selected normative branches include:

- Reject an algorithm outside the allowed/deprecated set with `cawg.x509.algorithm.unsupported`; require a trust-chain decision and do not return `cawg.identity.trusted` without the named trust-model check.
- Select a validated signing time from the assertion, then potentially a C2PA claim or timestamp manifest/assertion; unsupported or mismatched timestamp tokens are ignored with distinct informational codes rather than automatically accepted as trusted.
- Evaluate certificate validity and trust-anchor `notBefore`/`notAfter` constraints relative to trusted attested time, or current time when no trusted timestamp is present.
- The normative CA-certificate revocation test rejects if revocation was effective at the relevant time. For the named-actor certificate, the text explicitly prescribes treating a certificate as *not revoked* when the certificate does not support revocation status or the issuer offers no query method. This rule is **not** equivalent to proving a positive non-revocation observation. It warrants an explicit evidence-status distinction in the assurance/UX evaluation.

**New cross-lane test requirement:** demonstrate that X.509 `credential.trusted`/timestamp informational or failure codes, vLEI chain/role verification, and a higher-layer `identity.trusted` result cannot be conflated by a verifier or UI. Record whether each result follows from validated evidence, an explicit specification default, or unavailable evidence. Do not label all three evidence categories interchangeably. This is a proposed RAHP interpretation to test, not a claim that upstream violates its own rules.

## Required completion work and closure gate

1. Inspect the substantive net change in the expanded X.509 validation text. Identify genuinely new controls, unresolved status semantics and any changed temporal assumptions.
2. Map the above conditions to the actual CAWG scenario corpus. Add minimal cases only when the existing corpus cannot represent a materially distinct failure path. Preserve the ownership boundary between CAWG and RAHP.
3. Perform a new reproducible source-pinned RAHP, security and combined assessment. Record actual commands, input version, outcome and evidence locations. Do not report source review alone as a passing test run.
4. Produce a new revision-specific durable review or explicit successor to `CAWG-SR-011`, preserving the old review unchanged, and validate its structured and rendered representations with `tools/render_pressure_tests.py` and `tools/validate_pressure_tests.py`.
5. Dispose of each finding with evidence and a testable retest condition. Only then mark #1163 assessment-complete, even if independent durable findings remain open.

**Current disposition:** `assessment-required`. Increment 1 source-history baseline completed; remaining increments **not yet executed**. No claim of verifier runtime conformance or upstream acceptance.


## Executable bounded regression evidence

The branch includes [`tests/test_cawg_vlei_1163.py`](../../../tests/test_cawg_vlei_1163.py), a standard-library `unittest` suite. It exercises an explicitly limited *assurance decision model* for nonempty OOBI arrays, all-witness unavailability, current versus historical role status and non-collapsed X.509/vLEI trust lanes. These are **model unit tests**, not verification of real KERI key events, CESR signatures, ACDC status, X.509 certificates or COSE data. The revision SHA constants provide source context, not automated upstream retrieval.

**Recorded local execution (2026-10-28):** `python -m unittest -v /mnt/data/test_cawg_vlei_1163.py`, Python standard-library `unittest`: four tests passed, zero failed. This was performed against the locally constructed test file before committing equivalent test source to the PR. It is **not** a GitHub Actions result and must not be described as repository-wide CI success. To reproduce from the repository root after checkout run `python3 -m unittest -v tests/test_cawg_vlei_1163.py` (or `python3 tests/test_cawg_vlei_1163.py`).

**Remaining evidence obligations:** run CI against the committed branch; perform actual source-pinned RAHP/security/combined assessments; generate structured successor review; run renderer and pressure-test validator against that review; retain actual outputs and dispositions. The model tests do not satisfy these gates and #1163 remains `assessment-required`.
