from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sync_dtg_profile", ROOT / "tools" / "sync_dtg_profile.py")
sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sync)


def target(repo="trustoverip/example", role="normative-specification", paths=None):
    return {
        "id": repo.lower().replace("/", "-"),
        "repository": repo,
        "branch": "main",
        "source": "portfolio-monitor",
        "upstream": None,
        "workstream": "example",
        "role": role,
        "lifecycle": "active",
        "reporting_weight": "critical",
        "material_paths": paths or ["README.md", "spec/**"],
    }


def test_portable_target_preserves_authoritative_portfolio_metadata():
    item = sync.portable_target(target())
    assert item["repository"] == "trustoverip/example"
    assert item["context"]["type"] == "normative-specification"
    assert "reporting_weight=critical" in item["context"]["description"]
    assert item["scope"]["include"] == ["README.md", "spec/**"]
    assert item["reviews"] == ["rahp", "security", "combined"]


def test_diff_detects_missing_repository():
    expected = [sync.portable_target(target())]
    profile = {"repositories": []}
    assert "missing repository: trustoverip/example" in sync.diff(profile, expected)


def test_diff_detects_role_or_scope_drift():
    expected = [sync.portable_target(target())]
    drifted = {"repositories": [sync.portable_target(target(role="task-force-workspace"))]}
    assert "metadata drift: trustoverip/example" in sync.diff(drifted, expected)


def test_diff_accepts_exact_authoritative_projection():
    expected = [
        sync.portable_target(target("trustoverip/a")),
        sync.portable_target(target("trustoverip/b", role="implementation")),
    ]
    assert sync.diff({"repositories": expected}, expected) == []


def test_diff_detects_order_drift_for_reproducible_snapshots():
    expected = [
        sync.portable_target(target("trustoverip/a")),
        sync.portable_target(target("trustoverip/b")),
    ]
    assert "repository ordering drift" in sync.diff({"repositories": list(reversed(expected))}, expected)
