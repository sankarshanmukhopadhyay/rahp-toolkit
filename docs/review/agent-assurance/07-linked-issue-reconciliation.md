# Agent assurance I1 — linked issue reconciliation

Tracking: #970

## Purpose
Distinguish prior research propositions from executable evidence so that agent assurance reuses real assets without overclaiming coverage.

| Issue | Prior contribution | Verified artifact/status | AAP relevance | I1 disposition |
| --- | --- | --- | --- | --- |
| #884 | Tests domain-independent RAHP-core hypothesis using fiduciary-agent assurance | Closed research/architecture issue; establishes hypothesis and classification questions, not by itself runtime coverage | all | REFERENCE; do not treat as implementation evidence |
| #172 | Effective-actor substitution | Closed/deferred; explicitly requested no implementation | AAP-001, AAP-009 | PROPOSITION SOURCE; implementation gap remains to verify |
| #165 | Delegation laundering / hidden principals | Closed/deferred; explicitly requested no implementation | AAP-002, AAP-008, AAP-010 | PROPOSITION SOURCE; enrich principal/beneficiary/accountability analysis |
| #177 | Confused-deputy context binding | Closed/deferred; explicitly requested no implementation | AAP-003, AAP-006, AAP-010, AAP-011 | PROPOSITION SOURCE; preserve principal/resource/purpose/context binding |
| #186 | Delegated authority lineage across composition | Closed pre-specification evidence candidate; calls for revoked/expired/scope-exceeded/redelegated fixtures | AAP-004, AAP-005, AAP-008, AAP-010 | REQUIREMENT SOURCE; executable coverage not established by issue |
| #189 | Meaningful principal authorization | Closed pre-specification evidence candidate; requires positive/negative authorization fixtures | AAP-006, AAP-007 | REQUIREMENT SOURCE; distinguish protocol completion from authorization evidence |
| #379 | End-to-end actuation invariant | Closed convergence work item defining consequential-action and replay vectors | AAP-006, AAP-011, AAP-012, AAP-014 | STRONG REUSE CANDIDATE; locate retained execution artifacts before new evaluator work |
| #774 | Agent Names × Trust Tasks pressure test | Closed complete assessment; retained pressure-test YAML and composed corpus verified on current main | AAP-001, AAP-005, AAP-008, AAP-009, AAP-010, AAP-014 | REUSE scenario baseline; not implementation conformance |

## Verified current-main reusable artifacts

### Agent Names × Trust Tasks
- `examples/cross-spec/agent-names--trust-tasks/pressure-test.yaml`
- `corpora/agent-names-trust-tasks-composed.yaml`

These retain scenarios for:
- name-to-authority substitution;
- controller drift while a task remains executable;
- principal/agent role confusion across delegation hops;
- cross-context correlation/reuse.

The assessment explicitly states that these are scenario-baseline findings requiring maintainer/WG disposition, not upstream defects or implementation conformance.

### Evidence adequacy
- `tools/evidence_adequacy.py`
- `tests/test_evidence_adequacy.py`

The tests cover PASS, FAIL, missing evidence, unavailable evidence, mixed negative+missing, conflicts, scope mismatch, malformed inputs, duplicate/unknown evidence and order invariance. Missing/unavailable/conflicting/out-of-scope evidence is therefore an executable reuse candidate for AAP-014, while terminal controller integration remains a separate boundary.

## Consequence for #970
Do not create new implementations merely because #165/#172/#177/#186/#189 are closed. Their closure does not mean their propositions were implemented. Conversely, do not rebuild the #774 scenario corpus or R1 evidence-adequacy behavior.

The next verification target is #379's retained actuation/replay implementation evidence, followed by authority/delegation schema validation paths and tests.
