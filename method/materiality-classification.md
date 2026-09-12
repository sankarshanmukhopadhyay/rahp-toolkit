# Materiality classification

RAHP's DTG instance separates **change detection**, **materiality classification**, **assurance routing**, and **durable proposition ownership**. These are related stages but they do not have the same semantics.

## Decision path

The intended path is:

`raw change → semantic classification → materiality reason → assurance-surface intersection → routing → durable proposition owner`

A configured repository path is therefore a materiality **signal**, not the sole admission gate. This prevents an incomplete external registry path profile from hiding a normative or implementation change that clearly intersects an assurance surface.

## Assurance surfaces

The DTG adapter uses a bounded vocabulary:

- `normative-semantics`
- `authority-and-delegation`
- `credential-lifecycle-status`
- `execution-and-outcome`
- `privacy-correlation-disclosure`
- `key-custody-export-signing`
- `identity-binding-resolution`
- `governance-policy-redress`
- `interop-composition-contract`
- `evidence-observability-audit`

A path can intersect more than one surface. Surface classification is evidence for materiality; it is not an assurance verdict and does not determine PASS, FAIL, DPIP applicability, or remediation.

## Classification sources

The classifier records why a path was admitted. Sources include configured material paths, instance-wide always-material paths, role-aware semantic paths, semantic tokens, and a conservative implementation-source fallback.

Normative specification roles receive first-class treatment for `spec/`, `specs/`, schemas, and term-definition surfaces even when the external portfolio registry omitted those paths. Implementation roles similarly inspect changed source paths for assurance-relevant semantic tokens rather than requiring a prior registry match.

Unknown implementation semantics are not silently converted to no-action. An implementation source path that cannot be mapped confidently remains visible as triage unless another high-confidence materiality signal justifies assessment.

## Low-value fan-out

Generated code, evidence-only changes, release propagation, manifests, and documentation retain their existing bounded treatment. Volume does not allow low-weight fan-out to mask one high-value semantic change, and volume alone does not create an assurance conclusion.

Documentation-only changes for roles configured for documentation triage remain triage rather than broad assessment.

## Calibration fixtures

Historical queue records provide regression evidence:

- **#601** demonstrated under-classification: workflow files were admitted while the large `spec/body.md` WD02 normative change was outside material scope. A normative body change must now be admitted through the `normative-semantics` surface even when the registry path profile is incomplete.
- **#604** demonstrated misleading scope: a one-line design-document change was admitted while substantial persona binding, correlation, disclosure, and state-handler implementation changes were outside material scope. Those implementation paths must now be admitted through their semantic assurance surfaces.
- Known-good Trust Tasks and VTI material detections remain regression fixtures so calibration does not merely make the monitor quieter.

## Non-inference

- new SHA ≠ material assurance change;
- configured path match ≠ assurance impact;
- semantic surface match ≠ finding;
- large diff ≠ high materiality;
- small diff ≠ low materiality;
- unknown semantics ≠ no-action;
- materiality classification ≠ routing or proposition disposition.

This model deliberately improves explainability and recall before changing global thresholds. Threshold tuning should be evidence-driven and independently testable rather than used to compensate for incomplete semantic classification.
