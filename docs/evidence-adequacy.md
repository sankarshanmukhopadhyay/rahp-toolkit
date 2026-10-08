---
layout: default
title: "Evidence adequacy evaluation"
parent: Learn RAHP
nav_order: 6
has_toc: true
permalink: /docs/evidence-adequacy/
---
# Evidence adequacy evaluation (experimental R1)

Tracking: [#931](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/931).

The optional [evidence adequacy evaluator](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/main/tools/evidence_adequacy.py) is a pure, deterministic **structural evaluation profile**. It is not a new terminal assurance controller, evidence authenticator, rules language, or LLM. It is **not** wired into existing assessor-result v1 consumers.

## Contract

Input schema marker: `rahp-evidence-adequacy/v1`. Supply a nonempty `proposition_id`, a bounded `scope`, unique `required_evidence` identifiers, and an array of observations. Each observation has a unique `id`, declared `evidence_id`, matching `scope`, and one of `SATISFIED`, `NOT_SATISFIED`, or `UNAVAILABLE`.

Each required evidence ID must have exactly one matching, in-scope observation to support PASS. Duplicate observations are treated as `CONFLICT` even if they agree; source deduplication, precedence, and supersession must happen outside this profile. A declared scope is not independently authenticated by this evaluator.

| Evidence condition | Bounded result |
| --- | --- |
| Every required item uniquely SATISFIED | PASS |
| One or more NOT_SATISFIED, no unresolved items | FAIL |
| Missing, UNAVAILABLE, CONFLICT or OUT_OF_SCOPE | INDETERMINATE |
| Negative and missing together | INDETERMINATE, retaining both findings |
| Malformed IDs, states or undeclared references | Explicit ValueError, no result |

The evaluator sorts findings by evidence ID, and observation IDs within each finding, to ensure order-invariant results. No evidence item is silently discarded.

**Important:** This is a *proposed conservative policy* for an optional profile, not a change to the existing `evidence_assertion_assessor.py` missing-first behavior. Structural sufficiency is not evidence authenticity, truth, authorization, or full RAHP assurance. The caller must supply and govern its evidence declarations and source pins separately.

## Executable example

From the repository root:

```python
from tools.evidence_adequacy import evaluate

profile = {
    "schema": "rahp-evidence-adequacy/v1",
    "proposition_id": "EXAMPLE-001",
    "scope": "pinned specification example",
    "required_evidence": ["ER-1"],
    "observations": [
        {"id": "OBS-1", "evidence_id": "ER-1",
         "scope": "pinned specification example", "state": "SATISFIED"}
    ],
}
print(evaluate(profile))
```

A PASS here means only that the **declared** observation set meets this structural policy. It does not mean the specification or deployment has passed RAHP assurance.

## Tests and compatibility

```bash
python3 -m unittest tests.test_evidence_adequacy -v
python3 -m unittest tests.test_reasoning_trace -v
python3 tools/evidence_assertion_assessor.py --self-test
```

The optional evaluator is deliberately not integrated into `tools/reasoning_trace.py` or `tools/assurance_fsm.py`. The optional [R2 temporal applicability profile](temporal-provenance.md) now examines declared observation and effective times, as-known-at cutoffs, and source-pin metadata. It does not authenticate sources, settle supersession or historical truth, or justify automatic controller integration. See [reasoning architecture](reasoning-architecture.md), [reasoning trace](reasoning-trace.md), and [agent integration](reasoning-integration.md).
