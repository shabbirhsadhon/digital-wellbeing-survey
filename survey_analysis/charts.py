"""Charts for the digital wellbeing survey (matplotlib)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .analyzer import Response, screen_time_groups


def _save(fig, output: Path) -> Path:
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)
    return output


def screen_vs_sleep(responses: list[Response], output: str | Path) -> Path:
    """Scatter: daily screen hours vs sleep hours."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(
        [r.daily_screen_hours for r in responses],
        [r.sleep_hours for r in responses],
        alpha=0.6,
        color="#4C72B0",
    )
    ax.set_title("Screen Time vs Sleep")
    ax.set_xlabel("Daily screen time (hours)")
    ax.set_ylabel("Sleep (hours)")
    ax.grid(True, alpha=0.3)
    return _save(fig, Path(output))


def group_comparison(responses: list[Response], output: str | Path) -> Path:
    """Bar chart: average sleep / CGPA / stress by screen-time group."""
    groups = screen_time_groups(responses)
    labels = list(groups.keys())
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, key, title in [
        (axes[0], "avg_sleep_hours", "Avg sleep (hours)"),
        (axes[1], "avg_cgpa", "Avg CGPA"),
        (axes[2], "avg_stress", "Avg stress (1–5)"),
    ]:
        ax.bar(labels, [groups[label][key] for label in labels], color="#55A868")
        ax.set_title(title)
        ax.tick_params(axis="x", labelrotation=20)
    fig.suptitle("Low vs Medium vs Heavy Screen Time")
    return _save(fig, Path(output))


def stress_distribution(responses: list[Response], output: str | Path) -> Path:
    """Bar chart: how many students report each stress level."""
    from collections import Counter

    counts = Counter(r.stress_level for r in responses)
    levels = sorted(counts)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([str(l) for l in levels], [counts[l] for l in levels], color="#C44E52")
    ax.set_title("Stress Level Distribution (1 = low, 5 = high)")
    ax.set_xlabel("Stress level")
    ax.set_ylabel("Students")
    return _save(fig, Path(output))
