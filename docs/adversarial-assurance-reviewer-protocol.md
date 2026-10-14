---
layout: default
title: "Adversarial assurance reviewer challenge"
parent: Learn RAHP
---
# Independent adversarial challenge protocol

Tracking: [#1023](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1023). Campaign threat model: [adversarial assurance qualification](adversarial-assurance-qualification.md).

**Status: available for external use, NOT INDEPENDENTLY EXECUTED.** The maintainer-authored tests and successful CI do not establish an independent red-team assessment.

## Scope and authority

Exercise the **RAHP assurance instrument**, not unrelated production infrastructure. Use synthetic or otherwise authorized inputs and a pinned checkout of the target source. No credential misuse, external-service disruption, or unauthorized modification of third-party assets.

An external reviewer may challenge: evidence adequacy, declared versus authenticated provenance, historical and current source authority, full-stack lens inclusion, failure/timeout handling, assessment report representations, and controller transition reachability.

Reviewers should devise at least one **novel** attack rather than merely replaying listed maintainer fixtures. The outcome may be a valid non-finding.

## Baseline and first reproduction

Record the exact checkout SHA, Python version, operating system and run ID. For the initial maintainer campaign the starting baseline was `88cf85e09375483b526e57d4873274ca8860d82d` (2026-10-14). For a reviewer campaign, **record and test the actual selected current commit**, not that earlier starting baseline by assumption.

```bash
git rev-parse HEAD
python3 --version
python3 -m unittest tests.test_adversarial_assurance_1023 -v
python3 -m unittest tests.test_evidence_adequacy tests.test_temporal_provenance tests.test_reproducibility_challenge -v
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/validate.py
```

These commands form a reproducibility starting point. Execute in a disposable checkout with controlled fixtures. Save stdout/stderr and exit codes separately. Check the repository's then-current validation workflow for additional required checks.

## Reviewer-owned challenge

1. Choose a materially consequential assurance claim and identify the **trust boundary** at which RAHP accepts data or transitions state.
2. Describe attacker control, constraints, target outcome and what would count as a meaningful compromise.
3. Construct a synthetic attack fixture and an unaffected positive control. Preserve the fixture and its SHA-256 hash.
4. Run both using the same pinned RAHP implementation and configuration; save unmodified outputs, exceptions and logs.
5. Separate **attack delivered**, **guard triggered**, and **assurance integrity compromised**. Avoid interpreting rejection or technical parse success as assurance success.
6. If a bypass is observed, reproduce it before recommending a fix, identify the narrowest enforcement point and prove the regression afterward.
7. Challenge both the machine result and the *reader-facing representation*. A syntactically valid R1 PASS, R2 APPLICABLE or R3 DECLARED_MATCH has explicitly limited meaning.
8. Document any disagreements and unknowns without silently modifying prior assessment records.

## Evidence-record template

```yaml
scenario_id: "EXTERNAL-001"
reviewer: "independent participant identifier"
authorization_scope: "controlled synthetic fixture"
baseline_sha: "<exact commit>"
runtime: "<python version and environment>"
claim: "<bounded assurance proposition>"
trust_boundary: "<input, transition or report boundary>"
attacker_control: "<specific controlled material>"
attack_hypothesis: "<falsifiable statement>"
expected_safe_behavior: "<observable invariant>"
positive_control:
  command: "<exact command>"
  fixture_sha256: "<sha256>"
  exit_code: null
adversarial_run:
  command: "<exact command>"
  fixture_sha256: "<sha256>"
  stdout_sha256: "<sha256>"
  stderr_sha256: "<sha256>"
  exit_code: null
observations: "<literal supported observations>"
attack_delivery: "SUCCEEDED | FAILED | INDETERMINATE"
assurance_integrity: "RESISTED | COMPROMISED | INDETERMINATE"
failure_layer: "implementation | methodology | operational | none | unknown"
finding_or_challenge_ref: null
residual_risk: "<unresolved limitation>"
```

## Findings and disposition

A confirmed `COMPROMISED` result requires executable evidence of an unsafe **assurance outcome or presentation**. A guard refusal with preserved non-PASS outcome can support a bounded `RESISTED` judgment. Unknown provenance, unavailable evidence, or an unexercised path must remain `INDETERMINATE` or `NOT_EXECUTED` as applicable.

Do not treat the campaign as a certification or infer attack resistance outside exercised surfaces. Independent assessment completion requires an external participant, source-pinned record, raw execution evidence and explicit review disposition. The maintainer cannot grant independence merely by publishing this protocol.
