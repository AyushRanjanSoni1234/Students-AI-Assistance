from sources.logger import logging
from sources.exception import CustomException
import sys

logging.info("Analytics agent initialized successfully")

def analytics_agent(state):
    try:
        logging.info("Analytics agent called")
        attempts = state["quiz_attempts"]

        total = len(attempts)
        correct = sum(1 for a in attempts if a["correct"])

        score = (correct / total) * 100 if total > 0 else 0

        weak_topics = [a["topic"] for a in attempts if not a["correct"]]

        feedback = f"""
        Your Score: {score:.2f}%

        Strengths:
        - Good understanding of correct answers

        Weak Areas:
        - {set(weak_topics)}

        Recommendation:
        Practice weak topics and retry quiz.
        """

        return {
            "score": score,
            "feedback": feedback
        }

        logging.info("Analytics agent completed successfully")

    except Exception as e:
        logging.error("Error in analytics agent")
        raise CustomException(e, sys)
