# Policy-as-subject graduation evidence decision

Tracker: #668  
Parent research: #662  
Implementation PR: #667 (draft)  
Measured implementation SHA: `0c29f9226a44bc3c0efbd0213a46d2c4b6fb66ce`

## Current disposition

**`continue-research` — with the implementation considered ready for socialisation and independent reviewer evidence collection.**

This is a graduation-study decision, not a statement that the implementation is incomplete. The engineering research vehicle is substantially complete and green. What remains is evidence about usefulness, reviewer burden and judgment stability from independent humans applying the fixed candidate to the registered corpus.

A future `graduate-candidate` or `bounded-graduate-candidate` decision will still **not authorize merging #667 into `main`**. Positive graduation evidence should first be socialised on the research branch, external feedback sought, and only then should a separate stable-integration decision be considered.

## Evidence register

| Evidence | State | Observation |
|---|---|---|
| Source-preserving ingestion | MEASURED | Existing research tests and real-policy pressure tests preserve source spans, hashes and source identity. |
| Real-policy structure | MEASURED | GitHub terms/AUP/appeal plus external Kubernetes and Apache policy/governance surfaces are registered. |
| Publisher diversity | MEASURED | Corpus spans GitHub, Kubernetes Community and Apache Software Foundation. |
| Definition/reference/incorporation boundary | MEASURED | Candidate semantics preserve definitions/references as reviewable relationships and do not silently traverse links. |
| Split/merge/reject review lineage | MEASURED | Review implementation preserves machine proposal and source parents; rejected/unresolved ambiguous propositions do not enter reviewed RAHP analysis. |
| Stable RAHP isolation | MEASURED | Research capability remains outside the stable controller and terminal semantics. |
| Independent human Reviewer A | MISSING | Required study evidence has not yet been collected. |
| Independent human Reviewer B | MISSING | Required study evidence has not yet been collected. |
| Human disagreement/reconciliation metrics | MISSING | Depends on the two immutable reviewer records. |
| Reviewer effort/burden | MISSING | Requires measured human review effort. |
| Hypothesis usefulness scoring by humans | MISSING | Existing tests establish behavior, not human usefulness. |
| Evidence-work-queue usefulness scoring by humans | MISSING | Existing tests establish routing, not practical usefulness. |
| Policy-versus-runtime graduation case | PARTIAL | Runtime evidence-class separation is implemented/tested; a measured graduation-study case still needs reviewer scoring. |
| Policy-version graduation case | PARTIAL | Delta/reassessment is implemented/tested; a measured “what changed that matters?” comparison still needs reviewer scoring. |

## Gate judgment

### 1. Utility

**State: MISSING human evidence.**

The implementation can produce reviewable propositions across materially different documents, but graduation requires measured accept/amend/reject/split/merge outcomes from independent human reviewers. Engineering tests cannot establish that the proposition set is worth the review cost.

### 2. Assurance value

**State: PARTIAL.**

Bounded RAHP risk hypotheses and evidence work queues are traceable and non-terminal. Human scoring is still required to establish whether they are consistently useful, material and actionable rather than merely well-formed.

### 3. Judgment discipline

**State: MEASURED / strong.**

The research path visibly separates source text, reviewed propositions, RAHP inference and runtime evidence. Ambiguous propositions remain judgment-required; legal/domain interpretation and precedence resolution do not become hidden automatic facts. AI-assisted review is explicitly barred from satisfying the independent-human graduation gate.

### 4. Operational cost

**State: MISSING human evidence.**

No defensible conclusion can yet be made about reviewer burden, amendment rate or time-to-review.

### 5. Architecture fit

**State: MEASURED / strong.**

The capability remains additive and experimental. Stable controller, engine contract and terminal semantics remain untouched. The candidate is suitable for branch-level socialisation without implying production support.

## Why the current decision is not `graduate-candidate`

The missing evidence is not another parser feature. It is the central empirical question of #668: whether two independent humans find the extracted proposition model and downstream assurance workflow useful enough, stable enough and cheap enough to justify a stable capability.

Calling the result `graduate-candidate` before collecting that evidence would turn the graduation exercise into a self-certification exercise and would violate the visible-judgment discipline used throughout #662.

## Socialisation readiness

**YES.**

The branch is ready to be shown to external reviewers with:

- a pinned measured implementation SHA;
- a five-item, three-publisher real-policy/governance corpus;
- explicit source/licensing provenance;
- a fixed review protocol;
- a machine-readable reviewer template;
- metrics that keep acceptance, amendment, rejection and high-materiality disagreement distinct;
- a non-merge decision boundary.

This is the correct point to seek feedback because reviewers can now critique both the capability and the graduation protocol without their feedback being silently absorbed into a moving implementation during measurement.

## Next evidence-producing actions

1. Recruit/identify Reviewer A and Reviewer B.
2. Give each reviewer the same frozen candidate outputs and `reviewer-template.json` separately.
3. Collect immutable review records without cross-viewing.
4. Run `tools/policy_graduation_metrics.py` over the records.
5. Reconcile disagreements in a third record without mutating either original review.
6. Score one runtime-composition case and one policy-delta case.
7. Update this decision against the five gates.
8. If the result becomes `graduate-candidate` or `bounded-graduate-candidate`, keep #667 draft/on the research branch and begin a socialisation/feedback period rather than merging.
