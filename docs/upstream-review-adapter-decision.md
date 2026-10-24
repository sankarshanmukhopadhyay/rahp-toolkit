# Decision: upstream specification-review adapter demand

**Tracking:** ToIP RAHP Task Force convergence issue #17, Increment 6.  
**Disposition:** **No generic adapter for the three inspected Python entry points** at the pinned baseline; reopen upon evidence of a concrete consumer. This decision does not establish exhaustive absence of dynamic or external consumers.

## Authority and source pins

- Upstream review records: accepted task-force source `448e2ff4ca7f747ca899e0e845adfe45f750f094`; canonical `rahp-spec-review/v1` and historical VRC `SR-201`/`SR-202` records.
- Downstream source inspected: `62daf6b1ffc1051c7ecd0c476ad987b78e54b750` and the PR's subsequent narrow execution code.
- Source-derived input: actual `tools/review.py`, `tools/assessor_contract.py`, `tools/evidence_provenance_router.py` function/interface definitions, with related downstream review-mode documentation and architecture convergence matrix.
- Prior constraints: upstream review boundary PR #1138 and example evidence/reassessment boundary PR #1139, both already merged downstream. These do not prove a general upstream-to-downstream converter is needed.

## Consumer inventory and qualification

| Inspected surface | Actual interface and authority | Upstream review ingestion found? | Disposition |
| --- | --- | --- | --- |
| `tools/review.py` | Initializes/validates downstream pressure-test, security and combined review records. Downstream target uses `commit`, not upstream `target.revision`; a reviewer authors findings. | No direct `rahp-spec-review/v1` or `validate_spec_review` reference in named entry point. | **No adapter justified** absent an integration request. |
| `tools/assessor_contract.py` | Explicit `normalize_external` API needs assessor, assessment ID, outcome, reason code, evidence, residual risk and action. | No direct upstream review parser. These authoritative judgment inputs cannot be derived solely from upstream finding status. | **Do not infer terminal assurance**; deliberate separation. |
| `tools/evidence_provenance_router.py` | Routes provenance-insufficient specialist returns and external evidence obligations after a real producer/specialist event. | No direct upstream review parser. | Review records are not a replacement for target-attributable operational evidence. |

**Limitations:** This is a bounded examination of named Python entry points, not a complete runtime call-graph proof. Repository automation, third-party integrations and dynamic consumers outside the examined files are not excluded by a negative text-reference check. Findings must be revisited if actual callers or accepted schemas change. The evidence-bearing script fails closed if expected entry points disappear or a direct upstream contract reference emerges.

## Worked VRC reassessment demand experiment

The executable experiment reads retained VRC baseline and reassessed reviews from the pinned upstream checkout and confirms that `F-001` moves `open → resolved` while `F-002` remains `open → open`, on **different immutable source revisions**. It inspects downstream entry-point contracts and refuses to treat these finding states as downstream specialist `PASS`, controller `GREEN`, risk acceptance, or operator authorization.

**This is not successful ingestion through a downstream consumer.** It is a controlled **consumer qualification** experiment. Its falsifiable result is that the three named interfaces do not expose a demonstrated direct requirement for `rahp-spec-review/v1` ingestion; no adapter acceptance criteria can therefore be derived without inventing demand.

```sh
python3 -m unittest discover -s tests -p 'test_upstream_review_consumer_decision.py' -v
python3 tools/upstream_review_consumer_decision.py --upstream /path/to/pinned/upstream --downstream . --output decision.json
```

CI runs the same check in the existing `validate.yml` workflow with the immutable upstream revision; it retains JSON evidence. The source pin and CI run must be recorded before treating this disposition as qualified.

## Alternatives and explicit decision

1. **No adapter (chosen):** Keep upstream review records and example evaluators authoritative; reuse the source-pinned boundary checks now merged downstream.
2. **Documentation/profile:** Reasonable only when a named adopter requests interpretation or field guidance; this document already supplies the known distinctions.
3. **Bounded adapter:** Justified only after a named consumer supplies an actual upstream review, an expected downstream behavior, a reproducible failure, a minimal reviewed mapping and negative tests proving no authority escalation.
4. **Shared schema/method migration:** Not justified by the inspected interfaces. Requires separate upstream method authority and independent semantic governance.

**Reopen conditions:** A real consumer must demonstrate demand by supplying pinned VRC/TRQP review input, the downstream API or workflow requiring it, an explicit authorized result, and a failing test. Distinguish incomplete/unknown evidence from assurance PASS; preserve source and lifecycle history. A mapping must not silently translate `resolved` into `PASS`, `risk_accepted` into valid authorization, or successful validation into review/acceptance authority.

## Remaining Increment 6 / 7 boundaries

The completed engineering verifies accepted upstream contracts and identifies three inspected non-consumers. It does **not** establish general schema equivalence, exhaustive adoption, or a complete downstream consumer integration. Upstream Increment 6 closure still depends on its full acceptance criteria; Increment 7 still needs an unfamiliar adopter. No release is warranted by this decision-only contribution.

**Provenance:** AI-assisted examination and implementation, with separate machine-readable results and human-readable reasoning. Independent reviewability applies. The repository owner may accept under governing policy but no independent approval is claimed unless provided.
