# Digital Wellbeing Survey - Screen Time, Sleep & Student Life

**How does screen time affect sleep, stress, and grades among Bangladeshi
university students?** This project answers that question with a real
survey questionnaire, a dataset of 240 responses, and a full Python
analysis - correlations, group comparisons, and charts.

> Note: The included dataset is **synthetic** (generated with a fixed seed).
> It behaves like real survey data so the analysis is real - but it is
> NOT real people. To run a real study, copy the questionnaire into a
> Google Form and replace the CSV with your export.

## Key findings (from the 240-response sample)

| Finding | Number |
| ------- | ------ |
| Average daily screen time | **6.09 hours** |
| Students who feel addicted to their phone | **25.8%** |
| Students using their phone in bed | **84.2%** |
| Students with poor sleep quality | **14.2%** |
| Students with 8h+ screen time per day | **21.2%** |

**Heavy screen users (>8h/day) vs light users (<4h/day):**

| Group | Sleep | CGPA | Stress (1–5) | Study |
| ----- | ----- | ---- | ------------ | ----- |
| Light (<4h) | 8.07h | 3.40 | 2.09 | 4.48h |
| Heavy (>8h) | 6.32h | 3.21 | 3.78 | 3.85h |

**Correlations with screen time:**

| Relationship | r |
| ------------ | --- |
| Screen time vs sleep | **−0.474** |
| Screen time vs stress | **+0.581** |
| Screen time vs CGPA | −0.205 |
| Screen time vs study hours | −0.161 |

**The story in one line:** more screen time goes with less sleep and
much higher stress - heavy users sleep ~1.75 hours less and report
nearly double the stress of light users.

## Quick start

```bash
git clone https://github.com/shabbirhsadhon/digital-wellbeing-survey.git
cd digital-wellbeing-survey
pip install -r requirements.txt
python -m survey_analysis report data/survey_responses.csv --charts reports
```

Or build a beautiful **HTML report** (Python generates the page, plain
HTML + CSS, **no JavaScript**) and open it in your browser:

```bash
python -m survey_analysis html-report data/survey_responses.csv --out reports/report.html
```

## The survey

13 questions in [`survey/questionnaire.md`](survey/questionnaire.md) -
age, gender, university, screen time, social media hours, sleep,
study hours, CGPA, stress (1–5), phone addiction, sleep quality,
phone-before-bed, and physical activity.

## Project structure

```
digital-wellbeing-survey/
├── survey/
│   └── questionnaire.md     # the 13 survey questions
├── data/
│   └── survey_responses.csv # 240 synthetic responses
├── scripts/
│   └── generate_data.py     # regenerates the synthetic dataset (seed 42)
├── survey_analysis/
│   ├── analyzer.py          # loading, stats, correlations, groups
│   ├── charts.py            # matplotlib charts
│   ├── report_html.py       # builds the HTML report (Python + HTML, no JS)
│   └── __main__.py          # `python -m survey_analysis report ...`
├── tests/
│   └── test_analyzer.py
├── requirements.txt
└── README.md
```

## Run the tests

```bash
python -m unittest -v
```

## Tech stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

Python 3.10+ and Matplotlib only - the analysis itself uses the
standard library, and the report is plain HTML + CSS with **no JavaScript**,
so it is easy to read and learn from.

## License

MIT - see [LICENSE](LICENSE).
