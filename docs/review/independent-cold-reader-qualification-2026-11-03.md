# Independent cold-reader qualification: RAHP protection coverage and first adoption

**State:** `READY_FOR_EXTERNAL_EXECUTION`, **not executed by an independent reviewer**.  
**Owners:** [research #1159](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1159) for protection-coverage disposition; RAHP maintainer for adoption evaluation.  
**Source boundary:** RAHP `v2.9.0`; [candidate projection](protection-coverage-pilot-2026-11-03.md) with its own historical review pins. The reviewer must record the actual RAHP checkout SHA used.  
**No new normative schema, human score, certification or protection finding is introduced.**

## Purpose and separation of authority

This protocol evaluates two **different** questions:

1. **Reconstruction:** Can a competent reader challenge the three existing protection-coverage conclusions using canonical historical RAHP records, without explanatory assistance?
2. **Adoption:** Can a new user follow the maintained RAHP-only entry path, create and interpret an evidence-bounded review, and identify what remains unverified?

The first evaluates research-method interpretability. The second evaluates the usable software/documentation path. Do not mark either successful because the author completed the other. The maintained machine-only onboarding smoke test already exercises artifact generation and overwrite refusal; it **does not** establish independent human comprehension.

Participation and acceptance are controlled by the actual human reviewer and repository maintainer, respectively. A draft response, completed checklist prepared by an AI, or structural GitHub identity link is not an attributable independent assessment.

## Prerequisites and reviewer independence

A reviewer should have competence in source-controlled specifications, protocol authorization and assurance evidence, but should **not** receive the pilot author's explanation before attempting the tasks. Record any prior contribution to the reviewed source or to RAHP and whether it could bias the judgment. Do not assert an independence property solely from a username.

The maintainer supplies a clean checkout and this instruction, but does not interpret findings during execution. The reviewer records source and operating environment, starts at the published adoption entry point, and is free to reject or qualify the framing.

Avoid personal identifiers, real credentials, private policy, community records and sensitive evidence. Use only the maintained bundled fixtures and repository-pinned public sources.

## Track A: Reconstruct protection-coverage candidate (#1159)

**Entry:** [pilot](protection-coverage-pilot-2026-11-03.md). Follow its three links to the *canonical* Trust Tasks, Credential Specification and composed `pressure-test.yaml` records at pinned RAHP `42df1e2660a0db8221fdf587c9222b628f95419e`.

Without accepting the pilot's labels as facts, answer for **each** canonical source record:

- What exact upstream revision is being interpreted? Is it the same epoch as the other records?
- Which cited specification passages support the recorded observation? Identify any unreachable/missing source link.
- Which statements are normative upstream text, which are RAHP findings, and which are analyst inferences?
- Does authenticated origin, valid membership or scoped ACL state prove effective delegated authority at consequential action time? If not, identify the exact missing authority/status/revocation evidence.
- Is responsibility implemented by the assessed specification, delegated elsewhere, unresolved, or absent from the bounded search? Explain why an empty matrix cell must mean `NOT_ASSESSED`, not `NOT_APPLICABLE`.
- Which dependency revision or contradictory observation would trigger invalidation/reassessment?

Record one of `reconstructed`, `reconstructed_with_disagreement`, `not_reconstructable`, or `not_attempted` **per packet**. These are *study observations*, never portable RAHP assurance-state values. Preserve quotations and source links sufficient for another reviewer to retrace a disagreement; avoid full verbatim copying of third-party specifications.

**Completion criterion:** Three independently reconstructed/challenged packet interpretations, or an attributable explanation for each failure. A disagreement is a substantive result, not a reason to force PASS.

## Track B: Cold-start RAHP-only adoption

**Start:** [adoption gateway](../adoption-guide.md) → [Hello RAHP](../../examples/hello-rahp/README.md) → [real-source TRQP exercise](../../examples/standalone-trqp/README.md).

Use a clean checkout, documented dependencies and only the maintained sample. Record installed Python/package versions and checkout SHA. Execute these documented commands *as written* from the repository root:

```bash
python3 tools/rahp.py config-validate --config examples/hello-rahp/rahp.yaml
python3 tools/rahp.py targets --config examples/hello-rahp/rahp.yaml
python3 tools/rahp.py review --config examples/hello-rahp/rahp.yaml \
  --target hello-spec --mode rahp --offline --dry-run
python3 tools/rahp.py review --config examples/hello-rahp/rahp.yaml \
  --target hello-spec --mode rahp --offline
```

Check that the output is an `in-progress` *working scaffold*, not a substantive review verdict. Inspect the generated YAML's source commit, RAHP method release, empty findings and accompanying README. Repeat the last command **without** `--force`: overwrite must be refused and the existing artifact's SHA-256 must remain unchanged. Do not use `--force` to mask a failure.

Continue through the maintained TRQP real-specification example. Independently answer:

- What was reviewed, and which source commit and RAHP method version were used?
- Which controls/findings are supported by source evidence, and what runtime/deployment evidence is missing?
- Does schema validity alone establish authority or time freshness? Where does the example refuse that inference?
- Could a new user export/replay the result without a specialist or an agent?
- At which step, if any, did the guide require unstated prerequisites, context, or author assistance?

**Completion criterion:** an attributable attempt with commands, exit codes, output/artifact hashes and interpretation; unexpected failures or assistance are recorded, not silently corrected.

## Evidence record and interpretation

Submit one Markdown review report linked from #1159 and the relevant adoption tracking decision. It should contain:

| Field | Required evidence |
|---|---|
| Reviewer participation | Reviewer-controlled attribution, participation date, declared relationship to assessed work |
| RAHP source | Exact commit SHA and method version; source revisions for each historical artifact |
| Environment | OS/architecture, Python/tool versions, installation notes |
| Track A | Three per-packet dispositions, source citations, contrary interpretations and missing evidence |
| Track B | Commands, exit codes, generated SHA-256s, non-overwrite negative, source/method provenance, interpretation |
| Assistance/limitations | Any hints, synthetic inputs, skipped actions, missing dependencies, privacy/redaction decisions |
| Reviewer decision | What is reconstructable/useful and what should be corrected, retained provisional or rejected |
| Maintainer response | Finding-by-finding acceptance/rejection with rationale and follow-up links |

No report exists merely because this protocol exists. Until a real review is furnished, **independent research acceptance and independent adoption remain `NOT_YET_TESTED` / `PENDING`**.

## Proportionate adversarial review and follow-up

Challenge false success: a successful CLI exit without a review finding; a `dry-run` treated as implementation evidence; a nonempty source link treated as accurate historical content; a first-party self-review labelled independent; an omitted packet treated as `NOT_APPLICABLE`; a newer upstream fix retroactively clearing a historical finding; a human reader following author's hints rather than reconstructing the evidence.

On failure, prefer a **bounded correction of the existing evidence/navigation/CLI documentation**. A generic dashboard, new harm taxonomy, protection score, assessor API or new RAHP schema is not justified without independently demonstrated unmet needs. If the existing methods suffice, explicitly close the research-method question as `NO_EXTENSION_NEEDED` only after attributable judgment; retain meaningful unresolved real-world evidence obligations separately.

**Validation:** existing machine regression tests `tests.test_hello_rahp_offline_scaffold`, `tests.test_adoption_version_provenance` and `tests.test_reader_five_questions` should remain green in CI. These are distinct from external-review acceptance.

**Release:** commit-only documentation; no external compatibility change or release justified.
