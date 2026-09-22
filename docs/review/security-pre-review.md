# RAHP hostile-input security pre-review

Status: pre-review evidence for independent-review readiness. This is not a claim that RAHP is secure against every hostile input.

## Scope

The review considered the reviewer-facing CLI, YAML/JSON parsing surfaces, subprocess invocation, file/path handling, CI execution, dependency resolution and resource-bound assumptions. The review target is the stable v2.4.0 / engine-contract revision 1.3 boundary, plus the review-readiness changes made after that release.

## Findings and disposition

### SRR-001 — promotion slug could escape the intended review path

**Materiality:** high for a local reviewer invoking promotion on untrusted instructions or input.

'review.py init' validated review slugs, but 'review.py promote' previously accepted its slug without applying the same grammar. Because the slug participates in source and destination paths, path components such as '../' could escape the intended '.rahp/reviews/<slug>' namespace. Promotion still required a matching source layout and local filesystem access, so this was not a remote-code-execution path; nevertheless the path boundary was weaker than the initialization boundary.

**Disposition:** remediated. Promotion now applies the same 'slug_ok' predicate as initialization before constructing paths. Regression tests reject traversal and absolute-like slugs.

**Evidence:** 'tools/review.py'; 'tests/test_review_cli_security.py'.

## Observed defensive properties

YAML read paths inspected in the principal review and validation entry points use 'yaml.safe_load'. Review subprocess orchestration constructs an argument vector and invokes 'subprocess.run' without a shell. The review CLI requires a full 40-character commit SHA at initialization. CI uses an isolated hosted runner and invokes repository scripts as explicit commands.

These observations are bounded to the inspected surfaces; they are not a repository-wide proof that unsafe parsing or process invocation can never be introduced.

## Residual risks and limits

Dependency versions in 'requirements.txt' are lower-bounded rather than cryptographically locked, so clean reproduction is not bit-for-bit dependency reproduction. Several validators intentionally load repository-controlled structured data without general resource quotas; comprehensive denial-of-service qualification for adversarially huge inputs has not been established. Source availability and authenticity outside the repository remain governed by provenance/source-pin rules rather than by this pre-review. GitHub Actions and third-party actions are supply-chain dependencies; workflow pinning and platform controls should be reviewed independently by a third party.

No unresolved finding discovered in this bounded pre-review currently justifies a positive security assurance claim. Absence of another finding is not evidence of absence.
