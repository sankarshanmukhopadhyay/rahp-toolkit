# Release publication privilege separation — 2026-10-18

**Owner:** [#958](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/958). Scope is **current main**. Historical v2.7.0 tag, release evidence, qualification decisions and published notes remain unchanged.

Previous `.github/workflows/release.yml` granted `contents:write` to the entire single publication job, including dependency installation, TypeScript conformance, qualification and metadata inspection. As GitHub Actions tokens are job-scoped, this allowed preparatory steps to run with unnecessary publication authority.

This change uses two explicit jobs:

1. **`qualify` — `contents:read`:** checkout, dependency setup, TypeScript checks, declaration classification, branch and qualification gates, historical v2.7.0 evidence checks, and publication-notes preflight. It exposes only the intended qualification metadata and publish decision as workflow-job outputs.
2. **`publish` — `contents:write`:** runs only after qualification has succeeded and explicitly returned `publish=true`. It checks out the *same triggering commit*, recomputes the declaration metadata, reruns qualification and release-notes preflight, compares tag, version, title, notes path and target branch against the earlier qualified outputs, and only then creates/verifies the tag and reconciles the GitHub Release. The existing postflight verifies the published release and latest pointer.

This **reduces the privilege-bearing step surface** without changing who is authorized to publish. The publisher still has write authority for its remaining tag and release steps; review of actual GitHub/organization token restrictions, environment protections and private artifact/CI log retention remains required.

## Executable regressions

```bash
python3 -m unittest tests.test_release_privilege_segmentation -v
python3 tools/validate_workflow_governance.py
```

Negative/invariant tests assert only the publisher may request `contents:write`; the qualification job contains no `git push` or `gh release` mutation; and requalification plus metadata comparison occur *before* any publishing operation.

**Assurance limitations:** No actual production release was attempted as part of this assessment. A green workflow validation test checks structure, not live effective token permissions. Dependency locking with exact hashes and externally verified release-environment controls remain separate #958 requirements. This change must not be treated as satisfying human security review or a historical v2.7.0 certification.
