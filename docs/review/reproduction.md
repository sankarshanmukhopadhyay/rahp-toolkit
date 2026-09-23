# Independent review reproduction guide

## Goal

Reproduce the stable RAHP validation boundary from a clean checkout without importing prior `.rahp/` working state or treating CI success as assurance success.

## Baseline

- stable toolkit: `v2.4.0`
- default branch: `main`
- CI Python: `3.11`
- engine: `rahp-engine-contract-v1` revision `1.3`
- result schema: `1`
- evidence retention: `rahp-evidence-retention-v1`

For historical review, check out the immutable tag or commit being reviewed rather than assuming current `main`.

## Clean execution

```bash
git clone https://github.com/sankarshanmukhopadhyay/rahp-toolkit.git
cd rahp-toolkit
git checkout v2.4.0
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python3 tools/validate.py
python3 tools/validate_engine_contract.py
python3 tools/validate_negative_fixtures.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

For the post-v2.4 review-readiness material itself, repeat against the exact review-candidate commit once one is qualified.

## Intentionally non-positive reproduction

The negative-fixture validator is expected to preserve deficient material evidence as a non-positive outcome. Reviewers should also inspect `method/review/false-assurance-challenges.yaml` and independently mutate inputs rather than relying only on maintained fixtures.

## Record

A reproducibility report should record OS/container image, Python version, exact Git commit, `pip freeze`, commands executed, exit codes, relevant generated outputs, network access required, and any nondeterminism. Preserve logs as review artifacts; do not infer assurance from an exit code.

## Current reproducibility bound

The project does not currently claim bit-for-bit dependency reproduction because `requirements.txt` uses minimum-version constraints. This is a declared residual, not silently normalized away.

## CI clean-runner evidence

The governed `validate` workflow repeats the reviewer minimum path on a fresh GitHub-hosted Ubuntu runner with Python 3.11 and emits the `rahp-independent-review-reproduction` artifact. It records the commit, runner OS, Python/pip versions, resolved `pip freeze`, and review-validation command output. This is environment/reproduction evidence, not an assurance result and not a claim of bit-for-bit dependency reproducibility.
