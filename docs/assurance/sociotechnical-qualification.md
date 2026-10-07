# Bounded sociotechnical qualification record

Owner: #913. Disposition: **engineering candidate; independent human review pending**.

## What was established

The opt-in `rahp-sociotechnical/v1` profile reconciles explicitly reviewed assertions through the existing assurance-run state machine. It preserves framing, evidence-class/context admission, declared assessor dependence, conflicting assertions, organizational risk acceptance, affected-party objection, technical repair, remedy obligations and reporting limits.

The implementation does not create a general fairness score or autonomous institutional judgment. It reuses the existing compelled-disclosure and meaningful-choice evaluators, adds conservative evidence admission and reviewed dependence grouping, and fixes the canonical renderer's omission of newer run-state fields.

## Immutable baseline and iteration evidence

- Stable: `v2.6.0`, commit `b18dc9b0acfc8dad36ef9f5b4a5030de38e683f1`.
- Development at commencement: `b5d1381b8ef747ce78c5a5d9cf66b57bb79b41ff`.
- Corpus/coverage commit: `7f4c46ff278c10483feaa1b42a717a51211241b2`.
- Implementation/test commit: `df086113cfdb0abe570e50e8539710ba0fcdf75e`.
- Corpus input hashes and baseline: `examples/sociotechnical-assurance/corpus.json`.
- Machine qualification summary: `sociotechnical-qualification.json` beside this file.

Before implementation, the renderer regression reproduced six dropped dimensions: process state, assurance state, evidence maturity, lenses, required evidence and probe ledger. The corpus and expected outcomes were committed before the profile implementation. The regression is now covered by `tests/test_sociotechnical_record_regression.py`.

## Executed evidence

| Case | Result | What the result supports |
|---|---|---|
| A: harmful intended operation | FAIL | A passing technical proposition does not hide the independently failed disclosure-pressure proposition |
| B: transferred recovery burden | INDETERMINATE | Governance wording does not satisfy required runtime choice evidence |
| C: correlated assessment | FAIL | Correlated positive assertions do not outvote admitted refutation |
| D: context-only change | INDETERMINATE | Unchanged code does not preserve evidence for a changed policy context |
| E: repair without remedy | FAIL | Technical repair and operator closure do not erase a failed remedy proposition |
| F: summary loses scope | INDETERMINATE | Unresolved dispute constrains aggregate assurance; altered maintained output is rejected |
| P: supported bounded control | PASS | Explicitly supported synthetic choice propositions can pass within their declared boundary |
| N: justified non-applicability | NOT_APPLICABLE | Non-applicability needs a reason and supporting evidence |

Local execution passed 25 focused tests, the 482-test Python suite and 60 validator commands selected from the repository validation workflow. Artefact validation retained one pre-existing warning; it reported zero errors. The qualification does not hide that warning or claim strict warning-free validation.

The relevant validators include engine/result compatibility, release verification/qualification, evidence/freshness/delta, governed remediation/retest, architecture, current examples, review readiness, documentation/adoption and generated-reference checks. Python-TypeScript conformance also passed across seven result fixtures, three lifecycle fixtures and three profiles. Generated `build/` remains unchanged. Local execution is attributable to this engineering run, not an independent review.

## Acceptance mapping

| Issue requirement | Evidence / disposition |
|---|---|
| Pinned stable/development baseline and coverage | Coverage matrix, corpus register and this record |
| Six adversarial cases plus controls | Frozen eight-case corpus; deterministic replay and outcome checks |
| Missing/stale/contradictory/insufficient/wrong-class evidence | Focused admission, refutation, unknown and non-applicability tests |
| Harmful intended operation without technical defect | Case A reuses existing disclosure-pressure evaluator with separate passing technical proposition |
| Benefits/burdens and participation basis | Input schema/frame and maintained human report; synthetic/unrepresented actors explicit |
| Dependence and unknown independence | Dependence grouping tests across all five dimensions and unknown-review counterexample |
| Context-only reassessment | Tests change each context field, reject old evidence, change identity and permit explicit renewed support |
| Risk acceptance/agreement/repair/remedy separation | Case E; open/resolved obligation, closure and false-demonstration tests |
| Disagreement and remedy retained in summaries | Canonical projection, direct rendering and tampering regressions |
| Machine/human equivalence | Embedded YAML equals canonical machine record; material facts visible in human sections |
| Relevant regressions and repository checks | Local checks above; GitHub workflow will publish clean-runner replay evidence |
| Cold-reader reproduction and independent review | Guide provided; actual independent human participation pending under #913 |
| Compatibility and historical records | Additive opt-in profile; no normalized result/engine revision change; stable/history untouched |

## Maintainer-facing compatibility and placement judgment

The engineering choice is an opt-in execution profile on the existing extensible assurance-run envelope. Normalized result schema v1, engine-contract revision 1.3 and historical source helper outcomes remain unchanged. Existing canonical renderer consumers receive previously omitted fields when those fields are present; consumers must respect the envelope's extensibility.

The profile is candidate development work until maintainer acceptance and any separately warranted release qualification. This record does not move the stable tag, promote policy-subject research or decide #884's domain-independence hypothesis. A merge may accept the implementation without asserting independent sociotechnical validation or a deployment's effective remedy.

## Residuals and durable ownership

- **#913:** independent human review is pending; no reviewer or affected-party participation is manufactured. Completed review needs a separate attributable packet preserving original judgments.
- **#913:** evidence sufficiency and declared dependence are reviewed assertions. Hidden relationships and unreported external events remain beyond automatic detection. The model preserves these boundaries; metadata is not proof of them.
- **#610:** real DTG cross-boundary remedy remains its own deployment/governance obligation. These synthetic cases do not close it.
- **#662/#667/#668:** policy-subject extraction/graduation remains experimental and separately gated.
- **#884:** domain-independent core research remains separately owned.
- **Maintained reporting only:** RAHP cannot prevent third parties from altering copied summaries or marketing claims outside its validated output path.

Keep #913 open through PR review and acceptance reconciliation. A linked follow-up is not evidence that an unmet core acceptance criterion was satisfied. External review may remain pending only with the qualification claim explicitly bounded as above.
