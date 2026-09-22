# RAHP threat model for independent review

## Security objective

RAHP must fail conservatively when assessment inputs, evidence, provenance or execution context are malformed, incomplete, stale, contradictory or adversarial. The security objective is not merely code execution safety; it includes preventing false assurance escalation.

## Assets

Material assets include assurance state, source identity and pins, evidence/provenance records, specialist results, normalized findings, reconciliation decisions, authority inputs, durable lineage, release/qualification evidence and reviewer-visible documentation.

## Adversaries and failure sources

The review should assume untrusted or compromised target repositories; malformed YAML/JSON and schemas; misleading metadata; stale evidence replay; duplicated or correlated evidence presented as independent; hostile dependency graphs; crafted source paths/identifiers; resource-exhaustion inputs; compromised or mistaken evidence producers; and ordinary implementation defects.

## Principal threat classes

| Threat | Failure mode | Required safe behaviour |
|---|---|---|
| Evidence omission | required evidence absent | INDETERMINATE/evidence-required or equivalent non-positive residual |
| Stale evidence replay | prior evidence reused after material change | freshness/retest state, never silent PASS |
| Provenance substitution | evidence belongs to wrong subject/revision | reject, quarantine or preserve explicit unresolved state |
| False independence | correlated sources counted as independent | no independence credit without basis |
| Specialist spoof/malformation | invalid specialist result enters reconciliation | validation failure or indeterminate; never synthesized PASS |
| Partial execution | workflow or stage completes incompletely | no terminal positive assurance from transport success |
| Composition laundering | component PASS presented as composition PASS | separate composition proposition/evidence required |
| Authority confusion | repository permission or policy PASS used as governance authority | independent authority check required |
| Normative drift | local interpretation silently replaces upstream semantics | source pin and explicit upstream authority preserved |
| Resource exhaustion | hostile scale/shape consumes unbounded resources | bounded failure should not fabricate an assurance result |
| Dependency/supply-chain drift | newer compatible dependency changes behaviour | CI detects regressions; reproducibility limitation remains explicit |

## Trust assumptions

The current toolkit assumes the Python runtime and installed dependencies are not malicious; Git/GitHub-provided immutable commit identifiers are correctly resolved by the execution environment; repository-local validators execute with the permissions of the runner; and external evidence authenticity is only as strong as the provenance/integrity mechanism recorded for it.

These are assumptions, not guarantees. The current dependency file uses minimum versions rather than a cryptographic lock, so bit-for-bit dependency reproduction is not claimed.

## Security review method

Reviewers should combine code review, negative fixtures, malformed-input testing, provenance substitution, stale replay, source-pin mutation, specialist-return mutation, duplicate-evidence tests and resource-boundary tests. A security test that merely demonstrates that a command exits zero is insufficient.

## Finding rule

Any path that can produce PASS/GREEN while a material required proposition lacks sufficient valid evidence is a high-materiality assurance defect regardless of whether conventional confidentiality/integrity/availability impact is demonstrated.
