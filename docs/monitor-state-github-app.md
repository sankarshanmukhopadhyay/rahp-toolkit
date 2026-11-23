# Monitor-state GitHub App credential boundary

The incremental instance monitor **observes** DTG/CAWG sources using its
read-only authority and **publishes** eligible assessment events using its
separately scoped `publish_external` job. A GitHub App installation-token
preflight runs **before observation or issue publication**; the short-lived
preflight token is not passed to assessment scripts. The `persist` job mints
a separate short-lived installation token for the signed observation-state
branch push and protected-main PR creation. It does not own RAHP assessment
cases, authorize Registry transfers, execute specialist reviews, or bypass
GitHub rulesets.

## Operational qualification

The live [monitor run #45089579389, attempt 2](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/45089579389)
authenticated the installed repository-scoped App, observed DTG/CAWG source
state, completed external publication and staged a signed state branch.
[App-authored PR #1248](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1248)
passed native DCO, validation, impact, build and TypeScript conformance checks,
then merged through normal protected-main rules as
`5ffdf6e0b1df17b61160ed725ffc3188def028d4`. Canonical reconciliation
and Toolkit-local incident processing subsequently passed. This qualifies
the **state-PR authentication and persistence path** without claiming
external Registry case-owner or publisher cutover.

An earlier attempt to retry only a failed persistence job exposed a separate
recovery limitation: per-attempt artifact names do not carry forward to a
failed-job-only retry when observation was successful in the preceding
attempt. Do not substitute a previous attempt's artifact implicitly. Use
a fresh, fully observed current-main run (or a separately evidence-qualified
replay mechanism) rather than claim a persistence-only retry succeeded.

## Repository administrator setup

Install a dedicated GitHub App **only** on
`sankarshanmukhopadhyay/rahp-toolkit` with repository permissions:
**Contents: Read and write** and **Pull requests: Read and write**.
It does not need Issues, Actions, Checks, Administration, or permission to
merge protected `main`. In Toolkit's Actions settings, configure:

- Repository variable `RAHP_STATE_APP_ID`: numeric App ID.
- Repository secret `RAHP_STATE_APP_PRIVATE_KEY`: complete PEM private key.

Never print or commit the private key. Rotate it through GitHub App settings
and update the Actions secret if compromised. Remove the App installation to
revoke future state-writing authority. Keep a scope review on any App
permission or installation change.

## Runtime and credentials

The job uses SHA-pinned `actions/create-github-app-token` to request a
short-lived, installation-scoped token limited to this repository and the two
write permissions. `actions/checkout` does not retain the default workflow
token in Git configuration. Git resolves the authenticated App bot identity
for the author and its matching DCO Signed-off-by trailer. A temporary Git
credential helper supplies the App token for the **one branch push**; `gh`
uses it to create the state PR. Token values are not written to repository
files or printed in logs.

The native `pull_request` event from the App-created PR must execute required
checks on the PR merge candidate. Previously implemented `workflow_dispatch`
head checks remain available for targeted diagnostics, but **do not**
substitute for required merge-candidate checks. No automatic merge is granted.
Only merged, protected-main state is eligible for canonical reconciliation
and Toolkit-local incident publication.

## Qualification checklist

1. Review the PR that changes the workflow; require DCO, actionlint,
   governance, validation, build, impact and TypeScript checks.
2. Observe a genuine subsequent `instance-monitor-main.yml` run. Verify
   `monitor`, `publish_external` and `persist` succeed and one branch
   `automation/instance-monitor-<run>-<attempt>` is created by the App.
3. Inspect the **PR actor**, signed state commit and native PR-triggered
   required checks. Confirm that the synthetic PR merge candidate has the
   required successful checks, not merely its branch head.
4. Accept the PR through normal protected-main merge only after all checks
   pass. Verify `dtg-assurance-reconcile.yml` runs `reconcile` and
   `local_incidents` after acceptance, not before.
5. Re-run monitoring with the accepted baseline. Confirm there are no
   duplicate issue effects or orphan branches and that Registry transfer
   fences still reject Toolkit publication for Registry-owned keys.

If the App ID, private key, installation, bot identity or permission
qualification is unavailable, the persistence job must **fail closed**.
Do not fall back to the default `GITHUB_TOKEN` for PR creation, disable
branch protection or make a fake status check green. Preserve the monitored
source artifact for controlled replay. This credential does **not** complete
the independent Toolkit-to-Registry producer migration tracked in Registry
issue #77.
