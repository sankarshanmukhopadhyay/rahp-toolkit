# RAHP Performance Characterisation — 2026-09-30

## Scope

This report records measured scaling and runtime-attribution evidence for issues #857 and #858.

The measurements are engineering evidence from GitHub-hosted runners. They are not hardware-independent throughput guarantees and they are not RAHP assurance outcomes.

## Evidence identity

- Pull request implementation: #861
- Branch head measured by the performance workflow: `fde9f1e99fe1aef7dd8a73ca41afead9be7cf9ba`
- Workflow run: `36649462350`
- Benchmark contract: `rahp-execution-benchmark-v1`
- Scaling dimension: `dtg_runnable_compositions`
- Runnable compositions in registry: 8

Raw workflow artefacts retained by the run include:

- `rahp-scaling-cross-spec-dtg-scale-small` — artifact `11069234822`
- `rahp-scaling-cross-spec-dtg-scale-medium` — artifact `11070116716`
- `rahp-scaling-cross-spec-dtg-scale-full` — artifact `11070017197`
- `rahp-runtime-profile-core-validation` — artifact `11070215038`
- `rahp-runtime-profile-cross-spec-dtg-full` — artifact `11069967487`

Semantic-reference digests are embedded in each scaling benchmark artefact.

## Scaling observation

Single-run measurements for the bounded composition-breadth workloads were:

| Runnable compositions executed | Profile | Wall time | Child CPU time | Peak child RSS |
|---:|---|---:|---:|---:|
| 1 | `cross-spec-dtg-scale-small` | 1.559 s | 1.558 s | 20,872 KB |
| 4 | `cross-spec-dtg-scale-medium` | 5.834 s | 5.833 s | 20,840 KB |
| 8 | `cross-spec-dtg-scale-full` | 11.613 s | 11.611 s | 20,872 KB |

Across these three points, wall time is approximately linear in composition count. A simple linear fit is approximately:

```text
wall_seconds ≈ 0.110 + 1.437 × composition_count
```

The fit is descriptive only; three single-run points are insufficient for a universal scaling law. Within this bounded workload, however, there is no evidence of super-linear growth and no material memory growth.

The CPU/wall relationship is effectively 1:1 for all three measurements. The workload is therefore CPU-dominant on this runner rather than waiting on network or filesystem latency.

## Core-validation attribution

The representative `core-validation` profile reported:

- wall time: **5.779 s**
- child CPU time: **5.742 s**
- CPU/wall ratio: **0.9936**
- classification: **cpu-dominant**

Largest command-level contributors:

| Command | Wall share |
|---|---:|
| `tools/validate.py` | 37.3% |
| `tools/validate_project_invariants.py` | 27.2% |
| `tools/validate_catalogue.py` | 14.4% |

The raw cProfile evidence identifies two distinct causes:

1. `validate.py`: approximately 1.708 s of its profiled execution was in PyYAML `safe_load` across 16 loads. YAML composition/parsing dominates the command.
2. `validate_catalogue.py`: approximately 0.586 s was in PyYAML `safe_load` across six loads.
3. `validate_project_invariants.py`: the largest cost is the subprocess-based stripped-core check, including roughly 1.23 s waiting for the child process. This is process orchestration rather than an assurance-evaluation kernel.

## Cross-specification attribution

The representative `cross-spec-dtg-full` profile reported:

- wall time: **35.523 s**
- child CPU time: **35.482 s**
- CPU/wall ratio: **0.9988**
- classification: **cpu-dominant**

The profile executes eight real DTG cross-specification compositions.

The repeated pattern is stable:

- each `validate_scenario_corpora.py` invocation consumes roughly 1.87–1.92 s, about 5.3% of total runtime;
- each `validate_pressure_tests.py` invocation consumes roughly 2.34–2.47 s, about 6.6–6.9% of total runtime;
- each `cross_spec_review.py` invocation is small, roughly 0.15–0.18 s.

For the sampled `validate_pressure_tests.py` commands, cProfile shows approximately 2.27–2.38 s in PyYAML `safe_load` across 31 loads. YAML composition/parsing accounts for nearly the entire command.

The evidence therefore points to **repeated parsing and repeated process-local loading of the same catalogue/corpus structures** as the dominant scaling cost.

## Bottleneck disposition

### Observed

- representative RAHP validation paths are CPU-dominant;
- cross-spec runtime scales approximately linearly with composition breadth over 1, 4, and 8 real compositions;
- peak child RSS stayed approximately flat near 20.8 MB for the bounded scaling workload;
- YAML parsing is the dominant Python hot path in the largest validation commands;
- repeated command/process execution causes the same semantic catalogues to be reparsed many times.

### Inferred, with high confidence

The current performance bottleneck is **not evidence of a computationally expensive assurance decision kernel**.

The strongest optimization candidates are instead:

1. reduce repeated YAML parsing;
2. share or serialize normalized catalogue/corpus data across validation steps where compatibility permits;
3. consolidate repeated validators when doing so does not blur their independent claims;
4. reduce process startup and duplicate stripped-core validation work;
5. preserve existing semantic-digest and fail-closed behavior while testing these changes.

### Not established

The evidence does not establish that a C, C++, or Rust evaluator would materially improve end-to-end RAHP performance.

A native rewrite of the current hot path would mostly accelerate general YAML parsing and validation orchestration, areas where lower-risk architectural improvements are available first.

## Assurance boundary

Performance optimization MUST NOT:

- weaken validation rules;
- reuse stale semantic data across changed inputs;
- collapse missing or indeterminate evidence into PASS;
- change normalized assurance outcomes;
- make a derived cache authoritative.

Any cache or shared normalized representation must be invalidated by the semantic input digests already retained by the benchmark framework.

## Disposition for #857

The realistic-workload objective is satisfied for the first bounded scaling dimension:

- real workload: DTG runnable cross-specification compositions;
- sizes: 1, 4, 8;
- machine-readable dimensions: present;
- semantic references: digested;
- measured artifacts: retained;
- observed scaling: approximately linear within the tested range.

Further dimensions may be added later when a concrete scaling question warrants them; they are not prerequisites for this tranche.

## Disposition for #858

Runtime bottlenecks have been attributed sufficiently to guide the next engineering decision:

- CPU-bound: **yes**;
- memory-bound: **not observed** in the bounded scaling workload;
- network-bound: **no evidence in these non-publishing profiles**;
- principal hot path: **repeated YAML parsing / catalogue loading**;
- secondary cost: **process/subprocess orchestration**;
- native semantic kernel justified by current evidence: **not established**.

Issue #859 should therefore evaluate optimization of the existing Python data-loading/validation architecture before considering a native evaluator.
