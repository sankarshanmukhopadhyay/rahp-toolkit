---
layout: default
title: "Getting started"
nav_order: 1
has_toc: true
parent: Learn RAHP
---
# Getting started

This page is the shortest path from a fresh checkout to a useful RAHP review. It routes to the detailed method pages rather than duplicating them.

## 1. Install and validate

RAHP's primary tooling is Python-based. From the repository root:

```bash
pip install -r requirements.txt
python3 tools/validate.py
```

For the TypeScript reference implementation:

```bash
npm install
npm run build:ts
npm run test:ts
```

If you are modifying the repository rather than only running a review, use the full validation inventory in the [Developer guide](developer-guide.md).

## 2. Inspect the unified review entry point

```bash
python3 tools/review.py --help
```

RAHP supports complementary review modes rather than one all-purpose score. Choose the mode that matches the question you are asking. See [Review modes](review-modes.md).

## 3. Start with a minimal configuration

Validate the portable example configuration and list its targets:

```bash
python3 tools/rahp.py config-validate --config examples/configurations/minimal.yaml
python3 tools/rahp.py targets --config examples/configurations/minimal.yaml
python3 tools/validate_portability.py
```

Configuration separates the portable method from deployment-specific repositories, paths and policy. See [Configuration](configuration.md) and [Adopting RAHP](../ADOPTION.md).

## 4. Pick a review path

| Goal | Guide |
|---|---|
| Review one specification for risks and harms | [Pressure-testing a specification](pressure-testing-a-spec.md) |
| Add a security/adversarial lens | [Security and hardening review](security-hardening-review.md) |
| Review several specifications as one system | [Cross-spec pressure testing](cross-spec-pressure-testing.md) |
| Use domain scenarios as reusable test vectors | [Scenario corpora](scenario-corpora.md) |
| Understand how evidence supports a result | [Evidence classification](evidence-classification.md) |
| Understand a completed result | [Interpreting results](interpreting-results.md) |

A useful first exercise is to open one of the worked assessments under `examples/`, read its canonical `pressure-test.yaml`, and compare it with the rendered `README.md`. The YAML is the review record; rendered Markdown is the human-facing projection.

## 5. Preserve provenance

A review should identify the target revision actually examined. For changing upstream specifications, prefer an immutable commit pin over an unversioned branch head. Scenario corpora follow the same rule: advancing a source repository does not automatically advance the reviewed corpus baseline.

See [Corpus synchronization and provenance](corpus-synchronization.md) and [Review evidence and retention](evidence-retention.md).

## 6. Interpret conservatively

RAHP distinguishes several residual states. In particular, **no finding does not mean assured**. Evidence may still be incomplete, stale, inapplicable or require human disposition.

Use [Assurance evaluation](assurance-evaluation.md), [Interpreting results](interpreting-results.md), and [Continuous assurance](continuous-assurance.md) when moving from a one-time assessment to durable assurance.

## 7. After a material change

Do not automatically rerun everything. Use impact analysis and evidence freshness to determine what must be reassessed, then preserve the old record and record the assurance delta.

The lifecycle is:

```text
material change
  → impacted propositions
  → evidence freshness
  → focused reassessment
  → finding / gap / controlled / assured
  → remediation and retest
  → governed disposition
```

See [Assurance graph and impact analysis](assurance-graph-impact.md), [Evidence provenance and freshness](evidence-freshness-delta.md), and [Remediation and retesting](remediation-lifecycle.md).
