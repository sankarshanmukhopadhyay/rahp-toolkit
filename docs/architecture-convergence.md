# RAHP–DPIP–Interop architecture convergence

Tracking: [RAHP #501](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/501)

The graduation review converges the portfolio onto three stable responsibility boundaries:

```text
RAHP        = assurance control plane
DPIP        = specialist privacy assessor / privacy semantics owner
Interop Lab = executable evidence plane / target-specific pressure-test environment
```

The result is not a monorepo and not a minimum-workflow target. It is a contract-and-ownership architecture in which new propositions normally extend data, profiles, cases, producers or specialist semantics rather than create another end-to-end assurance controller.

The machine-readable disposition and ownership record is [`architecture/convergence-matrix.yaml`](../architecture/convergence-matrix.yaml).

## Steady-state flow

```text
normative / implementation / deployment change
        ↓
RAHP normalization + materiality + routing
        ↓
RAHP assurance obligation
        ↓
ordinary RAHP assessment ───────────────┐
        │                                │
        └─ privacy-specialist route → DPIP intake/examination
                                      │
                                      ├─ evidence sufficient → DPIP interpretation
                                      │
                                      └─ evidence required → registered producer / Interop Lab case
                                                              ↓
                                                   source-pinned raw evidence
                                                              ↓
                                                   RAHP producer-result contract
                                                              ↓
                                                        DPIP interpretation
                                                              ↓
                                                   RAHP assessor-result contract
                                                              ↓
RAHP terminal reconciliation ←───────────────────────────────┘
        ↓
PASS / FAIL / INDETERMINATE / NOT_APPLICABLE and portfolio posture
```

A specialist may complete successfully while RAHP remains `INDETERMINATE`. A producer workflow may be green while the required evidence remains incomplete. These are features of the assurance model, not orchestration defects.

## Stable primitive ownership

### RAHP owns the control plane

RAHP is authoritative for:

- assessment/controller identity;
- normalized findings and materiality;
- routing and specialist referral;
- assurance obligations and evidence requirements;
- the portable executable-evidence producer result contract;
- the portable specialist assessor-result contract;
- generic assurance-pattern meaning;
- evidence provenance, freshness and invalidation;
- final reconciliation and terminal assurance state.

The clean-room executor remains the isolated reference path for citable terminal results. DTG-specific Portfolio Monitor ingestion and repository review remain instance adapters: they may know DTG source vocabulary, but they do not define generic RAHP assurance meaning.

The RAHP↔DPIP lifecycle reconciler is the canonical specialist lifecycle boundary. Dedicated compatibility/instance trigger workflows may remain while they have live event consumers, but they must not become alternate state machines.

## DPIP owns privacy semantics

DPIP remains authoritative for:

- admission of privacy examination requests after RAHP routing;
- observer/threat-model semantics;
- A/B and comparison experiment meaning;
- privacy-specific causal interpretation;
- privacy-specific PASS/FAIL/CONSTRAINED/INDETERMINATE/NOT_APPLICABLE dispositions;
- the reusable observability model graduated through DPIP #221;
- durable specialist return delivery.

Its staged intake → setup → execute → evidence plan/acquire → return workflows are lifecycle transitions with retry/recovery behavior. They are not separate assurance authorities. Workflow success does not equal privacy PASS, and successful return delivery does not equal RAHP GREEN.

DPIP consumes RAHP's generic producer/provenance and assessor-result contracts rather than owning competing generic envelope definitions.

## Interop Lab owns target execution

The Interop Lab owns:

- source-pinned target execution;
- target adapters;
- experimental and graduated case fixtures;
- adversarial vectors;
- raw observations and execution artifacts;
- characterization/equivalence evidence for reusable runners.

The first completed workflow convergence proves the intended model. The current OpenVTC Track A, Track B status and Track B task evidence producers now share one characterized reusable workflow and common runner. Track B policy did **not** get forced into the same abstraction because characterization demonstrated a materially deeper DPIP→RAHP specialist integration chain.

The complete per-workflow disposition and admission rule live in Interop Lab #188 / `docs/workflow-rationalisation.md`.

## What graduated during this tranche

Four coordinated capabilities now establish the stable seams:

- **RAHP #490** — target-neutral executable-evidence producer/result contract;
- **DPIP #221** — implementation-neutral privacy observability/evaluation semantics;
- **RAHP #491** — disciplined promotion of mature target-neutral assurance concepts into the generic catalogue;
- **RAHP #506** — singular authoritative `rahp-assessor-result/v1` contract after a real DPIP↔RAHP integration exposed schema drift.

These are implementation boundaries, not merely documentation conventions. They have executable tests and current consumers.

## Convergence decisions

The audit uses five classifications:

- `KEEP` — the mechanism represents a distinct responsibility or lifecycle boundary;
- `CONSOLIDATE` — equivalent repeated mechanics have been moved behind shared machinery;
- `GENERALISE` — repeated semantics became a stable reusable contract or pattern;
- `RETIRE` — safe supersession is evidenced;
- `DEFER` — a compatibility, runtime, history or semantic boundary prevents safe convergence now.

A `DEFER` finding is not unfinished architecture when the reason is positive and explicit. For example, a historical source-pinned regression workflow, an external adversarial harness with digest verification, or a privileged release workflow should not be folded into generic evidence orchestration simply to reduce YAML count.

No additional retirement was forced where active-consumer or historical-reproducibility evidence was insufficient.

## Extension rule

A new assurance proposition should normally require some combination of:

1. a RAHP proposition/profile mapping or assurance obligation;
2. a DPIP privacy pattern/experiment only when privacy-specialist semantics are required;
3. a declarative Interop case/fixture/assertion set when execution is needed;
4. a registered producer using the portable RAHP evidence result;
5. a specialist result returned through the authoritative RAHP assessor contract.

A new bespoke Lab workflow is justified only when a materially distinct runtime/security boundary, external dependency lifecycle, privilege/secrets requirement, failure semantic, evidence collection mechanism, or reproducibility/claim-boundary isolation requirement cannot safely fit existing reusable machinery.

## Non-inference rules

The graduated architecture preserves these boundaries:

- workflow green != assurance green;
- missing evidence != PASS;
- producer success != specialist PASS;
- specialist PASS != terminal assurance PASS;
- local execution evidence != deployment-wide evidence;
- historical source-pinned evidence != current assurance after material invalidation;
- candidate proof construction != normative interoperability;
- target-specific behavior != generic assurance semantics.

## Graduation conclusion

The stack is now organized around stable primitives rather than repository accidents:

```text
RAHP controls assurance meaning and state
        ↓
DPIP specializes privacy meaning when routed
        ↓
Interop executes bounded target evidence when required
        ↓
portable evidence / specialist contracts return facts upward
        ↓
RAHP reconciles terminal assurance
```

This architecture leaves room for more producers, specialists and ecosystem profiles without requiring another assurance architecture for each one. That is the maturity claim established by #501.
