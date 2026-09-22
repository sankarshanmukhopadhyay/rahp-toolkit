# Authority-at-Commitment Assurance Pattern

## Assessment proposition

A material action MUST NOT be treated as authorized merely because the actor authenticated, signed the request, advertised a capability, has favorable reputation, or possessed some broader delegation. The assurance question is whether **the exact action was covered by current principal-derived authority at the material transition time**.

## Risk patterns

- `RKP-AUTH-04` — commitment authority mismatch;
- `RKP-AUTH-05` — approval not bound to the exact commitment;
- `RKP-AUTH-06` — reputation/capability substituted for authority;
- `RKP-AUTH-07` — commitment authority cannot be reconstructed.

Existing `RKP-AUTH-01..03` and delegation risks remain applicable and should be composed rather than duplicated.

## Evidence questions

An assessor should seek evidence for:

1. the principal and authority source;
2. the actor/delegate and delegation lineage;
3. the mandate effective at the evaluation time;
4. the exact action or canonical digest;
5. material scope/constraint results;
6. fresh status/revocation evidence;
7. exact-action approval when required;
8. policy identifier/version;
9. the resulting decision and stable reason;
10. evidence sufficient for later reconstruction.

## Disposition rules

- **GREEN/PASS is not available from absence of a known blocker.** Positive authority evidence must establish the required propositions.
- Expired/revoked authority, exceeded material constraints, or mismatched approval are negative evidence.
- Missing, stale, ambiguous, conflicting or unsupported material authority evidence remains **INDETERMINATE/AMBER** or a stricter repository-defined posture; it MUST NOT become PASS.
- Reputation, capability, identity, discovery and assurance evidence may inform the assessment but cannot create authority.

## Boundary

RAHP evaluates risks, harms, security/composition concerns and assurance evidence. It does not define the underlying mandate protocol, negotiation state machine, runtime admission policy or settlement semantics.
