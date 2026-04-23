from sources.model.model import LLM_Model
from sources.logger import logging
from sources.exception import CustomException
import sys


llm = LLM_Model()

logging.info("Tutor agent initialized successfully")

def tutor_agent(state):
    try:
        logging.info("Tutor agent called")
        topic = state["weak_topic"]
        subject = state["subject"]

        prompt = f"""
    Explain {topic} in {subject} in a simple way with examples.
    """

        explanation = llm.generate_response(prompt).content

        logging.info("Tutor agent completed successfully")
        return {"explanation": explanation}

    except Exception as e:
        logging.error("Error in tutor agent")
        raise CustomException(e, sys)