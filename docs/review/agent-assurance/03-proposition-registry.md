# Agent Assurance Proposition Registry

Tracking: #970

Status: I1 candidate registry. IDs are stable within this workstream; proposition wording may be refined before profile qualification.

| ID | Proposition | Primary evidence need | Mode |
| --- | --- | --- | --- |
| AAP-001 | The acting agent/effective actor is identified without conflating it with its principal. | identity/provenance binding | design + implementation |
| AAP-002 | The principal on whose behalf the action occurs is explicit and independently attributable. | principal/authority evidence | design + execution |
| AAP-003 | Delegated authority is bounded to explicit capabilities and resources. | delegation scope | design + implementation |
| AAP-004 | Delegated authority is valid at the evaluated action time. | validity + time evidence | execution |
| AAP-005 | Revoked, suspended or expired authority cannot support an authorized-action conclusion. | authoritative status evidence | implementation + execution |
| AAP-006 | The specific consequential action is authorized; broader capability or registration is insufficient. | action/resource authorization | execution |
| AAP-007 | Required human confirmation is evidenced as performed, not merely declared. | confirmation record | implementation + execution |
| AAP-008 | Delegation composition does not amplify scope or exceed permitted depth. | chain + attenuation evidence | design + execution |
| AAP-009 | Agent substitution/replacement preserves authority only with valid continuity evidence. | lineage/rebinding evidence | execution |
| AAP-010 | Multi-agent handoff preserves the originating principal and bounded authority context. | handoff lineage | execution |
| AAP-011 | Tool/API execution remains within authorized task, resource and effect boundaries. | execution trace + effect evidence | implementation + execution |
| AAP-012 | Retry/replay cannot silently duplicate a consequential effect. | idempotency/replay evidence | implementation + execution |
| AAP-013 | A consequential action has reconstructable evidence linking authority, decision, execution and effect. | evidence manifest/trace | execution |
| AAP-014 | Missing, stale, conflicting or inaccessible authority evidence cannot produce PASS. | adequacy/freshness evidence | all |
| AAP-015 | Historical authority state is distinguished from current authority state at the evaluated time. | temporal provenance | design + execution |

## Traceability rule
No new agent-assurance evaluator or profile field should be introduced without a proposition ID and a coverage-matrix gap. Existing generic machinery should be reused where it satisfies the proposition.
