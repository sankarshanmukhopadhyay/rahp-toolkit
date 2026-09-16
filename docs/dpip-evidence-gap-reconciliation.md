# DPIP evidence-obligation reconciliation

RAHP consumes DPIP privacy-specialist state without collapsing specialist findings into broader harm or assurance conclusions.

## Inputs

A DPIP evidence obligation contributes four independent facts to reconciliation:

1. materiality of the privacy evidence gap;
2. obligation lifecycle state;
3. evidence-access blocker / assurability state;
4. minimum evidence maturity required for the claim.

These supplement, rather than replace, the RAHP proposition evaluator.

## Reconciliation rules

- A RAHP `FAIL` remains `FAIL`; a DPIP obligation does not replace the RAHP harm/power judgment.
- A RAHP `INDETERMINATE` remains `INDETERMINATE`.
- A RAHP `PASS` with a **material unresolved** DPIP obligation becomes bounded `INDETERMINATE` for the dependent proposition.
- A non-material blocked obligation does not prevent a dependent RAHP `PASS`.
- A material obligation in `SATISFIED`, `FALSIFIED`, or `SUPERSEDED` state no longer blocks the dependent proposition, subject to normal RAHP reevaluation.
- `NO_OBSERVATION_SURFACE`, `NO_INSTRUMENTATION`, and `NON_REPRODUCIBLE` remain explicit `ASSURABILITY_GAP` states.
- `NO_TARGET` means target/deployment behavior is not established. It does not justify creation of synthetic replacement evidence.
- `ACCEPTED_RESIDUAL_RISK` requires named authority and bounded scope; anonymous acceptance is invalid.

## Current #179 / DPIP #191 disposition

The three DPIP #191 obligations are material E3 target-runtime obligations. No target is currently nominated, so each remains `BLOCKED: NO_TARGET`. If the dependent RAHP model were otherwise to pass, these obligations still prevent promotion of the proxy-inference proposition to assurance `PASS`.

This preserves the current bounded state:

- synthetic evidence remains useful for evaluator behavior and controlled proposition pressure;
- no named deployment is accused of sensitive/social proxy inference;
- no target-runtime claim is made;
- the exact evidence needed to change the state is machine-addressable.

## CI and evidence

`tests/test_evidence_obligation_reconciliation.py` is automatically included by the repository's existing `python3 -m unittest discover -s tests -p 'test_*.py'` validation step. No additional GitHub Actions workflow is introduced, preserving the governed workflow budget.

Reproduce directly:

```bash
python3 -m unittest tests/test_evidence_obligation_reconciliation.py -v
python3 tools/evidence_obligation_reconciliation.py \
  --input fixtures/human-power/dpip-191-evidence-obligations.json \
  --rahp-outcome PASS \
  --check
```

A green test proves reconciliation semantics and contract handling only. It does not establish the missing target-runtime facts.
