#!/usr/bin/env python3
"""Choose Toolkit publication inputs only after a Registry-observed group receipt.

No cutover if reservation is pending, approval withdrawn, Registry issue missing,
current event not acknowledged, or either repository changes during qualification.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

import publish_assessment_issues as publisher
import stage_registry_source_partition as partition

REG = "sankarshanmukhopadhyay/rahp-assessment-registry"
TK = publisher.CANONICAL_RAHP_ISSUE_REPOSITORY
API = "https://api.github.com/repos/"
KEY = "dtg:portfolio:combined:spec-dependency-alignment"
CASE_MARK = "<!-- registry-assessment-key:" + KEY + " -->"
GROUP_MARK = "<!-- rahp-registry-monitored-group:v1:"
ACK_MARK = "<!-- rahp-registry-observation:v1:"
SCOPE_MARK = "<!-- rahp-registry-maintainer-scope:v1:"
USER = "sankarshanmukhopadhyay"

class PartitionError(ValueError):
    pass

def all_pages(get, repo, path):
    rows = []
    for page in range(1, 101):
        batch = get(API + repo + path + ("&" if "?" in path else "?") +
                    "per_page=100&page=" + str(page))
        if not isinstance(batch, list):
            raise PartitionError("incomplete GitHub pagination for " + repo)
        rows.extend(batch)
        if len(batch) < 100:
            return rows
    raise PartitionError("GitHub pagination exceeded safe limit")

def branch(get, repo):
    obj = get(API + repo + "/branches/main")
    sha = ((obj or {}).get("commit") or {}).get("sha")
    if not isinstance(sha, str) or not re.fullmatch("[0-9a-f]{40}", sha):
        raise PartitionError("unavailable main branch authority: " + repo)
    return sha

def trusted(comment):
    if not isinstance(comment, dict) or not isinstance(comment.get("user"), dict):
        return False
    actor = comment["user"]
    return ((actor.get("login") == USER and
             comment.get("author_association") == "OWNER") or
            (actor.get("login") == "github-actions[bot]" and actor.get("type") == "Bot"))

def verify_scope(get, scope):
    comments = all_pages(get, REG, "/issues/11/comments?")
    matches = []
    for obj in comments:
        body = obj.get("body") or ""
        found = re.findall(re.escape(SCOPE_MARK) +
                           r"(accept|withdraw):([0-9a-f]{64}) -->", body)
        for action, digest in found:
            if digest == scope:
                if not trusted(obj) or obj["user"].get("login") != USER:
                    raise PartitionError("unauthorized scoped maintainer decision")
                if type(obj.get("id")) is not int:
                    raise PartitionError("unverifiable maintainer decision order")
                matches.append((obj["id"], action))
    if not matches or sorted(matches)[-1][1] != "accept":
        raise PartitionError("maintainer approval absent or withdrawn")
    return True

def verify_registry_ack(get, transfer, event_sha):
    issue_url = transfer["registry_issue_url"]
    expected = publisher.REGISTRY_ISSUE_PREFIX
    if not isinstance(issue_url, str) or not re.fullmatch(
            re.escape(expected) + r"[1-9][0-9]*", issue_url):
        raise PartitionError("invalid accepted Registry issue URL")
    n = int(issue_url.removeprefix(expected))
    registry_head = branch(get, REG)
    issue = get(API + REG + "/issues/" + str(n))
    if (not isinstance(issue, dict) or issue.get("number") != n
            or issue.get("html_url") != issue_url or issue.get("state") != "open"
            or "pull_request" in issue):
        raise PartitionError("accepted Registry issue not live and open")
    body = issue.get("body") or ""
    if CASE_MARK not in body or GROUP_MARK + transfer["group_sha256"] + " -->" not in body:
        raise PartitionError("Registry owner lacks exact group identity")
    if transfer["toolkit_issue_url"] not in body:
        raise PartitionError("Registry owner lacks original Toolkit identity")
    for fid in transfer["finding_ids"]:
        if fid not in body:
            raise PartitionError("Registry owner omits original source finding")
    owners = [x for x in all_pages(get, REG, "/issues?state=all")
              if isinstance(x, dict) and "pull_request" not in x
              and CASE_MARK in (x.get("body") or "")]
    if len(owners) != 1 or owners[0].get("number") != n:
        raise PartitionError("duplicate or missing Registry assessment key owner")
    acks = all_pages(get, REG, "/issues/" + str(n) + "/comments?")
    marker = ACK_MARK + event_sha + " -->"
    acknowledgments = [x for x in acks if isinstance(x, dict)
                       and marker in (x.get("body") or "")]
    if not acknowledgments or any(not trusted(x) for x in acknowledgments):
        raise PartitionError("current observation lacks authenticated Registry acknowledgment")
    verify_scope(get, transfer["maintainer_scope_sha256"])
    if branch(get, REG) != registry_head:
        raise PartitionError("Registry source authority changed during acknowledgment")
    return issue_url

def plan(paths, stage_dir, ledger, *, token=None, get=None, context=None,
         source_combined=None):
    if not isinstance(paths, list) or len(paths) != 3:
        raise PartitionError("exactly three Toolkit event batches required")
    if [p.name for p in paths] != [
            "controller-events.json", "combined-events.json", "dpip-events.json"]:
        raise PartitionError("unknown or reordered canonical publication batches")
    records = json.loads(ledger.read_text(encoding="utf-8"))["transfers"]
    receipt = partition.stage(paths, stage_dir, ledger,
                              source_combined=source_combined)
    if not records:
        if receipt["held_count"] != 0:
            raise PartitionError("empty ledger unexpectedly held source events")
        return {"schema": "rahp-toolkit-guarded-publication-selection/v1",
                "mode": "legacy_no_transfer", "paths": [str(p) for p in paths],
                "retained_count": receipt["retained_count"], "held_count": 0,
                "registry_observation_acknowledged": False, "cutover_authorized": False}
    if len(records) != 1 or records[0]["state"] != "accepted_group":
        raise PartitionError("unaccepted/legacy mixed transfer blocks source-specific publication")
    transfer = records[0]
    if transfer["assessment_key"] != KEY:
        raise PartitionError("only reviewed pilot group has a source-specific route")
    if receipt["held_count"] != 1:
        raise PartitionError("accepted group must hold exactly one current observation")
    held = []
    selected = []
    for path in paths:
        held.extend(json.loads((stage_dir / (path.name + ".held.json")).read_text()))
        selected.append(stage_dir / (path.name + ".retained.json"))
    if (len(held) != 1 or held[0]["transfer"] != transfer
            or held[0]["source_event_sha256"] != transfer["group_sha256"]):
        raise PartitionError("staged group differs from approved source event")
    context = context or os.environ
    if (context.get("GITHUB_ACTIONS") != "true" or
            context.get("GITHUB_REPOSITORY") != TK or
            context.get("GITHUB_REF") != "refs/heads/main" or
            not re.fullmatch(r"[0-9a-f]{40}", context.get("GITHUB_SHA", ""))):
        raise PartitionError("accepted transfer may execute only in live Toolkit main workflow")
    if not token:
        raise PartitionError("authenticated cross-repository Registry receipt required")
    get = get or (lambda url: publisher.request("GET", url, token))
    if branch(get, TK) != context["GITHUB_SHA"]:
        raise PartitionError("Toolkit branch moved after the event runner started")
    registry_owner = verify_registry_ack(get, transfer, held[0]["source_event_sha256"])
    if branch(get, TK) != context["GITHUB_SHA"]:
        raise PartitionError("Toolkit main changed during acceptance check")
    for path in selected:
        publisher.preflight_transfer_files([path], ledger)
    return {"schema": "rahp-toolkit-guarded-publication-selection/v1",
            "mode": "registry_acknowledged_retained",
            "paths": [str(p) for p in selected],
            "retained_count": receipt["retained_count"],
            "held_count": receipt["held_count"],
            "registry_owner": registry_owner,
            "registry_observation_acknowledged": True,
            "cutover_authorized": False}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batches", nargs=3, required=True, type=Path)
    p.add_argument("--stage-dir", required=True, type=Path)
    p.add_argument("--source-combined", type=Path,
                   help="original pre-journal combined group source")
    p.add_argument("--ledger", default=publisher.TRANSFER_LEDGER, type=Path)
    p.add_argument("--receipt", required=True, type=Path)
    p.add_argument("--github-output", type=Path)
    args = p.parse_args()
    try:
        result = plan(args.batches, args.stage_dir, args.ledger,
                      token=os.getenv("GITHUB_TOKEN"),
                      source_combined=args.source_combined)
    except (OSError, ValueError, KeyError, TypeError, publisher.GitHubAPIError) as exc:
        print("BLOCKED Toolkit guarded retained publication:", exc, file=sys.stderr)
        return 1
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.github_output is not None:
        with args.github_output.open("a", encoding="utf-8") as output:
            for name, path in zip(("controller", "combined", "dpip"), result["paths"]):
                output.write(name + "=" + path + "\n")
    print("Toolkit publication selection:", result["mode"],
          "retained:", result["retained_count"], "held:", result["held_count"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
