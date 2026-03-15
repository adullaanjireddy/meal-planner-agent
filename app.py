import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_URL = os.getenv("FLASK_URL", "http://localhost:5000")

st.set_page_config(
    page_title="🍽️ AI Meal Planner",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 12px;
        text-align: center; color: white; margin-bottom: 2rem;
    }
    .main-header h1 { margin: 0; font-size: 2.5rem; }
    .main-header p  { margin: 0.5rem 0 0; opacity: 0.9; font-size: 1.1rem; }
    .stat-card {
        background: white; border: 1px solid #e0e0e0;
        border-radius: 10px; padding: 1rem; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .stat-card h3 { color: #667eea; font-size: 1.8rem; margin: 0; }
    .stat-card p  { color: #666; font-size: 0.85rem; margin: 0; }
    .plan-box {
        background: #f8f9ff; border-left: 4px solid #667eea;
        border-radius: 8px; padding: 1.5rem; margin: 1rem 0;
    }
    .shopping-box {
        background: #f0fff4; border-left: 4px solid #48bb78;
        border-radius: 8px; padding: 1.5rem;
    }
    .chat-box {
        background: #fffbf0; border-left: 4px solid #ed8936;
        border-radius: 8px; padding: 1rem; margin: 0.5rem 0;
    }
    div[data-testid="stButton"] button {
        border-radius: 8px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

for key, default in {
    "plan": None, "shopping_list": None, "pantry": [],
    "budget": 500, "dietary": [], "chat_history": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def call_flask(endpoint, payload):
    try:
        resp = requests.post(f"{FLASK_URL}/{endpoint}", json=payload, timeout=120)
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend. Is Flask running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_backend():
    try:
        return requests.get(f"{FLASK_URL}/health", timeout=5).status_code == 200
    except:
        return False


st.markdown("""
<div class="main-header">
    <h1>🍽️ AI Meal Planner</h1>
    <p>Smart meal planning · Budget-aware · Pantry-first</p>
</div>
""", unsafe_allow_html=True)

if not check_backend():
    st.error("⚠️ Flask backend is not reachable. Make sure Flask is running.")
    st.stop()

with st.sidebar:
    st.header("⚙️ Your Preferences")
    pantry_input = st.text_area(
        "🧺 Pantry Items (one per line)",
        placeholder="eggs\nchicken\nrice\ndal\nroti\npaneer\nonion\ngarlic",
        height=180
    )
    budget = st.slider("💰 Weekly Budget (₹)", 200, 5000, 1000, step=100)
    dietary = st.multiselect(
        "🥗 Dietary Restrictions",
        ["Vegetarian", "Vegan", "Jain", "Gluten-Free", "Dairy-Free",
         "Keto", "Halal", "Low-Sodium", "Low-Carb", "No Beef", "No Pork"]
    )
    household_size = st.number_input("👨‍👩‍👧 Number of people", min_value=1, max_value=10, value=2)
    st.divider()
    generate_btn = st.button("🚀 Generate Meal Plan", type="primary", use_container_width=True)
    if st.button("🔄 Clear Everything", use_container_width=True):
        for key in ["plan", "shopping_list", "chat_history"]:
            st.session_state[key] = None if key != "chat_history" else []
        st.rerun()

if generate_btn:
    pantry_list = [i.strip() for i in pantry_input.split("\n") if i.strip()]
    if not pantry_list:
        st.warning("Please add at least a few pantry items!")
    else:
        st.session_state.update({"pantry": pantry_list, "budget": budget, "dietary": dietary})
        with st.spinner("🤖 AI is crafting your personalized Indian meal plan..."):
            result = call_flask("generate-plan", {
                "pantry": pantry_list,
                "budget": budget,
                "dietary": dietary,
                "household_size": household_size,
            })
        if result.get("success"):
            st.session_state["plan"] = result["plan"]
            st.session_state["shopping_list"] = None
            st.success("✅ Meal plan generated!")
        else:
            st.error(f"❌ Error: {result.get('error')}")

tab1, tab2, tab3 = st.tabs(["📅 Meal Plan", "🛒 Shopping List", "💬 Ask the Agent"])

with tab1:
    if st.session_state["plan"]:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="stat-card"><h3>{len(st.session_state["pantry"])}</h3><p>Pantry Items</p></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-card"><h3>₹{st.session_state["budget"]}</h3><p>Weekly Budget</p></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-card"><h3>{len(st.session_state["dietary"])}</h3><p>Diet Filters</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="plan-box">', unsafe_allow_html=True)
        st.markdown(st.session_state["plan"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("🔄 Swap a Meal")
        col_a, col_b, col_c = st.columns(3)
        with col_a: swap_day = st.selectbox("Day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        with col_b: swap_meal_type = st.selectbox("Meal", ["Breakfast","Lunch","Dinner","Snack"])
        with col_c: swap_reason = st.text_input("Reason (optional)", placeholder="Don't like this meal...")

        if st.button("🔄 Get Alternatives"):
            with st.spinner("Finding alternatives..."):
                result = call_flask("swap-meal", {
                    "day": swap_day,
                    "meal_type": swap_meal_type,
                    "reason": swap_reason or "User preference",
                    "pantry": st.session_state["pantry"],
                    "dietary": st.session_state["dietary"],
                })
            if result.get("success"):
                st.markdown('<div class="plan-box">', unsafe_allow_html=True)
                st.markdown(result["suggestions"])
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(result.get("error"))
    else:
        st.info("👈 Fill in your preferences in the sidebar and click **Generate Meal Plan** to get started!")
        st.markdown("""
        ### How it works:
        1. **Add your pantry items** — ingredients you already have at home
        2. **Set your budget** — weekly grocery spending limit in ₹
        3. **Select dietary restrictions** — any food preferences or allergies
        4. **Generate** — AI creates a personalized 7-day Indian meal plan
        5. **Get your shopping list** — only what you actually need to buy
        """)

with tab2:
    if st.session_state["plan"]:
        if st.button("🛒 Generate Shopping List", type="primary"):
            with st.spinner("Building your shopping list..."):
                result = call_flask("shopping-list", {
                    "plan": st.session_state["plan"],
                    "pantry": st.session_state["pantry"],
                    "budget": st.session_state["budget"],
                })
            if result.get("success"):
                st.session_state["shopping_list"] = result["shopping_list"]
            else:
                st.error(result.get("error"))

        if st.session_state["shopping_list"]:
            st.markdown('<div class="shopping-box">', unsafe_allow_html=True)
            st.markdown(st.session_state["shopping_list"])
            st.markdown('</div>', unsafe_allow_html=True)
            st.download_button(
                "📥 Download Shopping List",
                data=st.session_state["shopping_list"],
                file_name="shopping_list.txt",
                mime="text/plain",
            )
    else:
        st.info("Generate a meal plan first, then come back here for your shopping list!")

with tab3:
    st.subheader("💬 Ask the Meal Planning Agent")
    st.caption("Ask anything about your meal plan, nutrition, substitutions, cooking tips, etc.")

    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-box">🧑 **You:** {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="plan-box">🤖 **Agent:** {msg["content"]}</div>', unsafe_allow_html=True)

    user_question = st.text_input(
        "Your question",
        placeholder="What can I cook with leftover dal? How much protein is in Day 3?",
        key="chat_input"
    )
    col1, col2 = st.columns([3, 1])
    with col1: ask_btn = st.button("💬 Ask", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

    if ask_btn and user_question:
        with st.spinner("Thinking..."):
            result = call_flask("ask", {
                "question": user_question,
                "plan_context": st.session_state["plan"] or "No plan yet."
            })
        if result.get("success"):
            st.session_state["chat_history"].append({"role": "user", "content": user_question})
            st.session_state["chat_history"].append({"role": "assistant", "content": result["answer"]})
            st.rerun()
        else:
            st.error(result.get("error"))

    if not st.session_state["plan"]:
        st.info("💡 Generate a meal plan first for more relevant answers!")

st.divider()
st.markdown(
    '<div style="text-align:center;color:#999;font-size:0.85rem;">🍽️ AI Meal Planner</div>',
    unsafe_allow_html=True
)
