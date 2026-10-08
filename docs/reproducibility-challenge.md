---
layout: default
title: "Reproducibility and challenges"
parent: Learn RAHP
nav_order: 8
has_toc: true
permalink: /docs/reproducibility-challenge/
---
# Reproducibility, disagreement and challenge (experimental R3)

Tracking: [#935](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/935).

The optional [R3 evaluator](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/reproducibility_challenge.py) compares **two declared assessment run records** and preserves explicit challenges. It neither reruns the evaluator nor authenticates the declared source inputs. A match is **not proof of independent execution**, evidence correctness, or an authoritative assurance determination.

## Contract

The `rahp-reproducibility-challenge/v1` input requires a nonempty `proposition_id`, exactly two `runs`, and a `challenges` array (which may be empty). Each run has a unique `id`, `evaluator_id`, `evaluator_version`, `outcome` (`PASS`, `FAIL`, `INDETERMINATE`) and an `input_pin` containing `algorithm: sha256` and a lowercase 64-character hex `digest`.

The digest is a **declared pin**; this module does not independently fetch or hash the referenced inputs. A run's `record_digest` is calculated from its normalized declared record for stable comparison and audit correlation, not as a signature.

| Comparison | Disposition |
| --- | --- |
| Input pins differ | `DIFFERENT_INPUT` |
| Input pins match but evaluator ID/version differs | `DIFFERENT_EVALUATOR` |
| Same input and evaluator, different outcomes | `OUTPUT_DISAGREEMENT` |
| Same input, evaluator and outcome | `DECLARED_MATCH` |

The comparisons are applied in table order; a difference in inputs takes precedence over a difference in outcomes. The evaluator does not treat different inputs as an output disagreement.

Each challenge must declare a unique `id`, referenced `run_id`, a `reason` (`EVIDENCE`, `METHOD`, `SCOPE`, `TEMPORAL`, or `OTHER`), and at least one unique nonempty `evidence_refs` identifier. Every challenge remains `OPEN`; resolution and appeals belong to an external governed process. Challenges do not silently reverse an earlier outcome.

## Executable example

```python
from tools.reproducibility_challenge import compare

run = {
    "evaluator_id": "example-evaluator",
    "evaluator_version": "1.0",
    "input_pin": {"algorithm": "sha256", "digest": "a" * 64},
    "outcome": "PASS",
}
profile = {
    "schema": "rahp-reproducibility-challenge/v1",
    "proposition_id": "P-001",
    "runs": [dict(run, id="RUN-A"), dict(run, id="RUN-B")],
    "challenges": [{
        "id": "CH-1", "run_id": "RUN-A", "reason": "EVIDENCE",
        "evidence_refs": ["E-1"]
    }]
}
print(compare(profile))
```

## Reviewer procedure and validation

1. Independently retrieve and hash the actual pinned input before claiming input equivalence.
2. Confirm evaluator implementation identity, version, configuration and execution independence outside this profile.
3. Compare the declared records using R3 and inspect all differences and open challenges.
4. Record evidence and resolve challenges through an explicitly authorized process, preserving the original record.

```bash
python3 -m unittest tests.test_reproducibility_challenge -v
python3 -m unittest tests.test_evidence_adequacy tests.test_temporal_provenance tests.test_reasoning_trace -v
python3 tools/evidence_assertion_assessor.py --self-test
```

## Assurance boundary

This is an optional **structural comparison profile**, not a challenge tribunal, provenance verifier, execution replay facility, controller, or authorization mechanism. A `DECLARED_MATCH` can occur even when both declared outcomes are wrong. It is not an RAHP terminal PASS. No changes are made to existing assessor-result v1, R1, R2, reasoning trace, or assurance FSM.

Related: [R1 evidence adequacy](evidence-adequacy.md), [R2 temporal provenance](temporal-provenance.md), [reasoning architecture](reasoning-architecture.md).
