# GitHub Actions workflow governance

This document records the intended ownership boundary of the RAHP Toolkit GitHub Actions surface. The objective is not to minimise workflow count mechanically. The objective is to keep **one execution owner per distinct assurance responsibility**, eliminate stale one-off entry points, and make thin adapters visibly different from duplicate engines.

## Governing rule

A workflow should exist only when it owns at least one of the following:

- a distinct reusable execution contract;
- a distinct lifecycle or state-machine transition;
- a distinct scheduled or event-driven recovery responsibility;
- a bounded evidence/benchmark surface whose cost or triggers justify independent execution; or
- a deliberately thin typed launcher over a reusable workflow.

Mechanical similarity is not sufficient reason to merge workflows when doing so would obscure semantic ownership. Conversely, target names, historical issue numbers, release names, or experiment-specific semantics must not be embedded in reusable workflow logic when those values can be supplied declaratively.

## Canonical workflow classes

### Reusable/core execution

- `validate.yml` — repository-wide assurance, method, conformance and generated-evidence validation.
- `pages.yml` — documentation build/render/deploy integrity. It intentionally does not duplicate the full validation suite.
- `cross-spec-pressure-test.yml` — reusable cross-specification assessment executor.
- `clean-room-assessment.yml` — generic declarative clean-room evidence executor.
- `release.yml` — qualified release publication.

### Typed launchers

- `cawg-cross-spec-pressure-test.yml` — CAWG/C2PA composition selector over the reusable cross-spec workflow.
- `dtg-cross-spec-pressure-test.yml` — DTG composition selector over the reusable cross-spec workflow.

These files intentionally preserve typed manual choices. They do not contain independent assessment engines.

### Lifecycle/state-machine controllers

- `combined-review-worker.yml` — bounded combined-review advancement.
- `dtg-repository-review-worker.yml` — DTG gatherer repository-review advancement.
- `dtg-portfolio-materiality-handoff.yml` — portfolio materiality/routing handoff.
- `dpip-handoff.yml` — explicit RAHP→DPIP referral transport.
- `dpip-lifecycle.yml` — RAHP/DPIP lifecycle telemetry and recovery reconciliation.
- `dtg-assurance-reconcile.yml` — DTG gatherer assurance reconciliation.
- `instance-watch.yml` — scheduled instance observation, publication and persistence controller.

These workflows share some bootstrap mechanics but own different event contracts, inputs and state transitions. They should not be collapsed merely to reduce file count.

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

The following historical workflows were removed by #255 after `clean-room-assessment.yml` became the canonical declarative executor:

- `clean-room-dogwood.yml`
- `true-clean-room-dogwood-248.yml`

They encoded a target and/or historical assessment issue directly in workflow logic. Retaining them would create competing clean-room entry points and reintroduce the coupling removed by #253/#254.

## Clean-room portability invariant

Reusable clean-room workflow logic must not depend on a target repository name, target codename/release, historical RAHP issue number, target-specific producer identifier, or target-specific evidence path. Those values belong in the run specification and adapter inputs.

A new conforming target should require a new declarative run specification/adapter configuration, not a new `clean-room-<target>.yml` workflow.

## Rationalisation policy

When auditing workflows, use this order:

1. remove superseded one-off workflows;
2. move target/experiment data into declarative inputs;
3. prefer reusable workflow calls for genuinely shared execution engines;
4. retain thin typed launchers when they improve safe manual operation;
5. retain distinct lifecycle controllers where state ownership differs;
6. consolidate repeated bootstrap mechanics only when it does not hide state-machine boundaries;
7. reduce scheduled recovery polling only after event-driven reliability has been demonstrated.

## Follow-on candidates

The following are candidates for later review rather than automatic consolidation:

- extract common issue-worker bootstrap/setup if a reusable worker wrapper remains transparent about the invoked state machine;
- introduce a generic path-scoped evidence-validator workflow if a third validation surface demonstrates the same execution contract as the current VTI evidence workflows;
- review hourly recovery schedules after sufficient operational evidence shows event-driven handoffs/reconciliation are reliable;
- converge action major versions opportunistically, without mixing version churn with semantic workflow changes.
