# Distributed Resilience and Amplification Risk Model

This directory contains RAHP's portable DRARM method data.

- `catalogue.yaml` defines reusable risks, controls, evidence expectations and assurance levels.
- `detectors.yaml` defines replaceable static evidence signals used by the Python reference adapter.
- `../mappings/resilience-to-assurance.yaml` defines the authoritative mappings from DRARM rules into portable RAHP assurance patterns where semantic equivalence exists.

The catalogue is portable. Detectors are non-normative evidence adapters and must not be confused with proof that a control is absent or present.

## Controller integration

DRARM remains independently executable through the resilience assessment command, but controller-driven assessment records now make resilience disposition explicit. A run records resilience as one of:

- `executed`;
- `not-applicable`, with decision provenance; or
- `required-but-not-executed`.

The controller resolves applicability from explicit target-class and profile policy. Ambiguous applicability remains unresolved rather than being inferred from source-text keywords. `profiles/resilience/default.yaml` contains the portable default policy; `tools/resilience_router.py` invokes the existing `resilience_assess.py` evaluator when that policy requires DRARM.

`combined` retains its existing RAHP + security meaning. DRARM integration does not redefine that CLI mode.

## Propositions and mappings

`tools/resilience_propositions.py` converts DRARM findings and review-required signals into source-preserving resilience propositions. Each proposition retains the exact `RLA-*` source rule and target provenance. Portable `RKP` / `CTP` / `GRP` / `ATP` mappings are attached only when they are present in `method/mappings/resilience-to-assurance.yaml`.

An unmapped rule remains a first-class resilience obligation. It MUST NOT be forced into an unrelated portable pattern merely to create graph coverage.

Static detector output is evidence triage. A DRARM `finding` or `review-required` signal becomes an `evidence-required` proposition; it is not, by itself, a terminal assurance result.

## Runtime evidence obligations

Higher-assurance claims can require evidence that static review cannot produce. `tools/resilience_evidence.py` creates deterministic evidence obligations bound to the DRARM proposition and exact target revision. The required DR assurance depth (`DR-A1` through `DR-A5`) is supplied explicitly; RAHP does not infer an assurance level from an evidence-class name.

RAHP owns:

- the proposition;
- the evidence obligation;
- the required assurance depth;
- state transition and reconciliation.

An external producer such as target CI, an interoperability lab, conformance harness or deployment test system owns:

- execution and measurement;
- the evidence artifact;
- producer provenance.

Evidence returns are matched to the exact obligation, DRARM rule, target revision and evidence class. Missing, mismatched, malformed or insufficient-depth evidence leaves the obligation unsatisfied. Missing evidence is never interpreted as PASS.

Runtime traces and large test artifacts follow `method/evidence-retention.yaml`: they normally remain referenced evidence outside the repository with immutable/versioned location and integrity metadata, while the durable RAHP record preserves the proposition, disposition and evidence reference.
