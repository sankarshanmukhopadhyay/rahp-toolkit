# Agent assurance worked example

Tracking: #970

This example qualifies the portable Agentic Assurance Profile against:
1. pinned ARPA revision `9f6e5c75c421419500c8def21052cfa0b105b59b`; and
2. a bounded delegated Git repository merge action represented as local fixtures.

The local fixture is intentional: RAHP assesses supplied evidence and does not become a Git hosting authorization service.

## Run

```bash
python -m unittest tests.test_agent_authority tests.test_agent_continuity
```

## ARPA specification findings

Pinned ARPA sources examined:
- `docs/authority-at-commitment.md`
- `docs/authority-non-amplification.md`
- `docs/historical-authority-resolution.md`
- `examples/scenarios/delegated-action.md`
- `examples/valid/redress-record.json`

The specification supports:
- registration/authentication does not imply action authority;
- exact action/resource binding;
- current authority and lifecycle status;
- non-amplification of constraints;
- required approval binding;
- missing/stale/conflicting state is not allow;
- current and historical authority are distinct;
- delegated action evidence and redress are explicit.

RAHP does not claim ARPA conformance from documentary inspection alone.

## Bounded operation

The positive test represents principal `did:example:principal` delegating `repo.merge` for exactly `repo:qbf/example` to `did:example:agent`, with current status, required human confirmation and bounded delegation depth.

Negative tests demonstrate:
- `repo.read` cannot authorize `repo.merge`;
- another repository cannot be substituted;
- expired/revoked/suspended authority cannot authorize;
- unavailable status remains INDETERMINATE;
- required human confirmation cannot be skipped;
- delegation depth cannot amplify;
- handoff cannot change the root principal;
- child capabilities cannot exceed parent capabilities;
- substitution requires continuity evidence;
- redress requires linkage and closure evidence.

## Claim boundary

These are deterministic assurance fixtures. They do not prove live Git provider enforcement, cryptographic identity, registry availability, or legal authority. Those remain external evidence obligations.
