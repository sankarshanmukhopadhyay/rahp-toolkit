# Dogwood → Eucalyptus comparative assurance example

This directory preserves the first end-to-end validation output for the RAHP Comparative Assurance Digest.

The example is intentionally difficult: Dogwood and Eucalyptus differ in assessment boundary and proposition coverage. The resulting digest therefore records material improvement in assessment capability and evidence preservation without claiming that Eucalyptus is better assured or acceptable for release.

## Reproduce

```bash
python3 tools/rahp.py compare \
  --baseline fixtures/comparative-assurance/dogwood-assessment.json \
  --candidate fixtures/comparative-assurance/eucalyptus-assessment.json \
  --profile fixtures/comparative-assurance/release-comparison-profile.json \
  --output /tmp/rahp-dogwood-eucalyptus

diff -u examples/comparative-assurance/dogwood-eucalyptus/comparison.json \
  /tmp/rahp-dogwood-eucalyptus/comparison.json
diff -u examples/comparative-assurance/dogwood-eucalyptus/comparison.md \
  /tmp/rahp-dogwood-eucalyptus/comparison.md
```

## Boundary

Dogwood and Eucalyptus are validation fixtures, not hard-coded release concepts. The comparison engine accepts any assessment pair and comparison profile that satisfy the portable input and digest contracts. Release identity, dimensions, materiality, compatibility, matching rules, evidence requirements and aggregation gates come from input artifacts.

Do not use this example's VTI-specific profile or dimension set as a universal model. A different release family should supply its own assessment artifacts and profile.

## Bounded conclusion

The preserved output establishes:

- assessment capability materially improved;
- evidence preservation materially improved;
- composition assurance remains indeterminate;
- privacy assurance is not comparable under the available profiles;
- overall release assurance is indeterminate; and
- release superiority is not established.

The fixture does not independently replay the underlying Dogwood and Eucalyptus campaigns. Its evidence references preserve the source lineage used by the manual design validation in issue #967.
