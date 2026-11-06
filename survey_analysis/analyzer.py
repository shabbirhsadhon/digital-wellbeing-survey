"""Core analysis for the digital wellbeing survey.

Works on the CSV produced by ``scripts/generate_data.py`` or on a
real Google Form export with the same columns. Only the standard
library is used here - no pandas needed.
"""

from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

NUMERIC = (
    "age",
    "daily_screen_hours",
    "social_media_hours",
    "sleep_hours",
    "study_hours",
    "cgpa",
    "stress_level",
    "physical_activity_days",
)


@dataclass
class Response:
    respondent_id: str
    age: int
    gender: str
    university: str
    daily_screen_hours: float
    social_media_hours: float
    sleep_hours: float
    study_hours: float
    cgpa: float
    stress_level: int
    feels_addicted: str
    sleep_quality: str
    uses_phone_before_bed: str
    physical_activity_days: int


def load_responses(path: str | Path) -> list[Response]:
    """Load survey responses from a CSV file."""
    rows: list[Response] = []
    with Path(path).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(
                Response(
                    respondent_id=row["respondent_id"],
                    age=int(row["age"]),
                    gender=row["gender"],
                    university=row["university"],
                    daily_screen_hours=float(row["daily_screen_hours"]),
                    social_media_hours=float(row["social_media_hours"]),
                    sleep_hours=float(row["sleep_hours"]),
                    study_hours=float(row["study_hours"]),
                    cgpa=float(row["cgpa"]),
                    stress_level=int(row["stress_level"]),
                    feels_addicted=row["feels_addicted"],
                    sleep_quality=row["sleep_quality"],
                    uses_phone_before_bed=row["uses_phone_before_bed"],
                    physical_activity_days=int(row["physical_activity_days"]),
                )
            )
    return rows


def mean(values: list[float]) -> float:
    return round(statistics.mean(values), 2)


def correlation(xs: list[float], ys: list[float]) -> float:
    """Pearson correlation coefficient between two lists."""
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    return round(num / den, 3) if den else 0.0


def describe(responses: list[Response]) -> dict:
    """Headline numbers for the whole sample."""
    screen = [r.daily_screen_hours for r in responses]
    return {
        "n": len(responses),
        "avg_screen_hours": mean(screen),
        "avg_sleep_hours": mean([r.sleep_hours for r in responses]),
        "avg_study_hours": mean([r.study_hours for r in responses]),
        "avg_cgpa": mean([r.cgpa for r in responses]),
        "avg_stress": mean([float(r.stress_level) for r in responses]),
        "pct_addicted": round(
            100 * sum(r.feels_addicted == "Yes" for r in responses) / len(responses), 1
        ),
        "pct_phone_before_bed": round(
            100 * sum(r.uses_phone_before_bed == "Yes" for r in responses) / len(responses),
            1,
        ),
        "pct_poor_sleep": round(
            100 * sum(r.sleep_quality == "Poor" for r in responses) / len(responses), 1
        ),
        "pct_screen_over_8h": round(100 * sum(s > 8 for s in screen) / len(screen), 1),
    }


def screen_time_groups(responses: list[Response]) -> dict[str, dict]:
    """Compare low / medium / heavy screen-time groups."""
    groups: dict[str, list[Response]] = defaultdict(list)
    for r in responses:
        key = "Low (<4h)" if r.daily_screen_hours < 4 else (
            "Medium (4–8h)" if r.daily_screen_hours <= 8 else "Heavy (>8h)"
        )
        groups[key].append(r)
    out: dict[str, dict] = {}
    for key, members in groups.items():
        out[key] = {
            "n": len(members),
            "avg_sleep_hours": mean([r.sleep_hours for r in members]),
            "avg_cgpa": mean([r.cgpa for r in members]),
            "avg_stress": mean([float(r.stress_level) for r in members]),
            "avg_study_hours": mean([r.study_hours for r in members]),
        }
    return out


def correlations(responses: list[Response]) -> dict[str, float]:
    """Key relationships in the data."""
    screen = [r.daily_screen_hours for r in responses]
    return {
        "screen_vs_sleep": correlation(screen, [r.sleep_hours for r in responses]),
        "screen_vs_stress": correlation(screen, [float(r.stress_level) for r in responses]),
        "screen_vs_cgpa": correlation(screen, [r.cgpa for r in responses]),
        "screen_vs_study": correlation(screen, [r.study_hours for r in responses]),
        "sleep_vs_cgpa": correlation([r.sleep_hours for r in responses], [r.cgpa for r in responses]),
    }


def category_counts(responses: list[Response], field: str) -> dict[str, int]:
    """Count responses per value of a categorical field."""
    return dict(Counter(getattr(r, field) for r in responses))
