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
        You are an Intent Detection Agent.

        Your task is to analyze user input and extract structured information.

        Input:
        "{user_input}"

        ----------------------
        Instructions:
        ----------------------
        1. Identify user intent:
        - "learn" → user wants to study or understand something
        - "quiz" → user wants questions or test

        2. Extract subject exactly as mentioned.

        3. Extract:
        - num_questions → ONLY if intent = "quiz"
        - difficulty → if mentioned, else default = "medium"

        4. Defaults:
        - intent → "learn" if unclear
        - subject → "general"
        - num_questions → 5 (only for quiz)
        - level → "medium"

        ----------------------
        Rules:
        ----------------------
        - Do NOT guess missing information unnecessarily
        - Do NOT add extra text
        - Return ONLY valid JSON
        - No explanations

        ----------------------
        Output Format:
        ----------------------
        {{
        "intent": "learn" or "quiz",
        "subject": "string",
        "num_questions": number,
        "level": "easy" or "medium" or "hard" or "beginner" or "intermediate" or "advanced"
        }}
        """
        raw = llm.generate_response(prompt).content
        cleaned = clean_text(raw)
        extracted = extract_json(cleaned)
    
        intent = (extracted or {}).get("intent", "learn")
        subject = (extracted or {}).get("subject", "general")
        
        if intent == "quiz":
            num_q = (extracted or {}).get("num_questions", 5)
            level = (extracted or {}).get("level", "medium")
        elif intent == "learn":
            num_q = None 
            level = (extracted or {}).get("level", "medium")

        logging.info("Intent agent completed successfully")

        return {
            "intent": intent,
            "subject": subject,
            "num_questions": num_q,
            "level": level
        }

    except Exception as e:
        logging.error("Error in intent agent")
        raise CustomException(e, sys)