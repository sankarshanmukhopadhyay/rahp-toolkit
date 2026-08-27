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
FIX_RE = re.compile(r"\b(fix|prevent|stop|reject|deny|harden|protect|idempotent|indistinguish)\w*\b", re.I)
STRENGTHEN_RE = re.compile(
    r"\b(prevent|stop|reject|deny|harden|protect|indistinguish|non[- ]disclos|"
    r"must not reveal|cannot reveal|must not disclose|cannot disclose|unlinkab|pairwise)\w*\b",
    re.I,
)
WEAKEN_RE = re.compile(
    r"\b("
    r"introduc(?:e|es|ed|ing).{0,48}(?:unauthori[sz]ed|disclos|leak)|"
    r"(?:allow|permit).{0,36}(?:unauthori[sz]ed|stranger|untrusted)|"
    r"bypass(?:es|ed|ing)?.{0,36}(?:auth|consent|check|validation)|"
    r"disable(?:s|d|ing)?.{0,36}(?:auth|consent|check|validation)|"
    r"remove(?:s|d|ing)?.{0,36}(?:auth|consent|check|validation)|"
    r"relax(?:es|ed|ing)?.{0,36}(?:auth|consent|check|validation)|"
    r"skip(?:s|ped|ping)?.{0,36}(?:auth|consent|validation)"
    r")\b",
    re.I | re.S,
)
CORRELATION_RE = re.compile(
    r"\b("
    r"introduc(?:e|es|ed|ing).{0,60}(?:correlat|linkab|stable identifier|durable identifier)|"
    r"(?:reuse|share|same).{0,48}(?:identifier|handle).{0,48}(?:across|cross[- ]context|cross[- ]party)|"
    r"(?:correlat|linkab).{0,60}(?:across contexts?|cross[- ]context|across parties|cross[- ]party|durable|stable identifier)|"
    r"(?:stable|durable) identifier.{0,48}(?:across contexts?|cross[- ]context|across parties|cross[- ]party)"
    r")\b",
    re.I | re.S,
)
CORRELATION_PREVENT_RE = re.compile(
    r"\b("
    r"(?:prevent|avoid|prohibit|reject|stop).{0,60}(?:correlat|linkab)|"
    r"(?:unlinkab|pairwise).{0,60}(?:identifier|handle|presentation|subject)|"
    r"must not correlate|cannot correlate|non[- ]correlat"
    r")\b",
    re.I | re.S,
)
DISCLOSURE_RE = re.compile(r"\b(stranger|disclos|leak|session exists|confidential)\w*\b", re.I)


def fetch_compare(repository: str, base: str, head: str, token: str | None = None) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repository}/compare/{base}...{head}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "rahp-dtg-auto-disposition/1.1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def _paths(compare: dict[str, Any]) -> list[str]:
    return [str(f.get("filename", "")) for f in compare.get("files", [])]


def _commit_text(compare: dict[str, Any]) -> str:
    return "\n".join(str(c.get("commit", {}).get("message", "")) for c in compare.get("commits", []))


def _added_patch_text(compare: dict[str, Any]) -> str:
    lines: list[str] = []
    for f in compare.get("files", []):
        for line in str(f.get("patch", "")).splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                lines.append(line[1:])
    return "\n".join(lines)


def _evidence(compare: dict[str, Any]) -> dict[str, Any]:
    paths = _paths(compare)
    commit_text = _commit_text(compare)
    added_text = _added_patch_text(compare)
    directional_text = "\n".join((commit_text, added_text))
    all_text = "\n".join(
        [commit_text] + [str(f.get("patch", "")) for f in compare.get("files", [])]
    )
    security_paths = [p for p in paths if SECURITY_RE.search(p)]
    test_paths = [p for p in paths if TEST_RE.search(p)]
    spec_paths = [p for p in paths if SPEC_RE.search(p) and not TEST_RE.search(p)]
    non_test_paths = [p for p in paths if not TEST_RE.search(p)]
    weakening = bool(WEAKEN_RE.search(directional_text))
    correlation = bool(CORRELATION_RE.search(directional_text))
    strengthening = bool(STRENGTHEN_RE.search(directional_text))
    correlation_prevention = bool(CORRELATION_PREVENT_RE.search(directional_text))
    return {
        "changed_files": paths,
        "spec_or_schema_paths": spec_paths,
        "test_paths": test_paths,
        "non_test_paths": non_test_paths,
        "security_paths": security_paths,
        "security_signal": bool(SECURITY_RE.search(all_text) or security_paths),
        "fix_signal": bool(FIX_RE.search(directional_text)),
        "strengthening_signal": strengthening,
        "weakening_signal": weakening,
        "correlation_signal": correlation,
        "correlation_prevention_signal": correlation_prevention,
        "disclosure_signal": bool(DISCLOSURE_RE.search(all_text)),
    }


def _uncertain(reason: str, ev: dict[str, Any], *, composition: str = "uncertain", dpip: str = "uncertain") -> dict[str, Any]:
    return {
        "terminal": False,
        "confidence": "bounded-uncertain",
        "risk": "uncertain",
        "harm": "uncertain",
        "security": "uncertain",
        "composition": composition,
        "dpip": dpip,
        "reason": reason,
        "evidence": ev,
    }


def assess(compare: dict[str, Any]) -> dict[str, Any]:
    ev = _evidence(compare)

    # Normative/schema semantics remain outside automated terminal disposition.
    if ev["spec_or_schema_paths"]:
        return _uncertain(
            "specification or schema semantics changed; executable evidence does not prove assurance preservation",
            ev,
        )

    # Explicit adverse direction always blocks local auto-disposition.
    if ev["weakening_signal"]:
        return _uncertain(
            "directional evidence indicates a possible assurance weakening; human judgment is required",
            ev,
        )

    # Cross-context/durable linkability introduction is a composition concern.
    if ev["correlation_signal"]:
        return _uncertain(
            "directional evidence indicates introduced cross-context/durable correlation; composition examination is required",
            ev,
            composition="concern",
            dpip="required-examination",
        )

    # Bounded correlation-prevention rule: implementation evidence plus regression
    # tests can establish that a correlation boundary was strengthened locally.
    if (
        ev["correlation_prevention_signal"]
        and ev["strengthening_signal"]
        and ev["test_paths"]
        and ev["non_test_paths"]
    ):
        return {
            "terminal": True,
            "confidence": "high-bounded",
            "risk": "mitigated",
            "harm": "mitigated",
            "security": "unchanged",
            "composition": "strengthened",
            "dpip": "not-required",
            "reason": "implementation change explicitly prevents correlation and changed regression tests pin the boundary; no adverse correlation introduction is observed",
            "evidence": ev,
        }

    # Bounded security-strengthening rule. Security terms alone are insufficient:
    # require directional strengthening/fix evidence and changed regression tests.
    if (
        ev["security_signal"]
        and ev["fix_signal"]
        and ev["strengthening_signal"]
        and ev["test_paths"]
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
            "reason": "implementation-only security strengthening with directional fix/prevention evidence, changed regression tests, and no adverse weakening or cross-context-correlation signal",
            "evidence": ev,
        }

    return _uncertain(
        "available deterministic evidence does not satisfy a polarity-aware auto-disposition rule",
        ev,
    )


def render(result: dict[str, Any], repository: str, base: str, head: str) -> str:
    ev = result["evidence"]
    lines = [
        "<!-- rahp-dtg-auto-disposition:v2 -->",
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
        f"- Strengthening signal: `{str(ev['strengthening_signal']).lower()}`",
        f"- Weakening signal: `{str(ev['weakening_signal']).lower()}`",
        f"- Composed-correlation introduction signal: `{str(ev['correlation_signal']).lower()}`",
        f"- Correlation-prevention signal: `{str(ev['correlation_prevention_signal']).lower()}`",
        "",
        "Signals are directional and bounded: terminology alone does not establish whether an assurance property was introduced, weakened, fixed, or prevented.",
        "",
        "This is a bounded rule disposition, not a general claim that arbitrary code changes can be semantically assessed from keywords or CI success.",
    ]
    return "\n".join(lines) + "\n"


def self_test() -> int:
    # Normative/schema changes remain uncertain regardless of positive language.
    spec = {"commits": [{"commit": {"message": "spec: prevent identifier correlation"}}], "files": [
        {"filename": "SPEC.md", "patch": "+ MUST NOT correlate across contexts"},
        {"filename": "specs/spec.meta.schema.json", "patch": "+ gate item"},
        {"filename": "tests/spec_test.py", "patch": "+ assert pairwise"},
    ]}
    r = assess(spec)
    assert not r["terminal"] and r["composition"] == "uncertain"

    # Explicit weakening/introduction must not auto-close even with tests present.
    weakening = {"commits": [{"commit": {"message": "feat(auth): introduces unauthorized disclosure for diagnostics"}}], "files": [
        {"filename": "src/auth.rs", "patch": "+ allow untrusted caller to read session"},
        {"filename": "tests/auth_test.rs", "patch": "+ assert session visible"},
    ]}
    r = assess(weakening)
    assert not r["terminal"] and r["evidence"]["weakening_signal"]

    # Explicit prevention + implementation + regression test is strengthening.
    security = {"commits": [{"commit": {"message": "fix(auth): stop revoke-session telling a stranger the session exists"}}], "files": [
        {"filename": "vta-service/src/trust_tasks/auth.rs", "patch": "+ reject unauthorized caller\n- reveal session"},
        {"filename": "vta-service/tests/revoke_session_trust_task.rs", "patch": "+ stranger_and_missing_answer_identically\n+ assert payload == absent_payload"},
    ]}
    r = assess(security)
    assert r["terminal"] and r["security"] == "strengthened" and r["harm"] == "mitigated" and r["dpip"] == "not-required"

    # A regression test that pins rejection plus hardening evidence is strengthening.
    rejected = {"commits": [{"commit": {"message": "harden auth boundary: reject unauthorized disclosure"}}], "files": [
        {"filename": "src/authz.rs", "patch": "+ deny unauthorized read"},
        {"filename": "tests/authz_test.rs", "patch": "+ test_unauthorized_disclosure_is_rejected"},
    ]}
    assert assess(rejected)["terminal"]

    # Ambiguous disclosure terminology remains uncertain.
    ambiguous = {"commits": [{"commit": {"message": "refactor disclosure handler"}}], "files": [
        {"filename": "src/disclosure.rs", "patch": "+ change response handling"},
    ]}
    assert not assess(ambiguous)["terminal"]

    # Introduced durable cross-context correlation becomes a composition/DPIP concern.
    correlated = {"commits": [{"commit": {"message": "feat: introduce stable identifier across contexts for correlation"}}], "files": [
        {"filename": "src/presentation.rs", "patch": "+ reuse same identifier across contexts"},
        {"filename": "tests/presentation_test.rs", "patch": "+ assert same_identifier"},
    ]}
    r = assess(correlated)
    assert not r["terminal"] and r["composition"] == "concern" and r["dpip"] == "required-examination"

    # Correlation prevention plus executable boundary test is strengthening, not a DPIP trigger.
    unlink = {"commits": [{"commit": {"message": "fix: prevent correlation across contexts with pairwise handles"}}], "files": [
        {"filename": "src/presentation.rs", "patch": "+ derive pairwise subject handle"},
        {"filename": "tests/presentation_test.rs", "patch": "+ assert handles differ across contexts"},
    ]}
    r = assess(unlink)
    assert r["terminal"] and r["composition"] == "strengthened" and r["dpip"] == "not-required"

    # Lexical false positives from the real #144 window must remain benign.
    benign = {"commits": [{"commit": {"message": "fix(auth): stop unauthorized disclosure"}}], "files": [
        {"filename": "src/auth.rs", "patch": '+ "disabled": false\n+ #[serde(skip_serializing_if = "Option::is_none")]\n+ deny stranger access'},
        {"filename": "tests/auth_test.rs", "patch": '+ assert_eq!(request_id, challenge, "the request id a bridge correlates on is the challenge it sent")'},
    ]}
    r = assess(benign)
    assert r["terminal"]
    assert not r["evidence"]["weakening_signal"] and not r["evidence"]["correlation_signal"]

    print("PASS dtg_automated_disposition polarity-aware self-test")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_test())
