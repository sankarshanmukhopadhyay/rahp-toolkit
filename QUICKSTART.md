---
layout: default
title: "Quick start"
nav_order: 21
has_toc: false
---
# RAHP Quickstart

This page is retained as a compatibility entry point. The canonical onboarding path is [Getting started](docs/getting-started.md).

For a fresh checkout, the minimum validation path is:

```bash
pip install -r requirements.txt
python3 tools/validate.py
python3 tools/review.py --help
```

Then continue with [Getting started](docs/getting-started.md). For adoption into another project use [Adopting RAHP](ADOPTION.md); for result semantics use [Interpreting results](docs/interpreting-results.md); for post-change reassessment use [Continuous assurance](docs/continuous-assurance.md); and for repository internals use the [Developer guide](docs/developer-guide.md).

Worked assessments remain under `examples/` as curated evidence and adoption examples.
