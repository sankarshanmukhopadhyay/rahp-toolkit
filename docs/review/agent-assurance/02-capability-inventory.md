# Agent assurance I1 — capability inventory

Tracking: #970

| Capability | Current surface | Evidence state | Initial decision |
| --- | --- | --- | --- |
| Generic lifecycle and terminal reconciliation | engine contract + controllers documented in reasoning architecture | documented + machine contract | REUSE |
| Finite specialist outcomes | assessor-result v1 | machine contract | REUSE |
| Evidence provenance and authority class | evidence-manifest schema | machine contract | REUSE |
| Evidence adequacy for missing/conflicting/unavailable observations | optional R1 evaluator | documented executable profile | REUSE/EXTEND after tests are mapped |
| Authority grants and status | authority schema | machine contract | REUSE/EXTEND |
| Delegated principal/delegate scope | delegation-scope v0.4 | machine contract | REUSE/EXTEND |
| Human-confirmation declaration | delegation-scope constraint | structural only in this baseline | QUALIFY enforcement |
| Delegation depth | delegation-scope constraint | structural only in this baseline | QUALIFY enforcement |
| Resource/action binding | authority + delegation scopes | partial structural coverage | EXTEND only if executable gap confirmed |
| Temporal validity/revocation | authority/delegation schemas; temporal profile exists separately | partial | QUALIFY composition |
| Agent substitution continuity | linked issue #172 | not re-proven in this PR | VERIFY |
| Confused-deputy context binding | linked issue #177 | not re-proven in this PR | VERIFY |
| Delegation laundering / hidden principal | linked issue #165 | not re-proven in this PR | VERIFY |
| Composition authority attenuation | linked issues #186/#379 | not re-proven in this PR | VERIFY |
| External agent invocation | reasoning integration guidance | documented | REUSE boundary |
| Agent identity authentication | explicitly outside automatic RAHP boundary | missing as generic automatic capability | REFERENCE/QUALIFY, not silently add |

## Rule
“Present in a schema” means structural expressibility, not operational enforcement. A capability moves to VERIFIED EXECUTABLE only when its implementation and positive/negative tests are cited and reproduced.
