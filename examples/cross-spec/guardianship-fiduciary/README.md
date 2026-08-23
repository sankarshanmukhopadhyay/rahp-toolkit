# Guardianship and fiduciary authority: cross-spec RAHP pressure test

This exploratory worked example applies the portable RAHP method to a composed digital-trust problem: how a system represents, proves, exercises, reviews and terminates **guardianship, fiduciary and other constrained authority** without collapsing legal or governance distinctions into a single credential or cryptographic proof.

The example uses the Trust over IP Digital Trust Graph (DTG) work as the first worked instance. It is deliberately **not** a DTG-specific extension to the RAHP method and is not listed in `examples/current-baselines.yaml` as a canonical maintained example.

## Why this case exists

A guardianship or fiduciary relationship is not adequately represented by proving only that an appointment exists. A decision may also depend on the authority's scope, activation conditions, duration, duties, conflicts, transaction thresholds, co-approval requirements, retained agency of the represented person, current status, oversight, redress and jurisdiction.

The pressure test therefore asks a broader question:

> Can a composed trust system distinguish valid authority from permissible exercise of that authority, while exposing enough evidence for oversight and redress without forcing disclosure of unnecessary sensitive status?

That distinction is the core hypothesis under test. Cryptographic validity is necessary evidence, but it is not by itself proof of fiduciary propriety.

## Baseline hypotheses

The assessment begins with five hypotheses that map to likely DTG work surfaces. These are **inputs to the assessment, not pre-decided issue conclusions**.

1. **Cross-DTG / general:** guardianship, fiduciary duties and constrained authority need a shared cross-spec model rather than isolated treatment in one credential type.
2. **Credential semantics:** credentials need to express bounded authority and its lifecycle without requiring unnecessary disclosure of sensitive status.
3. **Trust Tasks:** transaction execution needs evidence for approvals, conflicts, thresholds, co-approval, oversight and the authority state that applied at decision time.
4. **Privacy / ZKP:** presentations need privacy-preserving predicates and relationship proofs for authority, scope and approval composition rather than durable correlators or ancestry disclosure.
5. **Governance / assurance:** retained agency, least-restrictive authority, oversight, review, restoration and redress remain governance and assurance properties even when cryptographic evidence is valid.

A finding is useful only where evidence supports it. The assessment may confirm, narrow, split or reject any of these hypotheses.

## Predicate-first case model

The worked case decomposes the authority relationship into independently testable predicates and lifecycle properties:

- authority and appointment;
- scope;
- duration and activation;
- duty;
- conflict;
- transaction thresholds;
- co-approval;
- retained agency;
- privacy and disclosure minimization;
- status, suspension and supersession;
- cross-credential / cross-task composition;
- resolution and authoritative source discovery;
- audit and periodic review;
- redress;
- emergency authority;
- jurisdiction;
- interoperability;
- revocation and restoration;
- liability and accountability.

The purpose of the decomposition is to prevent semantic collapse. For example, proving `appointment = valid` must not silently imply `transaction = permitted`, and proving a threshold condition must not silently prove that conflicts or approval duties were satisfied.

## Adversarial scenarios

The pressure test explicitly challenges the composed system with failure modes including:

- replay of an old approval in a new Trust Task;
- use of an approval after the underlying authority has become stale, suspended or superseded;
- privacy leakage caused by proving co-approval or relationship ancestry;
- emergency authority that remains effective after the emergency condition ends;
- restoration of a represented person's authority that does not propagate to credentials, tasks or verifier decisions;
- supposedly confidential digests that are enumerable and therefore reveal sensitive status;
- cross-context linkability created by durable identifiers or reusable proof material;
- proofs constructed from unauthenticated or weakly governed source assertions;
- semantic collapse between appointment, authority, delegation, approval, duty and transaction permission;
- acceptance of cryptographic validity as sufficient evidence of fiduciary propriety.

## Evidence-closure rule

The example uses an evidence-closure discipline:

1. identify the decision or harm-relevant claim;
2. identify the predicates required to justify it;
3. identify the authoritative source and lifecycle state for each predicate;
4. identify the composition rule connecting those predicates to the decision;
5. identify privacy constraints on the evidence presentation;
6. identify retained uncertainty, governance judgment and redress obligations;
7. record the evidence needed to move a finding from hypothesis to disposition.

A missing predicate, missing source, missing lifecycle rule or missing composition rule remains an explicit assurance gap. The example does not infer closure merely because every individual credential verifies cryptographically.

## Initial work map

The machine-readable companion file records the initial findings and likely control-plane ownership. At this stage the map is advisory:

| Surface | Primary question |
| --- | --- |
| DTG General / cross-spec model | What common semantics distinguish appointment, bounded authority, duty, retained agency and exercise? |
| Credential Specification | What must be expressed or provable about authority, scope, lifecycle and status? |
| Trust Tasks | What transaction-bound evidence proves approvals, thresholds, conflicts and current authority? |
| ZKP / privacy | Which predicates and composed relationships must be provable without unnecessary correlators or sensitive-status disclosure? |
| Governance / assurance | What rules govern least-restrictive authority, oversight, periodic review, restoration, redress and liability? |

This table is not an instruction to open five downstream issues. The assessment should first produce source-pinned evidence and a hypothesis-delta analysis. Maintainers can then determine which concerns belong in existing work, require new work, or are out of scope.

## Intended use

This case is useful beyond guardianship. The same RAHP decomposition can pressure-test constrained authority involving trustees, attorneys-in-fact, executors, organizational representatives, regulated fiduciaries, delegated agents and other relationships where **being authorized** and **acting permissibly under that authority** are distinct propositions.

The DTG instance is therefore a worked deployment of a portable assessment pattern rather than the definition of the pattern itself.

## Machine-readable assessment

See [`pressure-test.yaml`](./pressure-test.yaml) for the exploratory findings, hypothesis deltas, evidence requirements and cross-spec disposition map.
