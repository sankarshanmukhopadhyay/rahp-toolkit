# Composed assurance walkthrough

This walkthrough explains when a RAHP adoption expands beyond the RAHP repository. It is a routing example, not a claim that every assessment needs these components.

## Scenario

Assume an adopter is assessing a composed trust flow and RAHP identifies three bounded propositions:

1. an authority/lifecycle proposition that RAHP can evaluate directly;
2. a composed privacy proposition that requires specialist examination; and
3. an implementation/composition proposition that requires executable evidence.

The resulting responsibility model is:

~~~text
assurance subject
  |
  v
RAHP controller
  |
  +-- proposition A: direct RAHP assessment
  |
  +-- proposition B: composed privacy question
  |      |
  |      +--> DPIP specialist examination
  |             |
  |             +--> rahp-assessor-result/v1
  |
  +-- proposition C: executable evidence obligation
         |
         +--> compatible evidence producer
                |
                +--> bounded evidence-producer result
                         |
                         v
                  RAHP reconciliation
                         |
                         v
             terminal assurance record
~~~

## Authority does not move with the message

Each repository keeps its own responsibility.

| Component | Owns | Does not own |
|---|---|---|
| RAHP | assessment identity/lifecycle, routing, reconciliation, residual/action and terminal assurance posture | DPIP privacy semantics or Lab implementation evidence |
| DPIP | bounded composed-privacy examination | overall RAHP terminal assurance |
| Interop Lab | bounded executable interoperability/implementation evidence for supported evidence surfaces | final RAHP or DPIP conclusions |
| Subject/upstream/deployer | its own normative, implementation or governance authority | RAHP assessment semantics merely because RAHP examines it |

A specialist PASS therefore remains an input to RAHP reconciliation. A successful Lab experiment remains evidence for the proposition it exercised. Neither silently becomes a system-wide PASS.

## Current stable portfolio boundary

This example is written against the current stable coordinated boundary:

- RAHP **v2.4.0**;
- DPIP **v0.2.0**;
- Trust Protocol Interop Lab **v0.6.0**.

Those versions are independently governed. Consumers should rely on the explicit machine contracts and source pins, not on coordinated release timing.

## Contract path

### 1. RAHP identifies a specialist question

RAHP scopes the subject and proposition, preserves immutable source identity, and routes a bounded specialist question when direct RAHP evidence is insufficient for the specialist semantic.

DPIP documentation:
- https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile
- https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile/blob/main/docs/understanding-dpip.md

### 2. The specialist returns a portable result

The portable RAHP specialist result is **rahp-assessor-result/v1**.

Authoritative RAHP schema:
- [schemas/rahp-assessor-result-v1.schema.json](../../schemas/rahp-assessor-result-v1.schema.json)

Contract guide:
- [Portable assessor-result contract](../../docs/assessor-result-contract.md)

DPIP return operations:
- https://github.com/sankarshanmukhopadhyay/dtg-privacy-implementation-profile/blob/main/docs/rahp-return-operations.md

### 3. RAHP identifies an executable evidence obligation

Where a proposition requires evidence that cannot be established by source/specification analysis alone, RAHP can express an evidence obligation using **rahp-assurance-obligation/v1**.

Authoritative schema:
- [schemas/rahp-assurance-obligation-v1.schema.json](../../schemas/rahp-assurance-obligation-v1.schema.json)

A compatible producer returns bounded evidence using the applicable evidence-producer contract:
- [schemas/rahp-evidence-producer-result-v1.schema.json](../../schemas/rahp-evidence-producer-result-v1.schema.json)

The Trust Protocol Interop Lab is a current evidence producer for supported implementation and composition surfaces:
- https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab
- https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/blob/main/docs/evidence-and-assurance.md

### 4. RAHP reconciles

RAHP evaluates the returned specialist result and executable evidence against the original proposition, required evidence class, source pins and boundedness.

Possible outcomes include PASS, FAIL, NOT_APPLICABLE and explicit INDETERMINATE/evidence-required states. Missing evidence is not converted into PASS.

## How an adopter decides whether to compose

Do **not** begin by installing every repository. Begin with the proposition.

Use DPIP when the unresolved question is a composed privacy property within DPIP's supported specialist boundary.

Use the Interop Lab when the unresolved proposition requires executable interoperability/implementation evidence and the Lab has a supported evidence surface capable of producing that evidence.

Use neither when RAHP can establish the bounded proposition with admissible evidence directly.

Use another compatible specialist or producer when the proposition falls outside DPIP or Lab responsibility.

## Next step

Return to the [Adoption gateway](../../docs/adoption-guide.md) for the decision matrix, or start with [Hello RAHP](../hello-rahp/README.md) if you have not yet exercised the RAHP-only path.
