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

## Guarded retained-event publication

The DTG workflow now selects publication inputs after the lossless staging check and before canonical issue publication. With the existing empty transfer ledger, it selects all three original input files unchanged and retains their existing semantics. A reserved group, older single-case transfer or mixed ledger remains fail-closed.

A future accepted_group record must specify the exact Monitor commit, grouped findings, source event digest, Registry case URL and maintainer scope digest. The selector rechecks source-event conservation, the unique open Registry issue, authenticated current-event acknowledgment on that issue, the maintainer decision without later withdrawal, and stable Toolkit/Registry main revisions. Only then does it forward retained-only batches into the existing canonical publisher and transfer preflight. No approval, owner, or source receipt is inferred merely from the record being syntactically valid.

No accepted-group entry or current observation comment has been activated, and there is no operational rollback or first-party specialist/controller migration evidence yet. This change introduces a protected path, not a cutover declaration or assurance PASS. Source changes fail before publication; no silent Toolkit fallback is authorized.
