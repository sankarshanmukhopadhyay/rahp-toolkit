# Known limitations and residual risk

This document is intentionally part of the independent-review surface. It records boundaries that must not be hidden by a successful validation run.

## Current limitations

1. **Dependency resolution is not bit-reproducible.** `requirements.txt` specifies compatible minimum versions rather than a hash-pinned lock. CI fixes Python at 3.11 but can resolve newer compatible packages. Review reproduction can therefore establish functional reproducibility, not identical dependency bytes.
2. **External source availability is not controlled by RAHP.** Source-pinned assessments can preserve the identity used for reasoning, but later retrieval of external repositories, artifacts or governance evidence depends on their retention and access.
3. **Evidence authenticity is bounded by provenance mechanisms.** A digest and immutable locator support integrity checking; they do not independently prove that an observation was honestly produced or that the producer was authoritative.
4. **Graph completeness is not guaranteed.** Absence of a represented dependency is not evidence of non-impact. Impact analysis is only as complete as the represented graph.
5. **Specialist coverage is bounded.** A specialist boundary can preserve uncertainty correctly without providing the missing specialist evidence. Privacy composition can therefore remain indeterminate.
6. **Synthetic fixtures are not realization evidence.** Conformance and negative fixtures exercise semantics but cannot substitute for genuine implementation-pair, runtime or operational evidence where the proposition requires those classes.
7. **Resource-exhaustion resistance is not claimed as comprehensively qualified.** The review threat model calls for hostile-scale testing; current qualification primarily establishes semantic and functional invariants.
8. **Release qualification is not independent review.** v2.4.0 qualification demonstrates the repository-defined release contract. It does not prove absence of defects or substitute for external scrutiny.
9. **AI assistance is not assurance evidence.** AI can assist analysis and drafting, but a model output does not satisfy an evidence obligation merely by being plausible.

## Residual-risk handling

A limitation may be narrowed only by attributable evidence. Until then, dependent claims must remain bounded, evidence-required, indeterminate or otherwise explicitly qualified. Review findings should not be closed by wording changes when the underlying evidence gap remains.
