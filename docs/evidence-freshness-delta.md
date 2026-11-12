---
layout: default
title: "Evidence provenance and freshness"
nav_order: 10
has_toc: true
parent: Operate assurance
---
# Evidence provenance, assurance freshness and delta

RAHP v1.5 development treats evidence provenance, assurance freshness and assessment-to-assessment change as separate but linked assurance objects.

The portable contracts are deployment-neutral. They apply equally to a specification, repository, implementation, service, dataset, governance process or composed system. DTG, OpenVTC, ARPA, CAWG/C2PA and other deployments may demonstrate the model but do not define it.

## Evidence provenance

`method/schema/evidence-manifest.schema.json` records the identity and provenance of consequential evidence, including:

- evidence type;
- source kind, locator and revision;
- production mechanism and workflow;
- observation time and optional validity bounds;
- integrity digest;
- authority class and basis; and
- assurance propositions or assessments supported by the evidence.

An evidence manifest is not itself proof that the evidence is sufficient. It makes the provenance required to evaluate sufficiency explicit and machine-verifiable.

## Assurance freshness

`method/schema/assurance-freshness.schema.json` describes whether an assessment run remains supportable after relevant changes.

Portable freshness states are:

```text
current
potentially-stale
stale
retest-required
superseded
indeterminate
```

Freshness is conservative. A change can invalidate or weaken the applicability of prior evidence without proving that the underlying system has become unsafe or non-conformant.

The reference helper derives freshness from explicit basis effects:

```text
supersedes      → superseded
requires-retest → retest-required
invalidating    → stale
unknown         → indeterminate
potential       → potentially-stale
otherwise       → current
```

`indeterminate` preserves uncertainty rather than silently converting missing knowledge into a pass.

The CLI and reference helper reject a missing, empty, or unsupported freshness-effect basis rather than returning `current`. A valid explicit `none` effect represents a checked basis with no freshness-changing effect. This input-contract rejection is not a new assurance status; it prevents malformed inputs from being interpreted as verified currency.

## Assurance delta

`method/schema/assurance-delta.schema.json` records the difference between two assessment runs. It separates:

- findings introduced, resolved, changed and unchanged;
- controls introduced, resolved, changed and unchanged;
- evidence introduced, resolved, changed and unchanged;
- previous/current assurance conclusions; and
- a classified conclusion transition.

Conclusion transitions include:

```text
unchanged
improved
degraded
resolved
regressed
indeterminate
```

A delta is evidence about change, not an authority decision. For example, `resolved` indicates that the current assurance conclusion moved from an adverse/residual state to a controlled/assured state; actual closure of a governed obligation remains subject to the remediation/retest authority model.

## Relationship to impact analysis

The portable lifecycle can now express:

```text
material change
  → graph impact selection
  → affected assessment
  → freshness evaluation
  → evidence retained / weakened / invalidated
  → reassessment or retest
  → assurance delta
  → governed disposition
```

Absence of a represented dependency or provenance record is not evidence of non-impact or current assurance.

## Validation

The deployment-neutral fixtures use a fictional payments specification:

```bash
python3 tools/validate_evidence_freshness_delta.py
python3 tools/assurance_state.py freshness examples/assurance-lineage/generic-assurance-freshness.yaml
python3 tools/assurance_state.py transition --previous finding --current controlled
```

Project-specific deployments MAY add stronger evidence validity, freshness or change-classification rules. They MUST NOT weaken these portable conservative semantics when claiming portable RAHP conformance.
