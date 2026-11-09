# import os

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 90  # LLM calls are slow; 10s was too short


def request_plan(payload: dict) -> tuple[str | None, str | None]:
    """Call the backend. Returns (plan, error_message); exactly one is set."""
    try:
        response = requests.post(f"{API_URL}/generatePlan", json=payload, timeout=REQUEST_TIMEOUT)
    except requests.Timeout:
        return None, "The request timed out. Please try again."
    except requests.ConnectionError:
        return None, "Can't reach the backend. Make sure the FastAPI server is running."
    except requests.RequestException:
        return None, "Something went wrong sending your request. Please try again."

    if not response.ok:
        if response.status_code == 422:
            return None, "Some of your inputs were invalid. Please check them and try again."
        try:
            detail = response.json().get("detail")
        except ValueError:
            detail = None
        return None, detail if isinstance(detail, str) else "The server hit an error. Please try again later."

    try:
        plan = response.json().get("workout_plan", "")
    except ValueError:
        plan = ""
    if not plan:
        return None, "We got an empty response. Please try again."
    return plan, None


st.title("Welcome to CB Workout Plan Generator")
st.subheader("A One Stop Place for All Your Fitness Goals")
st.markdown("##### Answer a Few Quick Questions To Get Started")

with st.form("workout_form"):
    fitness_goal = st.selectbox(
        "What's your fitness goal?",
        ["Build Muscle", "Lose Fat", "General Fitness", "Improve Endurance"],
    )
    experience_level = st.selectbox(
        "What's your experience level?", ["Beginner", "Intermediate", "Advanced"]
    )
    days_available = st.slider(
        "How many days per week can you train?", min_value=1, max_value=7, value=3, step=1
    )
    equipment_available = st.selectbox(
        "Equipment you have access to?", ["No equipment", "Home dumbbells", "Full gym"]
    )
    injuries = st.text_area(
        "Any injuries or limitations? (optional)",
        placeholder="e.g. bad knees, no overhead pressing",
        max_chars=300,
    )
    submitted = st.form_submit_button("Generate Plan")

if submitted:
    if days_available < 1:
        st.error("Please select at least 1 training day.")
    else:
        payload = {
            "fitness_goal": fitness_goal,
            "experience_level": experience_level,
            "days_available": days_available,
            "equipment_available": equipment_available,
            "injuries": injuries.strip(),
        }
        with st.spinner("Building your plan..."):
            plan, error = request_plan(payload)
        if error:
            st.error(error)
        else:
            st.success("Your Workout Plan")
            st.markdown(plan)