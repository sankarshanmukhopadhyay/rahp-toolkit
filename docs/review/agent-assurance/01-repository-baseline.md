# Agent assurance I1 — repository qualification baseline

Tracking: #970

## Purpose
Record the current-main capabilities that can support a portable agentic assurance profile before any new evaluator or controller behavior is introduced.

## Verified current-main baseline
The current RAHP architecture is already profile-oriented and agent-independent. The generic engine owns lifecycle, evidence/proposition contracts, inference boundaries and terminal semantics; external agents may invoke maintained entry points but do not acquire assurance authority.

Stable portable boundary:
- `rahp-engine-contract-v1`, revision `1.3`
- normalized result schema version `1`
- `rahp-evidence-retention-v1`
- finite specialist outcome: PASS / FAIL / INDETERMINATE / NOT_APPLICABLE

Relevant existing machine-readable surfaces:
- `method/engine-contract.yaml`
- `method/schema/authority.schema.json`
- `method/schema/delegation-scope.schema.json`
- `method/schema/evidence-manifest.schema.json`
- `method/schema/assurance-graph.schema.json`
- `method/schema/assessor-result.schema.json`

Relevant guidance:
- `docs/reasoning-architecture.md`
- `docs/reasoning-integration.md`
- `docs/data-model.md`
- `docs/evidence-adequacy.md`

## Architectural consequence
Agent assurance should begin as an optional profile over existing contracts. No evidence found in this bounded inspection justifies a second controller, a new terminal outcome, or treating an agent runtime as an assurance authority.

## Important existing capability
The current delegation-scope schema already separates principal/delegate, actor class, capabilities, resource scope, human confirmation, delegation depth, purpose, validity and revocation. The authority schema already represents scoped grants and active/suspended/revoked/expired status. These are candidate reuse surfaces, not proof that all #970 propositions are executable today.

## Evidence-conservative boundary
Current documentation explicitly states that RAHP does not automatically confer delegation, authenticate an agent principal, approve policy exceptions, guarantee external freshness, or settle contested substantive judgment. Agent-profile work must preserve those boundaries.

## Initial conclusion
The implementation problem is primarily qualification, proposition mapping and bounded extension. Core redesign is not justified by the evidence inspected for this baseline.
