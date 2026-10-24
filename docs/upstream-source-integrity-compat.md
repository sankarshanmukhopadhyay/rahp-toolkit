# Upstream RAHP retained-source compatibility probe

Tracking: ToIP RAHP Task Force convergence issue #17, Increment 6.

This bounded probe compares the accepted upstream `review/source_integrity.py::verify_source` against downstream `examples/standalone-trqp/replay.py::source_integrity` with the **same** synthetic retained-source manifest. It is a test of observable behavior, **not** proof of full contract equivalence or target assurance.

### Reproduce

Use two **trusted**, source-pinned local checkouts (this tool imports their code; it does not fetch them):

```sh
python3 tools/source_integrity_compat.py --upstream /path/to/upstream-rahp --downstream /path/to/rahp-toolkit
python3 -m unittest tests.test_source_integrity_compat -v
```

Inspected source revisions when drafted: upstream `448e2ff4ca7f747ca899e0e845adfe45f750f094` (includes accepted #33, excludes unmerged #22); downstream `e35de9c7633545a5e0a08bc81180c3c80566678f`.

Cases: valid manifest, bad SHA-256, incorrect source URL, duplicate entry, unsafe relative path. `compatible` means only both helpers accepted or rejected **that individual fixture**; `adaptation_required` is a disagreement. Neither means a shared method contract exists. Failures loading a required checkout fail closed.

### Evidence and next decisions

Probe-unit tests exercise fixture construction, distinct negative cases and missing checkout failure. **A comparative run against both full checkouts and broader repository validation have not been executed here.** Full Increment 6 acceptance requires pinned cross-checkout output, review semantics, vocabulary/validation alignment (after #22), and reassessment evidence. Preserve upstream method authority; do not standardize example-local evidence sidecars or import downstream assurance controllers solely to obtain compatibility.

AI-assisted contribution; subject to DCO, CI and independent review.
