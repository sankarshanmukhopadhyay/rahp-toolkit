---
layout: default
title: "Assurance graph and impact analysis"
nav_order: 9
has_toc: true
parent: Operate assurance
---
# Assurance graph and impact analysis

RAHP v1.5 development introduces a portable assurance graph for connecting targets, requirements, evidence, risks, harms, controls, guardrails, tests, assessments, findings, remediations and authorities without coupling the method to any particular repository, standards community or deployment.

The graph is not a universal ontology and does not make an assurance conclusion by itself. It records enough machine-readable dependency structure to answer a narrower operational question:

> If this governed target or assurance object changes, which assurance records may need to be reconsidered?

## Portable graph contract

`method/schema/assurance-graph.schema.json` defines nodes and typed edges. Each edge carries an explicit `impact_propagation` value:

- `source-to-target`
- `target-to-source`
- `both`
- `none`

Impact direction is therefore evidence carried by the graph, not an assumption hard-coded into the engine. Two deployments may use the same relationship type with different propagation semantics when their governance or dependency structure genuinely differs.

This is important for portability: RAHP does not assume that a repository, specification, implementation, dataset or operational service has the dependency layout of DTG, OpenVTC, ARPA, CAWG/C2PA or any other maintained example.

## Impact analysis

`tools/impact.py` performs deterministic reachability from one or more changed node identifiers.

```bash
python3 tools/impact.py \
  --graph examples/assurance-lineage/generic-assurance-graph.yaml \
  --changed-node target:payments-api \
  --json
```

The result records:

- changed nodes;
- every affected node and its shortest graph distance;
- the edge path (`via`) that explains why it was selected;
- affected stable assessment identities;
- assessments selected as `retest_required`; and
- changed node identifiers that could not be resolved.

`method/schema/impact-analysis.schema.json` defines the portable result contract.

## Reconstruct one reassessment-selection decision (#1189)

The public JSON already contains the evidence needed to reconstruct the
selection of `example:specification:payments-api` without another renderer:

```bash
python3 tools/impact.py \
  --graph examples/assurance-lineage/generic-assurance-graph.yaml \
  --changed-node target:payments-api --json
python3 -m unittest tests.test_assurance_graph_impact -v
```

Use the **same checked-out graph** as the input to the impact command.
The resulting `assessment:payments-auth` node has
`distance: 2` and `via: [e1, e5]`. Inspect the existing
`edges` in `examples/assurance-lineage/generic-assurance-graph.yaml`:

1. `e1` is declared `req:authorization → target:payments-api`, type
   `depends-on`, propagation `target-to-source`. Impact therefore
   travels **from** the changed `target:payments-api` **to**
   `req:authorization`, not along the displayed arrow.
2. `e5` is declared `assessment:payments-auth → req:authorization`,
   type `depends-on`, propagation `target-to-source`. Impact travels
   from the requirement to `assessment:payments-auth`.
3. That node declares `assessment_id:
   example:specification:payments-api`, which appears in both
   `affected_assessments` and `retest_required`.

The two edge IDs explain the distance of two traversals; the direction
comes from **each edge's `impact_propagation`**, not from the label
`depends-on`. The `via` array is a **selected shortest path**, not
necessarily a complete listing of every possible dependency route.
The committed `generic-impact-result.json` is the deterministic baseline
for this example; it is not another source of graph authority.

### Falsification and incomplete-graph cases

```bash
python3 tools/impact.py \
  --graph examples/assurance-lineage/generic-assurance-graph.yaml \
  --changed-node unknown:external-policy --json
```

The unchanged JSON output has `unresolved_changed_nodes:
["unknown:external-policy"]`, no selected assessment and a nonzero
CLI status (2). **No assessment selected is not a finding of no impact**.
If a real dependency edge is omitted from an otherwise structurally
valid graph, the algorithm cannot infer that omission: it may return a
longer alternative path or an empty candidate list. The focused
`test_unrepresented_dependency_is_not_inferred_as_no_effect` retains
this adverse observation as a limitation, rather than inventing a graph
completeness detector. Contradictory dependency claims or unverified
graph coverage must be investigated by the responsible graph/evidence
owner before declaring a reassessment set complete.

### Evidence and challenge boundary

A reviewer can challenge selection by pointing to the changed node,
declared edge IDs, propagation directions, typed assessment node and
source graph revision. This is **graph reachability**, not causal proof,
a source-change materiality decision, evidence freshness, an observed
failed control or an authorized risk disposition. The graph fixture is
fictional; no live payment deployment was tested.

**Feasibility disposition:** the maintained JSON already carries a
reconstructable path and unresolved changed-node identities. No
additional explanation API, schema, dashboard or alternate status
vocabulary is justified by this bounded test. Independent cold-reader
adoption has not been observed; these are executable reviewer
instructions, not attributed human study results.

## Governance boundary

Impact is **selection evidence**, not a finding and not a closure decision.

```text
material change
  → graph impact selection
  → affected assessment candidates
  → evidence review / reassessment
  → governed residual conclusion
```

A selected assessment is a candidate for retest. RAHP must not infer from graph reachability alone that a target is unsafe, that a finding exists, that a remediation failed, or that an upstream issue must be opened.

Likewise, absence from an incomplete graph is not evidence of non-impact. Deployments are responsible for the scope and quality of their graph data and should preserve uncertainty when relevant dependencies are not represented.

## Deployment-neutral conformance fixture

The canonical fixture uses the fictional Example Payments API Specification. A change to the target propagates through an authorization requirement, implementation control, assurance test and evidence into the stable assessment identity. The graph also retains downstream finding and remediation dependencies.

This demonstrates the portable contract without making any real project vocabulary part of core conformance.

Project-specific graph profiles MAY then map DTG, OpenVTC, ARPA, CAWG/C2PA or other projects into these node and edge contracts as real-world demonstrations.

## Validation

```bash
python3 tools/validate_assurance_graph.py
python3 -m unittest tests.test_assurance_graph_impact
```

The validator checks graph schema conformance, node uniqueness, edge reference integrity, impact-result conformance, deterministic target-change propagation and explicit treatment of unresolved changed nodes.
