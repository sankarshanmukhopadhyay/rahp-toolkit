---
layout: default
title: "Undeclared corpus evidence-grade assessment"
parent: "Scenario corpora"
has_toc: true
nav_exclude: true
---
# Assessment of five undeclared corpus evidence grades

**Review date:** 2026-10-20. **Tracker:** [#1079](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1079). **Source of truth:** the five `corpora/*.yaml` adapters and the registry `corpora/sources.yaml` at the revision of this document. This records a provenance decision, **not** a runtime assurance claim, conformance result, or safety assessment. A grade is not inferred from the title or description of an adapter.

| Corpus | Observed provenance | Grade disposition | Reason / limitation |
|---|---|---|---|
| [DTG ZKP](../corpora/dtg-zkp/) | `source_commit: cfd94063e5cfee7ba6df4dcfd28c10399a0ffd0a`; `provenance_status: authoritative-source-pinned-scenario-review-pending` | **Not declared; retain semantic requalification complete; mixed grounding** | #782 established the immutable upstream specification authority pin and #1147 requalified all 30 legacy UC-* mappings. Thirteen are retained, nine revised and eight remain scenario-baseline hypotheses. Mixed grounding does not justify a corpus-wide `source-pinned` grade. |
| [Trust Tasks](../corpora/trust-tasks/) | 40-character SHA `4937c70df95e56ed6404b8c004106ecb121a23cf`, scenario source anchors, `provenance_status: source-pinned` and an August 23 review note | **Not declared; retain pending grade authorization** | The adapter records a reviewed immutable revision, but the current metadata does not explicitly authorize `evidence_grade: source-pinned`. The reviewer should confirm that the evidence-grade classification criteria and source-span completeness are met before adding the separate field. |
| [Credential Specification](../corpora/credential-spec/) | SHA `b89f389abbdae77ba60b673c0836c781c2b54169`, scenario source anchors, `provenance_status: source-pinned` and August 23 review note | **Not declared; retain pending grade authorization** | A strong pin is present. Grade assignment is still a distinct reviewed classification; `provenance_status` does not automatically become an evidence grade. |
| [CAWG/C2PA](../corpora/cawg/) | `source_commit: multi-source-snapshot-2026-08-14`; multiple specifications represented | **Not declared; retain** | The symbolic date does not identify a checked set of immutable revisions for each relevant source. No complete portfolio baseline is established by this adapter. |
| [Trust Tasks × CredSpec](../corpora/trust-tasks-credspec-composed/) | `source_commit: derived-from-pinned-dependencies`; explicit `depends_on` source pins and recomposition note | **Not declared; retain pending composition evidence** | The two parent baselines are pinned, but a composed claim needs its own review of cross-specification anchors and derivation. No grade is inherited transitively from either parent. |

## Post-assessment authority update

On 2026-10-25, #1145 corrected the DTG ZKP source authority to the upstream specification/conformance repository using the reviewed #782 pin. The subsequent #1147 semantic requalification is complete, but the grade decision remains **Not declared** because eight retained UC-* rows are still scenario-baseline hypotheses rather than source-grounded constructions or requirements. See [DTG ZKP corpus authority rebaseline](dtg-zkp-corpus-authority-rebaseline.md) and [DTG ZKP legacy-scenario semantic requalification](dtg-zkp-scenario-requalification.md).

## Reproducibility and boundaries

Use the repository's [corpus provenance workflow](corpus-synchronization.md) to review sources and pins and run `python3 tools/validate_scenario_corpora.py`. Source-pinned cases record grounding in a reviewed revision, not the result of exercising a scenario against an implementation. For any claimed grade change, record the reviewer, reviewed source spans, immutable revisions, adaptation rule, and any composition-specific reasoning; update the adapter through a separate source-grounded PR.

The [corpora browser](../corpora/) and generated per-corpus pages deliberately display **Not declared** until the canonical `evidence_grade` field is set. This is accurate disclosure, not a defect for the renderer to repair.

## Outcome

No five-grade bulk promotion is justified by the inspected metadata alone. This assessment resolves the classification question at the current source baseline: the explicit current decision is to **retain all five as Not declared** and preserve specific evidence requirements for any future promotion. It does not block using these corpora as test-question collections, provided they are not presented as independently assured. This decision should be revisited if source-pinned evidence and accountable review substantiate a grade.
