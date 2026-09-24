# Policy-as-assurance-subject research capability

> **Experimental branch capability for issue #662.** Nothing in this document changes the stable RAHP controller contract or the v2.4.0 stable production capability boundary.

This research path asks whether policy documents can participate in RAHP as source-pinned assurance subjects without converting legal interpretation, policy declarations, AI output or missing evidence into false assurance conclusions.

The intended user question is:

> Give RAHP this policy document and show me what could harm people, why you think so, where exactly the policy says it, what you are uncertain about, and what I should investigate next.

## Architecture boundary

```text
policy source
  -> source-pinned structured policy subject
  -> deterministic structure/proposition candidates
  -> explicit human review: accept/amend/reject/split/merge
  -> reviewed proposition set
  -> definition/reference/precedence relationship review
  -> bounded portable RAHP risk hypotheses from reviewed propositions only
  -> evidence and specialist work queue
  -> optional runtime comparison
  -> non-terminal citable research report
  -> policy-version delta and reassessment trigger
```

The capability is implemented as additive research adapters and workflow tooling. It does **not** modify `tools/assessment_controller.py`, the stable engine contract, terminal assurance semantics, or release metadata.


## ODRL 2.2 semantic alignment

Issue #662 now requires the experimental proposition vocabulary to be pressure-tested against the W3C ODRL 2.2 Information Model and Vocabulary before the local vocabulary is treated as durable.

ODRL is used here as a **policy-expression interoperability reference**, not as the RAHP assurance model:

```text
policy source
  -> reviewed policy proposition
      -> ODRL-aligned semantic projection where genuinely equivalent
      -> explicit partial/profile-candidate/outside-ODRL state otherwise
  -> RAHP risk / harm / control hypotheses
  -> evidence obligations / specialist routing
  -> non-terminal research assessment
```

The alignment contract is `method/experimental/policy-odrl-alignment-v1.yaml`. It distinguishes `direct`, `profile-candidate`, `partial`, and `outside-odrl` mappings. A coarse local proposition type is **not** sufficient to emit a usable ODRL rule: permissions, prohibitions and duties still need explicit action and target semantics, and applicable party/constraint semantics must be established rather than inferred.

The research branch therefore follows two complementary paths:

1. **Natural-language policy path.** Reviewed propositions receive loss-aware ODRL projection-readiness metadata. If required structure is missing, the result is `insufficient-structure` or `semantic-review-required`; the adapter does not fabricate an ODRL policy.
2. **ODRL-native control path.** A bounded ODRL 2.2 JSON-LD fixture is ingested deterministically so that already-machine-readable policy semantics can be compared with the natural-language extraction/review path.

Generated ODRL alignment/projection artifacts are derived semantics, not replacement source evidence. A supplied ODRL policy may itself be the pinned governance source being assessed. ODRL conformance or evaluation does not imply legal validity, fairness, runtime conformance, or terminal RAHP assurance.

No RAHP ODRL Profile is defined or authorized by this research. Concepts such as discretion, generic representation, risk/harm hypotheses, evidence obligations, assurance state, specialist routing, residuals and reassessment triggers remain outside ODRL unless future evidence supports a separate profile/design decision.


## What is implemented

| Workstream from #662 | Research implementation | Current boundary |
|---|---|---|
| W1 source acquisition/pinning | Local UTF-8 text/Markdown, URI/version/retrieval metadata, full-source SHA-256 | Remote retrieval and scanned/OCR inputs deliberately unsupported |
| W2 structure/segmentation | Exact offsets/hashes; YAML metadata; heading hierarchy; list items; definitions; links; textual Section references | Complete table semantics and remote document resolution remain future work |
| W3 proposition extraction | Conservative proposition classification plus review-only actor, temporal, consequence and section-reference facets | Object/trigger/affected-party extraction remains incomplete |
| W4 human review | Accept/amend/reject/split/merge with immutable machine/source lineage; rationale required for material changes | No graphical review UI; workflow is JSON/CLI research tooling |
| W5 risk/harm hypotheses | Portable RAHP risk mapping consumes the reviewed proposition set only | Mapping remains deliberately bounded and non-terminal |
| W6 evidence/specialist routing | Runtime, UX, privacy/DPIP, legal/domain, human-judgment and RAHP evidence queue | No external specialist is invoked automatically |
| W7 synthesis | Cold-reader Markdown/JSON separating source, reviewed interpretation, relationships, inference, evidence and uncertainty | No aggregate policy score is produced |
| W8 change path | Deterministic proposition-aware source-version delta and reassessment flag | Semantic matching remains conservative and research-grade |

## Review boundary is now executable

`rahp-policy-review/v2` makes the W4 boundary operational rather than documentary.

Supported actions are:

- `accept` — retain the machine proposition as the reviewed proposition;
- `amend` — create reviewed text while preserving the machine proposal and source span;
- `reject` — exclude the proposition from downstream RAHP analysis;
- `split` — create two or more reviewed child propositions linked to one immutable source proposition;
- `merge` — create one reviewed proposition linked to multiple immutable source propositions.

`amend`, `reject`, `split`, and `merge` require rationale. Rejected propositions and unresolved ambiguous propositions do **not** enter reviewed RAHP analysis. Risk/harm hypotheses are generated from the reviewed proposition set rather than from opaque machine extraction.

Example split decision:

```json
[
  {
    "proposition_id": "pol-example",
    "action": "split",
    "parts": [
      "We may suspend your account.",
      "We may share account information with service providers."
    ],
    "reviewer": "human-reviewer",
    "rationale": "The source contains two independently reviewable propositions."
  }
]
```

Example merge decision:

```json
[
  {
    "action": "merge",
    "proposition_ids": ["pol-a", "pol-b"],
    "text": "The operator may delegate activity to service providers acting on its behalf.",
    "reviewer": "human-reviewer",
    "rationale": "The two source clauses form one delegation proposition when read together."
  }
]
```

## Definitions, references and precedence

`rahp-policy-relationships/v1` models structural relationships without turning them into legal conclusions.

The model provides:

1. **Definition-use candidates.** Definitions are indexed and lexical uses can be surfaced for review. Detection is not semantic substitution.
2. **Referenced-document relationships.** Internal anchors, ordinary external references and incorporated-document candidates remain untraversed. A reviewer may accept, reject or reclassify the relationship; acceptance still does not fetch the target.
3. **Cross-document definition conflicts.** If related structured subjects define the same term differently, the conflict becomes `judgment-required` rather than being resolved by ordering or parser heuristics.
4. **Precedence-language candidates.** Language such as “the more specific terms apply” is surfaced as a candidate. It does not automatically decide which document governs.
5. **Explicit precedence decisions.** A reviewer may select a subject digest and record rationale for the research interpretation. The resulting record explicitly says `legal_conclusion: false` and `terminal_assurance: false`.

This lets RAHP represent “these documents may conflict and a reviewer chose this research interpretation” without pretending to determine enforceability or legal hierarchy.

## Real-document pressure tests

The branch includes a bounded corpus under `examples/policy-assurance/real/`, derived from the public `github/site-policy` repository pinned at commit `b9578b546d2506febda1da2cd7431644d58e512c`. The upstream corpus is CC0 1.0.

The corpus covers acceptable-use/enforcement, appeal/reinstatement, and a Terms of Service structural snapshot containing definitions, incorporated policies, precedence language and cross-section references. Upstream blob identity and the SHA-256 of the retained RAHP research snapshot remain separate provenance fields.

The pressure tests have already falsified several naive assumptions: plural provider language, `in its discretion`, `refers, collectively, to`, and contractual incorporation expressed through `agree ... not ... violate [policy]` all required refinement. Those failures were fixed in the implementation rather than weakened out of the tests.

## Run the end-to-end experiment

```bash
python3 tools/policy_assessment.py \
  examples/policy-assurance/real/github-terms-structural-snapshot.md \
  --uri github-site-policy://terms-structural-snapshot \
  --version b9578b546d2506febda1da2cd7431644d58e512c \
  --format markdown
```

Optional inputs now include:

- `--review review.json`
- `--runtime runtime.json`
- `--previous-subject previous.json`
- `--related-subject related.json` (repeatable)
- `--reference-decisions reference-decisions.json`
- `--precedence-decisions precedence-decisions.json`

The CLI uses structure-preserving ingestion. A default run intentionally leaves ambiguous propositions, incorporated-document relationships and precedence candidates at explicit judgment boundaries.

## Citable evidence obligations

The evidence work queue now emits explicit `rahp-policy-evidence-obligation/v1` records rather than bare questions. Each obligation has a deterministic identifier, preserved source-proposition lineage, evidence class, route, materiality, and a human-readable `why_required` justification. This makes downstream evidence requests citable and reviewable without implying that the requested evidence already exists.

An unevaluated obligation has `terminal_effect: none-until-evidence-evaluated`; unresolved human judgment similarly has no terminal effect until the judgment boundary is crossed. This keeps work-queue generation separate from assurance disposition and provides a cleaner hand-off surface for runtime tests, UX evidence, DPIP/privacy specialists, legal/domain specialists, and ordinary RAHP assessment.

## Evidence-obligation lifecycle and reassessment

Citable obligations now have an explicit research lifecycle: `OPEN`, `EVIDENCE_SUPPLIED`, `SATISFIED`, `CONTRADICTED`, `INDETERMINATE`, or `SUPERSEDED`. Evidence is linked by reference and evaluated with an explicit rationale; even a satisfied or contradicted obligation remains non-terminal in this adapter.

When a supplied previous policy version produces a delta, obligations whose immutable source lineage points to a changed or removed proposition become `SUPERSEDED`. Their prior evidence is not silently inherited by the new policy version. The output records that reassessment is required, preserving the distinction between historical evidence and evidence applicable to the current policy source.

This lifecycle is deliberately local to the experimental policy adapter. It does not modify the stable RAHP controller state machine.

## Evidence discipline

The research artifact separates five layers:

1. **Policy text establishes** — immutable source spans and source propositions.
2. **Reviewer interprets** — accepted/amended/split/merged proposition lineage.
3. **Policy relationships require judgment** — definitions, incorporation, precedence and conflicts.
4. **RAHP infers** — bounded risk/harm hypotheses generated only from the reviewed analytical set.
5. **Evidence shows / cannot yet determine** — runtime evidence, specialist requirements, unresolved judgment and evidence gaps.

Missing remedy text remains an evidence gap, not proof that no remedy exists. A declared safeguard remains governance-source evidence, not proof that it operates. AI confidence, if introduced later, must not substitute for evidence confidence.

## Tests and falsification evidence

The repository-wide unittest suite now covers:

- exact source reconstruction and hashing;
- real-policy structure and hierarchy;
- ambiguity preservation;
- definition/reference/incorporation candidates;
- cross-document definition conflicts;
- non-automatic precedence handling;
- explicit non-legal precedence resolution;
- accept/amend/reject/split/merge lineage;
- rejected propositions being excluded from RAHP inference;
- amended/split/merged reviewed text being the actual analytical input;
- evidence-class separation and runtime comparison;
- deterministic, citable evidence-obligation identifiers and explicit justification;
- policy-change reassessment and evidence-obligation invalidation;
- cold-reader synthesis;
- stable-controller non-regression;
- ODRL alignment-state boundaries and refusal to invent missing action/target semantics;
- deterministic ODRL-native control-fixture ingestion and non-terminal authority boundaries.

The standard command remains:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## What this branch deliberately does not claim

This branch does not claim legal advice, enforceability analysis, regulatory certification, proof of consent/fairness, proof that declared safeguards operate, automatic resolution of ambiguous clauses, automatic legal precedence, or that a referenced policy is binding merely because it is linked. It does not add policy-specific semantics to the stable assessment controller.

## Graduation criteria before any main-branch merge

A future merge to stable `main` should require explicit evidence that:

- clause/source traceability remains lossless across representative documents;
- reviewed proposition operations are useful and maintainable;
- rejected and unresolved propositions cannot contaminate assurance inference;
- definition/reference/precedence handling preserves explicit judgment boundaries;
- privacy/legal/domain specialist routing has a durable contract where needed;
- policy delta behaviour is reliable enough for continuous assurance;
- the end-user artifact is understandable without internal RAHP knowledge;
- the complete RAHP validation suite remains green;
- an explicit RAHP-to-ODRL alignment matrix and ODRL-native control case have been independently reviewed;
- a human explicitly decides the capability should graduate.

Until those gates are met, the branch and PR #667 remain experimental and unmerged.
