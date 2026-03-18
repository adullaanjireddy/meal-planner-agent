import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class MealPlannerAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.system_prompt = """You are an expert Indian meal planning assistant and nutritionist.
You help users plan delicious, practical Indian meals based on their pantry, budget, and dietary needs.
Always respond in simple Indian English.
Always use Indian Rupees with this symbol: Rs. for all prices. For example: Rs.10, Rs.20, Rs.30
Never use tilde symbol ~ anywhere in your response.
Never use strikethrough text anywhere in your response.
Always suggest popular Indian dishes like Dal, Rice, Roti, Sabzi, Biryani, Idli, Dosa, Paratha, Khichdi etc.
Keep meals balanced and nutritious with Indian cooking style.
Format clearly with emojis for readability.
Always be encouraging, practical, and budget-conscious."""

    def chat(self, messages: list) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "system", "content": self.system_prompt}] + messages
        )
        return response.choices[0].message.content

    def generate_meal_plan(self, pantry=[], budget=100, dietary=[], recipes=[], history=[]):
        dietary_str = ", ".join(dietary) if dietary else "None"
        pantry_str = ", ".join(pantry) if pantry else "Not specified"

        prompt = f"""Create a detailed 7-day Indian meal plan with STRICT constraints:

           Pantry Items Available: {pantry_str}
           Weekly Budget: Rs.{budget}
         Dietary Restrictions: {dietary_str}

         CRITICAL RULE (VERY IMPORTANT):
         - You MUST ONLY use these pantry items as the main ingredients: {pantry_str}
         - Do NOT generate meals like Idli, Dosa, Fruit Salad, or any dish that does NOT use these pantry items
         - Every meal MUST directly include at least one pantry item
         - You are allowed to add only basic supporting ingredients (rice, roti, spices, onion, tomato)
         - Do NOT introduce unrelated ingredients like fruits or completely different dishes

         Meal Planning Rules:
           1. Every meal must include at least one pantry item
           2. Stay within the weekly budget
          3. Respect dietary restrictions
           4. Keep meals simple, practical, and Indian-style
          5. Avoid repeating the same dish too often

         IMPORTANT RULES:
         - Never use tilde symbol ~ anywhere
         - Never use strikethrough text
         - Always write price like this: (Rs.10, 20 mins)

         Format each day exactly like this:
         Day 1 - Monday
         Breakfast: [Meal name] (Rs.X, XX mins)
         Lunch: [Meal name] (Rs.X, XX mins)
          Dinner: [Meal name] (Rs.X, XX mins)
          Snack: [Snack name] (Rs.X)
          Note: Mention which pantry item is used in each meal

         End with Weekly Cost Summary in Rs. and Top Tips for this week."""

        messages = history + [{"role": "user", "content": prompt}]
        return self.chat(messages)

    def generate_shopping_list(self, plan, pantry, budget):
        pantry_str = ", ".join(pantry) if pantry else "Nothing"
        prompt = f"""Based on this 7-day Indian meal plan:
{plan}

Already in pantry: {pantry_str}
Remaining budget for groceries: Rs.{budget}

Generate a shopping list with ONLY the missing ingredients.
Use Indian grocery terms and Rs. for prices.
Never use tilde symbol ~ anywhere.
Never use strikethrough text.

Format as:
Vegetables (Sabzi)
- Item: quantity (Rs.price)

Dairy (Dudh/Dahi)
- Item: quantity (Rs.price)

Meat/Protein (Gosht/Dal)
- Item: quantity (Rs.price)

Pantry and Dry Goods (Kirana)
- Item: quantity (Rs.price)

Estimated Total: Rs.XX
Money-Saving Tips: [2-3 tips for Indian grocery shopping]"""

        return self.chat([{"role": "user", "content": prompt}])

    def swap_meal(self, day, meal_type, reason, pantry, dietary, history=[]):
        prompt = f"""The user wants to swap their {meal_type} on {day}.
Reason: {reason}
Available pantry: {', '.join(pantry)}
Dietary restrictions: {', '.join(dietary) if dietary else 'None'}

Suggest 3 alternative Indian {meal_type} options.
Write price like this: (Rs.X, XX mins)
Never use tilde symbol ~ anywhere."""

        messages = history + [{"role": "user", "content": prompt}]
        return self.chat(messages)

    def answer_question(self, question, context, history=[]):
        prompt = f"""Context about the user's Indian meal plan:
{context}

User question: {question}

Please answer helpfully in simple Indian English.
Never use tilde symbol ~ anywhere.
Write prices like this: Rs.10"""

        messages = history + [{"role": "user", "content": prompt}]
        return self.chat(messages)