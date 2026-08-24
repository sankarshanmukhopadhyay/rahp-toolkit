---
layout: default
title: Performance and execution efficiency
parent: Learn RAHP
nav_order: 9
---
# Performance and execution efficiency

RAHP treats performance work as an assurance-preserving engineering activity. Faster execution is useful only when identical inputs continue to produce semantically equivalent normalized results, evidence lineage and validation outcomes.

## Measure before optimizing

The benchmark contract is defined in `method/execution-benchmarks.yaml`. It declares stable, non-publishing execution profiles for:

- portable core validation;
- packaged corpus and pressure-test validation;
- a representative source-pinned Trust Tasks × Credential Spec cross-specification run; and
- repository-wide non-Pages validation.

Run a profile locally with:

```bash
python3 tools/benchmark_execution.py core-validation
python3 tools/benchmark_execution.py corpus-validation
python3 tools/benchmark_execution.py cross-spec-dtg-tt-credspec
python3 tools/benchmark_execution.py full-validation
```

Each run writes machine-readable timing evidence to `build/execution-benchmark.json` unless another `--output` path is supplied.

## Metrics

The v1 benchmark contract records:

- total wall-clock duration;
- per-command duration and exit status;
- child-process peak RSS where the platform exposes it;
- command-output digests; and
- digests of selected semantic reference records.

The benchmark deliberately excludes external issue publication so performance measurement cannot create work items or mutate assessed repositories.

## Optimization invariant

For identical inputs, performance changes MUST NOT silently change normalized assessment semantics. Timing improvements therefore need to be evaluated together with the existing validation, conformance and evidence-lineage gates.

The initial engineering target is a material reduction in full-validation and representative cross-specification wall time, with a directional goal of at least 50% where duplicate execution, unnecessary setup or unaffected reassessment can be eliminated without weakening assurance.

## Expected optimization areas

The benchmark is intended to make the following opportunities measurable rather than assumed:

- reuse of parsed/validated immutable inputs;
- dependency caching in CI;
- elimination of duplicate validation between the main assurance job and Pages build;
- impact-selected scenario and cross-specification execution;
- parallel execution of independent validation lanes;
- avoiding repeated generation of unchanged derived views; and
- preserving already-current evidence rather than recomputing it solely because another surface changed.

The benchmark contract is versioned independently from semantic RAHP result contracts so the measurement method can evolve without changing the assurance model.
