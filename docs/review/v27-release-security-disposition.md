# v2.7.0 candidate security and privacy review disposition

**Status:** BOUNDED_REVIEW_COMPLETE / RELEASE_OWNER_RESIDUAL_ACCEPTANCE_RECORDED  
**Date:** 2026-10-08  
**Candidate SHA:** `0c1773640e211157766574d295f58360b591a358`  
**Release enforcement SHA:** `86266def567009a87aae7c756f339777d60be021`  
**Comparison:** [v2.6.0…candidate](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/compare/v2.6.0...0c1773640e211157766574d295f58360b591a358)  
**Tracking:** [#941](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941)

This is a bounded source/control review, **not** a complete adversarial security audit, an independent review, or a publication authorization. The candidate delta comprises 27 commits through the later enforcement commit; review focus was changed executable surfaces, authority boundaries, optional assurance semantics, evidence validation, and existing security limitations.

## Examined controls and observations

| Area | Observed control | Remaining limitation | Disposition |
| --- | --- | --- | --- |
| Issue publication authority | `tools/publish_assessment_issues.py` restricts publication to the canonical RAHP repository; GitHub requests use a fixed API host and a 30-second timeout | Caller token scope and deployment permissions must be verified in live workflow context; HTTP error responses are surfaced to logs | REVIEW_REQUIRED |
| Sociotechnical optional profile | `tools/sociotechnical_assurance.py` validates JSON schema, rejects unsupported independence flags, checks evidence source/context/revision, rejects traversal outside the corpus directory | Inputs are not generally resource-quota bounded; output may include reviewed evidence and contextual personal information | REVIEW_REQUIRED |
| Reasoning profiles R1–R3 | Optional profile implementations are separately versioned; release notes explicitly exclude terminal assurance and independent adoption | External provenance/authority and operational reproduction are not established by synthetic fixtures | DISCLOSED_RESIDUAL |
| Release publication | Merged PR #950 enforces seven-gate JSON, owner GO, and candidate ancestry before tag creation | Evidence validator checks declarations/URL shape, not authenticity of reviewer identity or linked GitHub runs | HUMAN_VERIFICATION_REQUIRED |
| Dependency/supply chain | CI uses explicit Python/Node setup and tests; workflow governance passed at enforcement SHA | Python requirements are not hash-locked; third-party action and token permission review is still required | REVIEW_REQUIRED |
| Privacy and retention | Stable evidence-retention contract remains `rahp-evidence-retention-v1`; optional profile retains explicit scope/context | Actual sensitive-data handling, log redaction and external artifact retention need deployment-specific examination | REVIEW_REQUIRED |

## Candidate-specific checks performed

1. Inspected `v2.6.0` to enforcement SHA changed-file inventory via GitHub compare API.
2. Read the changed publisher, sociotechnical profile, R1/R2/R3 and reasoning-trace modules for high-risk parsing, process invocation, network calls and file writes. This is a **targeted code inspection**, not complete line-by-line coverage.
3. Read `docs/review/security-pre-review.md` and `docs/review/known-limitations.md`; the former explicitly covers an older v2.4.0 baseline and must not be represented as v2.7.0 security signoff.
4. Checked that the v2.7 release evidence validator requires seven declared PASS gates, matching candidate SHA, a repository URL and explicit owner GO; it does not authenticate those declarations.
5. Verified successful post-enforcement workflow runs: [validation](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37719178567), [workflow governance](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37719178645), [Pages](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37719178667), [corpus](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37719178594).

## Remaining mandatory release-security evidence

- [ ] Attributable reviewer identifies scope, inspected commit and methodology, including security/privacy/supply-chain deltas and actual workflow token permissions.
- [ ] Exercise malicious/oversized inputs and path boundaries where relevant, or explicitly accept a bounded non-blocking residual with rationale.
- [ ] Confirm output/log redaction, retention, artifact access and privacy handling for representative records.
- [ ] Review action dependencies and release token authority, including protected publication and tag behavior.
- [ ] Record each material finding with severity, remediation or accepted residual, and independent evidence links.
- [ ] Record security gate PASS only if the reviewer concludes no release-blocking unresolved findings.
- [ ] Obtain final maintainer GO **after** complete seven-gate evidence inspection. The prior conditional risk acceptance is not that final GO.

## Initial pre-disposition release status (superseded by the owner-risk disposition below)

**NO-GO at initial review.** CI is green, but a successful CI run is not security review. The candidate is not independently adopted; no terminal assurance claim is authorized. Do not create `method/v2.7-release-evidence.json` with fabricated PASS entries or dispatch the release workflow until all mandatory evidence exists.

## Release owner risk disposition — 2026-10-08

**Decision scope:** v2.7.0 only, pinned tested baseline `81acbff96f7a7e840a427aae99263eb9f46f041f`. This supplements, but does not rewrite, the earlier bounded review observations. The release owner expressed conditional willingness to accept documented residual risks [here](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941#issuecomment-6051116581), subsequently instructed publication [here](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941#issuecomment-6051355105). The review itself was AI-assisted and **not independent or a penetration test**.

| Residual | Severity / decision for this release | Required operational boundary |
| --- | --- | --- |
| Publisher API error bodies may reach logs | MODERATE / accepted for publication under canonical-repository-only publication | Use minimum-scope token; do not include secrets or personal information in issue payloads; restrict log access |
| Optional sociotechnical JSON can be large or contain sensitive evidence | MODERATE / accepted as optional, experimental tooling | Only trusted inputs in controlled environments; bound input size externally and keep output artifacts private |
| Evidence URL/SHA validator does not authenticate reviewer identity | MODERATE / accepted with explicit human verification requirement | Owner checks linked Actions results and scope before dispatch; do not interpret structural validation as attestation |
| Dependencies and Actions are not fully hash-pinned | MODERATE / accepted as pre-existing supply-chain exposure | Use repository-controlled Actions permissions and revisit dependency pinning in a subsequent hardening release |

**Bounded release-security conclusion:** No release-blocking exploit was demonstrated in the examined changed surfaces. These four documented residuals are treated as accepted for **this specific release**, not as resolved vulnerabilities or evidence of independent assurance. The `security_review` gate represents this **bounded and disclosed risk disposition only**; it must not be described as an independent audit. The owner must verify this record and the linked CI runs before manually entering `PUBLISH` in the guarded workflow. If the owner does not accept any residual, publication must be withheld.
