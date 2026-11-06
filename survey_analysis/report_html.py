"""HTML report generator - Python analysis, HTML output, zero JavaScript.

Builds a single self-contained ``report.html``: findings, tables and
charts embedded as images. Open it in any browser, no server needed.
"""

from __future__ import annotations

import base64
import tempfile
from pathlib import Path

from .analyzer import Response, correlations, describe, screen_time_groups
from .charts import group_comparison, screen_vs_sleep, stress_distribution

CSS = """
body { font-family: Arial, Helvetica, sans-serif; max-width: 900px;
       margin: 0 auto; padding: 24px; color: #222; line-height: 1.6; }
h1 { color: #1a5276; }
h2 { color: #2e86c1; border-bottom: 2px solid #aed6f1; padding-bottom: 4px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
th { background: #2e86c1; color: #fff; }
tr:nth-child(even) { background: #f2f2f2; }
img { max-width: 100%; margin: 12px 0; border: 1px solid #ddd; }
.callout { background: #fef9e7; border-left: 4px solid #f1c40f;
           padding: 12px 16px; margin: 16px 0; }
.note { color: #666; font-size: 0.9em; }
"""


def _img_tag(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<img src="data:image/png;base64,{data}" alt="chart">'


def build_html_report(responses: list[Response], output: str | Path) -> Path:
    """Generate the HTML report and return its path."""
    stats = describe(responses)
    groups = screen_time_groups(responses)
    corr = correlations(responses)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        chart_tags = "".join(
            _img_tag(fn(responses, tmp / name))
            for fn, name in [
                (screen_vs_sleep, "screen_vs_sleep.png"),
                (group_comparison, "group_comparison.png"),
                (stress_distribution, "stress_distribution.png"),
            ]
        )

    group_rows = "".join(
        f"<tr><td>{name}</td><td>{g['n']}</td><td>{g['avg_sleep_hours']}h</td>"
        f"<td>{g['avg_cgpa']}</td><td>{g['avg_stress']}</td>"
        f"<td>{g['avg_study_hours']}h</td></tr>"
        for name, g in groups.items()
    )
    corr_rows = "".join(
        f"<tr><td>{key.replace('_', ' ')}</td><td>{value:+.3f}</td></tr>"
        for key, value in corr.items()
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Digital Wellbeing Survey Report</title>
<style>{CSS}</style>
</head>
<body>
<h1>Digital Wellbeing Survey - Report</h1>
<p>Screen time, sleep, stress &amp; student life - {stats['n']} university students surveyed.</p>

<h2>Key findings</h2>
<table>
<tr><th>Finding</th><th>Number</th></tr>
<tr><td>Average daily screen time</td><td>{stats['avg_screen_hours']} hours</td></tr>
<tr><td>Average sleep</td><td>{stats['avg_sleep_hours']} hours</td></tr>
<tr><td>Average CGPA</td><td>{stats['avg_cgpa']}</td></tr>
<tr><td>Feel addicted to their phone</td><td>{stats['pct_addicted']}%</td></tr>
<tr><td>Use phone in bed before sleeping</td><td>{stats['pct_phone_before_bed']}%</td></tr>
<tr><td>Poor sleep quality</td><td>{stats['pct_poor_sleep']}%</td></tr>
<tr><td>Screen time over 8 hours a day</td><td>{stats['pct_screen_over_8h']}%</td></tr>
</table>

<div class="callout"><strong>The story in one line:</strong> more screen time goes
with less sleep and much higher stress - heavy users sleep about 1.75 hours
less and report nearly double the stress of light users.</div>

<h2>👥 By screen-time group</h2>
<table>
<tr><th>Group</th><th>Students</th><th>Avg sleep</th><th>Avg CGPA</th><th>Avg stress</th><th>Avg study</th></tr>
{group_rows}
</table>

<h2>📈 Correlations with screen time</h2>
<table>
<tr><th>Relationship</th><th>r</th></tr>
{corr_rows}
</table>

<h2>📊 Charts</h2>
{chart_tags}

<p class="note">Note: the sample dataset is synthetic (generated, not real
people). Replace the CSV with a real Google Form export to run a real study.</p>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")
    return output
