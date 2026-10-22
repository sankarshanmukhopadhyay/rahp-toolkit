# Current-main release security disposition — 2026-10-22

**Tracking:** #958  
**Scope:** current `main` release engineering and representative CI evidence.  
**Historical boundary:** this record does not alter the v2.7.0 tag, its publication decision, or the historical v2.7 security disposition.  
**Assurance boundary:** bounded source/configuration/CI review; **not** an independent security audit or penetration test.

## Executive disposition

Current release engineering has materially improved since v2.7.0:

- release-related third-party Actions are pinned to reviewed immutable SHAs;
- release qualification is read-only and publication authority is isolated to a distinct `contents:write` job;
- `protect-main` is active with strict required checks, linear history, pull-request enforcement and no bypass actors;
- repository web commit sign-off is required;
- release Python qualification uses a reviewed hash-locked CPython 3.11/Linux dependency set;
- CI independently proves a clean hash-enforced installation of that set;
- representative ephemeral validation artifacts explicitly use the portable RAHP 14-day retention default.

These controls are release-readiness evidence. They do not establish effective organization-level token policy, GitHub log-retention settings, private environment protections, or independent human review.

## Evidence table

| Area | Evidence | Disposition |
| --- | --- | --- |
| Release Action identity | Release/codename Actions pinned to reviewed commit SHAs; regression coverage rejects mutable refs | **CONTROLLED** |
| Publication privilege | `release.yml` qualification is `contents: read`; write authority exists only in the publication job after qualification and explicit publication classification | **CONTROLLED** at workflow declaration |
| Branch/repository gate | Active `protect-main` ruleset requires PRs, linear history, strict status checks including `validate`, `build`, and `DCO`; no bypass actors | **CONTROLLED** at readable repository ruleset |
| Commit sign-off | Repository API reports `web_commit_signoff_required: true`; repository-native DCO is a required branch check | **CONTROLLED** for governed contributions |
| Python supply chain | `requirements-release.lock` pins the exact package set observed in successful current-main CI and supplies SHA-256 hashes; release install uses `--require-hashes --only-binary=:all:` | **CONTROLLED** for GitHub-hosted CPython 3.11/Linux qualification |
| Lock installation | `validate.yml` creates a clean venv, installs only the release lock and imports the direct RAHP tooling dependencies | **EXECUTABLE EVIDENCE REQUIRED/PRESENT when CI passes** |
| CI evidence retention | The portable policy defines ephemeral evidence as 14 days. Representative validation artifacts now declare `retention-days: 14` explicitly | **CONTROLLED** for those workflow artifacts |
| Raw GitHub Actions logs | Repository is public; workflow logs can contain operational metadata. Admin-level log-retention settings are not exposed through the available connector | **EXTERNAL / NOT VERIFIED** |
| Effective organization/token policy | Workflow YAML is inspectable, but GitHub Actions permission/admin endpoints are unavailable through the current integration | **EXTERNAL / NOT VERIFIED** |
| Environment protection | Release workflow does not currently declare a protected GitHub Environment; organization/repository environment policy was not independently inspected | **DISCLOSED RESIDUAL** |
| Independent human security review | No attributable independent human reviewer has been recorded for this current-main security disposition | **PENDING HUMAN EVIDENCE** |

## Dependency-lock scope

The release lock is intentionally narrower than `requirements.txt`.

`requirements.txt` remains the portable development/tooling declaration. The release lock captures the exact dependency set used to qualify and publish on the governed GitHub runner:

- Ubuntu `ubuntu-latest` x86-64;
- CPython 3.11;
- binary distributions only;
- exact versions and SHA-256 digests.

The locked versions were derived from successful current-main validation run 39725166992, then converted into a reviewed hash-enforced set. Platform-specific binary hashing means this file is not represented as a universal developer lock.

## Privacy and retention

RAHP's portable retention rule remains: **Git preserves assurance state, not execution exhaust.**

Representative validation artifacts contain reproducibility output, bounded sociotechnical replay evidence and human-power reconciliation evidence. They are operational evidence rather than durable governance state, so the workflow now applies the method's 14-day `ephemeral` default explicitly.

This repository is public. Workflow logs and intentionally uploaded artifacts must therefore be treated as potentially publicly observable while retained. Sensitive assessment payloads, secrets, raw personal data and unrestricted deployment evidence must not be placed in those artifacts. Large/sensitive evidence belongs in deployment-controlled storage and should be referenced through integrity-protected manifests under `rahp-evidence-retention-v1`.

The GitHub repository-level default for logs/artifacts could not be read through the current integration. Before this change, live artifacts from run 39725166992 showed an approximately 90-day expiry. Explicit 14-day workflow retention removes dependence on that default for the representative uploaded validation artifacts; it does not change raw Actions log retention.

## Residuals and release interpretation

The following are **not** converted into PASS:

1. effective organization-level Actions permissions and token ceilings;
2. repository/organization log-retention configuration;
3. any protected-environment policy outside the checked-in workflow;
4. independent human security review.

These are external/governance evidence obligations. A future release qualification may disclose them as bounded residuals if the release owner accepts that scope; it must not call this record an independent audit.

## Current-main judgment

No release-blocking source/configuration defect is known in the reviewed release pipeline after the controls above are validated by CI. The engineering security tranche can be considered complete when its PR is merged and the clean locked-install/retention tests pass.

**Independent human security review remains a separate human-governance obligation.** It cannot be satisfied by CI, repository automation or AI-assisted review.
