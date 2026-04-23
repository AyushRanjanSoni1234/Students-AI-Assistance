from sources.model.model import LLM_Model
import json
from sources.logger import logging
from sources.exception import CustomException
import sys


llm = LLM_Model()

logging.info("Intent agent initialized successfully")


def intent_agent(state):
    try:
        logging.info("Intent agent called")
        user_input = state["input"]

        prompt = f"""
        Analyze the user request and extract:
    1. intent (quiz / learn / feedback)
    2. subject (python, math, science, etc.)
    3. number_of_questions (if quiz)

    Return JSON:
    {{
      "intent": "...",
      "subject": "...",
      "num_questions": 5
    }}

    User Input: {user_input}
    """

        response = llm.generate_response(prompt).content

        try:
            parsed = json.loads(response)
        except:
            parsed = {
            "intent": "quiz",
            "subject": "general",
            "num_questions": 5
        }

        logging.info("Intent agent completed successfully")
        return parsed
    except Exception as e:
        logging.error("Error in intent agent")
        raise CustomException(e, sys)