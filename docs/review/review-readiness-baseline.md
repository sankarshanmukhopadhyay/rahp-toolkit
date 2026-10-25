# RAHP Independent Review Readiness Baseline

Status: initial baseline for independent third-party review preparation.

## Repository baseline

- Default branch: `main`.
- Stable release declared by the repository: `v2.9.0` (Common Windmill).
- Primary runtime exercised by CI: Python 3.11.
- Ordinary contributor/test dependencies in `requirements.txt` use minimum-version constraints. The governed release runner separately uses the hash-locked `requirements-release.lock`; these are different reproducibility boundaries.
- The primary validation workflow is `.github/workflows/validate.yml`.
- The workflow runs repository validation, portable assurance validation, negative-fixture validation, unit tests, security-review validation, specialist/reconciliation checks, VTI assessment checks, engine-contract checks, generated-view checks, and other bounded conformance surfaces.

## Existing assurance posture

The repository already declares and exercises several review-relevant invariants:

- missing evidence does not become PASS;
- workflow success is distinct from assurance success;
- component PASS does not imply composition PASS;
- specialist results cross explicit boundaries;
- provenance, freshness and source-pinned evidence are material to conclusions;
- indeterminate outcomes are first-class.

These are claims to be independently tested, not premises the reviewer is expected to accept.

## Initial review risks / evidence gaps

1. **Environment reproducibility:** minimum-version dependency declarations do not by themselves establish bit-for-bit or dependency-graph reproducibility.
2. **Review navigation:** review evidence is distributed across method, tools, tests, fixtures, release records and documentation; an external reviewer needs a bounded entry path.
3. **Claim traceability:** material assurance claims need a compact claim → evidence → falsification ledger.
4. **Security scope:** existing security validation does not substitute for an explicit threat model of RAHP as an assessor processing hostile evidence.
5. **Semantic coverage:** conventional test execution does not by itself show proposition coverage across missing, stale, contradictory, non-independent and composition evidence.
6. **Known limitations:** limitations and externally owned evidence gaps need one candid reviewer-facing register.

## Current review-readiness state

The working pack is synchronized to the current stable release boundary, but **no independent external audit or certification is claimed**. Repository-defined review-readiness validation establishes that the reviewer surface is internally synchronized and reproducible enough to challenge; it does not establish that an independent reviewer has executed or accepted the pack.

The original v2.4.0 baseline exposed several review gaps. Subsequent work added the claim/evidence ledger, false-assurance challenges, hostile-input pre-review, release dependency lock, clean-runner reproduction evidence and stable-boundary synchronization. Remaining limitations are recorded in `docs/review/known-limitations.md`.

## Baseline next actions

- publish the external review charter;
- establish the high-materiality claim ledger;
- document architecture/trust boundaries;
- threat-model hostile assessment inputs;
- expand false-GREEN challenges;
- execute clean-environment reproduction;
- publish semantic coverage and limitations;
- assemble the reviewer working pack.

No release/tag is created at this stage.
