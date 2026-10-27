# Five-minute specification examination demonstration

This is a condensed presentation of the existing [TRQP specification examination](README.md), not a new assessment or a live service test. The source-pinned review, evidence, findings and dispositions remain in their existing authoritative files.

## Run

From the repository root, after `pip install -r requirements.txt`:

```bash
python3 examples/standalone-trqp/demo.py --check
```

The command verifies retained source identity, replays positive and negative schema checks, compares upstream specification examples, and checks the result against `expected-replay.json`. It exits nonzero on unexpected drift. It requires no running TRQP service, specialist, AI model or network access after checkout.

For machine-readable output:

```bash
python3 examples/standalone-trqp/replay.py --check
```

## Four-minute presentation sequence

| Time | Show | Explain |
| --- | --- | --- |
| 0:00–0:40 | `source/api.md.txt` authorization example | The question: what does a schema-valid response establish? |
| 0:40–1:20 | `source/trqp_authorization_response.schema.json` | Required fields do not prove actual authority. |
| 1:20–2:10 | `demo.py --check` output | Source integrity, positive case, negative control and schema-valid example mismatch. |
| 2:10–3:10 | `pressure-test.yaml`, F-001 and F-002 | Separate source observations from reviewer inference and evidence requests. |
| 3:10–4:00 | Final posture and `expected-replay.json` | Replay success is not deployment conformance or independent assurance. |

The retained API example contains a schema-valid response whose requested time differs from its query time; the HTTPS example matches. That supports a bounded documentation clarification request, not a live service defect claim. A constructed response without historical provenance passes the schema but does not prove that deployments lack provenance elsewhere.

## Validation

```bash
python3 examples/standalone-trqp/demo.py --check
python3 -m unittest discover -s tests -p 'test_standalone_trqp_demo.py' -v
python3 tools/validate_pressure_tests.py --file examples/standalone-trqp/pressure-test.yaml
python3 tools/render_pressure_tests.py --check
```

Maintain the source snapshot, review record and expected replay separately. Do not rewrite expected evidence to make a demonstration pass. Keep `REVIEW REQUIRED`, open findings and `NOT ASSESSED` implementation claims visible in any recording. Upstream specification authority is not transferred to RAHP.
