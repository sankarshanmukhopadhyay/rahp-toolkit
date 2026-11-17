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
