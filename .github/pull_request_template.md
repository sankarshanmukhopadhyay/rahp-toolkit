## What changed

<!-- One or two sentences. -->

## Artefact IDs affected

<!-- e.g. RK-ID07 (new), CT-67 (new), GR-07 (updated), M-12 (updated) -->

## Provenance — what triggered this change?

<!-- Spec section, discussion thread, practitioner report, threat intelligence,
     review session. Every new or materially changed record needs a provenance
     block in the YAML as well. -->

## Durable artefact placement

<!-- For every new durable file, identify its role: normative/profile authority,
     executable contract, executable implementation, evidence, assurance judgment,
     historical record, or canonical reader documentation. If it fits none of these,
     prefer preserving the material in the Issue/PR/Discussion record. For reader
     documentation, state why an existing canonical page cannot own the material. -->

- New durable file(s), if any:
- Role / canonical owner:
- Existing document considered before adding new reader documentation:

## Validation output

<!-- Paste the output of: python3 tools/validate.py --summary -->

```
```

## Checklist

- [ ] `python3 tools/validate.py` exits 0
- [ ] Every new/changed record has a `provenance` block
- [ ] New guardrails have an assurance test; new controls reach a metric
- [ ] No generated file under `build/` was edited by hand
- [ ] If a risk score changed, the evidence for the change is stated above
- [ ] New durable files have a clear role and do not duplicate an existing canonical reader document
