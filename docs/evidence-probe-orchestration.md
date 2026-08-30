# Evidence-probe orchestration

RAHP/DPIP evidence requirements are not satisfied merely because a requirement exists, and they are not legitimately `NOT_EVIDENCED` merely because a workflow omitted the corresponding probe.

For every required evidence item, the assurance lineage must retain an attempt state:

- `EXECUTED` — an applicable producer materially ran; its result may be `SATISFIED`, `ABSENT`, or `NOT_EVIDENCED` only if the producer itself reports that the required surface was not materially exercised.
- `ATTEMPTED_UNAVAILABLE` — an applicable producer was invoked but could not complete/materially execute; the evidence result remains `NOT_EVIDENCED` with the failure reason.
- `NO_APPLICABLE_PRODUCER` — no registered producer can currently exercise the required target/surface; the result remains `NOT_EVIDENCED` and the missing capability is explicit.

An evidence requirement with no attempt-ledger entry is an **orchestration defect**, not an assurance result.

This preserves three boundaries:

1. workflow completion never becomes assurance PASS;
2. missing probe execution is distinguishable from a target that executed and exposed no relevant value (`ABSENT`);
3. composition/runtime producers remain attributable to the component that actually produced the observation and must not be silently re-attributed to the target under assessment.
