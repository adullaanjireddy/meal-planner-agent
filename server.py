from flask import Flask, request, jsonify
from backend.agent import MealPlannerAgent

app = Flask(__name__)
agent = MealPlannerAgent()


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.json

        pantry = data.get("pantry", [])
        budget = data.get("budget", 1000)
        dietary = data.get("dietary", [])

        plan = agent.generate_meal_plan(pantry, budget, dietary)

        cost = agent.calculate_cost(pantry)
        calories, protein = agent.calculate_nutrition(pantry)

        return jsonify({
            "success": True,
            "plan": plan,
            "cost": cost,
            "calories": calories,
            "protein": protein
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/shopping-list", methods=["POST"])
def shopping_list():
    data = request.json
    result = agent.generate_shopping_list(
        data.get("plan"),
        data.get("pantry"),
        data.get("budget")
    )
    return jsonify({"success": True, "shopping_list": result})


@app.route("/swap-meal", methods=["POST"])
def swap_meal():
    data = request.json
    result = agent.swap_meal(
        data.get("day"),
        data.get("meal_type"),
        data.get("reason"),
        data.get("pantry"),
        data.get("dietary")
    )
    return jsonify({"success": True, "suggestions": result})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    result = agent.answer_question(
        data.get("question"),
        data.get("plan_context")
    )
    return jsonify({"success": True, "answer": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
