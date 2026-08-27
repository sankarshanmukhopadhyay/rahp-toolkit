#!/usr/bin/env python3
"""Route DTG Portfolio Monitor findings into explicit assurance dispositions."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
from collections import defaultdict
from typing import Any

import yaml


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("routing policy must be a mapping")
    return value


def qualifies(finding: dict[str, Any], policy: dict[str, Any]) -> bool:
    q = policy.get("qualification") or {}
    return (
        finding.get("state") == "open"
        and finding.get("review_status") in (None, "unreviewed")
        and finding.get("materiality") in set(q.get("materiality") or [])
        and finding.get("assurance_impact") in set(q.get("assurance_impact") or [])
    )


def matches(rule: dict[str, Any], finding: dict[str, Any]) -> bool:
    repo = str(finding.get("repository") or "")
    title = str(finding.get("title") or "")
    if rule.get("repository_regex") and not re.search(str(rule["repository_regex"]), repo, re.I):
        return False
    if rule.get("title_regex") and not re.search(str(rule["title_regex"]), title, re.I):
        return False
    return True


def route_findings(findings: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    routed: list[dict[str, Any]] = []
    fallback = policy.get("fallback") or {"outcome": "unresolved"}
    for finding in findings:
        if not qualifies(finding, policy):
            continue
        decision = None
        for rule in policy.get("finding_rules") or []:
            if matches(rule, finding):
                decision = rule
                break
        decision = decision or fallback
        routed.append({
            "finding": finding,
            "rule_id": decision.get("id", "fallback"),
            "outcome": decision.get("outcome", "unresolved"),
            "decision": decision,
        })
    return routed


def compositions(routed: list[dict[str, Any]], policy: dict[str, Any]) -> list[str]:
    names: set[str] = set()
    for item in routed:
        finding = item["finding"]
        if finding.get("repository"):
            names.add(str(finding["repository"]).lower())
        names.update(str(v).lower() for v in finding.get("related_repositories") or [])
    joined = "\n".join(sorted(names))
    selected: list[str] = []
    for rule in policy.get("composition_rules") or []:
        tokens = [str(t).lower() for t in rule.get("requires_repository_tokens") or []]
        if tokens and all(token in joined for token in tokens):
            selected.append(str(rule["id"]))
    return list(dict.fromkeys(selected))


def cluster_digest(items: list[dict[str, Any]]) -> str:
    ids = sorted(str(i["finding"].get("fingerprint") or i["finding"].get("finding_id")) for i in items)
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()[:16]


def findings_table(items: list[dict[str, Any]]) -> str:
    rows = ["| Finding | Repository | Change |", "|---|---|---|"]
    for item in items:
        f = item["finding"]
        title = str(f.get("title") or "").replace("|", "\\|")
        rows.append(f"| `{f.get('finding_id')}` | `{f.get('repository')}` | {title} |")
    return "\n".join(rows)


def combined_event(rule_id: str, items: list[dict[str, Any]], day: str) -> dict[str, Any]:
    digest = cluster_digest(items)
    body = (
        "# Automated bounded combined review\n\n"
        f"<!-- dtg-routing-policy:v1 -->\n"
        f"<!-- dtg-routing-cluster:{digest} -->\n\n"
        f"Portfolio snapshot: `{day}`  \nRouting rule: `{rule_id}`\n\n"
        "## Proposition\n\n"
        "Determine whether this coherent material change set preserves, strengthens, weakens, or creates new RAHP/security assurance propositions. Treat apparent mitigations as falsifiable claims and check for regressions.\n\n"
        f"## Routed findings\n\n{findings_table(items)}\n\n"
        "## Required disposition\n\n"
        "- Record proposition-level outcomes: preserved / strengthened / weakened / new / uncertain.\n"
        "- Record boundary cases and regression evidence.\n"
        "- Promote any privacy-composition question through the canonical DPIP handoff rather than resolving it here.\n"
        "- Link the result to the portfolio controller.\n"
    )
    return {
        "assessment_key": f"dtg:portfolio:combined:{rule_id}",
        "observed_at": day,
        "source": "dtg-portfolio-monitor-routing",
        "title": f"[DTG portfolio] Bounded combined RAHP + security review — {rule_id}",
        "labels": ["assessment-required", "dtg-instance"],
        "affected_reviews": ["rahp", "security", "combined"],
        "body": body,
    }


def dpip_event(rule_id: str, items: list[dict[str, Any]], day: str) -> dict[str, Any]:
    decision = items[0]["decision"]
    dpip = decision.get("dpip") or {}
    digest = cluster_digest(items)
    source = {
        "monitor_fingerprint": f"dtg-portfolio-{day}-{digest}",
        "repository": "sankarshanmukhopadhyay/dtg-portfolio-monitor",
        "revision": day,
    }
    source_pins = []
    seen_pins: set[tuple[str, str]] = set()
    for item in items:
        finding = item["finding"]
        repository = str(finding.get("repository") or "")
        revisions: list[str] = []
        direct = str(finding.get("revision") or finding.get("commit_sha") or "")
        if re.fullmatch(r"[0-9a-f]{40}", direct, re.I):
            revisions.append(direct)
        for url in finding.get("evidence_urls") or []:
            match = re.search(r"/commit/([0-9a-f]{40})(?:$|[/?#])", str(url), re.I)
            if match:
                revisions.append(match.group(1))
        for revision in revisions:
            key = (repository, revision.lower())
            if repository and key not in seen_pins:
                seen_pins.add(key)
                source_pins.append({"label": repository, "repository": repository, "revision": revision})
    payload = {
        "dpip": {
            "recommendation": "examine",
            **{k: v for k, v in dpip.items() if k != "question"},
            "source_change": source,
            "source_pins": source_pins,
            "question": dpip.get("question"),
        }
    }
    yaml_block = yaml.safe_dump(payload, sort_keys=False).rstrip()
    body = (
        "# RAHP privacy referral\n\n"
        f"<!-- dtg-routing-policy:v1 -->\n"
        f"<!-- dtg-routing-cluster:{digest} -->\n\n"
        f"Portfolio snapshot: `{day}`  \nRouting rule: `{rule_id}`\n\n"
        f"## Routed findings\n\n{findings_table(items)}\n\n"
        "## Promotion gate\n\n"
        "RAHP has determined that these material changes raise a composed privacy/correlation question. RAHP does not prejudge the DPIP result; DPIP owns applicability, evidence selection and the scoped conclusion.\n\n"
        f"```yaml\n{yaml_block}\n```\n"
    )
    return {
        "assessment_key": f"dtg:portfolio:dpip:v2:{rule_id}:{digest}",
        "observed_at": day,
        "source": "dtg-portfolio-monitor-routing",
        "title": f"[DPIP requested] DTG portfolio privacy examination — {rule_id}",
        "labels": ["assurance:dpip-requested", "dtg-instance"],
        "body": body,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings", type=pathlib.Path, required=True)
    ap.add_argument("--policy", type=pathlib.Path, required=True)
    ap.add_argument("--snapshot-date", required=True)
    ap.add_argument("--out-dir", type=pathlib.Path, required=True)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    policy = load_yaml(args.policy)
    if args.self_test:
        fixture = [
            {"finding_id":"p","fingerprint":"p","state":"open","review_status":"unreviewed","materiality":"high","assurance_impact":"potentially-breaking","repository":"trustoverip/dtgwg-cred-spec","title":"Name asymmetric relationship edge correlation scope","related_repositories":[]},
            {"finding_id":"s","fingerprint":"s","state":"open","review_status":"unreviewed","materiality":"high","assurance_impact":"breaking","repository":"OpenVTC/openvtc","title":"fix auth conformance","related_repositories":[]},
            {"finding_id":"u","fingerprint":"u","state":"open","review_status":"unreviewed","materiality":"high","assurance_impact":"breaking","repository":"example/unknown","title":"unknown material change","related_repositories":[]},
        ]
        outcomes = [x["outcome"] for x in route_findings(fixture, policy)]
        assert outcomes == ["dpip", "combined", "unresolved"], outcomes
        grouped = defaultdict(list)
        for item in route_findings(fixture, policy):
            grouped[(item["outcome"], item["rule_id"])].append(item)
        combined_body = combined_event("openvtc-security-combined", grouped[("combined", "openvtc-security-combined")], "2026-08-27")["body"]
        dpip_body = dpip_event("relationship-correlation-privacy", grouped[("dpip", "relationship-correlation-privacy")], "2026-08-27")["body"]
        assert 'f"' not in combined_body and '\\n"' not in combined_body
        assert 'f"' not in dpip_body and '\\n"' not in dpip_body
        assert "## Routed findings" in combined_body and "## Promotion gate" in dpip_body
        assert "credential-proof-trust-task-consequential-execution" in dpip_body
        assert "correlation-scope-does-not-expand-through-composition" in dpip_body
        event = dpip_event("relationship-correlation-privacy", grouped[("dpip", "relationship-correlation-privacy")], "2026-08-27")
        assert event["assessment_key"].startswith("dtg:portfolio:dpip:v2:relationship-correlation-privacy:")
        assert event["assessment_key"].endswith(cluster_digest(grouped[("dpip", "relationship-correlation-privacy")]))
        print("PASS dtg portfolio routing self-test")
        return 0

    findings = json.loads(args.findings.read_text(encoding="utf-8"))
    if not isinstance(findings, list):
        raise SystemExit("findings must be a JSON array")
    routed = route_findings(findings, policy)
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in routed:
        grouped[(item["outcome"], item["rule_id"])].append(item)

    combined = [combined_event(rule, items, args.snapshot_date) for (outcome, rule), items in grouped.items() if outcome == "combined"]
    dpip = [dpip_event(rule, items, args.snapshot_date) for (outcome, rule), items in grouped.items() if outcome == "dpip"]
    unresolved = [
        {"finding_id": item["finding"].get("finding_id"), "repository": item["finding"].get("repository"), "title": item["finding"].get("title"), "rule_id": item["rule_id"]}
        for item in routed if item["outcome"] == "unresolved"
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "routing.json").write_text(json.dumps(routed, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "combined-events.json").write_text(json.dumps(combined, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "dpip-events.json").write_text(json.dumps(dpip, indent=2) + "\n", encoding="utf-8")
    (args.out_dir / "unresolved.json").write_text(json.dumps(unresolved, indent=2) + "\n", encoding="utf-8")
    selected = compositions(routed, policy)
    (args.out_dir / "compositions.txt").write_text("\n".join(selected) + ("\n" if selected else ""), encoding="utf-8")
    print(json.dumps({"qualified": len(routed), "combined": len(combined), "dpip": len(dpip), "unresolved": len(unresolved), "compositions": selected}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
