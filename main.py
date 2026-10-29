import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from groq import Groq

load_dotenv()

app = FastAPI(title="Groq Workout Planner API")

class Planner(BaseModel):
    fitness_goal:str
    experience_level:str
    days_available:int
    equipments_available:str
    injuries:str


def generate_workout_plan(plan_data: Planner) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing GROQ_API_KEY in environment")

    client = Groq()
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional and certified gym and fitness trainer who has trained people and help them achieve their fitness goals. You have a combined 15 years of experience in the fitness world"},
            {"role": "user", "content": f"Generate a weekly workout plan based on the data provided by the user which is, Fitness Goal: {plan_data.fitness_goal}, Current Experience: {plan_data.experience_level}, No of days he/she can workout during the week: {plan_data.days_available}, Equipments Owned: {plan_data.equipments_available}, Injuries or medical history: {plan_data.injuries}."},
        ],
        temperature=1.0,
        max_tokens=900,
    )

    plan = completion.choices[0].message.content
    if not plan:
        raise HTTPException(status_code=502, detail="LLM returned an empty plan")
    print(plan)
    return plan.strip()


@app.post("/generatePlan")
def generate_workout(plan_data: Planner) -> dict[str, str]:
    resp = generate_workout_plan(plan_data)
    return {"Message":"Your Workout Plan","WorkoutPlan":resp}