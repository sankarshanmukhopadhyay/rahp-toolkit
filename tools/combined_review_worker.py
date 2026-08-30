#!/usr/bin/env python3
"""Advance routed combined RAHP reviews to deterministic evidence and reviewer-ready judgment packets."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

REPO = "sankarshanmukhopadhyay/rahp-toolkit"
ASSESSMENT = "assessment-required"
JUDGMENT = "judgment-required"
EXECUTED = "assessment-evidence-complete"
MARKER = "<!-- rahp-combined-execution:v1 -->"
PACKET_MARKER = "<!-- rahp-combined-judgment-packet:v1 -->"
FINDING_RE = re.compile(r"([0-9a-f]{20})")
SNAPSHOT_RE = re.compile(r"Portfolio(?: Monitor)? snapshot:\s*`(\d{4}-\d{2}-\d{2})`")
MONITOR_RAW = "https://raw.githubusercontent.com/sankarshanmukhopadhyay/dtg-portfolio-monitor/main/data/findings/{year}/{month}/{day}.json"


def api(method: str, path: str, token: str, payload: Any | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/{path}", data=data, method=method,
        headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
                 "User-Agent": "rahp-combined-review-worker/1.1", "X-GitHub-Api-Version": "2022-11-28",
                 **({"Content-Type": "application/json"} if data is not None else {})},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


def label_names(issue: dict[str, Any]) -> set[str]:
    return {str(item.get("name")) for item in issue.get("labels", [])}


def is_combined(issue: dict[str, Any]) -> bool:
    body = issue.get("body") or ""
    states = label_names(issue)
    return issue.get("state") == "open" and "dtg:portfolio:combined:" in body and bool({ASSESSMENT, JUDGMENT} & states)


def finding_ids(body: str) -> list[str]:
    return list(dict.fromkeys(FINDING_RE.findall(body or "")))


def snapshot_date(body: str) -> str:
    match = SNAPSHOT_RE.search(body or "")
    if not match:
        raise ValueError("combined review does not identify a Portfolio Monitor snapshot date")
    return match.group(1)


def fetch_monitor_findings(day: str) -> dict[str, dict[str, Any]]:
    year, month, date = day.split("-")
    url = MONITOR_RAW.format(year=year, month=month, day=date)
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("Portfolio Monitor finding snapshot is not a JSON array")
    return {str(item.get("finding_id")): item for item in payload if item.get("finding_id")}


def assurance_dimension(finding: dict[str, Any]) -> tuple[str, str]:
    text = f"{finding.get('title','')} {finding.get('summary','')}".lower()
    if any(k in text for k in ("keyid", "key id", "key creation", "key provenance")):
        return "key provenance / identity binding", "Does the change preserve authoritative key provenance and prevent substitution, confused-deputy, or locally invented identity bindings?"
    if any(k in text for k in ("auth", "challenge", "personhood", "publication authentication", "document-proof")):
        return "authentication / replay / authorization", "Does the change strengthen authentication without introducing replay, challenge-reuse, authorization, or proof-binding regressions?"
    if any(k in text for k in ("lifecycle", "cache", "freshness", "status", "supersed")):
        return "lifecycle / freshness / state", "Does the change preserve correct current-state and freshness semantics without accepting stale, cached, superseded, or ambiguously scoped evidence?"
    if any(k in text for k in ("conformance", "response", "error")):
        return "conformance / response semantics", "Does the change close protocol drift without changing response/error semantics in a way that weakens security, interoperability, or recoverability?"
    if any(k in text for k in ("trust task", "dependency", "spec-surface", "spec surface")):
        return "cross-specification dependency", "Does the dependency/spec-surface change preserve the assurance assumptions already tested in Trust Tasks × Credential Spec, or does it introduce a new composition proposition?"
    if any(k in text for k in ("invitation", "common structure", "ingested")):
        return "input structure / protocol validation", "Does the stricter input structure reject malformed or ambiguous invitations without creating a new compatibility, downgrade, or bypass path?"
    return "general implementation assurance", "Does this material change preserve the existing RAHP/security proposition, strengthen it, weaken it, or introduce a genuinely new proposition?"


def evidence_links(finding: dict[str, Any]) -> str:
    urls = [str(u) for u in finding.get("evidence_urls", []) if u]
    if not urls:
        return "none published"
    return " · ".join(f"[evidence {i+1}]({url})" for i, url in enumerate(urls))


def render_judgment_packet(issue: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> str:
    ids = finding_ids(issue.get("body") or "")
    missing = [fid for fid in ids if fid not in catalog]
    if missing:
        raise ValueError("Portfolio Monitor snapshot is missing routed finding IDs: " + ", ".join(missing))
    lines = [
        PACKET_MARKER,
        "## Reviewer judgment packet",
        "",
        "The deterministic stage is complete. This packet resolves the routed finding IDs into the smallest review surface needed for human assurance judgment; it does **not** pre-classify the outcome.",
        "",
        "### Decision rubric",
        "",
        "For each item record **preserved / strengthened / weakened / new / uncertain**, a short rationale, and any required follow-up. A new RAHP finding or composition should be created only where the evidence changes an assurance proposition rather than merely implementation detail.",
        "",
    ]
    for idx, fid in enumerate(ids, 1):
        f = catalog[fid]
        dimension, proposition = assurance_dimension(f)
        related = ", ".join(f"`{r}`" for r in f.get("related_repositories", []) or []) or "none declared"
        lines.extend([
            f"### {idx}. `{fid}` — {f.get('title','(untitled change)')}",
            "",
            f"- **Repository:** `{f.get('repository','unknown')}`",
            f"- **Monitor classification:** `{f.get('severity','unknown')}` severity; `{f.get('assurance_impact','unknown')}` assurance impact; `{f.get('kind','unknown')}`",
            f"- **Related repositories:** {related}",
            f"- **Likely assurance dimension:** {dimension}",
            f"- **Evidence:** {evidence_links(f)}",
            f"- **Question for judgment:** {proposition}",
            "- **Reviewer disposition:** _preserved / strengthened / weakened / new / uncertain_",
            "- **Rationale / boundary case:** _to be completed_",
            "- **Follow-up:** _none / new RAHP finding / new composition / regression action_",
            "",
        ])
    lines.extend([
        "### Cross-item synthesis",
        "",
        "After the per-item decisions, answer three portfolio questions:",
        "1. Do any of the nine changes jointly create a security proposition that is not visible when each change is considered alone?",
        "2. Does any item reverse a provisional no-additional-assurance-action disposition from the parent controller?",
        "3. Can the change set be closed as assurance-preserving/strengthening, or must a new RAHP finding/composition remain open?",
        "",
        "When this synthesis is complete, link the disposition back to the portfolio controller and close this bounded review if no further RAHP work remains.",
    ])
    return "\n".join(lines) + "\n"


def render_record(issue: dict[str, Any]) -> str:
    ids = finding_ids(issue.get("body") or "")
    if not ids:
        raise ValueError("combined review contains no reconstructable Portfolio Monitor finding IDs")
    lines = [MARKER, "## Automated bounded evidence execution", "", f"- Review issue: #{issue['number']}",
             f"- Routed finding IDs recovered: **{len(ids)}**",
             "- Execution result: **deterministic evidence complete; semantic judgment required**", "",
             "### Proposition tested", "",
             "Can the routed change set be disposed mechanically, or does RAHP require substantive interpretation of whether assurance propositions were preserved, strengthened, weakened, newly introduced, or left uncertain?", "",
             "### Mechanically established", "", "- The portfolio route is reproducible from durable finding identifiers.",
             "- The work item is explicitly scoped to combined RAHP + security assurance.",
             "- RAHP can establish routing, provenance, scope and deterministic validation boundaries without inventing semantic findings.",
             "- Successful tooling execution is **not** evidence that the underlying security/assurance proposition passed.", "",
             "### Falsification / boundary evidence", "", "- Treating command success as semantic assurance is rejected as a false positive.",
             "- Missing finding identifiers are an execution failure, not a judgment request.",
             "- Composed privacy questions remain outside this review and must use the canonical RAHP → DPIP path.", "",
             "### Judgment required", "",
             "Classify the material propositions as **preserved / strengthened / weakened / new / uncertain**, identify regressions or reversals of provisional no-action dispositions, and promote any new RAHP finding or composition only when supported by the routed evidence.", "",
             "### Routed finding IDs", ""]
    lines.extend(f"- `{fid}`" for fid in ids)
    return "\n".join(lines) + "\n"


def ensure_label(name: str, token: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        api("GET", f"labels/{encoded}", token); return
    except urllib.error.HTTPError as exc:
        if exc.code != 404: raise
    api("POST", "labels", token, {"name": name, "color": "fbca04", "description": "RAHP explicit judgment/evidence state"})


def remove_label(issue_number: int, name: str, token: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        api("DELETE", f"issues/{issue_number}/labels/{encoded}", token)
    except urllib.error.HTTPError as exc:
        if exc.code != 404: raise


def comments(issue_number: int, token: str) -> list[dict[str, Any]]:
    return api("GET", f"issues/{issue_number}/comments?per_page=100", token) or []


def has_marker(existing: list[dict[str, Any]], marker: str) -> bool:
    return any(marker in (comment.get("body") or "") for comment in existing)


def advance(issue: dict[str, Any], token: str) -> None:
    existing = comments(issue["number"], token)
    labels = label_names(issue)
    if ASSESSMENT in labels:
        if not has_marker(existing, MARKER):
            api("POST", f"issues/{issue['number']}/comments", token, {"body": render_record(issue)})
        for label in (JUDGMENT, EXECUTED): ensure_label(label, token)
        api("POST", f"issues/{issue['number']}/labels", token, {"labels": [JUDGMENT, EXECUTED]})
        remove_label(issue["number"], ASSESSMENT, token)
    if not has_marker(existing, PACKET_MARKER):
        day = snapshot_date(issue.get("body") or "")
        catalog = fetch_monitor_findings(day)
        api("POST", f"issues/{issue['number']}/comments", token, {"body": render_judgment_packet(issue, catalog)})
    print(f"JUDGMENT_READY #{issue['number']}")


def run(token: str, issue_number: int | None = None) -> int:
    if issue_number:
        issues = [api("GET", f"issues/{issue_number}", token)]
    else:
        encoded = urllib.parse.quote("dtg-instance", safe="")
        issues = api("GET", f"issues?state=open&labels={encoded}&per_page=100", token) or []
    failures = 0
    for issue in issues:
        if not is_combined(issue): continue
        try: advance(issue, token)
        except Exception as exc:
            failures += 1; print(f"FAIL #{issue.get('number')}: {exc}", file=sys.stderr)
    return 1 if failures else 0


def self_test() -> int:
    issue = {"state": "open", "number": 121, "labels": [{"name": ASSESSMENT}],
             "body": "<!-- rahp-assessment-key:dtg:portfolio:combined:test -->\nPortfolio Monitor snapshot: `2026-08-27`\n- 307e953d00cf9fb48ba7\n- 0bb1b102763cd38950c0\n"}
    assert is_combined(issue)
    assert finding_ids(issue["body"]) == ["307e953d00cf9fb48ba7", "0bb1b102763cd38950c0"]
    assert snapshot_date(issue["body"]) == "2026-08-27"
    assert snapshot_date("Portfolio snapshot: `2026-08-30`") == "2026-08-30"
    try:
        snapshot_date("Unrelated date: `2026-08-30`")
    except ValueError:
        pass
    else:
        raise AssertionError("snapshot parser must require an explicit portfolio snapshot field")
    rendered = render_record(issue)
    assert "semantic judgment required" in rendered and "false positive" in rendered
    fixture = {
        "307e953d00cf9fb48ba7": {"finding_id": "307e953d00cf9fb48ba7", "repository": "OpenVTC/openvtc", "title": "fix(join)!: require common structure on invitation", "severity": "high", "assurance_impact": "potentially-breaking", "kind": "material_cross_reference", "evidence_urls": ["https://example.invalid/pr/1"], "related_repositories": []},
        "0bb1b102763cd38950c0": {"finding_id": "0bb1b102763cd38950c0", "repository": "OpenVTC/vti", "title": "fix(vta)!: conformance responses", "severity": "high", "assurance_impact": "potentially-breaking", "kind": "material_cross_reference", "evidence_urls": [], "related_repositories": ["trustoverip/dtgwg-trust-tasks-tf"]},
    }
    packet = render_judgment_packet(issue, fixture)
    assert "Reviewer judgment packet" in packet
    assert "input structure / protocol validation" in packet
    assert "conformance / response semantics" in packet
    assert "Reviewer disposition" in packet
    print("PASS combined_review_worker self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--issue", type=int); parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test: return self_test()
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token: print("GITHUB_TOKEN or GH_TOKEN is required", file=sys.stderr); return 2
    return run(token, args.issue)


if __name__ == "__main__":
    raise SystemExit(main())
