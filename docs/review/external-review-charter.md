# External Review Charter

## Objective

Independently challenge whether RAHP implements the bounded assurance behavior it claims, including whether incomplete, stale, contradictory, non-independent, malformed or adversarial evidence can cause a stronger conclusion than warranted.

The review covers both ordinary software quality and assurance fidelity.

## In scope

- correctness and maintainability;
- security of RAHP itself;
- evidence/provenance handling;
- controller and reconciliation behavior;
- composition inference;
- specialist boundaries;
- source pins and historical assessment preservation;
- reproducibility;
- CI and supply-chain controls;
- bounded completeness and documentation accuracy.

## Non-goals

The review is not expected to prove universal safety, universal completeness, correctness of every external authority, or correctness of specialist systems outside the evidence/contracts RAHP consumes.

## Claims are open to challenge

Reviewers are explicitly invited to falsify material claims, modify fixtures, substitute evidence, replay stale evidence, break provenance, provide malformed inputs, challenge independence assumptions, and attempt to obtain terminal PASS/GREEN without sufficient evidence.

## Independence

Reviewers should not treat repository documentation, existing PASS states, release qualification records, or maintainer intent as proof. They are inputs to be tested against executable and attributable evidence.

## Finding classes

- A — implementation defect
- B — security defect
- C — assurance-model defect
- D — evidence/provenance defect
- E — claim/documentation defect
- F — maintainability/operability defect
- G — reproducibility defect

## Evidence expectations

A material finding should identify the proposition affected, reproducible input or condition where practical, observed behavior, expected bounded behavior, affected evidence or implementation surface, and residual uncertainty.

A material positive conclusion should identify the evidence actually examined and its scope. Absence of a finding is not evidence of universal correctness.

## Reproducibility

Review findings should be reproducible against a source-pinned RAHP revision and declared inputs/environment where practical. Network-dependent and externally mutable evidence must be identified as such.

## Security scope

RAHP is treated as software exposed to untrusted repositories, malformed structured data, adversarial schemas/evidence, stale or misleading metadata, hostile dependency graphs and resource-exhaustion inputs.

The central security/assurance question is whether hostile input can alter execution or produce unjustifiably strong assurance.

## Assurance-model scope

Review should specifically test non-equivalences including:

```text
workflow success != assurance success
identity != authority
discovery != recognition
recognition != authorization
component validity != composition validity
protocol completion != semantic completion
multiplicity != independence
```

Unknown, unavailable and indeterminate evidence must remain distinguishable from positive establishment.

## Unresolved findings

Material findings are not to be hidden or closed for presentation quality. They should become bounded issue/PR work or explicit residual risk with owner, evidence state and retest trigger.

## Candidate qualification

A review candidate is qualified only when the reviewer pack, claim ledger, architecture/trust-boundary guide, threat model, challenge evidence, reproducibility evidence, semantic coverage matrix and known-limitations register are present and required CI is green.
