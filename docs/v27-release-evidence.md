# v2.7.0 release evidence contract

**State: NO-GO until all seven gates are evidenced and owner approval is explicit.**

The non-publishing candidate manifest is [v2.7-release-candidate.yaml](../method/v2.7-release-candidate.yaml). Its `PENDING` entries are intentional and must not be overwritten with optimistic claims. This document defines an independently inspectable decision record; it does not authorize a GitHub Release.

## Candidate verification

1. Pin the exact 40-character candidate commit SHA after the synchronized version PR has merged.
2. Run full Python validation, TypeScript conformance, stable-contract compatibility, Pages build, publication-metadata checks, and security/privacy review on **that exact SHA**. A successful workflow on an earlier commit is insufficient.
3. Record each gate's result, SHA and evidence URL in a JSON file based on the template below. Link the complete record and relevant artifacts in [#941](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/941).
4. Obtain a distinct maintainer GO decision after inspecting evidence and residuals. Independent adoption remains `NOT_YET_TESTED` unless separately evidenced; optional R1–R3 outputs do not imply terminal assurance.
5. Run `python3 tools/validate_v27_release_evidence.py <record.json>`. This checks **structure and declared links**, not GitHub run provenance or authenticity. A human must inspect each linked run, artifact and commit SHA.
6. Publication remains manual through the guarded workflow. Do not dispatch it without explicit owner authorization.

## JSON record template

Replace the placeholder SHA, URLs and results **only after evidence exists**. The following is deliberately a failing NO-GO record:

```json
{
  "contract": "rahp-release-evidence/v1",
  "candidate_version": "v2.7.0",
  "candidate_sha": null,
  "publication_authorized": false,
  "gates": {
    "full_regression": {"result": "PENDING", "candidate_sha": null, "source": null},
    "typescript_conformance": {"result": "PENDING", "candidate_sha": null, "source": null},
    "stable_compatibility": {"result": "PENDING", "candidate_sha": null, "source": null},
    "docs_rendering": {"result": "PENDING", "candidate_sha": null, "source": null},
    "publication_metadata": {"result": "PENDING", "candidate_sha": null, "source": null},
    "security_review": {"result": "PENDING", "candidate_sha": null, "source": null},
    "owner_approval": {"result": "PENDING", "candidate_sha": null, "source": null, "decision": "PENDING"}
  }
}
```

## Release metadata sequencing

The v2.6.0 historical qualification remains preserved. Synchronize `method/release.yaml`, `PROJECT-STATUS.yaml`, `method/versioning.yaml`, package and lock versions, portable fixture, README, ROADMAP, CHANGELOG, versioned release notes, qualification validator and butterfly history in one separately reviewed change. The publication workflow is now manual-only; **metadata merge is not publication authorization**.

The candidate codename must be selected using the repository's pinned unused-butterfly pool and persisted with verified scientific name and selection date. Do not invent or reuse a codename. A release tag is created only after qualification and owner GO.

## Evidence limitations

This contract validates presence and internal SHA agreement in submitted declarations. It cannot independently verify that a GitHub URL identifies a successful workflow, that artifacts match the declared SHA, that a security review was substantive, or that the owner truly approved. Those remain mandatory manual verification tasks, not automatic PASS.
