# Registry transfer publication guard

The Toolkit publisher remains the operational source until an individual
assessment proposition has a verified Registry successor and a coordinated
consumer/publication cutover.

`instances/dtg/registry-transfers.json` is a deliberately empty exclusion
ledger. Each future accepted entry must name an exact assessment key, the
original Toolkit issue, and its Registry successor. It is not an authorization
to publish in Registry. The current Toolkit publisher refuses the **entire**
batch if an accepted transferred key is encountered (including through
`related_assessment_key`). This leaves the original input available for
controlled replay; it neither drops an observation nor reopens the historical
Toolkit owner.

Before admitting a nonempty entry, verify the reciprocal live issue links,
source-proposition ownership, active publication path, source-pinned pending
intake, DPIP/review-worker issue-number correlation, no duplicate owner, and
rollback. Coordinate the Toolkit workflow and Registry outbox changes in the
same controlled migration exercise. A ledger entry alone does not establish
exclusive authority or RAHP assurance PASS.

The empty ledger changes no production routing. Use existing Toolkit tests,
the Registry outbox/consumer tests, and manual dispatch for the cutover
evidence. No new scheduled workflow is required.

## DTG materiality batch preflight

The DTG materiality handoff performs an **all-batch read-only preflight**
after materiality enrichment and controller-event generation, before its first
GitHub issue publication. Run the equivalent check manually with:

```sh
python3 tools/publish_assessment_issues.py --check-transfers \
  build/dtg-routing/controller-events.json \
  build/dtg-routing/combined-events.json \
  build/dtg-routing/dpip-events.json
```

This validates the exact key and related-key boundaries across the three
publication batches. Invalid, missing or non-array input fails before any
Toolkit issue is mutated by those publication steps. This does **not** make
the multi-repository cutover atomic or cover other Toolkit workflows and
independent controller-incident publishers. An accepted transfer must not be
activated until those remaining producers and first-party consumers are
addressed.
