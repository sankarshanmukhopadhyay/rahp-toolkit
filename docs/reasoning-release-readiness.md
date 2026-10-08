---
layout: default
title: "Release readiness — R1–R3"
parent: Learn RAHP
nav_order: 12
has_toc: true
permalink: /docs/reasoning-release-readiness/
---
# R1–R3 release-readiness decision record

**Status: CANDIDATE — NOT YET APPROVED FOR A NEW RELEASE.** This is a bounded decision record, not a release announcement. Tracking: [#939](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/939).

## Baseline and scope

The latest published stable release at the time of this review (2026-10-08) is **v2.6.0**. R1 evidence adequacy, R2 temporal provenance, R3 reproducibility/challenge and the combined worked example were merged after that release. These additions are **optional experimental profiles**. No change to the stable assessor-result v1, assurance FSM, or terminal controller is claimed.

## Gate register

| Gate | Evidence / present finding | Disposition |
| --- | --- | --- |
| Source merged | R1 PR #932, R2 PR #934, R3 PR #936, example PR #938 | SATISFIED |
| Post-merge CI | R1, R2, R3 and example post-merge validation runs succeeded | SATISFIED |
| Pages build | Corresponding deployment workflows succeeded | SATISFIED |
| Documentation render | R1–R3 pages owner-confirmed; combined worked example requires explicit rendered-page check | PENDING |
| Independent consumer execution | Participant, fresh fixtures, uncoached transcript and assessment are not yet available | NOT_YET_TESTED |
| Stable compatibility | Optional APIs deliberately avoid stable controller contracts; release-candidate regression run still needed | PARTIAL |
| Version and change scope | Decide patch/minor version and explicitly label experimental surfaces after diff audit | PENDING |
| Release hygiene | Verify release workflow, tags, changelog, version strings, docs links, packaging and published artifact content | PENDING |
| Security and evidence | Confirm no private fixtures, tokens or false provenance claims in release | PENDING |

## Recommended release decision

**Do not publish a new release solely because the R1–R3 example merged.** The merged work can remain on `main` while adoption evidence is collected. A release is warranted when a clear user-facing capability boundary, validated distribution contents, release notes and green candidate checks exist.

The independent participant exercise is a **research/adoption gate**, not automatically a hard blocker for shipping explicitly experimental features. If the maintainer elects to release before independent adoption evidence, the release notes must say **NOT_YET_INDEPENDENTLY_VALIDATED** and must not claim consumer interoperability, specification conformance, or assurance certification.

## Candidate preparation checklist

- [ ] Confirm rendered worked-example and adoption-kit pages.
- [ ] Run a fresh release-candidate validation on pinned `main` SHA, including all R1–R3 tests and the worked-example tests.
- [ ] Compare release `v2.6.0` with candidate SHA; classify **all** intervening changes, not only R1–R3.
- [ ] Confirm version policy and release naming; do not infer version number from this record.
- [ ] Audit links, changelog, published docs navigation, distribution inclusion and release workflow.
- [ ] Review security/privacy and evidence-claim wording.
- [ ] Publish an evidence-linked release recommendation (GO / CONDITIONAL_GO / NO_GO) with explicit scope and residuals.
- [ ] If GO, prepare release notes and create a release only after approval.

## Decision ownership

Maintainer/release authority: repository owner. This document provides evidence and recommendations; it does not delegate release authority to an automated evaluator. Closing #939 requires actual independent participant evidence, regardless of whether a release proceeds.
