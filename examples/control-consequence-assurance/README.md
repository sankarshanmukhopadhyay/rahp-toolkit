# Control consequence assurance example

This protocol-neutral example exercises the existing RAHP control-side-effect mechanism across materially different control classes. It does **not** add a risk-balancing algorithm, renewal policy, or a requirement that every possible control consequence become a portable catalogue record.

## Existing method support

RAHP already provides:

- `CTP-RISK-01` — Control side-effect assessment;
- `ATP-RISK-01` — Control side-effect test;
- `EVP-RISK-01` — evidence for risks mitigated, introduced/amplified, affected groups and disposition;
- `introduces_or_amplifies_risks` on portable control patterns;
- the stable glossary term `Control side effect`;
- catalogue validation for side-effect risk references and evidence.

`CTP-ID-03` is an existing machine-readable example: uniqueness assurance can introduce or amplify `RKP-EXC-02` and `RKP-PRV-01`.

## Cases

The fixture pressure-tests five controls:

1. renewal/action-time authority evaluation, using #1106 `CRA-008` as motivating evidence;
2. explicit uniqueness assurance;
3. contestability/audit evidence retention;
4. revocation propagation;
5. a principal intent checkpoint with deliberately insufficient side-effect evidence.

Each case records the target benefit, affected actors, exposure changes, existing risk mappings, disposition and control credit. The negative case stays `INDETERMINATE` and withholds credit rather than treating an unassessed consequence as absent.

## Dispositions

The example uses the four #1089 dispositions:

- `existing_coverage` — an existing portable risk/harm/control relationship captures the consequence;
- `context_dependent_residual` — keep the trade-off visible in the assessment rather than creating a new risk;
- `candidate_distinct_reusable_risk` — reserve for evidence that current portable coverage is insufficient;
- `insufficient_evidence` — preserve an indeterminate outcome and do not silently grant control credit.

No case in this fixture currently establishes a `candidate_distinct_reusable_risk`.

## Reproduce

```bash
python3 -m pytest tests/test_control_consequence_assurance.py -q
python3 tools/validate_catalogue.py
python3 tools/validate_v04_method.py
python3 tools/validate.py
python3 tools/build.py
python3 tools/validate_reference_links.py
```

## Authority and limits

A control consequence is a review proposition, not automatically an observed harm. Control ownership and residual-risk acceptance remain with the relevant deployment or governance authority. Portable catalogue fields should represent reusable/intrinsic side-effect relationships; context-dependent effects can remain in assessment evidence rather than polluting every control record with speculative risks.
