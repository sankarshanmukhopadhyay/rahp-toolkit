---
layout: default
title: "Assurance evaluation"
nav_order: 7
has_toc: true
parent: Run assessments
---
# Evidence-driven assurance evaluation

RAHP separates **signals** from **assurance conclusions**. A detector, reviewer, static analyser, scenario corpus, or resilience rule may identify a risk signal, but that signal does not become a finding until relevant control evidence, assurance evidence, contradictory evidence, and target context have been evaluated.

The portable assurance-evaluation object preserves residual states including `assured`, `controlled`, `finding`, `assurance-gap`, `review-required`, `not-assessed`, and `not-applicable`. These states are intentionally richer than pass/fail. In particular, **zero findings is not a pass** when assurance gaps, review-required propositions, or unassessed propositions remain.

These evaluation residuals are not the autonomous controller's terminal-state vocabulary. Current controller flows terminate into defined outcomes such as `PASS`, `FAIL`, `NOT_APPLICABLE`, `INDETERMINATE/evidence-required`, `INDETERMINATE/model-gap`, upstream-action, or defined controller/contract error states. The evaluation object supplies evidence-rich reasoning that can contribute to reconciliation and posture without creating a second controller state machine.

`method/schema/assurance-evaluation.schema.json` defines the portable object. Each evaluation contains a proposition, detector/reviewer signals, credited control evidence, assurance-test evidence, and a residual conclusion with reasoning and any missing evidence obligations.

Evidence references are typed by context (`normative-spec`, `implementation`, `test`, `deployment`, `governance`, `operational-evidence`, `build-infrastructure`, `documentation`, `example`, `historical`) and authority (`normative`, `authoritative`, `supporting`, `informative`, `incidental`). This prevents incidental repository text from being treated as equivalent to normative or implementation evidence.

## Conservative reference inference

The Python and TypeScript references expose a conservative inference helper. It is not a universal risk-scoring algorithm and it does not replace the controller lifecycle. It demonstrates the invariant that uncertainty must not be converted into assurance:

- risk + absent control or failed assurance evidence → `finding`;
- risk + present control + passing assurance evidence → `controlled`;
- risk + present control + incomplete assurance evidence → `assurance-gap`;
- risk without enough control evidence → `review-required`;
- evidenced control + passing test without a risk signal → `assured`;
- otherwise → `not-assessed`.

```bash
python3 tools/assurance_cli.py validate-evaluation evaluation.json
python3 tools/assurance_cli.py summarize result.json
```

See [Interpreting results](interpreting-results.md) for the distinction between evaluation residuals, controller terminal outcomes and portfolio/deployment posture.
