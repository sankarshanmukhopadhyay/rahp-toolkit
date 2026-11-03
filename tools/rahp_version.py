"""Read the declared RAHP stable method release for review provenance.

Never label a newly scaffolded review with an obsolete hard-coded toolkit version.
The declared release is the *method* baseline, not proof that main equals its tag.
"""
from __future__ import annotations

from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSIONING = ROOT / "method" / "versioning.yaml"


def stable_release(path: Path = VERSIONING) -> str:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read RAHP release declaration {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("id") != "rahp-versioning-v1":
        raise ValueError(f"invalid RAHP versioning declaration: {path}")
    release = data.get("stable_release")
    if not isinstance(release, str) or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", release):
        raise ValueError(f"missing or invalid stable_release in {path}")
    return release
