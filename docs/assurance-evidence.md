# Assurance evidence contract

RAHP separates toolkit execution, corpus integrity, publication, and optional cross-specification evidence.

| Claim | Required control | Freshness expectation |
|---|---|---|
| Toolkit validation | repository validation workflow | Required |
| Corpus integrity | `.github/workflows/corpus-status.yml` | Required; successful recent execution |
| Publication integrity | repository publication workflow | Required |
| Cross-specification pressure test | applicable pressure-test workflow | Optional unless separately governed |

A green toolkit workflow must not be used to infer corpus integrity.

Portfolio finding lineage: `PF-9769E5EB9C48` (issue #223).

## Retest rule

Run the corpus-integrity control successfully, rerun the Portfolio Assurance Monitor, and close only when `PF-9769E5EB9C48` is recorded as resolved.
