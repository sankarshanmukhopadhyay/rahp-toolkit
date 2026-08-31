# DTG assurance operating modes

RAHP has two conceptually different DTG assurance operations. They must not be conflated.

## Incremental instance monitor

The scheduled GitHub Actions workflow is a **stateful, delta-driven monitor**. It compares the current DTG portfolio and selected architecture issues with persisted RAHP instance state.

A successful monitor run means the monitoring machinery executed successfully. It does **not** mean the current DTG portfolio has been freshly reassessed from first principles, and it does not imply an assurance-GREEN outcome.

When there are no new material events, the correct monitor behaviour is to create no new assessment issue.

The end-to-end reconciler still evaluates retained gatherer lineages. If it reports `RED / PIPELINE_BROKEN`, existing RAHP/DPIP issues remain the durable owners when the blocker already references them. The monitor creates a separate controller incident only for broken-pipeline blockers that have no durable issue owner.

## Clean-room assessment

A clean-room assessment is a separate assurance operation. It should:

- start from a new immutable portfolio snapshot;
- evaluate the configured portfolio independently of prior assessment conclusions;
- preserve prior evidence only as attributable source material, not as an inherited disposition;
- create a distinct gatherer/evaluation lineage;
- execute materiality, RAHP/security/composition analysis and DPIP routing as warranted; and
- reach an independently attributable terminal portfolio conclusion.

The incremental monitor must never be presented as having performed this operation.

## Interpretation rule

Always distinguish:

```
workflow success != assurance GREEN
incremental monitor != clean-room assessment
existing blocker owner != need for duplicate issue
unowned RED blocker => durable controller incident
```
