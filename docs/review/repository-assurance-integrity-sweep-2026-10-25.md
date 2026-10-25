# Repository assurance-integrity sweep — 2026-10-25

**Tracker:** [#1150](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1150)  
**Trigger:** [#1142](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1142)  
**Baseline main:** `23a79aa15f16d88d0cf169ab870c3b38d33d8a83`  
**Stable release:** `v2.9.0` — Common Windmill  
**Published v2.9.0 tag commit:** `89831dd739625a416e5b4d84e3486bbfbed5243f`  
**v2.9.0 qualified evidence candidate:** `f02186c513d028e9532ba66925b709d176248a46`  
**GitHub Actions surface at baseline:** 20 workflow files / governed budget 20

## Purpose and boundary

This is a maintainer-executed adversarial consistency and evidence-integrity sweep of the RAHP Toolkit repository as a **published assurance system**. It asks whether a competent outsider can trace material claims to the authority, evidence, validation path, limitation and currentness/reassessment boundary that actually support them.

It is not an independent audit, certification, penetration test, production-safety determination or proof that every RAHP judgment is substantively correct.

The sweep follows the project engineering guidance:

- authoritative source state is established before judging derived representations;
- missing, stale, contradictory, unavailable and indeterminate evidence remain distinct from PASS;
- deterministic contradictions become regression tests where practical;
- historical records are not rewritten merely to look current;
- new automation is composed into existing workflows rather than creating new GitHub Actions surfaces.

## Existing mechanisms reused

The sweep did not create a parallel assurance framework. It reused:

- `method/review/claim-evidence-ledger.yaml`;
- `method/review/false-assurance-challenges.yaml`;
- `tools/validate_review_readiness.py`;
- `tools/validate_pressure_tests.py` and `tools/render_pressure_tests.py`;
- `tools/validate_workflow_governance.py`;
- `tools/corpus_claim_integrity.py` and scenario-corpus validation;
- current release declaration/qualification/evidence machinery;
- existing negative fixtures, unit tests and generated-view checks.

## Claim inventory coverage

The maintained claim/evidence ledger now covers eleven high-materiality propositions spanning:

1. missing evidence and positive assurance;
2. workflow success versus assurance outcome;
3. component versus composition PASS;
4. source freshness and reassessment;
5. specialist uncertainty;
6. governance authority versus policy/repository permission;
7. stable compatibility metadata;
8. corpus provenance/evidence-grounding integrity;
9. independent-review boundary synchronization;
10. the governed 20-workflow Actions budget; and
11. release dependency reproducibility and its limits.

The ledger remains a bounded reviewer entry path, not an exhaustive enumeration of every sentence in the repository.

## Findings and disposition

### AIS-001 — current reviewer pack contained stale stable-release metadata

**Classification:** cross-artifact contradiction / documentation defect  
**Observed:** `review/README.md` and the claim ledger were synchronized to v2.9.0, while `docs/review/review-readiness-baseline.md`, `docs/review/reproduction.md` and `docs/review/known-limitations.md` still described the current review boundary using v2.4.0-era release and dependency statements.

**Why it matters:** a cold reader could follow the reviewer entry point and receive contradictory instructions about the stable subject and dependency reproducibility boundary.

**Disposition:** remediated.

- current reviewer-facing baseline/reproduction/limitations now identify v2.9.0;
- release hash-locking is distinguished from the flexible contributor/test environment;
- the v2.4 hostile-input security pre-review is retained as historical evidence and explicitly labelled historical;
- `validate_review_readiness.py` derives the stable release from `method/versioning.yaml` and rejects stale current-review documents;
- negative regression coverage intentionally substitutes an older stable release and confirms rejection.

### AIS-002 — historical three-spec review hid component pins behind stale “current main” wording

**Classification:** authority/provenance ambiguity / publication defect  
**Observed:** the historical Credential × ZKP × Trust Tasks pressure test contains explicit immutable component pins, but its human-facing target version said “Credential Specification current main × ZKP current main” and the generated metadata displayed only one aggregate commit.

**Why it matters:** the underlying record was more precise than its published representation. A reader could mistake a 2026-08-27 historical snapshot for current source authority or assume the single displayed SHA covered the complete three-repository composition.

**Disposition:** remediated without rewriting the historical findings.

- the canonical target description now says the assessment is against recorded immutable component commits;
- the renderer exposes each component repository and full SHA;
- multi-repository pressure-test validation requires matching repository/commit key sets and full immutable SHAs;
- pinned multi-repository reviews cannot describe their target as “current main”;
- the README explicitly distinguishes historical ZKP task-force evidence from the current maintained `dtgwg-zkp-spec` authority established later by #1145/#1147;
- negative tests cover key mismatch, symbolic component revisions, stale current-main wording and aggregate-pin mismatch.

### AIS-003 — v2.9 release evidence SHA and published tag commit require an explicit lineage interpretation

**Classification:** release provenance gap / acceptable historical release pattern with hardening required  
**Observed:** v2.9.0 evidence is pinned to qualified candidate `f02186c…`; the annotated release tag points to `89831dd…`, one descendant commit later. Issue #1126 records this intentionally as “candidate evidence SHA” → “qualified release commit”. The intervening commit changed release/publication metadata and documentation, not executable implementation.

**Why it matters:** without the issue trail, a reviewer could reasonably ask whether post-evidence code changed before the tag was cut.

**Disposition:** historical v2.9 lineage retained and future publication hardened.

- this report records the candidate/tag relationship in-repository;
- `tools/validate_release_candidate_lineage.py` requires the qualified candidate to be an ancestor of the release head;
- any post-candidate changes must be confined to a bounded release/publication metadata allow-list;
- executable code or test changes after the evidence SHA cause publication rejection unless a new qualification baseline is produced;
- the existing `release.yml` runs this check both before the publication handoff and again in the write-authorized publication job;
- FAC-010 records post-candidate implementation drift as a false-assurance challenge.

This does not retroactively alter the immutable v2.9.0 tag or its qualification record.

### AIS-004 — duplicate current-boundary prose reduced review clarity

**Classification:** documentation defect  
**Observed:** duplicate independent-review wording in `review/README.md` and a duplicated normalized-result sentence in `docs/engine-contract.md`.

**Disposition:** corrected. No semantic contract change.

## Cold-reader reconstruction sample

### Standalone specification review — TRQP

**Result:** reconstructable with appropriate bounds.

A reader can identify the immutable TRQP source pin, retained source files, constructed versus observed evidence, replay commands, open findings, what schema validity establishes and what remains not assessed. The example explicitly states that successful replay is not runtime authorization or full TRQP conformance.

No additional deterministic defect was identified in this sample.

### Historical composed review — Credential × ZKP × Trust Tasks

**Result before remediation:** source pins reconstructable from YAML but inadequately exposed in the rendered reader path.

**Result after remediation:** all component pins are visible, the historical/current authority distinction is explicit, and review-complete remains distinguishable from current corpus provenance state.

### Comparative assurance — Dogwood → Eucalyptus

**Result:** appropriately bounded.

The example states that assessment capability and evidence preservation improved while composition assurance remains indeterminate, privacy is not comparable under the available profile, overall release assurance is indeterminate, and release superiority is not established. The fixture also states that it does not independently replay the source campaigns.

No deterministic overclaim was identified in this sample.

### Controller / terminal assessment — Eucalyptus

**Result:** appropriately fail-closed in the sampled terminal/report surfaces.

The machine record reports `assurance_state: indeterminate`; individual evidence obligations remain `NOT_EVIDENCED` where producers are unavailable; the human report separates component-test execution from service-composition proof and does not convert successful dependency/test execution into terminal assurance.

No deterministic overclaim was identified in this sample.

### Stable release — v2.9.0

**Result:** qualification scope and residuals are materially explicit, with the candidate/tag lineage hardening described in AIS-003.

The release notes preserve NOT_YET_TESTED independent adoption, bounded runtime evidence, #958 NOT VERIFIED admin/human-review residuals and the derived/non-authoritative assurance-registry boundary.

## GitHub Actions budget

No workflow is added by #1150.

The existing policy already enforces:

```yaml
max_workflows: 20
```

and requires an exact declared inventory. The audit adds this as a material claim in the review ledger rather than duplicating the governance mechanism.

Any additional self-audit logic introduced by this tranche executes through existing tooling/tests and the existing validation/release workflows.

## Negative results

A sweeping audit is credible only if it records where the examined paths held up.

The sampled surfaces did **not** show evidence that:

- the comparative digest silently upgrades indeterminate comparison into release superiority;
- the Eucalyptus terminal record converts missing runtime evidence into PASS;
- the standalone TRQP example treats constructed fixtures as captured runtime evidence;
- the current corpus claim-integrity layer inherits parent evidence grades transitively;
- current ZKP source authority has reverted to the downstream fork;
- an additional GitHub Actions workflow is required for this audit.

These negative results are bounded to the examined repository state and paths.

## Residual limitations

This sweep does not establish:

- exhaustive semantic review of all 1,400+ repository files;
- correctness or truth of external source statements;
- independent reviewer agreement;
- comprehensive security or denial-of-service resistance;
- live deployment conformance;
- complete dependency-graph impact representation;
- bit-for-bit reproduction of GitHub-hosted runner images or external services;
- that future prose cannot introduce a new misleading implication that no deterministic rule can recognize.

Historical release-specific documents may legitimately retain old versions and old constraints when they are clearly identified as historical. Current-state validators should not rewrite them to match current main.

## Reproduction

Focused checks introduced or strengthened by this sweep:

```bash
python3 tools/validate_review_readiness.py
python3 tools/validate_pressure_tests.py
python3 -m unittest discover -s tests -p 'test_review_boundary_synchronization.py' -v
python3 -m unittest discover -s tests -p 'test_pressure_test_target_provenance.py' -v
python3 -m unittest discover -s tests -p 'test_release_candidate_lineage.py' -v
python3 -m unittest discover -s tests -p 'test_release_workflow.py' -v
python3 tools/validate_workflow_governance.py
```

The ordinary repository validation and documentation checks remain the broader gates.

## Release decision

**Commit-only.**

The audit produces material hardening, but it does not by itself justify a new consumable release. A future release should include these changes when a coherent user-facing baseline is otherwise warranted. This decision should be revisited if downstream consumers require the new release-lineage or review-integrity guards as a versioned dependency.

## Completion interpretation

The repository is not declared “audited clean.” The stronger and supportable conclusion is:

> Within the executed #1150 scope, material contradictions found by the sweep were either remediated and regression-protected or recorded as bounded historical/provenance conditions. Representative standalone, composed, comparative, controller and release paths were reconstructed without private maintainer context, and no new workflow surface was introduced.
