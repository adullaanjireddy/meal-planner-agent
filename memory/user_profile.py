import json
import os
from datetime import datetime

PROFILE_DIR = "memory/profiles"


def ensure_dir():
    os.makedirs(PROFILE_DIR, exist_ok=True)


def load_profile(user_id: str = "default") -> dict:
    ensure_dir()
    path = f"{PROFILE_DIR}/{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "user_id": user_id,
        "pantry": [],
        "budget": 100,
        "dietary": [],
        "household_size": 2,
        "liked_meals": [],
        "disliked_meals": [],
        "past_plans": [],
        "created_at": datetime.now().isoformat(),
    }


def save_profile(profile: dict, user_id: str = "default"):
    ensure_dir()
    path = f"{PROFILE_DIR}/{user_id}.json"
    profile["updated_at"] = datetime.now().isoformat()
    with open(path, "w") as f:
        json.dump(profile, f, indent=2)


def update_pantry(pantry: list, user_id: str = "default"):
    profile = load_profile(user_id)
    profile["pantry"] = pantry
    save_profile(profile, user_id)


def save_plan(plan: str, user_id: str = "default"):
    profile = load_profile(user_id)
    profile["past_plans"].append({
        "plan": plan,
        "saved_at": datetime.now().isoformat()
    })
    if len(profile["past_plans"]) > 5:
        profile["past_plans"] = profile["past_plans"][-5:]
    save_profile(profile, user_id)


def add_liked_meal(meal: str, user_id: str = "default"):
    profile = load_profile(user_id)
    if meal not in profile["liked_meals"]:
        profile["liked_meals"].append(meal)
    save_profile(profile, user_id)


def add_disliked_meal(meal: str, user_id: str = "default"):
    profile = load_profile(user_id)
    if meal not in profile["disliked_meals"]:
        profile["disliked_meals"].append(meal)
    save_profile(profile, user_id)