"""Exercise the supported read-only external result CLI, not internal-only helpers."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_evidence_producer_result import PIN, valid_result
from tools.validate_external_assurance_result import diagnose

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/validate_external_assurance_result.py"


def obligation():
    return {
        "schema": "rahp-assurance-obligation/v1",
        "proposition_key": "rahp-obligation:" + "c" * 20,
        "evidence_contract_key": "rahp-evidence-contract:" + "d" * 20,
        "state": "evidence-acquirable",
        "action_owner": {"surface": "evidence-producer"},
        "artifact_to_produce": {"kind": "runtime-evidence", "description": "bounded observation"},
        "producer": {"mode": "registered-executable", "id": "example-producer-v1"},
        "lineage": [],
        "evidence_requirement_ids": ["ER-EXAMPLE-AB"],
        "source_pins": [PIN],
    }


def assessor():
    return {
        "schema": "rahp-assessor-result/v1",
        "assessor": "independent-example",
        "assessment_id": "rahp:assess-1",
        "outcome": "INDETERMINATE",
        "reason_code": "evidence-required",
        "evidence_used": ["ER-EXAMPLE-AB"],
        "residual_risk": "Deployment behavior is unverified.",
        "action_required": "Obtain a bounded runtime observation.",
        "source_pins": [PIN],
    }


class ExternalAssuranceCliTests(unittest.TestCase):
    def cli(self, *, kind="producer", result=None, context=True, previous=None, expected_id=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "return.json").write_text(json.dumps(
                valid_result() if result is None else result), encoding="utf-8")
            args = [sys.executable, str(CLI), "--kind", kind,
                    "--result", str(root / "return.json")]
            if context:
                (root / "obligation.json").write_text(json.dumps(obligation()), encoding="utf-8")
                args += ["--obligation", str(root / "obligation.json")]
            if previous is not None:
                (root / "previous.json").write_text(json.dumps(previous), encoding="utf-8")
                args += ["--previous-result", str(root / "previous.json")]
            if expected_id is not None:
                args += ["--expected-assessment-id", expected_id]
            process = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=30)
            return process.returncode, json.loads(process.stdout)

    def test_producer_valid_contract_bound_but_not_authenticated(self):
        code, report = self.cli()
        self.assertEqual(code, 0, report)
        self.assertEqual(report["status"], "VALID_BOUND_CONTRACT")
        self.assertEqual(report["contract"], "rahp-evidence-producer-result/v1")
        self.assertIs(report["authenticated"], False)
        self.assertIsNone(report["assurance_determination"])

    def test_wrong_proposition_revision_and_requirements_rejected(self):
        for mutation in ("proposition", "revision", "requirement"):
            with self.subTest(mutation=mutation):
                data = copy.deepcopy(valid_result())
                if mutation == "proposition":
                    data["obligation"]["proposition_key"] = "rahp-obligation:" + "f" * 20
                elif mutation == "revision":
                    data["source"]["pins"][0]["revision"] = "f" * 40
                    data["freshness"]["valid_against"][0]["revision"] = "f" * 40
                else:
                    data["obligation"]["evidence_requirement_ids"] = ["UNRELATED"]
                code, report = self.cli(result=data)
                self.assertNotEqual(code, 0)
                self.assertEqual(report["status"], "REJECTED_BINDING")

    def test_missing_context_and_unavailable_evidence_are_not_success(self):
        for kwargs in ({"context": False}, {"result": self.unavailable()}):
            code, report = self.cli(**kwargs)
            self.assertNotEqual(code, 0)
            self.assertEqual(report["status"], "NOT_ESTABLISHED")

    @staticmethod
    def unavailable():
        data = valid_result()
        data["execution"]["status"] = "unavailable"
        data["evidence"]["status"] = "evidence-incomplete"
        data["evidence"]["artifacts"] = []
        data["evidence"]["observations"] = []
        data["claim_boundary"]["supports"] = []
        return data

    def test_duplicate_and_conflicting_retries_fail_closed(self):
        old = valid_result()
        duplicated = copy.deepcopy(old)
        altered = copy.deepcopy(old)
        altered["evidence"]["artifacts"][0]["sha256"] = "f" * 64
        for data in (duplicated, altered):
            code, report = self.cli(result=data, previous=old)
            self.assertNotEqual(code, 0)
            self.assertEqual(report["status"], "REJECTED_BINDING")
            self.assertTrue(any("return" in error for error in report["errors"]))

    def test_unknown_version_and_malformed_return_rejected(self):
        data = valid_result()
        data["schema"] = "rahp-evidence-producer-result/v2"
        code, report = self.cli(result=data)
        self.assertNotEqual(code, 0)
        self.assertEqual(report["status"], "INVALID_CONTRACT")
        code, report = self.cli(result=[])
        self.assertNotEqual(code, 0)
        self.assertEqual(report["status"], "INVALID_INPUT")

    def test_assessor_context_misbinding_and_non_authorization(self):
        code, report = self.cli(kind="assessor", result=assessor(), expected_id="rahp:assess-1")
        self.assertEqual(code, 0, report)
        self.assertIsNone(report["assurance_determination"])
        self.assertIs(report["authenticated"], False)
        code, report = self.cli(kind="assessor", result=assessor())
        self.assertNotEqual(code, 0)
        self.assertEqual(report["status"], "NOT_ESTABLISHED")
        code, report = self.cli(kind="assessor", result=assessor(), expected_id="wrong-assessment")
        self.assertNotEqual(code, 0)
        self.assertEqual(report["status"], "REJECTED_BINDING")

    def test_assessor_unrelated_evidence_and_positive_claim_do_not_authorize(self):
        data = assessor()
        data["evidence_used"] = ["NOT-OUR-OBLIGATION"]
        code, report = self.cli(kind="assessor", result=data, expected_id="rahp:assess-1")
        self.assertNotEqual(code, 0)
        self.assertEqual(report["status"], "REJECTED_BINDING")
        data = assessor()
        data["outcome"] = "PASS"
        code, report = self.cli(kind="assessor", result=data, expected_id="rahp:assess-1")
        self.assertEqual(code, 0, report)
        self.assertIsNone(report["assurance_determination"])


if __name__ == "__main__":
    unittest.main()
