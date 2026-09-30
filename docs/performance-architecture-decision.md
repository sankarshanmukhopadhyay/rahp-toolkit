# Performance Architecture Decision: Native Evaluation Kernel

Status: **Accepted**  
Decision issue: #859  
Parent workstream: #855  
Evidence tranches: #857, #858  
Decision date: 2026-09-30

## Decision

RAHP SHOULD NOT extract or rewrite its assurance evaluation path in C, C++, Rust, or another native language at this stage.

The measured performance evidence supports optimizing the current Python execution architecture first, with priority on repeated YAML parsing, repeated validator initialization/process execution, and reuse of immutable parsed inputs.

A native evaluator MAY be reconsidered only after those costs are reduced and a residual narrow computational kernel is shown to remain both material and semantically stable.

## Decision question

Does measured RAHP performance evidence justify extracting a narrow native evaluator prototype?

**Answer: no, not on the current evidence.**

The evidence establishes that representative RAHP execution is CPU-active, but it does not establish that the material CPU cost belongs to a narrow assurance-evaluation kernel suitable for native extraction.

## Evidence set

This decision is based on the benchmark and profiling evidence produced through the existing governed execution-benchmark workflow.

### Scaling evidence

GitHub Actions run: `36649462350`  
Revision profiled/benchmarked: `fde9f1e99fe1aef7dd8a73ca41afead9be7cf9ba`

Composition-breadth results:

| Profile | Runnable compositions | Wall time | Child CPU time |
|---|---:|---:|---:|
| `cross-spec-dtg-scale-small` | 1 | 1.559s | 1.558s |
| `cross-spec-dtg-scale-medium` | 4 | 5.834s | 5.833s |
| `cross-spec-dtg-scale-full` | 8 | 11.613s | 11.611s |

The observed scaling is approximately linear over the bounded 1/4/8 composition range. The measured cost per selected composition is approximately 1.56s, 1.46s, and 1.45s respectively.

This is evidence of predictable scaling, not evidence of a super-linear algorithmic bottleneck.

### Core validation profile

Representative `core-validation` profile:

- wall time: **5.779s**
- child CPU time: **5.742s**
- CPU/wall ratio: **0.994**
- classification: **cpu-dominant**

Largest wall-time contributors:

| Command | Wall time | Share |
|---|---:|---:|
| `tools/validate.py` | 2.155s | 37.3% |
| `tools/validate_project_invariants.py` | 1.572s | 27.2% |
| `tools/validate_catalogue.py` | 0.833s | 14.4% |

The raw `cProfile` evidence for `tools/validate.py` attributes roughly 1.71s of cumulative time to sixteen `yaml.safe_load` calls. The corresponding catalogue validator also spends most of its measured runtime in YAML loading/composition.

`validate_project_invariants.py` is different: most of its dominant path is a subprocess-backed stripped-core check, so its cost is not evidence for an assurance-evaluation kernel either.

### Full DTG cross-spec profile

Representative `cross-spec-dtg-full` profile:

- wall time: **35.523s**
- child CPU time: **35.482s**
- CPU/wall ratio: **0.999**
- classification: **cpu-dominant**

The largest individual commands are repeated invocations of `validate_pressure_tests.py`, each contributing about 6.6–6.9% of total wall time.

For a representative invocation:

- wall time: approximately **2.37s**
- YAML documents loaded: **31**
- cumulative `yaml.safe_load` time: approximately **2.28s**

The same pattern recurs across the composition-specific pressure-test validations.

The material CPU cost is therefore dominated by repeated parsing and validation of overlapping YAML inputs across separate Python invocations.

## Native-kernel gate assessment

| Gate | Result | Evidence |
|---|---|---|
| Material CPU-bound fraction exists | **PASS** | Representative profiles are ~99% CPU-active |
| Scaling behavior matters at realistic workloads | **PASS, bounded** | 1/4/8 composition costs rise predictably and approximately linearly |
| Narrow stable semantic boundary identified | **FAIL** | Dominant cost is distributed across parsing, validators, and subprocess-backed checks |
| Deterministic native-kernel I/O contract available | **NOT ESTABLISHED** | Existing semantic contracts exist, but no dominant extracted kernel has been identified |
| Differential/conformance testing feasible | **POSSIBLE** | RAHP has strong conformance infrastructure, but there is no justified alternate kernel to test yet |
| Material end-to-end gain from native extraction demonstrated | **FAIL** | Amdahl benefit cannot be established because the dominant work is not isolated to one kernel |

The native extraction gate therefore does not pass.

## Architectural interpretation

“CPU-bound” is not equivalent to “rewrite in a faster language.”

The current evidence shows that CPU time is being spent substantially in:

1. PyYAML scanner/parser/composer execution;
2. repeated loading of immutable or overlapping YAML inputs;
3. repeated startup of validators as separate Python processes;
4. validator-specific orchestration, including subprocess-backed checks.

A native assurance evaluator would leave much of this work untouched.

Even a hypothetically instantaneous assurance kernel would not materially improve execution if the measured hot paths remain YAML parsing and repeated validator startup.

## Approved optimization direction

The next performance tranche SHOULD optimize the existing Python execution architecture in this order:

1. **Reduce repeated YAML parsing.**
   Introduce safe reuse of parsed immutable inputs within a validation run where semantics permit.

2. **Reduce repeated validation initialization.**
   Explore batching related pressure-test validations in one process so shared catalogue and registry inputs can be loaded once.

3. **Preserve semantic equivalence.**
   Every optimization MUST retain identical validation outcomes, evidence semantics, failure behavior, and semantic-reference digests.

4. **Re-run the same benchmarks.**
   Compare `core-validation` and the 1/4/8 composition profiles using the existing benchmark policy.

5. **Profile again before reconsidering native code.**
   Only a residual computational hot path that remains material after Python-level optimization may reopen the native-kernel question.

## Revocation / reconsideration conditions

This decision is not permanent.

Reconsider native extraction if future evidence demonstrates all of the following:

- Python parsing/process overhead has been materially reduced;
- a stable semantic kernel remains responsible for a material fraction of end-to-end runtime;
- that kernel has deterministic bounded inputs and outputs;
- differential testing against the Python implementation is practical;
- expected end-to-end gain is material, not merely microbenchmark improvement.

Until those conditions are met, native-language work is out of scope for RAHP performance engineering.

## Assurance boundary

This decision concerns implementation performance only.

Performance evidence:

- is not assurance evidence;
- cannot set or modify RAHP assurance outcomes;
- cannot justify weakening validation or evidence requirements;
- cannot override fail-closed behavior;
- cannot substitute for semantic conformance.

## Consequences

### Positive

- avoids an unjustified language rewrite;
- focuses engineering effort on measured bottlenecks;
- preserves contributor accessibility and current deployment ergonomics;
- keeps optimization changes small and testable;
- gives any future native experiment a stronger evidentiary threshold.

### Trade-offs

- Python remains the primary execution environment;
- YAML-heavy validation remains a known performance cost until follow-up optimization is implemented;
- some process-isolation benefits may constrain how aggressively validators can be batched;
- future optimization work must explicitly preserve assurance and failure boundaries.

## Follow-up

Open a dedicated performance issue for shared-input parsing and validator batching. That issue should require measurable improvement against the existing benchmark profiles and semantic equivalence as an acceptance condition.
