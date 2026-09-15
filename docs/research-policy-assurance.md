# Policy-as-assurance-subject research capability

> **Experimental branch capability for issue #662.** Nothing in this document changes the stable RAHP controller contract or the v2.3.0 production capability boundary.

This research path asks whether policy documents can participate in RAHP as source-pinned assurance subjects without converting legal interpretation, policy declarations, AI output or missing evidence into false assurance conclusions.

The intended user question is:

> Give RAHP this policy document and show me what could harm people, why you think so, where exactly the policy says it, what you are uncertain about, and what I should investigate next.

## Architecture boundary

```text
policy source
  -> source-pinned policy subject
  -> deterministic clause/proposition extraction
  -> explicit review / judgment boundary
  -> bounded portable RAHP risk hypotheses
  -> evidence and specialist work queue
  -> optional runtime comparison
  -> non-terminal citable research report
  -> policy-version delta and reassessment trigger
```

The capability is implemented as an additive adapter in `tools/policy_subject.py` plus the research workflow in `tools/policy_assessment.py`. It does **not** modify `tools/assessment_controller.py`, the stable engine contract, terminal assurance semantics, or release metadata.

## What is implemented

| Workstream from #662 | Research implementation | Current boundary |
|---|---|---|
| W1 source acquisition/pinning | Local UTF-8 text/Markdown, URI/version/retrieval metadata, full-source SHA-256 | Remote retrieval and scanned/OCR inputs deliberately unsupported |
| W2 structure/segmentation | Lossless paragraph-like spans with exact offsets, text and span hashes | Rich table/list/definition hierarchy is not yet reconstructed |
| W3 proposition extraction | Conservative deterministic classification into the experimental proposition vocabulary | Actor/object/trigger field extraction remains future research |
| W4 human review | Accept/amend/reject decisions with machine proposal preserved and rationale required for material change | Split/merge UI operations are not implemented in this branch |
| W5 risk/harm hypotheses | Small bounded mapping to existing portable RAHP risk patterns with explicit rationale | Mapping is intentionally incomplete and remains non-terminal |
| W6 evidence/specialist routing | Runtime, UX, privacy/DPIP, legal/domain, human-judgment and RAHP evidence queue | No external specialist is invoked automatically |
| W7 synthesis | Cold-reader Markdown/JSON report separating source, inference, evidence and uncertainty | No aggregate policy score is produced |
| W8 change path | Deterministic proposition-aware source-version delta and reassessment flag | Semantic matching is deliberately conservative and research-grade |

## Run the experiment

Generate a source-pinned subject:

```bash
python3 tools/policy_subject.py ingest \
  examples/policy-assurance/platform-terms-v1.md \
  --uri fixture://platform-terms-v1.md \
  --version v1 > /tmp/policy-subject.json
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

A review file is a JSON array. For example:

```json
[
  {
    "proposition_id": "pol-example",
    "action": "amend",
    "text": "Reviewed proposition text",
    "reviewer": "human-reviewer",
    "rationale": "Clarify the actor while preserving the source clause as immutable lineage."
  }
]
```

Supported research actions are `accept`, `amend` and `reject`. `amend` and `reject` require rationale. The immutable machine proposal and exact source span remain present in the review lineage.

## Runtime comparison

Runtime evidence is supplied separately and MUST declare `evidence_class: runtime-observation`:

```json
[
  {
    "proposition_id": "pol-example",
    "evidence_class": "runtime-observation",
    "observed": false,
    "evidence_ref": "run://example-001"
  }
]
```

The comparison result is `CONSISTENT`, `MISMATCH` or `INDETERMINATE`. None of these records is itself a terminal RAHP assurance result. Policy text cannot be passed as runtime evidence.

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

`tests/test_policy_subject.py` exercises:

- exact source-span reconstruction and hashing;
- two materially different policy fixtures;
- ambiguity preservation;
- portable risk hypotheses remaining hypotheses;
- missing-redress text remaining `INDETERMINATE`;
- deterministic policy-change reassessment;
- governance-source versus runtime-observation separation;
- rejection of tampered source spans.

`tests/test_policy_assessment.py` exercises:

- explicit human-review boundaries;
- preservation of machine proposals after amendments;
- rationale requirements for material review changes;
- runtime/privacy/UX/judgment/RAHP evidence routing;
- non-terminal synthesis and cold-reader report content;
- transition from `JUDGMENT_REQUIRED` to `EVIDENCE_REQUIRED` only after explicit review.

The repository's standard `python3 -m unittest discover -s tests -p 'test_*.py'` CI command discovers both research test files automatically.

## What this branch deliberately does not claim

This branch does not claim that RAHP can provide legal advice, determine enforceability, certify regulatory compliance, infer actual consent/fairness from policy language, prove that declared safeguards operate, or automatically resolve ambiguous clauses. It does not add policy-specific semantics to the stable assessment controller.

## Graduation criteria before any main-branch merge

A future merge to stable `main` should require explicit evidence that:

- clause/source traceability remains lossless across representative real documents;
- proposition classification is useful enough after human review to justify maintenance cost;
- policy inference does not weaken RAHP evidence or authority boundaries;
- privacy/legal/domain specialist routing has a durable contract where needed;
- richer document structure and incorporated-document handling have defensible semantics;
- policy delta behaviour is reliable enough for continuous assurance;
- the end-user output is understandable without requiring knowledge of internal RAHP record types;
- the full RAHP validation suite remains green;
- a human explicitly decides that the research capability should graduate.

Until those gates are met, the branch and its PR should remain experimental and unmerged.
