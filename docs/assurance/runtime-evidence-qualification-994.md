# Scope A/B/C runtime evidence qualification baseline — 2026-10-18

**Owner:** [RAHP #994](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/994). Data: [runtime-evidence-994.json](../../data/assurance/runtime-evidence-994.json).

This is a **nonterminal** executable evidence-manifest guard. Earlier #1048 implemented source/code-available cases, and #1063 corrected the false negative for wallet sign-in. Neither proves a real deployed system's authorization, privacy or protocol composition outcomes.

- **A: Trigger-link and wallet authorization.** Requires wrong origin, wrong persona, stale signature, replay and consent withdrawal traces. Includes corrected source finding `aa28149c7babc678e9e7`.
- **B: Foreign-protocol exchange binding.** Requires task-context-free attempt, wrong audience, expired exchange and replay-after-completion traces.
- **C: VTA-held-key protocol signatures.** Requires wrong-purpose, key, context and requester negatives, stale authority, replay, distinct JWS/CSR obligations.

Every scope begins `INDETERMINATE`; unexecuted cases are proposed probes, **not observed failures or PASS**. The gate intentionally excludes PASS as a valid statement from this *unreviewed routing manifest*: a qualified, independently governed assurance judgment is a separate record. FAIL requires a source-pinned, attributable observation. TRANSFERRED requires a durable successor issue. A privacy referral must point to a DPIP issue, while an exclusion requires a reviewable rationale. Retained-evidence inventories remain absent until observed; null is not evidence of zero retention.

Run:

```bash
python3 tools/validate_runtime_evidence_994.py
python3 -m unittest tests.test_runtime_evidence_994 -v
```

The validator checks machine-readable scope completeness and audit metadata. It **does not** execute VTI components or verify cryptographic evidence; only an actual source-pinned deployment or equivalent reproducible consumer run can satisfy #994 runtime requirements. Preserve exact deployment revision, actor, task identity, challenge, nonce, request and resulting status, privacy-compatible redactions, artifact SHA-256, environment/clock and replay command for any later evidence. Sensitive raw tokens should not be committed.

**Next trigger:** when real A/B/C client/service traces are available, add them through a source- and review-governed evidence channel and independently evaluate privacy/retention impact; do not silently flip the manifest to PASS.
