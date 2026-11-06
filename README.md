# Digital Wellbeing Survey - Screen Time, Sleep and Student Life

How does screen time affect sleep, stress, and grades among Bangladeshi
university students? This project answers that question with a survey
questionnaire, a dataset of 240 responses, a full Python analysis, a
stress-risk prediction model, and an interactive app.

The survey is built around Dhaka student life: long commutes in traffic,
mess and hostel living, part-time tuition work, and late-night phone use.
The app turns the analysis into something useful in real life: answer
a few questions about your own habits and get a risk prediction plus
practical next steps.

> Note: The included dataset is **synthetic** (generated with a fixed seed).
> It behaves like real survey data so the analysis is real - but it is
> NOT real people. To run a real study, copy the questionnaire into a
> Google Form and replace the CSV with your export.

## Key findings (from the 240-response sample)

| Finding | Number |
| ------- | ------ |
| Average daily screen time | **6.47 hours** |
| Average daily commute (Dhaka traffic) | **1.72 hours** |
| Students with a part-time job or tuition work | **27.1%** |
| Students who feel addicted to their phone | **32.9%** |
| Students using their phone in bed | **83.3%** |
| Students with poor sleep quality | **18.8%** |
| Students with 8h+ screen time per day | **22.1%** |

**Heavy screen users (>8h/day) vs light users (<4h/day):**

| Group | Students | Sleep | CGPA | Stress (1-5) | Study |
| ----- | -------- | ----- | ---- | ------------ | ----- |
| Light (<4h) | 28 | 8.04h | 3.51 | 2.14 | 4.62h |
| Medium (4-8h) | 159 | 7.29h | 3.32 | 3.02 | 3.99h |
| Heavy (>8h) | 53 | 6.61h | 3.09 | 3.77 | 3.66h |

**Correlations with screen time:**

| Relationship | r |
| ------------ | --- |
| Screen time vs sleep | **-0.399** |
| Screen time vs stress | **+0.416** |
| Screen time vs CGPA | -0.362 |
| Screen time vs study hours | -0.185 |
| Commute time vs stress | +0.119 |

**The story in one line:** more screen time goes with less sleep and
much higher stress - heavy users sleep about 1.4 hours less and report
much higher stress than light users.

## How it works

1. **Collect data automatically.** `survey_analysis/collector.py`
   downloads the survey CSV from a published source (a Google Form
   export link, or the CSV in this repo by default) and checks that
   the columns are right.
2. **Analyse it.** `survey_analysis/analyzer.py` computes averages,
   group comparisons, and correlations from the CSV.
3. **Predict risk.** `survey_analysis/model.py` trains a random forest
   that predicts whether a student is at risk (high stress or poor
   sleep) from screen time, sleep, study, activity, commute, and age.
   Test accuracy on the sample data: **73.3%**. Sleep hours matter
   most, then screen time.
4. **Use it.** The Streamlit app (`app.py`) lets anyone move sliders
   for their own habits and get a prediction plus practical advice.

## Quick start

```bash
git clone https://github.com/shabbirhsadhon/digital-wellbeing-survey.git
cd digital-wellbeing-survey
pip install -r requirements.txt
python -m survey_analysis report data/survey_responses.csv --charts reports
```

Build a self-contained HTML report (plain HTML and CSS, no JavaScript):

```bash
python -m survey_analysis html-report data/survey_responses.csv --out reports/report.html
```

Try the interactive app:

```bash
streamlit run app.py
```

## The survey

15 questions in [`survey/questionnaire.md`](survey/questionnaire.md) -
age, gender, university, screen time, social media hours, sleep,
study hours, CGPA, stress (1-5), phone addiction, sleep quality,
phone-before-bed, physical activity, daily commute, and part-time work.

## Project structure

```
digital-wellbeing-survey/
├── app.py                   # interactive Streamlit app
├── survey/
│   └── questionnaire.md     # the 15 survey questions
├── data/
│   └── survey_responses.csv # 240 synthetic responses
├── scripts/
│   └── generate_data.py     # regenerates the synthetic dataset (seed 42)
├── survey_analysis/
│   ├── analyzer.py          # loading, stats, correlations, groups
│   ├── charts.py            # matplotlib charts
│   ├── collector.py         # automatic data collection from a CSV source
│   ├── model.py             # stress-risk prediction model
│   ├── report_html.py       # builds the HTML report (Python + HTML, no JS)
│   └── __main__.py          # `python -m survey_analysis report ...`
├── tests/
│   ├── test_analyzer.py
│   ├── test_collector.py
│   └── test_model.py
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

Python, HTML, pandas, scikit-learn, Streamlit, and Matplotlib. The
analysis itself uses the standard library where possible, and the app
is written in plain Python - no JavaScript.

## License

MIT - see [LICENSE](LICENSE).
