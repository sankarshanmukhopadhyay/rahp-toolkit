---
layout: default
title: "Release-candidate qualification execution"
parent: Learn RAHP
nav_order: 14
has_toc: true
permalink: /docs/release-candidate-qualification/
---
# Release-candidate qualification execution

Tracking: [#941](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941). This page is a **prepublication procedure**, not a release qualification certificate.

## Pinned baseline

The initial post-v2.6.0 decision record merged at `039dedfa2131fc612fbd2b5dc00c71ad14269fbc` (19 commits and 82 files compared with v2.6.0). The **actual release candidate SHA must be pinned again** after all release-preparation changes; do not treat that prior SHA as the release candidate.

## Candidate execution

From a clean checkout of the intended candidate commit:

```bash
git status --short
git rev-parse HEAD
git diff --stat v2.6.0...HEAD
python3 --version
python3 -m pip install -r requirements.txt
python3 tools/release.py verify
python3 tools/release.py qualify
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m unittest tests.test_evidence_adequacy tests.test_temporal_provenance tests.test_reproducibility_challenge tests.test_reasoning_trace tests.test_reasoning_worked_example tests.test_sociotechnical_assurance tests.test_standalone_trqp -v
python3 -m tools.reasoning_worked_example --scenario baseline
python3 -m tools.reasoning_worked_example --scenario missing
python3 -m tools.reasoning_worked_example --scenario retroactive
python3 -m tools.reasoning_worked_example --scenario disagreement
python3 tools/validate_typescript_sdk.py
```

**Note:** The current release declaration is still v2.6.0. The two `tools/release.py` checks above validate the *existing* release state until a new qualification declaration is committed. They are **not** proof of qualification of the future candidate. Use CI logs, pinned SHA, exit codes and artifact digests as the evidence record.

## Mandatory workflow evidence

- Main validation: full Python test discovery and qualification checks.
- TypeScript conformance: verify it ran on the candidate, not merely skipped by change-impact classification.
- Documentation build and deployed HTML routes: inspect `/docs/reasoning-worked-example/`, `/docs/reasoning-adoption-exercise/`, `/docs/reasoning-adoption-record/`, `/docs/reasoning-release-readiness/`, and `/docs/post-v26-release-assessment/`.
- Confirm absence of broken local links and unintended exposure of credentials, sensitive fixtures or personal data.
- Confirm stable contracts, published artifacts and version alignment.

## Release-engineering coupling to resolve

The existing `tools/validate_v26_release.py` explicitly pins v2.6.0, Commander, current theme and portable fixture version. A new release **must not** simply change `method/release.yaml`: it needs a new qualification manifest and validator, synchronized `PROJECT-STATUS.yaml`, `method/versioning.yaml`, root/workspace packages and lockfile where applicable, portable fixture version, README, changelog and release notes. Preserve the v2.6 historical validator's ability to verify its historical artifacts without requiring current metadata to remain v2.6 forever; otherwise the main validation workflow will fail after version bump.

The existing publisher is declaration-driven and creates/verifies tags. It must not be triggered for a candidate until all metadata and qualification checks agree. Use the governed pinned codename pool and history; do not invent a codename.

## Explicit publication authorization

The publication workflow is **manual-only**. A metadata push to `main` must not create a tag, create a GitHub Release, or change which release is marked latest. Following a separately evidenced maintainer GO decision, dispatch `.github/workflows/release.yml` on the qualified `main` commit with `release_tag` equal to the declared tag and `confirm_publication` equal to `PUBLISH`. The workflow checks both inputs, `released` status, `qualified` qualification status, and reruns release qualification before any tag operation. Dispatching is an explicit publication action; merely merging qualification metadata is not.

## Decision record template

| Gate | Pinned evidence URL / SHA | Result | Reviewer |
| --- | --- | --- | --- |
| Full regression | PENDING | PENDING | PENDING |
| Python–TypeScript conformance | PENDING | PENDING | PENDING |
| Stable contract compatibility | PENDING | PENDING | PENDING |
| Docs and HTML rendering | PENDING | PENDING | PENDING |
| Version/qualification consistency | PENDING | PENDING | PENDING |
| Codename history | PENDING | PENDING | PENDING |
| Security and publication artifact review | PENDING | PENDING | PENDING |

**Decision: NO_GO for publication until mandatory gates pass.** The independent adoption study remains NOT_YET_TESTED; that limitation may be disclosed for experimental profiles but cannot be represented as completed testing.

See [draft candidate release notes](release-candidate-post-v2.6-draft.md).
