# Agent assurance — qualified coverage matrix

Tracking: #970

“Structural” means representable by an existing contract; “executable” means retained deterministic tests exercise the bounded proposition. Neither implies live external enforcement.

| Proposition | Qualified coverage | Evidence state | Disposition |
| --- | --- | --- | --- |
| AAP-001 | #774 scenarios + continuity chain actor fields | EXECUTABLE/SCENARIO | REUSE |
| AAP-002 | authority/delegation contracts + continuity root principal | EXECUTABLE + STRUCTURAL | REUSE |
| AAP-003 | `agent_authority` capability/resource checks | EXECUTABLE | REUSE |
| AAP-004 | `agent_authority` evaluated-time validity | EXECUTABLE | REUSE |
| AAP-005 | active/revoked/suspended/unavailable status behavior | EXECUTABLE; status resolution external | REUSE |
| AAP-006 | exact capability/resource binding | EXECUTABLE | REUSE |
| AAP-007 | required human confirmation satisfied/denied/unavailable | EXECUTABLE | REUSE |
| AAP-008 | continuity capability attenuation + depth bound | EXECUTABLE | REUSE |
| AAP-009 | explicit substitution continuity evidence | EXECUTABLE; cryptographic binding external | REUSE |
| AAP-010 | principal continuity + parent-authority lineage | EXECUTABLE | REUSE |
| AAP-011 | Track-G task/effect boundary | EXPERIMENTAL EXECUTABLE COMPOSITION | REUSE with stated boundary |
| AAP-012 | Track-G duplicate/prior-effect denial | EXPERIMENTAL EXECUTABLE COMPOSITION | REUSE; live exactly-once external |
| AAP-013 | evidence manifest + continuity/redress linkage | STRUCTURAL + EXECUTABLE BOUNDED | REUSE |
| AAP-014 | `evidence_adequacy` missing/unavailable/conflict behavior | EXECUTABLE | REUSE |
| AAP-015 | validity/current status + ARPA historical/current distinction | EXECUTABLE + PINNED DOCUMENTARY | REUSE |

## Coverage rule
A proposition is complete for this downstream experimental profile when its bounded RAHP behavior is deterministic and tested, and any external evidence/enforcement obligation is named. No row above claims cryptographic identity, live registry resolution, Git-provider enforcement, or legal authority.
