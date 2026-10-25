---
layout: default
title: "DTG ZKP legacy-scenario semantic requalification"
parent: "Scenario corpora"
has_toc: true
nav_exclude: true
---
# DTG ZKP legacy-scenario semantic requalification

**Tracker:** [#1147](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1147)  
**Authority:** `trustoverip/dtgwg-zkp-spec@cfd94063e5cfee7ba6df4dcfd28c10399a0ffd0a`  
**Machine record:** `corpora/reviews/dtg-zkp-semantic-requalification-2026-10-25.yaml`

## Result

All 30 retained `UC-*` scenarios were reviewed against the immutable specification/conformance authority established by #782 and #1145.

| Disposition | Count | Meaning |
|---|---:|---|
| Retain | 13 | The pinned specification directly supports the pressure question. |
| Revise | 9 | The pressure remains supported, but the legacy wording exceeded the source's stated inference boundary and was narrowed. |
| Scenario-baseline | 8 | The scenario remains a useful pressure-test hypothesis, but the reviewed ZKP specification does not substantiate it as a current source-grounded requirement or construction. |

The corpus therefore has **mixed grounding**. It remains without a corpus-wide `evidence_grade`; assigning `source-pinned` would overstate the eight scenario-baseline cases.

## Disposition matrix

| Scenario | Disposition | Current evidence basis / boundary |
|---|---|---|
| UC-001 | Revise | Record 002 supports context-scoped reuse detection but explicitly does not establish global one-person uniqueness. |
| UC-002 | Retain | Records 001/010 and the trust-graph lifecycle support private membership/community-anchored evidence. |
| UC-003 | Scenario-baseline | Attribute predicates are generally in scope, but no reviewed age/range construction exists in the pinned record set. |
| UC-004 | Revise | Record 003 and the integration profile support request/transcript binding; transaction value and step-up policy are application concerns. |
| UC-005 | Scenario-baseline | No account-recovery construction or recovery lifecycle is defined by the pinned ZKP specification. |
| UC-006 | Revise | Record 004 supports holder/key continuity; records 002/004 explicitly do not establish same-natural-person identity. |
| UC-007 | Revise | Record 002 supports scoped reuse detection, not global one-claim semantics. |
| UC-008 | Scenario-baseline | Scoped reuse detection exists, but election eligibility, ballot secrecy and one-vote governance are not specified. |
| UC-009 | Retain | Record 020 explicitly specifies delegated-authority presentation while preserving the act/execution boundary. |
| UC-010 | Revise | Record 003 + record 020 support request binding and delegation evidence, not proof of intent confirmation. |
| UC-011 | Retain | Records 020/021 explicitly define delegation and attenuated-authority presentations. |
| UC-012 | Revise | Record 006 supports non-revocation/status freshness but not correctness of a registry suspension decision. |
| UC-013 | Revise | Integration guidance requires policy/profile revision and freshness to be bound into the authenticated request. |
| UC-014 | Retain | Offline witness constraints, self-carrying status evidence and unavailable-registry policy are explicit concerns. |
| UC-015 | Revise | Integration guidance requires explicit root authority, update rules, historical acceptance and staleness; silent substitution is invalid. |
| UC-016 | Scenario-baseline | Cross-border or mutual-recognition governance is not defined in the reviewed ZKP baseline. |
| UC-017 | Retain | Target-device feasibility and measured construction cost are explicit evidence questions. |
| UC-018 | Retain | Offline counterparty/witness constraints and accepted status evidence are explicit. |
| UC-019 | Retain | Holder binding explicitly does not establish non-transfer or absence of account sharing. |
| UC-020 | Scenario-baseline | No accessibility-specific construction, alternative-liveness requirement or conformance rule is present. |
| UC-021 | Revise | Holder-key control is supported, while secure custody/non-transfer are explicit limitations; proof cannot establish an uncompromised wallet. |
| UC-022 | Retain | Hosted prover, witness custody and external policy components are part of the stated trust/adversary boundary. |
| UC-023 | Retain | Verifier and colluding-verifier adversaries and disclosure/context boundaries are explicit. |
| UC-024 | Retain | Issuer-verifier collusion is explicitly represented in construction adversary models. |
| UC-025 | Retain | The specification explicitly warns that composed proofs need fresh disclosure/negative-space analysis because individually sound proofs can leak jointly. |
| UC-026 | Retain | Profiles bind construction/circuit version, proof parameters, hashes and layouts; weaker alternatives must not be silently substituted. |
| UC-027 | Scenario-baseline | Appeals/redress are not defined as ZKP construction or conformance behavior. |
| UC-028 | Scenario-baseline | No emergency/degraded-operation proof profile is specified. |
| UC-029 | Scenario-baseline | Batch-verification semantics, logging obligations and throughput conformance are not specified. |
| UC-030 | Retain | Integration guidance requires concrete profiles and interoperable vectors before interoperability may be claimed. |

## Canonical wording changes

Nine legacy rows were narrowed in `corpora/dtg-zkp.yaml` so that the corpus does not imply more than the source supports:

- UC-001: global “one account/person” → context-scoped reuse detection.
- UC-004: high-value transaction/step-up → transcript-bound consequential presentation.
- UC-006: same-human login → controller continuity across presentations.
- UC-007: one benefit claim → single-use policy in an explicitly declared context.
- UC-010: agent step-up/intent confirmation → agent request binding with authority/intent separation.
- UC-012: issuer suspension → credential/authority status freshness.
- UC-013: generic policy version change → policy/profile version binding.
- UC-015: registry conflict → registry-root and policy disagreement.
- UC-021: compromised wallet → holder-secret/wallet compromise as a limitation of holder binding.

The other source-grounded rows gain source anchors to the pinned specification or construction record. Scenario-baseline rows intentionally do not gain artificial anchors.

## Assurance boundary

This review establishes **scenario semantics at one immutable source revision**. It does not establish implementation conformance, runtime safety, normative adoption of every informative construction record, or a corpus-wide source-pinned grade.

The pinned specification itself states that current construction records cover only part of the broader use-case space and separates proof verification from policy acceptance, authorization, execution and action receipt. The requalification preserves those boundaries rather than filling them from model knowledge.

## Reproduction

Run:

```bash
python3 tools/validate_scenario_corpora.py
python3 tools/validate_zkp_scenario_requalification.py
python3 -m unittest discover -s tests -p 'test_zkp_scenario_requalification.py' -v
```

The dedicated validator requires exactly one disposition for each `UC-001` through `UC-030`, pin consistency with the canonical corpus, source evidence for every retained/revised case, and no corpus-wide evidence grade while mixed grounding remains.
