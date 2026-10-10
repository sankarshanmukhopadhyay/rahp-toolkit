# Observability-induced harm: bounded experimental examination

Tracking: [RAHP #981](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/981) · [DTFC #105](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/105).

## Reconciliation

- RAHP #802 already distinguishes operational telemetry from assurance evidence; the existing privacy/correlation obligations remain authoritative for their own scope.
- DTFC DTF-032 covers proof-metadata correlation; DTF-033 covers status-query observability; DTF-036 covers aggregation; DTF-037 covers retained evidence as a correlation surface. Cross-context *operational trace identifiers* are a specific manifestation, not automatically a new taxonomy class.
- Missing-evidence cases DTF-010–012 and workflow/assurance substitution DTF-027 cover related evidence failures. Promotion of a telemetry anomaly into a consequential decision is the specific seam examined here.
- No new canonical risk or case ID is allocated without a demonstrated gap.

## Experimental contract

`tools/observability_harm.py` is an optional synthetic falsification helper, **not** an RAHP controller, privacy assessor, policy decision point, or certification mechanism.

1. A trace identifier reused across distinct declared contexts produces `FAIL / cross-context-trace-correlation` when cross-context correlation is prohibited.
2. An event claiming a consequential action sourced solely from telemetry produces `FAIL / telemetry-promoted-to-authority`.
3. Missing, malformed-in-semantics, or unavailable observations yield `INDETERMINATE`; absence of an observed failure also yields `INDETERMINATE`, never PASS.
4. Malformed event structures are rejected.

The helper assumes input event fields are synthetic, non-sensitive assertions. It does not prove whether identifiers are pseudonymous, whether real-world subjects can be correlated, or whether the decision source was truthfully reported. Real assessments need independent access-policy, collection, correlation, processor, retention, backup, deletion, and downstream decision evidence. Raw credentials, verifier transcripts, tokens, and real relationship identifiers must not be put in fixtures.

## Reproduction

`python -m unittest discover -s tests -p 'test_observability_harm.py' -v`

## Assurance boundary

This is **negative-test evidence for an illustrative contract**, not independent deployment evidence. It does not modify stable RAHP states, DTFC schema, or governance authority. A clean synthetic run does not justify a positive privacy or safety claim.
