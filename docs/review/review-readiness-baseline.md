# RAHP Independent Review Readiness Baseline

Status: initial baseline for independent third-party review preparation.

## Repository baseline

- Default branch: `main`.
- Stable release declared by the repository: `v2.4.0` (Redbreast Jezebel).
- Primary runtime exercised by CI: Python 3.11.
- Python dependencies are declared in `requirements.txt`; the current declarations use minimum-version constraints rather than a fully locked environment.
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

## Baseline qualification state

**NOT YET QUALIFIED FOR EXTERNAL REVIEW CANDIDATE TAGGING.**

This is expected. The readiness tranche exists to establish the missing review evidence without erasing legitimate uncertainty.

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
