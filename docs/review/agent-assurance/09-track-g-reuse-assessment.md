# Agent assurance I1 — Track G reuse assessment

Tracking: #970
Prior work: #379, PR #392

## Finding
The DTG architecture-convergence Track G work is not merely a requirement source. PR #392 retained an executable-composition assessment at:

`examples/cross-spec/dtg-architecture-convergence/track-g-end-to-end-actuation.yaml`

Its recorded evidence includes Interop Lab PR #96 at merged commit `727bd56facea7fa57f2cf3d93be82b011167ae78`.

## Existing actuation invariant
Track G already evaluates the proposition that consequential execution requires independently current actor/relationship, delegation/representation, authority, governance/policy, task/invocation, proof-binding, privacy-boundary and effect-admission conditions. No layer may enlarge or synthesize another.

It also separately records a one-effect/replay proposition: successful credential/proof/authority verification is not exactly-once execution evidence.

## Reusable negative vectors
The retained assessment records deterministic denial/staleness vectors for:
- revoked or absent authority;
- missing required representation;
- hidden-subject mismatch;
- task/invocation mismatch;
- policy change before actuation;
- duplicate-effect attempt;
- privacy-boundary failure;
- stale upstream source pins.

## AAP mapping
| AAP | Track-G evidence | Qualification |
| --- | --- | --- |
| AAP-004 | current authority/delegation at actuation | reusable experimental semantic evidence |
| AAP-005 | revoked/expired/stale authority denied | reusable experimental semantic evidence |
| AAP-006 | current authority + exact action scope independently gated | reusable experimental semantic evidence |
| AAP-008 | delegation/authority non-substitution and attenuation | reusable experimental semantic evidence |
| AAP-010 | represented execution retains independent predicates | partial; generic multi-agent handoff still needs qualification |
| AAP-011 | task/purpose/audience/invocation and effect-admission gates | reusable experimental semantic evidence |
| AAP-012 | duplicate/replayed effect independently denied | reusable experimental semantic evidence |
| AAP-014 | stale/missing specialist evidence remains bounded/non-green | reusable evidence-conservative behavior |
| AAP-015 | current-state boundary distinguishes stale/revoked/superseded state | reusable experimental semantic evidence |

## Boundary
Track G is explicitly **RAHP-inferred experimental composition evidence**, not universal normative agent authorization semantics. Its Data Room case is informative and DTG-specific. Reuse for #970 should therefore extract portable propositions/fixtures only after demonstrating that the semantics do not depend on DTG credential types or Data Room assumptions.

## Revised gap judgment
Do **not** create a new replay/idempotency evaluator or generic actuation evaluator yet. First determine whether Track G / Interop Lab #96 can be parameterized into an agent-profile fixture without changing its semantics. New code is justified only where portability fails or agent-specific evidence is genuinely absent.
