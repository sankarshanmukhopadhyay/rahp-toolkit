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

## Reservation before new-case publication

A **reserved** entry has an exact assessment key, original Toolkit issue URL,
source commit, finding ID and committed Registry `outbox/pending/*.json` intent.
It intentionally has no Registry issue URL. The Toolkit publisher rejects that
key and any related key just as it rejects an accepted transfer; it does not
silently drop or coalesce the observation. This permits source-specific
suppression to precede Registry's first new-case POST without fabricating a
successor identity.

The `reserved` entry is **not** Registry publication authority by itself.
Before activating one, the Registry must verify the live Toolkit default-branch
ledger, exact committed pending intent, current source/consumer correlation,
all affected Toolkit writers and rollback. A failure after reservation leaves
Toolkit publication blocked for that proposition until the Registry owner is
verified or the reservation is deliberately withdrawn, with the outbox intent
retained. The next phase replaces reservation with an `accepted` entry naming
the actual Registry issue. Do not remove a reservation merely because a POST
timed out. Existing history remains unchanged; empty ledger is the production
default until an authorized case qualifies.

## Source-scoped reservation and stale-run protection

The guarded DTG selector now permits publication of **unrelated retained
events** while an exact source-qualified `reserved_group` transfer is held.
The held group remains in the source partition with both its original and
journal-enriched event identities. This selection does **not** establish
Registry ownership or current observation acknowledgment.

The canonical Toolkit publisher also re-reads the live Toolkit main transfer
ledger before each issue mutation and refuses an event whose exact or related
assessment key has become transferred. It fails closed on unavailable or
changing branch authority. This narrows stale-checkout exposure without
providing an atomic condition on the eventual GitHub issue POST/PATCH.

**Operator requirement before activating the reservation:** stop/drain all
affected in-flight Toolkit issue writers, ensure no older unchecked publisher
can resume, and maintain exclusive control of effectful delivery while the
Registry owner and observation are established. The other Toolkit writer
entry points and first-party consumer issue-number references must be checked
before any live cutover. GitHub Actions concurrency is repository-scoped and
the separate Registry concurrency group does not establish cross-repository
mutual exclusion.

Rollback of an accepted transfer cannot consist of deleting its ledger
entry. The Registry writer must first be durably fenced and its accepted
observations preserved, followed by an explicitly authorized reverse
ownership transition and current-source requalification. No live rollback,
owner creation or production transfer is implemented by this increment.
