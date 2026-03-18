import streamlit as st
from backend.agent import MealPlannerAgent

agent = MealPlannerAgent()

st.set_page_config(
    page_title="🍽️ AI Meal Planner",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
for key, default in {
    "plan": None,
    "shopping_list": None,
    "pantry": [],
    "budget": 1000,
    "dietary": [],
    "chat_history": [],
    "cost": 0,
    "calories": 0,
    "protein": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------- HEADER ----------------
st.title("🍽️ AI Meal Planner")
st.caption("Smart meal planning · Budget-aware · Pantry-first")


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Preferences")

    pantry_input = st.text_area(
        "🧺 Pantry Items (one per line)",
        placeholder="egg\nchicken\npaneer",
        height=150
    )

    budget = st.slider("💰 Budget (₹)", 200, 5000, 1000)

    dietary = st.multiselect(
        "🥗 Dietary",
        ["Vegetarian", "Vegan", "Keto", "Low-Carb"]
    )

    generate = st.button("🚀 Generate Plan")


# ---------------- GENERATE PLAN ----------------
if generate:
    pantry_list = [i.strip().lower() for i in pantry_input.split("\n") if i.strip()]

    if not pantry_list:
        st.warning("Add pantry items")
    else:
        st.session_state["pantry"] = pantry_list
        st.session_state["budget"] = budget
        st.session_state["dietary"] = dietary

        with st.spinner("Generating meal plan..."):
            plan = agent.generate_meal_plan(pantry_list, budget, dietary)

            # ✅ NEW: cost + nutrition
            cost = agent.calculate_cost(pantry_list)
            calories, protein = agent.calculate_nutrition(pantry_list)

        st.session_state["plan"] = plan
        st.session_state["cost"] = cost
        st.session_state["calories"] = calories
        st.session_state["protein"] = protein

        st.success("Meal Plan Generated")


# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📅 Meal Plan", "🛒 Shopping", "💬 Chat"])


# ---------------- MEAL PLAN ----------------
with tab1:
    if st.session_state["plan"]:
        st.write(st.session_state["plan"])

        # ✅ COST + NUTRITION
        st.subheader("📊 Nutrition & Cost")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Cost", f"Rs.{st.session_state['cost']}")

        with col2:
            st.metric("🔥 Calories", st.session_state["calories"])

        with col3:
            st.metric("💪 Protein (g)", st.session_state["protein"])

        # 🔄 Swap
        st.subheader("🔄 Swap Meal")

        day = st.selectbox("Day", ["Monday","Tuesday","Wednesday"])
        meal_type = st.selectbox("Meal", ["Breakfast","Lunch","Dinner"])
        reason = st.text_input("Reason")

        if st.button("Swap"):
            suggestions = agent.swap_meal(
                day, meal_type, reason,
                st.session_state["pantry"],
                st.session_state["dietary"]
            )
            st.write(suggestions)

    else:
        st.info("Generate plan first")


# ---------------- SHOPPING ----------------
with tab2:
    if st.session_state["plan"]:

        if st.button("Generate Shopping List"):
            shopping = agent.generate_shopping_list(
                st.session_state["plan"],
                st.session_state["pantry"],
                st.session_state["budget"]
            )
            st.session_state["shopping_list"] = shopping

        if st.session_state["shopping_list"]:
            st.write(st.session_state["shopping_list"])
    else:
        st.info("Generate plan first")


# ---------------- CHAT ----------------
with tab3:
    question = st.text_input("Ask something")

    if st.button("Ask"):
        answer = agent.answer_question(
            question,
            st.session_state["plan"] or ""
        )
        st.write(answer)