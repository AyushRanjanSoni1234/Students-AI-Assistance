from sources.model.model import LLM_Model
from sources.logger import logging
from sources.exception import CustomException
import sys

llm = LLM_Model()
logging.info("Assessment agent initialized successfully")

def assessment_agent(state):
    try:
        logging.info("Assessment agent called")
        subject = state["subject"]
        topics = state["topics"]
        num_q = state.get("num_questions", 5)
        level = state.get("level", "beginner")

        prompt = f"""
        Create {num_q} {level} level MCQ questions on {subject}.

        Topics: {topics}

        Return JSON format:
        [
        {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "A",
            "topic": "..."
        }}
        ]
        """

        quiz = llm.generate_response(prompt).content

        logging.info("Assessment agent completed successfully")
        return {"quiz": quiz}

    except Exception as e:
        logging.error("Error in assessment agent")
        raise CustomException(e, sys)