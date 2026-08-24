---
layout: default
title: "AI-assisted process"
nav_order: 7
has_toc: true
parent: Run assessments
---
# AI-assisted RAHP workflows

RAHP can be operated with an AI assistant such as ChatGPT, Claude, Codex, or another repository-capable language model. The assistant can accelerate source inspection, scenario construction, evidence mapping, tooling execution, finding drafts, reassessment and remediation planning.

The assistant is **not** an evidence source and is **not** the final authority for a RAHP finding.

The governing rule is:

> Use the AI assistant to operate and interrogate the RAHP method. Use source-pinned evidence, RAHP contracts, validators and explicit human disposition to determine what the assessment establishes.

This guide is vendor-neutral. Product-specific capabilities differ, but the evidence and assurance boundaries below do not.

## When AI assistance is useful

An AI assistant can help an implementor or reviewer:

- inspect a specification, repository or implementation and identify candidate assessment surfaces;
- locate and pin authoritative source revisions;
- select or construct personas and scenarios;
- map source-specific scenarios to portable RAHP patterns;
- identify positive, negative and adversarial cases;
- construct cross-specification evidence closures;
- run RAHP validators and review generated artifacts;
- distinguish hypotheses from evidence-backed residuals;
- draft findings, recommendations and retest conditions;
- compare pre-remediation and post-remediation evidence;
- prepare issues or pull requests after a finding has been dispositioned; and
- explain RAHP outputs to maintainers, implementors and governance participants.

AI assistance is especially useful when the target spans several repositories or specifications, because the assistant can maintain the evidence chain while RAHP provides the machine-readable contracts and validation gates.

## What the assistant must not do

An AI-assisted RAHP run should not permit the model to:

- invent or paraphrase evidence that is not supported by the cited source;
- silently substitute model knowledge for an authoritative source;
- treat an unpinned web page or moving branch head as equivalent to source-pinned evidence;
- promote a hypothesis into a formal finding merely because it sounds plausible;
- infer authorization, governance legitimacy or substantive propriety from cryptographic validity alone;
- treat a component-level pass as proof that a composition passes;
- suppress negative cases because a preferred construction appears to work;
- bypass RAHP validators or modify generated evidence by hand to make validation pass;
- automatically create upstream work items before ownership and disposition are established; or
- claim legal, regulatory, policy or governance meaning that the reviewed sources do not establish.

When source evidence is incomplete, the correct RAHP result can be **insufficient evidence**, **governance-only**, **profile clarification required**, or another bounded disposition. The assistant should not fill the gap from general knowledge merely to produce a stronger-looking finding.

## Canonical AI-assisted workflow

A full source-pinned run should follow the same lifecycle as a human-operated RAHP review:

```text
Target and review question
        ↓
Authoritative source discovery
        ↓
Immutable source pins
        ↓
Personas + scenarios + pressure patterns
        ↓
Positive / negative / adversarial cases
        ↓
Evidence closure
        ↓
RAHP assessment and residual classification
        ↓
Machine-readable record
        ↓
Repository validators + generated-view checks
        ↓
Human interpretation / ownership / disposition
        ↓
Remediation or upstream work item when warranted
        ↓
RAHP retest
```

The AI assistant may perform many of these operations, but it should preserve the boundaries between them.

## Step 1 — define the target and question

Give the assistant a bounded assessment target. Prefer a repository, specification, implementation, profile or explicit composition rather than a broad topic.

Useful inputs include:

- repository URL;
- specification or document path;
- relevant branch/tag/version;
- the concrete review question;
- known adjacent specifications or dependencies; and
- whether the assessment is single-specification or cross-specification.

If the target is changing, ask the assistant to resolve and record the immutable source revision used for the review.

## Step 2 — require source-pinned evidence

For evidence-backed findings, instruct the assistant to cite the exact source and reviewed revision. A strong evidence record should make it possible for another reviewer to answer:

- Which repository or authoritative source was reviewed?
- Which immutable revision was used?
- Which source path or section supports the observation?
- Is the observation a quotation, paraphrase, test result or inference?
- Can the evidence be reproduced independently?

The assistant's own explanation is not evidence. The underlying specification text, implementation behavior, test output, registry state or other declared authoritative artifact is the evidence.

## Step 3 — build pressure coverage before conclusions

Ask the assistant to inspect existing RAHP corpora and scenario patterns before inventing new scenarios.

A good run should deliberately cover:

- expected/positive behavior;
- misuse and adversarial behavior;
- stale or conflicting state;
- composition failures;
- privacy and correlation surfaces;
- lifecycle transitions;
- authorization and authority boundaries;
- redress or recovery; and
- accessibility or exclusion where relevant.

New scenarios should be added because a pressure dimension is missing, not to increase a scenario count.

## Step 4 — construct evidence closure

For cross-specification work, do not assess each artifact in isolation if the claim depends on their composition.

Ask the assistant to construct the minimum complete evidence set needed for the proposition under review. Depending on the case, that may include:

- credentials;
- Trust Tasks or transaction evidence;
- delegation/authority evidence;
- status or lifecycle state;
- registry or policy evidence;
- approvals or supervision;
- external resolution;
- transaction context; and
- privacy/non-correlation constraints.

Evidence closure does not mean disclose everything. It means identify everything the verifier needs to establish the proposition, including the relationships among the evidence items.

## Step 5 — separate hypotheses from findings

An AI assistant is very good at generating plausible failure modes. RAHP should preserve those as hypotheses until evidence closes them.

Useful classifications during investigation include:

- confirmed;
- refined;
- weakened;
- contradicted;
- new finding;
- governance-only;
- profile clarification required; and
- insufficient evidence.

Only residuals that survive evidence review, construction and retest should normally become formal findings or candidate work items.

## Step 6 — use the repository tooling

The assistant should run the toolkit rather than merely describe RAHP conceptually.

Typical validation commands include:

```bash
python3 tools/validate.py
python3 tools/validate_scenario_corpora.py
python3 tools/validate_pressure_tests.py
python3 tools/build.py
python3 tools/validate_reference_links.py
```

For a selected cross-specification composition, use the composition-scoped validation path where available rather than rerunning unrelated corpora.

If the assistant changes a canonical `pressure-test.yaml`, it should regenerate the corresponding human-readable projection and confirm that the repository is clean under the normal validation gates.

See [Developer guide](developer-guide.md), [Cross-spec pressure testing](cross-spec-pressure-testing.md), and [Performance and execution efficiency](performance.md).

## Step 7 — require a human disposition checkpoint

Before creating an upstream issue, changing governance semantics or asserting normative ownership, review the finding with a human maintainer or responsible decision-maker.

The human checkpoint should answer:

1. Is the evidence correctly interpreted?
2. Is the residual real?
3. Is its classification correct?
4. Who owns the remediation?
5. What constitutes completion?
6. What evidence should trigger the RAHP retest?

A Discussion or equivalent research thread can be useful when the interpretation or ownership is still contested. An Issue is more appropriate once the residual is evidence-backed and actionable.

## Step 8 — retest after remediation

Do not close the evidence lifecycle when a patch or specification change lands.

Ask the assistant to:

1. preserve the prior assessment as lineage evidence;
2. inspect the remediation at an immutable revision;
3. rerun the affected scenarios/evidence closure;
4. compare old and new findings;
5. record any residual risk; and
6. update the formal RAHP record only when the new evidence supports the change.

## Copyable prompt — quick assessment

```text
Use the RAHP Toolkit in this repository to perform an initial assessment of <TARGET>.

Do not rely on model knowledge as evidence. Inspect the authoritative target source, record the reviewed revision, reuse existing RAHP personas/scenario patterns/corpora where applicable, and identify candidate pressure points.

Keep hypotheses separate from formal findings. For every candidate finding, show the supporting source evidence and say whether it is confirmed, refined, weakened, contradicted, governance-only, profile clarification required, or insufficient evidence.

Run the applicable RAHP validators before presenting the result. Do not create upstream issues or change the target project automatically.
```

## Copyable prompt — full source-pinned pressure test

```text
Perform a full source-pinned RAHP pressure test of <TARGET> using the RAHP Toolkit in this repository.

1. Resolve and record immutable source revisions for every authoritative source used.
2. Inspect existing RAHP corpora, personas and scenario patterns before adding new material.
3. Build positive, negative and adversarial cases sufficient to cover the target's important authority, privacy, lifecycle, composition, redress and misuse surfaces.
4. Where the claim spans multiple artifacts or specifications, construct the complete evidence closure rather than evaluating each component independently.
5. Map Persona → Scenario → Risk → Harm → Enabler → Control → Guardrail → Assurance evidence → Residual risk → likely owner where supported by the method.
6. Treat model reasoning as analysis, not evidence. Cite the source path/revision for every evidence-backed observation.
7. Preserve hypotheses until they survive evidence review and construction. Explicitly classify weakened, contradicted, governance-only and insufficient-evidence cases.
8. Produce/update the canonical machine-readable RAHP assessment artifacts and regenerate derived human-readable views.
9. Run all applicable repository validators and report any failure rather than bypassing it.
10. Do not create upstream work items automatically. First present the evidence-backed residuals, likely ownership and explicit retest/completion criteria for human disposition.
```

## Copyable prompt — reassess after remediation

```text
Reassess RAHP finding <FINDING-ID> after the remediation at <REVISION>.

Use the prior assessment as immutable lineage evidence. Inspect the remediation at the stated revision, rerun only the affected scenarios/compositions plus any dependencies required for evidence closure, and compare the new evidence with the original finding and retest condition.

Classify the finding as resolved, refined, still open, superseded, or insufficiently evidenced. Do not mark it resolved merely because a patch exists. Regenerate and validate the canonical RAHP artifacts before recommending any issue closure.
```

## Focused prompt patterns

For narrower tasks, the same evidence discipline applies. AI assistance is useful for:

- structuring an extreme-user profile from supplied fieldwork or source notes;
- synthesising a persona from multiple verified inputs;
- cross-referencing a design decision against an existing risk catalogue;
- drafting user stories from a validated objectives map; and
- identifying possible persona/pressure coverage gaps.

For each task, provide the relevant RAHP artifacts as context, require the assistant to flag extrapolation, and treat the output as a draft until the source evidence and interpretation have been reviewed.

The assistant should not assign authoritative risk scores, claim that an operational guardrail passed without observed evidence, make governance decisions, replace participant fieldwork, or be treated as a source-verification mechanism.

## Example: from Discussion to issue to retest

The guardianship/fiduciary constrained-authority example demonstrates the intended discipline:

1. broad hypotheses were first discussed and recorded;
2. source-pinned evidence weakened or refined several of them;
3. three concrete evidence-closure cases were constructed;
4. a post-construction RAHP retest collapsed ten candidate findings to four residuals;
5. only those four evidence-backed residuals became RAHP issues; and
6. upstream DTG work items remain a later disposition decision rather than an automatic result of the RAHP run.

See [`examples/cross-spec/guardianship-fiduciary/`](../examples/cross-spec/guardianship-fiduciary/) and [Discussion #51](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/discussions/51).

## Review checklist for AI-assisted runs

Before accepting an AI-assisted RAHP assessment, confirm that:

- [ ] authoritative sources are identified and immutable revisions are recorded where required;
- [ ] model statements are not presented as source evidence;
- [ ] existing corpora and portable patterns were reused before new ones were introduced;
- [ ] positive, negative and adversarial cases were considered;
- [ ] cross-spec claims were evaluated across complete evidence closure;
- [ ] hypotheses and formal findings remain distinguishable;
- [ ] governance-only and insufficient-evidence outcomes were not artificially converted into specification defects;
- [ ] generated files came from canonical structured sources;
- [ ] applicable RAHP validators passed;
- [ ] human review occurred before upstream issue creation or normative disposition; and
- [ ] every open finding has an explicit retest condition.

AI assistance should make RAHP faster and easier to operate. It should not lower the evidentiary threshold that makes the result trustworthy.
