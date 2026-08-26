# DPIP handoff operations

The RAHP → DPIP handoff is intentionally lower-frequency than repository observation. RAHP may observe and assess changes more often, but cross-repository DPIP referral transport runs **once weekly** after a fresh DTG Portfolio Monitor collection.

## Schedule

`Promote qualified RAHP referrals to DPIP` runs at **04:17 UTC every Tuesday** and can also be dispatched manually.

The DTG Portfolio Monitor currently collects at 00:17 and 12:17 UTC each day. The handoff schedule therefore consumes a recent Tuesday snapshot while avoiding issue churn from twice-daily repository activity.

## Activation

GitHub's repository `GITHUB_TOKEN` is repository-scoped and must not be broadened into an implicit cross-repository credential. Configure this repository secret:

- `DPIP_HANDOFF_TOKEN` — a narrowly scoped fine-grained token able to read metadata and read/write **Issues** only in `sankarshanmukhopadhyay/dtg-privacy-implementation-profile`.

Without this secret the scheduled workflow validates its transport logic and exits without creating DPIP issues.

The reciprocal DPIP repository uses a separate `RAHP_HANDOFF_TOKEN` for the return path. Keeping the directions separate limits blast radius and makes revocation straightforward.

## Promotion remains a RAHP decision

Automation does **not** infer privacy relevance from keywords, severity, repository name, or Monitor classification. It scans only open RAHP issues carrying:

```text
assurance:dpip-requested
```

The issue must also contain a valid `dpip:` YAML block satisfying the documented promotion gate. If the payload is incomplete, transport fails for that issue rather than guessing missing DPIP scope.

## Idempotency

Each transported referral carries a deterministic marker derived from:

- RAHP source issue;
- Portfolio Monitor fingerprint;
- immutable source revision;
- requested DPIP target/question digest.

Before creation, RAHP checks existing `source:rahp` DPIP issues for that marker. Re-running the weekly workflow therefore returns the existing intake instead of creating a duplicate.

## Completion

RAHP changes the source referral to `assurance:dpip-open` once a DPIP intake exists. DPIP's return workflow later posts the concise disposition and changes the RAHP label to `assurance:dpip-complete`.

The automated return does **not** close the RAHP issue: the issue may contain wider RAHP/security work beyond the DPIP subflow. Closure remains governed by the RAHP assessment itself.
