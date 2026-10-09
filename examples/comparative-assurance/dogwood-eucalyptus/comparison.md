# Comparative Assurance Digest: dogwood-to-eucalyptus

> This report is a non-normative rendering of the machine-readable comparison artifact. It informs but does not replace accountable human acceptance or release authority.

## Summary

| Field | Result |
|---|---|
| Baseline | VTI-Dogwood-RC-1 |
| Candidate | VTI-Eucalyptus |
| Comparability | partial |
| Overall judgment | indeterminate |
| Confidence | high |
| Release disposition | indeterminate |
| Release superiority established | no |

Profile gates produced an indeterminate comparison: Candidate coverage partial is below required bounded.

## Scope and coverage

- Boundary change: **changed**
- Material scope change: **yes**
- Coverage: **bounded → partial** (weakened)
- Newly admitted components: rahp-toolkit, vti-composition
- Added directly assessed components: vti-composition
- Added supporting dependencies (not independently assessed by inclusion): rahp-toolkit

## Dimension judgments

| Dimension | Category | Comparability | Judgment | Confidence |
|---|---|---|---|---|
| assessment-capability | assessment_process | compatible | materially_improved | high |
| composition-assurance | assurance_outcome | partial | indeterminate | high |
| evidence-preservation | evidence | compatible | materially_improved | high |
| privacy-assurance | assurance_outcome | not_comparable | not_comparable | high |

## Material finding and evidence changes

- **introduced**: none → EUC-EVIDENCE-PRESERVATION; evidence: none
- **changed**: VTI-COMPOSITION → VTI-COMPOSITION; evidence: not_comparable
- **changed**: VTI-PRIVACY → VTI-PRIVACY; evidence: not_comparable

## Unresolved limitations

- A common privacy-pressure profile has not been executed.
- Assessment boundary is changed relative to the baseline.
- Candidate composition propositions remain unclosed.
- Candidate coverage partial is below required bounded.
- Four bounded evidence requirements were assessed.
- Twenty propositions were admitted; substantive evidence gaps remain.

## Recommended next actions

- Execute matched privacy and composition propositions against both releases. (non-normative)

### Reassessment triggers

- Completion of the matched Dogwood and Eucalyptus proposition set
