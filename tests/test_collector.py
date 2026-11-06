"""Tests for automatic data collection."""

import tempfile
import unittest
from pathlib import Path

from survey_analysis.collector import DEFAULT_SOURCE, collect

DATA = Path(__file__).resolve().parent.parent / "data" / "survey_responses.csv"


class TestCollector(unittest.TestCase):
    def test_collect_from_file_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "copy.csv"
            result = collect(source=DATA.as_uri(), dest=dest)
            self.assertTrue(result.exists())
            self.assertIn("daily_screen_hours", result.read_text(encoding="utf-8"))

    def test_bad_columns_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.csv"
            bad.write_text("a,b,c\n1,2,3\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                collect(source=bad.as_uri(), dest=Path(tmp) / "out.csv")

    def test_default_source_is_github_raw(self):
        self.assertIn("raw.githubusercontent.com", DEFAULT_SOURCE)
        self.assertIn("digital-wellbeing-survey", DEFAULT_SOURCE)


if __name__ == "__main__":
    unittest.main()
