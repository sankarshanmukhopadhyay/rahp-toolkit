# Public repository baseline

This record captures the repository-owned controls reviewed under issue #363. It is repository assurance evidence, not external certification.

| Control | State | Evidence | Residual risk |
|---|---|---|---|
| Purpose, maturity, adoption and authority surfaces | PASS | `README.md`, `QUICKSTART.md`, `ADOPTION.md`, `PROJECT-STATUS.yaml`, `ROADMAP.md` | Fork-local results do not imply upstream adoption. |
| Licensing | PASS | repository license surface | None identified. |
| Security reporting and supported versions | PASS | `SECURITY.md` | GitHub private-vulnerability-reporting enablement remains hosted setting evidence. |
| Contribution/community/support guidance | PASS | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, issue and PR templates | None identified. |
| Dependency update management | PASS | `.github/dependabot.yml` | Hosted Dependabot enablement remains platform evidence. |
| Default-branch governance | PASS | active `protect-main` ruleset observed 2026-09-05: PRs, resolved conversations, linear history, deletion/non-fast-forward protection, strict required `validate`, `TypeScript conformance`, and `build` checks, no bypass actors | Required check names must remain aligned with actual CI over time. |
| CI / evidence discipline | PASS | repository workflows and required checks | Workflow green is execution evidence, not an assurance conclusion by itself. |
| Release/status provenance | PASS | `CHANGELOG.md`, `PROJECT-STATUS.yaml`, release workflow/docs | Release publication remains an explicit maintainer judgment. |
| Documentation integrity and adopter path | PASS | README/Quickstart/Adoption + Pages/docs workflows | None identified in this baseline pass. |
| Authority and assessment boundary | PASS | RAHP method/governance documentation | External assessed projects retain normative authority; missing evidence remains indeterminate, never PASS. |

## Completion boundary

The repository-owned public baseline is complete when the associated remediation PR is merged with the required ruleset checks green. Hosted security-feature enablement remains platform evidence and is not inferred from repository files.
