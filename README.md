# 🍽️ Meal Planner AI Agent

An AI-powered Meal Planner Agent that generates personalized meal plans based on user preferences, dietary needs, and available ingredients.
The system can also swap meals, generate shopping lists, and store user preferences and gives suggestions.

---

## 🚀 Features

* 🧠 AI-based meal plan generation (pantry items)
* 🔄 Swap meals dynamically
* 🛒 Generate shopping lists automatically
* 👤 Store user profiles and preferences
* 💾 Maintain memory of previous meals
* ⚡ Fast backend API for handling requests
* 🧠 It's gives a suggestions and you can also ask questions with agent.

---

## 🏗️ Project Structure

```
meal-planner-agent/
│
├── backend/
│   ├── __init__.py
│   ├──  nutrition.py             
│   ├── agent.py               # Core AI logic
│   ├── price.py 
│                
│   
│  
│
│
├── memory/
│   ├── __init__.py
│   ├── user_profile.py
│   ├── profiles/
│   │   └── default.json
│
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│
│
├── app.py                     # Streamlit frontend
│
├── requirements.txt
├── README.md
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── server.py
├── .env                       
└── venv                 
---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** (Frontend interface)
* **AI Agent logic**
* **Docker** (for containerization)
* **Git & GitHub** (version control)
* **groq API KEY**

---


## 🧠 How It Works

1. User enters dietary preferences and meal requirements.
2. The AI agent processes the request.
3. A personalized meal plan is generated.
4. Users can swap meals or request a shopping list.
5. The system stores preferences for future recommendations.


---

## 📌 Future Improvements

* Integration with nutrition APIs
* Advanced dietary recommendation system
* Voice-based meal planning assistant
* Cloud deployment

---
**Adulla Ramanjaneya Reddy**

AI / Data Science Enthusiast
Interested in learning and building machine learning and intelligent AI agents and real-world applications.