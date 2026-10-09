# Agent assurance I1 — evidence ledger

Tracking: #970

| Evidence ID | Source | Supports | State | Notes |
| --- | --- | --- | --- | --- |
| AAP-EV-001 | `method/engine-contract.yaml` | generic lifecycle, finite specialist outcomes, evidence-conservative invariants | VERIFIED DOCUMENTARY/MACHINE CONTRACT | stable revision 1.3 |
| AAP-EV-002 | `method/schema/authority.schema.json` | AAP-002/003/004/005/006 | VERIFIED STRUCTURAL | does not itself prove runtime authorization |
| AAP-EV-003 | `method/schema/delegation-scope.schema.json` | AAP-001/002/003/004/005/007/008 | VERIFIED STRUCTURAL | v0.4; confirmation/depth are declarations until enforcement is evidenced |
| AAP-EV-004 | `method/schema/evidence-manifest.schema.json` | AAP-013/014 | VERIFIED STRUCTURAL | source, producer, time, integrity, authority and supports |
| AAP-EV-005 | `method/schema/assurance-graph.schema.json` | AAP-008/010/013 | VERIFIED STRUCTURAL | typed authorizes/supports/composes edges |
| AAP-EV-006 | `tests/test_evidence_adequacy.py` | AAP-014 | VERIFIED EXECUTABLE TEST | negative and indeterminate evidence states tested |
| AAP-EV-007 | `examples/cross-spec/agent-names--trust-tasks/pressure-test.yaml` | AAP-001/005/008/009/010/014 | VERIFIED RETAINED ASSESSMENT | scenario-baseline, not conformance |
| AAP-EV-008 | `corpora/agent-names-trust-tasks-composed.yaml` | AAP-001/009/010 | VERIFIED SCENARIO CORPUS | four reusable composition scenarios |
| AAP-EV-009 | issues #165/#172/#177 | identity/authority threat propositions | VERIFIED RESEARCH SOURCE | explicitly deferred/no implementation requested |
| AAP-EV-010 | issues #186/#189 | composition/meaningful authorization requirements | VERIFIED PRE-SPEC SOURCE | calls for executable fixtures; not itself evidence of them |
| AAP-EV-011 | issue #379 | actuation/replay requirements | VERIFIED REQUIREMENT SOURCE | retained executable artifacts still to locate |

## Evidence-state vocabulary
- **VERIFIED EXECUTABLE TEST:** implementation behavior is exercised by retained tests.
- **VERIFIED STRUCTURAL:** machine-readable contract can represent the concept; enforcement is not implied.
- **VERIFIED RETAINED ASSESSMENT:** a durable RAHP assessment artifact exists.
- **VERIFIED SCENARIO CORPUS:** reusable scenario input exists.
- **VERIFIED RESEARCH/REQUIREMENT SOURCE:** proposition/rationale exists but does not prove implementation.
- **UNVERIFIED:** no adequate retained evidence located yet.
