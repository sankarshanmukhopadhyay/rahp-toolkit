---
layout: default
title: "Identity-to-action boundary coverage"
parent: Run assessments
nav_order: 19
has_toc: true
---
# Identity-to-action boundary: #922 coverage disposition

**Status:** source-pinned gap analysis; no new generic RAHP capability is justified by the current evidence.  
**Repository snapshot:** `sankarshanmukhopadhyay/rahp-toolkit@fa4d7ad0a6522120bdbbf1bdff074353479d3b3d` (main, 7 October 2026). The supplied archive SHA-256 is `b314eeb8d98e95b261e942253d1ce0dae871145e70747eb19451940c85171d9f`. Its Git blob IDs for `examples/README.md`, `tests/test_pages_projection_contract.py`, `docs/assurance/sociotechnical-coverage.md` and `corpora/trust-tasks-credspec-composed.yaml` match the recursive tree for that commit.
**Related work:** [#922](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/922), [#913](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/913), [#252](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/252), [#897](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/897), [#915](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/915).

## Decision

Do not add a parallel schema, control catalogue, scoring mechanism, or six-case corpus at this point. The proposed cases substantially repeat maintained, source-pinned cross-specification scenarios and the #913 sociotechnical corpus. Existing contracts already keep proof, current authority, agreement, service outcome, challenge and remedy as separate propositions or obligations.

The bounded next step is to reuse the existing records and keep the remaining real-world fallback question deployment-specific. A live fallback claim needs evidence from the relevant service and population; synthetic RAHP fixtures cannot establish that it works in practice. If a future deployment examination finds that existing RAHP records cannot represent a concrete fallback or challenge failure, raise that demonstrated case as a narrowly scoped gap.

This is a no-new-code disposition for the generic RAHP Toolkit. It does not close, resolve or promote upstream specification findings in #252, establish deployment approval, or satisfy the independent human review pending in #915.

## Six-case reconciliation

| #922 case | Existing coverage at the pinned snapshot | Disposition |
|---|---|---|
| A. Valid proof, excessive action | [Cross-spec corpus XSP-002, XSP-007, XSP-009, XSP-010, XSP-013, XSP-014, XSP-016, XSP-019 and XSP-020](../../corpora/trust-tasks-credspec-composed.yaml); [authority/outcome seam candidate](../../examples/cross-spec/trust-tasks-credspec/authority-outcome-seam-candidate.yaml) distinguishes credential proof from scoped, current action authority and outcome. | Covered as a cross-spec assessment proposition. The domain-specific findings remain with #252 and upstream owners. |
| B. Valid proof, coerced or absent agreement | [Sociotechnical case B](../../examples/sociotechnical-assurance/B-transferred-recovery-burden.json) and [case A](../../examples/sociotechnical-assurance/A-harmful-intended-operation.json); tests `test_correct_technical_control_cannot_hide_compelled_disclosure` and `test_policy_assertion_does_not_establish_runtime_choice` in [the profile tests](../../tests/test_sociotechnical_assurance.py). | Covered at the synthetic model/evidence-contract level. These fixtures do not establish real consent or affected-party agreement. |
| C. Lifecycle skew | Cross-spec XSP-007, XSP-009, XSP-013, XSP-016 and XSP-019; [sociotechnical case D](../../examples/sociotechnical-assurance/D-context-only-change.json); test `test_each_context_change_invalidates_old_evidence_and_identity`. | Covered for source/context freshness and modeled lifecycle divergence. External changes remain observable only within declared monitoring limits. |
| D. Over-disclosure or correlation | Cross-spec XSP-005, XSP-006, XSP-011, XSP-018 and XSP-020; [#252 F-003](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/252) deliberately keeps privacy and non-inference distinct from the authority result. The sociotechnical profile also preserves specialist referral as unresolved evidence. | Existing privacy composition and handoff cover the generic assurance boundary. Concrete disclosure behavior still needs deployment evidence and DPIP where warranted. |
| E. Access-path failure | [case A](../../examples/sociotechnical-assurance/A-harmful-intended-operation.json) and [case B](../../examples/sociotechnical-assurance/B-transferred-recovery-burden.json), whose frame records device loss, alternatives, transferred recovery burden and coverage limits; the existing meaningful-choice evaluator and corpus cover failure to establish meaningful refusal/recovery choice. | Partially covered. The fixtures model the risk; they do not execute or prove that a real fallback path is usable under outage, disability, device loss or other stated conditions. This remains a deployment-level evidence need. |
| F. Challenge and recovery failure | [Sociotechnical case E](../../examples/sociotechnical-assurance/E-repair-without-remedy.json) and [case F](../../examples/sociotechnical-assurance/F-summary-loses-scope.json); tests `test_repair_and_operator_closure_do_not_resolve_human_remedy`, `test_false_challenge_demonstration_is_not_positive_support`, and `test_human_record_embeds_exact_machine_record_and_visible_obligations`. Cross-spec XSP-012 and #252 F-003 cover cross-boundary redress. | Covered as a modeled obligation and reporting boundary; actual remedy remains external and must be evidenced by the accountable deployment. |

## Authority and interpretation boundary

The #913 opt-in `rahp-sociotechnical/v1` profile already supports reviewed propositions, explicit required evidence classes, source/context pins, current/stale/unknown evidence, disagreements, technical-repair and human-remedy obligations, challenge-route evidence and bounded aggregate reporting. Its eight-case corpus distinguishes expected FAIL and INDETERMINATE results from positive PASS and justified NOT_APPLICABLE; those outcomes are not deployment approvals.

The [cross-spec assessment](../../examples/cross-spec/trust-tasks-credspec/README.md) and [candidate decision profile](../../examples/cross-spec/trust-tasks-credspec/authority-outcome-seam-candidate.yaml) already articulate the central non-inference: valid proof is not current action authority, and confirmed authority is not evidence of execution or outcome. The candidate remains exploratory and records residual gates. This report does not promote it or decide its open findings.

## Verification performed

- Repository validator: `python3 tools/validate.py --summary` — **0 errors, 2 warnings**.
- Full unit suite attempted — **not verifiable in this runtime**: `jsonschema` is absent. The attempted dependency installation could not reach the configured package index. Test failures arising from unavailable dependencies are environment blockers, not attributed to the repository.
- Static coverage inspection used the pinned repository files and the existing recorded evidence above. No new case expected outcomes were invented and no implementation behavior was changed.

To rerun in a provisioned environment, follow [CONTRIBUTING.md](../../CONTRIBUTING.md), install `requirements.txt`, then run:

```bash
python3 -m unittest discover -s tests -p 'test_sociotechnical*.py'
python3 -m unittest discover -s tests -p 'test_authority_outcome_seam_candidate.py'
python3 tools/validate.py --summary
python3 tools/build.py
python3 tools/validate_reference_links.py
```

## Residual limitations

- #913 independent human review remains pending under #915.
- No affected-party participation or live service fallback test is present in this analysis.
- The cross-spec examples are scoped to their pinned specifications and do not establish a universal identity or authorization model.
- No stable release, external specification, policy decision or deployment outcome is changed by this disposition.

## Closure recommendation for #922

Close #922 as **completed by evidence-backed no-change disposition** after review of this mapping. Reopen or file a successor only when a concrete case demonstrates a generic RAHP representation/enforcement gap; otherwise place the fallback, consent and redress evidence in the responsible deployment or upstream assessment.

## Acceptance-criteria reconciliation

Status is assessed against the #922 wording. “Done” means the evidence exists in the cited maintained work; it does not mean a new #922-specific experiment occurred.

| Criterion | Status | Evidence and boundary |
|---|---|---|
| Stable and development baselines are distinguished and source-pinned. | **Done** | The repository snapshot and archive digest are pinned above. #913 records the stable v2.6.0 and development baselines and their comparison. This disposition adds no runtime changes. |
| Coverage matrix maps each in-scope proposition to contract, implementation, tests/evidence and limits. | **Partial** | The six-case reconciliation maps existing evidence and limits. The source-pinned #913/#252 artifacts provide the underlying implementation and tests, but this report is not a complete per-proposition contract-to-implementation-to-test matrix. |
| Existing issue ownership is reconciled; duplicate work is linked or removed from scope. | **Done** | #913, #252, #897 and #915 are linked and their ownership boundaries are stated above. No parallel schema, corpus or upstream finding is created. |
| No more than six synthetic cases have predetermined expected outcomes before candidate replay. | **Not done for #922** | No #922-specific case set was frozen and replayed. Existing #913/#252 cases were inspected and reused as evidence; they were not relabeled as a newly frozen #922 corpus. |
| Valid proof does not silently establish broader authority, consent, service outcome or remedy. | **Done in existing evidence; no new #922 replay** | The cited cross-spec and sociotechnical cases/tests preserve these distinctions. The claim is limited to the maintained modeled contracts and outputs. |
| Stale, revoked, out-of-scope or insufficient evidence cannot silently establish current action authority. | **Done in existing evidence; no new #922 replay** | The cross-spec lifecycle cases and #913 freshness/context tests exercise these boundaries. External state is bounded by declared monitoring and evidence limits. |
| Disclosure/correlation, access fallback and challenge/recovery limits remain visible where exercised. | **Partial** | Privacy composition and challenge/remedy limits are represented in existing evidence. Fallback risks and limitations are modeled, but a live service path was not exercised; its usability remains deployment evidence. |
| Positive/NOT_APPLICABLE outcomes are used only where justified by explicit evidence and scope. | **Done in #913 evidence; no new #922 replay** | The #913 frozen corpus includes bounded PASS and justified NOT_APPLICABLE controls alongside FAIL/INDETERMINATE cases. This disposition creates no new expected outcomes. |
| Any model gap remains explicit; no unsupported schema coercion or universal pass/fail claim is introduced. | **Done** | The report retains the deployment-level fallback and independent-review limits and introduces no schema/runtime behavior or universal rule. |
| Every code or contract change is tied to a failing case, has regression evidence, and includes compatibility analysis. | **N/A — no code/contract change** | PR #923 changed documentation only. No implementation or contract change was proposed. |
| Machine and human qualification outputs retain material scope, adverse findings and evidence limitations. | **Done in existing #913 evidence; no new #922 replay** | Existing #913 reporting tests/corpus are the evidence. PR #923 adds a human-readable disposition; no machine output changed. |
| Reproducible evidence bundle and bounded qualification/no-change report are available. | **Partial** | This source-pinned report and the existing CI/replay records are available. There is no dedicated #922 six-case input/output bundle, environment capture or replay artifact. |
| No claim of independent review, affected-party participation, real-world prevalence, or realized remedy is made without attributable evidence. | **Done** | The report explicitly disclaims independent review, affected-party participation, live fallback effectiveness, deployment approval and realized remedy. |

### Overall completion

The bounded **no-change gap analysis and documentation deliverable are complete**. The #922 acceptance criteria are **not all complete**: the new six-case freeze/replay and a dedicated reproducible #922 evidence bundle were not produced, while fallback effectiveness remains deployment-specific and the full mapping is partial. Existing #913/#252 evidence supports the documented no-change decision, but it must not be presented as a #922-specific replay. Keep the issue closed as a completed bounded analysis only if that narrower completion definition is acceptable; reopen it if strict satisfaction of every original acceptance criterion is required.


## Bounded replay using the existing frozen cases

This section updates the earlier acceptance-criteria reconciliation. It uses existing #913 and #252 evidence as permitted by #922; it does **not** create or claim a new #922 corpus.

### Pinned run and artifacts

- Source commit evaluated: `baa9b9d3bbb816791b8b476d8d5cc6bf7fce768d` (main; code baseline matching the supplied archive at `fa4d7ad0a6522120bdbbf1bdff074353479d3b3d`; intervening commits for this run were documentation-only).
- Sociotechnical corpus pins: stable `v2.6.0` / `b18dc9b0acfc8dad36ef9f5b4a5030de38e683f1`, development `b5d1381b8ef747ce78c5a5d9cf66b57bb79b41ff`, engine contract `rahp-engine-contract-v1 revision 1.3`, result schema 1.
- CI run: [#37639525853](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/actions/runs/37639525853). The workflow installed `requirements.txt`, ran `python3 -m unittest discover -s tests -p 'test_*.py'`, and replayed `python3 tools/sociotechnical_assurance.py --corpus examples/sociotechnical-assurance/corpus.json --output-dir "$RUNNER_TEMP/rahp-sociotechnical-evidence"`. All relevant CI jobs succeeded.
- Replay artifact: `rahp-sociotechnical-evidence`, artifact ID `11491511267`, GitHub SHA-256 `480e0d15342d80cf6af7b404c162d366fc054bb1d9bac23760c45d5c9014f547`. It contains JSON and human-readable outputs for all eight corpus entries. The downloaded archive independently hashed to the same digest. GitHub artifact retention currently expires 5 January 2027.
- The supplied archive's local validator reports 0 errors and 2 warnings. The focused local unittest command could not import `jsonschema`; the pinned CI run installed project requirements and passed the full unittest discovery and corpus replay.

The #913 corpus records six bounded adversarial cases with expected outcomes and input digests before implementation, plus a positive and a NOT_APPLICABLE control. The replay outputs match those expected results:

| #922 proposition | Reused frozen case(s) and relevant maintained contract/tests | Replayed result | What this establishes and limit |
|---|---|---|---|
| A. Proof versus current, scoped action authority and outcome | #252 XSP-002/007/009/013/016/019; [authority/outcome candidate](../../examples/cross-spec/trust-tasks-credspec/authority-outcome-seam-candidate.yaml); tests `test_authority_and_outcome_are_bounded_tri_state_decisions` and `test_missing_or_conflicting_evidence_cannot_silently_confirm_authority`. The entire XSP-001–020 coverage map is checked by the candidate test suite. | Full pinned unittest suite passed. The XSP records are source-pinned assessment scenarios; they do not have a separate per-scenario runtime outcome artifact in this replay. | The exploratory contract keeps proof, authority and outcome separate and missing/conflicting evidence unresolved. Open #252 findings and candidate retest gates remain unresolved; this is not upstream closure. |
| B. Coerced or absent agreement; access and recovery burden | Cases [A harmful intended operation](../../examples/sociotechnical-assurance/A-harmful-intended-operation.json) and [B transferred recovery burden](../../examples/sociotechnical-assurance/B-transferred-recovery-burden.json); tests `test_correct_technical_control_cannot_hide_compelled_disclosure` and `test_policy_assertion_does_not_establish_runtime_choice`. | A **FAIL**; B **INDETERMINATE**. | The profile does not infer agreement from a technical control or policy assertion. Case B models transferred recovery burden; neither case tests a live service fallback. |
| C. Lifecycle skew and stale evidence | [Case D context-only change](../../examples/sociotechnical-assurance/D-context-only-change.json); tests `test_each_context_change_invalidates_old_evidence_and_identity` and `test_stale_insufficient_unknown_and_wrong_pin_never_pass`; #252 XSP-002/007/009/013/016/019. | D **INDETERMINATE**; mutation tests passed in the full suite. | Changed context invalidates old evidence/identity and stale or insufficient evidence cannot produce PASS in the modeled profile. External changes remain subject to monitoring limits. |
| D. Disclosure composition and cross-context correlation | [Case C correlated assessment](../../examples/sociotechnical-assurance/C-correlated-assessment.json); candidate test `test_privacy_and_redress_are_not_folded_into_authority`; #252 XSP-005/006/011/018/020. | C **FAIL**; correlated-source and contradiction tests passed. | Correlated support cannot outvote a supplied refutation; privacy remains outside the authority result. Concrete deployment disclosure and linkability still need deployment evidence. |
| E. Credential/device/access-path failure and fallback | [Case B transferred recovery burden](../../examples/sociotechnical-assurance/B-transferred-recovery-burden.json); meaningful-choice evaluator and case B test. | B **INDETERMINATE**. | The evidence does not establish meaningful recovery choice for the modeled case. No live fallback path, outage, accessibility or population test was run; this remains deployment-specific. |
| F. Challenge, correction, recovery and remedy | [Case E repair without remedy](../../examples/sociotechnical-assurance/E-repair-without-remedy.json) and [case F summary loses scope](../../examples/sociotechnical-assurance/F-summary-loses-scope.json); tests `test_repair_and_operator_closure_do_not_resolve_human_remedy`, `test_open_remedy_blocks_aggregate_pass_even_after_supported_repair`, and `test_human_record_embeds_exact_machine_record_and_visible_obligations`. | E **FAIL**; F **INDETERMINATE**. | Technical repair does not resolve human remedy; unresolved disagreement remains visible in the aggregate. Actual remedy effectiveness remains external. |
| Positive control and justified NOT_APPLICABLE control | [P supported bounded control](../../examples/sociotechnical-assurance/P-supported-bounded-control.json); [N justified non-applicability](../../examples/sociotechnical-assurance/N-justified-non-applicability.json); positive/NA tests in the profile suite. | P **PASS**; N **NOT_APPLICABLE**. | These are proposition- and scope-bounded outcomes, not deployment approvals. |

### Decision and revised acceptance status

The existing cases and tests are sufficient for the **bounded generic RAHP question**: they preserve the distinctions, fail closed where evidence is missing or contradictory, and keep scope, adverse findings and remedy obligations visible. The replay found no generic representation or reporting defect that warrants new cases or code. The live fallback question is a deployment evidence gap, not something a synthetic RAHP case can settle. Add a new case only if a concrete deployment or upstream input exposes a specific, currently unrepresented failure.

This replay closes the earlier evidence gaps as follows: the six-case requirement is met by reusing the six predeclared #913 adversarial cases, with P/N controls; the coverage matrix above maps each proposition to contracts, tests/evidence and limits; and the reproducible outputs are available in the pinned CI artifact. The checklist items are therefore now **Done: 1–9, 11–13; N/A: 10**. “Done” is bounded to the generic modeled/toolkit scope and does not claim live fallback effectiveness, independent human review, affected-party participation, universal identity/authorization semantics, or resolution of #252 upstream findings.
