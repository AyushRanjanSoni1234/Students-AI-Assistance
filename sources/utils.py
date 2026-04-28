import json
import re


# -------------------------
# Clean LLM Text
# -------------------------
def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.strip().replace("\n\n", "\n")


# -------------------------
# Extract JSON from messy LLM output
# -------------------------
def extract_json(text: str):
    try:
        # Try JSON array first
        array_match = re.search(r"\[.*\]", text, re.DOTALL)
        if array_match:
            return json.loads(array_match.group())

        # Try JSON object
        obj_match = re.search(r"\{.*\}", text, re.DOTALL)
        if obj_match:
            return json.loads(obj_match.group())

    except Exception:
        pass

    return None


# -------------------------
# Safe JSON load (fallback)
# -------------------------
def safe_json_loads(text, default=None):
    try:
        return json.loads(text)
    except Exception:
        return default if default is not None else []


# -------------------------
# Validate Quiz Structure
# -------------------------
def validate_quiz(data):
    """
    Ensure quiz is always a list of valid dicts
    """
    if not isinstance(data, list):
        return []

    valid_quiz = []

    for q in data:
        if (
            isinstance(q, dict)
            and "question" in q
            and "options" in q
            and isinstance(q["options"], list)
            and "answer" in q
        ):
            valid_quiz.append({
                "question": q["question"],
                "options": q["options"],
                "answer": q["answer"],
                "topic": q.get("topic", "general")
            })

    return valid_quiz


# -------------------------
# Score Calculation
# -------------------------
def calculate_score(attempts):
    if not attempts:
        return 0

    correct = sum(1 for a in attempts if a.get("correct"))
    return (correct / len(attempts)) * 100


# -------------------------
# Weak Topics
# -------------------------
def get_weak_topics(attempts):
    return list(set(
        a.get("topic", "general")
        for a in attempts
        if not a.get("correct")
    ))