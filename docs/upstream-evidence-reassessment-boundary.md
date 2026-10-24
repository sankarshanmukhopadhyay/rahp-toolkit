# Upstream RAHP evidence-binding and reassessment boundary

Tracking: ToIP RAHP Task Force convergence issue #17, Increment 6.

## Source and claim

Pin accepted upstream `448e2ff4ca7f747ca899e0e845adfe45f750f094` and downstream baseline `5ba6a16cb67dfb801bf1cd41618626119a9d7510`. This contribution executes upstream's **own** TRQP `review/examine.py` and VRC `review/examples/vrc-v03/evaluate.py`, under a trusted upstream checkout. It does not translate or import example-specific sidecars as canonical downstream evidence contracts.

Both examples are examined from disposable **copies**; retained upstream source/records are not modified. The source-pinned CI run produces a JSON case matrix and retains it as a workflow artifact.

## Reproduce

```sh
python3 -m unittest discover -s tests -p 'test_upstream_evidence_boundary.py' -v
python3 tools/upstream_evidence_boundary.py --upstream /path/to/pinned/upstream --output evidence-boundary.json
```

Ten cases are asserted: original TRQP and VRC evaluations must pass; the following eight variants must fail.

| Example | Negative variants | Intended boundary |
| --- | --- | --- |
| TRQP | changed retained source | Source digest/identity cannot be bypassed |
| TRQP | wrong assessment ID | Evidence must identify reviewed assessment |
| TRQP | missing finding-evidence reference | No finding is silently considered covered |
| TRQP | incomplete execution | Incomplete execution cannot become assurance success |
| VRC | changed revised source | Retained source identity cannot be inherited |
| VRC | reused revision | Reassessment cannot silently claim the old source |
| VRC | missing evidence reference | Evidence closure cannot be inferred |
| VRC | false closure of still-open residual finding | Historical unresolved risk cannot silently become resolved |

## Interpretation and governance

Upstream TRQP and VRC use different **example-local** sidecar formats; their shared ideas are immutable target/method identity, review and corpus bindings, evidence references, observation versus inference, limitations and failure on stale/missing/contradictory evidence. These observations do **not** constitute a normative shared sidecar schema. The upstream VRC transition `SR-201 → SR-202` demonstrates one historically pinned source change, with `F-001` resolving and `F-002` remaining open; it is not a model of downstream controller terminal state.

Downstream owns its broader evidence-producer, specialist assessor, freshness/invalidation and terminal-reconciliation contracts. No acceptance rule, authority or algorithm is moved upstream or redefined here.

**Evidence limits:** This checks two accepted upstream example evaluators and their failure paths, not real-world target assurance, downstream adapter compatibility, independent human review or universal lifecycle interoperability. A later integration must demonstrate an actual consumer's translation need before proposing new mappings or schemas. AI-assisted implementation and analysis; independent reviewability APPLICABLE, with pins, commands, cases, expected failures and limitations recorded.
