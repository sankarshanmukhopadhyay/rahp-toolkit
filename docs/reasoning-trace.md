---
layout: default
title: "Optional reasoning trace"
parent: Learn RAHP
nav_order: 5
has_toc: true
permalink: /docs/reasoning-trace/
---
# Optional reasoning trace profile (experimental)

Tracking: [#928](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/928).

Read [reasoning architecture](reasoning-architecture.md) first for the distinction between invocation, assessment, and assurance terminalization.

## Scope and authority

The `rahp-reasoning-trace/v1` profile records a reviewable **justification**, not private chain-of-thought or a proof that an assessor is substantively correct. It is an **optional** artifact; `rahp-assessor-result/v1` remains the authoritative portable result contract. The controller's existing terminalization logic is unchanged.

A producer may embed the trace under `details.reasoning_trace` in a v1 result, or retain it as a separately pinned artifact. An integrating consumer must explicitly call `tools.reasoning_trace.validate_trace(trace, assessor_result)`; the portable v1 validator does not automatically validate nested profile semantics.

The assessor owns the proposition, evidence selection, method and judgment. RAHP owns structural validation and terminal reconciliation. The reviewer or governance authority owns approval, challenge and supersession. No automatic authority to accept residual risk is granted by this profile.

## Fields

- `schema`: `rahp-reasoning-trace/v1`
- `proposition_id`, `method`, `method_version`, `scope`: nonempty strings
- `evidence_refs`: unique evidence IDs matching the assessor result's `evidence_used`
- `observations`: nonempty array of unique `id`, `result` (`SATISFIED`, `NOT_SATISFIED`, `INDETERMINATE`) and nonempty `evidence_refs` subset
- `judgment`: `outcome` matching assessor result and nonempty `reason_codes`

The validator rejects a PASS with an unresolved or contradictory observation. This is deliberately conservative: producers needing a resolved contradiction must record a new explicit bounded assessment, not silently override an observation.

## Example

```json
{
  "schema": "rahp-reasoning-trace/v1",
  "proposition_id": "TRQP-TIME-001",
  "method": "source-example-time-comparison",
  "method_version": "1",
  "scope": "retained API example; not a live service",
  "evidence_refs": ["ER-API-EXAMPLE"],
  "observations": [
    {"id": "OBS-TIME", "result": "NOT_SATISFIED", "evidence_refs": ["ER-API-EXAMPLE"]}
  ],
  "judgment": {
    "outcome": "INDETERMINATE",
    "reason_codes": ["semantic-mismatch-requires-editor-clarification"]
  }
}
```

This example is a proposed trace over the documented TRQP example discrepancy, **not** a newly executed TRQP assessment. It does not resolve the upstream finding.

The optional [evidence adequacy profile](evidence-adequacy.md) addresses a different concern: declared evidence sufficiency and contradictions. Trace validation does not automatically invoke it.

Temporal applicability is a separate, optional check: see [R2 temporal and provenance reasoning](temporal-provenance.md). A valid reasoning trace does not imply historically applicable or authenticated evidence.

The optional [R3 reproducibility and challenge profile](reproducibility-challenge.md) supports declared-run comparison and open challenge records. Trace validity alone does not prove independent reproducibility.

## Verification

```bash
python3 -m unittest tests.test_reasoning_trace -v
python3 -m unittest tests.test_standalone_trqp -v
```

Future work: independent reviewer authority, freshness rules, supersession links and contradiction-resolution provenance. Those are intentionally **not** claimed as implemented by this first bounded profile.
