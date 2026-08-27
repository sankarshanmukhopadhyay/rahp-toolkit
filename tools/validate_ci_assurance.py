#!/usr/bin/env python3
"""Validate repository-wide ownership of RAHP CI assurance propositions."""
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = ROOT / "method" / "ci-assurance-propositions.yaml"
WORKFLOWS = ROOT / ".github" / "workflows"
PROPOSITION_ID = "python_typescript_conformance"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def load() -> dict:
    data = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    if data.get("id") != "rahp-ci-assurance-propositions-v1":
        fail("unexpected CI assurance policy id")
    proposition = (data.get("propositions") or {}).get(PROPOSITION_ID)
    if not isinstance(proposition, dict):
        fail(f"missing proposition {PROPOSITION_ID}")
    return proposition


def require_text(text: str, needle: str, context: str) -> None:
    if needle not in text:
        fail(f"{context} missing required contract marker: {needle}")


def main() -> int:
    p = load()
    required_keys = {
        "owner_workflow", "classifier", "repository_validator", "conformance_validator",
        "conditional_events", "full_backstop_events", "release_workflow", "release_mode",
        "fail_safe", "affected_paths",
    }
    missing = sorted(required_keys - set(p))
    if missing:
        fail("proposition missing keys: " + ", ".join(missing))
    if p["release_mode"] != "unconditional" or p["fail_safe"] != "required":
        fail("release_mode must be unconditional and fail_safe must be required")
    if set(p["conditional_events"]) != {"pull_request", "push"}:
        fail("conditional events must be pull_request and push")
    if set(p["full_backstop_events"]) != {"schedule", "workflow_dispatch"}:
        fail("full backstop events must be schedule and workflow_dispatch")

    owner = ROOT / p["owner_workflow"]
    release = ROOT / p["release_workflow"]
    classifier = ROOT / p["classifier"]
    repo_validator = ROOT / p["repository_validator"]
    conformance = ROOT / p["conformance_validator"]
    for path in (owner, release, classifier, repo_validator, conformance):
        if not path.exists():
            fail(f"declared CI assurance path does not exist: {path.relative_to(ROOT)}")

    affected = set(p["affected_paths"])
    governance_paths = {
        str(POLICY_PATH.relative_to(ROOT)),
        str(classifier.relative_to(ROOT)),
        str(repo_validator.relative_to(ROOT)),
        str(conformance.relative_to(ROOT)),
        str(owner.relative_to(ROOT)),
        str(release.relative_to(ROOT)),
    }
    absent = sorted(governance_paths - affected)
    if absent:
        fail("governance paths must force conformance: " + ", ".join(absent))

    owner_text = owner.read_text(encoding="utf-8")
    release_text = release.read_text(encoding="utf-8")
    require_text(owner_text, "tools/typescript_ci_impact.py", "owner workflow")
    require_text(owner_text, "--full", "owner workflow")
    require_text(owner_text, "schedule:", "owner workflow")
    require_text(owner_text, "workflow_dispatch:", "owner workflow")
    require_text(owner_text, "name: TypeScript conformance", "owner workflow")
    require_text(owner_text, "python3 tools/validate_typescript_sdk.py", "owner workflow")
    require_text(release_text, "Require Python-TypeScript conformance for release publication", "release workflow")
    require_text(release_text, "python3 tools/validate_typescript_sdk.py", "release workflow")
    if "tools/typescript_ci_impact.py" in release_text:
        fail("release workflow must not classify away TypeScript conformance")

    owners = []
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        if "tools/validate_typescript_sdk.py" in text:
            owners.append(str(workflow.relative_to(ROOT)))
    allowed = {p["owner_workflow"], p["release_workflow"]}
    if set(owners) != allowed:
        fail(f"cross-runtime conformance workflow ownership drift: found {owners}, expected {sorted(allowed)}")

    validate_workflow = owner_text
    require_text(validate_workflow, "python3 tools/validate_ci_assurance.py", "owner workflow")

    print("PASS repository-wide CI assurance proposition contract")
    print(f"  proposition: {PROPOSITION_ID}")
    print(f"  conditional owner: {p['owner_workflow']}")
    print(f"  unconditional release backstop: {p['release_workflow']}")
    print(f"  affected path patterns: {len(p['affected_paths'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
