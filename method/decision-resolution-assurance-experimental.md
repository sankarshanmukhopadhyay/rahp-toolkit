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

## Experimental risk, harm, guardrail, and evidence overlay

The assurance propositions are not evaluated in isolation. This branch adds an experimental RAHP-native overlay at `method/catalogue/experimental/decision-resolution-patterns.yaml` so the work can be exercised as a complete assurance chain:

```text
failure pattern
    ↓
risk relationship
    ↓
harm
    ↓
control / guardrail
    ↓
required evidence
    ↓
assurance disposition
```

### Authority laundering

**Authority laundering** is treated as an experimental composite failure pattern rather than a new stable catalogue record. It describes non-authoritative inputs such as peer influence, repetition, consensus, reputation, capability, discovery, endorsement, projection, aggregation, or unrelated authority being transformed or combined until a consequential decision treats them as authority the source did not possess.

The branch deliberately reuses stable RAHP patterns where they already cover the assurance surface:

- risks: `RKP-AUTH-01`, `RKP-AUTH-04`, `RKP-AUTH-06`, `RKP-DEL-01`, `RKP-COMP-04`;
- harms: `HRM-AUT-04`, `HRM-SEC-02`, `HRM-INF-01`, and where applicable `HRM-GOV-01`;
- controls: `CTP-AUTH-01`, `CTP-AUTH-02`, `CTP-AUTH-03`, `CTP-DEL-01`;
- guardrails: `GRP-AUTH-01`, `GRP-AUTH-02`, `GRP-COMP-01`;
- evidence: `EVP-AUTH-01`, `EVP-AUTH-02`, `EVP-DEL-01`.

This means the experiment tests a stronger composition claim without prematurely duplicating the stable catalogue.

### Candidate decision-resolution risks

Three additional candidate risks are kept provisional on this branch:

- `RKP-DR-X1` — **Decision-basis conflation**: an evidence, policy, lifecycle, correction, or evaluation-context change is misrepresented as an authority change.
- `RKP-DR-X2` — **Silent unresolved-condition clearance**: a material unresolved condition is treated as resolved without evidence of an admissible resolution event.
- `RKP-DR-X3` — **False persistence**: a condition remains blocking after current admissible evidence establishes legitimate resolution.

The first two guard against false permissiveness. The third prevents the assurance model from treating indefinite conservatism as correctness.

### Candidate guardrails and evidence

The branch also carries provisional guardrail and evidence patterns:

- `GRP-DR-X1` — no consequential transition through unresolved material state;
- `GRP-DR-X2` — no indefinite blocking after admissible resolution;
- `EVP-DR-X1` — decision-transition basis trace;
- `EVP-DR-X2` — resolution and reopening trace.

These identifiers are experimental placeholders only. They MUST NOT be treated as stable catalogue identifiers unless a later qualification tranche demonstrates a material assurance gap and explicitly promotes them.

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
- Authority laundering is a failed assurance condition when non-authoritative signals are combined, repeated, projected, endorsed, or aggregated into effective authority without competent provenance.
- Decision-basis conflation is a failed assurance condition when a non-authority change is recorded or relied upon as an authority grant.
- Silent clearance and false persistence are dual failures: an assurance system must neither erase unresolved material state without admissible evidence nor preserve it after admissible resolution evidence is current and sufficient.

## Portfolio authority boundary

TSMM owns canonical decision-resolution semantics. TIS owns portable serialization where adopted. ARPA owns its authority/delegation protocol semantics. The Trust Protocol Interop Lab can produce executable composition evidence. RAHP independently assesses whether evidence is sufficient for an assurance proposition and does not acquire authority over those source semantics.

## Research provenance

This branch-only experiment is informed by the TSMM/TIS/ARPA/ARA workstream and a read-only review of the independent **Protocol of Care for Agents** project:

- https://github.com/JessHines360/protocol-of-care-for-agents
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/BRIEF.md
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/experiments/SIMULATION_01_RUNBOOK.md

RAHP does not adopt `CareSignal`, `DeliberativeHold`, or the upstream normative vocabulary. No upstream writes were made.

## Qualification and merge boundary

This work intentionally remains experimental on `research/decision-resolution-assurance`. The branch is designed to remain additive and merge-compatible with `main`: the experimental overlay is namespaced under `method/catalogue/experimental/` and does not modify stable catalogue records.

Merging the branch into `main` would therefore publish experimental research artifacts, not promote them into the stable RAHP capability boundary. Promotion of any provisional `RKP-DR-X*`, `GRP-DR-X*`, or `EVP-DR-X*` identifier into the stable catalogue requires a later, separately approved qualification tranche.
