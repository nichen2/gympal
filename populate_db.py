import os
import requests
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from app import app, db  
from models import Exercise  

# Load environment variables from .env file
load_dotenv()

# Define your muscle groups
muscle_groups = [
    "abdominals", "abductors", "adductors", "biceps", "calves",
    "chest", "forearms", "glutes", "hamstrings", "lats",
    "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"
]

def fetch_exercises_for_muscle(api_key, muscle):
    api_url = 'https://api.api-ninjas.com/v1/exercises'
    params = {'muscle': muscle, 'offset': 20}
    response = requests.get(api_url, headers={'X-Api-Key': api_key}, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching exercises for {muscle}: {response.text}")
        return []

def populate_exercises(api_key):
    with app.app_context():
        for muscle in muscle_groups:
            exercises = fetch_exercises_for_muscle(api_key, muscle)
            for exercise_data in exercises:
                new_exercise = Exercise(
                    name=exercise_data['name'],
                    type=exercise_data['type'],
                    muscle=exercise_data['muscle'],
                    difficulty=exercise_data['difficulty'],
                    instructions=exercise_data['instructions'],
                )
                db.session.add(new_exercise)
        db.session.commit()

if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API key not found. Ensure API_KEY is set in .env.")
    populate_exercises(api_key)
