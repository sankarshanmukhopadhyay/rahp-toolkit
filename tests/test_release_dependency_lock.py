from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "requirements-release.lock"
RELEASE = ROOT / ".github" / "workflows" / "release.yml"
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"


def _locked_packages():
    text = LOCK.read_text(encoding="utf-8")
    packages = {}
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line and not line.startswith("--"):
            current = line.split("==", 1)[0].lower()
            version = line.split("==", 1)[1].split()[0].rstrip("\\")
            packages[current] = {"version": version, "hashes": []}
        match = re.search(r"--hash=sha256:([0-9a-f]{64})", line)
        if match and current:
            packages[current]["hashes"].append(match.group(1))
    return packages


def test_release_lock_is_exact_and_hash_bearing():
    packages = _locked_packages()
    expected = {
        "pyyaml", "attrs", "et-xmlfile", "jsonschema", "jsonschema-specifications",
        "openpyxl", "referencing", "rpds-py", "typing-extensions",
    }
    assert set(packages) == expected
    assert all(record["version"] and record["hashes"] for record in packages.values())


def test_release_workflow_uses_only_hash_locked_python_set():
    text = RELEASE.read_text(encoding="utf-8")
    assert text.count("--require-hashes --only-binary=:all: -r requirements-release.lock") == 2
    assert text.count("cache-dependency-path: requirements-release.lock") == 2
    assert "pip install -r requirements.txt" not in text


def test_validation_proves_clean_locked_install():
    text = VALIDATE.read_text(encoding="utf-8")
    assert "Prove clean release dependency installation" in text
    assert "--require-hashes --only-binary=:all: -r requirements-release.lock" in text
    assert "release dependency lock imports: PASS" in text


def test_ephemeral_validation_artifacts_use_policy_retention():
    text = VALIDATE.read_text(encoding="utf-8")
    uploads = text.count("uses: actions/upload-artifact@")
    assert uploads >= 3
    assert text.count("retention-days: 14") >= uploads
