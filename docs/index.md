---
layout: default
title: RAHP Toolkit
nav_order: 1
has_toc: true
---
# RAHP Toolkit documentation

RAHP Toolkit is a **portable specification-assurance toolkit**. It provides a method, configuration contract, review tooling, scenario patterns, validation and evidence rendering for pressure-testing standards and technical specifications against risks, harms and adversarial failure conditions.

The repository contains deployments and examples, but **RAHP is not the DTG deployment and it is not the CAWG/C2PA deployment**. DTG is the historical origin and a bundled exemplar; CAWG/C2PA is the first substantial external deployment proving that the same method and engine can operate with independent scope, risks, state and governance.

## Choose your path

The documentation is organized by task rather than by file type:

| I want to… | Go to |
|---|---|
| Understand what a scenario means for people who rely on a system | [Reading a scenario corpus](reading-scenario-corpus.md) |
| Understand the method and portable assurance catalogue | [Learn RAHP](learn.md) |
| Configure RAHP for my project | [Adopt RAHP](adopt.md) |
| Run or interpret an assessment | [Run assessments](assess.md) |
| Operate monitoring, evidence and disposition | [Operate assurance](operate.md) |
| Build or integrate an engine | [Implement RAHP](implement.md) |
| Inspect DTG, CAWG/C2PA or A2A | [Deployments & examples](deployments.md) |
| Find diagrams, registers and project history | [Reference](reference.md) |
| See release history | [Releases](releases/index.md) |

The portable method is independent of the bundled deployments. Deployment pages are evidence that the same contract works in different governance contexts; they are not prerequisites for adoption.

## Historical material

The [Historical Library](../archive/) retains earlier personas, requirements, registers, spreadsheets and generated views. It is provenance, not the portable RAHP method and not current deployment state.

- [Personas and actor roles](personas.md)


## Implementations

RAHP v1.0 ships Python and TypeScript reference implementations against the stable [v1 engine contract](engine-contract.md). See [Implementation conformance](conformance.md) for the compatibility promise and differential test boundary.
