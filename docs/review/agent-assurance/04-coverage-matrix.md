# Agent assurance I1 — initial coverage matrix

Tracking: #970

This matrix is deliberately conservative. “Structural” means the concept can be represented by an existing contract; it does not claim enforcement.

| Proposition | Current candidate coverage | Evidence state | Decision |
| --- | --- | --- | --- |
| AAP-001 | evidence producer actor; delegation delegate; existing actor-substitution work to inspect | PARTIAL / VERIFY | REUSE/EXTEND |
| AAP-002 | delegation principal; authority issuer/subject | STRUCTURAL | REUSE/EXTEND |
| AAP-003 | delegation capabilities/resource_scope; authority grants/scope | STRUCTURAL | REUSE |
| AAP-004 | delegation validity; authority valid_from/valid_until | STRUCTURAL | QUALIFY evaluator |
| AAP-005 | authority status; delegation revocation metadata | PARTIAL STRUCTURAL | QUALIFY authoritative status |
| AAP-006 | authority grant action/scope + delegation capabilities | PARTIAL STRUCTURAL | QUALIFY action binding |
| AAP-007 | human_confirmation_required | DECLARATIVE ONLY in inspected schema | GAP candidate |
| AAP-008 | max_delegation_depth; linked composition work | PARTIAL / VERIFY | QUALIFY attenuation |
| AAP-009 | provenance/supersedes surfaces + #172 | PARTIAL / VERIFY | QUALIFY continuity |
| AAP-010 | graph composition/authority edges + linked work | PARTIAL / VERIFY | QUALIFY handoff |
| AAP-011 | no generic enforcement established in bounded inspection | UNKNOWN | GAP candidate |
| AAP-012 | no generic replay/effect enforcement established in bounded inspection | UNKNOWN | GAP candidate |
| AAP-013 | evidence manifest + result/lineage contracts | PARTIAL | REUSE/EXTEND |
| AAP-014 | R1 evidence adequacy + terminal semantics | STRONG CANDIDATE | REUSE; verify integration boundary |
| AAP-015 | validity fields + optional temporal profile | PARTIAL | REUSE/EXTEND |

## Next evidence pass
For every PARTIAL, VERIFY, UNKNOWN or GAP candidate row, cite implementation/test paths and run the relevant tests before opening implementation child issues.
