import os
from groq import Groq
from dotenv import load_dotenv

# Correct imports
from backend.price import PRICES
from backend.nutrition import NUTRITION

# Load environment variables
load_dotenv()


class MealPlannerAgent:
    def __init__(self):
        # Initialize Groq client
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Model
        self.model = "llama-3.3-70b-versatile"

        # System prompt
        self.system_prompt = """You are an expert Indian meal planning assistant and nutritionist.
You help users plan meals based on pantry, budget, and dietary needs.

Rules:
- Respond in simple Indian English
- Use Rs. for prices (example: Rs.10)
- Do NOT use ~ symbol
- Do NOT include unrelated foods outside pantry
- Always keep meals practical and home-style
"""

    # ---------------- CHAT FUNCTION ----------------
    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "system", "content": self.system_prompt}] + messages
        )
        return response.choices[0].message.content

    # ---------------- MEAL PLAN ----------------
    def generate_meal_plan(self, pantry=[], budget=100, dietary=[]):

        pantry_str = ", ".join(pantry) if pantry else "Not specified"
        dietary_str = ", ".join(dietary) if dietary else "None"

        prompt = f"""
Create a 7-day Indian meal plan.

Pantry Items: {pantry_str}
Budget: Rs.{budget}
Dietary Restrictions: {dietary_str}

STRICT RULES:
- ONLY use these pantry items: {pantry_str}
- Every meal MUST include at least one pantry item
- Do NOT include foods like idli, dosa, fruits if not in pantry
- You can use basic items like rice, roti, onion, tomato

Format:
Day 1 - Monday
Breakfast: Meal (Rs.X, XX mins)
Lunch: Meal (Rs.X, XX mins)
Dinner: Meal (Rs.X, XX mins)
Snack: Snack (Rs.X)
"""

        return self.chat([{"role": "user", "content": prompt}])

    # ---------------- SHOPPING LIST ----------------
    def generate_shopping_list(self, plan, pantry, budget):

        pantry_str = ", ".join(pantry) if pantry else "Nothing"

        prompt = f"""
Based on this meal plan:
{plan}

Already in pantry: {pantry_str}
Budget left: Rs.{budget}

Generate ONLY missing ingredients.

Format:
Vegetables:
- item (Rs.price)

Dairy:
- item (Rs.price)

Estimated Total: Rs.XXX
"""

        return self.chat([{"role": "user", "content": prompt}])

    # ---------------- SWAP MEAL ----------------
    def swap_meal(self, day, meal_type, reason, pantry, dietary):

        prompt = f"""
User wants to change {meal_type} on {day}
Reason: {reason}

Pantry: {', '.join(pantry)}
Dietary: {', '.join(dietary) if dietary else 'None'}

Suggest 3 alternative meals.
Each must use pantry items.
Write price like (Rs.X, XX mins)
"""

        return self.chat([{"role": "user", "content": prompt}])

    # ---------------- ASK QUESTION ----------------
    def answer_question(self, question, context):

        prompt = f"""
Meal Plan Context:
{context}

User Question: {question}

Answer clearly in simple Indian English.
Use Rs. for prices.
"""

        return self.chat([{"role": "user", "content": prompt}])

    # ---------------- COST CALCULATION ----------------
    def calculate_cost(self, pantry):
        total = 0
        for item in pantry:
            if item in PRICES:
                total += PRICES[item]
        return total

    # ---------------- NUTRITION CALCULATION ----------------
    def calculate_nutrition(self, pantry):
        calories = 0
        protein = 0

        for item in pantry:
            if item in NUTRITION:
                calories += NUTRITION[item]["calories"]
                protein += NUTRITION[item]["protein"]

        return calories, protein
