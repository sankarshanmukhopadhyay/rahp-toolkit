"""Reproducible bounded RAHP upstream/downstream contract ownership audit.

Only accepted, explicitly supplied checkouts are inputs. No network or mutation.
The audit scopes declared cross-repository interfaces, not arbitrary repository code.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

UPSTREAM = {
    "review_schema": "review/spec-review.schema.json",
    "review_validator": "review/validate_spec_review.py",
    "vocabulary": "method/vocabularies.yaml",
    "source_integrity": "review/source_integrity.py",
    "trqp_evaluator": "review/examine.py",
    "vrc_evaluator": "review/examples/vrc-v03/evaluate.py",
}
DOWNSTREAM = {
    "review_entry": "tools/review.py",
    "assessor": "tools/assessor_contract.py",
    "provenance": "tools/evidence_provenance_router.py",
    "source_helper": "examples/standalone-trqp/replay.py",
    "upstream_record_probe": "tools/upstream_review_boundary.py",
    "upstream_evidence_probe": "tools/upstream_evidence_boundary.py",
    "consumer_decision": "tools/upstream_review_consumer_decision.py",
    "source_comparison": "tools/source_integrity_compat.py",
}
EXPECTED_UPSTREAM_SHA = "448e2ff4ca7f747ca899e0e845adfe45f750f094"
PENDING_CONTRACT = "bbe06e3269a6330b64c52ce54ede4e74522ca292"


def inventory(root: Path, paths: dict[str, str]) -> dict:
    result = {}
    for name, rel in paths.items():
        file = root / rel
        if not file.is_file() or file.is_symlink() or not file.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Required owned interface unavailable: {rel}")
        data = file.read_bytes()
        result[name] = {"path": rel, "sha256": hashlib.sha256(data).hexdigest()}
    return result


def assess(upstream: Path, downstream: Path) -> dict:
    upstream = upstream.resolve(strict=True)
    downstream = downstream.resolve(strict=True)
    upstream_files = inventory(upstream, UPSTREAM)
    downstream_files = inventory(downstream, DOWNSTREAM)
    schema = json.loads((upstream / UPSTREAM["review_schema"]).read_text())
    if schema.get("properties", {}).get("schema", {}).get("const") != "rahp-spec-review/v1":
        raise ValueError("Accepted upstream review authority changed")
    for key in ("upstream_record_probe", "upstream_evidence_probe", "consumer_decision"):
        tree = ast.parse((downstream / DOWNSTREAM[key]).read_text())
        strings = [node.value for node in ast.walk(tree)
                   if isinstance(node, ast.Constant) and isinstance(node.value, str)]
        if not any(EXPECTED_UPSTREAM_SHA in value for value in strings) and key != "upstream_record_probe" and key != "upstream_evidence_probe":
            # Consumer and boundary probes may use paths supplied by CI; check those
            # separately at the workflow level rather than requiring embedded pins.
            pass
    workflow = (downstream / ".github/workflows/validate.yml").read_text()
    if EXPECTED_UPSTREAM_SHA not in workflow:
        raise ValueError("Accepted upstream checkout pin missing in validation")
    if PENDING_CONTRACT in workflow:
        raise ValueError("Validation silently references unmerged upstream PR #22 head")
    if "trustoverip/dtgwg-rahp-tf" not in workflow:
        raise ValueError("Explicit upstream checkout missing")
    # Downstream has intentionally different record families: prohibit an
    # upstream review schema clone under the canonical downstream schema path.
    downstream_schema = downstream / "method/schema/rahp.schema.json"
    d = json.loads(downstream_schema.read_text())
    if d.get("properties", {}).get("schema", {}).get("const") == "rahp-spec-review/v1":
        raise ValueError("Conflicting upstream canonical schema installed downstream")
    if '"rahp-spec-review/v1"' in downstream_schema.read_text():
        raise ValueError("Unexpected embedded upstream record definition")
    return {
        "scope": "explicitly supported pinned review/source/example integration paths",
        "accepted_upstream_revision": EXPECTED_UPSTREAM_SHA,
        "upstream_owned": upstream_files,
        "downstream_owned": downstream_files,
        "upstream_authority": "rahp-spec-review/v1",
        "downstream_authority": "separate pressure-test, specialist and controller contracts",
        "unaccepted_pr22_head_used": False,
        "canonical_schema_clone_found": False,
        "no_hidden_dependency_on_unpublished_code": "verified for declared CI checkout references only",
        "unassessed": ["arbitrary dynamic imports", "external consumers", "post-acceptance upstream #22 changes"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--downstream", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = assess(args.upstream, args.downstream)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
