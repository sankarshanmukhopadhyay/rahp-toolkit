---
layout: default
title: "Review modes"
nav_order: 2
has_toc: true
parent: Run assessments
---
# Review modes

RAHP exposes three coordinated review modes through `tools/review.py`.

> **v0.8 storage default:** `review.py init` writes working review artefacts under ignored `.rahp/reviews/`. This prevents ordinary runs from automatically growing the committed `examples/` corpus. Use `review.py promote` only when a completed review is intentionally maintained as a worked example. Deployment dispositions belong under `instances/<id>/reviews/` as compact records.


## 1. RAHP pressure test

Use the RAHP lens when the primary question is:

> What harms, governance failures, assurance gaps, affected-party consequences, or trust-system weaknesses remain?

```bash
python3 tools/review.py init \
  --mode rahp \
  --slug example-spec \
  --title "Example Specification" \
  --repository owner/repo \
  --version "Draft 0.1" \
  --commit <40-character-sha>
```

The default working record is `.rahp/reviews/<slug>/pressure-test.yaml`, with a sibling `README.md`. If the review is deliberately promoted as a maintained exemplar, those become `examples/<slug>/pressure-test.yaml` and `examples/<slug>/README.md`.

## 2. Security-hardening review

Use the security lens when the primary question is:

> How can an adversary, compromised component, malicious participant, or unsafe implementation violate a security property?

```bash
python3 tools/review.py init \
  --mode security \
  --slug example-spec \
  --title "Example Specification" \
  --repository owner/repo \
  --version "Draft 0.1" \
  --commit <40-character-sha>
```

The default working record is `.rahp/reviews/<slug>/security-findings.yaml`, with `SECURITY_REVIEW.md`. A promoted exemplar uses `examples/security-hardening/<slug>/findings.yaml` and its sibling report.

## 3. Combined review

Combined mode scaffolds both canonical records and a third linkage record:

```bash
python3 tools/review.py init \
  --mode combined \
  --slug example-spec \
  --title "Example Specification" \
  --repository owner/repo \
  --version "Draft 0.1" \
  --commit <40-character-sha>
```

By default this produces one ignored working directory:

```text
.rahp/reviews/example-spec/
  pressure-test.yaml
  README.md
  security-findings.yaml
  SECURITY_REVIEW.md
  combined-review.yaml
```

After accountable review, `review.py promote --mode combined --slug example-spec` may copy the maintained exemplar into the three `examples/` surfaces. Promotion is not required for a normal deployment assessment; durable deployment dispositions belong under `instances/<id>/reviews/`.

The combined report is **not a third independent test**. It synthesizes the two lenses, showing where RAHP and security findings share canonical risks, controls, guardrails, or assurance tests, and which findings remain specific to one lens.

## Analysis is reviewer work

`tools/review.py` scaffolds, renders, validates, and synthesizes. It does not claim to statically scan a specification and discover defensible findings by itself. A human or AI-assisted reviewer must inspect the target and populate the canonical YAML records with evidence.

An `in-progress` scaffold may contain zero findings without breaking CI. Once the review status moves beyond `in-progress`, findings are required and the ordinary validators enforce their structure and references.

## Orchestration commands

Render the selected review mode:

```bash
python3 tools/review.py render --mode combined
```

Validate it:

```bash
python3 tools/review.py validate --mode combined
```

Render and validate in one command:

```bash
python3 tools/review.py run --mode combined
```

Inspect discovered review records:

```bash
python3 tools/review.py status
```

The lower-level renderer and validator scripts remain available for automation and CI.

### Deployment-local references

Pressure-test validation may resolve deployment-local catalogue IDs from `instances/<id>/data/` without importing them into the bundled DTG `data/` catalogue. Rendering preserves that authority boundary: a deployment-local record with an explicit `link` uses that deployment-owned link; without one, the renderer shows the ID and title as code rather than manufacturing a deep link into the DTG catalogue.
