import ast
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_jtd_site.py"


def literal_assignment(name):
    tree = ast.parse(VALIDATOR.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found")


def materialize_common_site(site: pathlib.Path):
    html = "<!doctype html><html><body>ok</body></html>"
    themed = '<!doctype html><html><body><main id="main-content">ok</main></body></html>'

    for rel in literal_assignment("REQUIRED_DOCS"):
        p = site / rel
        if pathlib.Path(rel).suffix == ".md":
            p = p.with_suffix(".md.html")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(html, encoding="utf-8")

    # Canonical structured-data paths must remain structured data, not HTML.
    for rel in literal_assignment("REQUIRED_STRUCTURED_SOURCES"):
        p = site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith((".yaml", ".yml")):
            p.write_text("record_type: fixture\nrecords: []\n", encoding="utf-8")
        else:
            p.write_text('{"fixture": true}\n', encoding="utf-8")

    for rel in literal_assignment("REQUIRED_HUMAN_PROJECTIONS"):
        p = site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(themed, encoding="utf-8")

    for rel in literal_assignment("REQUIRED_JTD_SHELL"):
        p = site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(themed, encoding="utf-8")

    return html, themed


class TestJtdBaseUrlRegression(unittest.TestCase):
    def test_standalone_onboarding_routes_require_rendered_shell(self):
        routes = (
            "examples/index.html",
            "examples/hello-rahp/index.html",
            "examples/standalone-trqp/index.html",
        )
        required = literal_assignment("REQUIRED_JTD_SHELL")
        for route in routes:
            self.assertIn(route, required)
            with self.subTest(route=route), tempfile.TemporaryDirectory() as td:
                site = pathlib.Path(td)
                materialize_common_site(site)
                (site / route).write_text("# Raw Markdown is not a rendered page\n")
                run = subprocess.run([sys.executable, str(VALIDATOR), str(site)], cwd=ROOT, capture_output=True, text=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertIn("missing Just-the-Docs shell", run.stdout)

    def test_rahp_toolkit_baseurl_links_resolve_from_site_root(self):
        with tempfile.TemporaryDirectory() as td:
            site = pathlib.Path(td)
            html, _ = materialize_common_site(site)
            target = site / "docs" / "baseurl-target.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding="utf-8")
            source = site / "docs" / "baseurl-source.html"
            source.write_text('<!doctype html><html><body><a href="/rahp-toolkit/docs/baseurl-target.html">target</a></body></html>', encoding="utf-8")
            run = subprocess.run([sys.executable, str(VALIDATOR), str(site)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_bare_html_fragment_is_rejected_for_themed_route(self):
        with tempfile.TemporaryDirectory() as td:
            site = pathlib.Path(td)
            _, themed = materialize_common_site(site)
            shell_routes = literal_assignment("REQUIRED_JTD_SHELL")
            broken = site / shell_routes[0]
            broken.write_text('<h1>bare fragment</h1>', encoding="utf-8")
            run = subprocess.run([sys.executable, str(VALIDATOR), str(site)], cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("missing Just-the-Docs shell", run.stdout)

    def test_structured_source_cannot_be_replaced_by_html(self):
        with tempfile.TemporaryDirectory() as td:
            site = pathlib.Path(td)
            materialize_common_site(site)
            source_rel = literal_assignment("REQUIRED_STRUCTURED_SOURCES")[0]
            source = site / source_rel
            source.write_text('<!doctype html><html><body>wrong surface</body></html>', encoding="utf-8")
            run = subprocess.run([sys.executable, str(VALIDATOR), str(site)], cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("canonical structured source was replaced by HTML", run.stdout)

    def test_human_projection_requires_jtd_shell(self):
        with tempfile.TemporaryDirectory() as td:
            site = pathlib.Path(td)
            materialize_common_site(site)
            projection_rel = literal_assignment("REQUIRED_HUMAN_PROJECTIONS")[0]
            projection = site / projection_rel
            projection.write_text('<!doctype html><html><body>bare projection</body></html>', encoding="utf-8")
            run = subprocess.run([sys.executable, str(VALIDATOR), str(site)], cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("human-readable projection missing Just-the-Docs shell", run.stdout)

    def test_markdown_projection_keeps_sibling_relative_links_in_source_directory(self):
        with tempfile.TemporaryDirectory() as td:
            site = pathlib.Path(td)
            materialize_common_site(site)
            review_dir = site / "examples" / "security-hardening" / "fixture"
            review_dir.mkdir(parents=True, exist_ok=True)
            (review_dir / "findings.yaml").write_text("findings: []\n", encoding="utf-8")
            (review_dir / "SECURITY_REVIEW.html").write_text(
                '<!doctype html><html><body><a href="findings.yaml">findings</a></body></html>',
                encoding="utf-8",
            )
            run = subprocess.run([sys.executable, str(VALIDATOR), str(site)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
