# Security Policy

## Supported versions

Security fixes are applied to the current `main` branch and the latest supported release line identified by `PROJECT-STATUS.yaml` / release metadata. Older versions should be treated as unsupported unless a maintainer explicitly states otherwise.

## Reporting a vulnerability

Do not open a public issue for an undisclosed vulnerability. Use GitHub private vulnerability reporting when available, or contact the repository maintainer through a private channel identified on the maintainer profile.

Include affected versions/revisions, reproduction steps, impact, affected assurance evidence, and any known mitigation.

## Assurance implications

RAHP is an assurance method/toolkit, not a certification authority. A defect may invalidate risk, harm, privacy, security, composition, routing, or reconciliation evidence. Remediation must identify affected evidence and avoid silently converting missing/invalid evidence into PASS. DTG-specific consumers do not transfer their authority into RAHP core.
