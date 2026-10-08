"""Guard the documented reasoning modes and local code references."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDES = [
    ROOT / "docs/reasoning-architecture.md",
    ROOT / "docs/reasoning-integration.md",
    ROOT / "docs/reasoning-trace.md",
    ROOT / "examples/standalone-trqp/README.md",
]


class ReasoningDocumentationTests(unittest.TestCase):
    def test_all_local_markdown_links_resolve(self):
        for doc in GUIDES:
            text = doc.read_text()
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("http:", "https:", "#", "mailto:", "/rahp-toolkit/")):
                    continue
                with self.subTest(doc=str(doc.relative_to(ROOT)), target=target):
                    relative = target.split("#", 1)[0]
                    self.assertTrue((doc.parent / relative).exists(), target)

    def test_entry_points_and_example_are_connected(self):
        for file in ["README.md", "docs/how-rahp-works.md", "examples/standalone-trqp/README.md"]:
            text = (ROOT / file).read_text()
            self.assertIn("reasoning-architecture.md", text)
            self.assertIn("reasoning-integration.md", text)

    def test_no_agent_dependency_claim(self):
        text = (ROOT / "docs/reasoning-architecture.md").read_text()
        self.assertIn("does not require an AI agent", text)
        self.assertIn("not automatically evidence", text)


if __name__ == "__main__":
    unittest.main()
