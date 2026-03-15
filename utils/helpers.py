import re
from datetime import datetime


def parse_pantry_input(raw_text: str) -> list:
    items = [line.strip().lower() for line in raw_text.split("\n") if line.strip()]
    seen = set()
    unique = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def format_budget(amount: float) -> str:
    return f"${amount:,.2f}"


def estimate_cost_per_serving(total_budget: float, days: int = 7, meals_per_day: int = 3, people: int = 2) -> float:
    total_servings = days * meals_per_day * people
    return round(total_budget / total_servings, 2)


def get_day_name(day_index: int) -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[day_index % 7]


def get_week_dates() -> list:
    from datetime import timedelta
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%A, %b %d") for i in range(7)]


def truncate_text(text: str, max_chars: int = 500) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def validate_api_keys(groq_key: str) -> dict:
    result = {"groq": False, "warnings": []}
    if groq_key and groq_key.startswith("gsk_") and len(groq_key) > 20:
        result["groq"] = True
    else:
        result["warnings"].append("Groq API key looks invalid or missing.")
    return result