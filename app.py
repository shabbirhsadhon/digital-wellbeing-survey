"""Interactive Streamlit app for the survey.

Run it with:
    streamlit run app.py

Everything in this file is plain Python. Streamlit turns the
sliders and buttons below into a web page, no JavaScript needed
from the author.
"""

from pathlib import Path

import streamlit as st

from survey_analysis.analyzer import describe, load_responses
from survey_analysis.charts import group_comparison, screen_vs_sleep
from survey_analysis.collector import collect
from survey_analysis.model import predict_risk, recommendations, train_model

DATA_PATH = Path(__file__).parent / "data" / "survey_responses.csv"


@st.cache_resource
def get_model():
    responses = load_responses(DATA_PATH)
    return train_model(responses)


@st.cache_data
def get_responses():
    return load_responses(DATA_PATH)


st.set_page_config(page_title="Digital Wellbeing Survey", layout="wide")
st.title("Digital Wellbeing Survey")
st.write(
    "Screen time, sleep, stress and student life in Dhaka, Bangladesh. "
    "Move the sliders to see the predicted risk for a student like you."
)

tab_predict, tab_data, tab_model = st.tabs(["Predict risk", "Explore the data", "The model"])

with tab_predict:
    st.header("Am I at risk?")
    st.write("Risk means high stress (level 4 or 5) or poor sleep quality.")
    col1, col2 = st.columns(2)
    with col1:
        screen = st.slider("Daily screen time (hours)", 1.0, 14.0, 6.0, 0.5)
        social = st.slider("Social media (hours)", 0.5, 10.0, 3.0, 0.5)
        sleep = st.slider("Sleep per night (hours)", 3.5, 10.0, 7.0, 0.5)
    with col2:
        study = st.slider("Study per day (hours)", 0.5, 10.0, 4.0, 0.5)
        activity = st.slider("Physically active days per week", 0, 7, 3)
        commute = st.slider("Daily commute to campus (hours, Dhaka traffic)", 0.0, 4.5, 1.5, 0.5)
        age = st.slider("Age", 18, 25, 21)
    if st.button("Predict"):
        result = get_model()
        answers = {
            "daily_screen_hours": screen,
            "social_media_hours": social,
            "sleep_hours": sleep,
            "study_hours": study,
            "physical_activity_days": activity,
            "commute_hours": commute,
            "age": age,
        }
        label, probability = predict_risk(result["model"], answers)
        if label == 1:
            st.error(f"At risk, probability {probability:.0%}.")
        else:
            st.success(f"Not at risk, probability of risk {probability:.0%}. Keep it up.")
        st.subheader("What you can do")
        for tip in recommendations(answers):
            st.write("- " + tip)

with tab_data:
    st.header("The survey data")
    responses = get_responses()
    stats = describe(responses)
    st.write(f"{stats['n']} students. Average screen time "
             f"{stats['avg_screen_hours']} hours, average sleep "
             f"{stats['avg_sleep_hours']} hours.")
    if st.button("Refresh data from the source"):
        collect(dest=DATA_PATH)
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Data refreshed from the source.")
    st.image(str(screen_vs_sleep(responses, Path("reports/screen_vs_sleep.png"))),
             caption="Screen time vs sleep")
    st.image(str(group_comparison(responses, Path("reports/group_comparison.png"))),
             caption="Low vs medium vs heavy screen time")

with tab_model:
    st.header("How the prediction model works")
    result = get_model()
    st.write(f"Random forest, test accuracy **{result['accuracy']:.1%}**.")
    st.write("Most important features:")
    for name, value in result["importances"].items():
        st.write(f"- {name}: {value}")
    st.text(result["report"])
