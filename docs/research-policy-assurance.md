# Policy-as-assurance-subject research capability

> **Experimental branch capability for issue #662.** Nothing in this document changes the stable RAHP controller contract or the v2.3.0 production capability boundary.

This research path asks whether policy documents can participate in RAHP as source-pinned assurance subjects without converting legal interpretation, policy declarations, AI output or missing evidence into false assurance conclusions.

The intended user question is:

> Give RAHP this policy document and show me what could harm people, why you think so, where exactly the policy says it, what you are uncertain about, and what I should investigate next.

## Architecture boundary

```text
policy source
  -> source-pinned policy subject
  -> deterministic structure/proposition candidates
  -> explicit review / judgment boundary
  -> bounded portable RAHP risk hypotheses
  -> evidence and specialist work queue
  -> optional runtime comparison
  -> non-terminal citable research report
  -> policy-version delta and reassessment trigger
```

The capability is implemented as additive research adapters and workflow tooling. It does **not** modify `tools/assessment_controller.py`, the stable engine contract, terminal assurance semantics, or release metadata.

## What is implemented

| Workstream from #662 | Research implementation | Current boundary |
|---|---|---|
| W1 source acquisition/pinning | Local UTF-8 text/Markdown, URI/version/retrieval metadata, full-source SHA-256 | Remote retrieval and scanned/OCR inputs deliberately unsupported |
| W2 structure/segmentation | Exact source offsets/hashes; YAML metadata; heading hierarchy; list-item boundaries; definition candidates; Markdown links and textual Section references | Complete tables, resolved definitions and precedence across incorporated documents remain future work |
| W3 proposition extraction | Conservative proposition classification plus review-only actor, temporal, consequence and section-reference facets | Facets are candidates, not reviewed facts; object/trigger/affected-party extraction remains incomplete |
| W4 human review | Accept/amend/reject decisions with machine proposal preserved and rationale required for material change | Split/merge UI operations and definition/reference resolution workflow are not yet implemented |
| W5 risk/harm hypotheses | Small bounded mapping to existing portable RAHP risk patterns with explicit rationale | Mapping is intentionally incomplete and remains non-terminal |
| W6 evidence/specialist routing | Runtime, UX, privacy/DPIP, legal/domain, human-judgment and RAHP evidence queue | No external specialist is invoked automatically |
| W7 synthesis | Cold-reader Markdown/JSON report separating source, inference, evidence and uncertainty | No aggregate policy score is produced |
| W8 change path | Deterministic proposition-aware source-version delta and reassessment flag | Semantic matching is deliberately conservative and research-grade |

## Real-document pressure-test tranche

The branch includes a bounded real-policy corpus under `examples/policy-assurance/real/`, derived from the public `github/site-policy` repository pinned at commit `b9578b546d2506febda1da2cd7431644d58e512c`. The upstream corpus is CC0 1.0.

The fixtures retain separate provenance for the authoritative upstream blob and for the local research snapshot. RAHP calculates the assessment-source SHA over the actual retained bytes; it does not reuse the upstream blob SHA as if the snapshot were the complete upstream document.

The corpus now covers three structurally different policy surfaces:

- acceptable-use rules and enforcement;
- appeal/reinstatement and human-review language;
- a bounded Terms of Service structural snapshot focused on definitions, incorporated policies, precedence language, and cross-section references.

The tests pressure-test:

- YAML front matter as metadata rather than propositions;
- heading hierarchy attached to each proposition;
- list items as independent source spans;
- exact source-offset reconstruction;
- materially different policy models;
- discretionary language remaining judgment-required;
- definitions remaining review candidates rather than silently rewriting clauses;
- incorporated-document links being identified but never traversed automatically;
- Section references being retained unresolved;
- actor/temporal/consequence facets remaining deterministic review candidates;
- precedence language remaining source text rather than an automatically executed conflict rule;
- portable risk mappings remaining hypotheses rather than terminal findings.

See `examples/policy-assurance/real/`, `tests/test_policy_real_corpus.py`, and `tests/test_policy_structural_semantics.py`.

## Structural-semantic review boundary

The research path now makes several distinctions explicit:

1. **Definition detection is not definition resolution.** A quoted term followed by language such as `means`, `refers to`, `represents`, or `is where` can be recorded as a candidate definition. The candidate does not silently rewrite other propositions using that term.
2. **A link is not automatically an incorporated obligation.** Links are classified as internal anchors, ordinary external references, or incorporated-document candidates using bounded textual signals. Every candidate remains untraversed and requires review.
3. **A textual Section reference is not automatically resolved.** `Section E`, for example, remains an unresolved structural reference until an explicit resolver/reviewer confirms the target.
4. **Facet extraction is not proposition acceptance.** Candidate actors, temporal phrases and consequences are emitted as `deterministic-facet-candidate` records with `requires_review: true`.
5. **Precedence language is not an executable precedence engine.** Statements such as “the more specific terms apply” remain source propositions. Resolving conflicts across multiple incorporated documents remains a separate research problem.

These boundaries are deliberate. The experiment should make hidden interpretation harder, not easier.

## Run the experiment

Generate a source-pinned subject:

```bash
python3 tools/policy_subject.py ingest \
  examples/policy-assurance/platform-terms-v1.md \
  --uri fixture://platform-terms-v1.md \
  --version v1 > /tmp/policy-subject.json
```

For structure-preserving Markdown ingestion:

```bash
python3 tools/policy_structure.py \
  examples/policy-assurance/real/github-terms-structural-snapshot.md \
  --uri github-site-policy://terms-structural-snapshot \
  --version b9578b546d2506febda1da2cd7431644d58e512c
```

Generate bounded RAHP hypotheses:

```bash
python3 tools/policy_subject.py map /tmp/policy-subject.json
```

Run the end-to-end research assessment and render a human-readable report:

```bash
python3 tools/policy_assessment.py \
  examples/policy-assurance/platform-terms-v1.md \
  --uri fixture://platform-terms-v1.md \
  --version v1 \
  --format markdown
```

The default review path deliberately leaves ambiguous propositions at `JUDGMENT_REQUIRED`. This is expected behaviour, not an error.

## Optional reviewed proposition decisions

A review file is a JSON array. Supported research actions are `accept`, `amend` and `reject`. `amend` and `reject` require rationale. The immutable machine proposal and exact source span remain present in the review lineage.

## Runtime comparison

Runtime evidence is supplied separately and MUST declare `evidence_class: runtime-observation`. The comparison result is `CONSISTENT`, `MISMATCH` or `INDETERMINATE`. None of these records is itself a terminal RAHP assurance result. Policy text cannot be passed as runtime evidence.

## Policy-version change

Create two source-pinned subject JSON files and compare them:

```bash
python3 tools/policy_subject.py diff old-subject.json new-subject.json
```

The delta reports added, removed and likely changed propositions and whether reassessment is required. Prior assessments remain independent records; a revised policy does not overwrite historical lineage.

## Evidence discipline

The research workflow visibly separates four statements:

1. **Policy text establishes** — exact source spans and direct-source proposition records.
2. **RAHP infers** — bounded, explainable risk hypotheses mapped to portable patterns.
3. **Evidence shows** — separate runtime observations when supplied.
4. **Cannot yet determine** — judgment-required clauses and evidence/specialist work items.

Missing remedy text is treated as an evidence gap, not proof that no remedy exists. Jurisdiction-dependent language creates specialist work rather than a legal conclusion. AI confidence, if AI extraction is explored later, must not become assurance evidence.

## Tests and falsification evidence

The research tests exercise source reconstruction and hashing, materially different policy fixtures, ambiguity preservation, non-terminal risk hypotheses, missing-redress `INDETERMINATE`, policy-change reassessment, evidence-class separation, tamper detection, explicit human-review lineage, rationale requirements, specialist routing, cold-reader synthesis, real-policy Markdown structure, definition/reference/incorporation boundaries, review-only proposition facets, and judgment-state transitions.

The repository's standard `python3 -m unittest discover -s tests -p 'test_*.py'` CI command discovers the research test files automatically.

## What this branch deliberately does not claim

This branch does not claim that RAHP can provide legal advice, determine enforceability, certify regulatory compliance, infer actual consent/fairness from policy language, prove that declared safeguards operate, automatically resolve ambiguous clauses, resolve legal precedence between documents, or infer that a referenced policy is binding merely because it is linked. It does not add policy-specific semantics to the stable assessment controller.

## Graduation criteria before any main-branch merge

A future merge to stable `main` should require explicit evidence that:

- clause/source traceability remains lossless across representative real documents;
- proposition classification is useful enough after human review to justify maintenance cost;
- policy inference does not weaken RAHP evidence or authority boundaries;
- privacy/legal/domain specialist routing has a durable contract where needed;
- richer document structure, definitions and incorporated-document handling have defensible review semantics;
- proposition facets improve review usefulness without becoming unreviewed assurance facts;
- cross-document conflict/precedence handling has an explicit, falsifiable boundary;
- policy delta behaviour is reliable enough for continuous assurance;
- the end-user output is understandable without requiring knowledge of internal RAHP record types;
- the full RAHP validation suite remains green;
- a human explicitly decides that the research capability should graduate.

Until those gates are met, the branch and its PR should remain experimental and unmerged.
