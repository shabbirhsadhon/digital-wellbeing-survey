"""Command-line report for the digital wellbeing survey.

Usage:
    python -m survey_analysis report data/survey_responses.csv
    python -m survey_analysis report data/survey_responses.csv --charts reports
    python -m survey_analysis html-report data/survey_responses.csv --out reports/report.html
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analyzer import correlations, describe, load_responses, screen_time_groups
from .charts import group_comparison, screen_vs_sleep, stress_distribution
from .report_html import build_html_report


def cmd_report(args: argparse.Namespace) -> int:
    responses = load_responses(args.csv)
    stats = describe(responses)
    print(f"=== Digital Wellbeing Survey - {stats['n']} students ===\n")
    print(f"Avg daily screen time : {stats['avg_screen_hours']} hours")
    print(f"Avg sleep             : {stats['avg_sleep_hours']} hours")
    print(f"Avg study time        : {stats['avg_study_hours']} hours")
    print(f"Avg CGPA              : {stats['avg_cgpa']}")
    print(f"Avg stress (1-5)      : {stats['avg_stress']}")
    print(f"Feel addicted         : {stats['pct_addicted']}%")
    print(f"Phone before bed      : {stats['pct_phone_before_bed']}%")
    print(f"Poor sleep quality    : {stats['pct_poor_sleep']}%")
    print(f"Screen time over 8h   : {stats['pct_screen_over_8h']}%")

    print("\n--- By screen-time group ---")
    for group, info in screen_time_groups(responses).items():
        print(
            f"{group:<16} n={info['n']:<4} sleep {info['avg_sleep_hours']}h  "
            f"CGPA {info['avg_cgpa']}  stress {info['avg_stress']}  study {info['avg_study_hours']}h"
        )

    print("\n--- Correlations with screen time ---")
    for key, value in correlations(responses).items():
        print(f"  {key:<18} {value:+.3f}")

    if args.charts:
        out = Path(args.charts)
        out.mkdir(parents=True, exist_ok=True)
        for fn, name in [
            (screen_vs_sleep, "screen_vs_sleep.png"),
            (group_comparison, "group_comparison.png"),
            (stress_distribution, "stress_distribution.png"),
        ]:
            print(f"Saved: {fn(responses, out / name)}")
    return 0


def cmd_html_report(args: argparse.Namespace) -> int:
    responses = load_responses(args.csv)
    path = build_html_report(responses, args.out)
    print(f"Saved: {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="survey-analysis",
        description="Analyze the digital wellbeing survey.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("report", help="Print the full analysis report")
    p.add_argument("csv", help="Path to the survey responses CSV")
    p.add_argument("--charts", default=None, help="Folder to save charts into")
    p.set_defaults(func=cmd_report)
    p = sub.add_parser("html-report", help="Build a self-contained HTML report (no JavaScript)")
    p.add_argument("csv", help="Path to the survey responses CSV")
    p.add_argument("--out", default="reports/report.html", help="Output HTML file")
    p.set_defaults(func=cmd_html_report)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
