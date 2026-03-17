import os
import sys

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from backend.agent import MealPlannerAgent
from memory.user_profile import (
    load_profile,
    save_profile,
    save_plan,
    update_pantry,
    add_liked_meal,
    add_disliked_meal,
)

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
agent = MealPlannerAgent()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "meal-planner-flask"})


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.json
        pantry = data.get("pantry", [])
        budget = float(data.get("budget", 100))
        dietary = data.get("dietary", [])
        user_id = data.get("user_id", "default")

        update_pantry(pantry, user_id)
        plan = agent.generate_meal_plan(
            pantry=pantry,
            budget=budget,
            dietary=dietary,
            recipes=[],
            history=[]
        )
        save_plan(plan, user_id)

        return jsonify({"success": True, "plan": plan})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/shopping-list", methods=["POST"])
def shopping_list():
    try:
        data = request.json
        plan = data.get("plan", "")
        pantry = data.get("pantry", [])
        budget = float(data.get("budget", 100))

        if not plan:
            return jsonify({"success": False, "error": "No meal plan provided"}), 400

        shopping = agent.generate_shopping_list(plan, pantry, budget)
        return jsonify({"success": True, "shopping_list": shopping})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/swap-meal", methods=["POST"])
def swap_meal():
    try:
        data = request.json
        result = agent.swap_meal(
            data.get("day", ""),
            data.get("meal_type", ""),
            data.get("reason", ""),
            data.get("pantry", []),
            data.get("dietary", [])
        )
        return jsonify({"success": True, "suggestions": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask_agent():
    try:
        data = request.json
        question = data.get("question", "")
        if not question:
            return jsonify({"success": False, "error": "No question provided"}), 400

        answer = agent.answer_question(question, data.get("plan_context", ""))
        return jsonify({"success": True, "answer": answer})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/profile", methods=["GET"])
def get_profile():
    user_id = request.args.get("user_id", "default")
    return jsonify({"success": True, "profile": load_profile(user_id)})


@app.route("/profile/update", methods=["POST"])
def update_profile():
    try:
        data = request.json
        user_id = data.get("user_id", "default")
        profile = load_profile(user_id)
        for field in ["budget", "dietary", "household_size"]:
            if field in data:
                profile[field] = data[field]
        save_profile(profile, user_id)
        return jsonify({"success": True, "profile": profile})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.json
        meal = data.get("meal", "")
        user_id = data.get("user_id", "default")
        if data.get("liked", True):
            add_liked_meal(meal, user_id)
        else:
            add_disliked_meal(meal, user_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)