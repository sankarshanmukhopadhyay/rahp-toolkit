# Agent authority control — v1

Tracking: #970

`tools/agent_authority.py` is an optional deterministic profile control. It evaluates one bounded action against one supplied delegation document and supplied current-status evidence.

It **does not** authenticate an agent or principal, fetch registry/revocation state, infer capabilities, or grant runtime permission.

## Evaluated predicates
- requested capability is explicitly delegated;
- requested resource is within declared resource scope;
- evaluation time falls within delegation validity;
- supplied authoritative status is active;
- required human confirmation is evidenced;
- delegation depth does not exceed its declared maximum.

## Conservative outcomes
- Any known violated constraint -> **FAIL**.
- Missing resource scope, unavailable authoritative status, missing required confirmation evidence, or unavailable required depth evidence -> **INDETERMINATE**.
- **PASS** requires every applicable predicate to be satisfied.

This intentionally preserves RAHP's evidence-conservative semantics: a successful identity/credential check cannot manufacture action authority.

## Tests
`tests/test_agent_authority.py` covers:
- positive bounded merge action;
- read permission not implying merge permission;
- resource-scope expansion;
- expiry;
- revoked/suspended state;
- unavailable revocation state;
- human confirmation absent/denied;
- delegation-depth amplification;
- missing resource scope;
- input immutability.

## Boundary
The evaluator consumes already-resolved status evidence. A registry/TRQP/ARPA adapter may later supply that evidence, but external lookup is deliberately outside this portable control.
