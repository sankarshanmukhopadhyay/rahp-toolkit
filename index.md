---
layout: default
title: Home
nav_order: 1
has_toc: true
---
# RAHP Toolkit

RAHP is a reusable **Risk Assessment & Harms Prevention** method for pressure-testing standards against human harms, security failures, governance weaknesses and operational edge conditions.

{: .decision }
RAHP now supports **scenario-driven pressure testing**: a specification can be tested against reusable scenario patterns and domain-specific scenario corpora, not only reviewed as static text.

## Start here

**Not a specification author?** Start with [Reading a scenario corpus](docs/reading-scenario-corpus.md) to understand what a scenario says about possible failure, affected people and evidence, and what it does not establish.


- [How RAHP works](docs/how-rahp-works.md)
- [Pressure-testing a specification](docs/pressure-testing-a-spec.md)
- [Scenario-driven pressure testing](docs/scenario-driven-pressure-testing.md)
- [Scenario corpora](docs/scenario-corpora.md)
- [Review modes](docs/review-modes.md)
- [Use an AI agent to run a pressure test](docs/using-an-ai-agent.md)
- [Security-hardening review](docs/security-hardening-review.md)
- [Adoption guide](ADOPTION.md)
- [Quick start](QUICKSTART.md)
- [CAWG/C2PA external instance](docs/cawg-instance.md)
- [CAWG/C2PA worked pressure tests](examples/cawg-c2pa/README.md)
- [GitHub Pages coverage](docs/pages-coverage.md)

## Assurance chain

```mermaid
flowchart LR
  S[Specification] --> C[Scenario corpus]
  C --> P[Scenario patterns]
  P --> A[Actors / personas]
  A --> R[Risks and harms]
  R --> CT[Controls]
  R --> G[Guardrails]
  G --> T[Assurance tests]
  CT --> F[Findings]
  T --> F
  F --> X[Specification / governance action]
```

## Deployment model

RAHP Toolkit is the portable method and engine. **DTG and CAWG/C2PA are deployments, not the identity of the toolkit.** The bundled DTG material preserves project provenance and provides mature scenario/governance examples; CAWG/C2PA is the first substantial external deployment proof. Each deployment retains independent scope, assessment vocabulary, monitoring state and governance.
