#!/usr/bin/env python3
"""Validate the RAHP-only GitHub issue publication boundary."""
from __future__ import annotations

import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "sankarshanmukhopadhyay/rahp-toolkit"
errors: list[str] = []

# Deployment configs must point assessment publication at RAHP itself.
for rel in ("instances/dtg/instance.yaml", "instances/cawg/instance.yaml"):
    path = ROOT / rel
    data = yaml.safe_load(path.read_text())
    configured = (data.get("assessment") or {}).get("issue", {}).get("repository")
    review = (data.get("instance") or {}).get("review_repository")
    if configured != CANONICAL:
        errors.append(f"{rel}: assessment.issue.repository must be {CANONICAL}, got {configured!r}")
    if review != CANONICAL:
        errors.append(f"{rel}: instance.review_repository must be {CANONICAL}, got {review!r}")

# Every workflow invocation of the sole publisher must use the canonical destination.
workflow_dir = ROOT / ".github" / "workflows"
for path in sorted(workflow_dir.glob("*.y*ml")):
    text = path.read_text()
    if "publish_assessment_issues.py" in text:
        calls = text.split("publish_assessment_issues.py")[1:]
        for idx, tail in enumerate(calls, 1):
            fragment = tail[:600]
            # A standalone preflight reads event files and cannot issue GitHub writes.
            # Actual publication invocations must retain the canonical destination.
            if re.match(r"^--(?:check-transfers|verify-transfer-rollback)(?:\s|$)", fragment.lstrip()):
                continue
            if f'--repository "{CANONICAL}"' not in fragment:
                errors.append(f"{path.relative_to(ROOT)} publisher call {idx}: canonical --repository is required")
    # Guard against direct gh issue creation or direct GitHub issue API POSTs in workflows.
    if re.search(r"\bgh\s+issue\s+create\b", text):
        errors.append(f"{path.relative_to(ROOT)}: direct `gh issue create` is forbidden; use the RAHP publisher")
    if re.search(r"api\.github\.com/repos/.+/issues", text):
        errors.append(f"{path.relative_to(ROOT)}: direct GitHub issues API usage is forbidden")

# Publisher constant is itself part of the invariant.
publisher = (ROOT / "tools" / "publish_assessment_issues.py").read_text()
if f'CANONICAL_RAHP_ISSUE_REPOSITORY = "{CANONICAL}"' not in publisher:
    errors.append("tools/publish_assessment_issues.py: canonical RAHP issue repository constant missing or changed")

if errors:
    for error in errors:
        print("ERROR", error)
    raise SystemExit(f"RAHP issue-publication policy validation failed: {len(errors)} error(s)")

print(f"RAHP issue-publication policy clean: automated issues are confined to {CANONICAL}.")
