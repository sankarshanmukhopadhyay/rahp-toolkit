# RAHP open-issue queue rebaseline — 2026-10-18

**Purpose:** A defensible *point-in-time* classification of the [52 issues open in the downstream RAHP toolkit](../../data/assurance/queue-rebaseline-2026-10-18.json) after the October disposition tranche. This is a management/disposal baseline, **not** a checklist of issues falsely marked PASS. The complete per-issue list and titles are in the JSON file; the validator rejects omissions, duplicate IDs and inappropriate closure claims.

## Queue classification

| Class | Count | Intended execution/trigger |
| --- | ---: | --- |
| Controller reconciliation | 8 | Reconcile the full qualified finding roster; route combined/covered/no-action/DPIP, then close snapshot issue when all obligations have terminal decisions or transfers |
| Publication verification | 2 | Independently inspect live GitHub Pages /corpora/ and /docs/reasoning-worked-example/ routes; CI build alone not sufficient |
| Implementation/evidence | 23 | Bounded test, source pin or implementation/assurance evidence; preserve runtime unknowns |
| Upstream normative dependency | 6 | Check for authoritative specification/WD convergence, then selectively rebaseline; source hypotheses remain unverified |
| External privacy evidence | 7 | DPIP/retention/correlation evidence required; no blanket inference of privacy conformance |
| Bounded research | 4 | Run explicitly scoped evaluations; do not equate new code volume with portfolio progress |
| Independent human judgment | 1 | #915 needs attributable authorized human examination |
| Intentional dormancy | 1 | #973 remains open deliberately; reactivate only on external qualification trigger |
| **Total** | **52** | |

The eight exact snapshot controllers are **#1028, #1040, #1042, #1043, #1045, #1046, #1047 and #1054**. All 15 UNMAPPED entries in #1054 now have durable review owners, but the other 33 (`combined`, `covered`, `no-action`) have not been fully accounted for. The prior seven snapshots likewise require their non-UNMAPPED child reconciliation. Controller completion should be measured by **per-finding accountable disposition**, not disappearance from the current monitor snapshot.

## Closed/superseded administrative records

- #121 OpenVTC historical combined review and #527 historical Data Rooms wrapper are CLOSED and now explicitly protected by the opt-in terminal-wrapper routing mechanism from [PR #1059](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1059). Unseen material generates a separately tracked bounded successor; an explicit invalidation can still reopen.
- #1022 TEE bootstrap is CLOSED after its verified source/test assessment [PR #1055](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1055), but the upstream VTI-ACL-001 interpretation remains with VTI spec #64.
- #1016 DTG discovery availability is CLOSED via tested [PR #1050](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1050).
- #1041 HTX review is closed with explicit evidence limits.
- #1039 and #937 are **still OPEN** due to live-page acceptance gates. CI green is not equivalent to a browser observation.

## Active bounded work order

1. **Controller child audit.** Obtain a source-pinned list of all qualifying findings and corresponding routed children/DPIP statuses. Never close from an UNMAPPED-only ledger.
2. **Publication gates.** Verify public content and actual navigability; only then close #1039/#937.
3. **#272 late release deltas.** Finish per-spec/binding classification, avoiding wholesale version-bump equivalence.
4. **#958** release supply chain. Immutable Action pinning is merged in [PR #1060](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/1060), but hashed Python lock, effective token/environment access, private artifact/log retention and independent human verification remain.
5. **#928** reasoning. The optional trace, negative fixtures and cross-process synthetic replay exist; independent source-authenticated reviewer replay and governed challenge resolution remain.
6. **#994 / #1051 / #1057** downstream runtime and composed privacy packet. Start from the existing test matrices; add new cases only where an actual evidence gap requires it.
7. **Remaining external/privacy/research queue.** Preserve necessary waiting and deliberate dormancy, with next source/review trigger recorded before administrative disposal.

## Assurance and lifecycle rules

An **open count is not an assurance-quality measure**. Only close a bounded review when its originally scoped question is assessed and all residual obligations have named, accepted owners. Never claim runtime or source conformance from schema validity, successful CI, an upstream closed PR, or a missing issue. For each material engineering PR, retain test commands, exact source versions, negative cases, evidence limits and any human authorization gate.

### Reproduction

```bash
python3 tools/validate_queue_rebaseline.py
python3 -m unittest tests.test_queue_rebaseline -v
```

This validation checks the completeness and internal consistency of the captured **2026-10-18 inventory**. It does **not** query GitHub live or assert that the same issues remain open tomorrow. A subsequent review must take a new immutable dated snapshot rather than silently changing the historical one.
