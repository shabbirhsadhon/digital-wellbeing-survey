"""Tests for the stress-risk prediction model."""

import unittest
from pathlib import Path

from survey_analysis.analyzer import load_responses
from survey_analysis.model import (
    build_dataset,
    is_at_risk,
    predict_risk,
    recommendations,
    train_model,
)

DATA = Path(__file__).resolve().parent.parent / "data" / "survey_responses.csv"


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.responses = load_responses(DATA)
        cls.result = train_model(cls.responses)

    def test_dataset_shape(self):
        X, y = build_dataset(self.responses)
        self.assertEqual(len(X), 240)
        self.assertEqual(len(X[0]), 7)
        self.assertTrue(all(v in (0, 1) for v in y))
        self.assertGreater(sum(y), 20, "there should be real at-risk cases")

    def test_accuracy_beats_chance(self):
        self.assertGreater(self.result["accuracy"], 0.6)

    def test_predict_returns_label_and_probability(self):
        features = {
            "daily_screen_hours": 10.0,
            "social_media_hours": 6.0,
            "sleep_hours": 5.0,
            "study_hours": 2.0,
            "physical_activity_days": 0,
            "commute_hours": 3.0,
            "age": 21,
        }
        label, probability = predict_risk(self.result["model"], features)
        self.assertIn(label, (0, 1))
        self.assertGreaterEqual(probability, 0.0)
        self.assertLessEqual(probability, 1.0)

    def test_heavy_user_scores_riskier_than_light_user(self):
        model = self.result["model"]
        heavy = {
            "daily_screen_hours": 12.0,
            "social_media_hours": 8.0,
            "sleep_hours": 4.5,
            "study_hours": 1.0,
            "physical_activity_days": 0,
            "commute_hours": 3.5,
            "age": 21,
        }
        light = {
            "daily_screen_hours": 3.0,
            "social_media_hours": 1.0,
            "sleep_hours": 8.5,
            "study_hours": 5.0,
            "physical_activity_days": 5,
            "commute_hours": 1.0,
            "age": 21,
        }
        _, p_heavy = predict_risk(model, heavy)
        _, p_light = predict_risk(model, light)
        self.assertGreater(p_heavy, p_light)

    def test_recommendations_mention_dhaka_life(self):
        tips = recommendations(
            {
                "daily_screen_hours": 10.0,
                "sleep_hours": 5.0,
                "commute_hours": 3.0,
                "study_hours": 1.0,
                "physical_activity_days": 0,
            }
        )
        self.assertGreaterEqual(len(tips), 3)
        self.assertTrue(any("Commute" in t for t in tips))


if __name__ == "__main__":
    unittest.main()
