# Portable assessor-result contract

`rahp-assessor-result/v1` is RAHP's portable specialist-assessor return contract.

## Authority

The authoritative machine-readable schema is:

`schemas/rahp-assessor-result-v1.schema.json`

`tools/assessor_contract.py` consumes that schema directly. The legacy file at `method/schema/assessor-result.schema.json` is retained only as a compatibility mirror for existing repository references and is constrained by executable equivalence tests. It is not a second source of contract meaning.

## v1 validation boundary

A v1 assessor result requires:

- `schema = rahp-assessor-result/v1`;
- assessor and assessment identifiers;
- one of `PASS`, `FAIL`, `INDETERMINATE`, or `NOT_APPLICABLE`;
- a non-empty reason code;
- unique string evidence references in `evidence_used`;
- residual risk and required action text.

Optional generic transport/context fields are `source_pins`, `provenance`, and `details`. Target- or specialist-specific semantics belong under those generic extension containers where appropriate; they do not widen the top-level RAHP contract.

The previously duplicated permissive representation admitted object-valued `evidence_used`, `boundedness`, `confidence`, arbitrary top-level properties and other shapes that the live RAHP consumer rejected. Those shapes were never portable through the actual RAHP consumer and are not part of the authoritative v1 boundary.

## Assurance boundary

A schema-valid specialist result proves contract compatibility only. In particular:

- specialist `PASS` is not terminal RAHP assurance `PASS`;
- workflow success is not assurance success;
- missing or incomplete evidence must not be promoted to `PASS`;
- specialist claim boundaries, residual uncertainty and evidence maturity remain inputs to RAHP reconciliation.

## External producers

External producers should validate against the authoritative schema before delivery. Producer and consumer CI should share representative fixtures for positive, negative, incomplete and bounded results so contract drift becomes visible before cross-repository execution.

The DPIP privacy-observability return proven through Interop Lab #193 is a current reference producer for this contract.

## Read-only external-return diagnostics

A third-party consumer may check an external result against its *actual
addressed obligation* without running a RAHP controller:

```bash
python3 tools/validate_external_assurance_result.py --kind producer \
  --result /path/to/producer-result.json --obligation /path/to/obligation.json
python3 tools/validate_external_assurance_result.py --kind assessor \
  --result /path/to/assessor-result.json --obligation /path/to/obligation.json \
  --expected-assessment-id 'controller-supplied-assessment-id'
```

The command invokes the canonical v1 validators and checks available
proposition/evidence-contract keys, requirement IDs and exact declared source
pins. The assessor contract does **not** declare a proposition key or
independently authenticate its assessment ID, so the caller must provide
the controller-issued assessment ID; absent context returns `NOT_ESTABLISHED`.
Use `--previous-result` to reject an identical or conflicting return under
the same producer execution ID or assessor assessment ID. Without a previous
return, the command cannot prove a delivery is the first or that a remote
service has not replayed it.

Machine JSON output distinguishes `VALID_BOUND_CONTRACT`,
`INVALID_CONTRACT`, `REJECTED_BINDING`, `NOT_ESTABLISHED` and
`INVALID_INPUT`. Only `VALID_BOUND_CONTRACT` exits zero. Even that status
is limited to **structural/declared-context consistency**:
`authenticated: false` and `assurance_determination: null` are always
returned. An executable producer's `succeeded` status does not prove
sufficient evidence; a specialist's portable `PASS` cannot authorize
terminalization. The command performs no network requests, evidence admission,
controller mutations, specialist dispatch or registry publication.

Run the public-interface regression tests with:

```bash
python3 -m unittest tests.test_external_assurance_result_cli -v
```

Obligation provenance, freshness beyond the declared source pins, caller
authentication, source signature verification and live transport retries
remain the responsibility of their existing authoritative producers and
controllers. Do not infer them from this validator.

## Fault-containment coverage inventory (#1190)

This inventory distinguishes checks on the **actual supported consumer entry point**
from tests of internal helpers. The public return command is
`tools/validate_external_assurance_result.py`; the underlying v1 validators
remain the contract authorities. Tests in
`tests/test_external_assurance_result_cli.py` execute the CLI as a subprocess.

| Fault | Consumer-facing evidence | Boundary |
| --- | --- | --- |
| Wrong proposition/contract key/requirement | `test_wrong_proposition_revision_and_requirements_rejected` | Rejected against a supplied valid obligation; no source-owner authentication |
| Wrong target source revision | Same test and `tests/test_evidence_producer_result.py` | Checks declared pins; cannot prove current authoritative revision |
| Duplicate return under same execution identity | `test_duplicate_and_conflicting_retries_fail_closed` | Requires prior return provided by caller; not an integrated replay store |
| Contradictory return under same identity | Same test | Rejects conflicting payload; does not adjudicate substantive disagreement across distinct runs |
| Unsupported v1 contract version/malformed return | `test_unknown_version_and_malformed_return_rejected` | Contract-invalid, no terminal outcome |
| Missing obligation/context | `test_missing_context_and_unavailable_evidence_are_not_success` | `NOT_ESTABLISHED`, not fabricated binding |
| Incomplete evidence / failed execution | `test_execution_failure_and_unavailable_evidence_have_distinct_diagnostics` | Retains distinct producer execution and evidence states; neither is assurance success |
| Wrong assessor assessment ID or evidence relationship | `test_assessor_context_misbinding_and_non_authorization` and `test_assessor_unrelated_evidence_and_positive_claim_do_not_authorize` | Caller-supplied controller identity; portable assessor contract lacks intrinsic proposition-key binding |
| Network timeout, delivery retry, concurrency, out-of-order receipt | **Not exercised through this offline CLI** | Requires an independently qualified transport/consumer environment; do not claim production fault containment |
| Materially stale evidence, revoked authority or historical applicability | **Not established** from declared pin equality alone | Requires authoritative freshness, revocation and effective-time inputs |

The **two bounded additional diagnostic gaps** addressed in the tranche were
wrong addressed-obligation binding and duplicate/conflicting return identity.
Other negative tests exercise existing contract boundaries without creating
new assurance-state or transport semantics. Tests show that rejected or
unavailable inputs cannot become a *successful validation receipt*. They do
not independently prove what a remote controller would do with those inputs.

The interface returns `VALID_BOUND_CONTRACT` only for consistency with the
supplied context, never independent authenticity or a controller decision.
The distinction between an evaluated specialist residual and an authoritative
RAHP outcome remains explicit: portable assessor `outcome` and `residual_risk`
are **input claims**, and `assurance_determination` is always `null`.
Simulation or local contract validation is not operational transport assurance.
