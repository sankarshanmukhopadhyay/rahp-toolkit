# Agent assurance I1 — cross-portfolio revision pins

Tracking: #970

Verified on 2026-10-09 through repository metadata.

| Workstream | Canonical repository checked | Pinned revision | Evidence state | Dependency decision |
| --- | --- | --- | --- | --- |
| ARPA | `qbf-consulting/agent-registry-protocol` | `9f6e5c75c421419500c8def21052cfa0b105b59b` | verified repository/revision | REFERENCE + QUALIFY; worked-spec input |
| TRQP | `sankarshanmukhopadhyay/tswg-trust-registry-protocol` | `009c589ffa4e3098c7700a19b007505d6a29c30a` | verified repository/revision | REFERENCE; not portable-core dependency |
| DTFC | `qbf-consulting/digital-trust-failure-corpus` | `319c8930bf98d8993a5fe1c0774a8d92d0c1edc0` | verified repository/revision | REUSE candidate; not portable-core dependency |
| ARA / Interop Lab | issue text named `trustoverip/trust-protocol-interop-lab` | none | **unresolved canonical path** | do not claim executable reuse from that path; Track-G retains a separately pinned historical `sankarshanmukhopadhyay/trust-protocol-interop-lab` commit as evidence |
| TSMS / TSMM | issue text named `qbf-consulting/trust-systems-modelling-methodology` | none | **unresolved canonical path** | DEFER; cannot block agent profile |
| GAAM / ONDTF | exact relevant assets not established | none | not examined | DEFER as planned |

## Judgment
Portable AAP functionality must not acquire a hard dependency on any portfolio repository. External projects own their semantics; RAHP consumes pinned evidence. An unresolved discovery link is recorded as unavailable rather than silently substituted.

The I5 worked examination therefore uses the verified ARPA pin for specification examination and a local schema-compatible bounded Git-operation fixture for execution qualification. This keeps the examination reproducible even if an external demo repository or lab changes.
