# Source-pinned independent replay challenge — 2026-10-18

**RAHP owner:** [#928](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/928). **Evidence grade:** deterministic replay of a *retained TRQP source snapshot* with constructed positive and negative responses, not authentication or a live authorization service. R1–R3 synthetic cross-process validation is separately covered by [#1053](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1053).

The standalone TRQP example has an explicit `source-manifest.json` with both SHA-256 and Git blob hashes, schema validation and `expected-replay.json`. These are a bounded basis for testing source-substitution refusal.

## Reproducible tests

```bash
python3 -m unittest tests.test_trqp_source_pinned_challenges -v
python3 examples/standalone-trqp/replay.py --check
```

The new negative and process-isolation tests:
- invoke the real portable replay CLI in *two fresh processes* and compare complete output, including its manifest `target_commit`;
- verify source-integrity status remains `verified` and the overall result remains `review-required`, never terminal PASS;
- mutate a retained upstream HTTP example and require the Git-blob/SHA-256 mismatch to raise instead of being ignored;
- change the expected schema validity of a constructed case and require a failure;
- preserve the contradictory historical query-vs-response time example, `requested_time_matches=false`, rather than normalizing it into a fabricated match.

## Distinctions

| Claim | Supported | Not established |
| --- | --- | --- |
| Content of retained source snapshot is bound to the manifest hashes | Yes, by tests and schema replay | Whether the upstream specification publisher was authoritative at the claimed commit |
| Two independent Python process invocations produce the same bounded result | Yes | Independent implementations or human reviewers reach the same normative assessment |
| Contradictory/missing constructed response rejected or surfaced | Yes | Authenticity, freshness and runtime authorization history of a deployed endpoint |
| New evidence may revise judgment | The challenge can be surfaced in a review record | Competent approval, supersession governance or closure of an external challenge |

This closes an **executable source-integrity/replay gap** in #928 without creating another trace schema. #928 remains OPEN for independent source acquisition/authentication, external reviewer attribution, and governed challenge/supersession acceptance. The code is entirely offline and safe to run under continuous integration; no real customer or credential data is committed.
