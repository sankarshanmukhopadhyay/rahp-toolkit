# Planned Discussion updates for the evidence-closure phase

This file keeps the repository record synchronized with the public RAHP Discussion while the next three evidence-closure constructions are developed.

The public Discussion remains the umbrella research thread. These update headings are intentionally placeholders until each case has been source-pinned and assessed.

## Update 2 — Case A: routine bounded-authority act

Record:

- scenario and actors;
- governing authority proposition;
- required predicates;
- current Credential artifacts;
- current Trust Task artifacts;
- applicable lifecycle/status source;
- privacy/non-inference requirements;
- complete evidence closure;
- verifier decision;
- residual gap, if any;
- RAHP disposition:
  - Existing primitives sufficient
  - Profile / composition clarification required
  - Missing normative primitive demonstrated
  - Governance-only / outside cryptographic specification
  - Insufficient evidence

### Minimum adversarial checks

- appointment is valid but action is outside scope;
- authority expired immediately before the task;
- verifier treats representative evidence as proof of principal incapacity;
- status lookup leaks a durable relationship identifier;
- authoritative source cannot be authenticated.

## Update 3 — Case B: threshold / co-approval act

Record:

- transaction/action whose permissibility depends on a threshold;
- authoritative source for the threshold rule;
- current representative authority;
- transaction amount/class binding;
- required co-approval or quorum;
- task-context/freshness/non-replay binding;
- privacy-preserving proof inputs;
- complete evidence closure;
- verifier decision;
- residual gap, if any;
- RAHP disposition.

### Minimum adversarial checks

- one co-representative acts alone;
- old approval is replayed for a changed amount or beneficiary;
- authority changes after approval but before execution;
- proof of quorum leaks the full representative set;
- stable appointment IDs link otherwise private presentations;
- conflict checking reveals a sensitive relationship unnecessarily.

## Update 4 — Case C: suspension / restoration act

Record:

- initial representative authority state;
- suspension/supersession/restoration event;
- previously issued credentials and task evidence;
- current authoritative lifecycle source;
- precedence between principal and representative decision rights;
- transaction-time status check;
- complete evidence closure;
- verifier decision;
- residual gap, if any;
- RAHP disposition.

### Minimum adversarial checks

- stale representative evidence remains cryptographically valid;
- restoration does not propagate to the relying party;
- partially restored agency is flattened into a binary represented/not-represented state;
- emergency authority remains usable after the trigger ends;
- old approvals survive supersession;
- principal cannot challenge a technically valid representative action.

## Consolidated disposition update

After all three cases, add one final Discussion update containing:

1. findings confirmed, refined, weakened or contradicted by the constructions;
2. controls already supplied by current DTG work;
3. residual composition/profile gaps;
4. governance-only questions;
5. privacy and conformance implications;
6. exact proposed owner for each demonstrated residual gap;
7. whether each residual concern warrants:
   - no further action;
   - documentation/profile clarification;
   - an update to existing downstream work;
   - a new narrowly scoped downstream Discussion; or
   - a new implementation/specification Issue.

The consolidated update is the gate before downstream issue creation. No downstream issue should be opened solely because it appeared in the original hypothesis set.