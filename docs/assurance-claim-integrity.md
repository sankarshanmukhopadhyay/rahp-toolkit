---
layout: default
title: "Scenario-corpus assurance claim integrity"
parent: "Scenario corpora"
has_toc: true
nav_exclude: true
---
# Scenario-corpus assurance claim integrity

**Tracker:** [#1144](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1144)

This capability checks whether recorded corpus provenance and evidence-grade metadata are internally defensible enough to publish without a machine-observable contradiction. It does **not** certify the source, decide that a grade is substantively deserved, prove implementation conformance, or replace accountable review.

## Why this exists

#1142 demonstrated that a corpus could be structurally valid while its provenance description and evidence grade were mutually inconsistent. #1145 then showed that even an immutable pin can be attached to the wrong authority surface. #1147 showed a third case: semantic requalification can be complete while the resulting corpus still has mixed grounding and therefore does not justify a corpus-wide source-pinned claim.

These cases establish three different questions:

| Question | Mechanism | Meaning |
|---|---|---|
| Is the corpus structurally well formed? | scenario-corpus validator | Required fields, IDs and references are coherent. |
| Is the provenance reproducible and internally consistent? | source registry, immutable pins, dependency rules, claim-integrity invariants | Recorded authority and derivation claims can be checked. |
| Is the assurance/evidence claim substantively justified? | accountable semantic review and retained evidence | A human-reviewed evidence judgment; not inferred from a passing validator. |

Passing the first two is necessary for defensible publication, not sufficient for the third.

## Existing claim-bearing fields

The capability deliberately reuses existing metadata rather than introducing a mandatory parallel claim-status schema.

| Field / mechanism | Role |
|---|---|
| `evidence_grade` | Declared corpus grounding class such as `scenario-baseline`, `source-informed`, or `source-pinned`. |
| `provenance_status` | Review or grounding state recorded by the adapter. |
| `source_commit` | Reviewed immutable revision or an explicitly symbolic provenance mode. |
| `source_anchor` | Scenario-level source grounding where available. |
| `depends_on[].source_commit` | Revision used by a composed corpus for each dependency. |
| `adapter_version` | Semantic adapter revision. |
| `corpora/sources.yaml` | Source authority, tracked paths, dependency graph, update mode, review policy and optional `authority_pin`. |
| `tools/corpus_status.py` | Moving-source drift and recomposition detection. |
| Pages projection | Reader-facing grade, provenance state, source anchors and claim-integrity interpretation. |

## Invariants

The executable rules are intentionally narrow. They fail only when the repository contains enough information to identify a contradiction.

| ID | Invariant | Enforcement |
|---|---|---|
| CI-01 | A standalone `source-pinned` grade requires an immutable 40-character source commit. | `corpus_claim_integrity.static_claim_errors` |
| CI-02 | No corpus-wide evidence grade can coexist with a provenance/composition review-pending state. | same |
| CI-03 | A corpus explicitly recorded as `semantic-requalification-complete-mixed-grounding` cannot claim any corpus-wide evidence grade. | same |
| CI-04 | A derived `source-pinned` corpus requires immutable dependency pins. | same |
| CI-05 | A declared `authority_pin` must match the corpus `source_commit`. | scenario-corpus validator |
| CI-06 | A corpus claiming `derived-from-pinned-dependencies` cannot silently use dependency pins that differ from the current parent baselines. | scenario-corpus validator |
| CI-07 | Independent dependency pins may differ from standalone parents only when that distinction is explicit in provenance. | scenario-corpus validator |
| CI-08 | Evidence grades are never inherited transitively from parent corpora. | design rule + regression coverage; no automatic grade derivation exists |
| CI-09 | Material tracked-source or dependency drift produces **reassessment-required**, not an automatic grade downgrade. | `corpus_status.py` + claim-state derivation |
| CI-10 | Publication must expose a pending, mixed or undeclared claim boundary rather than presenting raw grade metadata without interpretation. | Pages projection + regression test |

## Derived claim states

Claim state is a reader/monitor interpretation of recorded metadata; it is not a new certification level.

| State | Meaning |
|---|---|
| `undeclared` | No corpus evidence grade is declared. |
| `review-pending` | Recorded provenance says semantic/composition review remains incomplete. |
| `mixed-grounding` | Semantic review is complete but the corpus intentionally contains different grounding classes. |
| `declared` | An evidence grade is recorded and no repository-local contradiction is known. This does not establish substantive sufficiency or runtime assurance. |
| `declared-currentness-unchecked` | An offline check sees a declared grade but did not query source currentness. |
| `reassessment-required` | Tracked source/dependency material changed and the recorded grounding must be reassessed before currentness is relied on. |

The states are derived rather than persisted so the repository does not create a second lifecycle field that can itself drift from the source and provenance metadata.

## Change impact

`tools/corpus_status.py` remains the source-drift mechanism. The claim-integrity layer annotates each status result.

A relevant upstream change does **not** mechanically mutate or downgrade `evidence_grade`. Instead, a corpus with material tracked-source or dependency drift is surfaced as `reassessment-required`. This preserves historical evidence while making the currentness limitation explicit.

An offline run cannot claim source currentness. Where a grade is declared, it reports `declared-currentness-unchecked`.

## Publication behavior

The corpus browser now includes a `claim_integrity` row.

- pending provenance renders a **Review pending** warning;
- completed mixed grounding renders **Mixed grounding**;
- missing grade renders **Undeclared**;
- a declared grade is explicitly described as metadata that does not establish runtime assurance or substantive evidence sufficiency.

Repository validation blocks known contradictions before publication. The renderer therefore explains the surviving state rather than trying to adjudicate evidence.

## Worked cases

### #1142 — contradictory composition provenance

The three-spec Credential × ZKP × Trust Tasks corpus had independently selected dependency pins while describing itself as `derived-from-pinned-dependencies` and declaring `source-pinned` without a recorded composition review.

The repair:
- changed the provenance mode to independently pinned upstream revisions;
- removed the unsupported grade;
- recorded composition review as pending;
- added positive and negative validator cases.

### #1145 — authority pin without scenario qualification

The standalone ZKP corpus was moved from a downstream-fork archive snapshot to the reviewed upstream specification authority pin. The correction established authority and reproducibility but deliberately did not assign an evidence grade.

### #1147 — complete review with mixed grounding

All 30 legacy ZKP scenarios were reviewed against one immutable specification revision. Thirteen were retained, nine narrowed, and eight remained scenario-baseline hypotheses. Review is complete, but mixed grounding means a corpus-wide `source-pinned` grade would still be an overclaim.

This case is the reason CI-03 exists.

## Reproduction

Run:

```bash
python3 tools/validate_scenario_corpora.py
python3 tools/corpus_status.py --offline
python3 -m unittest discover -s tests -p 'test_corpus_claim_integrity.py' -v
python3 -m unittest discover -s tests -p 'test_corpus_pages_projection.py' -v
```

For live drift/currentness, run `tools/corpus_status.py` without `--offline` in an environment with GitHub access.

## Limitations

Automated claim-integrity checks can identify contradictions recorded in machine-readable metadata. They cannot determine whether:

- a source statement is true or normatively legitimate;
- a semantic adaptation is complete;
- an evidence grade deserves promotion;
- a control works in a live implementation;
- a governance authority is competent or legitimate; or
- a composition is safe merely because its components are individually valid.

Those remain evidence and review questions. A clean claim-integrity result means **no known machine-detectable contradiction at the checked repository state**, not “assurance passed.”
