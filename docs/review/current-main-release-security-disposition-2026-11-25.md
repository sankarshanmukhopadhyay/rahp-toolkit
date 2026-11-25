# Candidate release security disposition: 2026-11-25

Tracking: #958 and #1179. Scope: bounded source/configuration review and evidence plan for v2.10.0; not independent security audit. Status: PREQUALIFICATION. No security gate PASS is asserted.

## Observed baseline and required qualification

Main f12762890d7aa2e3e0cce47733a85d79fa0db701 passed [validate](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/45624723689), [documentation](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/45624723656) and [reconciliation](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/45624723690). These are historical baseline checks, not evidence for the candidate revision. Existing release workflow separates read-only qualification and contents:write publication, pins Actions and installs hash-locked CPython 3.11/Linux binary dependencies. Candidate checks must establish clean lock install, full regression, cross-language conformance, workflow governance, documentation and publication preflight on the exact candidate. Verify active protected-main rules and actual DCO checks. No change to release workflow is proposed by this increment.

## Historical DCO exception

Toolkit #1267 accepted exact tested state tree from ca343bb036635d4b70d26a2f4728dda4af9b268e. Squash f12762890d7aa2e3e0cce47733a85d79fa0db701 retained App author without matching App trailer; original head had matching DCO and required PR check passed. Squash author trailer mismatch remains a contribution-governance discrepancy. See [PR record](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1267#issuecomment-7163944242). Do not rewrite protected main or retroactively assert certification. Require explicit owner disposition of this exception before qualified promotion; future App-authored squash must retain verified matching App trailer and any applicable maintainer trailer. Subsequent green DCO only certifies those subsequent commits.

## Residual security and privacy boundaries

- Effective organization/token permission ceilings, raw Actions log retention and private environment administration: NOT VERIFIED (#958).
- Attributable independent human security review: NOT VERIFIED; independent external adoption: NOT_YET_TESTED (#939).
- Git retains assurance state, not sensitive execution exhaust. Public logs/artifacts may expose operational metadata; no secrets/raw personal evidence in them. Existing 14-day representative ephemeral retention remains distinct from raw log policy.
- Registry transfer authority and source-specific observer evidence do not establish complete migration or cross-repository atomicity. #123/#126 live ceremony admission/qualification and nine-event canonical accounting remain separate.
- People-impact causal pathway qualification and deployment certification are not implied by release qualification.

## Gate interpretation

No release authorization from this document. At promotion, bind actual candidate checks and a dated bounded security disposition to the evidence SHA. Owner must explicitly dispose of the historical DCO discrepancy and accept remaining bounded security scope; independent human review is not supplied by automation. Missing evidence or unaccepted governance exception remains a release blocker.
