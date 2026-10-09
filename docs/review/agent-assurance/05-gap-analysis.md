# Agent assurance I1 — preliminary gap analysis

Tracking: #970

## Confirmed architectural non-gaps
The bounded current-main inspection does **not** support creating:
- a second assurance controller;
- new terminal outcomes;
- an agent-only evidence store;
- an agent runtime or authorization service inside RAHP.

Existing contracts already provide portable authority, delegation, evidence, graph and specialist-result surfaces.

## Candidate gaps requiring executable verification
1. **Human confirmation enforcement (AAP-007):** the inspected delegation contract can declare the requirement; this baseline has not established evidence that performance is enforced.
2. **Action/effect boundary (AAP-011):** existing scopes can express bounded authority, but generic enforcement against observed tool/API effects has not been established.
3. **Replay/idempotency (AAP-012):** no generic consequential-effect replay control was established in this bounded inspection.
4. **Temporal authority composition (AAP-004/005/015):** relevant structural and optional temporal machinery exists, but a portable agent-specific composition of validity, revocation and evaluated action time needs qualification.
5. **Delegation composition and substitution (AAP-008/009/010):** substantial prior issue work exists; implementation/test reuse must be proven before new code.

## Do not open implementation issues yet
Each candidate gap must first be checked against current implementation and tests. A missing citation is not evidence of missing code.
