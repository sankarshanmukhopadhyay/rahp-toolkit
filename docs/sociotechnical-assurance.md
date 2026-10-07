---
layout: default
title: "Adversarial sociotechnical assessment"
parent: Run assessments
nav_order: 18
---
# Adversarial sociotechnical assessment

The opt-in `rahp-sociotechnical/v1` profile reconciles explicitly authored propositions and reviewed assertions about access, human choice, transferred burdens, institutional context and remedy. It uses the existing assurance-run state machine and terminal renderer. It does not infer that technical conformance establishes a beneficial deployment.

This is an additive candidate capability developed under #913. The v2.6.0 stable tag and historical qualification remain unchanged. Policy-subject extraction under #662/#667/#668 remains separate research. Domain-independent architecture research under #884 is not decided by these fixtures.

## Run a bounded assessment

Install the existing dependencies, then run from the repository root:

```bash
pip install -r requirements.txt
python3 tools/sociotechnical_assurance.py --input examples/sociotechnical-assurance/A-harmful-intended-operation.json > /tmp/rahp-sociotechnical.json
python3 tools/assurance_record.py /tmp/rahp-sociotechnical.json
```

Replay the frozen eight-case corpus and emit machine and human evidence:

```bash
python3 tools/sociotechnical_assurance.py --corpus examples/sociotechnical-assurance/corpus.json --output-dir /tmp/rahp-sociotechnical-evidence
python3 -m unittest discover -s tests -p 'test_sociotechnical*.py'
```

A zero exit code for corpus replay means expected outcomes matched, including expected FAIL and INDETERMINATE cases. It is not a deployment assurance PASS. The replay checks canonical input digests against the pre-implementation corpus register. Changing a fixture requires an explicit corpus revision; do not rewrite expected outcomes simply to obtain green execution.

## Supply evidence and judgment explicitly

The input contract is [`rahp-sociotechnical-input-v1.schema.json`](../schemas/rahp-sociotechnical-input-v1.schema.json). Start with a copy of a worked input and remove the corpus-only `case_id` and `expected_outcome` fields for ordinary use.

The profile requires purpose, scope/non-scope, actors and participation basis, scenario sources, coverage limits, alternatives, assumptions, control beneficiary/burden bearer and context-observation limits. Generated personas are synthetic constructs, not affected-party participation.

Each proposition names required evidence classes and whether independent corroboration is required. Evidence must reference the proposition, a declared source pin, matching producer revision and exact context digest. Stale, insufficient, unknown, wrong-context and wrong-class assertions are retained as rejected evidence. They cannot silently support PASS. Supplied relevant evidence cannot be hidden by removing its proposition reference.

`adjudicated` propositions evaluate reviewed support/refutation; the other supported evaluator types reuse existing compelled-disclosure and meaningful-choice invariants. The admission flag `sufficient` records reviewer judgment rather than independently proving it. For these evaluators the reviewer must establish that admitted assertions support the complete fact set. A material privacy-depth referral remains evidence-required; this profile does not fabricate a specialist return.

Refutation has precedence over positive support within the admitted proposition scope. Outcome aggregation does not vote or average confidence. Missing required evidence produces INDETERMINATE. NOT_APPLICABLE requires a non-empty reason and admitted supporting evidence. A mixed set of PASS and justified NOT_APPLICABLE can yield a bounded PASS; open disagreements or remedy obligations prevent that aggregate conclusion.

## Independence is a proposition

When independent corroboration is required, the profile requires reviewed dependence metadata and at least two disjoint source groups supporting each required evidence class. Shared control, maintainers, corpus, model/prompt lineage or fixtures conservatively joins assessors into one group, including transitive relationships. Unknown independence is not counted as established independence.

Dependence declarations and their review basis remain inspectable. Distinct identifiers, repositories or model runs do not establish independence. This is a conservative grouping rule over reviewed declarations, not a detector of undisclosed relationships. Independent human validation is separately pending: synthetic reviewers and verified fixture declarations are not actual independent people.

The legacy `evaluate_external_trust_sources` helper checks integrity, freshness and source multiplicity. Its historical output remains compatible, but it must not be used as proof of sociotechnical independence. Use this opt-in profile for that stronger claim.

## Context and remedy

The context snapshot names policy, ownership, access conditions, population and remedy arrangements. Its digest is part of subject identity and evidence admission. A changed context creates a new assessment identity and records lineage. Prior evidence cannot inherit support until its applicability to the new snapshot is explicitly established. Unreported external changes cannot be detected automatically; observation limits remain in the frame.

Organizational risk acceptance, affected-party agreement/objection, technical repair, human remedy and work-item state are separate records. Open obligations remain open despite an operator waiver or a closed issue. A resolved label without admitted, supporting evidence and a supported proposition remains unresolved. The challenge route records account independence and evidence; a false demonstration remains an unresolved qualification.

The profile does not create a real deployment challenge route. A positive synthetic control assessment is not proof that an affected person has obtained remedy. Deployment-specific closure remains with its accountable owner, including #610 where applicable.

## Maintained reporting boundary

The canonical renderer preserves process state, assurance state, evidence maturity, lens dispositions, required evidence and probe ledger, in addition to the opt-in profile. The profile record binds its complete input, derived dispositions and framing to assessment identity. Canonical projection and direct Markdown rendering reject altered/omitted material profile facts.

Human output exposes scope, actors, control burdens, dependence, rejected evidence, authority, disagreement and remedy, and embeds the same canonical machine record. It always states that deployment approval is not inferred. RAHP cannot prevent a downstream party from editing a copied report or misrepresenting a badge; consumers should retain the evidence-bound record and verify its immutable source.

## Review packet

Use the [cold-reader guide](assurance/sociotechnical-reviewer-guide.md), [initial coverage matrix](assurance/sociotechnical-coverage.md) and [qualification record](assurance/sociotechnical-qualification.md). Actual independent reviewers should supply separate attributable decisions and disagreements. The execution input cannot self-award independent human validation with a flag.


## Related boundary assessment

The follow-on review of identity proof, action authority and recourse found substantial coverage in this profile and the existing cross-specification assessment. See the [identity-to-action boundary coverage disposition](assurance/identity-action-boundary-disposition.md) for the source-pinned mapping, residual live-deployment evidence limits and no-new-code recommendation.
