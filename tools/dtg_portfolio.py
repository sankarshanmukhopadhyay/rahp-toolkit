#!/usr/bin/env python3
"""Discover the configured DTG portfolio and emit material repository-change events.

Operational contract:
- DTG deployment-specific adapter; portable RAHP core does not depend on it.
- Reads the DTG instance configuration plus the external portfolio registry and the
  persisted repository observation baseline.
- Resolves current repository heads, classifies changed paths against semantic assurance
  surfaces, and writes generated repository/review-event state for downstream publication.
- It detects deltas only; it does not perform a clean-room assessment and it does not
  itself prove that a changed or unchanged repository is safe.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import pathlib
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_CFG = ROOT / "instances/dtg/instance.yaml"

ASSURANCE_SURFACES = {
    "normative-semantics",
    "authority-and-delegation",
    "credential-lifecycle-status",
    "execution-and-outcome",
    "privacy-correlation-disclosure",
    "key-custody-export-signing",
    "identity-binding-resolution",
    "governance-policy-redress",
    "interop-composition-contract",
    "evidence-observability-audit",
}

SURFACE_TOKENS = {
    "authority-and-delegation": ("authority", "authoriz", "delegat", "admin", "scope", "capability", "permission", "acl"),
    "credential-lifecycle-status": ("credential", "status", "revocation", "revoke", "issuance", "expiry", "expiration", "vac", "vdc", "vic"),
    "execution-and-outcome": ("execution", "outcome", "process", "attestation", "result", "replay"),
    "privacy-correlation-disclosure": ("privacy", "correlation", "disclosure", "persona", "facet", "profile", "claim", "holder"),
    "key-custody-export-signing": ("key", "sign", "crypto", "export", "custody", "seed", "mnemonic", "kms", "keystore"),
    "identity-binding-resolution": ("identity", "binding", "bind", "did", "resolution", "resolver", "member", "subject"),
    "governance-policy-redress": ("governance", "policy", "redress", "appeal", "contest", "remediation"),
    "interop-composition-contract": ("interop", "protocol", "wire", "schema", "composition", "contract", "transport"),
    "evidence-observability-audit": ("evidence", "audit", "observ", "log", "backup", "restore", "trace", "telemetry"),
}

SOURCE_EXTENSIONS = {".rs", ".py", ".ts", ".tsx", ".js", ".mjs", ".go", ".java", ".kt", ".swift", ".c", ".cc", ".cpp", ".h"}
LOW_VALUE_METADATA_NAMES = {"changelog.md", "cargo.toml", "cargo.lock", "package.json", "package-lock.json"}


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def api_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "dtg-rahp-instance/0.6",
        **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.environ.get("GITHUB_TOKEN") else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def raw_text(repo: str, branch: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "dtg-rahp-instance/0.6"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode()


def slug(repo: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", repo.lower()).strip("-")


def discover(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    portfolio = cfg["portfolio"]
    registry = yaml.safe_load(raw_text(portfolio["registry_repository"], portfolio.get("registry_branch", "main"), portfolio["registry_path"]))
    base = []
    for repo in registry.get("repositories", []):
        base.append({
            "id": slug(repo["repo"]),
            "repository": repo["repo"],
            "branch": repo.get("default_branch", "main"),
            "source": "portfolio-monitor",
            "upstream": None,
            "workstream": repo.get("workstream"),
            "role": repo.get("role"),
            "lifecycle": repo.get("lifecycle", "active"),
            "reporting_weight": repo.get("reporting_weight", "medium"),
            "material_paths": repo.get("material_paths", []),
            "reviews": ["rahp", "security", "combined"],
        })
    base_names = {item["repository"] for item in base}
    owner = portfolio.get("fork_owner")
    if owner:
        page = 1
        while True:
            repos = api_json(f"https://api.github.com/users/{owner}/repos?per_page=100&page={page}&type=owner")
            if not repos:
                break
            for repo in repos:
                if not repo.get("fork"):
                    continue
                detail = api_json(repo["url"])
                parent = (detail.get("parent") or {}).get("full_name")
                if parent in base_names:
                    upstream = next(item for item in base if item["repository"] == parent)
                    base.append({
                        **upstream,
                        "id": slug(repo["full_name"]),
                        "repository": repo["full_name"],
                        "branch": repo.get("default_branch", "main"),
                        "source": "portfolio-fork",
                        "upstream": parent,
                    })
            if len(repos) < 100:
                break
            page += 1
    review_repo = cfg["instance"].get("review_repository")
    for target in base:
        target["self_hosted_instance"] = target["repository"] == review_repo
    return base


def head_sha(repo: str, branch: str) -> str | None:
    try:
        return api_json(f"https://api.github.com/repos/{repo}/commits/{branch}")["sha"]
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            return None
        raise


def compare(repo: str, base: str, head: str) -> dict[str, Any]:
    return api_json(f"https://api.github.com/repos/{repo}/compare/{base}...{head}")


def path_matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) or pathlib.PurePosixPath(path).match(pattern) for pattern in patterns)


def _commit_subjects(commits: list[dict[str, Any]]) -> list[str]:
    subjects = []
    for item in commits:
        message = ((item.get("commit") or {}).get("message") or "").splitlines()
        if message:
            subjects.append(message[0].strip().lower())
    return subjects


def _release_signals(commits: list[dict[str, Any]]) -> tuple[bool, bool]:
    subjects = _commit_subjects(commits)
    if not subjects:
        return False, False
    release_prefixes = ("chore: release", "chore(release)", "release:", "chore: publish", "chore(publish)")
    codegen_prefixes = ("fix(ts): regenerate", "fix(codegen): regenerate", "chore(codegen): regenerate", "chore: regenerate")
    forbidden = ("depend", "security", "cve", "upgrade", "bump dependency", "update dependency")
    if any(token in subject for subject in subjects for token in forbidden):
        return False, False
    release_present = any(any(subject.startswith(prefix) for prefix in release_prefixes) for subject in subjects)
    propagation_only = release_present and all(any(subject.startswith(prefix) for prefix in release_prefixes + codegen_prefixes) for subject in subjects)
    return release_present, propagation_only


def _small_release_manifest_delta(file: dict[str, Any], release_present: bool) -> bool:
    if not release_present:
        return False
    path = file["filename"]
    additions = int(file.get("additions", 0) or 0)
    deletions = int(file.get("deletions", 0) or 0)
    if path.endswith(("Cargo.toml", "package.json")):
        return additions <= 2 and deletions <= 2
    if path.endswith(("Cargo.lock", "package-lock.json")):
        return additions <= 12 and deletions <= 12
    return False


def semantic_assurance_surfaces(path: str, target: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    """Explain which assurance surfaces a changed path intersects.

    Configured material paths are evidence, not an admission gate. Role-aware semantic
    surfaces allow normative and implementation changes to be seen even when an external
    registry's path list is incomplete. Unknown implementation source remains visible as
    low-confidence semantic work rather than being silently ignored.
    """
    mc = cfg["assessment"]["materiality"]
    configured = target.get("material_paths", [])
    always = mc.get("always_material_paths", [])
    role = str(target.get("role") or "")
    lower = path.lower()
    suffix = pathlib.PurePosixPath(path).suffix.lower()
    basename = pathlib.PurePosixPath(path).name.lower()
    sources = []
    surfaces = []

    if path_matches(path, configured):
        sources.append("configured-path")
    if path_matches(path, always):
        sources.append("always-material-path")

    normative_role = role in {"normative-specification", "protocol-and-task-specification"}
    if normative_role and (lower.startswith(("spec/", "specs/", "schemas/")) or "/spec/" in lower or "/specs/" in lower or suffix in {".md", ".yaml", ".yml", ".json"} and ("term" in lower or "definition" in lower)):
        surfaces.append("normative-semantics")
        sources.append("role-semantic-path")

    # Release/manifests are still admitted when configured, but semantic-looking package
    # directory names must not turn bounded propagation metadata into a high-weight
    # assurance surface. Their significance is handled by materiality_breakdown().
    if basename not in LOW_VALUE_METADATA_NAMES:
        token_haystack = re.sub(r"[^a-z0-9]+", " ", lower)
        for surface, tokens in SURFACE_TOKENS.items():
            if any(token in token_haystack for token in tokens):
                surfaces.append(surface)
                sources.append("semantic-token")

    implementation_role = role in {"implementation", "reference-implementation", "implementation-and-examples"}
    source_path = suffix in SOURCE_EXTENSIONS or lower.startswith("src/") or "/src/" in lower
    if implementation_role and source_path and not surfaces:
        surfaces.append("interop-composition-contract")
        sources.append("implementation-source-fallback")
        confidence = "low"
    else:
        confidence = "high" if surfaces else ("medium" if sources else "unknown")

    surfaces = list(dict.fromkeys(surface for surface in surfaces if surface in ASSURANCE_SURFACES))
    sources = list(dict.fromkeys(sources))
    reason = (
        f"assurance surfaces={','.join(surfaces)} via {','.join(sources)}"
        if surfaces
        else (f"no semantic surface resolved; signals={','.join(sources)}" if sources else "no configured or semantic materiality signal")
    )
    return {"surfaces": surfaces, "sources": sources, "confidence": confidence, "reason": reason}


def _semantic_candidate(file: dict[str, Any], target: dict[str, Any], cfg: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    detail = semantic_assurance_surfaces(file["filename"], target, cfg)
    return bool(detail["surfaces"] or detail["sources"]), detail


def materiality_breakdown(files: list[dict[str, Any]], cfg: dict[str, Any], commits: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    mc = cfg["assessment"]["materiality"]
    profile = mc.get("semantic_weighting", {})
    paths = {
        "normative": profile.get("normative_paths", ["schemas/**", "specs/**", "**/*spec*.md"]),
        "security": profile.get("security_sensitive_paths", [".github/workflows/**", "**/auth/**", "**/security/**"]),
        "generated": profile.get("generated_paths", ["bindings/**", "**/bindings/**", "**/schema_index.rs", "**/src/specs/**"]),
        "evidence": profile.get("evidence_paths", ["tests/**", "**/tests/**", "**/*test*.*"]),
        "release": profile.get("release_metadata_paths", ["CHANGELOG.md", "**/CHANGELOG.md", "Cargo.lock", "**/Cargo.lock"]),
        "manifests": profile.get("manifest_paths", ["Cargo.toml", "**/Cargo.toml", "package.json", "**/package.json", "package-lock.json", "**/package-lock.json"]),
    }
    weights = {"normative": 8.0, "security": 8.0, "semantic": 6.0, "dependency": 6.0, "generated": 2.0, "evidence": 1.0, "release": 0.25}
    weights.update({key: float(value) for key, value in (profile.get("weights") or {}).items()})
    release_present, release_only_window = _release_signals(commits or [])
    buckets = {key: [] for key in weights}
    for file in files:
        path = file["filename"]
        if path_matches(path, paths["normative"]):
            kind = "normative"
        elif path_matches(path, paths["security"]):
            kind = "security"
        elif path_matches(path, paths["generated"]):
            kind = "generated"
        elif path_matches(path, paths["evidence"]):
            kind = "evidence"
        elif path_matches(path, paths["release"]):
            kind = "release"
        elif path_matches(path, paths["manifests"]):
            kind = "release" if _small_release_manifest_delta(file, release_present) else "dependency"
        else:
            kind = "semantic"
        buckets.setdefault(kind, []).append(path)
    score = sum(weights.get(kind, 0.0) * len(items) for kind, items in buckets.items())
    return {
        "buckets": buckets,
        "weights": weights,
        "score": round(score, 2),
        "release_propagation_present": release_present,
        "release_propagation_window": release_only_window,
    }


def classify(target: dict[str, Any], files: list[dict[str, Any]], cfg: dict[str, Any], commits: list[dict[str, Any]] | None = None) -> tuple[str, list[str], list[str]]:
    mc = cfg["assessment"]["materiality"]
    reasons = []
    if target.get("lifecycle") == "transitional" and not mc.get("include_transitional", True):
        return "ignore", [], ["transitional repository excluded by DTG instance policy"]

    candidates = []
    details = {}
    for file in files:
        include, detail = _semantic_candidate(file, target, cfg)
        details[file["filename"]] = detail
        if include:
            candidates.append(file)

    matched = [file["filename"] for file in candidates]
    configured_count = sum("configured-path" in details[path]["sources"] or "always-material-path" in details[path]["sources"] for path in matched)
    semantic_only_count = sum(bool(details[path]["surfaces"]) and not ({"configured-path", "always-material-path"} & set(details[path]["sources"])) for path in matched)
    if matched:
        reasons.append(f"{len(matched)} changed file(s) carry configured or semantic assurance materiality signals")
        reasons.append(f"materiality sources: configured/always={configured_count}; semantic-only={semantic_only_count}")
    if target.get("reporting_weight") in mc.get("review_weights", []) and files:
        reasons.append(f"portfolio reporting weight is {target.get('reporting_weight')}")
    if not matched:
        return "ignore", matched, reasons

    surface_counts = {}
    low_confidence = []
    for path in matched:
        for surface in details[path]["surfaces"]:
            surface_counts[surface] = surface_counts.get(surface, 0) + 1
        if details[path]["confidence"] == "low":
            low_confidence.append(path)
    if surface_counts:
        reasons.append("assurance surfaces: " + ", ".join(f"{name}={count}" for name, count in sorted(surface_counts.items())))
    if low_confidence:
        reasons.append(f"{len(low_confidence)} implementation source file(s) have low-confidence semantic classification and remain visible for triage")

    documentation = mc.get("documentation_paths", [])
    triage_roles = set(mc.get("documentation_triage_roles", []))
    role = target.get("role")
    docs_only = bool(documentation) and all(path_matches(path, documentation) for path in matched)
    if role in triage_roles and docs_only:
        reasons.append("all material matches are documentation/routing paths for a triage-enabled repository role")
        return "triage", matched, reasons

    breakdown = materiality_breakdown(candidates, cfg, commits)
    buckets = breakdown["buckets"]
    summary = ", ".join(f"{kind}={len(items)}" for kind, items in buckets.items() if items)
    reasons.append(f"semantic materiality profile: {summary}; weighted evidence score={breakdown['score']}")
    if breakdown["release_propagation_window"]:
        reasons.append("commit window is bounded release/code-generation propagation; manifest fan-out receives release weight")

    # Assurance surfaces decide whether a path enters materiality and explain why. Once
    # admitted, the existing bounded file-kind model decides assessment vs triage/ignore,
    # so generated/evidence/release propagation cannot be upgraded merely by a semantic
    # token elsewhere in its package path.
    high_classes = ("normative", "security", "semantic", "dependency")
    if any(buckets.get(kind) for kind in high_classes):
        if low_confidence and len(low_confidence) == len(matched) and configured_count == 0:
            return "triage", matched, reasons
        return "assessment", matched, reasons
    if buckets.get("generated") or buckets.get("evidence"):
        reasons.append("matched changes are generated/evidence/release surfaces without a new high-weight semantic path")
        return "triage", matched, reasons
    if buckets.get("release") and breakdown["release_propagation_window"]:
        reasons.append("only release propagation remains after semantic weighting; no fresh assessment work item required")
        return "ignore", matched, reasons
    return "assessment", matched, reasons


def assessment_key(repo: str) -> str:
    return f"dtg:repository:{repo}"


def issue_mark(repo: str, sha: str) -> str:
    return f"<!-- rahp-assessment-key:{assessment_key(repo)} -->\n<!-- rahp-dtg-change:{repo}@{sha} -->"


def _file_rows(files: list[dict[str, Any]], matched: list[str]) -> str:
    return "\n".join(
        f"| `{file['filename']}` | {file.get('status','')} | +{file.get('additions',0)} / -{file.get('deletions',0)} | {'yes' if file['filename'] in matched else 'no'} |"
        for file in files[:100]
    )


def issue_body(target: dict[str, Any], old: str, new: str, comp: dict[str, Any], matched: list[str], reasons: list[str]) -> str:
    files = comp.get("files", [])
    commits = comp.get("commits", [])
    rows = _file_rows(files, matched)
    commit_rows = "\n".join(f"- `{commit['sha'][:12]}` {commit['commit']['message'].splitlines()[0]}" for commit in commits[:50])
    why = "\n".join(f"- {reason}" for reason in reasons) or "- Change intersects configured or semantic materiality signals."
    return f"""# DTG RAHP assessment required

{issue_mark(target['repository'], new)}

A change in a repository tracked by the DTG Portfolio Monitor has crossed the DTG
RAHP instance's materiality boundary. This issue is an **assessment queue record**,
not a finding and not evidence that the change is unsafe.

## Target

| Field | Value |
|---|---|
| Repository | `{target['repository']}` |
| Upstream | `{target.get('upstream') or 'n/a'}` |
| Portfolio source | `{target['source']}` |
| Workstream | `{target.get('workstream') or 'n/a'}` |
| Role | `{target.get('role') or 'n/a'}` |
| Lifecycle | `{target.get('lifecycle')}` |
| Reporting weight | `{target.get('reporting_weight')}` |
| Previous assessed/observed SHA | `{old}` |
| Current SHA | `{new}` |
| Compare | https://github.com/{target['repository']}/compare/{old}...{new} |

## Why review is required

{why}

Materiality is explainable independently from routing: configured paths are one signal,
while semantic assurance surfaces can promote otherwise omitted normative or implementation
changes. The change is queued for **combined RAHP + security review** by default.

## Material files

| File | Status | Delta | Materiality signal |
|---|---|---:|---|
{rows or '| _No file metadata returned_ | | | |'}

## Commits in the change window

{commit_rows or '- No commit metadata returned.'}

## Required review actions

1. Inspect the revision delta rather than reassessing unrelated repository content.
2. Determine whether changed requirements, schemas, workflows or implementation guidance alter existing risks, harms, controls, guardrails, threat assumptions or assurance evidence.
3. Run the appropriate RAHP, security or combined workflow using the target revision.
4. Store durable review artefacts under `instances/dtg/reviews/`.
5. Link findings to affected specification text and existing RAHP catalogue entries.
6. Record the disposition: no material assurance impact, finding(s) raised, remediation requested, or risk accepted by the relevant governance authority.
7. Close this issue only when the assessment record identifies the reviewed SHA `{new}`.

## Reproduce the workspace

```bash
python3 tools/rahp.py review --config instances/dtg/generated/repositories.yaml --mode combined --target {target['id']}
```

## Governance note

This issue was raised by the **DTG instance automation**. It is deliberately separate
from the portable RAHP toolkit. Other adopters do not inherit this portfolio, queue,
or DTG governance state.
"""


def triage_body(target: dict[str, Any], old: str, new: str, comp: dict[str, Any], matched: list[str], reasons: list[str]) -> str:
    files = comp.get("files", [])
    commits = comp.get("commits", [])
    rows = _file_rows(files, matched)
    commit_rows = "\n".join(f"- `{commit['sha'][:12]}` {commit['commit']['message'].splitlines()[0]}" for commit in commits[:50])
    why = "\n".join(f"- {reason}" for reason in reasons) or "- Change requires materiality classification."
    return f"""# DTG change classification required

{issue_mark(target['repository'], new)}

A change tracked by the DTG Portfolio Monitor carries configured or semantic materiality
signals, but the evidence is not sufficient for automatic promotion to a broad assessment.
This is a **classification queue record**, not a finding and not an assessment verdict.

## Target

| Field | Value |
|---|---|
| Repository | `{target['repository']}` |
| Workstream | `{target.get('workstream') or 'n/a'}` |
| Role | `{target.get('role') or 'n/a'}` |
| Lifecycle | `{target.get('lifecycle')}` |
| Previous observed SHA | `{old}` |
| Current SHA | `{new}` |
| Compare | https://github.com/{target['repository']}/compare/{old}...{new} |

## Why classification is required

{why}

## Changed files

| File | Status | Delta | Materiality signal |
|---|---|---:|---|
{rows or '| _No file metadata returned_ | | | |'}

## Commits in the change window

{commit_rows or '- No commit metadata returned.'}

## Required classification

Choose one disposition:
- **assessment-required** — semantics, assurance assumptions, security properties, governance dependencies, or interoperability behaviour changed;
- **topology-change** — canonical source, repository ownership/location, or portfolio routing changed without governed semantic change;
- **editorial/no-assurance-impact** — no assurance-relevant behaviour changed.

Unknown semantics remain visible and must not be converted silently into no-action.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["sync", "check"])
    parser.add_argument("--config", type=pathlib.Path, default=DEFAULT_CFG)
    parser.add_argument("--initialize", action="store_true", help="record current heads without raising review events")
    args = parser.parse_args()
    cfg = load_yaml(args.config)
    targets = discover(cfg)
    manifest = ROOT / cfg["generated"]["manifest"]
    manifest.parent.mkdir(parents=True, exist_ok=True)
    portable_targets = []
    for target in targets:
        portable_targets.append({
            "id": target["id"],
            "repository": target["repository"],
            "branch": target["branch"],
            **({"upstream": target["upstream"]} if target.get("upstream") else {}),
            "context": {
                "title": target["repository"],
                "type": target.get("role") or "repository",
                "description": f"DTG instance target discovered from {target['source']}; workstream={target.get('workstream') or 'n/a'}; lifecycle={target.get('lifecycle') or 'n/a'}; reporting_weight={target.get('reporting_weight') or 'n/a'}.",
            },
            "scope": {"include": target.get("material_paths") or ["README.md", "docs/**", "specs/**", "schemas/**", "**/*spec*.md", ".github/workflows/**"]},
            "reviews": ["rahp", "security", "combined"],
        })
    generated_profile = {
        "version": 1,
        "profile": {"id": "dtg-discovered", "title": "DTG RAHP discovered portfolio", "description": "Generated DTG Working Group RAHP deployment profile. Do not hand edit.", "owner": "DTG RAHP instance"},
        "assessment": {"default_mode": cfg["assessment"].get("default_mode", "combined")},
        "repositories": portable_targets,
        "output": {"directory": "build/targets"},
        "governance": {"namespace": "dtg"},
        "extensions": {"generated_at": datetime.now(timezone.utc).isoformat(), "source_registry": cfg["portfolio"]["registry_repository"], "fork_owner": cfg["portfolio"].get("fork_owner")},
    }
    manifest.write_text(yaml.safe_dump(generated_profile, sort_keys=False), encoding="utf-8")
    print(f"discovered {len(targets)} DTG instance target(s)")
    if args.command == "sync":
        return

    state_path = ROOT / cfg["state"]["file"]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = json.loads(state_path.read_text()) if state_path.exists() else {"version": 1, "repositories": {}}
    events = []
    for target in targets:
        if target.get("self_hosted_instance"):
            continue
        repo = target["repository"]
        old_entry = state["repositories"].get(repo, {})
        old = old_entry.get("sha")
        print(f"checking {repo}@{target['branch']}")
        new = head_sha(repo, target["branch"])
        if new is None:
            state["repositories"][repo] = {**({"sha": old} if old else {}), "status": "no-commits", "observed_at": datetime.now(timezone.utc).isoformat()}
            print(f"warning: {repo}@{target['branch']} has no commit history; skipped until a head revision exists")
            continue
        if not old or args.initialize:
            state["repositories"][repo] = {"sha": new, "status": "active", "observed_at": datetime.now(timezone.utc).isoformat()}
            continue
        if old == new:
            continue
        try:
            comp = compare(repo, old, new)
            classification, matched, reasons = classify(target, comp.get("files", []), cfg, comp.get("commits", []))
        except Exception as exc:
            classification, matched, reasons = "assessment", [], [f"unable to compare prior SHA cleanly; conservative review required ({exc})"]
            comp = {"files": [], "commits": []}
        if classification == "assessment":
            events.append({
                "target": target, "old": old, "new": new, "matched": matched, "reasons": reasons,
                "assessment_key": assessment_key(repo), "source": "repository-change", "repository": repo,
                "event_class": "assessment-required", "title": f"[RAHP review required] {repo}: {old[:7]} → {new[:7]}",
                "body": issue_body(target, old, new, comp, matched, reasons),
                "labels": cfg.get("assessment", {}).get("issue", {}).get("labels", ["assessment-required", "dtg-instance"]),
            })
        elif classification == "triage":
            events.append({
                "target": target, "old": old, "new": new, "matched": matched, "reasons": reasons,
                "assessment_key": f"dtg:classification:{repo}", "source": "repository-change", "repository": repo,
                "event_class": "change-triage", "title": f"[Change triage] {repo}: {old[:7]} → {new[:7]}",
                "body": triage_body(target, old, new, comp, matched, reasons), "labels": ["change-triage", "dtg-instance"],
            })
        state["repositories"][repo] = {"sha": new, "status": "active", "observed_at": datetime.now(timezone.utc).isoformat()}
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    events_path = ROOT / "instances/dtg/generated/review-events.json"
    events_path.write_text(json.dumps(events, indent=2) + "\n")
    print(f"material review event(s): {len(events)}")


if __name__ == "__main__":
    main()
