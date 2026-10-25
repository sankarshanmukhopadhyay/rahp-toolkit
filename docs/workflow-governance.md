# GitHub Actions workflow governance

This document records the ownership boundary of the RAHP Toolkit GitHub Actions surface. The objective is not cosmetic minimisation; it is to keep **one execution owner per distinct assurance responsibility** while preventing the Actions UI from growing through convenience wrappers, target-specific launchers and superseded one-off workflows.

The machine-readable authority for the current surface is `config/workflow-governance.yaml`.

## Workflow budget

RAHP currently permits **at most 20 workflow files**. The strict second-pass audit in #1153 reduces the active governed surface to **18 workflows**, leaving three slots of deliberate headroom rather than treating the budget as a target. The governed inventory is exact: every `.github/workflows/*.yml` file must be declared in `config/workflow-governance.yaml`, every declared workflow must exist, and each must own a unique responsibility.

A new workflow is therefore not a free additive change. It must demonstrate a distinct execution/state responsibility and either remain within the budget by replacing/consolidating an existing surface or be accompanied by an explicit governance decision to change the budget. `tools/validate_workflow_governance.py` enforces this invariant.

The budget applies to **execution frequency as well as workflow count**. Lifecycle controllers use event-driven advancement as the primary path. Scheduled execution is a recovery backstop and MUST NOT poll hourly. The current controller budget uses six-hour recovery for DPIP handoff, DTG assurance reconciliation, combined-review advancement and DTG repository-review advancement, and a three-hour DPIP lifecycle recovery cadence so the six-hour watchdog boundary still has margin.

Across those five controllers this reduces the scheduled baseline from roughly **120 runs/day to 24 runs/day**, while preserving event-triggered and manual execution.

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

- `combined-review-worker.yml` — bounded combined-review advancement.
- `dtg-repository-review-worker.yml` — DTG gatherer repository-review advancement.
- `dtg-portfolio-materiality-handoff.yml` — portfolio materiality/routing handoff; it dispatches the generic cross-spec executor directly.
- `dpip-handoff.yml` — explicit RAHP→DPIP referral transport.
- `dpip-lifecycle.yml` — RAHP/DPIP lifecycle telemetry **and terminal post-DPIP return reconciliation**. A returned specialist result is converted to `resolved`, `finding-open`, `evidence-required`, or `review-required`; completed referral containers are not retained as proxies for unresolved assurance.
- `dtg-assurance-reconcile.yml` — DTG gatherer assurance reconciliation.
- `instance-watch.yml` — scheduled instance observation, publication and persistence controller.

These workflows share bootstrap mechanics but own different event contracts and state transitions. They should not be collapsed merely to reduce file count.

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


The 25 Oct 2026 strict second-pass audit (#1153) retired three more bounded validation workflows:

- `vti-composition-wave.yml`
- `vti-semantic-completion.yml`

Their checks remain explicit in the required `validate.yml` job. They were removed because they had no distinct write-side state transition, manual evidence product, durable artifact, recovery responsibility, or required status context. Consolidation therefore reduces Actions surface while strengthening the merge gate: codename-policy and VTI evidence-vector validation now run under the required `validate` status.

This reduces the governed workflow surface from **20 to 18** without deleting an assurance invariant.

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

The strict #1153 audit keeps the following as evidence-led candidates rather than collapsing them now:

- **DPIP handoff + DPIP lifecycle:** `dpip-lifecycle.yml` already invokes the handoff controller and has a stronger three-hour recovery cadence, but `dpip-handoff.yml` owns the immediate `assurance:dpip-requested` label transition. Consolidate only after trigger-equivalence, idempotency and issue-scoped lifecycle tests prove no semantic widening.
- **Combined-review worker + DTG repository-review worker:** the workflow shells and six-hour recovery cadence are similar, but the state machines, issue markers and concurrency identities differ. A future shared workflow must retain two explicit controller jobs and independent routing.
- **Corpus review + corpus status:** both are read-only corpus-maintenance surfaces, but one produces a manually selected reviewer packet while the other is a scheduled source-currentness monitor. Merge only if reviewer UX and artifact semantics remain at least as clear.
- review whether six-hour/three-hour recovery backstops can be reduced further only after event-driven handoffs/reconciliation and watchdog evidence support the change;
- converge action major versions opportunistically, without mixing version churn with semantic workflow changes.

The existence of two free workflow-budget slots is not itself justification to create another workflow.
