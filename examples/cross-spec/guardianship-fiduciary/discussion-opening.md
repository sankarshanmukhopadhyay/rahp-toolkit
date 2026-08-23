# Pressure test: guardianship, fiduciary duties, and constrained representative authority

This Discussion opens a RAHP pressure test of a cross-specification problem in digital trust: how to represent and verify **constrained representative authority** where the authority is shaped not only by delegation or appointment, but also by duties, conflicts, retained principal agency, joint approval, lifecycle changes, oversight and redress.

This is **not** a proposal to settle DTG normative design in advance. The purpose is to state the hypotheses clearly, test them against current DTG artifacts, record where the hypotheses survive or fail, and only then decide whether any downstream specification work is justified.

The worked case is maintained in the RAHP Toolkit under:

`examples/cross-spec/guardianship-fiduciary/`

## Baseline question

The central question is:

> Can current digital-trust primitives for delegation/authorization, credential semantics, transaction evidence, privacy-preserving proof, lifecycle, conformance and governance be composed into a decision that establishes not merely that a representative exists, but that the representative is currently authorized to perform this particular act under the applicable constraints, while preserving retained principal rights and minimizing sensitive disclosure?

The initial hypothesis is that guardianship and fiduciary authority exposes a useful boundary condition for digital trust systems because **authorization and permissible exercise are not the same proposition**.

A valid appointment or delegation may establish that an actor has some authority. It does not necessarily establish that:

- the current transaction lies within the permitted domain;
- the transaction is below or within an applicable threshold;
- a required co-approval has been obtained;
- the authority has not been suspended, superseded, narrowed or restored to the principal;
- no disqualifying conflict applies;
- an emergency condition is still active;
- the principal lacks retained decision rights;
- an act satisfies fiduciary, best-interest, proportionality or least-restrictive requirements; or
- the act is immune from review, challenge or redress.

## Working decomposition

For purposes of the pressure test, the authority relationship is decomposed into three layers:

1. **Authority** — does this representative currently have authority of the relevant type and scope?
2. **Constraint / duty compliance** — does this transaction satisfy the conditions, approvals, thresholds, conflict rules and other constraints that make exercise of the authority permissible?
3. **Retained principal agency / redress** — what rights remain with the principal, how are restoration and partial restoration represented, and how can a decision be challenged or reviewed?

This decomposition is deliberately construction-neutral. It does not assume that the eventual implementation must use any particular credential format, commitment, selective-disclosure mechanism, accumulator, SNARK, BBS construction or other proof system.

## Baseline hypotheses to test

### H1 — Cross-spec semantics

Guardianship, fiduciary duties and constrained representative authority likely require shared semantics across multiple DTG surfaces rather than being modeled as one credential type or one Trust Task.

### H2 — Credential semantics

Credential-side semantics may need to express or make provable bounded authority, scope, activation, duration, lifecycle state and restoration without requiring unnecessary disclosure of sensitive status.

### H3 — Trust Task evidence

Transaction execution may require task-bound evidence for thresholds, approvals, co-approval, conflicts, supervision, emergency conditions, current authority state and post-action accountability.

### H4 — Privacy / ZKP composition

Where the relying party needs only a narrow predicate, the composed presentation should not require disclosure of durable identifiers, full appointment history, family or medical status, all representatives, or other unnecessary sensitive material.

Privacy therefore needs to be evaluated across the **complete composed evidence closure**, not credential-by-credential.

### H5 — Governance and assurance

Cryptographic validity cannot by itself establish substantive fiduciary propriety. Governance still has to define the meaning of duties, conflicts, least-restrictive authority, supported versus substituted decision-making, retained agency, review, restoration, liability and redress.

## Candidate predicates

The pressure test will examine whether existing DTG work can support predicates such as:

- representative currently has authority for action class X;
- action is within the representative's permitted domain;
- action is within an applicable transaction threshold;
- required co-approval or quorum has been obtained;
- relevant authority has not been suspended or superseded;
- no disqualifying conflict applies under the governing profile;
- principal retains the right to participate or act for this domain;
- an emergency condition is currently active;
- the authoritative source and lifecycle state supporting the predicate are current;
- evidence is attributable and reviewable without requiring unnecessary sensitive disclosure.

These are requirements-level predicates, not proposed identifiers or final proof constructions.

## Adversarial scenarios

The assessment will deliberately include cases such as:

- an elderly principal with a formally valid but abusive representative;
- a person with partial or fluctuating capacity;
- a principal whose authority has been restored but stale evidence still blocks them;
- a minor whose guardianship status becomes a durable cross-context correlator;
- co-guardians where one acts without the required second approval;
- fiduciary self-dealing;
- an abusive family member relying on technically valid authority;
- a representative exceeding a transaction threshold;
- a representative acting after suspension or supersession;
- emergency authority reused after the emergency has ended;
- a principal who cannot practically challenge a technically valid action;
- a verifier that over-collects legal, family or incapacity status;
- a status service that observes every verification event;
- a co-approval flow that reveals the full representative set;
- a conflict check that leaks a sensitive relationship;
- a legitimate representative who cannot act because proof flows are inaccessible;
- coercion of the principal into approving or waiving rights; and
- a verifier inferring incapacity merely from the existence of representative-authority artifacts.

Negative cases will also include replay, stale approvals, low-entropy deterministic hashes treated as hiding commitments, shared handles linking otherwise private artifacts, supersession flows requiring full appointment ancestry, mathematically valid proofs over unauthenticated source assertions, and technical authorization being over-read as fiduciary propriety.

## Initial ownership hypothesis

The current working boundary is:

- **Governance** defines legal/policy meaning, duties, constraints, retained agency, redress and authoritative-source policy.
- **Credential specifications** define what propositions must be expressible or provable.
- **Trust Tasks** expose transaction evidence and proof-capable interfaces.
- **ZKP/privacy profiles** define how required predicates and relationships can be proven privately.
- **Conformance/assurance** evaluates the complete composed evidence closure and the permitted non-inferences.

This is an ownership hypothesis, not a decision.

## What this Discussion should produce

The intended outputs are:

1. a reproducible RAHP worked case;
2. machine-readable findings and evidence requirements;
3. source-pinned observations against current DTG material;
4. explicit hypothesis deltas — confirmed, refined, weakened, contradicted, governance-only or insufficient evidence;
5. concrete evidence-closure constructions using existing primitives wherever possible;
6. an advisory cross-spec work map; and
7. maintainer disposition on whether any residual finding warrants downstream specification work.

The process will **not automatically create downstream DTG issues**. If the pressure test identifies a genuine missing primitive or normative gap, that should be proposed only after the evidence is visible here and maintainers have had a chance to assess the result.

## Questions for maintainers

The most useful feedback at this stage is:

- Is the authority / constraint-compliance / retained-agency decomposition materially wrong or incomplete?
- Are any of the candidate predicates already fully covered by current DTG work?
- Are there existing lifecycle, status, authorization or privacy mechanisms that should be treated as controlling evidence in the assessment?
- Which scenarios are useful pressure tests, and which are outside the intended DTG scope?
- Where should the boundary sit between machine-verifiable predicates and governance/accountability judgments that cannot safely be reduced to proof validity?

The goal is to let the evidence narrow the problem before the project creates new normative surface area.