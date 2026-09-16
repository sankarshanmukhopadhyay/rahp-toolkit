# Human-power DPIP specialist reconciliation

This tranche completes the deferred assurance path created by RAHP #161 and #179: Interop Lab observations are interpreted by DPIP for privacy depth, then returned to RAHP for bounded human-power/harm reconciliation.

## Executable governance boundary

```text
Interop Lab
execution observations
     |
     v
DPIP
privacy-depth judgment
     |
     v
RAHP
human-power/harm judgment + terminal bounded disposition
```

No layer may silently inherit another layer's authority.

- **Interop Lab** owns the production of bounded observations and their provenance.
- **DPIP** owns minimisation, observability, linkability/correlation and privacy evidence sufficiency.
- **RAHP** owns coercion/power-asymmetry and consequential-use harm judgment, plus the terminal bounded assurance disposition.

A DPIP `FAIL` is therefore not mechanically a RAHP harm `FAIL`; a DPIP `PASS` is not mechanically a RAHP `PASS`; and a material DPIP `INDETERMINATE` cannot be promoted to RAHP `PASS`.

## Immutable evidence lineage

The checked-in reconciliation fixture pins both producing commits and post-merge evidence artifacts:

- Interop Lab #121/#229 merge: `1c3d3367329313cc0b7eb4a3bc972e221e4bc4d9`
- Interop artifact `human-power-pressure-evidence`: `sha256:df03e239254f786108ba41ba1c84c8d3f57197a480ec22c15587271b90638a07`
- DPIP #190/#191 implementation PR: `#267`
- DPIP evaluator merge: `90a4658e745c0f985e3a7cb8fc9decfb0234c699`
- DPIP post-merge workflow run: `35050504113`
- DPIP artifact `dpip-human-power-privacy`: `sha256:a43297d3f2d30cab39aba3816515b364b0ab16e39a7ee9a1cff5960d29289ec4`

The reconciliation refuses an Interop revision mismatch rather than joining specialist evidence to a different producer epoch. Its machine-readable result also carries the Interop and DPIP artifact digests so later consumers can identify the exact evidence chain rather than relying only on narrative references.

## Reconciliation rules

### RAHP FAIL

A model-level RAHP FAIL remains FAIL because the RAHP harm proposition has independently failed. The DPIP outcome is preserved as supporting, unresolved or non-applicable specialist context; it does not create the RAHP failure.

### RAHP INDETERMINATE

RAHP remains INDETERMINATE. Specialist evidence may explain the remaining uncertainty but cannot supply facts outside the RAHP evaluator's admitted inputs.

### RAHP PASS with material DPIP handoff

- DPIP `PASS` or `NOT_APPLICABLE` permits the bounded reconciliation to PASS.
- DPIP `INDETERMINATE` forces reconciliation to INDETERMINATE.
- DPIP `FAIL` forces reconciliation to INDETERMINATE unless the RAHP model independently establishes the human-power/harm failure. This preserves the distinction between a privacy defect and a coercion/proxy-harm conclusion.

### RAHP PASS without material DPIP handoff

The bounded RAHP proposition may PASS because no unresolved specialist obligation is material to that proposition.

## Current bounded dispositions

### Compelled expanded disclosure

RAHP's existing disclosure-pressure evaluator receives the pressure-case facts: minimal proof available, unnecessary expanded disclosure, refusal not meaningfully available, high-dependency service and denial on refusal. RAHP independently returns `FAIL` for `unnecessary-expanded-disclosure-compelled`.

DPIP #190 independently returns bounded synthetic privacy `FAIL` for excess disclosure and correlation-scope expansion. Reconciliation therefore returns **FAIL**, while retaining `deployment_claim_supported: false` because the evidence epoch is synthetic.

This is a pressure-test failure, not a claim about any named deployment.

### Consequential proxy inference

RAHP's existing proxy evaluator sees consequential `community_membership` use but does not have evidence that it is a sensitive/social proxy. It returns `INDETERMINATE / proxy-effect-unknown` and requires DPIP privacy depth.

DPIP #191 also returns `INDETERMINATE`: consequential extra metadata use is observed, but the mapping to a sensitive/social characteristic and cross-context reuse are not observed. Reconciliation therefore remains **INDETERMINATE** and transports the exact residual evidence requirements.

No discrimination, legitimacy or sensitive-characteristic inference is invented.

## Output contract

Each reconciliation result uses `rahp-human-power-reconciliation/v1` and records:

- proposition and RAHP issue identity;
- RAHP model result;
- DPIP specialist result;
- immutable Interop and DPIP revisions;
- Interop and DPIP evidence artifact lineage where available;
- terminal bounded outcome;
- deployment-claim flag;
- residual evidence requirements;
- explicit authority ownership.

The bundle uses `rahp-human-power-reconciliation-bundle/v1`. Its `portfolio_outcome` is expressly bounded to this human-power tranche and MUST NOT be read as a whole-portfolio RAHP state.

## Reproduction

```bash
python -m unittest discover -s tests -p 'test_human_power_reconciliation.py' -v
python tools/human_power_reconciliation.py \
  --input fixtures/human-power/dpip-reconciliation-input.json \
  --output /tmp/rahp-human-power-reconciliation.json \
  --check
```

The repository-wide `validate` workflow executes the full test suite, runs the bounded reconciliation, and uploads `rahp-human-power-reconciliation`. Reconciliation is intentionally consolidated into that workflow so this capability does not expand RAHP's governed GitHub Actions surface.

## Runtime escalation rule

A new Interop Lab runtime task should be created only when this reconciliation leaves a named observation unresolved **and** a concrete implementation target exists.

For the current proxy proposition the residual contract requires, if a target claim is sought:

1. a target repository and immutable revision;
2. an observer-bound mapping, if any, from trust metadata to the claimed sensitive/social characteristic;
3. cross-context observation of whether the metadata/inference is reusable or linkable;
4. provenance sufficient for DPIP to judge the result;
5. return to the same RAHP proposition rather than creation of a substitute harm proposition.

Until such a target exists, `INDETERMINATE` is the correct completed state rather than an invitation to fabricate a generic deployment experiment.
