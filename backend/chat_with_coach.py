import json
from llm_client import query_llm
from financial_analysis import get_user_financial_summary
from goal_tracker import get_user_goals

# -----------------------------
# Helpers
# -----------------------------
def format_goals_for_prompt(goals: list[dict]) -> str:
    if not goals:
        return "No active savings goals."

    lines = []
    for g in goals:
        monthly_required = g["target_amount"] / g["duration_months"]
        lines.append(
            f"- {g['description']}: "
            f"${g['target_amount']} over {g['duration_months']} months "
            f"(~${monthly_required:.2f}/month)"
        )
    return "\n".join(lines)


def build_system_prompt(user_id: str) -> str:
    """
    Single source of truth for the finance coach system prompt.
    """
    metrics = get_user_financial_summary(user_id)
    goals = get_user_goals(user_id)
    formatted_goals = format_goals_for_prompt(goals)

    return f"""
You are a friendly personal finance coach.

Rules:
- Be conversational, concise, and helpful.
- If the user says "Hi" or "Hello", respond with a short greeting of "Hello! I'm your Personal Finance Coach. What can I help you with?"
- Do not repeat greetings after every user message.
- Treat all provided transactions, income, spending, and goals as real and accurate.
- Only provide analysis when explicitly asked.
- Avoid structured headers or lists unless requested.
- Use only the numbers provided; do not hallucinate.
- If you don’t have an answer, say so.

Use this JSON-like structured data to answer questions:

USER METRICS:
{json.dumps(metrics, indent=2, default=str)}

USER SAVINGS GOALS:
{formatted_goals}
"""


def query_coach(user_id: str, user_message: str) -> str:
    """
    High-level helper used by FastAPI.
    """
    system_prompt = build_system_prompt(user_id)
    prompt = system_prompt + f"\nUser question: {user_message}\nCoach reply:"

    response = query_llm(prompt)
    return response.strip()
