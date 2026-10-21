# TSP Release 1.0 normative-delta execution procedure

**Purpose:** reproduce the complete Rev 3 → Release 1.0 source difference and preserve a machine-readable, human-reviewable clause inventory. This is **not** a TSP conformance or four-lens assurance PASS.

## Inputs (immutable upstream commits)

- Rev 3: `f5b8668952aabe8e541b535fcbdf589484ffc4f4`
- Release 1.0 candidate: `ccda6b33159d860f05c328eb436dabe83548b705`
- Source path in both revisions: `spec/spec.md`

With an authenticated or public local checkout of `trustoverip/tswg-tsp-specification` containing both commits, run:

```sh
git -C /path/to/tswg-tsp-specification show f5b8668952aabe8e541b535fcbdf589484ffc4f4:spec/spec.md > /tmp/tsp-rev3.md
git -C /path/to/tswg-tsp-specification show ccda6b33159d860f05c328eb436dabe83548b705:spec/spec.md > /tmp/tsp-release1.md
python3 -m unittest discover -s tests -p test_tsp_normative_delta.py -v
python3 tools/tsp_normative_delta.py --before /tmp/tsp-rev3.md --after /tmp/tsp-release1.md --output /tmp/tsp-normative-delta.json
```

Record the JSON artifact's `old_sha256`, `new_sha256`, `changed_hunks`, and per-hunk source line ranges with the campaign. Each changed hunk is marked for **human normative review**. Normative keyword matches are review cues, not an automatic classification of whether an obligation changed. Review all hunks, including those without RFC 2119 terms.

## Source and implementation gates

1. Compare the complete 19-commit source history, not merely the final Release 1.0 header/version change.
2. Reconcile all changed obligations and encoded layouts with the Release 1.0 test matrix.
3. Establish implementation and test-vector source pins separately from the specification pin.
4. Execute targeted negative cases, security and composition cases, and DRARM; record unsupported and skipped coverage.
5. Keep final RAHP, security, composition and DRARM dispositions **INDETERMINATE** until each lens has evidence and acceptance review.

**Current status:** tooling and procedure committed; a full real-source inventory execution has **not** yet been demonstrated. No workflow is added and no routine CI network dependency is introduced.
