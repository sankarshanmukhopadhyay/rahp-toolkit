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

Cases: valid manifest, bad SHA-256, incorrect source URL, duplicate entry, unsafe relative path to a missing file, and traversal to an existing outside file. `compatible` means only both helpers accepted or rejected **that individual fixture**; `adaptation_required` is a disagreement. Neither means a shared method contract exists. Failures loading a required checkout fail closed.

### Evidence and next decisions

Probe-unit tests exercise fixture construction, distinct negative cases and missing checkout failure. **A comparative run against both full checkouts and broader repository validation have not been executed here.** Full Increment 6 acceptance requires pinned cross-checkout output, review semantics, vocabulary/validation alignment (after #22), and reassessment evidence. Preserve upstream method authority; do not standardize example-local evidence sidecars or import downstream assurance controllers solely to obtain compatibility.

AI-assisted contribution; subject to DCO, CI and independent review.

### Executed pinned comparison — GitHub Actions 2026-10-24

The initial five-scenario comparative probe executed successfully in [validate run 40057942238](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/40057942238), using accepted upstream revision `448e2ff4ca7f747ca899e0e845adfe45f750f094` and the downstream PR branch. The dedicated comparison step and focused unit tests passed. This is a **comparison-step result**, not by itself proof that every remaining CI job passed.

| Scenario | Upstream `verify_source` | Downstream `source_integrity` | Disposition |
| --- | --- | --- | --- |
| valid | accept | accept | common behavior |
| bad_hash | reject | reject | common behavior |
| bad_url | reject | accept | narrower downstream provenance-binding check |
| duplicate | reject | accept | narrower downstream manifest-uniqueness check |
| unsafe_path (missing traversal target) | reject | reject | same observed outcome, **not** proof of equal path-safety checks |
| traversal_existing | *requires fresh CI evidence* | *requires fresh CI evidence* | expected upstream reject / downstream accept; pending execution on latest head |

**Architectural disposition:** These are behavioral compatibility gaps at the helper boundary; they do **not** demonstrate a change in the upstream method or a need for shared sidecar/schema standardization. Treat downstream hardening of URL/provenance and duplicate-entry validation as a separate, bounded implementation decision. The initial unsafe-path fixture had a missing target and could not distinguish path-safety enforcement from file absence. The added `traversal_existing` fixture supplies the matching bytes outside the root, and the downstream checker accepts them; this demonstrates a path-containment gap in the narrow helper rather than in the upstream method.

Results are produced by the accepted downstream `.github/workflows/validate.yml` with a pinned upstream checkout; no additional workflow was retained because repository governance caps declared workflows. The JSON result is uploaded as a short-retention CI artifact. The six-scenario amended probe requires its own current-head execution before recording the sixth result as confirmed.
