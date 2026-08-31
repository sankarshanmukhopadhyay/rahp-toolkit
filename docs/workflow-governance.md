# GitHub Actions workflow governance

This document records the ownership boundary of the RAHP Toolkit GitHub Actions surface. The objective is not cosmetic minimisation; it is to keep **one execution owner per distinct assurance responsibility** while preventing the Actions UI from growing through convenience wrappers, target-specific launchers and superseded one-off workflows.

The machine-readable authority for the current surface is `config/workflow-governance.yaml`.

## Workflow budget

RAHP currently permits **at most 20 workflow files**. The governed inventory is exact: every `.github/workflows/*.yml` file must be declared in `config/workflow-governance.yaml`, every declared workflow must exist, and each must own a unique responsibility.

A new workflow is therefore not a free additive change. It must demonstrate a distinct execution/state responsibility and either remain within the budget by replacing/consolidating an existing surface or be accompanied by an explicit governance decision to change the budget. `tools/validate_workflow_governance.py` enforces this invariant.

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
- `vti-composition-wave.yml`
- `vti-semantic-completion.yml`
- `release-codename-policy.yml`

These remain independently useful because they are path-scoped, scheduled, manually selectable, or produce evidence with different runtime/cost characteristics.

## Removed workflows

Historical target-specific clean-room workflows were removed after `clean-room-assessment.yml` became the canonical declarative executor:

- `clean-room-dogwood.yml`
- `true-clean-room-dogwood-248.yml`

The 31 Aug 2026 workflow rationalisation also removed two dispatch-only cross-spec wrappers:

- `cawg-cross-spec-pressure-test.yml`
- `dtg-cross-spec-pressure-test.yml`

Both merely preset inputs to `cross-spec-pressure-test.yml`. CAWG and DTG now use the generic executor directly, reducing the workflow surface from **22 to 20** without removing an assurance capability.

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
8. reduce scheduled recovery polling only after event-driven reliability has been demonstrated.

## Follow-on candidates

The following remain candidates for evidence-led review rather than automatic consolidation:

- extract common issue-worker bootstrap/setup if a reusable worker wrapper remains transparent about the invoked state machine;
- introduce a generic path-scoped evidence-validator only if multiple existing evidence workflows demonstrate the same execution contract;
- review hourly recovery schedules after sufficient operational evidence shows event-driven handoffs/reconciliation are reliable;
- converge action major versions opportunistically, without mixing version churn with semantic workflow changes.
