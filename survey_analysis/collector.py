"""Automatic data collection for the survey.

The default source is the public CSV in this repo itself, so the
pipeline works out of the box. To use real answers, publish your
Google Form responses as CSV (File > Share > Publish to web, CSV
format) and pass that link as ``source`` instead.
"""

from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_SOURCE = (
    "https://raw.githubusercontent.com/shabbirhsadhon/"
    "digital-wellbeing-survey/main/data/survey_responses.csv"
)

REQUIRED_COLUMNS = {
    "respondent_id",
    "age",
    "gender",
    "university",
    "daily_screen_hours",
    "social_media_hours",
    "sleep_hours",
    "study_hours",
    "cgpa",
    "stress_level",
    "feels_addicted",
    "sleep_quality",
    "uses_phone_before_bed",
    "physical_activity_days",
    "commute_hours",
    "part_time_job",
}


def collect(source: str | None = None, dest: str | Path = "data/survey_responses.csv") -> Path:
    """Download the survey CSV from ``source`` and save it to ``dest``.

    Returns the path of the saved file. Raises ValueError if the
    downloaded file does not have the expected columns, and URLError
    if the download itself fails.
    """
    url = source or DEFAULT_SOURCE
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "survey-analysis/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise ConnectionError(f"Could not download data from {url}: {exc}") from exc
    header = {c.strip() for c in text.splitlines()[0].split(",")}
    missing = REQUIRED_COLUMNS - header
    if missing:
        raise ValueError(f"Downloaded CSV is missing columns: {sorted(missing)}")
    dest.write_text(text, encoding="utf-8")
    return dest
