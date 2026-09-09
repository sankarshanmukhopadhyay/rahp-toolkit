# Interop → RAHP pattern graduation

Tracking: [RAHP #491](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/491)

The Interop Lab is allowed to discover new assurance questions before their reusable meaning is stable. RAHP's generic catalogue should absorb only the concepts that survive replacement of the original implementation/protocol target without changing meaning.

The governing question is:

> If the original target were replaced tomorrow, would this assurance proposition still mean the same thing?

A second question follows immediately:

> Is the proposition already represented by an existing generic pattern without semantic distortion?

The default answer to a proposed new core pattern is therefore **no** until both questions are satisfied with evidence.

## Current candidate disposition

The machine-readable decision record is `method/catalogue/interop-graduation-dispositions.yaml`; CI validates its references and portability claims.

| Candidate | Disposition | Judgment |
|---|---|---|
| Action-time authority integrity | already covered | Reuse `ATP-AUTH-01`, `ATP-AUTH-02`, `ATP-COMP-02`, `ATP-OPS-02`; stronger examples are preferable to another overlapping pattern. |
| Evidence / historical validity → authority substitution | already covered | Reuse `ATP-AUTH-01`, `ATP-COMP-01`, `ATP-DEL-03`; evidence or lineage remains distinct from current authority. |
| Common-control / same-subject integrity | defer | Keep the residual coordinated through #500. Candidate constructions are not normative interoperability semantics. |
| Operator / effective-control independence | profile-specific | DTG Data Rooms P-ROOM-011 remains the concrete owner. Existing governance/dependency controls are adjacent, but a second independent consumer with equivalent evidence semantics is still missing. |
| Retrieved-content / authority separation | already covered | Existing authorization, agent-mandate and semantic-seam patterns already prohibit content presence/readability from enlarging authority. Target-specific injection/retrieval execution stays in the Lab. |
| Provenance across recall/composition | profile-specific | Persona P-PER-003 is concrete; delegation/action provenance is adjacent but not yet evidence-equivalent to arbitrary shared-memory recall. Do not over-generalise from one family. |
| Human-facing untrusted-content handling | Lab-only | Retain adversarial rendering pressure in the Lab until a second consumer and reusable evidence contract establish a generic assurance primitive. |

This outcome is intentionally conservative: the graduation exercise did **not** justify adding a new generic catalogue pattern in this tranche.

## Why the apparently reusable candidates did not all graduate

### Effective-control independence

The Data Room proposition is well-formed: distinct services, endpoints, identifiers or cryptographic actors are not evidence of independent control. RAHP already has governance/dependency controls that help assess this, including independent governance checks and dependency-control/exit analysis. However, the current repository evidence does not yet demonstrate an equivalent non-DTG consumer with the same assurance/evidence boundary. The proposition therefore stays profile-owned until portability is evidenced rather than assumed.

### Provenance across recall/composition

RAHP already understands delegation provenance and externally consequential action provenance. Persona P-PER-003 adds a different question: whether materialisation, projection, resolution, recall or composition preserves enough source state to distinguish supported, inline, superseded or differently-authorized content. Those concerns are related, not identical. A premature merge into an existing provenance pattern would hide that distinction; a premature new pattern would freeze a single DTG-shaped interpretation.

### Human-facing untrusted content

Authorization to store/retrieve content is not evidence that active or deceptive content is safe to render. The concern is real, but the current pressure case is still scenario/security-bound. Graduation requires reusable assurance meaning and an evidence contract, not merely a plausible generic sentence.

## Portability evidence

For candidates classified `already-covered`, the machine record requires two scenario families:

1. one DTG-derived consumer; and
2. one independent/generic consumer.

The validation test additionally proves that the referenced `ATP-*` records contain none of the forbidden target vocabulary (`OpenVTC`, `VDC`, `VAC`, `VMC`, `Trust Task`, `Data Room`, `Persona`). This is a narrow but useful executable guard against target semantics leaking into the generic catalogue.

The portability claim is about **assurance meaning**, not about identical implementation runners. Interop execution remains target-specific.

## Future graduation checklist

A future Interop-derived proposal should be reviewed in this order:

1. **State the proposition without target nouns.** If that changes the meaning, keep it profile/Lab-specific.
2. **Map existing catalogue semantics first.** Prefer `already-covered` or `pattern-refinement` over a new pattern.
3. **Name the evidence class and claim boundary.** Workflow success or a local test PASS is not sufficient.
4. **Show a second consumer where feasible.** Prefer one original/DTG-derived and one independent/generic consumer.
5. **Test negative/adversarial behavior.** Positive examples alone do not establish a reusable assurance boundary.
6. **Preserve ownership.** Privacy-specific meaning stays DPIP-owned; target execution stays in the Lab; RAHP owns only generic assurance meaning/reconciliation.
7. **Keep unresolved normative dependencies unresolved.** A candidate proof construction must not be promoted as settled semantics.
8. **Add executable catalogue validation before promotion.** A generic pattern should be testable and vocabulary-neutral.
9. **Clean up duplicates after graduation.** Profile/Lab records should reference the graduated RAHP meaning while retaining their target-specific proposition IDs and evidence.

## Incubation lifecycle

```text
Interop experiment / pressure case
        ↓
repeated assurance concern
        ↓
candidate target-neutral proposition
        ↓
existing-catalogue comparison
        ↓
portability + negative evidence
        ↓
ALREADY COVERED / REFINE / NEW GENERIC PATTERN
        ↓
profile/Lab mapping cleanup
```

A candidate may remain `profile-specific`, `specialist-owned`, `Lab-only`, or `defer` indefinitely if the evidence does not justify graduation. That is a successful judgment outcome, not a failure of the graduation process.
