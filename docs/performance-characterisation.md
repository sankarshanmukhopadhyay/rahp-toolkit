# RAHP Performance Characterisation Method

## Purpose

This document defines how RAHP performance evidence is collected before architectural optimization decisions are made.

Performance measurements are operational engineering evidence. They are not assurance outcomes and MUST NOT alter or substitute for RAHP assessment results.

## Current benchmark surface

RAHP uses `tools/benchmark_execution.py` with profiles defined in `method/execution-benchmarks.yaml`.

The runner records:

- profile wall time;
- child-process CPU time;
- peak child RSS;
- command-level wall and CPU time;
- command exit status;
- output digests and bounded output tails;
- semantic-reference digests;
- repeated-sample distributions when `--samples` is greater than one.

For repeated runs, the established top-level `wall_seconds` value is the median so existing baseline comparison remains compatible while reducing sensitivity to one noisy observation.

## Modes

### Pull-request regression check

Pull requests intentionally use one candidate sample and one baseline sample.

This is a low-cost regression signal, not a statistically strong performance claim. The existing regression policy requires both a relative and absolute slowdown before failing because hosted runners are noisy.

### Manual characterisation run

Use repeated samples when investigating an architectural question:

```bash
python3 tools/benchmark_execution.py core-validation --samples 3
```

The GitHub Actions workflow also supports 1, 3, or 5 samples for manually dispatched runs.

Repeated samples provide min, median, mean, and max values for wall and child CPU time.

## Interpretation

Wall time answers how long the profile took.

Child CPU time estimates how much processor time was consumed by the subprocesses executed by the benchmark runner.

The relationship between the two is diagnostic rather than dispositive:

- wall time materially greater than CPU time may indicate waiting, filesystem activity, process startup, or other non-CPU constraints;
- CPU time approaching or exceeding wall time may indicate CPU-intensive execution or parallel child work;
- neither metric alone proves which function or subsystem is responsible.

A profiler or more specific instrumentation is required before attributing a bottleneck to a semantic component.

## Semantic invariants

Performance work MUST preserve these invariants:

1. identical benchmark inputs retain their semantic reference digests;
2. benchmark command failure remains a failed/invalid run rather than a performance PASS;
3. repeated sampling does not mutate assessment state;
4. benchmark telemetry remains non-authoritative and cannot set assurance outcomes;
5. optimization claims require evidence from like-for-like execution profiles.

A faster result with different semantic reference inputs is not comparable.

## Realistic scaling workloads

RAHP's first controlled scaling dimension is the number of runnable DTG cross-specification compositions executed from the profile-owned registry.

The benchmark contract defines three bounded profiles:

- `cross-spec-dtg-scale-small` — 1 runnable composition;
- `cross-spec-dtg-scale-medium` — 4 runnable compositions;
- `cross-spec-dtg-scale-full` — all 8 currently runnable compositions.

These profiles execute real registry entries and their real assessment files through the existing corpus validation, pressure-test validation, and review rendering paths. They do not create artificial CPU work or duplicate synthetic evidence merely to increase runtime.

The selected composition count is emitted as `workload_dimensions` in benchmark JSON. The DTG registry and selected assessment files are included in the semantic-reference digest set so results remain tied to the exact workload inputs.

The dimension measures **composition breadth**. It does not claim to model repository network latency, concurrent assessment execution, or arbitrarily large evidence corpora.

When the registry's runnable composition count changes, the declared benchmark dimension must be deliberately reconciled rather than silently interpreted as the same workload.

## Runtime attribution

`tools/profile_execution.py` profiles the Python commands declared by an existing benchmark profile.

For each command it retains wall time, child CPU time, CPU/wall ratio, an explicit runtime classification, raw `cProfile` statistics, captured output and digest, and the top cumulative Python call paths. The aggregate report attributes each command's share of profile wall time and identifies the largest contributors.

Runtime classifications are deliberately coarse:

- `cpu-dominant`: child CPU / wall ratio is at least 0.80;
- `wait-or-process-dominant`: ratio is at most 0.40;
- `mixed`: values between those thresholds;
- `indeterminate`: invalid or zero-duration measurement.

These labels are diagnostic observations, not architectural conclusions. A process-heavy command may spend time in child processes that require separate profiling, and hosted-runner scheduling can affect wall time.

The profiling workflow automatically exercises `core-validation` and `cross-spec-dtg-full` when the profiler changes. Raw statistics, JSON runtime budgets, and Markdown reports are retained as workflow artifacts.

A bottleneck claim should identify the exact profile, revision, command, measured wall share, CPU/wall ratio, and raw profile artifact supporting it.

## Architecture decision gate

A C, C++, Rust, or other native evaluator is not justified merely because native code can execute faster.

Before a native evaluator prototype is opened as implementation work, evidence should establish:

- a material CPU-bound fraction in a representative RAHP execution path;
- scaling behavior that matters at realistic workloads;
- a narrow, stable semantic boundary suitable for extraction;
- deterministic inputs and outputs;
- differential or conformance testing against the current implementation;
- a material expected end-to-end improvement after accounting for time spent outside the candidate kernel.

If those conditions are not established, the appropriate outcome may instead be Python optimization, caching, reduced parsing, process reduction, I/O/concurrency work, or no optimization.

## Evidence handling

Benchmark JSON and comparison JSON generated by CI are the primary machine-readable evidence.

Raw measurements should be retained as workflow artifacts where practical. Architecture conclusions should cite the exact profile, revision, sample count, runner context, and relevant artifacts.

Performance evidence should be treated as environment-sensitive. Hosted-runner measurements are useful for regression detection and directional comparison, not as universal hardware-independent throughput guarantees.

## Follow-on work

Issue #855 tracks the wider characterisation tranche:

1. characterisation-quality benchmark evidence;
2. realistic workload/scaling dimensions;
3. attributable profiling of representative runs;
4. an evidence-based architecture decision.
