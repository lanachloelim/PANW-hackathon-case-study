from typing import List
import json
import os

GOALS_FILE = "data/goals.json"

# Ensure goals file exists
if not os.path.exists(GOALS_FILE):
    with open(GOALS_FILE, "w") as f:
        json.dump({}, f)

def get_user_goals(user_id: str) -> List[dict]:
    with open(GOALS_FILE, "r") as f:
        data = json.load(f)
    return data.get(user_id, [])

def add_goal(user_id: str, target_amount: float, duration_months: int, description: str = "Savings goal") -> dict:
    goal = {
        "description": description,
        "target_amount": target_amount,
        "duration_months": duration_months
    }
    data = {}
    with open(GOALS_FILE, "r") as f:
        data = json.load(f)
    if user_id not in data:
        data[user_id] = []
    data[user_id].append(goal)
    with open(GOALS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return goal
