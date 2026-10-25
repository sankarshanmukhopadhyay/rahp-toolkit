import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_review_readiness as review_validation


class ReviewBoundarySynchronizationTests(unittest.TestCase):
    def _fixture(self, stable_release="v2.9.0"):
        temp = tempfile.TemporaryDirectory()
        root = pathlib.Path(temp.name)
        for rel in (
            "docs/review/review-readiness-baseline.md",
            "docs/review/reproduction.md",
            "docs/review/known-limitations.md",
            "docs/review/security-pre-review.md",
        ):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)

        (root / "docs/review/review-readiness-baseline.md").write_text(
            f"Stable release: {stable_release}\n", encoding="utf-8"
        )
        (root / "docs/review/reproduction.md").write_text(
            f"Stable release: {stable_release}\ngit checkout {stable_release}\nrequirements-release.lock\n",
            encoding="utf-8",
        )
        (root / "docs/review/known-limitations.md").write_text(
            f"{stable_release}\nrequirements-release.lock\n", encoding="utf-8"
        )
        (root / "docs/review/security-pre-review.md").write_text(
            "historical v2.4.0 current-main-release-security-disposition-2026-10-22.md\n",
            encoding="utf-8",
        )
        return temp, root

    def test_current_review_boundary_is_accepted(self):
        temp, root = self._fixture()
        try:
            self.assertEqual(
                review_validation.check_current_review_docs(root, "v2.9.0"), []
            )
        finally:
            temp.cleanup()

    def test_stale_stable_release_is_rejected(self):
        temp, root = self._fixture(stable_release="v2.8.0")
        try:
            errors = review_validation.check_current_review_docs(root, "v2.9.0")
            self.assertTrue(any("review-readiness-baseline.md" in e for e in errors))
            self.assertTrue(any("reproduction.md" in e for e in errors))
            self.assertTrue(any("known-limitations.md" in e for e in errors))
        finally:
            temp.cleanup()

    def test_historical_pre_review_must_be_labelled_and_link_current_disposition(self):
        temp, root = self._fixture()
        try:
            (root / "docs/review/security-pre-review.md").write_text(
                "v2.4.0 pre-review\n", encoding="utf-8"
            )
            errors = review_validation.check_current_review_docs(root, "v2.9.0")
            self.assertTrue(any("historical-boundary token" in e for e in errors))
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
