# Real-policy pressure-test corpus

This directory contains **bounded research snapshots** derived from public policy documents for RAHP issue #662. They are not represented as complete copies of the upstream policies and must not be used as substitutes for the authoritative source.

## Provenance

The current tranche uses the public `github/site-policy` repository pinned at commit:

`b9578b546d2506febda1da2cd7431644d58e512c`

The upstream repository declares CC0 1.0 Universal. Each research snapshot records the authoritative upstream path and upstream blob SHA in YAML front matter. RAHP separately calculates its own assessment-source SHA-256 over the retained snapshot bytes. Those identifiers have different meanings and MUST NOT be conflated.

| Research snapshot | Upstream path | Upstream blob SHA | Pressure-test purpose |
|---|---|---|---|
| `github-acceptable-use-policies.md` | `Policies/acceptable-use-policies/github-acceptable-use-policies.md` | `5100dcce69b9b86beb8ecbe2d5b634700633d4df` | prohibitions, nested policy structure, privacy/use restrictions, enforcement discretion, redress linkage |
| `github-appeal-and-reinstatement.md` | `Policies/acceptable-use-policies/github-appeal-and-reinstatement.md` | `2600be9eaafe0d8178c4a74d53e1785aea9186ba` | remedy semantics, adverse-action scope, time bounds, discretion, human review, escalation/legal boundary |

## Why bounded snapshots

The research question at this stage is whether RAHP can preserve and reason over realistic policy structure without weakening evidence discipline. A bounded snapshot keeps the fixture reviewable and deterministic while retaining the source patterns needed to falsify W2/W3/W4 assumptions.

A later graduation tranche should add a reproducible acquisition/pinning command that can retrieve and verify the complete authoritative source outside offline CI, while keeping network retrieval out of deterministic unit tests.

## Current pressure-test claims

The real-corpus tests require that:

- YAML provenance/front matter is metadata, not a policy proposition;
- Markdown heading hierarchy remains attached to each derived proposition;
- list items remain independent source spans rather than becoming one opaque paragraph;
- every proposition can reconstruct its exact retained source bytes from offsets;
- materially different documents produce materially different proposition models;
- discretionary language remains judgment-required;
- risk mappings remain hypotheses rather than terminal assurance findings.

These claims are executable in `tests/test_policy_real_corpus.py`.

## Known limits retained deliberately

This tranche does not yet claim complete Markdown-table semantics, complete definition resolution, incorporation-by-reference traversal, remote source acquisition, scanned/PDF handling, or legal interpretation. Referenced policies should be identified and pinned before traversal is added; they must never be silently fetched and absorbed into the assessment subject.
