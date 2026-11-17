# DTG source-specific Registry partition staging

The Toolkit DTG handoff workflow stages all controller, combined and DPIP
events **after** materiality-journal enrichment and **before** the existing
fail-closed transfer preflight. Artifacts include retained and held exact event
objects, source digests and the validated transfer ledger entries.

Example:

\`\`\`sh
python3 tools/stage_registry_source_partition.py \
  --batches build/dtg-routing/controller-events.json \
  build/dtg-routing/combined-events.json \
  build/dtg-routing/dpip-events.json \
  --out-dir build/dtg-routing/registry-partition
\`\`\`

This stage never changes the original event files or GitHub state.
It deliberately does **not** feed retained output to the publisher. The
existing \`--check-transfers\` preflight still rejects the entire publication
batch if any held proposition matches a reserved or accepted Registry owner.
Reserved transfer intent has no successor. Accepted case succession does not
prove Registry has durably received the **current** observation, nor that
first-party controller, reviewer and DPIP issue-number consumers are migrated.

The staged partition is therefore falsifiable source-conservation evidence,
not cutover authority. No live transfer or Toolkit suppression is enabled.
To use it operationally, require a source-specific durable Registry receipt,
a compatible execution/return adapter and fleet-wide in-flight writer fencing
before a retained partition may be published independently.

## Multi-finding reservation (unactivated)

A monitored grouped proposition is not one source finding. The validated `reserved_group` ledger entry records the existing Toolkit issue, a Registry pending-intent path, an immutable Monitor commit, a snapshot date, sorted unique original 20-hex finding IDs and the SHA-256 of the exact combined event. It is held by the same fail-closed publication preflight as a single-finding reservation and is never accepted or acknowledged by staging. The existing `reserved` and `accepted` entries retain their semantics. No live ledger entry or publisher destination changes in this increment. Group acceptance and source-specific publishing remain gated by a real Registry group acknowledgment, issue-number consumer compatibility and all-writer exclusion.
