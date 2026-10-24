# RAHP source-integrity post-repair comparison

Tracking: ToIP RAHP Task Force convergence #17, Increment 6.

## Scope and source pins

- Accepted upstream source: `448e2ff4ca7f747ca899e0e845adfe45f750f094` (`review/source_integrity.py`).
- Post-repair downstream baseline: merged PR #1136, commit `d7150ba6bacb2a11c3b2ee8444c82b643c1bb067` (`examples/standalone-trqp/replay.py`).
- Original pre-repair comparison: [PR #1135](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1135), including evidence of URL-binding, duplicate-entry and existing-file traversal acceptance by the former downstream helper.
- Repair: [PR #1136](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1136), merged after documented maintainer acceptance, no independent reviewer approval claimed.

## Reproduce

The existing validation workflow on this PR checks out the exact accepted upstream commit, runs focused tests and this comparison, asserts expected accept/reject outcomes and retains JSON output:

```sh
python3 -m unittest discover -s tests -p 'test_source_integrity_compat.py' -v
python3 tools/source_integrity_compat.py --upstream /path/to/pinned/upstream --downstream /path/to/postrepair/downstream
```

Six cases are checked: valid source, corrupt digest, wrong source URL, duplicate entry, unsafe missing-file traversal and traversal to a real existing outside file. Equivalence is limited to **accept/reject results for these fixtures**; it is not proof of general schema equivalence, live source authenticity or target assurance.

## Completion limits

Only the bounded source-integrity component of Increment 6 can be qualified here. Review semantics, vocabulary, evidence-envelope and reassessment compatibility remain separately testable requirements. The merged TRQP helper still performs local evidence validation, not remote provenance authentication. CI run IDs and any observed discrepancies must be recorded before claiming this new comparison passed. Preserve historical evidence and distinguish maintained downstream behavior from accepted upstream method authority.

AI-assisted preparation. Independent reviewability: **APPLICABLE**, with source pins, negative tests, reproducible commands and explicit limitations.