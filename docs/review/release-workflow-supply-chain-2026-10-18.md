# Release-workflow supply-chain evidence checkpoint — 2026-10-18

**Owner:** [RAHP #958](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/958). Scope: **current main only**; no change to historical v2.7.0 release tag, published notes or original acceptance decision.

## Verified immutable Action identities

The release and release-codename-policy workflows previously referenced floating `v7` tags. Their upstream GitHub `git/ref/tags/v7` references were fetched and resolved to **commit** objects, not inferred from release names.

| Action | Immutable commit SHA | Source |
| --- | --- | --- |
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | `https://api.github.com/repos/actions/checkout/git/ref/tags/v7` |
| `actions/setup-python` | `5fda3b95a4ea91299a34e894583c3862153e4b97` | `https://api.github.com/repos/actions/setup-python/git/ref/tags/v7` |
| `actions/setup-node` | `949feb2413d6458794dcd2491c4babbbce0c15c1` | `https://api.github.com/repos/actions/setup-node/git/ref/tags/v7` |

`.github/workflows/release.yml` and `.github/workflows/release-codename-policy.yml` now use those exact commits with human-readable version comments. `tests/test_release_action_pins.py` rejects mutable tags, unsupported shapes and unexpected changes to approved Action SHAs. The policy test runs under the repository's Python unittest discovery in CI.

## Permission and trust-boundary inventory

- `release.yml` grants `contents: write` at workflow level because the single publication job creates/updates a Git tag and GitHub Release. The entitlement currently extends to earlier validation steps in that same job. **Least-privilege job isolation remains a residual**: a subsequent engineering tranche should split qualification (read-only) from publication (write), pass an immutable validated candidate SHA and recheck authorization at the privileged step.
- `release-codename-policy.yml` is `contents: read`.
- `pages.yml` uses `contents: read` in build; the deploy job requests `pages: write` and `id-token: write` for publication. Runtime deployment environment protection and operator access have **not** been independently inspected.
- These are repository YAML declarations, **not** verification of organization settings, active token entitlements, environment rules, artifact accessibility or their retention.

## Remaining #958 obligations

1. Verify live effective token permissions and environment protection, not just YAML.
2. Implement and test a reviewed hashed Python dependency lock with supported fresh installation.
3. Verify private/output artifact and CI-log retention/access policies in the actual GitHub repository settings.
4. Obtain attributable independent human review of the exact commit, scope and test evidence.
5. Update current-main security disposition following those results. Preserve historical accepted residuals for v2.7.0.

**Assurance judgment:** this increment removes mutable third-party Action refs from the two named release workflows with verifiable upstream identities; it does **not** complete #958, constitute independent security certification, or retroactively qualify any prior release.
