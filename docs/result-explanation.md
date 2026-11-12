---
layout: default
title: "Explain a retained result"
nav_order: 9
parent: Run assessments
has_toc: true
---
# Explain a retained RAHP result

The **assurance explanation interface** is a local, read-only consumer projection of one already-retained **normalized result schema v1** document. It does not run an assessment, infer a controller terminal PASS, authenticate evidence or authorize a governed action. It supplies an independently inspectable answer to **what was assessed, what was recorded, what remains unresolved, and what cannot be established from this input**.

This interface complements, rather than replaces, [Interpreting results](interpreting-results.md). The existing `tools/assurance_record.py` renders a **different terminal-run-state record**; do not pass that record type to this normalized-result command.

## Reproduce from a clean checkout

Install the existing Python dependencies using `pip install -r requirements.txt`, then run from the repository root:

~~~bash
python3 tools/engine_contract.py explain \
  tests/conformance/engine/valid-v12-assurance/result.json \
  --format json

python3 tools/engine_contract.py explain \
  tests/conformance/engine/valid-v12-assurance/result.json \
  --format markdown
~~~

The maintained fixture has **zero findings** but contains an `assurance-gap` residual for proposition `ATP-OPS-02` and a declared missing test (`lost-response-test`). The projection therefore records one unresolved residual, `overall_assurance: not-derived`, and `controller_terminal_outcome: not-established-by-normalized-result`. Freshness is `not-established` unless a separate, correctly bound freshness record is supplied. Neither successful command nor schema validation makes the finding count an assurance PASS.

A separate minimal fixture demonstrates a different boundary:

~~~bash
python3 tools/engine_contract.py explain \
  tests/conformance/engine/valid-minimal/result.json \
  --format json
~~~

Even though that fixture's normalized record is dispositioned and has zero findings, no per-proposition evaluation is recorded. The projection reports `evaluation.state: not-recorded` and does not synthesize `assured`.

## Add a separately declared freshness record

Freshness is **not embedded or authenticated by normalized result schema v1**. To avoid silently selecting another run's freshness, the optional file requires an explicit caller-supplied run identity and a matching assessment ID:

~~~bash
python3 tools/engine_contract.py explain \
  tests/conformance/engine/valid-v12-assurance/result.json \
  --freshness examples/assurance-lineage/explanation-freshness-example.yaml \
  --run-id RUN-EXPLAIN-001 \
  --format json
~~~

This fixture is **synthetic instructional data**, not evidence of the operational freshness of any real system. The example deliberately declares `requires-retest`; the output remains `retest-required`. The CLI validates the freshness schema, subject/run binding and basis-derived state. It does **not** independently prove that the declared run identity belongs to the normalized result, fetch evidence, or authenticate the observed change. The output labels this limitation.

An omitted `--run-id`, mismatched identity, malformed freshness document or contradiction between its declared basis and status is rejected with a nonzero exit and no explanation on standard output. Omitting freshness entirely is permitted, but produces `not-established`, never `current`.

## Output and interpretation

`--format json` (default) emits a deterministic `rahp-result-explanation/v1` **derived projection**, not a new normative method or engine contract. `--format markdown` renders the same supported facts with untrusted source text escaped.

| Section | What it exposes | What it does not establish |
|---|---|---|
| `assessment` | Stable assessment ID/key, mode, reviewed repository and revision | Authenticated source content or assessment scope beyond the recorded fields |
| `decision` | Normalized record status and declared disposition | Controller terminal result, risk acceptance, publication or closure authority |
| `findings` / `evaluation` | Recorded findings, residual reasoning and missing obligations | That zero findings means assured; the validity of substantive reasoning |
| `evidence` | Declared IDs, classes and reference metadata | Evidence authenticity, integrity verification, retrieval or inferred proposition linkage |
| `freshness` | Not-established or separately bound declared freshness | Independent run/evidence authentication |
| `retest_triggers` | Recorded triggers, if present | Completeness of all possible invalidation/retest conditions |

Absent `evaluations`, `freshness` and `retest_triggers` are displayed as missing/not-established rather than interpreted as verified absence of risk.

## Failure and negative paths

~~~bash
# This fixture violates the existing reviewed-revision closure invariant.
# The command rejects it and exits nonzero; it does not emit an explanation.
python3 tools/engine_contract.py explain \
  tests/conformance/engine/invalid-closure-revision/result.json

# Reproducible CLI/consumer tests, including invalid input and injection.
python3 -m unittest tests.test_result_explanation -v
~~~

The interface reads local files only. It does not traverse remote evidence URLs, publish issue updates, mutate the assessment, execute an evidence producer, or reconcile a new terminal determination. Evidence references may require separate access governance, retention and privacy controls.

## Compatibility, authority and maintenance

The authoritative inputs remain `method/schema/rahp-result.schema.json`, `method/schema/assurance-freshness.schema.json`, and the existing `tools/engine_contract.py` and `tools/assurance_state.py` validation semantics. The derived explanation is **not** a revision to `rahp-engine-contract-v1` (revision 1.3), normalized result schema 1, or `rahp-evidence-retention-v1`.

Consumer tests run in the required repository validation workflow. A passing test establishes the local projection behavior only; independent methodological acceptance and deployment conformance are not established. Further qualification belongs to the applicable upstream, deployment, or reviewer authority.
