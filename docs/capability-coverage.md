# Capability coverage packs

Capability coverage is a portable RAHP mechanism for expressing assurance propositions about a bounded subject without adding that subject's vocabulary to RAHP core.

## Contract

A coverage record identifies a subject, assessment maturity, and propositions. Each proposition selects a generic assurance pattern, an evidence provider, required evidence, evidence references, and a scoped judgment.

Supported maturity levels are `architectural`, `specification`, `implementation`, `runtime`, and `deployment`. Maturity and judgment are independent: evidence that satisfies a proposition at one maturity does not satisfy the same proposition at a later maturity.

Judgments are `SATISFIED`, `UNSATISFIED`, `INDETERMINATE`, `EVIDENCE_REQUIRED`, and `NOT_APPLICABLE`. Missing required evidence cannot produce `SATISFIED`.

Providers identify the source/owner of evidence, not the final assurance authority: `rahp`, `dpip`, `interop-lab`, `external`, or `human-judgment`.

## Generic patterns

The initial registry covers context isolation, positive disclosure, provenance preservation, authority non-composition, capability attenuation and chain integrity, lifecycle/current-authority integrity, confidentiality boundaries, unlinkability/correlation, rollback/freshness integrity, operator independence, untrusted agent input, human handling of untrusted content, and cross-context aggregation/non-inference.

Subject-specific vocabulary belongs in instance coverage packs, not in this registry.

## Example

```yaml
coverage:
  id: example-capability
  subject: example
  maturity: implementation
  propositions:
    - id: P-EX-001
      pattern: context-isolation
      provider: rahp
      judgment: SATISFIED
      assessed_at_maturity: implementation
      evidence_required:
        - negative access evidence
      evidence:
        - source: example-implementation
          revision: abc123
```

Evidence references should retain source identity and revision. RAHP's existing freshness/reconciliation machinery remains authoritative for determining whether a source change makes evidence stale or requires retest; coverage does not introduce a competing freshness state machine.

## Validation and reporting

Run:

```bash
python3 tools/capability_coverage.py path/to/coverage.yaml --summary
```

The summary reports propositions defined and assessed, plus counts for each judgment. Validation rejects duplicate/missing proposition identifiers, unknown maturity/provider/judgment/pattern values, satisfaction without required evidence, and implicit maturity promotion.

## Claim boundary

A coverage pack supports only the maturity and evidence actually recorded. Architectural evidence is not implementation evidence; implementation evidence is not runtime or deployment evidence. `EVIDENCE_REQUIRED` is an explicit assurance outcome and never aliases PASS.
