from sources.model.model import LLM_Model
from sources.logger import logging
from sources.exception import CustomException
from sources.utils import clean_text, extract_json
import sys

llm = LLM_Model()

logging.info("Intent agent initialized successfully")


def intent_agent(state):
    try:
        logging.info("Intent agent called")

        user_input = state.get("input", "")

        # -------------------------
        # Prompt
        # -------------------------
        prompt = f"""
        You are an AI system that extracts structured data.

        Input: "{user_input}"

        Rules:
        - Identify intent: "quiz" or "learn"
        - Extract subject exactly as mentioned
        - Extract number of questions (default = 5 if not mentioned)

        Return ONLY JSON:
        {{
            "intent": "...",
            "subject": "...",
            "num_questions": ...
        }}
        """

        # -------------------------
        # LLM Call
        # -------------------------
        raw_output = llm.generate_response(prompt).content

        # -------------------------
        # Clean + Extract JSON
        # -------------------------
        cleaned = clean_text(raw_output)
        extracted = extract_json(cleaned)

        # -------------------------
        # Safe fallback
        # -------------------------
        if not extracted:
            logging.warning("Intent extraction failed, using defaults")
            return {
                "intent": "quiz",
                "subject": "general",
                "num_questions": 5
            }

        intent = extracted.get("intent", "quiz")
        subject = extracted.get("subject", "general")
        num_q = extracted.get("num_questions", 5)

        logging.info("Intent agent completed successfully")

        return {
            "intent": intent,
            "subject": subject,
            "num_questions": num_q
        }

    except Exception as e:
        logging.error("Error in intent agent")
        raise CustomException(e, sys)