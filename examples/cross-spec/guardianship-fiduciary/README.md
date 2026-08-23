# Guardianship and fiduciary authority: cross-spec RAHP pressure test

This exploratory worked example applies the portable RAHP method to a composed digital-trust problem: how a system represents, proves, exercises, reviews and terminates **guardianship, fiduciary and other constrained authority** without collapsing legal or governance distinctions into a single credential or cryptographic proof.

The Trust over IP Digital Trust Graph (DTG) is the first worked instance. This is not a DTG-specific extension to RAHP and is intentionally not listed in `examples/current-baselines.yaml` as a canonical maintained example.

## Assessment lifecycle

The case deliberately separates exploratory inputs from formal RAHP assessment records:

1. [`hypothesis-baseline.yaml`](./hypothesis-baseline.yaml) preserves the **initial hypotheses and candidate findings** before source review. It is intentionally not a formal `pressure-test.yaml` contract.
2. [`pressure-test.yaml`](./pressure-test.yaml) is the **conformant in-progress RAHP pressure-test wrapper**. Findings enter this record only after they satisfy the repository's finding/evidence contract.
3. [`evidence-pass.yaml`](./evidence-pass.yaml) records the **source-pinned reassessment** against current DTG revisions.
4. [`evidence-review.md`](./evidence-review.md) explains the evidence and hypothesis deltas for human review.

Keeping these stages separate is intentional. A pressure test should be able to weaken its own starting claims rather than silently rewriting them after evidence appears, while files named `pressure-test.yaml` must remain valid executable RAHP records.

## Discussion record

The public GitHub Discussion is intended to remain the umbrella research thread for this case. Because the connected GitHub tooling does not currently expose Discussion create/update operations, the exact public-post text is retained here so that the public thread and repository evidence cannot drift apart:

- [`discussion-opening.md`](./discussion-opening.md) — opening post: hypotheses, scenarios, questions and disposition boundary;
- [`discussion-evidence-update.md`](./discussion-evidence-update.md) — first source-pinned evidence-pass update;
- [`discussion-next-updates.md`](./discussion-next-updates.md) — synchronized structure for the three evidence-closure case updates and the final consolidated disposition.

The intended sequence is:

`Discussion hypotheses -> RAHP pressure test -> source-pinned evidence -> evidence-closure cases -> consolidated maintainer disposition -> downstream work only where justified`

A downstream DTG Issue is therefore an output of demonstrated residual evidence, not a substitute for the exploratory Discussion.

## What the evidence pass changed

The first source-pinned pass materially narrowed the original problem.

Current DTG sources already provide substantial reusable machinery for:

- distinguishing cryptographic proof from authorization;
- validity, expiry and applicable revocation checks;
- scoped and expiring authorization grants;
- explicit revocation and scope reduction;
- audience binding and exchange/citation context;
- task-context binding;
- source/issuer authorization checks.

The companion ZKP fork additionally provides explicit controls for composed-presentation privacy, low-entropy/enumerable hiding constructions, task-context non-inference, external-evidence governance, and the separation of proof assurance from governance assurance.

Those companion controls are evidence of a viable design direction; they are **not treated as upstream DTG adoption**.

The revised residual question is therefore:

> Can existing DTG primitives be composed into an interoperable constrained-authority profile that establishes appointment, current scope, transaction permission, duties/conflicts and retained agency at decision time, while preserving privacy and redress boundaries?

That is a smaller and more actionable question than “does DTG support guardianship?”

## Baseline hypotheses

The initial assessment tested five hypotheses:

1. constrained authority needs a cross-spec composition model;
2. credential semantics must support bounded authority without unnecessary sensitive-status disclosure;
3. Trust Tasks must carry decision-relevant transaction and authority evidence;
4. privacy must hold over composed authority/approval proofs rather than individual credentials alone;
5. governance and assurance properties such as retained agency, restoration, oversight and fiduciary propriety cannot be inferred from cryptographic validity.

The evidence pass classifies these respectively as **refined**, **refined**, **weakened**, **confirmed/partially controlled**, and **confirmed/narrowed**.

## Predicate-first model

The case decomposes constrained authority into independently testable properties rather than introducing one omnibus credential:

- appointment and authority;
- scope, duration and activation;
- duty and conflict;
- transaction thresholds and co-approval;
- retained agency;
- privacy and disclosure minimization;
- status, suspension and supersession;
- cross-credential / cross-task composition;
- authoritative-source resolution;
- audit, periodic review and redress;
- emergency authority;
- jurisdiction and interoperability;
- revocation, restoration, liability and accountability.

The central non-inference remains: `appointment = valid` must not silently imply `transaction = permitted`.

## Evidence-closure rule

For a constrained-authority decision, the example asks implementers to identify:

1. the decision or harm-relevant claim;
2. predicates required to justify it;
3. the authoritative source and lifecycle state for each predicate;
4. the composition rule connecting those predicates to the decision;
5. privacy constraints on the presentation;
6. retained governance judgment and redress obligations;
7. evidence needed before a finding can be dispositioned.

Cryptographic verification of all component artifacts is not, by itself, evidence closure.

## Current work map

After source review, the findings group more usefully as follows:

| Work class | Findings | Next move |
| --- | --- | --- |
| Composition/profile construction | F01, F02, F03, F04, F08 | Construct concrete transactions using current primitives before proposing normative changes. |
| Proof-construction guardrail | F05 | Preserve enumeration and correlation resistance for future hidden-status constructions. |
| Governance/profile first | F06, F07, F09, F10 | Define policy semantics and evidence expectations before assigning specification ownership. |

This is **not** an instruction to open downstream DTG issues.

## Next gate

The next useful RAHP step is executable case construction around three flows:

- a routine constrained-authority act;
- a threshold/co-approval act;
- a suspension/restoration act.

For each flow, current Credential and Trust Task primitives should be reused first. Only predicates that cannot be represented or privately proven with the pinned interfaces should graduate into candidate specification work.

## Intended use

The pattern extends beyond guardianship to trustees, attorneys-in-fact, executors, organizational representatives, regulated fiduciaries, delegated agents and similar relationships where **being authorized** and **acting permissibly under that authority** are distinct propositions.
