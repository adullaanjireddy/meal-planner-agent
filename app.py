import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_URL = os.getenv("FLASK_URL", "http://127.0.0.1:5000")

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


# ---------------- API CALL ----------------
def call_flask(endpoint, payload):
    try:
        res = requests.post(f"{FLASK_URL}/{endpoint}", json=payload, timeout=60)
        return res.json()
    except:
        return {"success": False, "error": "Flask backend not running"}


# ---------------- HEADER ----------------
st.title("🍽️ AI Meal Planner")
st.caption("Smart meal planning · Budget-aware · Pantry-first")

# ---------------- BACKEND CHECK ----------------
try:
    requests.get(f"{FLASK_URL}/health")
except:
    st.error("⚠️ Flask not running. Run backend/app.py first")
    st.stop()

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
            res = call_flask("generate-plan", {
                "pantry": pantry_list,
                "budget": budget,
                "dietary": dietary
            })

        if res.get("success"):
            st.session_state["plan"] = res["plan"]

            # ✅ NEW: store cost + nutrition
            st.session_state["cost"] = res.get("cost", 0)
            st.session_state["calories"] = res.get("calories", 0)
            st.session_state["protein"] = res.get("protein", 0)

            st.success("Meal Plan Generated")
        else:
            st.error(res.get("error"))

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📅 Meal Plan", "🛒 Shopping", "💬 Chat"])

# ---------------- MEAL PLAN ----------------
with tab1:
    if st.session_state["plan"]:
        st.write(st.session_state["plan"])

        # ✅ SHOW COST + NUTRITION
        st.subheader("📊 Nutrition & Cost")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Cost", f"Rs.{st.session_state['cost']}")

        with col2:
            st.metric("🔥 Calories", st.session_state["calories"])

        with col3:
            st.metric("💪 Protein (g)", st.session_state["protein"])

        st.subheader("🔄 Swap Meal")

        day = st.selectbox("Day", ["Monday","Tuesday","Wednesday"])
        meal_type = st.selectbox("Meal", ["Breakfast","Lunch","Dinner"])
        reason = st.text_input("Reason")

        if st.button("Swap"):
            res = call_flask("swap-meal", {
                "day": day,
                "meal_type": meal_type,
                "reason": reason,
                "pantry": st.session_state["pantry"],
                "dietary": st.session_state["dietary"]
            })

            if res.get("success"):
                st.write(res["suggestions"])
            else:
                st.error(res.get("error"))
    else:
        st.info("Generate plan first")

# ---------------- SHOPPING ----------------
with tab2:
    if st.session_state["plan"]:

        if st.button("Generate Shopping List"):
            res = call_flask("shopping-list", {
                "plan": st.session_state["plan"],
                "pantry": st.session_state["pantry"],
                "budget": st.session_state["budget"]
            })

            if res.get("success"):
                st.session_state["shopping_list"] = res["shopping_list"]
            else:
                st.error(res.get("error"))

        if st.session_state["shopping_list"]:
            st.write(st.session_state["shopping_list"])
    else:
        st.info("Generate plan first")

# ---------------- CHAT ----------------
with tab3:
    question = st.text_input("Ask something")

    if st.button("Ask"):
        res = call_flask("ask", {
            "question": question,
            "plan_context": st.session_state["plan"] or ""
        })

        if res.get("success"):
            st.write(res["answer"])
        else:
            st.error(res.get("error"))