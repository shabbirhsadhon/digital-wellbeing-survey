"""Generate the synthetic survey dataset.

The data is SYNTHETIC — generated with a fixed seed so every run
produces the same file. It is realistic (screen time correlates
with less sleep and higher stress) but it is NOT real survey data.
Real data would come from a Google Form export in the same format.
"""

import csv
import random
from pathlib import Path

SEED = 42
N = 240

UNIVERSITIES = ["UIU", "DU", "BUET", "NSU", "BRAC University", "JU", "CU", "RU"]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def generate(path: str | Path) -> Path:
    rng = random.Random(SEED)
    rows = []
    for i in range(1, N + 1):
        screen = round(_clamp(rng.gauss(6.5, 2.2), 1.5, 14.0), 1)
        social = round(_clamp(screen * rng.uniform(0.35, 0.7), 0.5, 10.0), 1)
        # More screen time -> less sleep, more stress, slightly lower CGPA.
        sleep = round(_clamp(rng.gauss(7.2, 1.1) - (screen - 6.5) * 0.28, 3.5, 10.0), 1)
        stress = int(_clamp(round(rng.gauss(3.0, 1.0) + (screen - 6.5) * 0.3), 1, 5))
        cgpa = round(_clamp(rng.gauss(3.3, 0.35) - (screen - 6.5) * 0.04, 2.0, 4.0), 2)
        study = round(_clamp(rng.gauss(4.0, 1.5) - (screen - 6.5) * 0.15, 0.5, 10.0), 1)
        rows.append(
            {
                "respondent_id": f"R{i:03d}",
                "age": rng.randint(18, 25),
                "gender": rng.choice(["Female", "Male"]),
                "university": rng.choice(UNIVERSITIES),
                "daily_screen_hours": screen,
                "social_media_hours": social,
                "sleep_hours": sleep,
                "study_hours": study,
                "cgpa": cgpa,
                "stress_level": stress,
                "feels_addicted": "Yes" if screen >= 7 and rng.random() < 0.75 else "No",
                "sleep_quality": (
                    "Poor" if sleep < 6 else "Good" if sleep >= 7.5 else "Fair"
                ),
                "uses_phone_before_bed": "Yes" if rng.random() < 0.82 else "No",
                "physical_activity_days": rng.randint(0, 7),
            }
        )

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    out = generate(Path(__file__).resolve().parent.parent / "data" / "survey_responses.csv")
    print(f"Wrote {N} synthetic responses to {out}")
