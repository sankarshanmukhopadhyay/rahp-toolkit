---
layout: default
title: "Quick start"
nav_order: 21
has_toc: true
---
# RAHP Quickstart

This page is retained as a compatibility entry point. The canonical onboarding path is [Getting started](docs/getting-started.md), which is maintained with the current release architecture and links to the detailed method pages.

For a fresh checkout, the minimum validation path is:

```bash
pip install -r requirements.txt
python3 tools/validate.py
python3 tools/review.py --help
```

Then continue with [Getting started](docs/getting-started.md) to configure a target, choose a review mode, preserve source provenance, interpret results conservatively, and move into continuous reassessment when the target changes.

## Common next steps

- [Adopt RAHP for another project](ADOPTION.md)
- [Configuration-driven adoption](docs/configuration.md)
- [Pressure-test a specification](docs/pressure-testing-a-spec.md)
- [Cross-specification pressure testing](docs/cross-spec-pressure-testing.md)
- [Interpreting results](docs/interpreting-results.md)
- [Continuous assurance](docs/continuous-assurance.md)
- [Use an AI agent](docs/using-an-ai-agent.md)
- [Developer guide](docs/developer-guide.md)

Worked assessments remain under `examples/`. They are curated evidence and adoption examples, not the default storage location for ordinary run artefacts.

A command or workflow completing successfully is not an assurance conclusion. RAHP terminal outcomes remain evidence-conservative, and missing evidence never becomes PASS.
