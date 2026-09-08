from tools.capability_coverage import completeness, validate


def record(**overrides):
    proposition = {
        "id": "P-EX-001",
        "pattern": "context-isolation",
        "provider": "rahp",
        "judgment": "SATISFIED",
        "evidence_required": ["negative access evidence"],
        "evidence": [{"source": "example", "revision": "abc123"}],
        "assessed_at_maturity": "implementation",
    }
    proposition.update(overrides.pop("proposition", {}))
    coverage = {"id": "example", "subject": "example", "maturity": "implementation", "propositions": [proposition]}
    coverage.update(overrides)
    return {"coverage": coverage}


def test_valid_coverage_and_completeness():
    doc = record()
    assert validate(doc) == []
    assert completeness(doc)["satisfied"] == 1


def test_missing_and_duplicate_ids_are_rejected():
    doc = record()
    doc["coverage"]["propositions"].append(dict(doc["coverage"]["propositions"][0]))
    assert any("duplicate proposition id" in e for e in validate(doc))
    doc = record(proposition={"id": ""})
    assert any("missing id" in e for e in validate(doc))


def test_unknown_maturity_judgment_provider_are_rejected():
    assert any("unknown maturity" in e for e in validate(record(maturity="imaginary")))
    assert any("unknown judgment" in e for e in validate(record(proposition={"judgment": "PASS"})))
    assert any("unknown provider" in e for e in validate(record(proposition={"provider": "magic"})))


def test_missing_evidence_cannot_satisfy():
    errors = validate(record(proposition={"evidence": []}))
    assert any("SATISFIED without required evidence" in e for e in errors)


def test_maturity_cannot_be_implicitly_promoted():
    errors = validate(record(proposition={"assessed_at_maturity": "architectural"}))
    assert any("cannot promote" in e for e in errors)


def test_evidence_required_is_explicit_not_pass():
    doc = record(proposition={"judgment": "EVIDENCE_REQUIRED", "evidence": []})
    assert validate(doc) == []
    summary = completeness(doc)
    assert summary["evidence_required"] == 1
    assert summary["satisfied"] == 0
