# DTG architecture convergence — proposition/evidence matrix

This directory is the canonical RAHP control point for the work opened from [Discussion #371](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/371) and tracked by [issue #372](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/372).

The purpose is to stop the correlation-scope, VDC, VAC, ZKP, node-model and actuation tracks from independently inventing slightly different interpretations of the emerging DTG architecture.

The machine-readable source of truth is [`proposition-matrix.yaml`](./proposition-matrix.yaml).

## Authority classes

The matrix deliberately separates four kinds of material:

| Authority status | Meaning |
|---|---|
| `adopted` | Normative upstream material already accepted by the responsible authority. |
| `proposed-upstream` / related proposed states | Text or semantics currently proposed in an upstream PR/issue/discussion. Experimental RAHP work may test these semantics but MUST NOT describe them as adopted DTG behavior. |
| `informative-design` | Implementation-shaped design material used to expose composition questions. It is not normative DTG text. |
| `rahp-inferred-composition` | A proposition RAHP believes must hold for the composite assurance claim. It is a falsifiable assessment proposition, not an assertion that upstream already specifies it. |

The current upstream inputs are deliberately source-pinned where an immutable PR head is available:

| Source | Status | Pin |
|---|---|---|
| Credential spec PR #30 — correlation scope | proposed upstream | `b3840f430f5bd01addab95881350a7f860e763e2` |
| Credential spec PR #19 — VDC | proposed upstream | `ad5876f1b96e2149adec84d37d6595b4a212db9c` |
| Credential spec PR #29 — VAC | proposed upstream | `84650749afd48798e1c8919a95be359c0367a1c9` |
| Credential spec issue #22 | mutable deliberation | issue URL |
| Credential TF Discussion #41 | mutable deliberation | discussion URL |
| [Verifiable Data Rooms](https://docs.fpp.storm.ws/data-rooms-concept.html) | informative design pressure test | mutable public design document, observed 2026-09-02 |

A mutable discussion/design source is never treated as equivalent to an immutable source revision. If it changes materially, dependent evidence becomes a reassessment candidate.

## Canonical proposition set

| ID | Proposition | Authority | Primary downstream track |
|---|---|---|---|
| `DTG-371-P01` | Role and correlation scope are independent dimensions. | proposed upstream | #373 / #378 |
| `DTG-371-P02` | Holder scope declaration does not prove counterparty disclosure behavior. | proposed upstream | #373 |
| `DTG-371-P03` | Proposed scope vocabulary is `pairwise → directed → public`. | proposed upstream | #373 |
| `DTG-371-P04` | Correlation scope and identifier durability are independent. | proposed upstream | #373 |
| `DTG-371-P05` | Scope-declaration carriage remains an assurance-relevant open question. | proposed upstream open question | #373 |
| `DTG-371-P06` | Delegation and authority cannot substitute for one another. | proposed upstream | #374 |
| `DTG-371-P07` | Effective delegated ability is an intersection, never a union. | proposed upstream | #374 |
| `DTG-371-P08` | VAC attenuation must be monotonically non-widening. | proposed upstream | #375 |
| `DTG-371-P09` | Signature validity cannot substitute for current authority/delegation state. | RAHP composition inference | #374 / #375 |
| `DTG-371-P10` | Hidden-subject multi-credential authorization requires same-subject/common-control evidence. | proposed upstream | #376 |
| `DTG-371-P11` | Cross-governance action semantics require explicit semantic equivalence, not lexical equality. | proposed upstream design constraint | #377 |
| `DTG-371-P12` | Node identity does not imply credential applicability. | proposed upstream design constraint | #378 |
| `DTG-371-P13` | Declared, observable and effective correlation scope are separate assurance facts. | RAHP composition inference | #373 / #376 |
| `DTG-371-P14` | Consequential actuation requires all applicable current layers; component validity is insufficient. | RAHP composition inference | #379 |
| `DTG-371-P15` | Verification success does not establish one-effect execution or replay safety. | RAHP composition inference | #379 |

## Evidence discipline

The matrix intentionally records evidence classes instead of treating all evidence as interchangeable.

- **Specification analysis** can support claims about what proposed text says.
- **Implementation/model vectors** can show whether a semantic model is internally executable.
- **Runtime current-state evidence** is required for revocation/expiry/supersession claims.
- **Runtime A/B privacy evidence** is required for effective-correlation claims that depend on observable traffic, metadata or retained evidence.
- **Executable positive/negative ZKP evidence** is required for same-subject/common-control composition claims.
- **End-to-end execution evidence** is required before RAHP can claim that the complete stack makes a defensible actuation decision.

Missing evidence is not a pass. A component PASS is never promoted to composition PASS without explicit composition evidence.

## Falsification and remediation

Every proposition in the YAML carries:

- a precise statement;
- an authority owner/status;
- source references;
- required evidence class;
- current evidence state;
- a falsification condition;
- remediation owner(s);
- dependent issue(s).

The falsification condition matters more than a generic acceptance statement: downstream tests should attempt to make the proposition false under controlled conditions.

When a proposition fails, RAHP should route the resulting obligation to the authority that can produce the missing substantive artifact — specification, profile, governance, implementation, specialist evidence producer or Interop Lab test harness — while RAHP remains the orchestration/reconciliation owner.

## Reassessment rule

Experimental evidence produced from a proposed upstream primitive is valid only against its exact source boundary.

If a cited PR head changes materially, an upstream proposal is merged/rejected/superseded, or a mutable design/discussion changes a pressure-test assumption:

1. preserve the historical result;
2. mark affected evidence stale where the proposition boundary changed;
3. pin the new source revision;
4. rerun only the propositions whose semantic/evidence boundary was affected;
5. do not rewrite the historical conclusion in place.

This is the same assurance-lineage principle used elsewhere in RAHP: a newer source boundary may supersede an old assessment, but it does not erase it.

## Downstream consumption

Issues #373–#379 MUST reference these proposition IDs rather than restating their own normative interpretation.

- #373 — correlation scope and disclosure semantics: `P01`–`P05`, `P13`
- #374 — VDC × VAC composition: `P06`, `P07`, `P09`, `P14`
- #375 — attenuation/lifecycle: `P08`, `P09`, `P14`
- #376 — hidden-subject proof composition: `P10`, `P13`, `P14`
- #377 — action-vocabulary governance: `P11`, `P14`
- #378 — node/credential applicability: `P01`, `P12`, `P14`
- #379 — end-to-end actuation: consumes all relevant prior evidence, with `P14` and `P15` as umbrella propositions.

## Verifiable Data Rooms boundary

[Verifiable Data Rooms](https://docs.fpp.storm.ws/data-rooms-concept.html) is valuable because it composes room identity, membership, authority, agents, privacy-preserving proofs, MLS and host portability into one implementation-shaped scenario.

It remains an **informative pressure test**. A Data Room requirement is not automatically a DTG requirement, and no Data Room-specific rule belongs in generic RAHP core unless independent evidence demonstrates a reusable assurance abstraction.

## Current judgment

The matrix does **not** conclude that the emerging DTG architecture is complete or incomplete. It establishes what must be separately tested before that conclusion can be made.

The most important architectural boundary to preserve through the wave is:

> Valid evidence at one layer must not silently manufacture the proposition owned by another layer.

That is what Tracks A–G now have to falsify.
