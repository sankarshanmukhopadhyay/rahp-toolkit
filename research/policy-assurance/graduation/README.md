# Policy-as-Subject Research Review Guide

This directory is the reviewer-facing entry point for the experimental RAHP policy-as-assurance-subject work on branch `research/policy-assurance-subjects-662`.

## What this branch is testing

The research question is whether version-pinned policy and governance documents can be converted into source-preserving, reviewable RAHP assurance subjects while keeping direct source statements, human judgment, RAHP inference, specialist interpretation and runtime evidence visibly separate.

This branch is **not a production release and not a merge request for stable `main`**. Even if the graduation evidence eventually supports a `graduate-candidate` disposition, the intention is to keep the work on this branch for socialisation, external review and feedback before any separate stable-integration decision.

## Canonical links

- Research branch: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/research/policy-assurance-subjects-662
- Research issue #662: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/662
- Graduation evidence tracker #668: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/668
- Draft research PR #667: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/667
- Research documentation: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/docs/research-policy-assurance.md
- Experimental contract: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/method/experimental/policy-subject-v1.yaml
- Graduation protocol: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/research/policy-assurance/graduation/protocol.md
- Corpus register: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/research/policy-assurance/graduation/corpus.yaml
- Reviewer template: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/research/policy-assurance/graduation/reviewer-template.json
- Current graduation decision record: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/research/policy-assurance/graduation/graduation-decision.md
- Graduation metrics implementation: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/tools/policy_graduation_metrics.py

## What to review

A useful review does not require accepting the extraction model. Reviewers should pressure-test whether the branch makes interpretation and uncertainty inspectable.

### 1. Source preservation

Check that a reviewed or inferred proposition can be traced back to exact source material and that source text is not silently rewritten as a finding.

Relevant implementation:
- `tools/policy_subject.py`
- `tools/policy_structure.py`

### 2. Human judgment boundary

Check whether ambiguous propositions remain reviewable and whether accept/amend/reject/split/merge decisions preserve immutable source lineage.

Relevant implementation:
- `tools/policy_review.py`
- `tools/policy_assessment.py`
- `tools/policy_assessment_v2.py`

### 3. Definitions, references and precedence

Check that definitions, cross-section references, incorporated documents and precedence/conflict relationships stay explicit rather than becoming hidden legal interpretation.

Relevant implementation:
- `tools/policy_relationships.py`
- `method/experimental/policy-subject-v1.yaml`

### 4. Risk/harm inference

Check whether RAHP hypotheses are reasonable, traceable and bounded, and whether rejected or unresolved ambiguous propositions are excluded from analytical input.

Relevant implementation:
- `tools/policy_review.py`
- `tools/policy_subject.py`

### 5. Evidence separation

Check that policy text is treated as governance/source evidence, not proof of runtime realization, and that runtime, UX, legal/domain and assurance-evidence routes remain separate.

Relevant implementation:
- `tools/policy_assessment_v2.py`

### 6. Graduation evidence design

Check whether the protocol and metrics are sufficient to answer the practical question: is this capability useful enough, disciplined enough and maintainable enough to become a candidate stable RAHP capability?

Relevant artifacts:
- `protocol.md`
- `corpus.yaml`
- `reviewer-template.json`
- `graduation-decision.md`

## Current corpus

The graduation study uses real public policy/governance surfaces from more than one publisher family, including GitHub policy material, Kubernetes community governance and Apache community conduct material. Source identity, provenance and licensing basis are recorded in `corpus.yaml` and the bounded fixtures under `examples/policy-assurance/real/`.

## Current decision state

The current disposition is **`continue-research` with the branch ready for socialisation and independent reviewer evidence collection**.

That means:
- the research implementation is mature enough to review;
- CI health is necessary evidence but not sufficient evidence of graduation;
- two independent human review records are still required for the graduation study;
- AI-assisted rehearsal must not be represented as independent human review;
- no `graduate-candidate` decision will by itself authorize merging this branch into `main`.

## Feedback that is especially valuable

Please focus feedback on concrete failure modes rather than broad preferences. Particularly useful observations include:

- a proposition that cannot be reconstructed from its cited source span;
- a machine proposition that materially changes legal/governance meaning;
- ambiguity that becomes falsely deterministic;
- a necessary split/merge operation the review model cannot represent;
- a definition/reference/precedence relationship that is silently resolved;
- a risk/harm hypothesis that overreaches the reviewed proposition;
- a missing evidence route or a route that conflates policy with runtime evidence;
- reviewer effort that makes the capability impractical;
- a case where the output is technically traceable but hard for a cold reader to understand.

Feedback can be recorded on the graduation tracker:
https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/668

For implementation-specific discussion, use the draft PR:
https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/667

## Validation

Run the normal repository validation from this branch:

```bash
pip install -r requirements.txt
python3 tools/validate.py
```

The policy research tests are part of repository-wide unittest discovery. A green build shows that the branch is internally coherent; it does not constitute graduation evidence by itself.
