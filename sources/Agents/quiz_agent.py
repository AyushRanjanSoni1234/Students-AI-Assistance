from sources.model.model import LLM_Model
from sources.logger import logging
from sources.exception import CustomException
from sources.utils import clean_text, extract_json
import sys

llm = LLM_Model()

logging.info("Quiz agent initialized successfully")


def quiz_agent(state):
    try:
        subject = state.get("subject", "general")
        topic = state.get("weak_topic") or subject
        num_q = state.get("num_questions", 5)
        level = state.get("level", "medium")

        prompt = f"""
        Generate {num_q} MCQs on {topic} ({subject}) at {level} level.

        RULES:
        - Return ONLY JSON
        - options must be FULL TEXT (not A/B/C)
        - answer must match EXACT option text

        FORMAT:
        {{
          "quiz": [
            {{
              "question": "string",
              "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
              "answer": "Option 1",
              "topic": "{topic}"
            }}
          ]
        }}
        """

        raw = llm.generate_response(prompt).content
        cleaned = clean_text(raw)
        extracted = extract_json(cleaned)

        quiz = extracted.get("quiz", []) if isinstance(extracted, dict) else extracted

        if not isinstance(quiz, list) or not quiz:
            return fallback_quiz(topic, num_q)

        return {**state, "quiz": quiz[:num_q]}
        logging.info("Quiz agent completed successfully")

    except Exception as e:
        logging.error("Error in quiz agent")
        raise CustomException(e, sys)


# -------------------------
# Fallback Function
# -------------------------
def fallback_quiz(topic, num_q):
    logging.warning("Using fallback quiz")

    return {
        "quiz": [
            {
                "question": f"What is {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "Option A",
                "topic": topic
            }
            for _ in range(num_q)
        ]
    }