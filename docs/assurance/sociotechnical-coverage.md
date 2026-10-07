# Sociotechnical assurance coverage at commencement

Owner: #913. Inspected development baseline: `b5d1381b8ef747ce78c5a5d9cf66b57bb79b41ff`.
Stable baseline: `v2.6.0` / `b18dc9b0acfc8dad36ef9f5b4a5030de38e683f1`.
Engine: `rahp-engine-contract-v1`, revision 1.3; normalized result schema: 1.

The compared changes since the stable tag concern issue forms, queue evidence and DTG routing/publication. The method/evaluators/renderer cited below have identical content at both pins. This table describes inspected coverage, not the absence of every possible implementation elsewhere.

| Invariant | Existing authority / implementation / evidence | Initial classification | Tranche action |
|---|---|---|---|
| Harm despite technical success | `docs/how-rahp-works.md`; `tools/human_choice_invariants.py`; `tests/test_wave4_human_choice_invariants.py` | implemented-and-tested for compelled disclosure and meaningful choice | Reuse these evaluators; bind admitted facts to evidence and frame |
| Benefits versus transferred burdens | `method/schema/assurance-graph.schema.json`; harm traceability in `tools/assurance_record.py` | partially evidenced: flexible graph/trace, no bounded framing gate in inspected renderer | Explicit opt-in profile frame, actors, burdens, coverage limits |
| Contradiction cannot become success | `method/schema/assurance-evaluation.schema.json`; `tools/assurance.py::infer_residual`; `tests/test_assurance_evaluation.py` | implemented inference; profile-specific evidence admissibility remains unqualified | Keep refutation and evidence-class/context sufficiency visible |
| Source count does not prove independence | `tools/actor_dependency_invariants.py::evaluate_external_trust_sources`; `tests/test_wave2_actor_dependency_invariants.py` | defective independence claim: two checked sources suffice without independence metadata | New profile gates with attributable dependence review; clarify legacy evaluator boundary without silently changing its contract |
| Context-only change invalidates inherited conclusions | `tools/assurance_fsm.py::stable_assessment_id`; `tools/assurance_state.py`; `tests/test_evidence_freshness_delta.py` | partially evidenced: pins support generic invalidation, context observation/representation is caller-owned | Include context digest in assessment identity and evidence admission; record changed context and lineage |
| Technical repair differs from human remedy | `method/schema/remediation-manifest.schema.json`; `tools/authority.py`; #610 | partially evidenced: generic remediation ownership, deployment contestability external | Typed profile obligations, contested dispositions and challenge route; closure does not remove obligations |
| Maintained summaries preserve qualifications | `schemas/rahp-assurance-run-state-v1.schema.json`; `tools/assurance_record.py::canonical_record` | defective: canonical allowlist drops process/assurance/evidence-maturity dimensions and lenses | Preserve current run-state facts plus profile evidence; reject profile-result tampering |
| Independent review is attributable | `docs/ai-assisted-process.md`; #668 independent reviewer protocol | documented; this tranche has no independent human review | Cold-reader packet and explicit pending review, never synthetic participation |

## Compatibility judgment before implementation

Use an additive, opt-in profile on the existing extensible assurance-run envelope. Keep normalized result v1 and engine contract revision unchanged. Existing callers remain valid. The new profile will reject unsupported positive claims only when explicitly selected. It evaluates reviewed assertions; it does not extract policy, discover external institutional changes or certify fairness. The profile's schema and bounded qualification apply to this candidate until separately accepted; the stable tag remains immutable.

The legacy external-source helper can establish checked-source multiplicity; this tranche must not claim it establishes sociotechnical independence. Changing its historical outcome contract is deliberately avoided. The opt-in profile must enforce the stronger property and document that boundary.

## Predetermined corpus

`examples/sociotechnical-assurance/corpus.json` pins eight inputs and expected outcomes before implementation. These are synthetic model assertions. A/B exercise existing choice evaluators, C tests correlation and contradiction, D context-only change, E repair without remedy, F presentation/disagreement, P a supported bounded positive control, N a justified non-applicability case. Expected failures are successful falsification fixtures, not claims about real deployments.
