#!/usr/bin/env python3
"""Validate executable VTI lifecycle/freshness pressure vectors."""
from datetime import datetime, timezone
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "examples" / "cross-spec" / "vti-lifecycle-freshness" / "evidence.yaml"


def parse_time(value):
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def evaluate(vector):
    observed = parse_time(vector["observation_time"])
    currency = vector["currency"]
    determined = parse_time(currency.get("determined_at"))
    bound = int(vector["freshness_bound_seconds"])

    if not currency.get("source_entitled") or determined is None:
        return {"outcome": "INDETERMINATE", "effective_state": None}

    age = (observed - determined).total_seconds()
    if age < 0 or age > bound:
        return {"outcome": "INDETERMINATE", "effective_state": None}

    state = currency.get("state")
    if state in {None, "unknown"}:
        return {"outcome": "INDETERMINATE", "effective_state": None}

    return {"outcome": "CURRENT", "effective_state": state}


def main():
    try:
        doc = yaml.safe_load(PATH.read_text(encoding="utf-8"))
        vectors = doc["evidence"]["vectors"]
        if not vectors:
            raise AssertionError("no lifecycle/freshness vectors")
        for vector in vectors:
            actual = evaluate(vector)
            expected = vector["expected"]
            if actual != expected:
                raise AssertionError(
                    f"{vector['id']}: expected {expected!r}, got {actual!r}"
                )
        stale = next(v for v in vectors if v["id"] == "stale-current-state-evidence")
        if stale["historical_artifact"]["state"] != "active":
            raise AssertionError("negative fixture must preserve a last-known active state")
        if evaluate(stale)["effective_state"] is not None:
            raise AssertionError("stale currency must not default to last-known state")
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError, AssertionError) as exc:
        print(f"FAIL VTI lifecycle/freshness: {exc}", file=sys.stderr)
        return 1

    print("PASS VTI lifecycle/freshness")
    print(f"- vectors: {len(vectors)}")
    print("- stale/unknown currency => INDETERMINATE")
    print("- historical cryptographic validity does not override fresh authoritative state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
