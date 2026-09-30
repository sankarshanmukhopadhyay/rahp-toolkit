# Full-stack assurance orchestration

This contract was hardened after the LPC pre-demo campaign in RAHP #851.

The lesson from that campaign is that **workflow completion and assurance sufficiency are different claims**. A full-stack campaign may legitimately complete while the subject remains INDETERMINATE, but it must not silently omit a material assurance lens or an applicable evidence probe.

## Three independent run dimensions

A lifecycle may now retain:

- `process_state` — whether orchestration is still running, complete, or errored;
- `assurance_state` — what the available evidence supports;
- `evidence_maturity` — the strongest evidence class actually acquired.

For example, the #851 shape is valid as:

```yaml
process_state: complete
assurance_state: indeterminate
evidence_maturity: source-only
```

It is not equivalent to PASS.

## Lens disposition ledger

Full-stack subjects use explicit records for:

- RAHP;
- security;
- composition;
- DRARM;
- specialist assessment.

Each lens records materiality, execution state, result, evidence maturity, rationale and provenance where required.

A material lens may end as `required-but-not-executed / INDETERMINATE` when the target or evidence producer does not yet exist. Silence is not a disposition.

Security-shaped RAHP tests do not by themselves count as an executed security assessment. Component PASS does not count as composition PASS.

## Evidence attempt discipline

When the campaign declares required evidence, it reuses the existing `rahp-evidence-probe-ledger/v1` contract.

Every required evidence item must have one attributable attempt classification:

- `EXECUTED`;
- `ATTEMPTED_UNAVAILABLE`;
- `NO_APPLICABLE_PRODUCER`.

An omitted probe is an orchestration defect. `NOT_EVIDENCED` is valid only with attributable attempt/no-producer state.

## DRARM

Campaign/manual paths use the same resilience applicability semantics as normal controller paths.

DRARM silence is invalid. A campaign records one of:

- executed;
- not applicable, with provenance;
- required but not executed.

Where resilience is material, the lens can also retain achieved and required DR-A depth so source/static review is not confused with induced-failure or fleet/adversarial evidence.

## Composition and version skew

Multi-component migrations may be described as producer → contract → consumer semantics with old/new versions.

The portable compatibility helper derives four combinations:

- old producer → old consumer;
- new producer → new consumer;
- old producer → new consumer;
- new producer → old consumer.

Mixed-version behavior must be declared as compatible, explicit refusal, or unspecified. Unspecified behavior remains INDETERMINATE/model-gap. Semantic mismatch creates a review proposition, never an automatic defect finding.

This mechanism is intentionally domain-neutral. The #851/#870 credential migration is a regression fixture, not logic in the portable core.

## Terminal full-stack rule

A full-stack terminal record is valid only when:

- process, assurance and evidence-maturity dimensions are explicit;
- every configured lens has an explicit disposition;
- N/A/not-material decisions have provenance;
- applicable unexecuted lenses remain INDETERMINATE rather than PASS;
- a full-stack PASS is supported by PASS from every applicable lens;
- every declared required evidence item has an attributable probe attempt.

The purpose is not to force green outcomes. It is to make bounded uncertainty explicit and machine-verifiable.
