# Assessment issue ownership

RAHP distinguishes an **observation**, an **assurance proposition**, and the GitHub **work item that owns that proposition**.

An observation is evidence that something changed: a new portfolio snapshot, repository revision, upstream discussion, or other monitor signal. Observations are repeatable and may occur many times while the underlying assurance question remains the same.

An assurance proposition is the semantic question RAHP must resolve. Its stable `rahp-assessment-key` is the durable identity used by automated publication. For bounded portfolio reviews, repeated observations routed to the same assessment key belong to the same proposition unless the routing layer deliberately declares a distinct lineage or proposition.

A GitHub assessment issue is the durable owner of that proposition. Closing the issue records a terminal disposition for the assessed evidence epoch; it does not erase ownership. A later observation with the same assessment key therefore does not create a successor issue merely because the owner is closed.

## Publication rules

1. **No existing owner:** create an issue for the new assessment key.
2. **Open owner:** coalesce the observation into that issue and preserve provenance.
3. **Closed owner, no invalidation:** retain the terminal owner and suppress creation of a new issue.
4. **Closed owner, explicit invalidation/retest:** reopen the same owner only when the event declares `reopen_closed: true` and supplies a non-empty `retest_reason`.
5. **Duplicate issues:** an issue closed with state reason `duplicate` never displaces a non-duplicate owner for the same assessment key.
6. **Epoch-scoped controllers:** portfolio controller keys may intentionally include a snapshot date or clean-room lineage. Their child reviews should still resolve to durable proposition owners where the child assessment key is stable.

## Non-inference boundaries

- new observation != new proposition;
- new snapshot != new child issue;
- new repository SHA != automatic invalidation of a terminal assurance conclusion;
- closed issue != permanently true conclusion: an evidenced retest condition may reopen it;
- workflow success != assurance PASS;
- implementation fail-closed != resolution of a missing normative proposition.

## Retest/invalidation responsibility

The publisher does not infer semantic invalidation from a SHA change. The producer/routing layer must decide that a source change materially alters a proposition premise and emit the explicit retest signal with a reason. This keeps the publication layer deterministic and prevents monitoring frequency from becoming issue churn.

## Regression case

The September 2026 duplicate wave that created RAHP #611–#616 is the reference regression case. Those observations repeated assessment keys already owned by earlier reviews. Re-processing equivalent observations must resolve to the existing durable owner; if that owner is terminal, the result is a terminal-owner suppression unless an explicit retest condition is supplied.
