# GitHub Actions workflow governance

This document records the ownership boundary of the RAHP Toolkit GitHub Actions surface. The objective is not cosmetic minimisation; it is to keep **one execution owner per distinct assurance responsibility** while preventing the Actions UI from growing through convenience wrappers, target-specific launchers and superseded one-off workflows.

The machine-readable authority for the current surface is `config/workflow-governance.yaml`.

## Workflow budget

RAHP currently permits **at most 20 workflow files**. The strict second-pass audit in #1153 reduced the active governed surface to 18 workflows. The evidence-led controller consolidation in #1155 reduces it further to **16 workflows**, leaving four slots of deliberate headroom rather than treating the budget as a target. The governed inventory is exact: every `.github/workflows/*.yml` file must be declared in `config/workflow-governance.yaml`, every declared workflow must exist, and each must own a unique responsibility.

A new workflow is therefore not a free additive change. It must demonstrate a distinct execution/state responsibility and either remain within the budget by replacing/consolidating an existing surface or be accompanied by an explicit governance decision to change the budget. `tools/validate_workflow_governance.py` enforces this invariant.

The budget applies to **execution frequency as well as workflow count**. Lifecycle controllers use event-driven advancement as the primary path. Scheduled execution is a recovery backstop and MUST NOT poll hourly. The current controller budget uses a three-hour DPIP lifecycle recovery cadence, a single six-hour review-worker recovery workflow containing independent combined-review and DTG repository-review jobs, and six-hour DTG assurance reconciliation. DPIP handoff recovery is now owned by the three-hour lifecycle workflow, whose globally serialized handoff job runs after successful lifecycle recovery. The former separate six-hour handoff recovery is removed.

For the five responsibilities originally counted in #784 (DPIP handoff, DPIP lifecycle, DTG assurance reconciliation, combined-review advancement and DTG repository-review advancement), scheduled workflow invocations are reduced from **24/day to 16/day**. The two review state machines still execute as separate jobs on each shared recovery run.

## Governing rule

A workflow should exist only when it owns at least one of the following:

- a distinct reusable execution contract;
- a distinct lifecycle or state-machine transition;
- a distinct scheduled or event-driven recovery responsibility; or
- a bounded evidence/benchmark surface whose cost or triggers justify independent execution.

A workflow that exists only to preset inputs and call another local reusable workflow is not a distinct execution owner. Profile, target, release and experiment selection should be declarative inputs to a generic executor instead.

Mechanical similarity is not sufficient reason to merge workflows when doing so would obscure semantic ownership. Conversely, target names, historical issue numbers, release names, or experiment-specific semantics must not be embedded in reusable workflow logic when those values can be supplied declaratively.

## Canonical workflow classes

### Reusable/core execution

- `validate.yml` — repository-wide assurance, method, conformance and generated-evidence validation.
- `pages.yml` — documentation build/render/deploy integrity. It intentionally does not duplicate the full validation suite.
- `cross-spec-pressure-test.yml` — the sole reusable and manually dispatchable cross-specification assessment executor. Ecosystem selection is supplied through `registry_path`, `composition_id` and validation-mode inputs.
- `clean-room-assessment.yml` — generic declarative clean-room evidence executor.
- `release.yml` — qualified release publication.

### Lifecycle/state-machine controllers

- `review-workers.yml` — one workflow shell with two explicit jobs:
  - `combined_review` owns bounded combined-review advancement for `dtg:portfolio:combined:` work;
  - `dtg_repository_review` owns gatherer-native repository-review advancement for `rahp-assessment-key:dtg:repository:` work.
  Issue routing, manual selection and concurrency groups remain separate. One six-hour schedule provides recovery for both jobs.
- `dtg-portfolio-materiality-handoff.yml` — portfolio materiality/routing handoff; it dispatches the generic cross-spec executor directly.
- `dpip-lifecycle.yml` — owns both explicit RAHP→DPIP referral transport and RAHP/DPIP lifecycle/return reconciliation. The `assurance:dpip-requested` label routes only to a globally serialized handoff job; it does **not** invoke lifecycle reconciliation. Scheduled/manual lifecycle execution hands off only after successful lifecycle processing.
- `dtg-assurance-reconcile.yml` — DTG gatherer assurance reconciliation.
- `instance-watch.yml` — scheduled instance observation, publication and persistence controller.

Consolidation at the workflow-file level does not merge the underlying state machines. Independent job conditions, concurrency identities and controller commands remain visible where state ownership differs.

### Bounded evidence and operational validation

- `corpus-review.yml`
- `corpus-status.yml`
- `distributed-resilience-assessment.yml`
- `execution-benchmark.yml`
- `release-codename-policy.yml`

These remain independently useful because they are scheduled, manually selectable, or produce evidence/artifacts with materially different runtime or reviewer-use characteristics.

Deterministic repository invariants that do not own a distinct lifecycle, publication action, manual evidence product, or expensive execution profile belong in the required `validate.yml` surface rather than consuming a separate workflow file.

`release-codename-policy.yml` is intentionally retained despite being deterministic because it is part of the release supply-chain boundary: its checkout/setup actions are immutable-SHA pinned and regression-tested. Moving that check into the broader validation workflow would currently weaken that property.

`execution-benchmark.yml` is measurement evidence, not a routine assurance gate. Ordinary PRs do not run the full validation + cross-spec benchmark matrix. PR execution is limited to a single core benchmark when the benchmark runner, benchmark contract, or benchmark workflow itself changes; full and cross-spec benchmark profiles remain explicitly dispatchable.

## Removed workflows

Historical target-specific clean-room workflows were removed after `clean-room-assessment.yml` became the canonical declarative executor:

- `clean-room-dogwood.yml`
- `true-clean-room-dogwood-248.yml`

The 31 Aug 2026 workflow rationalisation also removed two dispatch-only cross-spec wrappers:

- `cawg-cross-spec-pressure-test.yml`
- `dtg-cross-spec-pressure-test.yml`

Both merely preset inputs to `cross-spec-pressure-test.yml`. CAWG and DTG now use the generic executor directly, reducing the workflow surface from **22 to 20** without removing an assurance capability.


The 25 Oct 2026 strict second-pass audit (#1153) retired two bounded validation workflows:

- `vti-composition-wave.yml`
- `vti-semantic-completion.yml`

Their checks remain explicit in the required `validate.yml` job. They were removed because they had no distinct write-side state transition, manual evidence product, durable artifact, recovery responsibility, or required status context. Consolidation therefore reduces Actions surface while strengthening the merge gate: the VTI evidence-vector validations now run under the required `validate` status. The release codename policy remains separate because its immutable Action pins are part of the release supply-chain boundary.

This reduces the governed workflow surface from **20 to 18** without deleting an assurance invariant.

The follow-up controller-consolidation tranche (#1155) then removed three workflow files while adding one replacement shell:

- removed `dpip-handoff.yml`; its immediate label-trigger transport and recovery handoff now live as a globally serialized job in `dpip-lifecycle.yml`;
- removed `combined-review-worker.yml`;
- removed `dtg-repository-review-worker.yml`;
- added `review-workers.yml`, retaining two explicit jobs and state-machine identities.

Net effect: **18 → 16 workflows**. DPIP handoff remains event-driven and globally serialized; review-worker recovery remains six-hour and state-machine-specific even though both jobs share one workflow invocation.

## Clean-room portability invariant

Reusable clean-room workflow logic must not depend on a target repository name, target codename/release, historical RAHP issue number, target-specific producer identifier, or target-specific evidence path. Those values belong in the run specification and adapter inputs.

A new conforming target should require a new declarative run specification/adapter configuration, not a new `clean-room-<target>.yml` workflow.

## Post-assessor lifecycle invariant

A specialist assessor return is not the end of the RAHP transaction. A returned DPIP result must be reconciled into RAHP-owned state.

`PASS`/not-applicable can resolve the referral; `FAIL` creates or reuses a durable finding residual; `INDETERMINATE` creates or reuses an evidence-required residual; unknown/unparseable returns become review-required. In every case, the referral container represents the completed handoff and is not kept open merely because the broader assurance proposition remains non-green.

Closing a referral is therefore **not** equivalent to privacy PASS. The durable residual owns whatever evidence, remediation or retest remains.

## Rationalisation policy

When auditing workflows, use this order:

1. remove superseded one-off workflows;
2. move target/profile/experiment data into declarative inputs;
3. prohibit dispatch-only local wrappers over reusable workflows;
4. prefer reusable workflow calls or direct generic dispatch for shared execution engines;
5. retain distinct lifecycle controllers where state ownership differs;
6. retain bounded evidence workflows where independent triggers/cost/evidence products are meaningful;
7. consolidate repeated bootstrap mechanics only when it does not hide state-machine boundaries;
8. use event-driven controller execution as the primary path and scheduled execution only as a bounded recovery backstop;
9. do not run expensive benchmark matrices on ordinary PRs unless the benchmark machinery itself is under test.

## Deferred consolidation candidates

#1155 completed the two controller consolidations that #1153 had deferred, after adding explicit trigger/concurrency regression evidence. Remaining candidates are narrower:

- **Corpus review + corpus status:** both are read-only corpus-maintenance surfaces, but one produces a manually selected reviewer packet while the other is a scheduled source-currentness monitor. Merge only if reviewer UX and artifact semantics remain at least as clear.
- review whether six-hour/three-hour recovery backstops can be reduced further only after event-driven handoffs/reconciliation and watchdog evidence support the change;
- converge action major versions opportunistically, without mixing version churn with semantic workflow changes.

The existence of four free workflow-budget slots is not itself justification to create another workflow.
