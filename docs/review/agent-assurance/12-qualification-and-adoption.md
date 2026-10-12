# Agentic Assurance Profile — qualification and adoption

Tracking: #970

## Profile status
Version: **AAP v1 experimental downstream profile**

AAP reuses RAHP's existing finite outcomes and evidence-conservative posture. It adds two optional deterministic controls:
- `tools/agent_authority.py`: bounded action-authority evaluation;
- `tools/agent_continuity.py`: handoff, substitution and redress continuity evaluation.

Neither control is a terminal assurance engine or runtime permission service.

## Coverage disposition

| Dimension | Qualification |
| --- | --- |
| Identity/provenance | structural + scenario coverage; cryptographic identity remains external evidence |
| Authority/delegation | executable bounded evaluator |
| Action authorization | executable capability/resource/current-state/confirmation checks |
| Execution boundaries | Track-G reusable experimental evidence; live tool enforcement external |
| Evidence/accountability | existing evidence-adequacy executable control |
| Lifecycle | validity/revocation plus substitution continuity; external status resolution remains external |
| Multi-agent composition | executable principal/lineage/capability attenuation checks |
| Intervention/redress | executable evidence-completeness check; substantive appeal correctness remains governance-owned |

## Setup and execution

No new dependency is introduced.

```bash
python -m unittest tests.test_evidence_adequacy tests.test_agent_authority tests.test_agent_continuity
```

Consumers provide already-resolved evidence. Registry, protocol, identity, signature, policy and Git-provider enforcement remain authoritative outside RAHP.

## Interpretation
- **PASS** means every predicate within the bounded control is supported by supplied evidence.
- **FAIL** means supplied evidence demonstrates at least one violated required predicate.
- **INDETERMINATE** means required evidence is missing/unavailable or cannot justify a positive conclusion.

A PASS is never a general declaration that an agent is trustworthy or permitted by every relevant system.

## Remediation
For FAIL, correct the violated authority/scope/lineage/continuity condition and re-examine.
For INDETERMINATE, obtain authoritative current evidence; do not replace absence with inference.
For external enforcement questions, collect execution receipts or provider evidence and assess them separately.

## Residual risks
- supplied identifiers and evidence are not cryptographically authenticated by these controls;
- revocation/current status is consumed, not fetched;
- Track-G actuation evidence is experimental and DTG-specific;
- exactly-once side-effect enforcement remains an implementation responsibility;
- redress control establishes reconstructability, not fairness or legal sufficiency;
- live multi-agent workflow behavior can diverge from declared delegation evidence.

## Portable-core recommendation
Candidate for portable RAHP core:
- generic evidence-adequacy semantics;
- bounded authority non-amplification patterns;
- continuity/lineage predicates that remain domain-neutral.

Remain profile-only:
- agent-specific actor classes and vocabulary;
- Git-operation examples;
- ARPA mapping;
- any model/AI-specific hazard extension.

Upstream convergence should occur only after downstream use demonstrates stable portability. #970 does not itself initiate upstream convergence.

## Human acceptance boundary
The implementation is suitable for downstream experimental qualification. Promotion to normative upstream RAHP semantics, legal interpretation of delegation, or acceptance of an external registry as authoritative requires human/governance decision outside this issue.
