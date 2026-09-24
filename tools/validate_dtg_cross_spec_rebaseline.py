#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "profiles/dtg/cross-spec-tests.yaml"
REBASELINE = ROOT / "instances/dtg/reviews/2026-09-24-cross-spec-rebaseline.yaml"
ALLOWED_JUDGMENTS = {"PASS", "FAIL", "INDETERMINATE", "NOT_APPLICABLE"}
ALLOWED_EVIDENCE = {"verified", "partially_verified", "execution_evidence_pending", "unverified"}

def main() -> int:
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    record = yaml.safe_load(REBASELINE.read_text(encoding="utf-8"))
    expected = {c["id"] for c in registry.get("compositions", []) if c.get("runnable") is True}
    actual = {c["id"] for c in record.get("compositions", [])}
    assert actual == expected, (sorted(expected - actual), sorted(actual - expected))
    assert len(actual) == 8, actual
    pins = record.get("authority_pins", {})
    for c in record["compositions"]:
        assert c["current_judgment"] in ALLOWED_JUDGMENTS, c
        assert c["evidence_state"] in ALLOWED_EVIDENCE, c
        assert c.get("terminal_rationale"), c["id"]
        for repository, sha in c.get("current_pins", {}).items():
            assert pins.get(repository) == sha, (c["id"], repository, sha, pins.get(repository))
        if c["current_judgment"] == "PASS":
            assert c["evidence_state"] == "verified", c
    zkp = record.get("zkp_authority", {})
    assert zkp.get("requirements_and_discussion") == "trustoverip/dtgwg-zkp-tf", zkp
    assert zkp.get("specification_and_conformance") == "trustoverip/dtgwg-zkp-spec", zkp
    summary = record.get("summary", {})
    for judgment in ALLOWED_JUDGMENTS:
        count = sum(c["current_judgment"] == judgment for c in record["compositions"])
        assert summary.get(judgment) == count, (judgment, summary.get(judgment), count)
    assert summary.get("composition_count") == len(actual), summary
    assert summary.get("upstream_defects_proven_by_rebaseline") == 0, summary
    print("DTG 2026-09-24 cross-spec rebaseline: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
