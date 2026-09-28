# Decision-Resolution Assurance — Experimental Branch Note

**Status:** experimental, branch-only; not part of the RAHP stable capability boundary.

## Assurance question

Can an assessed trust system demonstrate that:

1. authority is not amplified by communication, repetition, endorsement, aggregation, discovery, projection, reputation, or unrelated delegation;
2. a material decision transition preserves whether its causal basis was authority, evidence, policy, lifecycle, correction, or evaluation-context change; and
3. a material unresolved condition does not silently disappear merely because workflow execution progressed?

## Assessment propositions

### RAHP-DR-01 — authority non-amplification

PASS requires positive evidence that the authority used for a consequential action traces to competent authoritative provenance, applicable scope, current lifecycle state, and governing policy.

Peer influence, repetition, consensus, reputation, discovery, capability, or possession of unrelated authority MUST NOT substitute for that evidence.

### RAHP-DR-02 — decision-basis separation

Where a material decision changes, the assessment SHOULD be able to determine which material input changed.

An evidence-, policy-, lifecycle-, correction-, or evaluation-context change MUST NOT be reported as an authority grant merely because the resulting decision became more permissive.

Missing or contradictory causal-basis evidence remains INDETERMINATE/AMBER unless governing policy requires a stricter outcome.

### RAHP-DR-03 — explicit resolution

A material unresolved condition MUST remain open until evidence establishes an admissible resolution event.

Workflow progression, peer pressure, repetition, confidence, or reputation are not resolution evidence.

A previously resolved condition MUST be reassessed when material authority or evidence becomes revoked, stale, conflicting, unsupported, or otherwise invalidated before the consequential transition.

## Minimum evidence

An assessment should seek:

- condition/proposition identifier;
- establishment time and evidence;
- prior and current decision references where applicable;
- exact action/effect boundary;
- causal transition category;
- authority/evidence/policy/lifecycle references supporting that category;
- evaluation time and freshness;
- status/revocation evidence;
- evidence sufficient to reconstruct why the condition remained open, resolved, or reopened.

## Disposition discipline

- Missing resolution evidence never becomes PASS.
- A green workflow is not resolution evidence.
- Agreement among several non-authoritative actors is not authority evidence.
- Evidence that changes a factual predicate is not authority evidence unless an independent authority event also occurred.
- False persistence is also a defect: if admissible current evidence resolves the condition, an implementation that remains blocked should not be described as correct merely because it is conservative.

## Portfolio authority boundary

TSMM owns canonical decision-resolution semantics. TIS owns portable serialization where adopted. ARPA owns its authority/delegation protocol semantics. The Trust Protocol Interop Lab can produce executable composition evidence. RAHP independently assesses whether evidence is sufficient for an assurance proposition and does not acquire authority over those source semantics.

## Research provenance

This branch-only experiment is informed by the TSMM/TIS/ARPA/ARA workstream and a read-only review of the independent **Protocol of Care for Agents** project:

- https://github.com/JessHines360/protocol-of-care-for-agents
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/BRIEF.md
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/experiments/SIMULATION_01_RUNBOOK.md

RAHP does not adopt `CareSignal`, `DeliberativeHold`, or the upstream normative vocabulary. No upstream writes were made.

## Branch constraint

This work intentionally remains on `research/decision-resolution-assurance`. It MUST NOT be treated as part of the stable RAHP release boundary unless a later, separately approved qualification tranche promotes it.
