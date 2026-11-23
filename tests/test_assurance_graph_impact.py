import unittest
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from impact import analyze  # noqa: E402


class AssuranceGraphImpactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = yaml.safe_load((ROOT / "examples" / "assurance-lineage" / "generic-assurance-graph.yaml").read_text())

    def test_target_change_selects_assessment(self):
        result = analyze(self.graph, ["target:payments-api"])
        self.assertIn("example:specification:payments-api", result["retest_required"])

    def test_control_change_propagates_to_test_evidence_and_assessment(self):
        result = analyze(self.graph, ["control:authorization-check"])
        ids = {item["id"] for item in result["affected_nodes"]}
        self.assertIn("test:authorization-revoked", ids)
        self.assertIn("evidence:test-run", ids)
        self.assertIn("assessment:payments-auth", ids)

    def test_unknown_node_is_reported_without_false_impact(self):
        result = analyze(self.graph, ["unknown:thing"])
        self.assertEqual([], result["affected_nodes"])
        self.assertEqual(["unknown:thing"], result["unresolved_changed_nodes"])
        self.assertEqual([], result["retest_required"])

    def test_selected_assessment_has_real_directed_path_from_change(self):
        result = analyze(self.graph, ["target:payments-api"])
        by_id = {node["id"]: node for node in result["affected_nodes"]}
        selected = by_id["assessment:payments-auth"]
        self.assertEqual(selected["distance"], 2)
        self.assertEqual(selected["via"], ["e1", "e5"])
        edges = {edge["id"]: edge for edge in self.graph["edges"]}
        cursor = "target:payments-api"
        for edge_id in selected["via"]:
            edge = edges[edge_id]
            direction = edge["impact_propagation"]
            if cursor == edge["source"]:
                self.assertIn(direction, ("source-to-target", "both"))
                cursor = edge["target"]
            else:
                self.assertEqual(cursor, edge["target"])
                self.assertIn(direction, ("target-to-source", "both"))
                cursor = edge["source"]
        self.assertEqual(cursor, selected["id"])
        self.assertEqual(len(selected["via"]), selected["distance"])
        self.assertEqual(result["retest_required"], ["example:specification:payments-api"])

    def test_known_and_unresolved_changed_nodes_do_not_hide_uncertainty(self):
        result = analyze(self.graph, ["target:payments-api", "unknown:external-policy"])
        self.assertEqual(result["unresolved_changed_nodes"], ["unknown:external-policy"])
        self.assertIn("example:specification:payments-api", result["retest_required"])
        # A valid observed path does not establish complete graph coverage.
        self.assertIn("Impact is graph-reachability evidence, not an assurance conclusion.",
                      result["notes"])

    def test_unrepresented_dependency_is_not_inferred_as_no_effect(self):
        from copy import deepcopy
        incomplete = deepcopy(self.graph)
        incomplete["edges"] = [
            edge for edge in incomplete["edges"] if edge["id"] != "e5"
        ]
        result = analyze(incomplete, ["target:payments-api"])
        # There remains a longer path through control/test/evidence.
        node = next(x for x in result["affected_nodes"]
                    if x["id"] == "assessment:payments-auth")
        self.assertEqual(node["via"], ["e1", "e2", "e3", "e4", "e6"])
        self.assertEqual(node["distance"], 5)
        incomplete["edges"] = [
            edge for edge in incomplete["edges"] if edge["id"] != "e6"
        ]
        no_path = analyze(incomplete, ["target:payments-api"])
        self.assertEqual(no_path["retest_required"], [])
        # This is an epistemic limit of graph reachability, not a finding
        # of no material impact. Completeness must be independently assessed.
        self.assertEqual(no_path["unresolved_changed_nodes"], [])

    def test_impact_is_deterministic(self):
        first = analyze(self.graph, ["target:payments-api"])
        second = analyze(self.graph, ["target:payments-api"])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
