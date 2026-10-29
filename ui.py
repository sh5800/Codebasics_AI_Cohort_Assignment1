import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Welcome to CB Workout Plan Generator")
st.subheader("A One Stop Place for All Your Fitness Goals")

st.markdown('##### Answer a Few Quick Questions To Get Started')
with st.form("tea_form"):
    fitness_goal = st.selectbox("What's your Fitness Goal ?", ["Build Muscle", "Loose Fat","General Fitness","Improve Endurance"])
    experience_level = st.selectbox("What's Your Experience Level ?",["Beginner","Intermediate","Advanced"])
    days_available = st.slider("How many days can you dedicate ?",min_value=0,max_value=7,step=1)
    equipments_available = st.selectbox("Equipments that you own ?",["No equipment","Home Dumbbells","An Entire Gym with all Equipments"])
    injuries = st.text_area("Any injury or any medication that you currently have ? (Optional)")

    submitted = st.form_submit_button("Generate Plan")


if submitted:
    if not fitness_goal.strip():
        st.error("Please enter your fitness goal")
    elif not experience_level.strip():
         st.error("Please enter your experience level")
    elif days_available == 0:
        st.error("The number of days should be at least 1")
    elif not equipments_available.strip():
        st.error("Please enter which equipments you have")            
    else:
        plan_data = {
            "fitness_goal": fitness_goal.strip(),
            "experience_level": experience_level.strip(),
            "days_available": days_available,
            "equipments_available":equipments_available,
            "injuries":injuries
        }

        try:
            response = requests.post(
                f"{API_URL}/generatePlan",
                json=plan_data,
                timeout=10
            )

            if response.ok:
                result = response.json()
                st.success(result["Message"])
                st.markdown(result["WorkoutPlan"])
            else:
                st.error(
                    f"API error: {response.status_code}"
                )
                st.json(response.json())

        except requests.RequestException as error:
            st.error(f"Could not connect to API: {error}")