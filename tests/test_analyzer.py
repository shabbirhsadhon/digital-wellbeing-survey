"""Tests for the digital wellbeing survey analysis."""

import unittest
from pathlib import Path

from survey_analysis.analyzer import (
    correlation,
    correlations,
    describe,
    load_responses,
    screen_time_groups,
)

DATA = Path(__file__).resolve().parent.parent / "data" / "survey_responses.csv"


class TestAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.responses = load_responses(DATA)

    def test_loads_all_rows(self):
        self.assertEqual(len(self.responses), 240)

    def test_describe_ranges(self):
        stats = describe(self.responses)
        self.assertGreater(stats["avg_screen_hours"], 4)
        self.assertLess(stats["avg_screen_hours"], 9)
        self.assertGreaterEqual(stats["pct_addicted"], 0)
        self.assertLessEqual(stats["pct_addicted"], 100)

    def test_screen_groups_cover_all(self):
        groups = screen_time_groups(self.responses)
        total = sum(g["n"] for g in groups.values())
        self.assertEqual(total, 240)
        self.assertIn("Heavy (>8h)", groups)

    def test_heavy_users_sleep_less(self):
        groups = screen_time_groups(self.responses)
        self.assertLess(
            groups["Heavy (>8h)"]["avg_sleep_hours"],
            groups["Low (<4h)"]["avg_sleep_hours"],
        )

    def test_correlation_signs(self):
        corr = correlations(self.responses)
        self.assertLess(corr["screen_vs_sleep"], 0, "more screen -> less sleep")
        self.assertGreater(corr["screen_vs_stress"], 0, "more screen -> more stress")

    def test_correlation_bounds(self):
        self.assertAlmostEqual(correlation([1, 2, 3], [1, 2, 3]), 1.0)
        self.assertAlmostEqual(correlation([1, 2, 3], [3, 2, 1]), -1.0)

    def test_html_report(self):
        import tempfile

        from survey_analysis.report_html import build_html_report

        with tempfile.TemporaryDirectory() as tmp:
            out = build_html_report(self.responses, Path(tmp) / "report.html")
            html = out.read_text(encoding="utf-8")
            self.assertIn("Digital Wellbeing Survey", html)
            self.assertIn("6.09", html)  # avg screen time from the sample data
            self.assertNotIn("<script", html.lower(), "report must not use JavaScript")


if __name__ == "__main__":
    unittest.main()
