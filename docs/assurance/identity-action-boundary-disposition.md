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
