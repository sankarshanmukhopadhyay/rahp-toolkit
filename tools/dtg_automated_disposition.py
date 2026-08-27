#!/usr/bin/env python3
"""Conservative automated disposition for RAHP DTG gatherer repository deltas.

This module does not infer arbitrary semantic findings. It recognizes only bounded
change patterns whose evidence is sufficient for an explicit per-lens disposition;
otherwise it returns UNCERTAIN and requires reviewer judgment.
"""
from __future__ import annotations

import json
import re
import urllib.request
from typing import Any

SPEC_RE = re.compile(r"(^|/)(spec|specs|schema|schemas)(/|\.|$)|(^|/)SPEC\.md$", re.I)
TEST_RE = re.compile(r"(^|/)(tests?|test_support)(/|\.|$)|(_test|_tests|\.test)\.", re.I)
SECURITY_RE = re.compile(
    r"\b(auth|authorization|authorisation|access|consent|session|revoke|revocation|"
    r"unauthori[sz]ed|stranger|disclos|leak|confidential|permission|privilege)\w*\b",
    re.I,
)
FIX_RE = re.compile(r"\b(fix|prevent|stop|reject|deny|harden|protect|idempotent)\w*\b", re.I)
WEAKEN_RE = re.compile(r"\b(disable|bypass|skip|relax|permit all|allow any|remove check)\b", re.I)
CORRELATION_RE = re.compile(
    r"\b(correlat|cross[- ]context|pairwise|stable identifier|durable identifier|"
    r"linkability|unlinkability|status handle|audience binding)\w*\b",
    re.I,
)
DISCLOSURE_RE = re.compile(r"\b(stranger|disclos|leak|session exists|confidential)\w*\b", re.I)


def fetch_compare(repository: str, base: str, head: str, token: str | None = None) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repository}/compare/{base}...{head}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "rahp-dtg-auto-disposition/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def _text(compare: dict[str, Any]) -> str:
    messages = [str(c.get("commit", {}).get("message", "")) for c in compare.get("commits", [])]
    patches = [str(f.get("patch", "")) for f in compare.get("files", [])]
    return "\n".join(messages + patches)


def _paths(compare: dict[str, Any]) -> list[str]:
    return [str(f.get("filename", "")) for f in compare.get("files", [])]


def _evidence(compare: dict[str, Any]) -> dict[str, Any]:
    paths = _paths(compare)
    text = _text(compare)
    security_paths = [p for p in paths if SECURITY_RE.search(p)]
    test_paths = [p for p in paths if TEST_RE.search(p)]
    spec_paths = [p for p in paths if SPEC_RE.search(p) and not TEST_RE.search(p)]
    return {
        "changed_files": paths,
        "spec_or_schema_paths": spec_paths,
        "test_paths": test_paths,
        "security_paths": security_paths,
        "security_signal": bool(SECURITY_RE.search(text) or security_paths),
        "fix_signal": bool(FIX_RE.search(text)),
        "weakening_signal": bool(WEAKEN_RE.search(text)),
        "correlation_signal": bool(CORRELATION_RE.search(text)),
        "disclosure_signal": bool(DISCLOSURE_RE.search(text)),
    }


def assess(compare: dict[str, Any]) -> dict[str, Any]:
    ev = _evidence(compare)

    # Semantic specification/schema changes are intentionally outside the first
    # auto-disposition rule set. Passing CI cannot prove their assurance meaning.
    if ev["spec_or_schema_paths"]:
        return {
            "terminal": False,
            "confidence": "bounded-uncertain",
            "risk": "uncertain",
            "harm": "uncertain",
            "security": "uncertain",
            "composition": "uncertain",
            "dpip": "uncertain",
            "reason": "specification or schema semantics changed; executable evidence does not prove assurance preservation",
            "evidence": ev,
        }

    # Bounded security-strengthening rule. Require an explicit security-sensitive
    # fix, changed regression tests, no weakening signal, and no composed privacy signal.
    if (
        ev["security_signal"]
        and ev["fix_signal"]
        and ev["test_paths"]
        and not ev["weakening_signal"]
        and not ev["correlation_signal"]
    ):
        harm = "mitigated" if ev["disclosure_signal"] else "unchanged"
        return {
            "terminal": True,
            "confidence": "high-bounded",
            "risk": "mitigated",
            "harm": harm,
            "security": "strengthened",
            "composition": "unchanged",
            "dpip": "not-required",
            "reason": "implementation-only security-sensitive fix with regression-test evidence and no weakening or composed-correlation signal",
            "evidence": ev,
        }

    return {
        "terminal": False,
        "confidence": "bounded-uncertain",
        "risk": "uncertain",
        "harm": "uncertain",
        "security": "uncertain",
        "composition": "uncertain",
        "dpip": "uncertain",
        "reason": "available deterministic evidence does not satisfy an auto-disposition rule",
        "evidence": ev,
    }


def render(result: dict[str, Any], repository: str, base: str, head: str) -> str:
    ev = result["evidence"]
    lines = [
        "<!-- rahp-dtg-auto-disposition:v1 -->",
        "## Automated evidence-backed assurance disposition",
        "",
        f"- Repository: `{repository}`",
        f"- Revision window: `{base}` → `{head}`",
        f"- Confidence: **{result['confidence']}**",
        f"- Risk: **{result['risk']}**",
        f"- Harm: **{result['harm']}**",
        f"- Security: **{result['security']}**",
        f"- Cross-spec composition: **{result['composition']}**",
        f"- DPIP applicability: **{result['dpip']}**",
        f"- Terminal without human judgment: **{'yes' if result['terminal'] else 'no'}**",
        "",
        "### Evidence sufficiency rationale",
        "",
        result["reason"],
        "",
        "### Evidence observed",
        "",
        f"- Specification/schema paths: {', '.join(f'`{p}`' for p in ev['spec_or_schema_paths']) or 'none'}",
        f"- Regression-test paths: {', '.join(f'`{p}`' for p in ev['test_paths']) or 'none'}",
        f"- Security-sensitive paths: {', '.join(f'`{p}`' for p in ev['security_paths']) or 'none'}",
        f"- Weakening signal: `{str(ev['weakening_signal']).lower()}`",
        f"- Composed-correlation signal: `{str(ev['correlation_signal']).lower()}`",
        "",
        "This is a bounded rule disposition, not a general claim that arbitrary code changes can be semantically assessed from keywords or CI success.",
    ]
    return "\n".join(lines) + "\n"


def self_test() -> int:
    spec = {"commits": [{"commit": {"message": "spec: change identifier scope"}}], "files": [
        {"filename": "SPEC.md", "patch": "+ identifierScope means ..."},
        {"filename": "specs/spec.meta.schema.json", "patch": "+ gate item"},
        {"filename": ".github/workflows/rust.yml", "patch": "+ check"},
    ]}
    r = assess(spec)
    assert not r["terminal"] and r["composition"] == "uncertain"

    security = {"commits": [{"commit": {"message": "fix(auth): stop revoke-session telling a stranger the session exists"}}], "files": [
        {"filename": "vta-service/src/trust_tasks/auth.rs", "patch": "+ reject unauthorized caller\n- reveal session"},
        {"filename": "vta-service/tests/revoke_session_trust_task.rs", "patch": "+ stranger_cannot_observe_session"},
    ]}
    r = assess(security)
    assert r["terminal"] and r["security"] == "strengthened" and r["harm"] == "mitigated" and r["dpip"] == "not-required"

    ambiguous = {"commits": [{"commit": {"message": "refactor handlers"}}], "files": [{"filename": "src/x.rs", "patch": "+ change"}]}
    assert not assess(ambiguous)["terminal"]
    print("PASS dtg_automated_disposition self-test")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_test())
