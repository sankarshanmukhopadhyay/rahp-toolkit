---
layout: default
title: "Temporal and provenance reasoning"
parent: Learn RAHP
nav_order: 7
has_toc: true
permalink: /docs/temporal-provenance/
---
# Temporal applicability and provenance (experimental R2)

Tracking: [#933](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/933).

This optional profile checks **declared historical applicability** of source-pinned evidence. It does not reconstruct historical truth, verify source authority, infer revocation, or confer an RAHP assurance PASS. The stable assessor-result v1, R1 evaluator, reasoning trace, and assurance controller remain unchanged.

## Temporal semantics

- `target_time`: time the proposition concerns.
- `knowledge_cutoff`: only records whose `recorded_at` is no later than this time may inform the as-known-at determination.
- `evaluated_at`: time the evaluator runs; cutoff cannot exceed it.
- `observed_at`: when evidence was observed.
- `recorded_at`: when this assertion was recorded or discovered; cannot precede observation.
- `effective_from` and optional `effective_until`: **claimed** validity interval, inclusive start and exclusive end.
- `source_pin`: required repository and revision declaration, not cryptographic authentication.
- `max_observation_age_seconds`: optional nonnegative integer freshness policy, measured against `evaluated_at`. Omission imposes no implicit TTL.

All times require explicit UTC offsets. Equivalent instants in different timezones compare equally. The caller supplies a `proposition_id`, unique `required_evidence` IDs and `records` with unique IDs. Every record must reference a declared evidence ID.

## Decision semantics

| Condition | Finding |
| --- | --- |
| Exactly one known record covers target time and meets configured freshness | `APPLICABLE` |
| No record known at cutoff | `NOT_KNOWN_AT_CUTOFF` |
| More than one record known at cutoff | `CONFLICT` |
| Target outside effective interval | `OUTSIDE_EFFECTIVE_INTERVAL` |
| Optional freshness bound violated | `STALE_OR_FUTURE_OBSERVATION` |

The overall `disposition` is `APPLICABLE` only when **every** required evidence item is applicable. Otherwise it is `INDETERMINATE`. This is intentionally **not** an assessor-result outcome: applicability is not satisfaction. Malformed data raises `ValueError`.

Records discovered after the cutoff but by the evaluation time are disclosed in `later_record_ids`, not silently incorporated into the historical as-known-at answer. If a later assertion claims retroactive effect, rerun with a later cutoff to expose the competing assertion. Multiple known records conservatively yield `CONFLICT`; supersession and precedence require separate governed rules. The evaluator does not store source history or establish any source's legitimacy.

## Worked example

```python
from tools.temporal_provenance import evaluate_temporal

profile = {
    "schema": "rahp-temporal-provenance/v1",
    "proposition_id": "HIST-001",
    "target_time": "2026-04-15T00:00:00Z",
    "knowledge_cutoff": "2026-05-01T00:00:00Z",
    "evaluated_at": "2026-08-20T00:00:00Z",
    "required_evidence": ["ER-1"],
    "records": [{
        "id": "REC-1",
        "evidence_id": "ER-1",
        "source_pin": {"repository": "example/spec", "revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
        "observed_at": "2026-04-15T00:00:00Z",
        "recorded_at": "2026-04-16T00:00:00Z",
        "effective_from": "2026-04-10T00:00:00Z",
        "effective_until": "2026-05-01T00:00:00Z"
    }]
}
print(evaluate_temporal(profile))
```

## Conformance and limitations

```bash
python3 -m unittest tests.test_temporal_provenance -v
python3 -m unittest tests.test_evidence_adequacy tests.test_reasoning_trace -v
python3 tools/evidence_assertion_assessor.py --self-test
```

A source pin is a **claim**, not verification that the source was fetched, hashed, authenticated or authoritative. This evaluator cannot determine whether historical effective state was correct, whether a retroactive assertion is legitimate, or whether evidence was superseded. It does not automatically alter any prior assessment. A separate provenance verifier and governed authority policy would be required for that.

The optional [R3 reproducibility and challenge profile](reproducibility-challenge.md) can compare declared runs but does not prove the correctness of historical assertions.

Related: [R1 evidence adequacy](evidence-adequacy.md), [reasoning architecture](reasoning-architecture.md), [reasoning trace](reasoning-trace.md), and [agent integration](reasoning-integration.md).
