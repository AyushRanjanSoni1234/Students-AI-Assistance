from sources.model.model import LLM_Model
from sources.logger import logging
from sources.exception import CustomException
from sources.utils import clean_text, extract_json, validate_quiz
import sys

llm = LLM_Model()
logging.info("Assessment agent initialized successfully")


def assessment_agent(state):
    try:
        logging.info("Assessment agent called")

        subject = state.get("subject", "general")
        topics = state.get("topics", [])
        num_q = state.get("num_questions", 5)
        level = state.get("level", "beginner")

        # -------------------------
        # Prompt
        # -------------------------
        prompt = f"""
        Create {num_q} {level} level MCQ questions on {subject}.

        Topics: {topics}

        Strictly return ONLY JSON array in this format:
        [
        {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "topic": "..."
        }}
        ]
        """

        # -------------------------
        # LLM Call
        # -------------------------
        raw_output = llm.generate_response(prompt).content

        # -------------------------
        # Step 1: Clean text
        # -------------------------
        cleaned = clean_text(raw_output)

        # -------------------------
        # Step 2: Extract JSON
        # -------------------------
        extracted = extract_json(cleaned)

        # -------------------------
        # Step 3: Validate Quiz
        # -------------------------
        quiz = validate_quiz(extracted)

        logging.info("Assessment agent completed successfully")

        return {"quiz": quiz}

    except Exception as e:
        logging.error("Error in assessment agent")
        raise CustomException(e, sys)