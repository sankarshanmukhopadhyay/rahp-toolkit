# TRQP retained-source integrity hardening

Tracking: ToIP RAHP Task Force convergence issue #17, Increment 6, and [downstream comparison PR #1135](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1135).

## Bounded claim

The standalone TRQP teaching replay now fails closed for malformed retained-source manifests, duplicate paths or upstream identities, incorrect immutable provenance URL bindings, path traversal and symlink escapes, in addition to SHA-256/Git-blob mismatches. This change modifies the **example-local** helper only, not the RAHP method, assurance controller or general evidence schema.

## Source and reproduction

The differences were discovered by executing the pinned cross-repository probe in downstream PR #1135. Upstream accepted source revision: `448e2ff4ca7f747ca899e0e845adfe45f750f094`. Downstream base: `e35de9c7633545a5e0a08bc81180c3c80566678f`.

```sh
python3 -m unittest tests.test_trqp_source_integrity_hardening -v
python3 -m unittest tests.test_standalone_trqp -v
python3 examples/standalone-trqp/replay.py --check
```

The first suite verifies the unchanged retained-positive replay and rejects duplicate local or upstream paths, mismatched source URLs, traversal to an existing external file, symlink escapes, non-immutable revisions and altered source contents. The original replay remains source-only; its unchanged `overall_assurance: review-required` does not confer target assurance or operational authorization.

## Interpretation and limitations

The upstream helper is the behavioral reference for the narrow manifest checks. This is intentionally a local repair to a historical teaching example rather than an adoption of upstream's full method contracts. Files are checked locally; SHA and Git blob checks are integrity bindings, **not signatures or proof of GitHub provenance**. Neither implementation verifies actual repository access or deployed behavior. Reviewer judgment and upstream adoption gates remain separate.

AI-assisted preparation, implementation and documentation. Independent reviewability: **APPLICABLE**; source pins, negative cases, CLI reproduction, known limits and remediation boundary are recorded here.
