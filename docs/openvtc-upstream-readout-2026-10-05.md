# Upstream read-out — OpenVTC post-migration RAHP

Campaign: RAHP #901  
Date: 2026-10-05

## Summary

The DTG credential migration is now substantially coherent across current DTG Credentials, VSC Registry, Trust Tasks, VTI and OpenVTC source pins. RAHP did **not** reproduce the earlier broad migration-convergence gap (#870); that owner is now closed.

The upstream action list should therefore stay small. The following items are the ones that warrant action or explicit disposition.

## 1. VTI: block approved-join credential redelivery for removed/historical members

**RAHP owner:** #898  
**Result:** FAIL / remediation required

### Proposition

Credential redelivery may recover lost delivery of an existing current grant, but must not make old membership/authority credentials re-deliverable after the member has departed or been removed.

### Current evidence

The current resend predicate checks approved request + member row + stored current credential bodies, but does not reject `removed_at != None` / `member.is_removed()`.

With Historical removal, the member row and credential-bearing fields remain, so the old credentials can be queued for delivery again.

### Upstream ask

Before redelivery:

1. require current/live member state;
2. ensure the stored credential bodies are the live grant associated with the current membership;
3. add a negative regression: approved request + Historical removed member + `resendCredentials=true` must not queue credentials;
4. preserve current non-enumerating requester binding and resend rate limits.

## 2. VTI: make signing-key replacement failure-atomic

**RAHP owner:** #899  
**Result:** FAIL / remediation required

### Proposition

Replacing an active signing key must be one coherent authority transition. A failed replacement must not silently destroy the existing usable key.

### Current evidence

The implementation serializes the replacement under a lock, but mutates state as:

`revoke old delegation → enrol new delegation`

If enrolment fails after revocation succeeds, the old key is not restored.

### Upstream ask

Implement an atomic/recoverable replacement transition and add failure-injection evidence covering:

- failure between old-key revocation and new-key storage;
- concurrent replacement/revoke;
- exact active-key set after success;
- old key retained or explicit recoverable state after failure;
- audit failure distinguished from whether the authority transition landed.

## 3. DTG/OpenVTC migration guidance: refresh Flow 9

**RAHP owner:** #901 (documentation/coherence item; no new defect owner needed yet)  
**Result:** current implementation PASS; supplied guidance is superseded

### Proposition

The migration guidance should describe the same identity-check evidence model current canonical sources implement.

### Current evidence

The supplied migration narrative describes Flow 9 as a plain W3C identity-verification VC outside DTG.

Current canonical sources have since converged on a different model:

- VSC Registry permits the community itself to issue `vetted/1`;
- current Trust Tasks defines community identity checks as `vetted/1`;
- current VTI issues/consumes the community's own `vetted/1` statement for personhood evidence.

### Upstream ask

Refresh or supersede the migration guidance so Flow 9 names the current community-issued `vetted/1` model and clearly marks the older plain-IDVC proposal as historical.

This is primarily a documentation/provenance correction, not a current runtime defect.

## 4. Live VAC/status freshness remains an explicit residual where required

**RAHP owner:** #609  
**Result:** known residual / evidence required

A valid signature, chain and validity window are not by themselves evidence of current non-revocation or current governing policy.

Where a consequential action relies on externally presented VAC/status/policy state rather than the community's own authoritative current record, keep the #609 requirement explicit: live revocation/status and any required policy lookup need bounded freshness and fail-closed/INDETERMINATE handling.

This should not be duplicated into a new migration issue.

## What does not need upstream action

The following migration concerns now have adequate current source evidence and should **not** be raised as unresolved upstream defects:

- VEC vetting statement → `vetted/1` VSC;
- `CommunityRole` endorsement → VAC role authority;
- `statementType` semantics in Trust Tasks;
- `eligibleVetters.role` mapping to exact VAC `role:<role>`;
- required `issuerScope` in DTG v1 credentials;
- old context / retired VEC/VWC rejection;
- fail-closed predicate accept-list behaviour;
- vetting card/session/task binding;
- generated Trust Tasks semantic convergence tracked by historical #870.

