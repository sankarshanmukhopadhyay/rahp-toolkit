#!/usr/bin/env python3
"""Fetch the newest recent DTG Portfolio Monitor findings snapshot.

A missing same-day snapshot is treated as publication latency. The consumer searches a
small, explicit UTC lookback window and records the actual snapshot date consumed. If no
snapshot exists in that window, the workflow fails rather than silently consuming stale
or absent evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from typing import Callable

BASE_URL = "https://raw.githubusercontent.com/sankarshanmukhopadhyay/dtg-portfolio-monitor/main/data/findings"
DEFAULT_LOOKBACK_DAYS = 2


def snapshot_url(day: date) -> str:
    return f"{BASE_URL}/{day:%Y/%m/%d}.json"


def fetch_latest(
    today: date,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    opener: Callable[..., object] = urllib.request.urlopen,
) -> tuple[date, str, list[object], int]:
    if lookback_days < 0:
        raise ValueError("lookback_days must be non-negative")

    for age in range(lookback_days + 1):
        candidate = today - timedelta(days=age)
        url = snapshot_url(candidate)
        try:
            with opener(url, timeout=30) as response:  # type: ignore[attr-defined]
                findings = json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            raise

        if not isinstance(findings, list):
            raise ValueError(f"Portfolio Monitor snapshot must be a JSON array: {url}")
        return candidate, url, findings, age

    raise FileNotFoundError(
        f"No DTG Portfolio Monitor snapshot exists within {lookback_days} day(s) of {today.isoformat()}"
    )


def self_test() -> int:
    class Response:
        def __init__(self, payload: object):
            self.payload = payload
        def __enter__(self):
            import io
            return io.StringIO(json.dumps(self.payload))
        def __exit__(self, *_args):
            return False

    calls: list[str] = []
    wanted = date(2026, 9, 7)

    def delayed(url: str, timeout: int = 30):
        del timeout
        calls.append(url)
        if url.endswith("/2026/09/07.json"):
            raise urllib.error.HTTPError(url, 404, "missing", hdrs=None, fp=None)
        if url.endswith("/2026/09/06.json"):
            return Response([{"finding_id": "x"}])
        raise AssertionError(url)

    day, url, findings, age = fetch_latest(wanted, 2, delayed)
    assert day == date(2026, 9, 6)
    assert age == 1
    assert findings == [{"finding_id": "x"}]
    assert url.endswith("/2026/09/06.json")
    assert len(calls) == 2

    def absent(url: str, timeout: int = 30):
        del timeout
        raise urllib.error.HTTPError(url, 404, "missing", hdrs=None, fp=None)

    try:
        fetch_latest(wanted, 1, absent)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("bounded lookback must fail when every candidate is absent")

    try:
        fetch_latest(wanted, -1, absent)
    except ValueError:
        pass
    else:
        raise AssertionError("negative lookback must be rejected")

    print("PASS DTG snapshot fetch: bounded publication-latency fallback")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--lookback-days", type=int, default=DEFAULT_LOOKBACK_DAYS)
    parser.add_argument("--output", default="build/dtg-routing/findings.json")
    parser.add_argument("--github-output", default=os.getenv("GITHUB_OUTPUT", ""))
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    today = datetime.now(timezone.utc).date()
    try:
        day, url, findings, age = fetch_latest(today, args.lookback_days)
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(findings, indent=2) + "\n", encoding="utf-8")

    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as out:
            out.write(f"date={day.isoformat()}\n")
            out.write(f"url={url}\n")
            out.write(f"age_days={age}\n")

    if age:
        print(
            f"NOTICE: today's Portfolio Monitor snapshot is not yet available; "
            f"using {day.isoformat()} ({age} day(s) old): {url}"
        )
    else:
        print(f"Fetched current Portfolio Monitor snapshot {day.isoformat()}: {url}")
    print(f"Fetched {len(findings)} findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
