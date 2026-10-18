"""Guard discoverability of all packaged corpus adapters (issue #1039)."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def missing_browser_links(browser_text: str, corpus_paths: list[Path]) -> list[str]:
    """Every adapter needs a human-readable route, not only a raw YAML link."""
    return [
        p.stem for p in corpus_paths
        if f']({p.stem}/)' not in browser_text
    ]


class CorpusBrowserCompletenessTest(unittest.TestCase):
    def test_all_packaged_adapters_linked(self):
        corpus_paths = sorted(
            p for p in (ROOT / "corpora").glob("*.yaml")
            if p.name != "sources.yaml"
        )
        self.assertEqual(15, len(corpus_paths))
        browser = (ROOT / "corpora" / "index.md").read_text(encoding="utf-8")
        self.assertEqual([], missing_browser_links(browser, corpus_paths))

    def test_unlinked_adapter_is_detected(self):
        corpus_paths = [Path("corpora/vds.yaml"), Path("corpora/agent-names.yaml")]
        browser = "| VDS | [Browse](vds/) |\n"
        self.assertEqual(
            ["agent-names"], missing_browser_links(browser, corpus_paths)
        )


if __name__ == "__main__":
    unittest.main()
