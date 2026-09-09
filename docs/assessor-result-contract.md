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
