# Credential renewal authority assurance example

This maintained regression example demonstrates lifecycle-continuation assurance for automated renewal, successor creation and relationship endings. It is intentionally protocol-neutral. It does **not** define a credential-renewal protocol, wallet interaction model, HTX requirement, or upstream DTG lifecycle semantics.

## Assurance proposition

Renewal, reissuance or successor creation that extends consequential state is an authority boundary when continuation requires a current decision. Unchanged claims, possession of the prior credential, successful reissuance, an existing automation preference, expiry, or a missing response are not sufficient evidence of current authority or of a particular relationship-ending semantic.

The example reuses existing portable harms, risks, controls, guardrails and assurance patterns. No renewal-specific portable risk is introduced merely to mirror the labels used in the motivating discussion.

## Coverage reconciliation

The example now covers five additional hypotheses tracked by #1106:

1. **Dormant or zombie continuation:** existing `ATP-AUTH-03`, `RKP-AUTH-02`, `GRP-AUTH-02` already cover continuation without current authority.
2. **Coerced or concealed endings:** existing autonomy harms (`HRM-AUT-02`, `HRM-AUT-03`, `HRM-AUT-05`) cover the human consequence; the fixture distinguishes technical closure from evidence that the choice was voluntary.
3. **Demand-driven intent leakage:** `RKP-PRV-06`, `RKP-COMP-03`, `GRP-PRV-02` and `ATP-PRV-01` cover privacy leakage from lifecycle/status activity and composed metadata.
4. **Disproportionate assurance demand:** `RKP-EXC-02`, `HRM-ACC-02` and `CTP-EXC-01` cover burden and alternative-path questions. The case records the control-induced trade-off and links the general method question to #1089.
5. **Lapse versus closure/withdrawal:** `RKP-COMP-02`, `CTP-COMP-02` and `GRP-COMP-02` cover conflicting lifecycle semantics. Expiry without holder-closure or issuer-withdrawal evidence remains `INDETERMINATE`.

## Cases

`cases.yaml` retains the four original continuation cases and adds:

- `CRA-005`: expiry is not automatically deliberate closure or issuer withdrawal;
- `CRA-006`: a closure request stops continuation but contradictory coercion evidence prevents a claim that the ending was freely chosen;
- `CRA-007`: third-party-demanded/use-triggered renewal remains non-PASS when timing/relationship privacy evidence is missing;
- `CRA-008`: assurance uplift remains non-PASS when proportionality and alternative-path evidence are missing, and explicitly records burden transfer for #1089;
- `CRA-009`: a positive boundary contrast in which an authorized supporter assists through an accessible process with positive voluntariness evidence.

Historical evidence is preserved in every case. Preservation means an older object may remain usable to resolve a historical statement. It does not establish current authority, successor applicability, closure semantics, or present consent.

## Reproduce

From the repository root:

```bash
python3 -m pytest tests/test_credential_renewal_authority.py -q
python3 tools/validate_catalogue.py
python3 tools/validate_v04_method.py
python3 tools/validate.py
```

The unit test verifies existing-pattern reuse, lifecycle-state separation, privacy evidence behavior, coercion/accessibility boundaries, control-induced burden visibility, and non-promotion of missing evidence to `ALLOW`.

## Authority boundary and limitations

This example is downstream RAHP assurance evidence. HTX owns human-experience recommendations; Trust Tasks and credential profiles own lifecycle/successor semantics; upstream `trustoverip/dtgwg-rahp-tf` retains authority over its corpus. The fixture does not promote exploratory discussion text into adopted conformance rules.

A supporter or representative is not treated as authorized merely because a prompt or assistance path exists. `CRA-009` requires positive representative authorization plus accessible participation and voluntariness evidence.

A PASS in this example establishes only the tested assurance proposition. It does not establish deployed harm, legal validity, production readiness, universal renewal policy, or upstream adoption.

## Provenance

The original lifecycle-continuation example was triggered by downstream analysis of HTX Discussion #22 and tracked in #1031. The expanded reconciliation is tracked in #1106, with general control-consequence method work deliberately delegated to #1089 rather than duplicated here.
