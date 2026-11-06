"""Stress-risk prediction model for the survey data.

Target: a student is "at risk" when stress is high (level 4 or 5)
or sleep quality is poor. The model is a random forest trained on
screen time, social media hours, sleep, study time, physical
activity and age. Nothing here is medical advice, it is a
classroom-style model built on survey answers.
"""

from __future__ import annotations

import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from .analyzer import Response

FEATURES = [
    "daily_screen_hours",
    "social_media_hours",
    "sleep_hours",
    "study_hours",
    "physical_activity_days",
    "commute_hours",
    "age",
]


def is_at_risk(response: Response) -> int:
    """1 when the student is at risk, else 0."""
    return 1 if response.stress_level >= 4 or response.sleep_quality == "Poor" else 0


def build_dataset(responses: list[Response]) -> tuple[list[list[float]], list[int]]:
    """Feature matrix X and target y for the given responses."""
    X = [[float(getattr(r, name)) for name in FEATURES] for r in responses]
    y = [is_at_risk(r) for r in responses]
    return X, y


def train_model(responses: list[Response], test_size: float = 0.25) -> dict:
    """Train the model and return it with test metrics.

    Returns a dict with the trained ``model``, ``accuracy`` and the
    text ``report`` from sklearn, plus feature importances.
    """
    X, y = build_dataset(responses)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    return {
        "model": model,
        "accuracy": round(accuracy_score(y_test, predicted), 3),
        "report": classification_report(y_test, predicted, zero_division=0),
        "importances": dict(
            sorted(
                zip(FEATURES, [round(float(v), 3) for v in model.feature_importances_]),
                key=lambda item: item[1],
                reverse=True,
            )
        ),
    }


def predict_risk(model, features: dict) -> tuple[int, float]:
    """Predict risk for one student.

    ``features`` maps feature names to values. Returns
    (label, probability of being at risk).
    """
    row = [[float(features[name]) for name in FEATURES]]
    label = int(model.predict(row)[0])
    probability = round(float(model.predict_proba(row)[0][1]), 3)
    return label, probability


def recommendations(features: dict) -> list[str]:
    """Practical next steps for one student, based on their answers.

    Written for Dhaka student life: traffic, mess/hostel living,
    tuition work and late-night phone use.
    """
    tips: list[str] = []
    if features["daily_screen_hours"] > 8:
        tips.append(
            "Screen time is over 8 hours. Try a 1-hour no-phone window "
            "before bed and keep the phone out of the bedroom."
        )
    if features["sleep_hours"] < 6.5:
        tips.append(
            "Sleep is under 6.5 hours. Aim for 7 to 8 hours, even if it "
            "means one less episode or one less scroll session."
        )
    if features["commute_hours"] > 2:
        tips.append(
            "Commute is over 2 hours a day. Use the bus or rickshaw time "
            "for audio lectures or revision instead of social media."
        )
    if features["study_hours"] < 2:
        tips.append(
            "Study time is under 2 hours. Try 25-minute focused blocks "
            "with the phone on silent in another room."
        )
    if features["physical_activity_days"] < 2:
        tips.append(
            "Move more: even a 20-minute walk around campus or the "
            "neighbourhood, 3 days a week, helps sleep and stress."
        )
    if not tips:
        tips.append("Your habits look balanced. Keep the routine going.")
    return tips


def save_model(model, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(model, f)
    return path


def load_model(path: str | Path):
    with Path(path).open("rb") as f:
        return pickle.load(f)
