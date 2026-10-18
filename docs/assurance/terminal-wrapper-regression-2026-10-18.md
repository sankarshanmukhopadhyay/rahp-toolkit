# Historical wrapper reopening regression and repair — 2026-10-18

**Observed production regression:** After #121 and #527 were deliberately CLOSED as transferred, GitHub Actions reopened both at approximately **06:54 UTC** on 18 October in [DTG Portfolio Monitor handoff run 39105686672](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/39105686672), job `handoff`. GitHub issue-event history attributes both reopening operations to `github-actions[bot]`, not a human reviewer.

The downloaded artifact `12128461940` has `combined-events.json` records for `dtg:portfolio:combined:openvtc-security-combined` and `dtg:portfolio:combined:data-room-custody-lifecycle` with `reopen_closed_owner=true` and `retest_reason` set, despite the repository's transferred-wrapper opt-in marker having already been placed in the issues. This establishes that the earlier marker-dependent safeguard was insufficient in the **actual issue-index/event enrichment path**. The exact reason the marker was not visible to the gate at evaluation time cannot be proved from the artifact alone; avoid asserting a specific pagination or GitHub projection defect as established fact.

**Bounded correction:** Two *explicitly documented historical assessment keys* are now recognized even when issue-list lookup returns no owner or omits the opt-in marker:

- `dtg:portfolio:combined:openvtc-security-combined` → historical #121.
- `dtg:portfolio:combined:data-room-custody-lifecycle` → historical #527.

For these two keys, a previously unseen qualifying finding is never silently ignored: its set receives a deterministic, separately accountable successor assessment key and explicit review/DPIP transfer gates rather than reopening the archived wrapper. A genuine `invalidation_reason` is still allowed to reopen the terminal record if the original conclusion itself is specifically disproved. The normal fail-closed behavior for all **other** closed owners is unchanged. The earlier opt-in marker remains supported.

**Tests:** `tests/test_portfolio_materiality_journal.py` now covers missing marker on a known closed wrapper, absent issue-index owner for the Data Rooms key, and explicit normative invalidation bypass of successor routing. The two keys are intentionally fixed and limited; adding another key requires a reviewed terminal-transfer justification.

**Closure boundary:** This repairs identity/lifecycle routing, not downstream runtime behavior. Original #121/#527 successor owners remain #994/#908/#610 and #481/#482/#608/#609 respectively. Changes that cannot be mapped to an existing successor receive a new bounded assessment; no assurance PASS is inferred.
