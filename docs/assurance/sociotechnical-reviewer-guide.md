# Sociotechnical cold-reader exercise

Engineering provenance: #913 / #914. Independent-review owner: #915. Independent human review: **pending**. This packet is prepared for review; no reviewer participation or affected-party research is claimed.

1. Record the candidate commit SHA, runtime and dependency versions. Read the frozen corpus register and baseline coverage before running the implementation.
2. Choose cases A, C, D and E first. Without consulting generated results, record the proposition, affected actor, admissible evidence class, adverse/contradictory evidence, expected inference and outstanding obligation.
3. Run the replay command in `docs/sociotechnical-assurance.md`. Compare your original judgments with the terminal machine record and the human summary.
4. Inspect case F and remove a material qualification from a copy of its result. Confirm the maintained renderer rejects it. Do not change the authoritative corpus to match a preferred outcome.
5. Examine the positive and NOT_APPLICABLE controls. Determine whether their positive conclusion is correctly limited to reviewed synthetic assertions.
6. Challenge a declared dependence relationship and one evidence-sufficiency judgment. Record whether your objection changes the inference, exposes missing evidence or indicates a method/model gap.

Use this decision template in a separate attributable review artifact:

```yaml
candidate_sha: <exact commit>
reviewer: <attributable identity or governed identifier>
review_basis: <independence and expertise; material relationships>
case: <corpus case>
original_expected_outcome: <record before seeing generated result>
decision: accept | amend | reject | judgment-required
proposition: <identifier>
evidence_refs: []
rationale: <why the evidence supports or contradicts the conclusion>
unresolved_disagreement: <specific question, or none>
requested_action: <bounded change or evidence requirement>
```

Preserve the original reviewer artifact and its digest. Reconciliation should reference it rather than overwrite it. A second AI pass or same-author pass is internal checking, not independent human validation. Do not collect identifying affected-party narratives into public GitHub records; this corpus requires none.

The reviewer should be able to answer: who bears the harm, which assertion could be wrong, what evidence would falsify it, who can disposition the finding, and what remains unresolved after technical repair?
