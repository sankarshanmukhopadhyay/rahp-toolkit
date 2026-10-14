# Fiduciary booking-withdrawal fixture recommendations

Issue: #1018  
Research basis: #1011 and #1019

## Recommendation

Keep this tranche as a profile-local review fixture until the repository has at least one additional independent profile showing the same evidence-role closure and evidence-applicability needs.

Do not promote fiduciary vocabulary, affected-context overlays, or duty profiles into portable RAHP method from this fixture alone.

## Immediate use

Use the fixture to review whether RAHP can cleanly express the following invariant:

```text
A system may be technically capable, previously authorized, and partially evidenced, yet still not presently eligible to act.
```

The first review pass should check that each negative or adversarial scenario blocks PASS when authority evidence is withdrawn, missing, stale, contradictory, out of scope, or invalidated by relationship state.

## Follow-on candidates

1. Add a lightweight validator or script that checks `expected-results.yaml` against `evidence-manifest.yaml` for missing required evidence roles.
2. Add a reusable subject-boundary template for assembled agentic systems.
3. Add evidence-applicability guidance covering subject revision, authority state, relationship state, configuration, and time window.
4. Add documentation distinguishing technical-control assurance from human-outcome assurance.
5. Consider promoting the fixture to `examples/` only after it proves useful for teaching, regression, or conformance.

## Non-goals

- Do not import the Fiduciary Agent Threat and Assurance Matrix wholesale.
- Do not add fiduciary duties to RAHP core.
- Do not build a spreadsheet importer in this tranche.
- Do not treat matrix outcome states as native RAHP states without explicit mapping.
- Do not claim AIUC-1 certification or compliance.
- Do not claim RAHP authorizes runtime operation.

## Decision point

The next useful decision is whether to add executable validation for profile-local evidence-role closure. That should be a separate issue after this fixture lands and after repository validation confirms that the review fixture does not disturb existing method, docs, or build surfaces.
