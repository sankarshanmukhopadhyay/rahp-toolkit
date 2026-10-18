---
layout: default
title: "Scenario corpora browser"
nav_order: 6
parent: "Scenario corpora"
has_toc: true
---
# Scenario corpora browser

All **15 packaged scenario adapters** are linked below (189 scenarios in total). **Browse** opens a human-readable projection; **YAML** opens the canonical source. An adapter supplies candidate pressure tests and is not evidence that its subject conforms or passes assurance.

## Source or portfolio adapters

| Corpus | Browse | Canonical YAML | Scenarios | Evidence grade |
|---|---|---|---:|---|
| DTG ZKP | [Browse](dtg-zkp/) | [YAML](dtg-zkp.yaml) | 30 | Not declared (archive snapshot) |
| Trust Tasks | [Browse](trust-tasks/) | [YAML](trust-tasks.yaml) | 30 | Not declared (source pinned) |
| DTG Credential Spec | [Browse](credential-spec/) | [YAML](credential-spec.yaml) | 30 | Not declared (source pinned) |
| CAWG/C2PA | [Browse](cawg/) | [YAML](cawg.yaml) | 36 | Not declared (multi-source snapshot) |
| VDS interface baseline | [Browse](vds/) | [YAML](vds.yaml) | 4 | scenario-baseline |
| Agent Names interface baseline | [Browse](agent-names/) | [YAML](agent-names.yaml) | 4 | scenario-baseline |

## RAHP-authored composed adapters

| Corpus | Browse | Canonical YAML | Scenarios | Evidence grade |
|---|---|---|---:|---|
| Trust Tasks × CredSpec | [Browse](trust-tasks-credspec-composed/) | [YAML](trust-tasks-credspec-composed.yaml) | 20 | Not declared (derived from pinned dependencies) |
| CredSpec × ZKP | [Browse](credential-spec-zkp-composed/) | [YAML](credential-spec-zkp-composed.yaml) | 4 | source-informed |
| CredSpec × VDS | [Browse](credential-spec-vds-composed/) | [YAML](credential-spec-vds-composed.yaml) | 4 | scenario-baseline |
| Trust Tasks × ZKP | [Browse](trust-tasks-zkp-composed/) | [YAML](trust-tasks-zkp-composed.yaml) | 4 | source-informed |
| Trust Tasks × VDS | [Browse](trust-tasks-vds-composed/) | [YAML](trust-tasks-vds-composed.yaml) | 4 | scenario-baseline |
| ZKP × VDS | [Browse](zkp-vds-composed/) | [YAML](zkp-vds-composed.yaml) | 4 | scenario-baseline |
| Agent Names × Trust Tasks | [Browse](agent-names-trust-tasks-composed/) | [YAML](agent-names-trust-tasks-composed.yaml) | 4 | scenario-baseline |
| Agent Names × CredSpec | [Browse](agent-names-credential-spec-composed/) | [YAML](agent-names-credential-spec-composed.yaml) | 4 | scenario-baseline |
| Credential Spec × ZKP × Trust Tasks | [Browse](credential-zkp-trust-tasks-composed/) | [YAML](credential-zkp-trust-tasks-composed.yaml) | 7 | source-pinned |

**Evidence grade:** `source-pinned` identifies source evidence at a declared pin; `source-informed` draws on source semantics without claiming a complete normative baseline; `scenario-baseline` denotes a pressure-test hypothesis rather than a verified normative guarantee. **Not declared** is used where the corpus YAML provides no `evidence_grade` field; the source-commit description in parentheses is provenance context, not an inferred grade. Read the individual source and pin before making a stronger claim.

## How to read a corpus

Each scenario row gives an identifier, a domain or context, a `primary_goal`, a `primary_pressure` that could undermine that goal, and a priority (`P0` is a high-priority pressure probe; `P1` a secondary one). `source_anchor` may identify the specific source passage. `scenario_patterns` links the scenario to reusable `SP-*` pressure patterns in the [scenario patterns catalogue](../method/scenario-patterns/). Check the source revision and evidence grade; a scenario is a question to test, **not** a recorded runtime failure.

Human projections use clean directory routes such as `/corpora/vds/`; sibling `.yaml` files remain machine-readable and must not be replaced by HTML. For adaptation rules and scenario semantics, see [Scenario corpora](../docs/scenario-corpora.md); for drift, source pins and review workflows, see [Corpus synchronization and provenance](../docs/corpus-synchronization.md).
