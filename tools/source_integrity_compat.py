"""Compare bounded source-identity behavior in two trusted RAHP checkouts.

The result is comparative evidence, not a target-assurance conclusion.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path


def load_function(path: Path, name: str):
    if not path.is_file():
        raise FileNotFoundError(f"Required source missing: {path}")
    spec = importlib.util.spec_from_file_location("rahp_probe_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, name)


def fixture(root: Path, variant: str) -> None:
    data = b"retained source fixture\n"
    (root / "source").mkdir()
    (root / "source/spec.md.txt").write_bytes(data)
    blob = b"blob " + str(len(data)).encode() + b"\0" + data
    commit = "a" * 40
    entry = {
        "path": "source/spec.md.txt", "upstream_path": "spec.md",
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob_sha": hashlib.sha1(blob).hexdigest(),
        "url": f"https://github.com/example/target/blob/{commit}/spec.md",
    }
    if variant == "bad_hash":
        entry["sha256"] = "0" * 64
    elif variant == "bad_url":
        entry["url"] = f"https://github.com/example/other/blob/{commit}/spec.md"
    elif variant == "unsafe_path":
        entry["path"] = "../outside.txt"
    records = [entry, dict(entry)] if variant == "duplicate" else [entry]
    (root / "source-manifest.json").write_text(json.dumps({
        "repository": "example/target", "commit": commit, "files": records
    }), encoding="utf-8")


def outcome(check, root: Path) -> str:
    try:
        check(root)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError):
        return "rejected"
    return "accepted"


def compare(upstream: Path, downstream: Path) -> dict:
    checks = {
        "upstream": load_function(upstream / "review/source_integrity.py", "verify_source"),
        "downstream": load_function(downstream / "examples/standalone-trqp/replay.py", "source_integrity"),
    }
    results = []
    for scenario in ("valid", "bad_hash", "bad_url", "duplicate", "unsafe_path"):
        with tempfile.TemporaryDirectory(prefix="rahp-source-compat-") as temp:
            root = Path(temp)
            fixture(root, scenario)
            verdicts = {name: outcome(fn, root) for name, fn in checks.items()}
            results.append({"scenario": scenario, **verdicts,
                            "classification": ("compatible" if len(set(verdicts.values())) == 1
                                               else "adaptation_required")})
    return {"scope": "retained-source helper behavior only",
            "not_claimed": ["review schema equivalence", "lifecycle equivalence", "target assurance"],
            "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--downstream", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(compare(args.upstream, args.downstream), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
