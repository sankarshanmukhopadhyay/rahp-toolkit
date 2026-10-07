import pathlib
import unittest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


class TestPagesProjectionContract(unittest.TestCase):
    def test_onboarding_sources_are_jekyll_pages_for_link_rewriting(self):
        for directory in ("examples", "examples/hello-rahp", "examples/standalone-trqp"):
            with self.subTest(directory=directory):
                source = (ROOT / directory / "README.md").read_text()
                self.assertTrue(source.startswith("---\n"), "Source links must resolve to a Jekyll page, not raw Markdown")
                front_matter = yaml.safe_load(source.split("---", 2)[1])
                self.assertEqual(front_matter["layout"], "default")
                self.assertEqual(front_matter["permalink"], f"/{directory}/")

    def test_cawg_mandate_readiness_is_projected_from_instances(self):
        plugin = (ROOT / "_plugins" / "structured_data_pages.rb").read_text()
        validator = (ROOT / "tools" / "validate_jtd_site.py").read_text()
        self.assertIn("instances/cawg/mandate-readiness.yaml", plugin)
        self.assertIn("instances/cawg/mandate-readiness.yaml", validator)
        self.assertIn("instances/cawg/watch/issues.yaml", plugin)
        self.assertIn("instances/dtg/watch/issues.yaml", plugin)
        self.assertIn("instances/cawg/watch/issues.yaml", validator)
        self.assertIn("instances/dtg/watch/issues.yaml", validator)

    def test_cawg_docs_link_to_projected_readme_not_directory(self):
        for rel in ("docs/cawg-instance.md", "docs/cawg-mandate-readiness.md"):
            text = (ROOT / rel).read_text()
            self.assertNotIn("(../examples/cawg-c2pa/)", text)
            self.assertIn("../examples/cawg-c2pa/README.md", text)

    def test_a2a_and_persona_surfaces_are_required_pages_coverage(self):
        validator = (ROOT / "tools" / "validate_jtd_site.py").read_text()
        plugin = (ROOT / "_plugins" / "structured_data_pages.rb").read_text()
        for required in (
            "docs/a2a-example.html",
            "docs/personas.html",
            "examples/a2a/index.html",
            "examples/a2a/pressure-test.yaml",
        ):
            self.assertIn(required, validator)
        a2a_source = (ROOT / "examples/a2a/README.md").read_text()
        self.assertIn("permalink: /examples/a2a/", a2a_source)
        self.assertIn('parsed["review"]', plugin)
        self.assertIn("review_summary", plugin)

    def test_pressure_test_renderer_uses_directory_aware_catalogue_links(self):
        renderer = (ROOT / "tools" / "render_pressure_tests.py").read_text()
        self.assertIn("set_catalogue_relative", renderer)
        self.assertIn("os.path.relpath", renderer)
        self.assertIn('ROOT / "build/site/catalogue.html"', renderer)


if __name__ == "__main__":
    unittest.main()
