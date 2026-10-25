---
layout: default
title: "Three-spec composition provenance disposition"
parent: "Scenario corpora"
nav_exclude: true
---
# Credential Specification × ZKP × Trust Tasks: provenance disposition

**Tracker:** [#1142](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1142).

The three-spec corpus references the following independently selected upstream revisions:

| Dependency | Composition input revision | Standalone corpus baseline |
|---|---|---|
| Credential Specification | `b89f389abbdae77ba60b673c0836c781c2b54169` | Same revision |
| DTG ZKP | `3b6b3f2e76005d6f579d076ee2833ef56d599b65` | `archive-snapshot`, unverified |
| Trust Tasks | `6425a74136c1d2dfa7115889abe0b3521700e887` | `4937c70df95e56ed6404b8c004106ecb121a23cf` |

These revisions are declared inputs to this composition, **not** a claim that the current standalone parent adapters use identical baselines. The input pins are also not sufficient proof that the composition was independently reviewed. The previously declared `source-pinned` evidence grade has therefore been removed pending a source-span and composition-specific review. The corpus browser should display **Not declared**.

This disposition does not change scenario content, scenario identifiers, or portable assurance mappings. It does not re-baseline standalone corpora or qualify the three-spec composition for the frozen v1.6.0 corpus set. Before a future grade is assigned, record reviewed source spans, revision identities, adaptation reasoning, reviewer and composition-specific evidence. Divergent upstream input revisions are allowed when their provenance is explicitly explained; they are not automatically errors or grounds for grade inheritance.
