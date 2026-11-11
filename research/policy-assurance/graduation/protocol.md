# Policy-as-subject graduation evidence protocol

Status: experimental research protocol  
Tracker: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/668  
Parent research issue: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/662  
Implementation vehicle: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/667  
Candidate branch: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/tree/research/policy-assurance-subjects-662

Reviewer guide: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/blob/research/policy-assurance-subjects-662/research/policy-assurance/graduation/README.md

## Decision boundary

This exercise asks whether the policy-as-assurance-subject capability has enough evidence to be described as a candidate for stable RAHP adoption.

A positive disposition is **not merge authorization**. Even a `graduate-candidate` or `bounded-graduate-candidate` result remains on the research branch for socialisation, external feedback and further review. Any later stable integration must be a separate explicit decision and work item.

## Fixed-candidate rule

The measured candidate is frozen before reviewer scoring. Extraction/classification rules MUST NOT be tuned in response to reviewer disagreement during the scoring round. Defects are logged separately and may be fixed only after the measured round, creating a new candidate baseline.

Candidate implementation fields are recorded in `corpus.yaml` and the final evidence report.

## Corpus design

The target graduation corpus contains five materially different policy surfaces:

1. terms/contractual service policy;
2. privacy/data-handling policy;
3. acceptable-use/community policy;
4. appeal/enforcement/redress policy;
5. materially different governance or operating policy.

At least two target items SHOULD come from unrelated publishers/organizations. Source URI, source version/ref, retrieval date, local assessment digest and licensing/retention basis MUST be recorded separately.

A rehearsal may use synthetic or same-publisher fixtures, but such a rehearsal MUST NOT be represented as satisfying the external-corpus graduation gate.

## Reviewer protocol

Two independent human reviewers are the target graduation evidence source. Reviewer B must not see Reviewer A's proposition dispositions before submitting their own record.

Allowed proposition dispositions:

- `accept`
- `amend`
- `reject`
- `split`
- `merge`
- `judgment-required`
- `specialist-route`

Material amendment, rejection, split, merge, reference reclassification or precedence resolution requires rationale.

Reviewer records are immutable study evidence. Reconciliation creates a new record and MUST NOT overwrite either original review.

AI/model-assisted review may be used as a **rehearsal** or proposal generator, but MUST be labelled `reviewer_class: ai-assisted-rehearsal`; it does not satisfy the independent-human-review graduation gate.

## Per-proposition measures

For each extracted proposition record:

- disposition;
- reviewer rationale where required;
- proposition type agreement/disagreement;
- whether actor/object/trigger/consequence/temporal/affected-party candidates were useful;
- whether ambiguity was correctly exposed;
- whether legal/domain specialist routing was appropriate;
- whether source lineage remained sufficient to reconstruct the reviewed meaning.

## Corpus-level measures

### Extraction usefulness

`useful = accept + amend + split + merge`

Report counts and percentages separately. Do not collapse amendments into clean accepts.

Engineering signal thresholds for discussion, not universal truth:

- useful propositions >= 80%;
- outright reject <= 10%;
- 100% source-lineage preservation;
- zero unreviewed ambiguous propositions entering RAHP inference.

### Review burden

Record:

- proposition count;
- count requiring intervention;
- material rewrites;
- split/merge count;
- specialist-route count;
- reviewer-reported effort where available.

### Reviewer agreement

Compare reviewers on:

- disposition;
- proposition type;
- material ambiguity;
- high-materiality actor/consequence interpretation;
- incorporation/reference relationship;
- precedence/definition conflicts.

Agreement on high-materiality propositions matters more than raw agreement on low-impact text.

### RAHP hypothesis usefulness

Each hypothesis is classified:

- `useful-supported`;
- `useful-deployment-dependent`;
- `duplicate-or-low-value`;
- `unsupported`;
- `wrong-pattern`;
- `specialist-required`.

Every retained hypothesis must preserve reviewed-proposition lineage and explicit inference boundaries.

### Evidence-work-queue usefulness

Each work item is classified:

- `actionable`;
- `relevant-too-generic`;
- `unnecessary`;
- `wrong-route`;
- `missing-companion-question`.

## Runtime composition case

At least one reviewed policy proposition is compared with separately supplied `runtime-observation` evidence.

Required invariant:

```text
policy source
  -> reviewed proposition
  -> runtime observation
  -> CONSISTENT | MISMATCH | INDETERMINATE
  -> non-terminal evidence obligation/residual
```

Policy text itself MUST NOT be accepted as runtime evidence.

## Policy-version case

At least one policy pair is assessed as two immutable source versions. Reviewers answer `what changed that matters?` independently of the machine delta. Reconciliation compares:

- added/removed/changed propositions;
- new/expanded powers;
- removed/narrowed safeguards;
- changed retention/disclosure/redress;
- findings unaffected;
- findings requiring reassessment;
- new hypotheses.

## Graduation gates

The final evidence report makes an explicit judgment against five gates:

1. **Utility** — propositions are consistently useful after review.
2. **Assurance value** — reviewed propositions yield meaningful risk/harm and evidence questions.
3. **Judgment discipline** — ambiguity, legal/domain interpretation and uncertainty remain visible.
4. **Operational cost** — reviewer burden is proportionate to value.
5. **Architecture fit** — policy remains an adapter/research layer and does not weaken stable RAHP evidence/terminal semantics.

## Allowed final dispositions

- `graduate-candidate`
- `bounded-graduate-candidate`
- `continue-research`
- `do-not-graduate`

A positive result means **socialise and seek feedback on the branch**. It does not authorize merging https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/667 into `main`.

## Evidence completeness states

The report MUST distinguish:

- `MEASURED` — directly supported by study records;
- `REHEARSAL` — AI/model or synthetic exercise, useful but not the required human evidence;
- `MISSING` — required evidence not yet collected;
- `JUDGMENT` — explicit reviewer/maintainer conclusion based on cited evidence.
