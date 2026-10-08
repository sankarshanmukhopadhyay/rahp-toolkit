# RAHP release operator guide

## One qualifying merge, one publication

The release workflow publishes a declared, **already-qualified** release automatically when qualifying release metadata is merged to protected `main`. The operator does not need to dispatch a second workflow, create a tag, or manually edit a GitHub Release.

1. Prepare a release metadata PR with the next version, codename, release notes and the prescribed qualification/evidence contract. Review the release scope and assurance limitations.
2. Ensure the PR checks pass and that the declared `release.status` is `released` and `qualification_status` is `qualified`. The release workflow *revalidates* these states; merging an unqualified candidate does not publish it.
3. Merge the PR into `main`. The release workflow starts on relevant release metadata changes, requalifies, checks evidence, creates or preserves the annotated tag, reconciles the GitHub Release notes, checks the Latest designation and posts an outcome summary.
4. Open the release workflow run and check the final publication verification step. A successful job means its release metadata, published body, draft/prerelease states and Latest pointer were checked.

**Manual recovery:** The same `Publish qualified RAHP release` workflow can be run from `main`, specifying the exact declared tag and `PUBLISH`. This path is for retrying partial operations and correcting published metadata, not an ordinary additional approval hop. Reruns preserve an existing compatible tag.

## Assurance and failure handling

- The validated main-branch merge authorizes release evaluation; publication still requires the declared qualified state, version synchronization and release-specific evidence checks.
- Do not publish notes containing candidate/unqualified/pending language. The preflight check blocks tag creation in that case.
- The postflight check fails if the published release differs from the canonical title/notes, is a draft or prerelease, or is not the Latest release.
- Workflow executions are serialized to avoid concurrent tag/release operations.
- An Actions failure may occur after tag creation or release creation. Inspect the named failure, correct the source declaration or notes by PR, and rely on the idempotent automatic push path or manual retry. Do not force-move an existing tag.
- Qualification evidence and residual limitations remain governed by each release's manifest; independent testing must not be inferred solely from workflow success.

## Local checks

```sh
python3 -m unittest tests.test_release_publication
python3 tools/verify_published_release.py preflight docs/releases/v2.7.0.md
python3 tools/validate_workflow_governance.py
```

The release runner additionally executes full qualification and TypeScript conformance before publishing.
