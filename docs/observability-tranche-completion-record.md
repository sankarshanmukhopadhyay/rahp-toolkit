# Observability-harm tranche: cross-repository completion record

**Scope:** bounded synthetic observability examination and portable DTFC-to-RAHP fixture consumption. **Status:** implementation merged; operational deployment assurance not established.

## Work ledger

| Unit | DTFC | RAHP | Result |
| --- | --- | --- | --- |
| Original experimental evaluator, regression tests and reconciliation | [Issue #105](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/105), [PR #106](https://github.com/qbf-consulting/digital-trust-failure-corpus/pull/106), `bb1ec2304643040836da348f0f1ca4e08d9dfbbb` | [Issue #981](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/981), [PR #982](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/982), `370519fcdf3626d01f0d5b20d36da9a2110ee20b` | Merged |
| Portable source vectors and pinned consumer | [Issue #107](https://github.com/qbf-consulting/digital-trust-failure-corpus/issues/107), [PR #108](https://github.com/qbf-consulting/digital-trust-failure-corpus/pull/108), `8c2a4ef1d8cefaa1457861bc5ecbd0c9f93afecf` | [Issue #983](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/983), [PR #984](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/pull/984), `dc45a2ed538831f57bf93a9d36b7cde6aada5066` | Merged |

All four issues were closed with their respective experimental-scope dispositions. All four PRs had successful GitHub Actions validation prior to squash merge. GitHub PR check histories are the authoritative CI records; this document does not embed immutable workflow-run evidence for every job.

## Acceptance and claims ledger

| Proposition | Evidence | Disposition |
| --- | --- | --- |
| Reused trace across contexts is negatively detected | OBS-NEG-01 and regression | **Implemented/tested (synthetic)** |
| Telemetry alone cannot justify a consequential action under this helper | OBS-NEG-03 and regression | **Implemented/tested (synthetic)** |
| Missing evidence does not become positive assurance | OBS-NEG-02 and regression | **Implemented/tested (synthetic)** |
| No observed failure is not proof of safety | OBS-NEG-04 and regression | **Implemented/tested (synthetic)** |
| Consumer sees an exact reviewed fixture snapshot | RAHP vendored JSON plus pinned Git blob test | **Implemented/tested (repository)** |
| Operational telemetry is complete, truthful and unlinkable | No real deployment input or independent collector | **Not established** |
| Retention, access, deletion and backup controls work in practice | No live processor/control test | **Not established** |
| Consequential decisions are independently authorized in deployment | No external authorization/decision trace | **Not established** |
| New canonical case IDs or controller semantics needed | Existing thematic coverage, no demonstrated gap | **Not introduced** |
| Release qualification | No new standalone release warranted solely by synthetic fixture increment | **Separately gated** |

## Assurance interpretation

A synthetic `FAIL` demonstrates that the helper recognizes an author-supplied negative proposition. `INDETERMINATE` prevents false positive assurance when observation is insufficient or apparently clean. Neither result proves that any actual system behaved as asserted. No target-system adapter, independent reviewer, attested collection process, or operational data handling was introduced.

## Known design limits

The evaluator reports one reason, potentially hiding simultaneous failure mechanisms. Its inputs are self-reported dictionaries; it does not independently verify context, trace linkage, decision source or `evidence_state`. Its `consequential_action` detection is narrow and does not inspect all possible positive authorization outcomes. The fixture contract does not cover deletion, retention, access logging, adversarial manipulation of event streams, or evidence provenance. A pinned Git blob detects local drift, not source authenticity or incident truth.

## Maintenance ownership

DTFC owns the canonical synthetic vector file and semantic version of the vector contract; RAHP owns its imported snapshot and consumer tests. Change the source first, review its implications, update the RAHP pin in a separate PR, and verify both repositories. A downstream digest mismatch is a compatibility signal, not an assurance finding.

## Documentation entry points

- DTFC: `docs/observability-induced-harm.md`, `docs/observability-vector-reference.md`, `research/observability/synthetic-vectors-v1.json`.
- RAHP: `docs/observability-induced-harm.md`, `docs/observability-dtfc-consumer-guide.md`, `examples/observability-dtfc/synthetic-vectors-v1.json`.
- This record is a historical evidence map; it does not substitute for GitHub's underlying commits and workflow logs.
