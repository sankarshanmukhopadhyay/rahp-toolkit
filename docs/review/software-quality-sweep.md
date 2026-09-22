# Independent-review software-quality sweep

## Scope and method

This sweep is intentionally evidence-driven rather than metric-driven. It covers the stable validation path, unit tests, exception-sensitive reviewer entry points, nondeterminism and dependency boundaries, public compatibility metadata, documentation synchronization and generated-view drift.

## Evidence

The repository's required validation workflow executes the core artefact validator, portable catalogue and method invariants, lineage and remediation checks, assurance graph, freshness delta, authority/policy gates, release declarations, maintained examples, pressure tests, project/release/documentation checks, negative fixtures, review-readiness contracts, Python unit tests, specialist reconciliation, DTG/VTI checks, cross-spec registries, assessment queue, stable engine contract, generated views and reference links.

The independent-review tranche adds a clean-runner reproduction workflow and hostile-input regression tests. PR #757 established the reviewer contracts and passed the main validation, workflow-governance, benchmark and documentation workflows before merge.

## Findings

1. **Reviewer promotion path validation:** a concrete path-boundary defect was found and remediated; see 'security-pre-review.md'.
2. **Dependency determinism:** Python dependencies are lower-bounded, not locked. This is documented as a reproducibility limitation rather than silently described as deterministic.
3. **Warnings/skips:** the principal validator explicitly distinguishes warnings from errors unless '--strict' is used. Independent review should inspect warnings rather than treating exit code zero as semantic clearance.
4. **Generated state:** CI fails when committed 'build/' output differs after regeneration, reducing unnoticed generated-view drift.
5. **Public compatibility boundary:** review-readiness validation cross-checks the stable release, engine revision and normalized result schema against 'method/versioning.yaml'.

## Not claimed

This sweep does not claim formal verification, exhaustive dead-code detection, full static typing, fuzzing completeness, bit-reproducible dependencies, performance qualification, or comprehensive denial-of-service resistance. No refactoring is justified solely to improve a quality metric.
