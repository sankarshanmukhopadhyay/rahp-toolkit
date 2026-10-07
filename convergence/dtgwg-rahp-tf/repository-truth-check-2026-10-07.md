# Upstream repository truth-check and convergence disposition

Inspected upstream main: `e3ad6648ebc8c1a9a625dbdbefc8ba68b5bbd1e0`.
Prepared 7 October 2026. This is downstream evidence and contributor judgment, not an upstream architectural decision.

## Contribution reconciliation

| Upstream item | Current disposition | Remaining obligation |
|---|---|---|
| #10 reproducible specification-review records | Accepted at `8145351005fd6286f6c34536edc6ebfa2e2ad3fb` | Preserve upstream authority and source-pinned evidence |
| #11 bounded adoption guide | Accepted at `e3ad6648ebc8c1a9a625dbdbefc8ba68b5bbd1e0` | Check actual newcomer reproduction |
| #12 reader-facing model | Submitted; refreshed head `ffa2815241917957eda8cd8fabfa8bdc6dc772e8` | Upstream maintainer review/decision; not accepted |
| #13 current-layout reproduction repair | Submitted head `0b60baef0c46a353938747493d4571fcacf538ff` | Upstream maintainer review/decision; not accepted |
| #9 guided architecture umbrella | Partially addressed | Active validation, publication/adoption evidence and layout judgment remain |

## Inventory method and limits

`repository-inventory-2026-10-07.csv` contains one row per tracked file at the inspected main revision and all fields required by the convergence plan: current/possible target paths, role, authority/output classification, consumers, workflow/documentation/runtime/site references, migration risk and required validation.

References were identified by a static scan of UTF-8 tracked source for file paths/names, plus explicit instance-driven runtime consumers. Historical binary artifacts were classified by role, not inspected for embedded links. Dynamic dependencies and external consumers cannot be proven complete by filename scanning. Proposed target paths are planning hypotheses, not approved moves. This inventory is complete for tracked paths; a migration map is **not cleared** until runtime, hosting and external consumers are reconciled.

The canonical record set is derived from `instance.yaml`. The root `rahp.jsonld` is a canonical context; the other root record JSON-LD/HTML/JSON artifacts are retained outputs whose equivalence to a fresh build has not been established. Existing published URLs must not be moved based on a directory preference.

## Reproduced gaps

1. `python3 tools/validate.py --summary` fails: `tools/validate.py` does not exist.
2. `python3 validate.py --summary` fails: root resolution points outside the repository and expects absent `data/` and `method/` directories.
3. `build.py` has the same root/layout assumptions. Its generated JSON-LD references `../../context/rahp.jsonld`, although that context directory is absent.
4. Root `validate.yml` is outside `.github/workflows/`; no active workflow exists at the pinned baseline. DCO and EasyCLA do not execute the corpus validator or build.
5. README and CONTRIBUTING present the proposed directory layout as implemented. Historical migration helpers retain corresponding assumptions and need separate evidence before reuse.

The 11 original specification-review tests pass; that evidence does not establish the broader validation/build workflow.

## Bounded repair evidence

#13 corrects the two current commands and contributor documentation without moving canonical files or changing schema/vocabulary/corpus meaning. The output bundle includes its own copy of the canonical JSON-LD context, with a resolvable relative reference.

Local candidate validation: zero errors, 32 retained warnings. Build: six site pages, twelve record JSON-LD files, JSON/Markdown exports and context. All 14 tests pass, including CLI execution from a different working directory, relocated output context resolution and rejection of an invalid reference in an alternate record directory. Whitespace validation passes. Existing published outputs are untouched. No strict warning-free, live Pages, active CI or independent-human-review claim is made.

## Next contribution order

1. **Active validation and reproduction evidence.** After #13 is accepted or settled, propose a small real GitHub Actions workflow for the existing commands, review regressions and temporary-output build; upload bounded evidence. Retain warnings and avoid release/deployment privileges. Resolve the inactive template explicitly rather than maintaining two competing workflow contracts.
2. **Worked adoption and interpretation.** Following #12/#13 decisions, use the existing minimal review to demonstrate scope, persona/context, source pin, risks, evidence, control plane, disposition and reassessment trigger. Preserve the distinction between schema validity and assurance. Avoid new record types or importing a full downstream example.
3. **Guided generated-site navigation.** Once a maintainer agrees the publication source/destination, add Understand / Apply / Explore navigation with existing generated views as drill-down destinations. First establish output equivalence, hosting paths and link checks.
4. **Structural decision.** Reconcile maintainer reaction, newcomer evidence and the inventory. Choose retain-flat, bounded moves or a full tested migration based on benefits and compatibility. No automatic folder migration or archive relocation is authorized by this report.

Independent-review readiness remains a later candidate contingent on maintainer appetite. Controller orchestration, specialist routing, portfolio composition, major lineage machinery and releases remain outside this contribution cycle.

The isolated convergence ledger branch remains the durable provenance surface and is not merged into downstream main. Upstream PRs remain open for maintainer acceptance; auto-merge and contributor self-merge are excluded.

## Active validation contribution execution — 7 October 2026

Upstream #14 is a draft based on #13's reproduction branch. Head `c7022ab41e4dbf4c17cdafb47e1d5884a76760ff` passed [run 37563226549](https://github.com/trustoverip/dtgwg-rahp-tf/actions/runs/37563226549): all 14 tests, corpus/review checks, temporary-output build, generated-file digest manifest and upload. DCO and EasyCLA pass. Artifact `11457635529` has digest `sha256:ab0b43e3f1b47e7866131721a4579d42996bf9cab5c56d9ceffd49a20d13cf8d` with 14-day retention; this record preserves identity, not a permanent artifact copy.

The first workflow definition failed before scheduling a job because a runner context was referenced at job environment scope. The corrected head initializes temporary paths inside a runner step. The failure remains in execution history and does not count as validation evidence.

Acceptance remains pending. After #13 is accepted, retarget #14 to then-current main, reconcile its diff/checks and remove the temporary dependency wording before marking ready. Do not merge into the dependency branch. Canonical records and published root outputs remain unchanged; warnings are retained. The worked-adoption and site contributions remain subsequent work after these decisions.

## Worked adoption contribution — 7 October 2026

Upstream #15 is independently based on accepted main `e3ad6648ebc8c1a9a625dbdbefc8ba68b5bbd1e0`, using #10's existing review contract and #11's adoption guide. It does not require the pending implementation in #12/#13/#14. Head `9c775abc431be6a51326de2b049dd264bbe54381` is review-ready and conflict-free; DCO and EasyCLA pass. Two real source commits freeze fictional target versions before the authored review records.

Both new records pass the existing review CLI and all 12 tests on this branch pass locally. Governance documentary coverage moves from open to resolved, while the separate renewal finding remains open; the original review is preserved. No actual governance enactment, independent participation, deployment effectiveness, harm remedy or whole-target assurance is inferred. The guide separately pins the corpus because the existing schema records only a method label. Schema validity does not prove source existence or correct judgment.

Acceptance remains with upstream maintainers. The source-pinned packet can be inspected at [review/examples/worked-adoption/README.md](https://github.com/trustoverip/dtgwg-rahp-tf/blob/9c775abc431be6a51326de2b049dd264bbe54381/review/examples/worked-adoption/README.md). The next candidate is generated-site navigation after publication source/destination agreement; no directory moves, deployment or archive relocation are authorized.
